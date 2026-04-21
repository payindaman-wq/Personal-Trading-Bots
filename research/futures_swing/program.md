```markdown
# ODIN Research Program — FUTURES SWING
# Sharpe=2.3513 | Trades=1265 | Win=40.1% | Gen 3340 (stalled 3444+ gens)
# ══════════════════════════════════════════════════════════════════

## YOUR ONLY JOB
Copy the YAML below. Change EXACTLY ONE numeric value. Output ONLY the modified YAML.

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

## HARD RULES (check these BEFORE submitting)

| Parameter | Rule |
|---|---|
| stop_loss_pct | ≥ 1.70 always |
| rsi long (lt) | 30–45 only |
| rsi_period_hours | 18–30 only |
| timeout_hours | ≤ 210 only |
| pairs / fee_rate / size_pct / max_open / leverage | DO NOT CHANGE |
| Expected trades | Must stay 1000–1500. If your change would drop trades below 1000, pick a different value. |

**REJECT your proposal if it produces fewer than 1000 trades. The champion has 1265 trades. Low-trade configs (under 800) always have Sharpe below 1.0 and are useless.**

---

## WHAT TO CHANGE — FOLLOW THIS ORDER

### #1 PRIORITY: take_profit_pct (current: 4.65)
Try ONE value from this list (pick one not recently tried):
4.70 | 4.75 | 4.80 | 4.85 | 4.90 | 4.95 | 5.00 | 5.10 | 5.20 | 5.30 | 5.40 | 5.50 | 4.60 | 4.55 | 4.50

### #2 PRIORITY: stop_loss_pct (current: 1.92)
Try ONE value from this list:
1.95 | 2.00 | 2.05 | 2.10 | 2.15 | 2.20 | 2.25 | 2.30 | 1.90 | 1.85 | 1.80 | 1.75
**FLOOR = 1.70. Never go below 1.70.**

### #3 PRIORITY: timeout_hours (current: 166)
Try: 160 | 168 | 172 | 164 | 156 | 176 | 180 | 152 | 184 | 144 | 192

### #4 PRIORITY: RSI thresholds
- rsi long (lt), current 37.77 → try: 38.0 | 37.5 | 38.5 | 37.0 | 39.0 | 36.5 | 39.5 | 36.0 | 40.0 | 35.5
- rsi short (gt), current 60 → try: 59 | 61 | 58 | 62 | 57
- rsi period_hours, current 24 → try: 22 | 23 | 25 | 26 | 20 | 21

### #5 LAST RESORT ONLY
- trend period_hours (48) → 36 | 42 | 54 | 60 | 72
- pause_if_down_pct (8) → 6 | 7 | 9 | 10
- stop_if_down_pct (18) → 15 | 16 | 17 | 20 | 22

**Alternate between #1 and #2 on consecutive proposals to explore the 2D surface.**

---

## KNOWN BAD — DO NOT USE

- stop_loss_pct < 1.70 → always fails
- rsi long (lt) > 45 or < 30 → always fails
- timeout_hours > 210 → reject
- Any config with < 1000 trades → reject
- These exact values are poisoned attractors: take_profit_pct=4.65 + stop_loss_pct=1.92 together (that is the unchanged champion — you must change exactly one)

---

## FINAL CHECK

Before outputting, confirm:
- [ ] Exactly ONE value changed from the champion YAML above
- [ ] Changed value is different from current champion value
- [ ] stop_loss_pct ≥ 1.70
- [ ] rsi long (lt) between 30 and 45
- [ ] timeout_hours ≤ 210
- [ ] Change will NOT drop trades below 1000

Output ONLY the YAML. No commentary.

---
# ══════════════════════════════════════════════════════════════════
# OPERATOR NOTES (not sent to LLM)
# ══════════════════════════════════════════════════════════════════
# [CRITICAL-Z8] Run full 2D grid: take_profit_pct × stop_loss_pct
#   take_profit_pct: 4.50, 4.55, 4.60, 4.65, 4.70, 4.75, 4.80, 4.85,
#                   4.90, 4.95, 5.00, 5.10, 5.20, 5.30, 5.40, 5.50
#   stop_loss_pct:  1.70, 1.75, 1.80, 1.85, 1.90, 1.92, 1.95, 2.00,
#                   2.05, 2.10, 2.15, 2.20, 2.25, 2.30
#   ~224 backtests. LLM random walk CANNOT cover this. Human action needed.
#   Z8 is the primary unlock. Live deployment blocked until Z8+Z4 complete.
#
# [CRITICAL-MIN_TRADES] MIN_TRADES[futures_swing] must be raised to 1000.
#   Current value 400 allows 400-999 trade configs to waste backtest cycles.
#   Champion regime is 1263-1272 trades. 400-trade configs = Sharpe < 1.0.
#   BUG-5 (poison attractor bypassing gate) needs pre-backtest SHA-256 gate.
#
# [BUG-2] elite_0.yaml may lag in-memory champion. YAML shows 2.3513,
#   improvement log last shows 2.3494. Difference = 0.0019. Write on every accept.
# [BUG-4] Clone detection is post-backtest. Add pre-backtest SHA-256 gate.
# [BUG-5] Poison attractor (~84-190t) bypassing MIN_TRADES gate sporadically.
#   Apply gate PRE-backtest. Verify MIN_TRADES enforcement after raising to 1000.
# [Z4]  Confirm APT/SUI/ARB/OP have ≥17,520 candles before live deploy.
# [Z9]  Live deployment blocked until Z4+Z8 complete. Macro=CAUTION. 50% sizing.
# [Z10] Gen gap 5031→5944 (913 gens missing). Investigate log writes.
# [NOTE] Dedup rate ~65% in recent gens = LLM cycling same attractor basin.
#        Prompt has been shortened and restructured to YAML-first format.
#        If dedup rate remains >50% after this revision, consider adding
#        a "recently tried values" ban list injected per-generation.
# ══════════════════════════════════════════════════════════════════
```

---