# Architettura

## Confini di fiducia

| Componente | Può proporre trade | Può approvare trade | Possiede chiavi exchange |
|---|---:|---:|---:|
| Kronos | No | No | No |
| Nemotron | Sì | No | No |
| Risk Engine | No | Sì | No |
| Arena | No | No | No |
| OctoBot | No | No | Solo dopo attivazione live manuale |

Nemotron non chiama strumenti, non legge segreti e non comunica direttamente con Coinbase. Il Decision Service accetta solo richieste autenticate sulla rete Docker privata.

## Flusso

1. OctoBot o un adapter invia uno snapshot con almeno 32 candele OHLCV.
2. Arena replica lo stesso snapshot per le cinque corsie.
3. Kronos genera direzione, rendimento atteso, volatilità e confidenza.
4. Le corsie AI richiedono una proposta JSON a Nemotron; le baseline usano regole quantitative.
5. Il Risk Engine controlla simbolo, freschezza, spread, confidenza, allocazione, perdita giornaliera, posizioni, cooldown, stop loss e blocco live.
6. Una violazione o un errore produce `HOLD`.

## Contratto API

Endpoint: `POST /v1/decision`, header `X-API-Key`.

Campi principali in ingresso:

- `request_id`, `mode`, `lane_id`, `symbol`, `timeframe`;
- `market.timestamp`, `bid`, `ask`, `candles`;
- `portfolio.equity`, `cash`, `daily_pnl_pct`, `open_positions`.

Campi principali in uscita:

- `decision`: `BUY`, `SELL` o `HOLD`;
- `approved_by_risk_engine`;
- `allocation_pct`, stop loss, take profit e scadenza;
- `reason_codes` e versioni modello.

## Persistenza

PostgreSQL conserva audit delle decisioni e snapshot dell’arena. Non è un secondo ledger finanziario: ordini e portafoglio reale restano responsabilità di OctoBot/Coinbase.

## GPU

Nemotron usa la L4 tramite SGLang. Kronos-base resta su CPU per lasciare VRAM al modello 9B; il servizio può essere spostato su GPU in seguito dopo misure reali di latenza e memoria.

## Limitazione OctoBot

Questa release avvia OctoBot ma non installa automaticamente un Tentacle di esecuzione. Prima di scriverlo si deve bloccare una versione OctoBot, validarne l’API e superare la fase paper. Il contratto Decision API è intenzionalmente stabile per quel passaggio.

