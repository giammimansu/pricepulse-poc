# PricePulse POC

**PricePulse** is an advanced price-tracking service for monitoring and forecasting product prices on Amazon.it and eBay.it, featuring forecasting, smart bundles, notifications and a mobile app.

---

## 📦 Project Structure

```plaintext
pricepulse-poc/
├── docker-compose.yml   # orchestrating DB, Redis and the app
├── .env                 # environment variables and credentials
├── Dockerfile           # builds the Python image
├── requirements.txt     # dependencies
└── app/
    ├── main.py          # FastAPI server (health check, price history)
    └── crawler.py       # script for fetching prices via APIs

public/                  # (phase 4) static dashboard using Chart.js  
frontend/                # (phase 5) Next.js + Tailwind client  
mobile/                  # (phase 6) React Native or Flutter app  
```

---

## 🚀 Quickstart

1. **Configuration**  
   - Copy `docker-compose.yml`, `.env`, `Dockerfile` and `requirements.txt` into the project root.  
   - Populate `.env` with your Amazon PA-API credentials and your eBay Developer API credentials.

2. **Run Locally**  
   ```bash
   docker-compose up --build
   ```

3. **Verify**  
   - **Health check**:  
     ```http
     GET http://localhost:8000/health
     ```
     Response:  
     ```json
     { "status": "ok" }
     ```
   - **Price history**:  
     ```http
     GET http://localhost:8000/products/amazon/B0BMZYEY1V/history
     ```
     Returns up to 100 data points of historical prices.

---

## 🏗 Architecture

1. **docker-compose**  
   Defines three services: PostgreSQL, Redis, and the FastAPI application.

2. **Crawler** (`app/crawler.py`)  
   Fetches price and timestamp data from the Amazon PA-API and eBay API, storing results in PostgreSQL.

3. **API** (`app/main.py`)  
   Exposes endpoints via FastAPI:  
   - `GET /health` — health check  
   - `GET /products/{source}/{product_id}/history` — returns up to 100 price history points

4. **Dashboard** (future)  
   Static files or a React/Next.js + Tailwind front-end to visualize price trends.

5. **Mobile** (future)  
   A React Native or Flutter app with push notifications for price alerts.

---

## 🛠 Roadmap

1. **One-click Environment**  
   Docker Compose setup + health check  
2. **Base Crawler**  
   Data collection and `prices` table  
3. **Price History API**  
   History endpoint implementation  
4. **Static Dashboard**  
   Chart.js dashboard at `public/index.html`  
5. **Web App**  
   Next.js + React + Tailwind  
6. **Mobile App**  
   React Native or Flutter  
7. **Alerts & Notifications**  
   Celery + Redis + email/webhook  
8. **Forecasting & Bundles**  
   Prophet + bundle-generation logic  
9. **Plans & Payments**  
   Stripe integration  
10. **Production & Monitoring**  
    Kubernetes, CI/CD pipelines, Prometheus + Grafana

---

## 📝 License & Notes

This project is a proof-of-concept. It can be extended for production use by adding authentication, user persistence, paid-plan management, and multi-store support.
