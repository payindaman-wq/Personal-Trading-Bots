#!/usr/bin/env python3
"""
polymarket_auto_tick.py — Ullr autonomous sports betting bot for Polymarket.

Every 15 min: refresh open position prices, auto-close resolved markets.
Every 30 min: scan Polymarket for sports candidates, compare to Kalshi,
              ask Gemini to assess edge, trade if confirmed.
"""
import json, os, time, re, logging, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

AUTO_STATE_FILE = "/root/.openclaw/workspace/competition/polymarket/auto_state.json"
STRATEGY_FILE   = "/root/.openclaw/workspace/fleet/polymarket/ullr/strategy.yaml"
GEMINI_SECRET   = "/root/.openclaw/secrets/gemini.json"
DASH_OUTPUT     = "/var/www/dashboard/api/polymarket_auto.json"
LOG_FILE        = "/root/.openclaw/workspace/competition/polymarket/auto_tick.log"
POLL_SEC        = 900   # 15 min between ticks
SCAN_EVERY      = 2     # scan for new markets every 2 ticks (30 min)


os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)
log = logging.getLogger(__name__)
CONFIDENCE_RANK = {"low": 0, "medium": 1, "high": 2}


# ── Helpers ───────────────────────────────────────────────────────────────────

def api_get(url, timeout=10):
    req = urllib.request.Request(
        url, headers={"User-Agent": "ullr-polymarket-bot/1.0", "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def api_post(url, payload, headers=None, timeout=15):
    data = json.dumps(payload).encode()
    h = {"Content-Type": "application/json", "Accept": "application/json"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def load_secrets():
    with open(GEMINI_SECRET) as f:
        g = json.load(f)
    return {"gemini_api_key": g["gemini_api_key"]}


def load_strategy():
    """Parse strategy YAML manually (no PyYAML dependency)."""
    defaults = {
        "min_liquidity_usd": 1000,
        "max_days_to_resolve": 3,
        "min_edge_pts": 0.07,
        "min_confidence": "medium",
        "max_position_pct": 0.10,
        "max_positions": 5,
        "reeval_move_pts": 0.05,
        "stop_if_down_pct": 20,
        "starting_capital": 1000.0,
        "include_keywords": [" vs ", " vs. ", "O/U", " Over ", " Under ", "Spread:", "to win", "will win"],
        "exclude_keywords": ["election", "vote", "crypto", "bitcoin", "ethereum",
                             "president", "congress", "weather", "rain"],
    }
    try:
        import yaml
        with open(STRATEGY_FILE) as f:
            s = yaml.safe_load(f)
        mf = s.get("market_filter", {})
        ed = s.get("edge", {})
        ri = s.get("risk", {})
        defaults.update({
            "min_liquidity_usd":   mf.get("min_liquidity_usd", defaults["min_liquidity_usd"]),
            "max_days_to_resolve": mf.get("max_days_to_resolve", defaults["max_days_to_resolve"]),
            "min_edge_pts":        ed.get("min_edge_pts", defaults["min_edge_pts"]),
            "min_confidence":      ed.get("min_confidence", defaults["min_confidence"]),
            "max_position_pct":    ed.get("max_position_pct", defaults["max_position_pct"]),
            "max_positions":       ed.get("max_positions", defaults["max_positions"]),
            "stop_if_down_pct":    ri.get("stop_if_down_pct", defaults["stop_if_down_pct"]),
            "include_keywords":    mf.get("include_keywords", defaults["include_keywords"]),
            "exclude_keywords":    mf.get("exclude_keywords", defaults["exclude_keywords"]),
        })
    except Exception as e:
        log.warning(f"Could not parse strategy YAML ({e}), using defaults")
    return defaults


def load_state():
    with open(AUTO_STATE_FILE) as f:
        return json.load(f)


def save_state(state):
    state["generated_at"] = datetime.now(timezone.utc).isoformat()
    with open(AUTO_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# ── Polymarket market scanning ────────────────────────────────────────────────

def fetch_polymarket_sports_markets(strategy):
    """Fetch open Polymarket markets and filter to sports candidates."""
    candidates = []
    offset = 0
    limit = 100
    cutoff = datetime.now(timezone.utc) + timedelta(days=strategy["max_days_to_resolve"])
    include_kw = [k.lower() for k in strategy["include_keywords"]]
    exclude_kw = [k.lower() for k in strategy["exclude_keywords"]]

    while True:
        try:
            url = f"https://gamma-api.polymarket.com/markets?closed=false&active=true&limit={limit}&offset={offset}"
            markets = api_get(url, timeout=15)
        except Exception as e:
            log.warning(f"Polymarket fetch error (offset={offset}): {e}")
            break

        if not markets:
            break

        for m in markets:
            question = (m.get("question") or "").strip()
            q_lower  = question.lower()

            # Keyword filters
            if not any(k in q_lower for k in include_kw):
                continue
            if any(k in q_lower for k in exclude_kw):
                continue

            # Liquidity filter
            liquidity = float(m.get("liquidity") or 0)
            if liquidity < strategy["min_liquidity_usd"]:
                continue

            # End date filter
            end_date_str = m.get("endDate") or m.get("end_date_iso") or ""
            if end_date_str:
                try:
                    end_dt = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))
                    if end_dt > cutoff:
                        continue
                    if end_dt < datetime.now(timezone.utc):
                        continue
                except Exception:
                    pass

            # Parse outcomes and prices
            try:
                outcomes   = json.loads(m.get("outcomes", "[]"))
                out_prices = json.loads(m.get("outcomePrices", "[]"))
                if len(outcomes) != 2 or len(out_prices) != 2:
                    continue
                parsed = [
                    {"outcome": outcomes[i], "price": float(out_prices[i])}
                    for i in range(2)
                ]
            except Exception:
                continue

            candidates.append({
                "condition_id": m.get("conditionId", ""),
                "title":        question,
                "outcomes":     parsed,
                "liquidity":    liquidity,
                "end_date":     end_date_str,
            })

        if len(markets) < limit:
            break
        offset += limit

    log.info(f"Market scan: {len(candidates)} sports candidates found")
    return candidates


def fetch_market_price(condition_id):
    """Get current midpoint price for a condition."""
    try:
        url  = f"https://clob.polymarket.com/midpoints?conditionIds={condition_id}"
        data = api_get(url, timeout=5)
        val  = data.get("midpoints", {}).get(condition_id)
        return float(val) if val is not None else None
    except Exception:
        return None


# ── Vegas odds ────────────────────────────────────────────────────────────────

STOP_WORDS = {"will","the","a","an","of","in","on","at","to","for","is","are",
              "be","has","have","by","or","and","vs","vs.","who","what","when",
              "how","does","do","can","could","would","should","may","might"}

def _tokens(text):
    words = re.sub(r"[^a-z0-9 ]", " ", text.lower()).split()
    return set(w for w in words if w not in STOP_WORDS and len(w) > 2)

def build_title_index(markets):
    index = {}
    for i, m in enumerate(markets):
        for tok in _tokens(m["title"]):
            index.setdefault(tok, []).append(i)
    return index

def find_best_external_match(pm_title, markets, min_score=0.25, index=None):
    pm_toks = _tokens(pm_title)
    if not pm_toks:
        return None
    if index is not None:
        cand_indices = set()
        for tok in pm_toks:
            cand_indices.update(index.get(tok, []))
        candidates = [markets[i] for i in cand_indices]
    else:
        candidates = markets
    best, best_score = None, min_score
    for m in candidates:
        tb = _tokens(m["title"])
        if not tb:
            continue
        score = len(pm_toks & tb) / len(pm_toks | tb)
        if score > best_score:
            best, best_score = m, score
    return best

def fetch_kalshi_markets():
    """Fetch Kalshi markets with midpoint probability. No auth needed."""
    markets = []
    cursor = None
    for _ in range(10):
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
                    bid, ask = float(yes_bid), float(yes_ask)
                except (ValueError, TypeError):
                    continue
                if bid <= 0 or ask <= 0 or bid >= 1 or ask >= 1:
                    continue
                title = m.get("title", "") or event.get("title", "")
                if not title:
                    continue
                markets.append({
                    "id":    m.get("ticker", ""),
                    "title": title,
                    "prob":  round((bid + ask) / 2, 4),
                    "close": m.get("close_time", ""),
                })
        cursor = page.get("cursor")
        if not cursor or len(page.get("events", [])) < 200:
            break
    log.info(f"Fetched {len(markets)} Kalshi markets")
    return markets



# ── Gemini reasoning ──────────────────────────────────────────────────────────

def gemini_assess(title, outcome, polymarket_price, kalshi_match, gemini_api_key):
    """Ask Gemini to estimate true probability and assess edge."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if kalshi_match:
        ref_section = (
            f"Kalshi market consensus:\n"
            f"  '{kalshi_match['title']}': {kalshi_match['prob']:.1%}"
        )
    else:
        ref_section = "No external reference available — use your own assessment only."

    prompt = f"""You are a sharp sports betting analyst assessing a Polymarket prediction market.

Market: {title}
Outcome being assessed: {outcome}
Polymarket price: {polymarket_price:.3f} (implies {polymarket_price*100:.1f}% probability)
{ref_section}
Today's date: {today}

Assess the TRUE probability of this outcome based on:
- Your knowledge of the teams/players involved
- Current season form, injuries, head-to-head record
- Home/away advantage, venue, competition context
- Whether Polymarket appears to be mispricing vs the Kalshi consensus or your estimate

Respond ONLY with valid JSON (no markdown, no extra text):
{{"estimated_prob": 0.00, "confidence": "low|medium|high", "value": "YES|NO|FAIR", "reasoning": "2-3 sentences max", "key_factors": ["factor1", "factor2"]}}

Where "value" means:
- YES = Polymarket is underpricing this outcome, take it
- NO = Polymarket is overpricing this outcome, skip
- FAIR = price looks about right"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 256},
    }

    for attempt in range(2):
        try:
            resp = api_post(url, payload)
            text = resp["candidates"][0]["content"]["parts"][0]["text"].strip()
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
            result = json.loads(text)
            assert "estimated_prob" in result and "confidence" in result and "value" in result
            result["estimated_prob"] = float(result["estimated_prob"])
            return result
        except urllib.error.HTTPError as e:
            if e.code == 429:
                if attempt == 0:
                    log.warning("Gemini 429 — backing off 90s")
                    time.sleep(90)
                else:
                    log.warning("Gemini 429 persists — aborting scan, will retry next tick")
                    raise RuntimeError("GEMINI_QUOTA_ABORT")
            else:
                log.warning(f"Gemini HTTP error: {e.code}")
                return None
        except RuntimeError:
            raise
        except Exception as e:
            log.warning(f"Gemini assess error: {e}")
            return None
    return None


# ── Position management ───────────────────────────────────────────────────────

def open_position(bot, market, outcome, price, reasoning, strategy):
    cid      = market["condition_id"]
    size_usd = round(bot["cash"] * strategy["max_position_pct"], 2)

    if size_usd < 1.0:
        log.info(f"  [ullr] Insufficient cash (${bot['cash']:.2f}), skipping")
        return False
    if len(bot["positions"]) >= strategy["max_positions"]:
        log.info(f"  [ullr] Max positions reached ({strategy['max_positions']}), skipping")
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
        "reasoning":      reasoning,
    }
    bot["total_trades"] += 1
    log.info(f"  [ullr] OPEN {outcome} @ {price:.3f} | ${size_usd:.2f} | {market['title'][:50]}")
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
        "closed_at":   datetime.now(timezone.utc).isoformat(),
        "exit_price":  final_price,
        "proceeds_usd": proceeds,
        "pnl_usd":     pnl,
        "pnl_pct":     pnl_pct,
        "reason":      reason,
    })
    del bot["positions"][cid]
    log.info(f"  [ullr] CLOSE {reason} @ {final_price:.3f} | PNL ${pnl:+.2f} ({pnl_pct:+.1f}%) | {pos['title'][:40]}")


