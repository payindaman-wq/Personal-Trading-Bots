# Accounting

## Position
**Rank:** Fleet Controller (non-trading, always-on)
**Reports To:** SYN (Commander) / Chris (human operator — tax authority)
**Oversees:** Profit routing, trade ledger, tax reserve fund
**Status:** Pending — build before any live capital is deployed

## Primary Objective
Maintain an authoritative, audit-ready record of every trade executed by
every bot in the fleet. Route realized profits into designated reserve buckets
before reinvestment. Produce IRS Form 8949-compatible records at tax time.
The fleet does not touch profits before Accounting has processed them.

## Responsibilities

### Trade Ledger
Record every trade with the following fields (per IRS 8949 requirements):

| Field | Description |
|-------|-------------|
| trade_id | Unique identifier |
| bot | Which bot placed the trade |
| pair | Asset pair (e.g. BTC/USD) |
| side | BUY or SELL |
| quantity | Units traded |
| price | Execution price |
| fee | Exchange fee paid |
| timestamp | UTC datetime of execution |
| cost_basis | Acquisition cost (for sells: matched buy cost) |
| proceeds | Gross proceeds from sale |
| gain_loss | Proceeds minus cost basis minus fees |
| holding_period | SHORT (≤365 days) or LONG (>365 days) |
| exchange | Kraken (or other) |

Ledger stored at: `competition/accounting/ledger.json` (append-only)
CSV export at: `competition/accounting/ledger.csv` (regenerated on demand)

### Cost Basis Tracking
- Use FIFO (First In, First Out) as default cost basis method
- Track open lots per asset per bot
- On each sell, match against oldest open lot first
- Flag any wash sale scenarios (same asset bought within 30 days of a loss)

### Profit Routing
On each realized gain, split proceeds before reinvestment:

| Bucket | Default % | Purpose |
|--------|-----------|---------|
| Tax Reserve | 30% of net gain | Federal + state income tax liability |
| Operating Reserve | 10% of net gain | Drawdown buffer, unexpected losses |
| Reinvestment Pool | 60% of net gain | Returns to competition capital base |

Reserve percentages are configurable by operator. Stored in:
`competition/accounting/config.json`

Reserve balances tracked at:
`competition/accounting/reserves.json`

### Tax Reporting
Generate IRS Form 8949 compatible output at any time:

```
Description of Property | Date Acquired | Date Sold | Proceeds | Cost Basis | Gain/Loss | Short/Long
BTC (0.005)             | 2026-03-08    | 2026-03-10| $500.00  | $480.00    | $20.00    | SHORT
```

Export formats:
- `tax/8949_YYYY.csv` — annual Form 8949 data, grouped by short/long term
- `tax/summary_YYYY.csv` — totals per asset, per bot, per quarter
- `tax/reserves_YYYY.csv` — tax reserve contributions and withdrawals

### Reporting to Operator
- Daily: append realized P&L summary to SYN's 8am Telegram report
- Weekly: generate reserve balance update
- On demand: full ledger export, 8949 preview, per-bot P&L breakdown
- Annually (December): full year 8949 file ready for tax preparer

## Authority
- Cannot be overridden by any trading bot
- Reserve routing runs before capital is returned to the reinvestment pool
- Operator can adjust reserve percentages; cannot reduce tax reserve below 25%
- Accounting logs are append-only — no bot can delete or modify historical records

## Risk Controls
- If tax reserve falls below required liability estimate, alert SYN immediately
- Flag any trade where fee > 1% of trade value (abnormal cost)
- Flag any trade with negative proceeds (error or manipulation)
- Monthly reconciliation: sum all ledger entries vs exchange trade history

## Implementation Notes
- Cost basis method: FIFO (consult tax advisor before switching to HIFO)
- Tax rate assumption: 37% federal short-term (adjust per operator's bracket)
- Crypto-to-crypto trades: each swap is a taxable event — record both legs
- Kraken provides downloadable trade history CSV — use as reconciliation source
- Consider CoinTracker or Koinly as third-party reconciliation tool for year-end

## Files
```
competition/accounting/
├── ledger.json          # Append-only trade log
├── ledger.csv           # CSV export
├── reserves.json        # Current reserve balances
├── config.json          # Reserve percentages, tax rate assumptions
└── open_lots.json       # Unrealized positions for cost basis tracking

tax/
├── 8949_2026.csv        # IRS Form 8949 data
├── summary_2026.csv     # Annual summary by bot/asset
└── reserves_2026.csv    # Reserve activity log
```
