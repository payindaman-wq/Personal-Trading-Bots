```yaml
name: autobotday
style: trend-confirmed RSI pullback with VWAP filter and exploration of new indicators
pairs:
  - BTC/USD
  - ETH/USD
  - SOL/USD
position:
  size_pct: 20
  max_open: 1
  fee_rate: 0.001
entry:
  long:
    conditions:
      - indicator: trend
        period_minutes: 240
        operator: eq
        value: up
      - indicator: price_vs_vwap
        period_minutes: 15
        operator: eq
        value: below
      - indicator: rsi
        period_minutes: 30
        operator: lt
        value: 40
      - indicator: rsi
        period_minutes: 15
        operator: lt
        value: 30
  short:
    conditions:
      - indicator: trend
        period_minutes: 240
        operator: eq
        value: down
      - indicator: price_vs_vwap
        period_minutes: 15
        operator: eq
        value: above
      - indicator: rsi
        period_minutes: 30
        operator: gt
        value: 60
      - indicator: rsi
        period_minutes: 15
        operator: gt
        value: 70
exit:
  take_profit_pct: 1.7
  stop_loss_pct: 0.7
  timeout_minutes: 120
risk:
  pause_if_down_pct: 4
  pause_minutes: 60
  stop_if_down_pct: 10
guidance:
  # ---------------------------------------------------------------
  # CRITICAL: READ ALL RULES BEFORE PROPOSING ANY CHANGE
  # ---------------------------------------------------------------

  # === RULE 1: VALID INDICATORS ONLY ===
  # You MUST only use indicators from this exact list.
  # Any other name will cause a fatal error and waste a generation.
  # Valid indicators:
  #   - trend          (operators: eq, values: up / down)
  #   - price_vs_vwap  (operators: eq, values: above / below)
  #   - rsi            (operators: lt / gt, values: integer 10-90)
  #   - macd           (operators: eq, values: bullish / bearish)
  #   - bb_position    (operators: eq, values: above_upper / below_lower / inside)
  #   - stoch          (operators: lt / gt, values: integer 10-90)
  #   - volume_spike   (operators: eq, values: true / false)

  # === RULE 2: VALID PERIODS ===
  # period_minutes must be one of: 5, 15, 30, 60, 120, 240, 480
  # No other values are allowed.

  # === RULE 3: VALID EXIT PARAMETERS ===
  # take_profit_pct: float between 0.5 and 5.0
  # stop_loss_pct:   float between 0.3 and 3.0
  # timeout_minutes: integer, one of: 60, 120, 240, 360, 480

  # === RULE 4: VALID RISK PARAMETERS ===
  # pause_if_down_pct:  float between 2.0 and 8.0
  # pause_minutes:      integer between 30 and 240
  # stop_if_down_pct:   float between 5.0 and 20.0

  # === RULE 5: VALID POSITION PARAMETERS ===
  # size_pct:  integer between 5 and 40
  # max_open:  integer 1 or 2

  # === RULE 6: CONDITION COUNT ===
  # Each of entry.long and entry.short must have between 2 and 5 conditions.
  # Do not remove the trend condition — it is the most important filter.

  # ---------------------------------------------------------------
  # WHAT TO CHANGE (pick exactly ONE of these per generation)
  # ---------------------------------------------------------------
  # A) Adjust a single numeric threshold (e.g. rsi lt 30 -> rsi lt 35)
  #    Good candidates: rsi values, take_profit_pct, stop_loss_pct,
  #    timeout_minutes, pause_if_down_pct
  #