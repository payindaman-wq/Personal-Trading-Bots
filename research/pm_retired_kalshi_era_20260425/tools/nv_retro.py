"""30-day NV retrospective: re-classify every trade in live PM bot state +
historical sprint results, split into NV-legal vs NV-blocked (sports /
elections / entertainment), and recompute P&L per bot as if the NV filter
had always been in place. Starts bots at $1000 notional for comparability.

Heuristic classification by title keywords (trade records don't carry
category field). Errs on the side of over-blocking sports — we'd rather
underestimate NV P&L than claim a winner that's actually sports-fueled."""
import json, os, re, glob
from collections import defaultdict

STATE_DIR = "/root/.openclaw/workspace/competition/polymarket"
SPRINT_DIR = os.path.join(STATE_DIR, "sprint_results")
STARTING_CAP = 1000.0

SPORTS_PATTERNS = [
    # Bet structure
    r"\bspread\b", r"\bmoneyline\b", r"\bover/under\b", r"\bo/u\b", r"\b\-?\d+\.5\)",
    r"\bhandicap\b", r"\b1h\b", r"\b2h\b", r"\bhalftime\b", r"\bfinal score\b",
    r"\bkick(-|\s)?off\b", r"\bpoints o/u\b", r"\bprop\b", r"\bprop bet\b",
    # Player prop / scoring
    r"\bpoints o/u", r"\brebounds o/u", r"\bassists o/u", r"\bstrikeouts?\b",
    r"\bwin by (ko|tko|submission|decision)\b", r"\bgoals?\b", r"\btouchdown",
    r"\bhomerun", r"\bhome run", r"\bwin on \d{4}-\d{2}-\d{2}\b",
    r"\bvs\.?\b", r"\bdefeat", r"\bbeat\b.{0,20}\b(on|in|at)\s+\d{4}-\d{2}-\d{2}\b",
    # Leagues/tours/orgs
    r"\bnfl\b", r"\bnba\b", r"\bmlb\b", r"\bnhl\b", r"\bufc\b", r"\bmma\b", r"\bboxing\b",
    r"\bmls\b", r"\bepl\b", r"\bla liga\b", r"\bserie a\b", r"\bbundesliga\b",
    r"\bchampions league\b", r"\bworld cup\b", r"\beuro\s?20\d{2}\b", r"\bolympic",
    r"\bmasters\b", r"\bopen\b.{0,10}tennis", r"\bgrand slam\b", r"\bpga\b", r"\batp\b", r"\bwta\b",
    r"\bf1\b", r"\bformula 1\b", r"\bgrand prix\b",
    r"\bvalorant\b", r"\bcsgo\b", r"\bcs:go\b", r"\bdota\b", r"\bleague of legends\b",
    # Team/club suffixes common across soccer
    r"\bfc\b", r"\bunited\b.{0,10}fc", r"\bcity fc\b", r"\bcurrent fc\b",
    # Named teams (partial list — biasing toward over-block)
    r"\blakers\b", r"\bceltics\b", r"\bwarriors\b", r"\bheat\b", r"\brockets\b",
    r"\bknicks\b", r"\bnets\b", r"\bbucks\b", r"\bthunder\b", r"\bnuggets\b",
    r"\byankees\b", r"\bdodgers\b", r"\bred sox\b",
    r"\bpatriots\b", r"\bchiefs\b", r"\beagles\b", r"\bcowboys\b",
    r"\b(red|blue) bulls\b",
    # NBA / NFL / MLB / NHL star players (partial)
    r"\bshai gilgeous", r"\bluka doncic", r"\blebron\b", r"\bkevin durant\b",
    r"\bstephen curry\b", r"\bgiannis\b", r"\bjokic\b",
    r"\bmahomes\b", r"\blamar jackson\b", r"\bjosh allen\b",
]

ELECTIONS_PATTERNS = [
    r"\belection\b", r"\belectoral\b", r"\bpresidential\b", r"\bgovernor\b",
    r"\bsenator\b", r"\bsenate\b", r"\bhouse race\b", r"\bvote\b", r"\bcongress\b",
    r"\bmayor\b", r"\bnominee\b", r"\bprimary\b", r"\bdemocratic\b", r"\brepublican\b",
    r"\bapproval rating\b", r"\btrump\b", r"\bbiden\b", r"\bharris\b", r"\bvance\b",
    r"\bwhite house\b", r"\bimpeach", r"\bvice president\b", r"\bparliament\b",
    r"\bprime minister\b",
]

ENTERTAINMENT_PATTERNS = [
    r"\boscar", r"\bgrammy", r"\bemmy", r"\btony award", r"\bgolden globe",
    r"\bbox office\b", r"\bopening weekend\b", r"\btaylor swift\b", r"\bkanye\b",
    r"\bkardashian\b", r"\bbeyonce\b", r"\bdrake\b", r"\bmovie\b", r"\bfilm\b",
    r"\balbum\b", r"\bbillboard\b", r"\bnetflix\b.{0,20}(show|series|movie)",
    r"\bhbo\b", r"\bsuperbowl halftime\b", r"\bmet gala\b",
]

SPORTS_RE = re.compile("|".join(SPORTS_PATTERNS), re.IGNORECASE)
ELECTIONS_RE = re.compile("|".join(ELECTIONS_PATTERNS), re.IGNORECASE)
ENTERTAINMENT_RE = re.compile("|".join(ENTERTAINMENT_PATTERNS), re.IGNORECASE)


