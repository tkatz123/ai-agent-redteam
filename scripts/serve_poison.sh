#!/usr/bin/env bash
set -euo pipefail
trap 'echo "[ERR] $0 failed at line $LINENO" >&2' ERR
cd poisoned_site
echo "Serving poisoned_site on http://127.0.0.1:8000  (Ctrl+C to stop)"
python3 -m http.server 8000
