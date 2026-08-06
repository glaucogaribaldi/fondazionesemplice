# Aggiornamento sicuro della VPS

Questa procedura aggiorna l’installazione esistente senza formattare il disco e senza cancellare volumi, modelli o segreti locali. Non usare nuovamente `install_vm.sh`.

## Prompt per OpenClaw

```text
Aggiorna Fondazione Semplice sulla VPS fondazione 35.239.91.187, utente tre con sudo.

Regole inderogabili:
- non chiedere né utilizzare chiavi Coinbase: la release è esclusivamente paper;
- non cancellare dischi, volumi Docker, /mnt/data o /opt/fondazionesemplice/.env;
- non modificare TRADING_MODE=paper, LIVE_ENABLED=false, LIVE_CONFIRMATION vuoto;
- non esporre porte su 0.0.0.0;
- interrompi e segnala qualsiasi divergenza invece di forzare.

Procedura:
1. Verifica hostname, IP, GPU e almeno 50 GB liberi.
2. Salva fuori dalla working tree una copia protetta del solo file /opt/fondazionesemplice/.env.
3. In /opt/fondazionesemplice acquisisci dal repository ufficiale il commit immutabile indicato dall’utente e verifica l’hash.
4. Ripristina il file .env locale e aggiungi, se assenti:
   PAPER_FEE_BPS=60
   PAPER_SLIPPAGE_BPS=5
   COINBASE_PRODUCTS=BTC-USDC,ETH-USDC
   MARKET_TIMEFRAME_SECONDS=300
   MARKET_POLL_SECONDS=30
   MARKET_CANDLE_LIMIT=96
5. Valida configurazione e test unitari.
6. Esegui docker compose --profile gpu --profile observability up -d --build.
7. Attendi health di tutti i container, compreso market-feed.
8. Esegui ./scripts/smoke_test.sh --wait 900; deve superare anche il test end-to-end delle cinque corsie e l’idempotenza.
9. Conferma che arena-data esiste, che /v1/ranking contiene cinque corsie e che un riavvio di Arena conserva gli eventi.
10. Fornisci commit installato, stato container, risultato test, stato paper/live e gli eventuali errori. Non dichiarare successo se manca una verifica.
```

Sostituire nel prompt “commit immutabile indicato dall’utente” con l’hash pubblicato per il rilascio.
