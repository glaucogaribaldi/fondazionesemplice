# Flusso di controllo

```text
Operatore + ChatGPT/Codex
        │ modifica strategie e documentazione
        ▼
GitHub, commit immutabile
        │
        ▼ solo su richiesta dell’operatore
OpenClaw su U50
        │ valida e applica il commit
        ▼
VPS Fondazione
  ├─ Market Feed Coinbase pubblico
  ├─ Arena Manager e cinque ledger paper
  ├─ Kronos-base
  ├─ Nemotron Nano 9B v2 via SGLang
  ├─ Risk Engine deterministico
  ├─ PostgreSQL
  ├─ Grafana
  └─ OctoBot isolato per dashboard/backtest
```

ChatGPT/Codex non comunica direttamente con la VPS. Le modifiche diventano operative solo dopo pubblicazione su GitHub e invocazione esplicita dello skill OpenClaw `update-fondazionesemplice` con un commit immutabile.

La sostituzione di Qwen/Ollama con Nemotron/SGLang è la scelta hardware corrente. Non cambia il confine di controllo: il modello propone, il Risk Engine decide e Arena simula.

## Modificare una strategia

1. modificare `config/strategies.yml`;
2. assegnare un nuovo `release_id` in `config/release.yml`;
3. non aumentare i limiti globali in `config/risk.yml` senza revisione separata;
4. eseguire `make validate` e `make test`;
5. pubblicare un commit immutabile;
6. interpellare OpenClaw per applicarlo;
7. verificare release, cinque corsie e dashboard.
