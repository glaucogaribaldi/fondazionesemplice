# Design delle strategie

Le cinque corsie ricevono gli stessi dati e partono da `310 USDC` virtuali ciascuna. Non condividono capitale, posizioni o cooldown.

| Corsia | Profilo | Scopo |
|---|---|---|
| 1 | Kronos + Nemotron conservativa | Alta selettività |
| 2 | Kronos + Nemotron aggressiva | Maggiore frequenza controllata |
| 3 | Kronos quantitativa | Isolare il contributo del forecast |
| 4 | Baseline tecnica | Benchmark deterministico |
| 5 | Agente sperimentale | Esplorazione con limiti più stretti |

I parametri sono in `config/strategies.yml`. Nessuna corsia può modificare la propria configurazione a runtime.

## Confronto corretto

La classifica deve includere rendimento netto, max drawdown, Sortino, profit factor, fee, slippage, turnover, stabilità del modello e decisioni respinte. La semplice equity non è sufficiente per promuovere una strategia.

## Simulazione paper

Arena mantiene un ledger persistente per corsia e modella prezzo bid/ask, fee e slippage configurabili. Gestisce acquisti, vendite, costo medio, P&L realizzato, equity e drawdown. Fill parziali, latenza e liquidità di secondo livello restano fuori da questa release e devono essere aggiunti prima di valutare il live.
