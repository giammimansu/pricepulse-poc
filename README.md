# PricePulse POC

**PricePulse** is an advanced price-tracking service for monitoring and forecasting product prices on Amazon.it and eBay.it, featuring forecasting, smart bundles, notifications and a mobile app. :contentReference[oaicite:0]{index=0}

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
``` :contentReference[oaicite:1]{index=1}

---

## 🚀 Quickstart

1. **Configuration**  
   - Copy `docker-compose.yml`, `.env`, `Dockerfile` and `requirements.txt` into the project root.  
   - Populate `.env` with your Amazon PA-API credentials and your eBay Developer API credentials.

2. **Run Locally**  
   ```bash
   docker-compose up --build
Verify

Health check:

http
Copy
Edit
GET http://localhost:8000/health
Response:

json
Copy
Edit
{ "status": "ok" }
Price history:

http
Copy
Edit
GET http://localhost:8000/products/amazon/B0BMZYEY1V/history
Returns up to 100 data points of historical prices. README

🏗 Architecture
docker-compose
Defines three services: PostgreSQL, Redis, and the FastAPI application.

Crawler (app/crawler.py)
Fetches price and timestamp data from the Amazon PA-API and eBay API, storing results in PostgreSQL.

API (app/main.py)
Exposes endpoints via FastAPI:

GET /health — health check

GET /products/{source}/{product_id}/history — returns up to 100 price history points

Dashboard (future)
Static files or a React/Next.js + Tailwind front-end to visualize price trends.

Mobile (future)
A React Native or Flutter app with push notifications for price alerts. README

🛠 Roadmap
One-click Environment
Docker Compose setup + health check

Base Crawler
Data collection and prices table

Price History API
History endpoint implementation

Static Dashboard
Chart.js dashboard at public/index.html

Web App
Next.js + React + Tailwind

Mobile App
React Native or Flutter

Alerts & Notifications
Celery + Redis + email/webhook

Forecasting & Bundles
Prophet + bundle-generation logic

Plans & Payments
Stripe integration

Production & Monitoring
Kubernetes, CI/CD pipelines, Prometheus + Grafana README

📝 License & Notes
This project is a proof-of-concept. It can be extended for production use by adding authentication, user persistence, paid-plan management, and multi-store support. 
