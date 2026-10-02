#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
.venv/bin/python research/experiments/20261002T215033Z/forward.py --reproduce
.venv/bin/python research/experiments/20261002T215033Z/evaluate.py --reproduce
.venv/bin/python research/experiments/20261002T215033Z/audit.py
.venv/bin/python research/experiments/20261002T215033Z/audit_forward.py
.venv/bin/python checks/strategy_registry.py
