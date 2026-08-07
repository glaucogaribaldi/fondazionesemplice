# Bootstrap paper

Il bootstrap è la prima raccolta controllata di dati, non un passaggio al live.

## Obiettivo

Eseguire per almeno 72 ore le cinque corsie su BTC/USDT ed ETH/USDT, verificando che Kronos, Nemotron e Risk Engine producano decisioni valide senza errori `FAIL_CLOSED`.

## Condizioni iniziali

- release `bootstrap-paper-v1.2`;
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
