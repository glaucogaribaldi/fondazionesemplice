# Installazione con OpenClaw

## Importante

Lo script distrugge tutti i workload e volumi Docker presenti sulla VM e cancella `/opt/fondazionesemplice` **senza backup**. Non ripartiziona il disco di avvio: un vero formato completo si esegue eliminando la VM GCP e creandone una nuova da immagine Ubuntu.

La soluzione raccomandata è quindi:

1. pubblicare e taggare il repository GitHub;
2. eliminare la vecchia VM dal pannello GCP;
3. creare una `g2-standard-8` Ubuntu nuova con lo stesso disco dati solo se intenzionale;
4. eseguire OpenClaw sulla nuova VM;
5. installare da tag o commit immutabile.

## Preparare OpenClaw

Copiare la cartella:

```text
openclaw/skills/install-fondazionesemplice
```

nella directory skills del workspace OpenClaw, quindi usare il testo in `openclaw/INSTALL_PROMPT.md`.

## Comando deterministico

OpenClaw deve prima clonare e ispezionare il repository, poi eseguire:

```bash
sudo ./scripts/install_vm.sh \
  --repo https://github.com/glaucogaribaldi/fondazionesemplice.git \
  --ref v0.1.0 \
  --confirm ERASE_FOUNDATION_VM_WITHOUT_BACKUP
```

Usare un tag o commit, non `main`, per il deploy effettivo.

## Cosa fa

- elimina container, immagini, cache e volumi Docker;
- cancella la directory applicativa precedente;
- installa Docker e NVIDIA Container Toolkit;
- clona il riferimento Git richiesto;
- genera segreti locali con permessi `0600`;
- forza paper mode;
- avvia Kronos, SGLang/Nemotron, Decision Service, Arena, OctoBot, PostgreSQL, Prometheus e Grafana;
- verifica GPU e health check.

## Cosa non fa

- nessun backup;
- nessuna cancellazione del boot disk attivo;
- nessuna chiave Coinbase;
- nessuna apertura pubblica delle dashboard;
- nessun passaggio automatico al live.

## Report richiesto a OpenClaw

- URL e commit installato;
- modello GPU e VRAM rilevata;
- stato e health di ogni container;
- conferma di `TRADING_MODE=paper` e `LIVE_ENABLED=false`;
- indirizzi locali OctoBot e Grafana;
- errori senza tentativi di aggirare i controlli.
