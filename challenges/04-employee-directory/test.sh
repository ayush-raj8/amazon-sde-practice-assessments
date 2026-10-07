#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "$ROOT/../../shared/scripts/pick_python.sh"
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

python manage.py makemigrations employees --verbosity 0
python manage.py migrate --verbosity 0
exec python -m pytest "$ROOT/tests" -q