def update_bot_equity(bot):
    pos_value = sum(p.get("current_value", p["cost_usd"]) for p in bot["positions"].values())
    bot["equity"]  = round(bot["cash"] + pos_value, 4)
    bot["pnl_usd"] = round(bot["equity"] - bot["starting_capital"], 4)
    bot["pnl_pct"] = round((bot["pnl_usd"] / bot["starting_capital"]) * 100, 2)


def refresh_positions(bot, secrets, strategy):
    """Update prices on open positions; auto-close resolved markets."""
    for cid in list(bot["positions"].keys()):
        pos   = bot["positions"][cid]
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
        elif abs(price - pos["entry_price"]) >= strategy["reeval_move_pts"]:
            # Price moved significantly — ask Gemini if we should exit
            assessment = gemini_assess(
                pos["title"], pos["outcome"], price, None, secrets["gemini_api_key"]
            )
            bot["gemini_calls"] += 1
            if assessment and assessment.get("value") == "NO":
                close_position(bot, cid, "gemini_exit", price)


# ── Dashboard output ──────────────────────────────────────────────────────────

def write_dashboard(state):
    bots     = state.get("bots", [])
    all_pnl  = sum(b.get("pnl_usd", 0) for b in bots)
    all_wins = sum(b.get("wins", 0) for b in bots)
    all_tr   = sum(b.get("total_trades", 0) for b in bots)
    all_pos  = sum(len(b.get("positions", {})) for b in bots)
    all_gem  = sum(b.get("gemini_calls", 0) for b in bots)
    all_scan = sum(b.get("scan_count", 0) for b in bots)
    wr       = round(all_wins / all_tr * 100, 1) if all_tr > 0 else 0.0

    norm_bots = []
    for b in bots:
        t  = b.get("total_trades", 0)
        w  = b.get("wins", 0)
        norm_bots.append({
            "bot":              b["name"],
            "assigned_trader":  "Gemini 2.0 Flash",
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
                "trader":         "Gemini 2.0 Flash",
                "market":         pos.get("title", ""),
                "outcome":        pos.get("outcome", ""),
                "side":           pos.get("side", "BUY"),
                "entry_price":    pos.get("entry_price", 0),
                "current_price":  pos.get("current_price", 0),
                "cost_usd":       pos.get("cost_usd", 0),
                "current_value":  pos.get("current_value", 0),
                "unrealized_pnl": pos.get("unrealized_pnl", 0),
                "opened_at":      pos.get("opened_at", ""),
                "reasoning":      pos.get("reasoning", ""),
            })

    recent = []
    for b in bots:
        for t in b.get("closed_trades", [])[-20:]:
            recent.append({
                "bot":          b["name"],
                "market_title": t.get("title", ""),
                "direction":    t.get("outcome", ""),
                "outcome":      "win" if t.get("pnl_usd", 0) >= 0 else "loss",
                "pnl_usd":      t.get("pnl_usd"),
            })
    recent = recent[-20:]

    dashboard = {
        "generated_at":    datetime.now(timezone.utc).isoformat(),
        "mode":            state.get("mode", "paper"),
        "status":          state.get("status", "active"),
        "bot_type":        "autonomous",
        "stats": {
            "total_pnl_usd":    round(all_pnl, 2),
            "overall_win_rate": wr,
            "active_positions": all_pos,
            "total_trades":     all_tr,
            "gemini_calls":     all_gem,
            "markets_scanned":  all_scan,
        },
        "bots":            norm_bots,
        "tracked_traders": [{"name": "Gemini 2.0 Flash", "bot": "ullr", "roi_pct": 0}],
        "open_positions":  open_pos,
        "recent_trades":   recent,
    }

    os.makedirs(os.path.dirname(DASH_OUTPUT), exist_ok=True)
    with open(DASH_OUTPUT, "w") as f:
        json.dump(dashboard, f, indent=2)


