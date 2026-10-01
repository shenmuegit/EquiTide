#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
.venv/bin/python research/experiments/20261001T234032Z/evaluate.py --reproduce
.venv/bin/python research/experiments/20261001T234032Z/audit.py
.venv/bin/python research/experiments/20261001T133655Z/check_kernel.py
python3 checks/strategy_registry.py
