# Bootstrap paper

La release `bootstrap-paper-v1.5` esegue una sonda operativa iniziale per rendere verificabile l'intera catena di paper trading.

- una sola operazione `BUY` per ciascuna corsia;
- simbolo fisso `BTC/USDT`;
- attivazione esclusiva su una candela reale identificata dal Market Feed Coinbase;
- allocazione pari all'1% dell'equity;
- reason code esplicito `BOOTSTRAP_PROBE`;
- esecuzione solo in modalita `paper`, mai in `shadow` o `live`;
- approvazione obbligatoria del Risk Engine;
- nessuna ripetizione dopo il primo trade della corsia.

La sonda non rappresenta una previsione di Kronos o Nemotron. Dopo il fill, le cinque corsie riprendono le rispettive strategie senza ulteriori acquisti forzati.

Il bootstrap è la prima raccolta controllata di dati, non un passaggio al live.

## Obiettivo

Eseguire per almeno 72 ore le cinque corsie su BTC/USDT ed ETH/USDT, verificando che Kronos, Nemotron e Risk Engine producano decisioni valide senza errori `FAIL_CLOSED`.

## Condizioni iniziali

- release `bootstrap-paper-v1.5`;
- timeframe `5m` compatibile con Kronos;
- capitale virtuale invariato;
- fee e slippage attivi;
- nessuna chiave Coinbase;
- nessuna modifica ai limiti per forzare operazioni.

## Criteri di riuscita

- Market Feed sano per entrambi i prodotti;
- nessun `FAIL_CLOSED` persistente;
- motivi `HOLD` visibili in Grafana;
- almeno una decisione per prodotto ogni candela chiusa;
- ledger e ranking persistenti ai riavvii;
- release e strategie attive visibili in dashboard.

Se tutte le corsie rimangono `HOLD`, si analizzano forecast, confidenza e reason code prima di cambiare una soglia. Non si abbassano i controlli alla cieca.

Le release dalla `v1.1` usano una cache Kronos separata da SGLang e possono riscaricare i pesi al primo avvio. Il servizio diventa sano solo dopo caricamento e warm-up completi.

Dalla `v1.4`, lo smoke test usa un ledger effimero separato. Prezzi e operazioni sintetiche non possono modificare equity, posizioni o metriche delle cinque corsie reali paper.

La `v1.5` include `scripts/repair_v13_smoke_drawdown.py`, una riparazione una tantum che accetta soltanto la firma esatta lasciata dal prezzo sintetico `51595` della v1.3. Il comando parte sempre in dry-run e modifica esclusivamente `max_drawdown_pct` quando viene aggiunto `--apply`.
