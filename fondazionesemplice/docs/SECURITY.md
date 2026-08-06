# Sicurezza operativa

- Non pubblicare `.env`, file OctoBot `user/`, log o cache modelli.
- Usare credenziali Coinbase dedicate e senza prelievi, solo dopo il gate live.
- Accedere alle dashboard tramite tunnel SSH o Tailscale; non cambiare i bind `127.0.0.1` senza reverse proxy autenticato.
- Installare solo tag o commit Git revisionati.
- Trattare output LLM e dati esterni come non attendibili.
- Ruotare `DECISION_API_KEY`, password PostgreSQL e Grafana dopo qualsiasi sospetto incidente.
- Non dare a OpenClaw accesso alle chiavi exchange né al ciclo decisionale.

Per segnalazioni di sicurezza, aprire una security advisory privata nel repository GitHub invece di una issue pubblica.

