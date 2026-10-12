#!/usr/bin/env bash
set -euo pipefail
./.venv/bin/python research/experiments/20261012T060005Z/evaluate.py --reproduce
./.venv/bin/python research/experiments/20261012T060005Z/audit.py
python3 checks/strategy_registry.py
