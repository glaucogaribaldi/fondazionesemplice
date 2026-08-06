# Pubblicazione GitHub

## Prima pubblicazione

```bash
git init
git add .
git commit -m "feat: scaffold paper-first trading appliance"
git branch -M main
git remote add origin https://github.com/OWNER/fondazionesemplice.git
git push -u origin main
```

Creare il repository privato all’inizio. Rendere pubblico solo dopo revisione di licenze, sicurezza e assenza di segreti.

## Release installabile

```bash
git tag -s v0.1.0 -m "Fondazione Semplice v0.1.0 alpha"
git push origin v0.1.0
```

L’installer OpenClaw deve ricevere `v0.1.0` o il relativo commit, mai un branch mobile.

## Checklist

- GitHub Actions verde;
- secret scanning e Dependabot attivi;
- repository senza `.env`, dati OctoBot, log o modelli;
- README dichiara stato alpha e paper-only;
- release notes includono limiti noti;
- tag firmato o commit immutabile comunicato a OpenClaw.