def classify(title):
    t = title or ""
    if SPORTS_RE.search(t):       return "sports"
    if ELECTIONS_RE.search(t):    return "elections"
    if ENTERTAINMENT_RE.search(t): return "entertainment"
    return "nv_legal"


def process_bot(bot):
    name = bot.get("name", "?")
    raw_start = bot.get("sprint_start_equity") or bot.get("starting_capital") or STARTING_CAP
    # Normalize: treat current sprint as starting from STARTING_CAP for comparability
    closed = bot.get("closed_trades", []) or []
    open_positions = bot.get("positions", []) or []

    totals = {"nv_legal": {"n": 0, "pnl": 0.0, "cost": 0.0, "wins": 0},
              "sports":   {"n": 0, "pnl": 0.0, "cost": 0.0, "wins": 0},
              "elections":{"n": 0, "pnl": 0.0, "cost": 0.0, "wins": 0},
              "entertainment":{"n": 0, "pnl": 0.0, "cost": 0.0, "wins": 0}}

    for t in closed:
        if not isinstance(t, dict):
            continue
        title = t.get("title", "")
        cat = classify(title)
        pnl = float(t.get("pnl_usd", 0.0) or 0.0)
        cost = float(t.get("cost_usd", 0.0) or 0.0)
        totals[cat]["n"] += 1
        totals[cat]["pnl"] += pnl
        totals[cat]["cost"] += cost
        if pnl > 0: totals[cat]["wins"] += 1

    # Also mark-to-market open positions
    for p in open_positions:
        if not isinstance(p, dict):
            continue
        title = p.get("title", "")
        cat = classify(title)
        upnl = float(p.get("unrealized_pnl", 0.0) or 0.0)
        cost = float(p.get("cost_usd", 0.0) or 0.0)
        totals[cat]["n"] += 1
        totals[cat]["pnl"] += upnl
        totals[cat]["cost"] += cost
        if upnl > 0: totals[cat]["wins"] += 1

    return name, totals


def main():
    # 1. Live autonomous fleet
    path = os.path.join(STATE_DIR, "auto_state.json")
    if os.path.exists(path):
        with open(path) as f:
            d = json.load(f)
        print(f"\n### Autonomous fleet — {d.get('sprint_id')}")
        print(f"{'bot':<16} {'total':>10} {'NV-legal':>10} {'sports':>10} {'elect':>8} {'entn':>8}  (n_trades by cat)")
        for b in d.get("bots", []):
            name, totals = process_bot(b)
            tot = sum(t["pnl"] for t in totals.values())
            nv = totals["nv_legal"]["pnl"]
            sp = totals["sports"]["pnl"]
            el = totals["elections"]["pnl"]
            en = totals["entertainment"]["pnl"]
            counts = f"({totals['nv_legal']['n']}/{totals['sports']['n']}/{totals['elections']['n']}/{totals['entertainment']['n']})"
            print(f"{name:<16} {tot:>+10.2f} {nv:>+10.2f} {sp:>+10.2f} {el:>+8.2f} {en:>+8.2f}  {counts}")

    # 2. Kalshi copy fleet current
    path2 = os.path.join(STATE_DIR, "state.json")
    if os.path.exists(path2):
        with open(path2) as f:
            d = json.load(f)
        print(f"\n### Kalshi copy fleet — {d.get('sprint_id')}")
        print(f"{'bot':<16} {'total':>10} {'NV-legal':>10} {'sports':>10} {'elect':>8} {'entn':>8}")
        for b in d.get("bots", []):
            name, totals = process_bot(b)
            tot = sum(t["pnl"] for t in totals.values())
            print(f"{name:<16} {tot:>+10.2f} {totals['nv_legal']['pnl']:>+10.2f} "
                  f"{totals['sports']['pnl']:>+10.2f} {totals['elections']['pnl']:>+8.2f} "
                  f"{totals['entertainment']['pnl']:>+8.2f}")

    # 3. Historical sprint results (past 30d)
    print(f"\n### Historical sprint results")
    by_bot = defaultdict(lambda: {"nv_legal":{"n":0,"pnl":0.0}, "sports":{"n":0,"pnl":0.0},
                                   "elections":{"n":0,"pnl":0.0}, "entertainment":{"n":0,"pnl":0.0}})
    sprint_files = sorted(glob.glob(os.path.join(SPRINT_DIR, "*.json")))
    for sf in sprint_files:
        try:
            with open(sf) as f:
                sd = json.load(f)
        except Exception:
            continue
        raw = sd.get("bots", []) or []
        bots = raw if isinstance(raw, list) else list(raw.values())
        for b in bots:
            if not isinstance(b, dict): continue
            name, totals = process_bot(b)
            for cat in by_bot[name]:
                by_bot[name][cat]["n"] += totals[cat]["n"]
                by_bot[name][cat]["pnl"] += totals[cat]["pnl"]

    if by_bot:
        print(f"{'bot':<16} {'tot_pnl':>10} {'NV-legal':>10} {'sports':>10} {'elect':>8} {'entn':>8}")
        rows = []
        for name, t in by_bot.items():
            total = sum(x["pnl"] for x in t.values())
            rows.append((name, total, t))
        rows.sort(key=lambda x: -x[2]["nv_legal"]["pnl"])
        for name, total, t in rows:
            print(f"{name:<16} {total:>+10.2f} {t['nv_legal']['pnl']:>+10.2f} "
                  f"{t['sports']['pnl']:>+10.2f} {t['elections']['pnl']:>+8.2f} "
                  f"{t['entertainment']['pnl']:>+8.2f}")


if __name__ == "__main__":
    main()
