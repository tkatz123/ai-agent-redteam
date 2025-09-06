#!/usr/bin/env bash
set -euo pipefail

# always use the venv's Python
./.venv/bin/python -m src.app --mode clean --policy normal
