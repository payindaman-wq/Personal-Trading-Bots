```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 23601 | Incumbent (STORED): Sharpe=1.3445, trades=58
# TRUE PERFORMANCE TARGET: Gen 20502, Sharpe=1.6060, trades=54
# MIMIR-reviewed 2026-04-18 (v46)
#
# ══════════════════════════════════════════════════════════════════════
# CRITICAL SITUATION SUMMARY (READ THIS FIRST — 30 SECONDS)
# ══════════════════════════════════════════════════════════════════════
#
# STORED CHAMPION: Sharpe=1.3445, trades=58 (elite_0.yaml — GROUND TRUTH)
# RESEARCH TARGET: Sharpe=1.6060, trades=54 (Gen 20502 — must be restored)
#
# THE SYSTEM WILL ACCEPT ANYTHING > 1.3445.
# THE GEN 20502 BASE YAML ALONE SCORES ≈1.60 AND WILL BE A NEW BEST.
# JUST OUTPUT THE CORRECT YAML AND IT WILL IMPROVE THE STORED CHAMPION.
#
# ══════════════════════════════════════════════════════════════════════
# ████████████████████████████████████████████████████████████████████
# █  STEP 1 — OUTPUT THIS YAML EXACTLY. NO CHANGES. DO NOT READ AHEAD.█
# ████████████████████████████████████████████████████████████████████
#
# ```yaml
# name: gen20502_rsi35
# style: randomly generated
# pairs:
# - BTC/USD
# - ETH/USD
# - SOL/USD
# position:
#   size_pct: 25.0
#   max_open: 2
#   fee_rate: 0.001
# entry:
#   long:
#     conditions:
#     - indicator: momentum_accelerating
#       period_hours: 48
#       operator: eq
#       value: false
#     - indicator: bollinger_position
#       period_hours: 48
#       operator: eq
#       value: below_lower
#     - indicator: macd_signal
#       period_hours: 48
#       operator: eq
#       value: bullish
#     - indicator: price_change_pct
#       period_hours: 24
#       operator: lt
#       value: -0.5
#     - indicator: rsi
#       period_hours: 14
#       operator: lt
#       value: 35.0
#   short:
#     conditions:
#     - indicator: momentum_accelerating
#       period_hours: 48
#       operator: eq
#       value: false
#     - indicator: bollinger_position
#       period_hours: 168
#       operator: eq
#       value: above_upper
#     - indicator: macd_signal
#       period_hours: 24
#       operator: eq
#       value: bearish
#     - indicator: price_change_pct
#       period_hours: 24
#       operator: gt
#       value: 0.54
# exit:
#   take_profit_pct: 9.5
#   stop_loss_pct: 1.5
#   timeout_hours: 156
# risk:
#   pause_if_down_pct: 8
#   stop_if_down_pct: 18
#   pause_hours: 48
# ```
#
# ████████████████████████████████████████████████████████████████████
# █  STEP 1 COMPLETE. ONLY NOW READ THE REST.                         █
# ████████████████████████████████████████████████████████████████████
#
# ══════════════════════════════════════════════════════════════════════
# POISON CHECK — 5 RULES. FAIL ANY ONE → DISCARD AND USE STEP 1.
# ══════════════════════════════════════════════════════════════════════
#
# ✗ Rule 1: pairs must be [BTC/USD, ETH/USD, SOL/USD]  (3 pairs, not 1)
# ✗ Rule 2: size_pct must be 25.0  (not 30)
# ✗ Rule 3: max_open must be 2  (not 3)
# ✗ Rule 4: take_profit_pct must be 9.5  (not 6.63)
# ✗ Rule 5: timeout_hours must be 156  (not 129 or 133)
#
# POISON RESULT SIGNATURES — if you get either of these, your YAML is wrong:
#   trades=58, Sharpe≈1.34  →  you used the wrong base (BTC/USD only, size=30)
#   trades=0,  Sharpe=0.00  →  malformed YAML or too many conditions
#
# If your result is trades≥50 and Sharpe>1.34 → VALID. Report result.
#
# ══════════════════════════════════════════════════════════════════════
# WHAT CHANGE IS BEING TESTED (D7b)
# ══════════════════════════════════════════════════════════════════════
#
# ONE CHANGE from the Gen 20502 base:
#   rsi long entry value: 32.96 → 35.0  (slightly relaxed entry filter)
#   This is already in the STEP 1 YAML above.
#   Do not make any other changes.
#
# Why this test: RSI=35 relaxes the entry threshold slightly.
# If trades increase above 65: entry too loose → D7c will use rsi=33.5
# If trades stay 50-65 and Sharpe improves: RSI sensitivity confirmed
# If Sharpe drops vs. base: RSI=35 is worse → D7c will use rsi=33.5
#
# ══════════════════════════════════════════════════════════════════════
# RESULT CLASSIFICATION (WHAT TO DO NEXT)
# ══════════════════════════════════════════════════════════════════════
#
# trades=0,  Sharpe=0.00  [POISON/MALFORMED] → Discard. Use STEP 1 YAML.
# trades=58, Sharpe≈1.34  [POISON BASE]      → Discard. Use STEP 1 YAML.
# trades=54, Sharpe≈1.60  [BASE, NO CHANGE]  → Confirm rsi=35.0 in YAML.
# trades≥50, Sharpe>1.60  [NEW BEST]         → Report success. Advance to D7c.
# trades≥50, Sharpe≥1.34  [VALID DISCARD]    → D7b tested. Mark dead. Move to D7c.
# trades>65               [TOO LOOSE]        → D7b dead. D7c: rsi=33.5.
# Sharpe<0                [CATASTROPHIC]     → Multiple params changed. Check YAML.
#
# ══════════════════════════════════════════════════════════════════════
# THE CORRECT BASE YAML (FOR REFERENCE — MUTATE FROM THIS)
# ══════════════════════════════════════════════════════════════════════
#
# Gen 20502 approximation — Sharpe=1.6027, trades=54, WR=44.4%
# TRUE incumbent Sharpe=1.6060. Stored champion Sharpe=1.3445.
# ANY valid test from this base will be a new stored best if Sharpe>1.3445.
#
# ```yaml
# name: gen20502_approximation
# style: randomly generated
# pairs:
# - BTC/USD
# - ETH/USD
# - SOL/USD
# position:
#   size_pct: 25.0
#   max_open: 2
#   fee_rate: 0.001
# entry:
#   long:
#     conditions:
#     - indicator: momentum_accelerating
#       period_hours: 48
#       operator: eq
#       value: false
#     - indicator: bollinger_position
#       period_hours: 48
#       operator: eq
#       value: below_lower
#     - indicator: macd_signal
#       period_hours: 48
#       operator: eq
#       value: bullish
#     - indicator: price_change_pct
#       period_hours: 24
#       operator: lt
#       value: -0.5
#     - indicator: rsi
#       period_hours: 14
#       operator: lt
#       value: 32.96
#   short:
#     conditions:
#     - indicator: momentum_accelerating
#       period_hours: 48
#       operator: eq
#       value: false
#     - indicator: bollinger_position
#       period_hours: 168
#       operator: eq
#       value: above_upper
#     - indicator: macd_signal
#       period_hours: 24
#       operator: eq
#       value: bearish
#     - indicator: price_change_pct
#       period_hours: 24
#       operator: gt
#       value: 0.54
# exit:
#   take_profit_pct: 9.5
#   stop_loss_pct: 1.5
#   timeout_hours: 156
# risk:
#   pause_if_down_pct: 8
#   stop_if_down_pct: 18
#   pause_hours: 48
# ```
#
# ══════════════════════════════════════════════════════════════════════
# D-SERIES TEST QUEUE (CONDENSED)
# ══════════════════════════════════════════════════════════════════════
#
# PRIORITY: Entry conditions only. Exit/risk changes don't improve Sharpe.
#
# D7b: rsi → 35.0           ← ACTIVE (Step 1 YAML above)
# D7c: rsi → 33.5           (if D7b dead/too loose)
# D7d: rsi → 31.5           (if D7c dead; retry of original D7a direction)
#
# D8a: long price_change_pct → -1.0   (after D7 resolves)
# D8b: long price_change_pct → -0.75  (if D8a dead)
# D8c: long price_change_pct → -0.3   (if D8b dead)
#
# D6a: long bollinger period_hours → 36   (after D8 resolves)
# D6b: long bollinger period_hours → 60   (if D6a dead)
#
# D9a: short price_change_pct → 1.0       (after D6 resolves)
# D9b: short bollinger period_hours → 72  (if D9a dead)
#
# SUSPENDED (exit/risk — no Sharpe gains observed from these):
#   D2:  stop_if_down_pct → 20
#   D3:  pause_hours variations
#   D4:  timeout_hours variations (129,133,135,138,144,168,192,216 all tested/dead)
#   D5:  take_profit_pct variations (6.63,7.14,7.36,7.38,10.0-11.5 all dead)
#
# DEAD (confirmed no improvement):
#   D1:  pause_if_down_pct → 10  (800+ gens, confirmed dead)
#
# ══════════════════════════════════════════════════════════════════════
# INCUMBENT TRAJECTORY (confirmed improvements only)
# ══════════════════════════════════════════════════════════════════════
#
#   Gen 19808: Sharpe=1.3483, trades=58, WR=41.4%
#   Gen 20475: Sharpe=1.4877, trades=55, WR=43.6%  (+0.139) entry change
#   Gen 20492: Sharpe=1.4898, trades=52, WR=50.0%  (+0.002) entry change
#   Gen 20502: Sharpe=1.6060, trades=54, WR=44.4%  (+0.116) TRUE PEAK
#
#   Gen 22157: Sharpe=1.3604  ← INCORRECTLY ACCEPTED. POISON. CORRUPTED ELITE.
#   Gen 22174: Sharpe=1.4449, trades=51  ← valid but below Gen 20502
#   Gen 23010: Sharpe=1.3595, trades=58  ← poison fingerprint accepted
#
#   STORED CHAMPION NOW: Sharpe=1.3445, trades=58 (corrupted — must restore)
#   RESTORE TARGET:      Sharpe=1.6060 (Gen 20502 base alone achieves ≈1.6027)
#
# KEY INSIGHT: Every large Sharpe gain came from entry condition changes.
# Trade count decreased (58→54) as Sharpe rose. Fewer, better-filtered = better.
# VALID RESULT RANGE: 50 ≤ trades ≤ 65.
#
# ══════════════════════════════════════════════════════════════════════
# MACRO CONTEXT (TYR Risk Officer — 2026-04-18)
# ══════════════════════════════════════════════════════════════════════
#
# F&G = 26 (Fear). BTC Dominance = 57.32%. Regime: CAUTION.
# TYR Directive: Reduce live position sizes to 50% of normal.
# Fear regime is FAVORABLE for this strategy's long entry logic.
# RSI<35 + below Bollinger lower + MACD bullish = fear capitulation setup.
# Backtest Sharpe=1.6060 was earned in similar regimes.
# Live sizing: 50% reduction per TYR directive regardless of backtest.
#
# ══════════════════════════════════════════════════════════════════════
# FINAL YAML CHECKLIST — VERIFY BEFORE SUBMITTING
# ══════════════════════════════════════════════════════════════════════
#
# ✓ name               = gen20502_rsi35
# ✓ pairs              = BTC/USD, ETH/USD, SOL/USD  (3 pairs — NOT just BTC)
# ✓ size_pct           = 25.0  (NOT 30)
# ✓ max_open           = 2     (NOT 3)
# ✓ fee_rate           = 0.001
# ✓ long momentum_accelerating   period=48, eq, false
# ✓ long bollinger_position       period=48, eq, below_lower
# ✓ long macd_signal              period=48, eq, bullish
# ✓ long price_change_pct         period=24, lt, -0.5
# ✓ long rsi                      period=14, lt, 35.0   ← THE ONE CHANGE
# ✓ short momentum_accelerating  period=48, eq, false
# ✓ short bollinger_position      period=168, eq, above_upper
# ✓ short macd_signal             period=24, eq, bearish
# ✓ short price_change_pct        period=24, gt, 0.54
# ✓ take_profit_pct    = 9.5   (NOT 6.63)
# ✓ stop_loss_pct      = 1.5
# ✓ timeout_hours      = 156   (NOT 129 or 133)
# ✓ pause_if_down_pct  = 8
# ✓ stop_if_down_pct   = 18
# ✓ pause_hours        = 48
```

---