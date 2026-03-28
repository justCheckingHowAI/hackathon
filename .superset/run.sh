#!/bin/sh
set -eu

workspace_path="${SUPERSET_WORKSPACE_PATH:-$(pwd)}"
cd "$workspace_path"

if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

bootstrap="${SUPERSET_RUN_BOOTSTRAP:-1}"
backend_host="${BACKEND_HOST:-0.0.0.0}"
backend_port="${BACKEND_PORT:-8001}"
frontend_host="${FRONTEND_HOST:-0.0.0.0}"
frontend_port="${FRONTEND_PORT:-8000}"
frontend_api_url="${VITE_API_URL:-${BACKEND_URL:-http://127.0.0.1:${backend_port}}}"

backend_cmd="${SUPERSET_RUN_BACKEND_CMD:-PYTHONPATH=api .venv/bin/uvicorn main:app --app-dir api --reload --host $backend_host --port $backend_port}"
frontend_cmd="${SUPERSET_RUN_FRONTEND_CMD:-VITE_API_URL=\"$frontend_api_url\" npm run dev -- --host $frontend_host --port $frontend_port}"

if [ "$bootstrap" = "1" ]; then
  if [ ! -x .venv/bin/python ]; then
    printf 'Creating backend virtualenv...\n'
    python3 -m venv .venv
    .venv/bin/pip install -r api/requirements.txt
  fi

  if [ ! -d app/node_modules ]; then
    printf 'Installing frontend dependencies...\n'
    (
      cd app
      npm install
    )
  fi
fi

printf 'Starting backend on http://127.0.0.1:%s\n' "$backend_port"
(
  cd "$workspace_path"
  exec sh -lc "$backend_cmd"
) &
backend_pid=$!

printf 'Starting frontend on http://127.0.0.1:%s\n' "$frontend_port"
(
  cd "$workspace_path/app"
  exec sh -lc "$frontend_cmd"
) &
frontend_pid=$!

cleanup() {
  if [ -n "${backend_pid:-}" ]; then
    kill "$backend_pid" 2>/dev/null || true
    wait "$backend_pid" 2>/dev/null || true
  fi

  if [ -n "${frontend_pid:-}" ]; then
    kill "$frontend_pid" 2>/dev/null || true
    wait "$frontend_pid" 2>/dev/null || true
  fi
}

wait_for_first_exit() {
  while :; do
    if ! kill -0 "$backend_pid" 2>/dev/null; then
      wait "$backend_pid"
      return $?
    fi

    if ! kill -0 "$frontend_pid" 2>/dev/null; then
      wait "$frontend_pid"
      return $?
    fi

    sleep 1
  done
}

trap 'cleanup; exit 0' INT TERM
trap 'cleanup' EXIT

wait_for_first_exit
