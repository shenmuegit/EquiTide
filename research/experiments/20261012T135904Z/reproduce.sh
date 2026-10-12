#!/usr/bin/env bash
set -euo pipefail
./.venv/bin/python research/experiments/20261012T135904Z/audit.py
python3 checks/strategy_registry.py
