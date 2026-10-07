#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
FAIL=0
for d in "$ROOT"/challenges/*/; do
  name="$(basename "$d")"
  echo ""
  echo "======== $name ========"
  if (cd "$d" && ./test.sh); then
    echo "[ok] $name — unexpected full pass on buggy starter? check defects"
  else
    echo "[expected failures present] $name"
  fi
done
echo ""
echo "Note: starter code is supposed to fail some tests. Fix challenges one by one."
exit 0
