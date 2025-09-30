#!/usr/bin/env bash
set -euo pipefail
trap 'echo "[ERR] $0 failed at line $LINENO" >&2' ERR
# Variant can be overridden: VARIANT=css scripts/run_attack.sh
VARIANT="${VARIANT:-comment}"
scripts/seed_poison.sh "$VARIANT"
# Baseline vulnerable policy to demonstrate compromise
./.venv/bin/python -m src.app --mode attack --policy normal
