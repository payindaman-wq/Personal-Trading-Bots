```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-6615 | Revised by MIMIR (Gen 6615 review)
# ══════════════════════════════════════════════════════════════════
# SHARPE=2.3513 | TRADES=1265 | WIN=40.1% | Source: elite_0.yaml
# STALLED since gen 3340 (3275+ gens). Z8 grid sweep is CRITICAL.
# ══════════════════════════════════════════════════════════════════

## YOUR ONLY JOB
Copy the YAML below. Change EXACTLY ONE value. Output the modified YAML.

```yaml
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
```

---

## HARD CONSTRAINTS — CHECK BEFORE SUBMITTING

| Constraint | Rule |
|---|---|
| stop_loss_pct | MUST be ≥ 1.70 |
| rsi long (lt) | MUST be 30–45 |
| rsi_period_hours | MUST be 18–30 |
| timeout_hours | MUST be ≤ 210 |
| Pairs | DO NOT add or remove |
| fee_rate | DO NOT change |
| size_pct / max_open / leverage | DO NOT change |
| Trade count target | Your change MUST keep trades near 1200–1300 |

**CRITICAL:** The champion produces ~1265 trades. If your change would cut trades below 800, REJECT IT and choose a different parameter. Changes that drop trades to 400–600 have Sharpe < 1.0 and are useless.

---

## WHAT TO CHANGE — PRIORITY ORDER

### PRIORITY 1 — take_profit_pct and stop_loss_pct (2D combinations)
The search is stalled. Try COMBINATIONS of these two parameters by changing one:

**take_profit_pct** (current: 4.65):
→ Try: 4.70, 4.75, 4.80, 4.85, 4.90, 4.95, 5.00, 5.10, 5.20, 5.30, 5.40, 5.50, 4.60, 4.55, 4.50

**stop_loss_pct** (current: 1.92):
→ Try: 1.95, 2.00, 2.05, 2.10, 2.15, 2.20, 2.25, 2.30, 1.90, 1.85, 1.80, 1.75
→ FLOOR = 1.70. Never go below 1.70.

Preferred: If take_profit_pct has been tried near 4.65, pick a stop_loss_pct value instead. Alternate between these two to explore the 2D surface.

### PRIORITY 2 — timeout_hours (current: 166)
→ Try: 160, 168, 172, 164, 156, 176, 180, 152, 184, 144, 192

### PRIORITY 3 — RSI entry threshold (current: 37.77)
**rsi long (lt)** — MUST stay 30–45:
→ Try: 38.0, 37.5, 38.5, 37.0, 39.0, 36.5, 39.5, 36.0, 40.0, 35.5, 35.0

**rsi_period_hours** (current: 24) — MUST stay 18–30:
→ Try: 22, 23, 25, 26, 20, 21, 18, 19, 27, 28

**rsi short (gt)** (current: 60):
→ Try: 59, 61, 58, 62, 57, 63

### PRIORITY 4 — Last resort only
**trend_period_hrs** (current: 48): → 36, 42, 54, 60, 72
**pause_if_down_pct** (current: 8): → 6, 7, 9, 10
**stop_if_down_pct** (current: 18): → 15, 16, 17, 20, 22

---

## KNOWN-BAD — DO NOT REPRODUCE

- stop_loss_pct < 1.70 → always bad
- rsi long (lt) > 45 → bad Sharpe
- rsi long (lt) < 30 → bad Sharpe
- timeout_hours > 210 → reject
- Any config producing < 800 trades → reject
- These trade counts are known poisoned: ~84, ~143, ~190, ~185, ~174, ~224, ~178, ~158, ~239

---

## FINAL CHECKLIST

Before outputting, verify:
- [ ] Copied YAML exactly — only ONE value changed
- [ ] Changed value is NOT the current champion value (4.65 / 1.92 / 166 / 37.77 / 60 / 24 / 48)
- [ ] stop_loss_pct ≥ 1.70
- [ ] rsi long (lt) between 30 and 45
- [ ] timeout_hours ≤ 210
- [ ] Expected trade count: 800–3000 (champion is 1265; stay close)

Output ONLY the YAML. No explanation needed.

---
# ══════════════════════════════════════════════════════════════════
# OPERATOR NOTES (not sent to LLM)
# ══════════════════════════════════════════════════════════════════
# [STATUS] Stalled since gen 3340. 3275+ gens no improvement.
#          Dedup rate ~65%. Random single-param walk exhausted.
# [Z8]  CRITICAL PATH: Run full 2D grid sweep take_profit_pct ×
#       stop_loss_pct (~150 backtests). LLM sampling cannot find
#       improvement without systematic coverage. Human action required.
# [Z4]  Confirm APT/SUI/ARB/OP have ≥17,520 candles before live deploy.
# [Z9]  Live deployment blocked until Z4+Z8 complete.
#       Macro = CAUTION. Live sizing = 50% of normal only.
#       Do NOT change size_pct in YAML (keep 25 for comparability).
# [Z10] Gen gap 5031→5944 (913 gens missing). Investigate log writes.
# [BUG-2] elite_0.yaml may lag in-memory champion. Fix: write on every accept.
# [BUG-4] Clone detection is post-backtest. Fix: pre-backtest SHA-256 gate.
# [BUG-5] Poison attractor (~84-190t) bypassing MIN_TRADES=400 gate
#          sporadically (seen gen 6607: 84t, gen 6613: 143t).
#          Gate must be applied PRE-backtest. Verify enforcement.
# [NOTE] Champion regime: ~1265 trades, 40.1% win, 4.65/1.92 R:R=2.42.
#        LLM proposals yielding 444-524 trades are structurally wrong.
#        Adding trade-count awareness to prompt (800-trade floor guidance).
# ══════════════════════════════════════════════════════════════════
```

---