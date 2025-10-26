#!/usr/bin/env bash
set -euo pipefail

# Choose python binary: prefer local venv, else system python
PYBIN="${PYBIN:-./.venv/bin/python}"
if [ ! -x "$PYBIN" ]; then
  if command -v python >/dev/null 2>&1; then
    PYBIN="python"
  elif command -v python3 >/dev/null 2>&1; then
    PYBIN="python3"
  else
    echo "No python interpreter found." >&2
    exit 127
  fi
fi
export PYBIN

echo "== Seeding attack: comment =="
bash scripts/seed_poison.sh comment

echo "== Baseline (normal) =="
"$PYBIN" -m src.app --mode attack --policy normal

echo "== Defense (strict) =="
CONSENT_MODE=always "$PYBIN" -m src.app --mode attack --policy strict

echo "== Batch quick compare (N=10) =="
"$PYBIN" -m src.eval.batch_runner --runs 10 --policy normal --mode attack --variants comment css zwc collusion
CONSENT_MODE=always "$PYBIN" -m src.eval.batch_runner --runs 10 --policy strict  --mode attack --variants comment css zwc collusion

./scripts/asr_compare.py
