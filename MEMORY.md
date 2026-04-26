# MEMORY.md — Operational Notes

## Configuration

See config.yaml for deployment-specific settings (gitignored).
See config.example.yaml for the full schema.

## Fleet

Run `python3 scripts/generate_fleet.py --help` to create your bot fleet.
See docs/example_fleet_reference.md for an example fleet configuration.

## Executive Officers

| Officer  | Role                          | Script                            |
|----------|-------------------------------|-----------------------------------|
| ODIN     | Strategy Officer              | research/odin_researcher_v2.py    |
| MIMIR    | Analysis Officer              | research/mimir.py                 |
| LOKI     | Implementation Officer        | research/loki.py                  |
| FREYA    | Prediction Markets Officer    | research/freya_researcher.py      |
| TYR      | Risk Officer                  | research/tyr.py                   |
| HEIMDALL | Market Intelligence Officer   | research/heimdall.py              |
| VIDAR    | Strategic Arbitration Officer | research/vidar.py                 |
| SYN      | Operations Officer            | sys_heartbeat.py (composite)      |

## Repository

Repo: https://github.com/YOUR_USERNAME/YOUR_FORK
