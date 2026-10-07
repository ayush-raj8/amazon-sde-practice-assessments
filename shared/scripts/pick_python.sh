# shellcheck shell=bash
# Prefer a Django-friendly Python (3.12/3.10) over bleeding-edge defaults.
if [[ -z "${PYTHON:-}" ]]; then
  if command -v python3.12 >/dev/null 2>&1; then
    PYTHON=python3.12
  elif command -v python3.10 >/dev/null 2>&1; then
    PYTHON=python3.10
  else
    PYTHON=python3
  fi
fi
export PYTHON
