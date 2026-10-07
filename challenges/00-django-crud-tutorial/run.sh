#!/usr/bin/env bash
# Start backend + frontend, or launch the coaching agent.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "$ROOT/../../shared/scripts/pick_python.sh"
AGENT="$ROOT/../../shared/coach/agent.py"

if [[ "${1:-}" == "--agent" ]]; then
  cd "$ROOT"
  exec "$PYTHON" "$AGENT" "${@:2}"
fi

cd "$ROOT/backend"
if [[ ! -d .venv ]]; then
  "$PYTHON" -m venv .venv
  # shellcheck disable=SC1091
  source .venv/bin/activate
  pip install -q -r requirements.txt
else
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

python manage.py migrate --verbosity 0
python manage.py seed_desk

if [[ "${1:-}" == "--backend" ]]; then
  echo "Backend: http://127.0.0.1:8005/api/health/"
  exec python manage.py runserver 127.0.0.1:8005
fi

cd "$ROOT/frontend"
if [[ ! -d node_modules ]]; then
  npm install
fi

if [[ "${1:-}" == "--frontend" ]]; then
  exec npm run dev
fi

cleanup() {
  kill "$BACK_PID" "$FRONT_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

cd "$ROOT/backend"
# shellcheck disable=SC1091
source .venv/bin/activate
python manage.py runserver 127.0.0.1:8005 &
BACK_PID=$!

cd "$ROOT/frontend"
npm run dev &
FRONT_PID=$!

echo ""
echo "============================================"
echo " Campus Club Desk (CRUD tutorial) is running"
echo " UI:  http://127.0.0.1:5178"
echo " API: http://127.0.0.1:8005/api/health/"
echo " Tests: ./test.sh"
echo " Coach: ./run.sh --agent"
echo "============================================"
wait
