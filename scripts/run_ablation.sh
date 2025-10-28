#!/usr/bin/env bash
set -euo pipefail
PYBIN="${PYBIN:-python}"
VARIANTS="${VARIANTS:-comment css zwc collusion}"
RUNS="${RUNS:-20}"

echo "== Ablations on variants: ${VARIANTS} (N=${RUNS} each) =="

for prof in baseline D1 D2 D2+structured; do
  echo "--- ${prof} ---"
  "$PYBIN" -m src.eval.batch_runner --runs "${RUNS}" --policy normal --mode attack \
    --variants ${VARIANTS} \
    --tool auto \
    --defense_profile "${prof}"
done
