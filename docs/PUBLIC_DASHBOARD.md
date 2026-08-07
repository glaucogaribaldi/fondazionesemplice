# Dashboard pubblica protetta

La dashboard puo essere esposta su `https://fondazione.pianodivino.com` tramite Caddy, TLS automatico e il login nativo di Grafana.

## DNS

Prima del deploy, verificare che l'IP esterno della VPS sia statico. Creare quindi un record:

```text
Tipo: A
Nome: fondazione
Valore: IP pubblico statico della VPS
TTL: 300 durante l'attivazione
```

Non creare il record usando un IP effimero. L'indirizzo osservato durante l'installazione era `35.239.91.187`, ma OpenClaw deve confermare che sia ancora assegnato e riservato come statico.

## Attivazione

Impostare in `.env`:

```dotenv
FOUNDATION_DOMAIN=fondazione.pianodivino.com
GRAFANA_ROOT_URL=https://fondazione.pianodivino.com
GRAFANA_COOKIE_SECURE=true
```

Aprire nel firewall GCP esclusivamente TCP `80`, TCP `443` e, facoltativamente, UDP `443` per HTTP/3. Non esporre direttamente le porte `3000`, `5001`, `8080`, `8082`, `8083` o `30000`.

Avviare:

```bash
docker compose --profile gpu --profile observability --profile public up -d --build
```

Caddy richiede che il DNS risolva correttamente prima di ottenere il certificato. Grafana deve continuare a richiedere il login. Il PDF metodologico e disponibile all'indirizzo `/fondazione-semplice-metodo.pdf`.
