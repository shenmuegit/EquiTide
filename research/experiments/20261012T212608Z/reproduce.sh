#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
python3 research/experiments/20261012T212608Z/check.py
python3 checks/strategy_registry.py
