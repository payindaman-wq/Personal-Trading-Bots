# Fleet Roles & Chain of Command

## Organizational Chart

```
SYN — Commander / Manager
├── Macro Governor          (always-on advisory — risk signals to all)
├── Accounting              (always-on operational — books, taxes, reserves)
├── Spot Day League         (4h competition sprints — Kraken spot)
├── Spot Swing League       (7-day competition sprints — Kraken spot)
├── Futures Day League      (4h sprints — pending, after spot proven)
├── Futures Swing League    (7-day sprints — pending, after spot proven)
├── Statistical Arb         (swing league — pending)
├── Cross-Pair Spread       (swing league — pending)
└── Polymarket Division     (separate — pending)
```

## Roles Index

| File | Role | Status |
|------|------|--------|
| [commander.md](commander.md) | Commander / Manager (SYN) | Live |
| [macro-governor.md](macro-governor.md) | Macro Governor | Pending |
| [accounting.md](accounting.md) | Accounting | Pending |
| [spot-day.md](spot-day.md) | Spot Day Trader | Live |
| [spot-swing.md](spot-swing.md) | Spot Swing Trader | Live |
| [futures-day.md](futures-day.md) | Futures Day Trader | Pending |
| [futures-swing.md](futures-swing.md) | Futures Swing Trader | Pending |
| [statistical-arb.md](statistical-arb.md) | Statistical Arbitrage Trader | Pending |
| [cross-pair-spread.md](cross-pair-spread.md) | Cross-Pair Spread Trader | Pending |
| [polymarket.md](polymarket.md) | Polymarket Trader | Pending |

## Funding Flow

Competition sprints determine which bots earn live capital. Only the
competition winner gets funded. Accounting intercepts all realized profits
before reinvestment and routes a reserve percentage to the tax fund.

```
Trade Realized P&L
    └── Accounting Bot
            ├── Tax Reserve (set-aside %)
            ├── Operating Reserve (drawdown buffer %)
            └── Reinvestment Pool → Competition Winner
```
