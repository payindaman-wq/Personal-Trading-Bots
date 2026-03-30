# FREYA Research Program — Prediction Markets

## Objective
Find prediction market filter strategies that maximize risk-adjusted ROI by identifying market categories and keyword buckets where crowd prices are systematically miscalibrated vs. historical resolution rates.

## Simulator
- 300k+ resolved Polymarket/Kalshi/Manifold markets
- Category base rates: sports=30.6%, politics=29.1%, crypto=31.5%, economics=26.0%, world_events=12.0%
- Bet: if market_odds > base_rate + min_edge_pts -> bet NO; if market_odds < base_rate - min_edge_pts -> bet YES
- Fitness: adj_score = sharpe x log(n_bets/20 + 1)

## Key Insights (updated by Mimir)
- world_events is the largest category (290k markets) with YES rate of only 12%
  -- markets priced above ~17% represent systematic YES overpricing
- Sports/politics/crypto/economics have more symmetric pricing (base rates 26-32%)
- Keyword filters reduce noise by finding sub-buckets with stronger calibration gaps
- Higher min_liquidity_usd filters to better-quality markets
  -- explore both low-liquidity (inefficiency edge) and high-liquidity tiers

## Mutation Guidelines
1. Try specific keyword combinations within world_events -- news events, political decisions, announcements
2. Experiment with price_range to isolate over/under-confident market segments
3. Test min_edge_pts in 0.03-0.20 range -- lower catches more bets, higher filters noise
4. Compare categories: world_events volume vs sports/politics precision
5. Avoid keywords so broad they barely filter (e.g. "will" alone in world_events)

## What to Avoid
- Strategies with n_bets < 50 (insufficient statistical evidence)
- Extremely high sharpe with very few bets (overfitting)
- Exclude keywords that accidentally remove most of a category
