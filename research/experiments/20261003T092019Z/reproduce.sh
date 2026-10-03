#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
.venv/bin/python research/experiments/20261003T092019Z/forward.py --reproduce
.venv/bin/python research/experiments/20261003T092019Z/evaluate.py --reproduce
.venv/bin/python research/experiments/20261003T092019Z/audit.py
.venv/bin/python research/experiments/20261003T092019Z/audit_forward.py
.venv/bin/python checks/strategy_registry.py
