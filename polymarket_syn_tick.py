#!/usr/bin/env python3
"""
polymarket_syn_tick.py — SYN orchestrator for 15 autonomous Polymarket bots.

SYN is the manager. Each tick:
  1. Fetches ALL data once (Polymarket, Kalshi, Metaculus, Manifold)
  2. Distributes pre-filtered candidates to each specialist bot
  3. Runs Gemini once per unique market (deduplicated across bots)
  4. Arb bots skip Gemini — pure price-gap math
  5. Executes trades, manages sprints, writes dashboard
"""
import json, os, re, time, logging, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta
from copy import deepcopy

# ── Paths ──────────────────────────────────────────────────────────────────
WORKSPACE        = "/root/.openclaw/workspace"
AUTO_STATE_FILE  = f"{WORKSPACE}/competition/polymarket/auto_state.json"
RESULTS_DIR      = f"{WORKSPACE}/competition/polymarket/auto_results"
FLEET_DIR        = f"{WORKSPACE}/fleet/polymarket"
DASH_OUTPUT      = "/var/www/dashboard/api/polymarket_auto.json"
LOG_FILE         = f"{WORKSPACE}/competition/polymarket/syn_tick.log"
CYCLE_STATE_FILE = f"{WORKSPACE}/competition/polymarket/polymarket_cycle_state.json"
BOT_TOKEN        = None  # loaded from TELEGRAM_SECRET at startup
CHAT_ID          = None
GEMINI_SECRET    = "/root/.openclaw/secrets/gemini.json"
KALSHI_SECRET    = "/root/.openclaw/secrets/kalshi.json"
TELEGRAM_SECRET  = "/root/.openclaw/secrets/telegram.json"

# ── Tuning ─────────────────────────────────────────────────────────────────
POLL_SEC             = 900    # 15 min between ticks
SCAN_EVERY           = 2      # scan new markets every 2nd tick (30 min)
MAX_GEMINI_PER_TICK  = 12     # total Gemini calls per tick (4 per key × 3 keys)
GEMINI_SLEEP         = 6      # seconds between Gemini calls
GEMINI_DAILY_LIMIT   = 1200   # per-key hard stop (1200 × 3 keys = 3600/day; actual use: 384/key/day)
GEMINI_CACHE_TTL_H   = 4      # reuse assessment if < 4h old and price unchanged
GEMINI_CACHE_DELTA   = 0.02   # skip cache if PM price moved more than 2 cents
SPRINT_HOURS         = 168    # 7-day sprints


os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)
log = logging.getLogger(__name__)
CONF_RANK = {"low": 0, "medium": 1, "high": 2}


# ── HTTP helpers ───────────────────────────────────────────────────────────

