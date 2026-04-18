```markdown
# ODIN Research Program — Swing Trading Strategy Optimizer
# Effective from Gen 23933 | Incumbent (STORED): Sharpe=1.6344, trades=54
# MIMIR-reviewed 2026-04-18 (v47)
#
# ══════════════════════════════════════════════════════════════════════
# SITUATION SUMMARY (READ THIS FIRST — 30 SECONDS)
# ══════════════════════════════════════════════════════════════════════
#
# STORED CHAMPION: Sharpe=1.6344, trades=54, WR=44.4% (elite_0.yaml — GROUND TRUTH)
# RESEARCH GOAL:   Beat Sharpe=1.6344 by tuning entry conditions only
#
# THE CHAMPION IS REAL AND STORED. DO NOT TRY TO RESTORE ANYTHING.
# JUST MAKE ONE SMALL CHANGE TO THE CHAMPION YAML BELOW AND SUBMIT.
#
# ══════════════════════════════════════════════════════════════════════
# ████████████████████████████████████████████████████████████████████
# █  STEP 1 — OUTPUT THIS YAML WITH EXACTLY ONE CHANGE (SEE STEP 2). █
# ████████████████████████████████████████████████████████████████████
#
# CHAMPION BASE YAML (Sharpe=1.6344, trades=54):
#
# ```yaml
# name: gen23933_d8a
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
#       value: -1.0
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
# █  STEP 2 — THE ONE CHANGE IN THIS YAML (vs. champion)             █
# ████████████████████████████████████████████████████████████████████
#
# ACTIVE TEST: D8a
#   long price_change_pct value: -0.5 → -1.0
#   (Requires a larger dip before entering long — higher quality entries)
#   This is the ONLY change. Everything else is identical to the champion.
#
# WHY: The champion enters on -0.5% dips. Testing -1.0% requires a deeper
# pullback, which may improve entry quality and win rate.
# If trades drop below 40: too restrictive → D8b will use -0.75
# If trades stay 45-65 and Sharpe improves: confirmed improvement
# If Sharpe drops: D8b will use -0.75
#
# ══════════════════════════════════════════════════════════════════════
# POISON CHECK — FAIL ANY ONE → DISCARD AND RESUBMIT STEP 1 YAML
# ══════════════════════════════════════════════════════════════════════
#
# ✗ Rule 1: pairs must be [BTC/USD, ETH/USD, SOL/USD]  (3 pairs, not 1)
# ✗ Rule 2: size_pct must be 25.0  (not 22.67 or 30)
# ✗ Rule 3: max_open must be 2
# ✗ Rule 4: take_profit_pct must be 9.5  (not 6.63)
# ✗ Rule 5: timeout_hours must be 156  (not 129, 132, or 133)
# ✗ Rule 6: rsi value must be 35.0  (not 32.5 or 32.96)
# ✗ Rule 7: long price_change_pct must be -1.0  (not -0.5)
#
# POISON RESULT SIGNATURES — if you get any of these, your YAML is wrong:
#   trades=54, Sharpe≈1.6344  →  CLONE — you made no change. Check Rule 7.
#   trades=58, Sharpe≈1.34    →  wrong base (BTC/USD only, size=22.67)
#   trades=0,  Sharpe=0.00    →  malformed YAML or too many conditions
#   trades=60, Sharpe≈1.34    →  old corrupted base, wrong pairs/size
#
# VALID RESULT: trades between 35 and 65, Sharpe computed (any value)
#
# ══════════════════════════════════════════════════════════════════════
# RESULT CLASSIFICATION
# ══════════════════════════════════════════════════════════════════════
#
# trades=0,  Sharpe=0.00      [POISON/MALFORMED] → Discard. Resubmit Step 1.
# trades=54, Sharpe≈1.6344    [CLONE — NO CHANGE] → Check price_change_pct.
# trades=58, Sharpe≈1.34      [WRONG BASE]        → Check pairs and size_pct.
# trades<35                   [TOO RESTRICTIVE]   → D8a dead. Move to D8b (-0.75).
# trades 35-65, Sharpe>1.6344 [NEW BEST]          → Report success. Advance to D8b.
# trades 35-65, Sharpe≤1.6344 [VALID DISCARD]     → D8a tested. Move to D8b (-0.75).
# Sharpe<0                    [CATASTROPHIC]      → Multiple params changed. Check YAML.
#
# ══════════════════════════════════════════════════════════════════════
# CHAMPION YAML — EXACT VALUES (FOR REFERENCE)
# ══════════════════════════════════════════════════════════════════════
#
# Sharpe=1.6344, trades=54, WR=44.4% (Gen 23932 — CURRENT STORED CHAMPION)
# The Step 1 YAML above differs by EXACTLY ONE value: price_change_pct = -1.0
#
# Champion values for verification:
#   pairs:               BTC/USD, ETH/USD, SOL/USD
#   size_pct:            25.0
#   max_open:            2
#   long rsi:            35.0, lt, period=14
#   long price_change:   -0.5, lt, period=24   ← D8a changes this to -1.0
#   long bollinger:      below_lower, period=48
#   long macd:           bullish, period=48
#   long momentum:       false, period=48
#   short bollinger:     above_upper, period=168
#   short macd:          bearish, period=24
#   short price_change:  0.54, gt, period=24
#   short momentum:      false, period=48
#   take_profit_pct:     9.5
#   stop_loss_pct:       1.5
#   timeout_hours:       156
#   pause_if_down_pct:   8
#   stop_if_down_pct:    18
#   pause_hours:         48
#
# ══════════════════════════════════════════════════════════════════════
# D-SERIES TEST QUEUE
# ══════════════════════════════════════════════════════════════════════
#
# PRIORITY: Entry conditions only. Exit/risk changes do not improve Sharpe.
# All tests mutate from the CURRENT CHAMPION (Sharpe=1.6344), not Gen 20502.
#
# COMPLETED:
#   D7b: rsi → 35.0           ✓ COMPLETE — contributed to champion 1.6344
#
# ACTIVE:
#   D8a: long price_change_pct → -1.0   ← ACTIVE (Step 1 YAML above)
#
# QUEUED:
#   D8b: long price_change_pct → -0.75  (if D8a dead or too restrictive)
#   D8c: long price_change_pct → -0.3   (if D8b dead; loosens entry)
#
#   D6a: long bollinger period_hours → 36   (after D8 resolves)
#   D6b: long bollinger period_hours → 60   (if D6a dead)
#
#   D9a: short price_change_pct → 1.0       (after D6 resolves)
#   D9b: short bollinger period_hours → 72  (if D9a dead)
#
#   D7c: rsi → 33.5           (if D8 series all dead, revisit RSI direction)
#   D7d: rsi → 36.5           (further RSI relaxation)
#
# SUSPENDED (exit/risk — no Sharpe gains observed from these ever):
#   D2:  stop_if_down_pct variations
#   D3:  pause_hours variations
#   D4:  timeout_hours variations (129,133,135,138,144,156,168,192,216 tested)
#   D5:  take_profit_pct variations (6.63,7.14,7.36,7.38,10.0-11.5 all dead)
#
# PERMANENTLY DEAD:
#   D1:  pause_if_down_pct → 10  (800+ gens, confirmed dead)
#
# ══════════════════════════════════════════════════════════════════════
# INCUMBENT TRAJECTORY (confirmed improvements only)
# ══════════════════════════════════════════════════════════════════════
#
#   Gen 19808: Sharpe=1.3483, trades=58, WR=41.4%
#   Gen 20475: Sharpe=1.4877, trades=55, WR=43.6%  (+0.139) entry change
#   Gen 20492: Sharpe=1.4898, trades=52, WR=50.0%  (+0.002) entry change
#   Gen 20502: Sharpe=1.6060, trades=54, WR=44.4%  (+0.116) multi-pair + RSI
#   [Gen 22157-23010: corrupted/poison results — disregard]
#   Gen 23612: Sharpe=1.5983, trades=54, WR=46.3%  restored from base
#   Gen 23638: Sharpe=1.6069, trades=54, WR=46.3%  (+0.007) entry tweak
#   Gen 23765: Sharpe=1.6343, trades=54, WR=44.4%  (+0.027) entry tweak
#   Gen 23932: Sharpe=1.6344, trades=54, WR=44.4%  (+0.000) CURRENT CHAMPION
#
# KEY INSIGHTS:
#   • Every Sharpe gain came from entry condition changes
#   • Trade count stabilized at 54 — this is the signal count in 2yr backtest
#   • Win rate is 44.4% — strategy profits from large TP (9.5%) vs small SL (1.5%)
#   • 6.3:1 reward/risk ratio compensates for sub-50% win rate
#   • Fewer, better-filtered trades = better Sharpe
#   • Exit/risk parameters are at their optimal values — do not change them
#
# ══════════════════════════════════════════════════════════════════════
# FAILURE PATTERNS — WHAT THE LLM KEEPS DOING WRONG
# ══════════════════════════════════════════════════════════════════════
#
# 1. CLONE OUTPUT (most common): LLM outputs champion YAML unchanged.
#    Signature: trades=54, Sharpe≈1.6343-1.6344. DISCARDED.
#    Fix: Verify price_change_pct = -1.0 (not -0.5) before submitting.
#
# 2. ZERO TRADES (common): LLM adds extra conditions or tightens thresholds.
#    Signature: trades=0, Sharpe=0.00, max_trades_reject.
#    Fix: Make ONLY the ONE change in Step 2. Do NOT add conditions.
#    Do NOT change momentum, bollinger, macd, or rsi simultaneously.
#
# 3. WRONG BASE (less common): LLM uses old BTC-only strategy.
#    Signature: trades=58, Sharpe≈1.34. pairs=[BTC/USD] only.
#    Fix: pairs must list ALL THREE: BTC/USD, ETH/USD, SOL/USD.
#
# 4. EXIT PARAMETER DRIFT: LLM changes take_profit or timeout.
#    Fix: take_profit_pct=9.5 ALWAYS. timeout_hours=156 ALWAYS.
#
# ══════════════════════════════════════════════════════════════════════
# MACRO CONTEXT (TYR Risk Officer — 2026-04-18)
# ══════════════════════════════════════════════════════════════════════
#
# F&G = 26 (Fear). BTC Dominance = 57.43%. Regime: CAUTION.
# TYR Directive: Reduce live position sizes to 50% of normal.
# Fear regime is FAVORABLE for this strategy's long entry logic.
# RSI<35 + below Bollinger lower + MACD bullish = fear capitulation setup.
# Backtest Sharpe=1.6344 was earned in fear/capitulation regimes.
# Live sizing: 50% reduction per TYR directive regardless of backtest.
# NOTE: size_pct in YAML is the BACKTEST size. Live sizing is managed by TYR.
#
# ══════════════════════════════════════════════════════════════════════
# FINAL YAML CHECKLIST — VERIFY BEFORE SUBMITTING
# ══════════════════════════════════════════════════════════════════════
#
# ✓ name               = gen23933_d8a
# ✓ pairs              = BTC/USD, ETH/USD, SOL/USD  (3 pairs — NOT just BTC)
# ✓ size_pct           = 25.0  (NOT 22.67)
# ✓ max_open           = 2
# ✓ fee_rate           = 0.001
# ✓ long momentum_accelerating   period=48, eq, false
# ✓ long bollinger_position       period=48, eq, below_lower
# ✓ long macd_signal              period=48, eq, bullish
# ✓ long price_change_pct         period=24, lt, -1.0   ← THE ONE CHANGE
# ✓ long rsi                      period=14, lt, 35.0
# ✓ short momentum_accelerating  period=48, eq, false
# ✓ short bollinger_position      period=168, eq, above_upper
# ✓ short macd_signal             period=24, eq, bearish
# ✓ short price_change_pct        period=24, gt, 0.54
# ✓ take_profit_pct    = 9.5   (NOT 6.63)
# ✓ stop_loss_pct      = 1.5
# ✓ timeout_hours      = 156   (NOT 129 or 132)
# ✓ pause_if_down_pct  = 8
# ✓ stop_if_down_pct   = 18
# ✓ pause_hours        = 48
#
# DOUBLE-CHECK: Is price_change_pct = -1.0?  If it says -0.5, you have a clone.
```