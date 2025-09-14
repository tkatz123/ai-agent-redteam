#!/usr/bin/env bash
set -euo pipefail
cd poisoned_site
echo "Serving poisoned_site on http://127.0.0.1:8000  (Ctrl+C to stop)"
python3 -m http.server 8000
