# Let It Out

A private unsent-letter experience with a FastAPI backend and Nuxt frontend.

## Local development

Start the API from the repository root:

```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
cp .env.example .env
./venv/bin/uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

In another terminal, start the frontend:

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 3000
```

The frontend calls `http://127.0.0.1:8000` by default. Override it with
`NUXT_PUBLIC_API_BASE` in `frontend/.env`.

## Environment

Groq reflection is enabled by default. Set `AI_API_KEY` in the root `.env` file to use it. If the
key is missing or the provider cannot be reached, the API returns a local fallback reflection.

`ALLOWED_ORIGINS` accepts a comma-separated list. Local development uses:

```dotenv
ALLOWED_ORIGINS=http://127.0.0.1:3000,http://localhost:3000
```

Use the exact deployed frontend origin in production. The root and frontend `.env` files are ignored
by Git and must never be committed.

## Checks

```bash
./venv/bin/pytest -q
./venv/bin/ruff check backend
cd frontend
npm run typecheck
npm run build
```
