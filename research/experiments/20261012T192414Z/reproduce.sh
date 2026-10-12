#!/usr/bin/env bash
set -euo pipefail
./.venv/bin/python research/experiments/20261012T192414Z/audit.py
python3 checks/strategy_registry.py
