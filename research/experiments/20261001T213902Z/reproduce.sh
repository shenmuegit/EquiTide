#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
.venv/bin/python research/experiments/20261001T213902Z/evaluate.py --reproduce
.venv/bin/python research/experiments/20261001T213902Z/audit.py
python3 checks/strategy_registry.py
