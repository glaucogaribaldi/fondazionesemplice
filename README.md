# Fondazione Semplice

Appliance di trading AI **paper-first** per una VM GCP `g2-standard-8` con NVIDIA L4. Combina Kronos-base, NVIDIA Nemotron Nano 9B v2 su SGLang, un Risk Engine deterministico, cinque corsie paper isolate e OctoBot.

> **Stato: alpha di ricerca.** Non è consulenza finanziaria e non promette rendimenti. L’integrazione di esecuzione con OctoBot resta disabilitata finché il ciclo paper/shadow non è stato validato.

## Principi di sicurezza

- default obbligatorio `TRADING_MODE=paper` e `LIVE_ENABLED=false`;
- Nemotron propone, il Risk Engine autorizza o trasforma in `HOLD`;
- ogni errore, timeout o risposta invalida produce `HOLD`;
- nessuna chiave Coinbase nel repository o nell’installer;
- dashboard esposte solo su `127.0.0.1`;
- passaggio live manuale e a doppia conferma.

## Architettura

```text
OctoBot / market snapshot
           │
           ▼
      Arena Manager ───── cinque portafogli paper
           │
           ▼
    Decision Service
      │           │
      ▼           ▼
 Kronos-base   Nemotron 9B v2 / SGLang
      └──────┬────┘
             ▼
     Risk Engine deterministico
             │
             ▼
       BUY / SELL / HOLD
```

Dettagli: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Avvio locale senza GPU

```bash
cp .env.example .env
# sostituire tutti i valori change-me
make validate
make test
docker compose --profile mock --profile observability up -d --build
./scripts/smoke_test.sh
```

Interfacce locali:

- OctoBot: `http://127.0.0.1:5001`
- Grafana: `http://127.0.0.1:3000`
- Decision API: `http://127.0.0.1:8080/docs`
- Arena API: `http://127.0.0.1:8082/docs`

## Avvio sulla L4

Impostare in `.env`:

```dotenv
AI_BACKEND=sglang
KRONOS_BACKEND=real
TRADING_MODE=paper
LIVE_ENABLED=false
```

Poi:

```bash
./scripts/preflight.sh --gpu
docker compose --profile gpu --profile observability up -d --build
./scripts/smoke_test.sh --wait 600
```

Il primo avvio scarica circa 18 GB di pesi Nemotron oltre a Kronos. La cache è conservata nel volume `model-cache`.

## Installazione OpenClaw

La procedura è in [`docs/INSTALL_OPENCLAW.md`](docs/INSTALL_OPENCLAW.md). Lo skill installabile si trova in [`openclaw/skills/install-fondazionesemplice`](openclaw/skills/install-fondazionesemplice).

## Percorso di rilascio

1. mock locale;
2. arena paper sulla L4;
3. backtest con fee, spread e slippage;
4. shadow live senza invio ordini;
5. revisione manuale;
6. capitale reale limitato, solo dopo la checklist in [`docs/PAPER_TO_LIVE.md`](docs/PAPER_TO_LIVE.md).

## Riferimenti upstream

- [Kronos](https://github.com/shiyu-coder/Kronos)
- [NVIDIA Nemotron Nano 9B v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2)
- [SGLang](https://github.com/sgl-project/sglang)
- [OctoBot](https://github.com/Drakkar-Software/OctoBot)
- [OpenClaw](https://github.com/openclaw/openclaw)

Il build Kronos è bloccato al commit `67b630e67f6a18c9e9be918d9b4337c960db1e9a`; SGLang e OctoBot sono bloccati rispettivamente a `v0.5.15.post1` e `2.1.1`.

## Licenza

Codice del repository: MIT. Modelli, immagini container e dipendenze mantengono le rispettive licenze upstream.