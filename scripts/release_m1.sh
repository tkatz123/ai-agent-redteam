#!/usr/bin/env bash
set -euo pipefail
git add -A
git commit -m "release: v0.1-first-compromise (reply trigger + multipage + batch ASR)"
git tag -a v0.1-first-compromise -m "M1: first end-to-end compromise"
echo "Tagged v0.1-first-compromise"
