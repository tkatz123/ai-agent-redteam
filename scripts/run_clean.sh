#!/usr/bin/env bash
set -euo pipefail
trap 'echo "[ERR] $0 failed at line $LINENO" >&2' ERR
# Seed clean page, then run clean pipeline with normal policy
scripts/seed_poison.sh clean
./.venv/bin/python -m src.app --mode clean --policy normal
