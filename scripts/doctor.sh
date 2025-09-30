#!/usr/bin/env bash
set -euo pipefail
echo "== Checking venv =="
[ -x ./.venv/bin/python ] || { echo "Missing .venv. Run: make venv"; exit 1; }
./.venv/bin/python -V
echo "== Checking deps import =="
./.venv/bin/python - <<'PY'
import yaml, bs4, requests
print("imports ok")
PY
echo "== Checking scripts executable =="
for s in scripts/seed_poison.sh scripts/serve_poison.sh scripts/run_clean.sh scripts/run_attack.sh; do
  [ -x "$s" ] || { echo "Fix perms: chmod +x $s"; exit 1; }
done
echo "== Checking poisoned_site write =="
bash scripts/seed_poison.sh clean
test -f poisoned_site/index.html || { echo "seed failed"; exit 1; }
echo "== OK =="
