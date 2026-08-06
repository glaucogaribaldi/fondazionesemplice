# Fondazione Semplice 3.10

AI trading research platform designed for Coinbase Advanced paper/live execution.

Architecture:

- OpenClaw Master (U50) controls remote node
- OpenClaw Node on trading VPS
- OctoBot execution layer
- Kronos-base forecasting model
- NVIDIA Nemotron Nano 9B v2 decision engine via SGLang
- Deterministic Risk Engine
- Arena Manager with 5 independent strategies

Default mode: PAPER ONLY.

Initial capital:

5 strategies x 310 USDC virtual capital.

The repository is the single source of truth for deployment.
