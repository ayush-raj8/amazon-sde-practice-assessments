#!/usr/bin/env bash
# Usage: ./run_challenge.sh 01-movies-search [--agent|--backend|--frontend]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
NAME="${1:-}"
if [[ -z "$NAME" ]]; then
  echo "Usage: $0 <challenge-folder> [--agent|--backend|--frontend]"
  echo "Available:"
  ls "$ROOT/challenges"
  exit 1
fi
shift || true
DIR="$ROOT/challenges/$NAME"
if [[ ! -d "$DIR" ]]; then
  echo "Unknown challenge: $NAME"
  exit 1
fi
cd "$DIR"
exec ./run.sh "$@"