# ── Main tick ─────────────────────────────────────────────────────────────────

def tick(bot, strategy, secrets, tick_count):
    log.info(f"Tick #{tick_count} | cash=${bot['cash']:.2f} equity=${bot['equity']:.2f} "
             f"positions={len(bot['positions'])} gemini_calls={bot['gemini_calls']}")

    # Always refresh existing positions
    refresh_positions(bot, secrets, strategy)
    update_bot_equity(bot)

    # Check stop-loss
    drawdown = (bot["starting_capital"] - bot["equity"]) / bot["starting_capital"] * 100
    if drawdown >= strategy["stop_if_down_pct"]:
        log.warning(f"  [ullr] Stop-loss hit ({drawdown:.1f}% down) — closing all positions")
        for cid in list(bot["positions"].keys()):
            price = fetch_market_price(cid) or bot["positions"][cid]["current_price"]
            close_position(bot, cid, "stop_loss", price)
        update_bot_equity(bot)
        return

    # Scan for new markets every SCAN_EVERY ticks
    if tick_count % SCAN_EVERY != 0:
        return

    bot["last_scan_at"] = datetime.now(timezone.utc).isoformat()
    candidates = fetch_polymarket_sports_markets(strategy)
    bot["scan_count"] += len(candidates)

    # Fetch Kalshi once per scan as the reference probability source
    kalshi_markets = fetch_kalshi_markets()
    kalshi_index   = build_title_index(kalshi_markets)

    MAX_GEMINI_PER_SCAN = 10
    gemini_this_scan = 0

    for market in candidates:
        if gemini_this_scan >= MAX_GEMINI_PER_SCAN:
            log.info(f"  Gemini cap ({MAX_GEMINI_PER_SCAN}) reached, stopping scan")
            break
        cid = market["condition_id"]
        if cid in bot["positions"]:
            continue

        # Pick the outcome to assess (the one priced lower = potential underdog value)
        outcomes = sorted(market["outcomes"], key=lambda x: x["price"])
        target   = outcomes[0]  # assess the cheaper outcome for YES value
        pm_price = target["price"]

        # Pre-filter: only call Gemini if price looks interesting (not near 0 or 1)
        if pm_price < 0.10 or pm_price > 0.90:
            continue

        # Match against Kalshi for a reference probability
        kalshi_match = find_best_external_match(market["title"], kalshi_markets, min_score=0.30, index=kalshi_index)

        # Pre-filter: if Kalshi match found, skip if gap < half of min_edge (save Gemini calls)
        if kalshi_match:
            gap = abs(kalshi_match["prob"] - pm_price)
            if gap < strategy["min_edge_pts"] / 2:
                log.debug(f"  Skipping {market['title'][:40]} — Kalshi gap too small ({gap:.3f})")
                continue

        # Only call Gemini when Kalshi reference found (saves quota on noise)
        if not kalshi_match:
            continue

        # Rate limit: 6s between calls (~10/min, free tier is 15 RPM)
        time.sleep(6)
        try:
            assessment = gemini_assess(
                market["title"], target["outcome"], pm_price, kalshi_match, secrets["gemini_api_key"]
            )
        except RuntimeError:
            log.warning("  Scan aborted due to Gemini quota — waiting for next tick")
            break
        bot["gemini_calls"] += 1
        gemini_this_scan += 1

        if assessment is None:
            continue

        est_prob   = assessment["estimated_prob"]
        confidence = assessment.get("confidence", "low")
        value      = assessment.get("value", "FAIR")
        edge       = abs(est_prob - pm_price)

        log.info(f"  [ullr] {market['title'][:45]} | PM={pm_price:.2f} "
                 f"Gemini={est_prob:.2f} edge={edge:.2f} conf={confidence} val={value}")

        if (value == "YES"
                and edge >= strategy["min_edge_pts"]
                and CONFIDENCE_RANK.get(confidence, 0) >= CONFIDENCE_RANK.get(strategy["min_confidence"], 1)):
            reasoning = assessment.get("reasoning", "")
            open_position(bot, market, target["outcome"], pm_price, reasoning, strategy)
            update_bot_equity(bot)




def main():
    if not os.path.exists(AUTO_STATE_FILE):
        log.error(f"State file not found: {AUTO_STATE_FILE}")
        log.error("Run polymarket_auto_init.py first.")
        return

    log.info(f"polymarket_auto_tick starting — polling every {POLL_SEC}s")
    secrets  = load_secrets()
    strategy = load_strategy()
    log.info(f"Strategy: min_edge={strategy['min_edge_pts']} "
             f"min_conf={strategy['min_confidence']} max_pos={strategy['max_positions']}")

    tick_count = 0
    while True:
        try:
            state = load_state()
            for bot in state["bots"]:
                tick(bot, strategy, secrets, tick_count)
            save_state(state)
            write_dashboard(state)
        except Exception as e:
            log.error(f"Tick error: {e}", exc_info=True)
        tick_count += 1
        time.sleep(POLL_SEC)


if __name__ == "__main__":
    main()
