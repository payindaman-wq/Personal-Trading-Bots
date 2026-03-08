# accounting

Maintains the fleet's trade ledger, computes realized gains/losses (FIFO
cost basis), routes profits to tax/operating/reinvestment reserves, and
generates IRS Form 8949-compatible reports.

**Call after every SELL trade executes on Kraken.**
**Call daily to generate P&L summary for the 8am SYN report.**
**Call before any live capital is moved to the reinvestment pool.**

## Chain of Command

Accounting reports to SYN (Commander) and the human operator (Chris).
No trading bot can modify the ledger. Accounting intercepts all realized P&L
before reinvestment.

## Profit Routing (defaults)

| Bucket | % of Net Gain | Purpose |
|--------|--------------|---------|
| Tax Reserve | 30% | Federal + state income tax liability |
| Operating Reserve | 10% | Drawdown buffer |
| Reinvestment Pool | 60% | Returns to competition capital base |

Losses reduce the reinvestment pool only (no reserve impact).

## Usage

### First-time setup (run once on VPS)
```
python3 /root/.openclaw/skills/accounting/scripts/accounting.py init
```

### Record a BUY trade
```
python3 /root/.openclaw/skills/accounting/scripts/accounting.py record \
  --bot floki --pair BTC/USD --side BUY --qty 0.005 --price 95000 --fee 2.50
```

### Record a SELL trade (triggers gain/loss calc + profit routing)
```
python3 /root/.openclaw/skills/accounting/scripts/accounting.py record \
  --bot floki --pair BTC/USD --side SELL --qty 0.005 --price 97000 --fee 2.50
```

Output includes: proceeds, cost basis, gain/loss, holding period, profit routing breakdown.
Watch for `wash_sale_warning` in output — flag immediately to operator.

### Show reserve balances
```
python3 /root/.openclaw/skills/accounting/scripts/accounting.py reserves
```

### Daily P&L summary (include in 8am SYN report)
```
python3 /root/.openclaw/skills/accounting/scripts/accounting.py daily
python3 /root/.openclaw/skills/accounting/scripts/accounting.py daily --date 2026-03-08
```

### Export IRS Form 8949 (annual, tax time)
```
python3 /root/.openclaw/skills/accounting/scripts/accounting.py export 8949 --year 2026
```
Output: `/root/.openclaw/workspace/tax/8949_2026.csv`

### Export annual summary by bot + asset
```
python3 /root/.openclaw/skills/accounting/scripts/accounting.py export summary --year 2026
```
Output: `/root/.openclaw/workspace/tax/summary_2026.csv`

### Export full ledger as CSV
```
python3 /root/.openclaw/skills/accounting/scripts/accounting.py export ledger
```
Output: `/root/.openclaw/workspace/competition/accounting/ledger.csv`

### Scan for wash sale violations
```
python3 /root/.openclaw/skills/accounting/scripts/accounting.py wash-sales --year 2026
```
A wash sale occurs when an asset sold at a loss is repurchased within 30 days.
The disallowed loss must be added to the cost basis of the new position.

### View or update config
```
python3 /root/.openclaw/skills/accounting/scripts/accounting.py config
python3 /root/.openclaw/skills/accounting/scripts/accounting.py config --set tax_reserve_pct=0.35
```

## Files (on VPS)

```
/root/.openclaw/workspace/
├── competition/accounting/
│   ├── ledger.json        # Append-only trade log (source of truth)
│   ├── ledger.csv         # CSV export (regenerated on demand)
│   ├── open_lots.json     # Unrealized positions for FIFO cost basis
│   ├── reserves.json      # Current reserve balances
│   └── config.json        # Reserve percentages, tax settings
└── tax/
    ├── 8949_YYYY.csv      # IRS Form 8949 data
    ├── summary_YYYY.csv   # Annual summary by bot/asset/term
    └── reserves_YYYY.csv  # Reserve activity (future)
```

## Important Tax Notes

- **Cost basis method:** FIFO (first purchased = first sold)
- **Crypto-to-crypto swaps** are taxable events — both legs must be recorded
- **Wash sales:** same asset sold at a loss + repurchased within 30 days = loss disallowed
- **Futures bots (when live):** may qualify for Section 1256 (60/40 rule) — flag separately
- **Polymarket settlements:** taxable events, tracked in a separate ledger (future)
- **Tax reserve assumption:** 37% federal short-term bracket — adjust via config for actual bracket
- Always reconcile ledger.json against Kraken's trade history CSV at year-end
