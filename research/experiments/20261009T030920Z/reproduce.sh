#!/bin/sh
set -eu
cd "$(dirname "$0")/../../.."
.venv/bin/python research/experiments/20261009T030920Z/restore_cache.py
.venv/bin/python research/experiments/20261009T030920Z/forward.py --reproduce
.venv/bin/python research/experiments/20261009T030920Z/evaluate.py --reproduce
.venv/bin/python research/experiments/20261009T030920Z/audit.py
.venv/bin/python research/experiments/20261009T030920Z/audit_forward.py
.venv/bin/python checks/strategy_registry.py
