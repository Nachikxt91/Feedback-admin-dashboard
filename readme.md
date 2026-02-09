# Admin Dashboard

Part of the [Feedback System](../README.md). See root README for full documentation.

## Quick Start

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py --server.port 8502
```

## Secrets

Create `.streamlit/secrets.toml`:
```toml
API_URL = "http://localhost:8000/api"
API_KEY = "your_admin_api_key"
```

## Live Demo

https://feedback-dashboard.streamlit.app/