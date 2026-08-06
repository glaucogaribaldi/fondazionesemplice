---
name: update-fondazionesemplice
description: Apply an operator-requested immutable Fondazione Semplice release to the dedicated VPS without erasing data, while enforcing paper mode and validating the strategy release.
---

# Update Fondazione Semplice

Use this skill only when the operator explicitly asks OpenClaw to deploy a repository commit.

1. Ask for the immutable 40-character commit SHA. Never deploy `main` directly.
2. Connect to the dedicated VPS and verify hostname, GPU and `/opt/fondazionesemplice`.
3. Preserve `.env`, Docker volumes, model cache, databases and `/mnt/data`.
4. Fetch the official repository and inspect the requested commit before checkout.
5. Refuse a dirty working tree unless every local code change is reviewed and already represented by the requested commit.
6. Check out the exact commit and verify `git rev-parse HEAD`.
7. Run `python3 scripts/validate_config.py` and `python3 scripts/validate_strategy_release.py`.
8. Verify `.env` still contains `TRADING_MODE=paper`, `LIVE_ENABLED=false` and an empty `LIVE_CONFIRMATION`.
9. Run `docker compose --profile gpu --profile observability up -d --build`.
10. Run the unit tests and `./scripts/smoke_test.sh --wait 900`.
11. Report commit, `release_id`, container health, test results and dashboard URL.

Never request Coinbase credentials, weaken risk limits, enable live mode, erase volumes or silently modify a strategy.
