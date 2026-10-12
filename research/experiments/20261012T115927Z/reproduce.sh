#!/usr/bin/env bash
set -euo pipefail
./.venv/bin/python research/experiments/20261012T115927Z/audit.py
python3 checks/strategy_registry.py
