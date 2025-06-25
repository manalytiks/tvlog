# TradingView Webhook Server

This is a Flask-based webhook listener for TradingView alerts.

## Routes

- `POST /tvwebhook`: Accepts JSON webhook payloads
- `GET /`: Health check route

## Deployment (Render.com)

- Link GitHub repo
- Select Python environment
- Build Command: `pip install -r requirements.txt`
- Start Command: `python web.py`
