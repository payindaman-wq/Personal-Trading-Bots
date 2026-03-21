```yaml
name: autobotday
style: trend-confirmed RSI pullback with VWAP filter
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
      - indicator: rsi
        period_minutes: 15
        operator: lt
        value: 45
      - indicator: price_vs_vwap
        period_minutes: 15
        operator: eq
        value: below
  short:
    conditions:
      - indicator: trend
        period_minutes: 240
        operator: eq
        value: down
      - indicator: rsi
        period_minutes: 15
        operator: gt
        value: 55
      - indicator: price_vs_vwap
        period_minutes: 15
        operator: eq
        value: above
exit:
  take_profit_pct: 1.3
  stop_loss_pct: 1.0
  timeout_minutes: 120
risk:
  pause_if_down_pct: 4
  pause_minutes: 60
  stop_if_down_pct: 10
guidance:
  # ===========================================================
  # YOUR JOB: Change EXACTLY ONE number or value below.
  # Output the COMPLETE strategy YAML. Change nothing else.
  # ===========================================================
  #
  # STEP 1: Pick ONE thing to change from this list:
  #
  #   a) RSI long threshold  (currently 45) -> try 35, 40, or 50
  #   b) RSI short threshold (currently 55) -> try 50, 60, or 65
  #   c) take_profit_pct     (currently 1.3) -> try 1.0, 1.1, 1.2, 1.5, 1.7, 2.0
  #   d) stop_loss_pct       (currently 1.0) -> try 0.5, 0.7, 0.8, 1.2, 1.5
  #   e) timeout_minutes     (currently 120) -> try 60, 240, or 360
  #   f) RSI period_minutes  (currently 15) -> try 5, 30, or 60
  #   g) VWAP period_minutes (currently 15) -> try 5, 30, or 60
  #   h) Add ONE new condition (max 4 per side). Pick from:
  #        macd / bb_position / stoch / volume_spike
  #   i) Remove one non-trend condition (min 2 per side)
  #   j) pause_if_down_pct   (currently 4) -> try 3, 5, or 6
  #
  # STEP 2: Make the change symmetrically for long AND short
  #         (e.g. if you change RSI long to 40, change RSI short to 60)
  #
  # STEP 3: Output the full YAML. Do NOT add commentary.
  #
  # ===========================================================
  # RULES - VIOLATIONS CAUSE ERRORS
  # ===========================================================
  #
  # Valid indicators ONLY:
  #   trend         (eq: up/down)
  #   price_vs_vwap (eq: above/below)
  #   rsi           (lt/gt: 10-90)
  #   macd          (eq: bullish/bearish)
  #   bb_position   (eq: above_upper/below_lower/inside)
  #   stoch         (lt/gt: 10-90)
  #   volume_spike  (eq: true/false)
  #
  # Valid period_minutes: 5, 15, 30, 60, 120, 240, 480
  # take_profit_pct: 0.5 to 5.0
  # stop_loss_pct: 0.3 to 3.0
  # timeout_minutes: 60, 120, 240,