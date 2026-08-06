# Architettura

## Confini di fiducia

| Componente | Può proporre trade | Può approvare trade | Possiede chiavi exchange |
|---|---:|---:|---:|
| Kronos | No | No | No |
| Nemotron | Sì | No | No |
| Risk Engine | No | Sì | No |
| Market Feed | No | No | No |
| Arena | No | Simula fill paper | No |
| OctoBot | No | No | No in questa release |

Nemotron non chiama strumenti, non legge segreti e non comunica direttamente con Coinbase. Il Decision Service accetta solo richieste autenticate sulla rete Docker privata.

## Flusso

1. Market Feed acquisisce candele e ticker dagli endpoint pubblici Coinbase.
2. Arena replica lo stesso snapshot per le cinque corsie.
3. Kronos genera direzione, rendimento atteso, volatilità e confidenza.
4. Le corsie AI richiedono una proposta JSON a Nemotron; le baseline usano regole quantitative.
5. Il Risk Engine controlla simbolo, freschezza, spread, confidenza, allocazione, perdita giornaliera, posizioni, cooldown, stop loss e blocco live.
6. Una violazione o un errore produce `HOLD`.
7. Arena registra una sola simulazione per coppia `request_id`/corsia, applicando spread, fee e slippage.

Il feed preserva sempre la valuta quotata del prodotto (`BTC-USDT` → `BTC/USDT`). Non converte né rinomina USDT in USDC.

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

Il volume `arena-data` contiene il ledger SQLite paper: contanti, posizioni, fill, commissioni, P&L e drawdown delle cinque corsie. La chiave univoca per richiesta rende l’elaborazione idempotente. PostgreSQL resta disponibile per l’audit applicativo futuro.

## GPU

Nemotron usa la L4 tramite SGLang. Kronos-base resta su CPU per lasciare VRAM al modello 9B; il servizio può essere spostato su GPU in seguito dopo misure reali di latenza e memoria.

## Ruolo di OctoBot

Questa release avvia OctoBot per dashboard e backtest, ma lo tiene fuori dal percorso di esecuzione. Collegare una chiave Coinbase a OctoBot non è necessario e non abilita Fondazione. Un adapter reale verrà considerato solo dopo la validazione paper e shadow.
