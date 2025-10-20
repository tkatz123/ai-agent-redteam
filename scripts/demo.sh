#!/usr/bin/env bash
set -euo pipefail
echo "== Seeding attack: comment =="
bash scripts/seed_poison.sh comment

echo "== Baseline (normal) =="
./.venv/bin/python -m src.app --mode attack --policy normal

echo "== Defense (strict) =="
CONSENT_MODE=always ./.venv/bin/python -m src.app --mode attack --policy strict

echo "== Batch quick compare (N=10) =="
./.venv/bin/python -m src.eval.batch_runner --runs 10 --policy normal --mode attack --variants comment css zwc
CONSENT_MODE=always ./.venv/bin/python -m src.eval.batch_runner --runs 10 --policy strict --mode attack --variants comment css zwc
./scripts/asr_compare.py