def api_get(url, timeout=12):
    req = urllib.request.Request(
        url, headers={"User-Agent": "syn-polymarket/1.0", "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def api_post(url, payload, timeout=20):
    data = json.dumps(payload).encode()
    req  = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


# ── Secrets + strategies ───────────────────────────────────────────────────

def load_secrets():
    global BOT_TOKEN, CHAT_ID
    with open(GEMINI_SECRET) as f:
        g = json.load(f)
    kalshi_key = None
    if os.path.isfile(KALSHI_SECRET):
        with open(KALSHI_SECRET) as f:
            k = json.load(f)
            kalshi_key = k.get("kalshi_api_key")
    if os.path.isfile(TELEGRAM_SECRET):
        with open(TELEGRAM_SECRET) as f:
            t = json.load(f)
            BOT_TOKEN = t.get("bot_token")
            CHAT_ID   = t.get("chat_id")
    else:
        log.warning(f"Telegram secret not found: {TELEGRAM_SECRET} — notifications disabled")
    # Support single key (legacy) or list of keys for rotation
    gemini_keys = g.get("gemini_api_keys") or [g["gemini_api_key"]]
    return {
        "gemini_api_key":  gemini_keys[0],
        "gemini_api_keys": gemini_keys,
        "kalshi_api_key":  kalshi_key,
    }


def load_all_strategies():
    """Load all strategy.yaml files from fleet/polymarket/*/strategy.yaml."""
    strategies = {}
    try:
        import yaml
        _yaml = yaml
    except ImportError:
        _yaml = None

    for bot_dir in os.listdir(FLEET_DIR):
        path = os.path.join(FLEET_DIR, bot_dir, "strategy.yaml")
        if not os.path.isfile(path):
            continue
        try:
            if _yaml:
                with open(path) as f:
                    s = _yaml.safe_load(f)
            else:
                s = _parse_yaml_simple(path)
            if s and s.get("name"):
                strategies[s["name"]] = s
        except Exception as e:
            log.warning(f"Failed to load strategy {path}: {e}")

    log.info(f"Loaded {len(strategies)} strategies: {sorted(strategies.keys())}")
    return strategies


def _parse_yaml_simple(path):
    """Minimal YAML parser for our flat strategy format (no PyYAML)."""
    import ast
    result, current_section, current_sub = {}, None, None
    with open(path) as f:
        for line in f:
            line = line.rstrip()
            if not line or line.strip().startswith("#"):
                continue
            indent = len(line) - len(line.lstrip())
            stripped = line.strip()

            if indent == 0 and ":" in stripped:
                k, _, v = stripped.partition(":")
                v = v.strip().strip('"')
                if v:
                    try:    result[k] = ast.literal_eval(v)
                    except: result[k] = v
                else:
                    current_section = k
                    result[k] = {}
                    current_sub = None
            elif indent == 2 and current_section:
                k, _, v = stripped.partition(":")
                v = v.strip().strip('"')
                if v:
                    try:    result[current_section][k] = ast.literal_eval(v)
                    except: result[current_section][k] = v
                else:
                    current_sub = k
                    result[current_section][k] = {}
            elif indent == 4 and current_section and current_sub:
                if stripped.startswith("- "):
                    val = stripped[2:].strip().strip('"')
                    lst = result[current_section].setdefault(current_sub, [])
                    if not isinstance(lst, list):
                        result[current_section][current_sub] = []
                    result[current_section][current_sub].append(val)
    return result


def load_state():
    with open(AUTO_STATE_FILE) as f:
        return json.load(f)


def save_state(state):
    state["generated_at"] = datetime.now(timezone.utc).isoformat()
    with open(AUTO_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# ── Data fetching (SYN pulls once per tick) ────────────────────────────────

def fetch_polymarket_markets(strategies):
    """Fetch all open Polymarket markets. SYN pulls once, bots filter locally."""
    markets, offset, limit = [], 0, 100
    # Collect all resolve windows needed across bots
    max_days = max(
        (s.get("market_filter", {}).get("max_days_to_resolve", 7)
         for s in strategies.values()), default=30
    )
    cutoff = datetime.now(timezone.utc) + timedelta(days=max_days)

    while True:
        try:
            url  = (f"https://gamma-api.polymarket.com/markets"
                    f"?closed=false&active=true&limit={limit}&offset={offset}")
            page = api_get(url, timeout=20)
        except Exception as e:
            log.warning(f"Polymarket fetch error (offset={offset}): {e}")
            break
        if not page:
            break

        for m in page:
            try:
                outcomes   = json.loads(m.get("outcomes", "[]"))
                out_prices = json.loads(m.get("outcomePrices", "[]"))
                if len(outcomes) < 2 or len(out_prices) < 2:
                    continue
                cid = m.get("conditionId", "")
                if not cid:
                    continue
                markets.append({
                    "condition_id": cid,
                    "title":        (m.get("question") or "").strip(),
                    "outcomes":     [{"outcome": outcomes[i], "price": float(out_prices[i])}
                                     for i in range(min(len(outcomes), len(out_prices)))],
                    "liquidity":    float(m.get("liquidity") or 0),
                    "end_date":     m.get("endDate") or m.get("end_date_iso") or "",
                })
            except Exception:
                continue

        if len(page) < limit:
            break
        offset += limit

    log.info(f"SYN fetched {len(markets)} Polymarket markets")
    return markets



def fetch_metaculus_markets():
    """Fetch open binary Metaculus questions with community predictions."""
    markets, offset, limit = [], 0, 100
    for _ in range(5):  # max 500 markets
        try:
            url  = (f"https://metaculus.com/api/questions/"
                    f"?status=open&type=binary&limit={limit}&offset={offset}&format=json")
            page = api_get(url, timeout=15)
            results = page.get("results", []) if isinstance(page, dict) else []
        except Exception as e:
            log.warning(f"Metaculus fetch error: {e}")
            break
        for q in results:
            pred = q.get("community_prediction") or {}
            full = pred.get("full") or {}
            prob = full.get("q2")  # median community prediction
            if prob is None:
                continue
            title = q.get("title") or q.get("question_text", "")
            if not title:
                continue
            markets.append({
                "id":       q.get("id"),
                "title":    title,
                "prob":     float(prob),
                "resolve":  q.get("resolve_time", ""),
            })
        if not results or len(results) < limit:
            break
        offset += limit

    log.info(f"SYN fetched {len(markets)} Metaculus questions")
    return markets


def fetch_kalshi_markets(kalshi_api_key=None):
    """Fetch Kalshi events with nested markets. No auth needed for public data."""
    markets = []
    cursor = None
    for _ in range(10):  # up to 2000 events
        try:
            url = ("https://api.elections.kalshi.com/trade-api/v2/events"
                   "?limit=200&with_nested_markets=true")
            if cursor:
                url += f"&cursor={cursor}"
            page = api_get(url, timeout=20)
        except Exception as e:
            log.warning(f"Kalshi fetch error: {e}")
            break
        for event in page.get("events", []):
            for m in event.get("markets", []):
                yes_bid = m.get("yes_bid_dollars")
                yes_ask = m.get("yes_ask_dollars")
                if yes_bid is None or yes_ask is None:
                    continue
                try:
                    bid = float(yes_bid)
                    ask = float(yes_ask)
                except (ValueError, TypeError):
                    continue
                if bid <= 0 or ask <= 0 or bid >= 1 or ask >= 1:
                    continue
                title = m.get("title", "") or event.get("title", "")
                if not title:
                    continue
                prob = (bid + ask) / 2  # 0-1 range
                markets.append({
                    "id":    m.get("ticker", ""),
                    "title": title,
                    "prob":  round(prob, 4),
                    "close": m.get("close_time", ""),
                })
        cursor = page.get("cursor")
        if not cursor or len(page.get("events", [])) < 200:
            break
    log.info(f"SYN fetched {len(markets)} Kalshi markets")
    return markets


def fetch_manifold_markets():
    """Fetch open binary Manifold markets with probability."""
    markets = []
    try:
        url  = "https://api.manifold.markets/v0/markets?limit=500"
        data = api_get(url, timeout=15)
        for m in data:
            if m.get("outcomeType") != "BINARY":
                continue
            if m.get("isResolved"):
                continue
            prob = m.get("probability")
            if prob is None:
                continue
            title = m.get("question", "")
            markets.append({
                "id":      m.get("id"),
                "title":   title,
                "prob":    float(prob),
                "close":   m.get("closeTime", ""),
            })
    except Exception as e:
        log.warning(f"Manifold fetch error: {e}")

    log.info(f"SYN fetched {len(markets)} Manifold markets")
    return markets


# ── Market matching ────────────────────────────────────────────────────────

STOP_WORDS = {"will","the","a","an","of","in","on","at","to","for","is","are",
              "be","has","have","by","or","and","vs","vs.","who","what","when",
              "how","does","do","can","could","would","should","may","might"}

def _tokens(text):
    words = re.sub(r"[^a-z0-9 ]", " ", text.lower()).split()
    return set(w for w in words if w not in STOP_WORDS and len(w) > 2)


def title_similarity(a, b):
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def build_title_index(markets):
    """Build inverted token index for O(1) candidate lookup."""
    index = {}
    for i, m in enumerate(markets):
        for tok in _tokens(m["title"]):
            index.setdefault(tok, []).append(i)
    return index


def find_best_external_match(pm_title, external_markets, min_score=0.25, index=None):
    """Find best matching external market by title similarity.
    Pass index for fast lookup (built with build_title_index)."""
    pm_toks = _tokens(pm_title)
    if not pm_toks:
        return None

    if index is not None:
        # Fast path: only score candidates sharing >=1 token
        cand_indices = set()
        for tok in pm_toks:
            cand_indices.update(index.get(tok, []))
        candidates = [external_markets[i] for i in cand_indices]
    else:
        candidates = external_markets

    best, best_score = None, min_score
    for m in candidates:
        score = title_similarity(pm_title, m["title"])
        if score > best_score:
            best, best_score = m, score
    return best


def _team_tokens(text):
    return set(re.sub(r"[^a-z0-9 ]", "", text.lower()).split())




# ── Bot candidate filtering ────────────────────────────────────────────────

def filter_for_bot(markets, strategy, existing_cids):
    """Return markets matching this bot's filter criteria."""
    mf      = strategy.get("market_filter", {})
    inc_kw  = [k.lower() for k in mf.get("include_keywords", [])]
    exc_kw  = [k.lower() for k in mf.get("exclude_keywords", [])]
    pr      = mf.get("price_range", [0.05, 0.95])
    min_liq = mf.get("min_liquidity_usd", 200)
    max_days= mf.get("max_days_to_resolve", 30)
    cutoff  = datetime.now(timezone.utc) + timedelta(days=max_days)

    candidates = []
    for m in markets:
        cid = m["condition_id"]
        if cid in existing_cids:
            continue
        title_lower = m["title"].lower()

        # Keyword filters
        if inc_kw and not any(k in title_lower for k in inc_kw):
            continue
        if any(k in title_lower for k in exc_kw):
            continue

        # Liquidity
        if m["liquidity"] < min_liq:
            continue

        # End date
        if m["end_date"]:
            try:
                end_dt = datetime.fromisoformat(m["end_date"].replace("Z", "+00:00"))
                if end_dt > cutoff or end_dt < datetime.now(timezone.utc):
                    continue
            except Exception:
                pass

        # Price range — check the cheaper outcome
        prices = sorted(o["price"] for o in m["outcomes"])
        if not prices or prices[0] < pr[0] or prices[0] > pr[1]:
            continue

        candidates.append(m)

    return candidates


# ── Gemini reasoning ───────────────────────────────────────────────────────

def gemini_assess(title, outcome, pm_price, kalshi_match, persona, api_key):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if kalshi_match:
        ref_section = (f"Kalshi market consensus:\n"
                       f"  '{kalshi_match['title']}': {kalshi_match['prob']:.1%}")
    else:
        ref_section = "No external reference available — use your own assessment only."

    prompt = (
        f"{persona}\n\n"
        f"Assess this Polymarket prediction market:\n"
        f"Market: {title}\n"
        f"Outcome assessed: {outcome}\n"
        f"Polymarket price: {pm_price:.3f} (implies {pm_price*100:.1f}% probability)\n"
        f"{ref_section}\n"
        f"Today: {today}\n\n"
        f"Estimate the TRUE probability considering all relevant factors. "
        f"Respond ONLY with valid JSON:\n"
        f'{"{"}"estimated_prob": 0.00, "confidence": "low|medium|high", '
        f'"value": "YES|NO|FAIR", "reasoning": "2 sentences max", '
        f'"key_factors": ["factor1", "factor2"]{"}"}\n\n'
        f'value=YES means Polymarket underprices this — take the position. '
        f'value=NO means Polymarket overprices it — skip. '
        f'value=FAIR means no edge.'
    )

    url     = (f"https://generativelanguage.googleapis.com/v1beta/models/"
               f"gemini-2.5-flash-lite:generateContent?key={api_key}")
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 150},
    }

    for attempt in range(2):
        try:
            resp = api_post(url, payload)
            text = resp["candidates"][0]["content"]["parts"][0]["text"].strip()
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
            result = json.loads(text)
            assert "estimated_prob" in result and "confidence" in result
            result["estimated_prob"] = float(result["estimated_prob"])
            return result
        except urllib.error.HTTPError as e:
            if e.code == 429:
                try:
                    err_body = json.loads(e.read().decode())
                    err_msg = err_body.get("error", {}).get("message", "")
                except Exception:
                    err_msg = ""
                # "quota" in message = daily quota exhausted → mark key exhausted
                # attempt 1 + no quota message = RPM persists → skip candidate only
                # attempt 0 + no quota message = RPM → wait 60s and retry
                if "quota" in err_msg.lower():
                    raise RuntimeError("GEMINI_KEY_EXHAUSTED")
                elif attempt == 1:
                    log.warning("Gemini 429 RPM persists on retry — skipping candidate")
                    return None
                else:
                    log.warning("Gemini 429 RPM — waiting 60s before retry")
                    time.sleep(60)
                    continue
            else:
                log.warning(f"Gemini HTTP {e.code}")
                return None
        except RuntimeError:
            raise
        except Exception as e:
            log.warning(f"Gemini error: {e}")
            if attempt == 0:
                continue  # retry once on parse/JSON errors
            return None
    return None


# ── Position management ────────────────────────────────────────────────────

def open_position(bot, market, outcome, price, reasoning, strategy):
    cid      = market["condition_id"]
    edge_cfg = strategy.get("edge", {})
    size_usd = round(bot["cash"] * edge_cfg.get("max_position_pct", 0.10), 2)
    max_pos  = edge_cfg.get("max_positions", 5)

    if size_usd < 1.0:
        return False
    if len(bot["positions"]) >= max_pos:
        return False
    if cid in bot["positions"]:
        return False

    shares = round(size_usd / price, 4)
    bot["cash"] = round(bot["cash"] - size_usd, 4)
    bot["positions"][cid] = {
        "condition_id":   cid,
        "title":          market["title"],
        "outcome":        outcome,
        "side":           "BUY",
        "entry_price":    price,
        "shares":         shares,
        "cost_usd":       size_usd,
        "current_price":  price,
        "current_value":  size_usd,
        "unrealized_pnl": 0.0,
        "opened_at":      datetime.now(timezone.utc).isoformat(),
        "reasoning":      reasoning[:200] if reasoning else "",
    }
    bot["total_trades"] += 1
    log.info(f"  [{bot['name']}] OPEN {outcome[:30]} @ {price:.3f} | ${size_usd:.0f} | {market['title'][:45]}")
    return True


def close_position(bot, cid, reason, final_price):
    pos = bot["positions"].get(cid)
    if not pos:
        return
    proceeds = round(pos["shares"] * final_price, 4)
    pnl      = round(proceeds - pos["cost_usd"], 4)
    pnl_pct  = round((pnl / pos["cost_usd"]) * 100, 2) if pos["cost_usd"] else 0
    bot["cash"] = round(bot["cash"] + proceeds, 4)
    if pnl >= 0:
        bot["wins"] += 1
    else:
        bot["losses"] += 1
    bot["closed_trades"].append({
        **pos,
        "closed_at":    datetime.now(timezone.utc).isoformat(),
        "exit_price":   final_price,
        "proceeds_usd": proceeds,
        "pnl_usd":      pnl,
        "pnl_pct":      pnl_pct,
        "reason":       reason,
    })
    del bot["positions"][cid]
    log.info(f"  [{bot['name']}] CLOSE {reason} @ {final_price:.3f} | PNL ${pnl:+.2f} ({pnl_pct:+.1f}%)")


def fetch_market_price(condition_id):
    try:
        url  = f"https://clob.polymarket.com/midpoints?conditionIds={condition_id}"
        data = api_get(url, timeout=5)
        val  = data.get("midpoints", {}).get(condition_id)
        return float(val) if val is not None else None
    except Exception:
        return None


def refresh_bot_positions(bot, markets_by_cid):
    """Update prices on open positions using cached market data, fall back to CLOB."""
    for cid in list(bot["positions"].keys()):
        pos   = bot["positions"][cid]
        # Use cached Polymarket data first
        pm    = markets_by_cid.get(cid)
        if pm:
            # Find matching outcome price
            for o in pm["outcomes"]:
                if o["outcome"].lower() == pos["outcome"].lower():
                    price = o["price"]
                    break
            else:
                price = pm["outcomes"][0]["price"]
        else:
            price = fetch_market_price(cid)

        if price is None:
            continue

        pos["current_price"]  = price
        pos["current_value"]  = round(pos["shares"] * price, 4)
        pos["unrealized_pnl"] = round(pos["current_value"] - pos["cost_usd"], 4)

        if price >= 0.99:
            close_position(bot, cid, "resolved_win", 1.0)
        elif price <= 0.01:
            close_position(bot, cid, "resolved_loss", 0.0)


def update_equity(bot):
    pos_value  = sum(p.get("current_value", p["cost_usd"]) for p in bot["positions"].values())
    bot["equity"]  = round(bot["cash"] + pos_value, 4)
    bot["pnl_usd"] = round(bot["equity"] - bot["starting_capital"], 4)
    bot["pnl_pct"] = round((bot["pnl_usd"] / bot["starting_capital"]) * 100, 2)


# ── Cycle management ──────────────────────────────────────────────────────

def tg_send(msg):
    """Send a Telegram message via the SYN bot."""
    try:
        data = json.dumps({"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}).encode()
        req  = urllib.request.Request(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data=data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        log.warning(f"Telegram notify failed: {e}")


def load_cycle_state():
    try:
        with open(CYCLE_STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {"cycle": 1, "sprint_in_cycle": 0, "sprints_per_cycle": 4,
                "cycle_started_at": None, "status": "active", "sprints": []}


def save_cycle_state(state):
    with open(CYCLE_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def update_cycle_after_sprint(sprint_id):
    """Record completed sprint. Returns True if cycle is now complete."""
    cs = load_cycle_state()
    if sprint_id not in cs.get("sprints", []):
        cs.setdefault("sprints", []).append(sprint_id)
    cs["sprint_in_cycle"] = len(cs["sprints"])
    cycle   = cs["cycle"]
    n       = cs["sprint_in_cycle"]
    per     = cs["sprints_per_cycle"]
    if n >= per:
        cs["status"] = "awaiting_review"
        save_cycle_state(cs)
        msg = "*Polymarket Cycle " + str(cycle) + " complete* - all " + str(per) + " sprints done. Review standings and adjust strategies, then run: python3 /root/.openclaw/workspace/polymarket_cycle_advance.py"
        tg_send(msg)
        log.info(f"Polymarket Cycle {cycle} complete — awaiting review. Telegram alert sent.")
        return True
    else:
        save_cycle_state(cs)
        log.info(f"Polymarket cycle state: Cycle {cycle}, Sprint {n}/{per}")
        return False


# ── Sprint management ──────────────────────────────────────────────────────

def sprint_is_expired(state):
    ends_at = state.get("sprint_ends_at")
    if not ends_at:
        return False
    try:
        end_dt = datetime.fromisoformat(ends_at.replace("Z", "+00:00"))
        return datetime.now(timezone.utc) >= end_dt
    except Exception:
        return False


def score_and_archive_sprint(state):
    sprint_id = state.get("sprint_id", "unknown")
    log.info(f"Sprint {sprint_id} expired — scoring...")

    bots = sorted(state["bots"], key=lambda b: b["equity"], reverse=True)
    for i, bot in enumerate(bots):
        log.info(f"  #{i+1} {bot['name']:<12} equity=${bot['equity']:.2f} pnl=${bot['pnl_usd']:+.2f}")

    # Write to unified sprint_results dir (same as copy-traders)
    unified_dir = os.path.join(os.path.dirname(RESULTS_DIR), "sprint_results")
    os.makedirs(unified_dir, exist_ok=True)

    bots_data = []
    for bot in bots:
        trades = bot.get("total_trades", 0)
        wins   = bot.get("wins", 0)
        pnl    = bot.get("pnl_usd", 0.0)
        bots_data.append({
            "bot":            bot["name"],
            "type":           bot.get("category", "auto"),
            "username":       "",
            "sprint_pnl_usd": round(pnl, 2),
            "sprint_pnl_pct": round(bot.get("pnl_pct", 0.0), 2),
            "sprint_trades":  trades,
            "sprint_wins":    wins,
            "win_rate":       round(wins / trades * 100, 1) if trades > 0 else 0.0,
        })

    result_file = os.path.join(unified_dir, f"{sprint_id}_auto.json")
    with open(result_file, "w") as f:
        json.dump({
            "sprint_id":  sprint_id,
            "started_at": state.get("sprint_started_at"),
            "ended_at":   datetime.now(timezone.utc).isoformat(),
            "bots":       bots_data,
        }, f, indent=2)
    log.info(f"Auto sprint results archived: {result_file}")

    # Keep legacy auto_results for backward compat
    result_dir = os.path.join(RESULTS_DIR, sprint_id)
    os.makedirs(result_dir, exist_ok=True)
    with open(os.path.join(result_dir, "final_score.json"), "w") as f:
        json.dump({"sprint_id": sprint_id, "scored_at": datetime.now(timezone.utc).isoformat(),
                   "bots": bots_data}, f, indent=2)

    # Regenerate unified leaderboard
    try:
        import subprocess as _sp
        lb_script = os.path.join(os.path.dirname(RESULTS_DIR), "..", "polymarket_leaderboard.py")
        lb_script = os.path.normpath(lb_script)
        _sp.Popen(["python3", lb_script, "--json"])
    except Exception as _e:
        log.warning(f"Could not run leaderboard: {_e}")


def start_new_sprint(state):
    now       = datetime.now(timezone.utc)
    sprint_id = f"poly-auto-{now.strftime('%Y%m%d-%H%M')}"
    state["sprint_id"]         = sprint_id
    state["sprint_started_at"] = now.isoformat()
    state["sprint_ends_at"]    = (now + timedelta(hours=SPRINT_HOURS)).isoformat()
    # Reset all bots
    for bot in state["bots"]:
        bot["cash"]          = 1000.0
        bot["equity"]        = 1000.0
        bot["pnl_usd"]       = 0.0
        bot["pnl_pct"]       = 0.0
        bot["total_trades"]  = 0
        bot["wins"]          = 0
        bot["losses"]        = 0
        bot["positions"]     = {}
        bot["closed_trades"] = []
        bot["scan_count"]    = 0
        bot["gemini_calls"]  = 0
        bot["last_scan_at"]  = None
    log.info(f"New sprint started: {sprint_id} — ends {state['sprint_ends_at']}")


# ── Dashboard output ───────────────────────────────────────────────────────

def write_dashboard(state):
    bots = state.get("bots", [])
    # Aggregate stats
    total_pnl  = round(sum(b.get("pnl_usd", 0) for b in bots), 2)
    total_tr   = sum(b.get("total_trades", 0) for b in bots)
    total_wins = sum(b.get("wins", 0) for b in bots)
    total_pos  = sum(len(b.get("positions", {})) for b in bots)
    total_gem  = sum(b.get("gemini_calls", 0) for b in bots)
    wr         = round(total_wins / total_tr * 100, 1) if total_tr > 0 else 0.0

    norm_bots = []
    for b in bots:
        t = b.get("total_trades", 0)
        w = b.get("wins", 0)
        norm_bots.append({
            "bot":              b["name"],
            "category":         b.get("category", ""),
            "assigned_trader":  f"Gemini [{b.get('category','')}]" if b.get("type") == "opinion" else "Arb Engine",
            "pnl_usd":          round(b.get("pnl_usd", 0), 2),
            "win_rate":         round(w / t * 100, 1) if t > 0 else 0.0,
            "trades":           t,
            "active_positions": len(b.get("positions", {})),
            "status":           state.get("status", "active"),
        })

    open_pos = []
    for b in bots:
        for cid, pos in b.get("positions", {}).items():
            open_pos.append({
                "bot":            b["name"],
                "trader":         f"Gemini [{b.get('category','')}]",
                "market":         pos.get("title", ""),
                "outcome":        pos.get("outcome", ""),
                "side":           "BUY",
                "entry_price":    pos.get("entry_price", 0),
                "current_price":  pos.get("current_price", 0),
                "cost_usd":       pos.get("cost_usd", 0),
                "current_value":  pos.get("current_value", 0),
                "unrealized_pnl": pos.get("unrealized_pnl", 0),
                "opened_at":      pos.get("opened_at", ""),
            })

    sprint_started_at = state.get("sprint_started_at", "")
    recent = []
    for b in bots:
        for t in b.get("closed_trades", []):
            ts = t.get("closed_at", "")
            if sprint_started_at and ts and ts < sprint_started_at:
                continue
            recent.append({
                "bot":          b["name"],
                "market_title": t.get("title", ""),
                "direction":    t.get("outcome", ""),
                "outcome":      "win" if t.get("pnl_usd", 0) >= 0 else "loss",
                "pnl_usd":      t.get("pnl_usd"),
                "pnl_pct":      t.get("pnl_pct"),
                "closed_at":    t.get("closed_at", ""),
                "reason":       t.get("reason", ""),
            })
    recent = sorted(recent, key=lambda x: x.get("closed_at") or "", reverse=True)

    dashboard = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode":         state.get("mode", "paper"),
        "status":       state.get("status", "active"),
        "bot_type":     "autonomous",
        "sprint_id":    state.get("sprint_id"),
        "sprint_ends_at": state.get("sprint_ends_at"),
        "stats": {
            "total_pnl_usd":    total_pnl,
            "overall_win_rate": wr,
            "active_positions": total_pos,
            "total_trades":     total_tr,
            "gemini_calls":     total_gem,
        },
        "bots":            norm_bots,
        "tracked_traders": [],
        "open_positions":  open_pos,
        "closed_positions": recent,
        "recent_trades":   recent,
    }
    os.makedirs(os.path.dirname(DASH_OUTPUT), exist_ok=True)
    with open(DASH_OUTPUT, "w") as f:
        json.dump(dashboard, f, indent=2)


# ── Main orchestration tick ────────────────────────────────────────────────

def run_tick(state, strategies, secrets, tick_count):
    log.info(f"─── Tick #{tick_count} | Sprint: {state.get('sprint_id','?')} "
             f"| Bots: {len(state['bots'])} ───")

    # Cycle gate — pause only when awaiting strategy review
    cs = load_cycle_state()
    if cs.get("status") == "awaiting_review":
        log.info(f"Polymarket Cycle {cs['cycle']} awaiting review — tick skipped.")
        return

    # Sprint check — archive and immediately restart (Polymarket runs 24/7)
    if sprint_is_expired(state):
        completed_sprint_id = state.get("sprint_id", "unknown")
        score_and_archive_sprint(state)
        cycle_done = update_cycle_after_sprint(completed_sprint_id)
        if cycle_done:
            log.info("Cycle complete — awaiting strategy review.")
            state["status"] = "awaiting_review"
        else:
            cs = load_cycle_state()
            next_sprint_num = cs["sprint_in_cycle"] + 1
            start_new_sprint(state)
            state["cycle"] = cs["cycle"]
            state["sprint_in_cycle"] = next_sprint_num
            cs["sprint_in_cycle"] = next_sprint_num
            cs["sprints"].append(state["sprint_id"])
            save_cycle_state(cs)
            log.info(f"New sprint auto-started: {state['sprint_id']}")

    # ── 1. Fetch all market data once ────────────────────────────────────
    pm_markets    = fetch_polymarket_markets(strategies)
    markets_by_cid = {m["condition_id"]: m for m in pm_markets}

    do_scan = (tick_count % SCAN_EVERY == 0)
    if do_scan:
        metaculus_markets = fetch_metaculus_markets()
        manifold_markets  = fetch_manifold_markets()
        kalshi_markets    = fetch_kalshi_markets(secrets.get("kalshi_api_key"))
        # Pre-build inverted indexes for fast title matching
        meta_index   = build_title_index(metaculus_markets)
        manif_index  = build_title_index(manifold_markets)
        kalshi_index = build_title_index(kalshi_markets)
    else:
        metaculus_markets, manifold_markets, kalshi_markets = [], [], []
        meta_index = manif_index = kalshi_index = {}
        log.info("Skipping external data fetch this tick (price refresh only)")

    # ── 2. Refresh all bot positions ──────────────────────────────────────
    for bot in state["bots"]:
        refresh_bot_positions(bot, markets_by_cid)
        # Check stop-loss
        dd = (bot["starting_capital"] - bot["equity"]) / bot["starting_capital"] * 100
        strategy = strategies.get(bot["name"], {})
        if dd >= strategy.get("risk", {}).get("stop_if_down_pct", 20):
            log.warning(f"  [{bot['name']}] Stop-loss: {dd:.1f}% down — closing all")
            for cid in list(bot["positions"].keys()):
                p = fetch_market_price(cid) or bot["positions"][cid]["current_price"]
                close_position(bot, cid, "stop_loss", p)
        update_equity(bot)

    if not do_scan:
        return

    # ── 3. Build candidate pools for each bot ─────────────────────────────
    # opinion_pool: {cid → {market, bots[], vegas}}
    # arb_pool:     {cid → {market, meta_match, manif_match, bots[]}}
    opinion_pool = {}
    arb_pool     = {}

    for bot in state["bots"]:
        strategy = strategies.get(bot["name"], {})
        if not strategy:
            continue
        existing_cids = set(bot["positions"].keys())
        bot_type      = strategy.get("type", "opinion")

        if bot_type == "arb":
            arb_sources = strategy.get("arb_sources", [])
            candidates  = filter_for_bot(pm_markets, strategy, existing_cids)
            for market in candidates:
                cid = market["condition_id"]
                if cid not in arb_pool:
                    meta_m   = find_best_external_match(market["title"], metaculus_markets, min_score=0.40, index=meta_index)   if "metaculus" in arb_sources else None
                    manif_m  = find_best_external_match(market["title"], manifold_markets,  min_score=0.40, index=manif_index)  if "manifold"  in arb_sources else None
                    kalshi_m = find_best_external_match(market["title"], kalshi_markets,    min_score=0.40, index=kalshi_index) if "kalshi"    in arb_sources else None
                    arb_pool[cid] = {
                        "market":       market,
                        "meta_match":   meta_m,
                        "manif_match":  manif_m,
                        "kalshi_match": kalshi_m,
                        "bots":         [],
                    }
                arb_pool[cid]["bots"].append(bot["name"])
        else:
            candidates = filter_for_bot(pm_markets, strategy, existing_cids)
            for market in candidates:
                cid = market["condition_id"]
                if cid not in opinion_pool:
                    kalshi_m = find_best_external_match(market["title"], kalshi_markets, min_score=0.30, index=kalshi_index)
                    opinion_pool[cid] = {
                        "market":   market,
                        "kalshi":   kalshi_m,
                        "bots":     [],
                        "category": strategy.get("category", ""),
                    }
                opinion_pool[cid]["bots"].append(bot["name"])

    log.info(f"Candidate pools — opinion: {len(opinion_pool)}  arb: {len(arb_pool)}")

    # ── 4. Run Gemini (deduplicated across all opinion bots) ──────────────
    gemini_cache = {}  # cid → assessment
    gemini_count = 0
    gemini_aborted = False

    # Key rotation + per-key daily quota tracking
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    gemini_keys = secrets.get("gemini_api_keys", [secrets["gemini_api_key"]])

    # Reset daily counters at UTC midnight
    gd = state.setdefault("gemini_daily", {})
    if gd.get("reset_date") != today_str:
        gd["reset_date"] = today_str
        gd["counts"]     = [0] * len(gemini_keys)
        gd["exhausted"]  = []

    counts    = gd.setdefault("counts",    [0] * len(gemini_keys))
    exhausted = gd.setdefault("exhausted", [])

    # Extend counts list if we added more keys since last reset
    while len(counts) < len(gemini_keys):
        counts.append(0)

    available_keys = [i for i in range(len(gemini_keys)) if i not in exhausted and counts[i] < GEMINI_DAILY_LIMIT]
    if not available_keys:
        log.warning("All Gemini keys daily quota exhausted — skipping Gemini this tick")
        gemini_aborted = True

    # Cross-tick assessment cache (persists in state, TTL = GEMINI_CACHE_TTL_H)
    now_ts = datetime.now(timezone.utc).timestamp()
    ac = state.setdefault("assessment_cache", {})
    # Prune expired entries
    stale = [k for k, v in ac.items() if now_ts - v.get("ts", 0) > GEMINI_CACHE_TTL_H * 3600]
    for k in stale:
        del ac[k]
    cache_hits = 0

    key_cursor = 0  # round-robin cursor within available_keys

    # Per-category round-robin: ensures all bot categories get Gemini slots,
    # then within each category prioritize by Kalshi edge + distance from 0.5.
    # Prevents winner-take-all where political/popular markets exhaust the 12-call budget.
    def _candidate_priority(item):
        cid, candidate = item
        outcomes = sorted(candidate["market"]["outcomes"], key=lambda x: x["price"])
        pm_price = outcomes[0]["price"] if outcomes else 0.5
        if pm_price < 0.04 or pm_price > 0.96:
            return 0.0
        kalshi = candidate.get("kalshi")
        kalshi_edge = abs(kalshi["prob"] - pm_price) if kalshi else 0.0
        return -(kalshi_edge * 2 + abs(pm_price - 0.5))

    # Group by category, sort within each, then round-robin interleave
    category_buckets = {}
    for cid, candidate in opinion_pool.items():
        cat = candidate.get("category", "general")
        category_buckets.setdefault(cat, []).append((cid, candidate))
    for cat in category_buckets:
        category_buckets[cat].sort(key=_candidate_priority)
    category_lists = list(category_buckets.values())
    sorted_candidates = []
    max_len = max((len(v) for v in category_lists), default=0)
    for i in range(max_len):
        for cat_list in category_lists:
            if i < len(cat_list):
                sorted_candidates.append(cat_list[i])

    for cid, candidate in sorted_candidates:
        if gemini_aborted or gemini_count >= MAX_GEMINI_PER_TICK:
            break

        market   = candidate["market"]
        outcomes = sorted(market["outcomes"], key=lambda x: x["price"])
        target   = outcomes[0]
        pm_price = target["price"]

        if pm_price < 0.04 or pm_price > 0.96:
            continue

        # Use persona from first interested bot
        first_bot = candidate["bots"][0] if candidate["bots"] else None
        if not first_bot:
            continue
        persona = strategies.get(first_bot, {}).get("prompt_persona", "You are a prediction market analyst.")

        # Check cross-tick cache: skip Gemini if assessed recently and price unchanged
        cached = ac.get(cid)
        if cached and (now_ts - cached["ts"] < GEMINI_CACHE_TTL_H * 3600) and (abs(pm_price - cached["pm_price"]) < GEMINI_CACHE_DELTA):
            gemini_cache[cid] = cached["assessment"]
            cache_hits += 1
            continue

        time.sleep(GEMINI_SLEEP)
        assessment = None
        while available_keys:
            key_idx = available_keys[key_cursor % len(available_keys)]
            try:
                assessment = gemini_assess(
                    market["title"], target["outcome"], pm_price,
                    candidate.get("kalshi"), persona, gemini_keys[key_idx]
                )
                counts[key_idx] += 1
                key_cursor += 1
                break
            except RuntimeError as e:
                if "GEMINI_KEY_EXHAUSTED" in str(e):
                    log.warning(f"Gemini key {key_idx} daily quota exhausted — rotating to next key")
                    exhausted.append(key_idx)
                    available_keys = [i for i in range(len(gemini_keys)) if i not in exhausted and counts[i] < GEMINI_DAILY_LIMIT]
                    key_cursor = 0
                else:
                    gemini_aborted = True
                    log.warning("Gemini error — aborting Gemini for this tick")
                    break
        else:
            gemini_aborted = True
            log.warning("All Gemini keys exhausted — skipping remaining opinion candidates this tick")
            break

        if gemini_aborted:
            break

        gemini_count += 1
        if assessment:
            entry = {
                **assessment,
                "outcome":  target["outcome"],
                "pm_price": pm_price,
            }
            gemini_cache[cid] = entry
            ac[cid] = {"assessment": entry, "pm_price": pm_price, "ts": now_ts}

    # Log daily usage after tick
    if gemini_count > 0 or cache_hits > 0:
        usage_str = " | ".join(f"key{i}={counts[i]}" for i in range(len(gemini_keys)))
        log.info(f"Gemini this tick: {gemini_count} calls, {cache_hits} cache hits | daily: {usage_str} (limit {GEMINI_DAILY_LIMIT}/key)")

    # Track Gemini calls across all bots (proportional distribution)
    if gemini_count > 0:
        per_bot = gemini_count / max(1, len([b for b in state["bots"] if strategies.get(b["name"], {}).get("type") == "opinion"]))
        for bot in state["bots"]:
            if strategies.get(bot["name"], {}).get("type") == "opinion":
                bot["gemini_calls"] += round(per_bot)

    # ── 5. Execute opinion bot trades ─────────────────────────────────────
    for bot in state["bots"]:
        strategy = strategies.get(bot["name"], {})
        if not strategy or strategy.get("type") != "opinion":
            continue

        edge_cfg = strategy.get("edge", {})
        min_edge = edge_cfg.get("min_edge_pts", 0.07)
        min_conf = edge_cfg.get("min_confidence", "medium")

        for cid, candidate in opinion_pool.items():
            if bot["name"] not in candidate["bots"]:
                continue
            if cid not in gemini_cache:
                continue
            if cid in bot["positions"]:
                continue

            assessment = gemini_cache[cid]
            est_prob   = assessment["estimated_prob"]
            confidence = assessment.get("confidence", "low")
            value      = assessment.get("value", "FAIR")
            pm_price   = assessment["pm_price"]
            edge       = abs(est_prob - pm_price)

            log.info(f"  [{bot['name']}] {candidate['market']['title'][:40]} | "
                     f"PM={pm_price:.2f} Gem={est_prob:.2f} edge={edge:.2f} "
                     f"conf={confidence} val={value}")

            if (value == "YES"
                    and edge >= min_edge
                    and CONF_RANK.get(confidence, 0) >= CONF_RANK.get(min_conf, 1)):
                open_position(
                    bot, candidate["market"], assessment["outcome"],
                    pm_price, assessment.get("reasoning", ""), strategy
                )
                update_equity(bot)

    # ── 6. Execute arb bot trades ─────────────────────────────────────────
    for bot in state["bots"]:
        strategy = strategies.get(bot["name"], {})
        if not strategy or strategy.get("type") != "arb":
            continue

        arb_sources    = strategy.get("arb_sources", [])
        arb_min_gap    = strategy.get("arb_min_gap", 0.08)
        req_consensus  = strategy.get("require_consensus", False)
        edge_cfg       = strategy.get("edge", {})

        for cid, arb in arb_pool.items():
            if bot["name"] not in arb["bots"]:
                continue
            if cid in bot["positions"]:
                continue

            market    = arb["market"]
            outcomes  = sorted(market["outcomes"], key=lambda x: x["price"])
            target    = outcomes[0]
            pm_price  = target["price"]
            meta_m    = arb.get("meta_match")
            manif_m   = arb.get("manif_match")
            kalshi_m  = arb.get("kalshi_match")

            meta_prob   = meta_m["prob"]   if meta_m   else None
            manif_prob  = manif_m["prob"]  if manif_m  else None
            kalshi_prob = kalshi_m["prob"] if kalshi_m else None

            # Compute gaps
            meta_gap   = abs(meta_prob   - pm_price) if meta_prob   is not None else 0
            manif_gap  = abs(manif_prob  - pm_price) if manif_prob  is not None else 0
            kalshi_gap = abs(kalshi_prob - pm_price) if kalshi_prob is not None else 0

            # Direction checks (external source says PM is underpriced)
            meta_agrees   = meta_prob   is not None and meta_prob   > pm_price and meta_gap   >= arb_min_gap
            manif_agrees  = manif_prob  is not None and manif_prob  > pm_price and manif_gap  >= arb_min_gap
            kalshi_agrees = kalshi_prob is not None and kalshi_prob > pm_price and kalshi_gap >= arb_min_gap

            if req_consensus:
                # Muninn: both Kalshi AND Manifold must agree
                if not (kalshi_agrees and manif_agrees):
                    continue
                reasoning = (f"Arb: PM={pm_price:.2f} Kalshi={kalshi_prob:.2f} "
                             f"Manif={manif_prob:.2f} — consensus gap")
            elif "kalshi" in arb_sources and "manifold" not in arb_sources and "metaculus" not in arb_sources:
                # Loki: Kalshi only
                if not kalshi_agrees:
                    continue
                reasoning = (f"Arb: PM={pm_price:.2f} Kalshi={kalshi_prob:.2f} "
                             f"gap={kalshi_gap:.2f}")
            elif "manifold" in arb_sources and "kalshi" not in arb_sources and "metaculus" not in arb_sources:
                # Huginn: Manifold only
                if not manif_agrees:
                    continue
                reasoning = (f"Arb: PM={pm_price:.2f} Manifold={manif_prob:.2f} "
                             f"gap={manif_gap:.2f}")
            elif "metaculus" in arb_sources and "kalshi" not in arb_sources and "manifold" not in arb_sources:
                # Legacy Metaculus-only mode
                if not meta_agrees:
                    continue
                reasoning = (f"Arb: PM={pm_price:.2f} Metaculus={meta_prob:.2f} "
                             f"gap={meta_gap:.2f}")
            else:
                continue

            log.info(f"  [{bot['name']}] ARB {market['title'][:40]} | {reasoning}")
            open_position(bot, market, target["outcome"], pm_price, reasoning, strategy)
            update_equity(bot)

    bot_summary = " | ".join(
        f"{b['name']}=${b['equity']:.0f}" for b in sorted(state["bots"], key=lambda x: x["equity"], reverse=True)[:5]
    )
    log.info(f"Top 5: {bot_summary}")


def main():
    if not os.path.exists(AUTO_STATE_FILE):
        log.error(f"State not found: {AUTO_STATE_FILE} — run polymarket_syn_init.py first")
        return

    log.info(f"SYN polymarket orchestrator starting — {POLL_SEC}s ticks")
    secrets    = load_secrets()
    strategies = load_all_strategies()
    log.info(f"Managing {len([s for s in strategies.values() if s.get('type')=='opinion'])} opinion bots "
             f"+ {len([s for s in strategies.values() if s.get('type')=='arb'])} arb bots")

    tick_count = 0
    while True:
        try:
            state = load_state()
            run_tick(state, strategies, secrets, tick_count)
            save_state(state)
            write_dashboard(state)
        except Exception as e:
            log.error(f"Tick error: {e}", exc_info=True)
        tick_count += 1
        time.sleep(POLL_SEC)


if __name__ == "__main__":
    main()
