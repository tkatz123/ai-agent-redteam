#!/usr/bin/env bash
set -euo pipefail
git add -A
git commit -m "release: v0.2-defense-v1-blocks (regex+ML detectors, reports)"
git tag -a v0.2-defense-v1-blocks -m "M2: Defense v1 with detectors"
echo "Tagged v0.2-defense-v1-blocks"