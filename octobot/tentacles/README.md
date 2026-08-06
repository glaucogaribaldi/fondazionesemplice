# Adapter OctoBot

Questa directory è riservata al Tentacle che invierà snapshot a `POST http://decision-service:8080/v1/decision` o `POST http://arena:8082/v1/evaluate`.

La release alpha non include esecuzione automatica. Il Tentacle va implementato soltanto dopo aver bloccato una versione OctoBot e validato il contratto contro la relativa API. Fino ad allora usare OctoBot per dashboard, market data, paper trading e backtest senza credenziali live.
