#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
.venv/bin/python research/experiments/20261007T185556Z/restore_cache.py
.venv/bin/python research/experiments/20261007T185556Z/forward.py --reproduce
.venv/bin/python research/experiments/20261007T185556Z/replay_driver.py --reproduce
.venv/bin/python research/experiments/20261007T185556Z/audit.py
.venv/bin/python research/experiments/20261007T185556Z/audit_forward.py
.venv/bin/python checks/strategy_registry.py
