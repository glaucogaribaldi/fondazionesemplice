# Da paper a live

Il live non è supportato nella release alpha. Questa checklist definisce il gate futuro e non costituisce un’autorizzazione a operare.

## Requisiti minimi

- almeno 30 giorni di paper trading continuo;
- backtest walk-forward separato dai dati usati per calibrare le strategie;
- fee Coinbase, spread, slippage, partial fill e timeout modellati;
- nessun incidente `FAIL_CLOSED` non spiegato negli ultimi 7 giorni;
- drawdown massimo e perdita giornaliera entro limiti prestabiliti;
- shadow live confrontato con prezzi realmente ottenibili;
- revisione manuale di log, segreti, firewall e permessi Coinbase;
- chiave Coinbase senza privilegi di prelievo;
- kill switch operativo e testato.

## Doppia conferma tecnica

Il Decision Service accetta richieste live soltanto con tutti i valori seguenti:

```dotenv
TRADING_MODE=live
LIVE_ENABLED=true
LIVE_CONFIRMATION=I_UNDERSTAND_LIVE_TRADING_CAN_LOSE_MONEY
```

Il preflight standard rifiuta deliberatamente questa configurazione. L’attivazione deve essere una modifica separata, revisionata e documentata.

## Rollback

1. impostare immediatamente `LIVE_ENABLED=false`;
2. riavviare Decision Service;
3. annullare manualmente gli ordini aperti in OctoBot/Coinbase;
4. verificare posizioni e saldi direttamente su Coinbase;
5. preservare audit e log per l’analisi.
