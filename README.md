# Gemellus Hackathon

Minimalny stack do demo składa się z:
- `app`: frontend Vite/React
- `api`: FastAPI z dashboardem, endpointami danych i integracją Vapi
- `api-worker`: worker `taskiq`
- `postgres`: baza danych seedowana z `api/sql`
- `redis`: broker dla workerów

## Wymagania

- Docker + Docker Compose
- albo lokalnie: Python 3.12+ i Node 20+

## Konfiguracja

1. Skopiuj env:

```bash
cp .env.example .env
```

2. Uzupełnij minimum:

```dotenv
POSTGRES_PASSWORD=change-me
GCP_PROJECT_ID=twoj-projekt
VAPI_PRIVATE_KEY=twoj_vapi_private_key
VAPI_DEFAULT_PHONE_NUMBER=+12604002243
```

`VAPI_DEFAULT_PHONE_NUMBER_ID` jest opcjonalne. Jeśli go nie ustawisz, API spróbuje znaleźć numer po `VAPI_DEFAULT_PHONE_NUMBER`.

## Start z Docker

`docker-compose.yml` jest bazą, a `dev-docker-compose.yml` jest override pod local dev.

Najprostszy wariant developerski:

```bash
docker compose -f docker-compose.yml -f dev-docker-compose.yml up --build
```

Po starcie:
- frontend: `http://localhost:8000`
- API: `http://localhost:8001`
- dashboard API: `http://localhost:8001/ui`
- health: `http://localhost:8001/health`
- health DB: `http://localhost:8001/health/db`
- Postgres: `127.0.0.1:${POSTGRES_PORT:-5432}`
- Redis: `127.0.0.1:6379`

## Start lokalny

Najwygodniej odpalić infrastrukturę pomocniczą z Dockera, a app/API lokalnie.

1. Postgres i Redis:

```bash
docker compose -f docker-compose.yml -f dev-docker-compose.yml up -d postgres redis
```

2. Backend:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r api/requirements.txt
set -a
source .env
set +a
export DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@127.0.0.1:${POSTGRES_PORT:-5432}/${POSTGRES_DB}"
export REDIS_URL="redis://127.0.0.1:6379/0"
PYTHONPATH=api uvicorn main:app --app-dir api --reload --port 8001
```

3. Worker:

```bash
source .venv/bin/activate
set -a
source .env
set +a
export DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@127.0.0.1:${POSTGRES_PORT:-5432}/${POSTGRES_DB}"
export REDIS_URL="redis://127.0.0.1:6379/0"
PYTHONPATH=api taskiq worker taskiq_broker:broker tasks
```

4. Frontend:

```bash
cd app
npm install
npm run dev -- --host 0.0.0.0 --port 8000
```

## Vapi API

Dostępne endpointy backendowe:
- `GET /vapi/assistant/{assistant_id}`
- `GET /vapi/phone-numbers`
- `POST /vapi/calls`

Przykład outbound call:

```bash
curl -X POST http://127.0.0.1:8001/vapi/calls \
  -H 'Content-Type: application/json' \
  -d '{
    "assistantId": "YOUR_ASSISTANT_ID",
    "customerNumber": "+48XXXXXXXXX"
  }'
```

Jeśli chcesz nadpisać numer źródłowy na pojedynczy request, możesz dodać `phoneNumberId` do payloadu.

## Testy

```bash
PYTHONPATH=api .venv/bin/python -m pytest api/tests/test_main.py -q
```
