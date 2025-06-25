# PricePulse POC

**PricePulse** è un servizio di price‑tracking evoluto per monitorare e prevedere i prezzi di prodotti su Amazon.it ed eBay.it, con funzionalità di forecast, smart bundles, notifiche e app mobile.

---

## 📦 Struttura del progetto

```plaintext
pricepulse-poc/
├── docker-compose.yml   # orchestrazione di DB, Redis e app
├── .env                 # variabili d'ambiente e credenziali
├── Dockerfile           # build dell'immagine Python
├── requirements.txt     # dipendenze
└── app/
    ├── main.py          # FastAPI server (health, storico prezzi)
    └── crawler.py       # script di raccolta prezzi da API
public/                  # (fase 4) dashboard statica con Chart.js
frontend/                # (fase 5) client Next.js + Tailwind
mobile/                  # (fase 6) app React Native o Flutter

```

---

## 🚀 Quickstart

1. **Configurazione**
   - Copia `docker-compose.yml`, `.env`, `Dockerfile`, `requirements.txt` nella root.
   - Riempi `.env` con le tue credenziali Amazon PA-API e eBay Developer API.

2. **Avvio locale**
   ```bash
   docker-compose up --build
   ```

3. **Verifica**
   - Health check: `GET http://localhost:8000/health` → `{ "status": "ok" }`
   - Storia prezzi: `GET http://localhost:8000/products/amazon/B0BMZYEY1V/history`

---

## 🏗 Architettura

1. **docker-compose**: tre servizi (PostgreSQL, Redis, app)
2. **Crawler** (`app/crawler.py`): recupera prezzo e timestamp da Amazon PA-API / eBay API e salva in Postgres.
3. **API** (`app/main.py`): FastAPI espone endpoint:
   - `GET /health` (health check)
   - `GET /products/{source}/{product_id}/history` (storico fino a 100 punti)
4. **Dashboard**: (futuro) static files o frontend React/Next.js + Tailwind
5. **Mobile**: (futuro) app React Native o Flutter, con notifiche push

---

## 🛠 Roadmap (step principali)

1. **Ambiente one-click**: Docker Compose + health check
2. **Crawler base**: raccolta dati e tabella `prices`
3. **API storico prezzi**: endpoint history
4. **Dashboard statica**: Chart.js su `public/index.html`
5. **Web App**: Next.js + React + Tailwind
6. **Mobile App**: React Native / Flutter
7. **Alert & notifiche**: Celery + Redis + email/webhook
8. **Forecast & Bundles**: Prophet + logica bundle
9. **Piani & pagamenti**: Stripe integration
10. **Prod & monitoring**: Kubernetes, CI/CD, Prometheus + Grafana

---

## 📝 Licenza & note

Questo progetto è un proof‑of‑concept: da qui si può estendere verso produzione, aggiungendo autenticazione, persistenza utenti, gestione piani a pagamento e supporto multi-store.
