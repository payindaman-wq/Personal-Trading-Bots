```markdown
# ODIN Research Program — FUTURES SWING
# Version: Post-Gen-6954 | Revised by MIMIR (Gen 6954 review)
# Sharpe=2.3513 | Trades=1265 | Win=40.1% | Stalled since gen 3340

## OUTPUT RULE
Output ONLY the modified YAML. One value changed. Nothing else.

---
## TEMPLATE — COPY EXACTLY, CHANGE ONE VALUE

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
## HARD LIMITS — VIOLATION = DISCARD

| Parameter | Rule |
|---|---|
| stop_loss_pct | ≥ 1.70, ≤ 2.30 |
| rsi long (lt) | 33–44 ONLY |
| rsi_period_hours | 18–30 ONLY |
| timeout_hours | ≤ 210 |
| Pairs | DO NOT change |
| fee_rate / size_pct / max_open / leverage | DO NOT change |

**TRADE COUNT RULE:** Your change must produce ~1000–1500 trades.
If you are unsure, pick from PRIORITY 1 values below — they are safe.

---
## WHAT TO CHANGE — PICK ONE FROM THIS LIST IN ORDER

### PRIORITY 1 — take_profit_pct (current: 4.65)
Change take_profit_pct to ONE of these values (pick the first untried):
4.70 | 4.75 | 4.80 | 4.85 | 4.90 | 4.95 | 5.00 | 5.10 | 5.20 | 5.30 | 4.60 | 4.55 | 4.50 | 4.45 | 5.40 | 5.50

### PRIORITY 2 — stop_loss_pct (current: 1.92)
Change stop_loss_pct to ONE of these values:
1.95 | 2.00 | 2.05 | 2.10 | 2.15 | 2.20 | 1.90 | 1.85 | 1.80 | 1.75
FLOOR = 1.70. CEILING = 2.30. Never go outside this range.

### PRIORITY 3 — timeout_hours (current: 166)
Change timeout_hours to ONE of these values:
160 | 168 | 172 | 164 | 156 | 176 | 180 | 152 | 184 | 144 | 192

### PRIORITY 4 — RSI thresholds
rsi long lt (current: 37.77) — RANGE 33–44:
38.0 | 37.5 | 38.5 | 37.0 | 39.0 | 36.5 | 39.5 | 36.0 | 40.0 | 35.5

rsi short gt (current: 60):
59 | 61 | 58 | 62 | 57

rsi_period_hours (current: 24) — RANGE 18–30:
22 | 23 | 25 | 26 | 20 | 21 | 27 | 28

### PRIORITY 5 — Last resort only
trend period_hours (current: 48): 36 | 42 | 54 | 60 | 72
pause_if_down_pct (current: 8): 6 | 7 | 9 | 10
stop_if_down_pct (current: 18): 15 | 16 | 17 | 20 | 22

---
## KNOWN BAD — DO NOT USE

- stop_loss_pct < 1.70 → always fails
- stop_loss_pct > 2.30 → too few trades
- rsi long lt < 33 or > 44 → always fails
- timeout_hours > 210 → reject
- Any combination previously producing < 800 trades → reject
- These exact values are ALREADY the champion — do not reproduce:
  take_profit_pct=4.65, stop_loss_pct=1.92, timeout_hours=166,
  rsi_lt=37.77, rsi_gt=60, rsi_period=24, trend_period=48

---
## CHECKLIST BEFORE OUTPUT

- [ ] Exactly ONE value changed from template
- [ ] Changed value differs from current champion value listed above
- [ ] stop_loss_pct is between 1.70 and 2.30
- [ ] rsi long lt is between 33 and 44
- [ ] timeout_hours ≤ 210
- [ ] Pairs, fee_rate, size_pct, max_open, leverage are unchanged

Output ONLY the YAML.
```

---
# OPERATOR NOTES (not sent to LLM)
# ══════════════════════════════════════════════════════════════════
# [STATUS] Stalled since gen 3340. 3614+ gens no improvement.
#          Dedup rate ~50% in last 20 gens. LLM attractor ~450-530t.
# [CRITICAL] MIN_TRADES[futures_swing] must be raised to 800 in code.
#            Current gate=400 allows 400-800 trade configs to waste
#            compute. See STRUCTURAL_PATCH below.
# [Z8]  CRITICAL PATH: Human must run full 2D grid sweep:
#       take_profit_pct: 4.45,4.50,4.55,4.60,4.70,4.75,4.80,4.85,
#                        4.90,4.95,5.00,5.10,5.20,5.30,5.40,5.50
#       stop_loss_pct:   1.70,1.75,1.80,1.85,1.90,1.95,2.00,2.05,
#                        2.10,2.15,2.20,2.25,2.30
#       = ~208 backtests. LLM random walk cannot cover this surface.
# [Z4]  Confirm APT/SUI/ARB/OP have ≥17,520 candles before live.
# [Z9]  Live blocked until Z4+Z8 complete. Macro=CAUTION. Size=50%.
# [Z10] Gen gap 5031→5944 (913 gens). Investigate log write failures.
# [BUG-2] elite_0.yaml may lag in-memory champion. Write on every accept.
# [BUG-4] Clone detection is post-backtest. Add pre-backtest SHA-256 gate.
# [BUG-5] Poison attractor (84-526t) bypassing MIN_TRADES=400 gate.
#          Gate must be raised to 800 and enforced PRE-backtest.
# [NOTE] RSI attractor: LLM keeps proposing rsi_lt ~32-34 → ~450-530t.
#        Prompt now restricts rsi long lt floor to 33 (was 30).
# ══════════════════════════════════════════════════════════════════
```

---