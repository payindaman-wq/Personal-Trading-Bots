```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-6117 | Revised by MIMIR

# ══════════════════════════════════════════════════════════════════
# CHAMPION YAML — COPY EXACTLY, CHANGE EXACTLY ONE VALUE
# ══════════════════════════════════════════════════════════════════
# Sharpe=2.3513 | Trades=1265 | Win=40.1% | elite_0.yaml

name: crossover
style: swing_momentum
league: futures_swing
leverage: 2
pairs:
- BTC/USD
- ETH/USD
- SOL/USD
- XRP/USD
- DOGE/USD
- AVAX/USD
- LINK/USD
- UNI/USD
- AAVE/USD
- NEAR/USD
- APT/USD
- SUI/USD
- ARB/USD
- OP/USD
- ADA/USD
- POL/USD
position:
  size_pct: 25
  max_open: 3
  fee_rate: 0.0005
entry:
  long:
    conditions:
    - indicator: trend
      period_hours: 48
      operator: eq
      value: up
    - indicator: rsi
      period_hours: 24
      operator: lt
      value: 37.77
  short:
    conditions:
    - indicator: trend
      period_hours: 48
      operator: eq
      value: down
    - indicator: rsi
      period_hours: 24
      operator: gt
      value: 60
exit:
  take_profit_pct: 4.65
  stop_loss_pct: 1.92
  timeout_hours: 166
risk:
  pause_if_down_pct: 8
  pause_minutes: 120
  stop_if_down_pct: 18

# ══════════════════════════════════════════════════════════════════
# HARD REJECT RULES — check BEFORE submitting, automatic fail:
# ══════════════════════════════════════════════════════════════════
# □ stop_loss_pct < 1.70              → REJECT
# □ rsi long (lt) value > 45 or < 30 → REJECT
# □ rsi_period_hours < 18 or > 30    → REJECT
# □ timeout_hours > 210              → REJECT
# □ trades outside 400–3000          → REJECT
# □ fee_rate changed                 → REJECT
# □ pairs added or removed           → REJECT
# □ more than ONE value changed      → REJECT
# □ identical to champion above      → REJECT

# ══════════════════════════════════════════════════════════════════
# PRIORITY 1 — MICRO-GRID (highest expected value — try these first)
# ══════════════════════════════════════════════════════════════════
# The champion is near a local optimum. Try fine-grained steps
# ADJACENT to the champion values before larger moves.
#
# take_profit_pct  4.65  →  TRY: 4.62, 4.63, 4.64, 4.66, 4.67,
#                                4.68, 4.69, 4.71, 4.72, 4.73,
#                                4.74, 4.76, 4.77, 4.78, 4.79
#
# stop_loss_pct    1.92  →  TRY: 1.88, 1.89, 1.90, 1.91, 1.93,
#                                1.94, 1.96, 1.97, 1.98, 1.99,
#                                2.01, 2.02, 2.03, 2.04, 2.06
#
# timeout_hours    166   →  TRY: 162, 163, 164, 165, 167, 168,
#                                169, 170, 171, 172, 158, 174,
#                                176, 178, 180
#
# rsi long (lt)   37.77  →  TRY: 37.3, 37.5, 37.6, 37.8, 37.9,
#                                38.0, 38.1, 38.2, 38.3, 38.4,
#                                38.5, 38.6, 38.7, 38.8, 38.9

# ══════════════════════════════════════════════════════════════════
# PRIORITY 2 — WIDER GRID (if micro-grid values are exhausted)
# ══════════════════════════════════════════════════════════════════
# take_profit_pct  →  4.80, 4.85, 4.90, 4.95, 5.00, 5.05, 5.10,
#                     5.15, 5.20, 5.30, 5.40, 5.50, 4.55, 4.50,
#                     4.45, 4.40
#
# stop_loss_pct    →  2.10, 2.15, 2.20, 2.25, 2.30, 2.35, 2.40,
#                     1.85, 1.80, 1.75, 1.70  ← hard floor
#
# rsi_period_hours →  22, 23, 25, 26, 20, 21, 27, 28, 19, 18
#                     (current=24, do NOT reuse 24)
#
# rsi short (gt)   →  59, 61, 58, 62, 57, 63

# ══════════════════════════════════════════════════════════════════
# PRIORITY 3 — LAST RESORT (only if P1+P2 fully exhausted)
# ══════════════════════════════════════════════════════════════════
# trend_period_hours  48  →  42, 54, 36, 60, 72
# pause_if_down_pct    8  →  7, 9, 6, 10
# stop_if_down_pct    18  →  16, 17, 20, 22, 15

# ══════════════════════════════════════════════════════════════════
# DO NOT CHANGE THESE (confirmed bad or structurally fixed):
# ══════════════════════════════════════════════════════════════════
# size_pct = 25        (fixed for backtest comparability)
# max_open = 3         (changing to 2 drops trades ~40%, kills Sharpe)
# fee_rate = 0.0005    (fixed)
# leverage = 2         (fixed)

# ══════════════════════════════════════════════════════════════════
# KNOWN-BAD SIGNATURES — do not reproduce any of these:
# ══════════════════════════════════════════════════════════════════
# (190t, −1.05), (190t, −1.63), (185t, −0.79), (174t, −1.96),
# (224t, −1.73), (178t, −0.80), (182t, −1.86), (158t, −2.08),
# (239t, −2.41), (397t, −0.54), (461t, −0.46), (220t, −0.84),
# (230t, −1.32), (115t, −0.43), (502t, +0.87), (501t, +1.00),
# (505t, +0.84), (708t, +0.36), (457t, +1.04)
# → Any config producing ~500 trades has already been tested and discarded.
# → stop_loss_pct < 1.70: confirmed catastrophic, do not try.
# → max_open=2 or trend_period=24: confirmed trade-count killer.

# ══════════════════════════════════════════════════════════════════
# VERIFICATION CHECKLIST (run before submitting)
# ══════════════════════════════════════════════════════════════════
# □ Copied YAML exactly from champion above
# □ Changed EXACTLY ONE parameter
# □ New value is NOT in KNOWN-BAD list
# □ New value is NOT the current champion value
# □ All HARD REJECT RULES pass
# □ Estimated trade count: 400–3000
# □ This exact config not submitted before

# ══════════════════════════════════════════════════════════════════
# INFRASTRUCTURE NOTES (human operator — do not send to LLM)
# ══════════════════════════════════════════════════════════════════
# [BUG-2] elite_0.yaml may lag in-memory champion. Fix: write on every accept.
# [BUG-4] Clone detection is post-backtest. Fix: pre-backtest SHA-256 gate.
# [BUG-5] Poison attractor (~190t). Fix: pre-backtest trade-count gate.
# [Z4]  Confirm APT/SUI/ARB/OP/POL have ≥17,520 candles before live deploy.
# [Z8]  CRITICAL: Run systematic 2D grid: take_profit_pct (4.40–5.50, step 0.10)
#       × stop_loss_pct (1.70–2.50, step 0.08) = ~150 backtests.
#       Random LLM sampling is exhausted after 6,100 gens / 10 improvements.
#       Systematic grid is REQUIRED before further LLM random search.
# [Z9]  Live deployment blocked until Z4+Z8 complete.
#       Macro = CAUTION. Live sizing = 50% only. Keep size_pct=25 in YAML.
# [Z10] Gen gap 5031→5944 (913 gens missing). Investigate log integrity.
#       Champion at 2.3513 may reflect an unlogged improvement above gen 3340.
# [Z11] Dedup-reject rate ~60% in last 20 gens = search space exhausted.
#       Top priority: implement pre-backtest SHA-256 gate (BUG-4) to stop
#       wasting backtest compute on already-tested configs.
# [Z12] Non-monotonic gen numbers in LOKI log (gen 5257 appearing after 9000)
#       suggests session resets or log corruption. Audit log integrity.
```

---