#!/bin/sh
set -eu
cd "$(dirname "$0")/../../.."
.venv/bin/python research/experiments/20261008T230850Z/restore_cache.py
.venv/bin/python research/experiments/20261008T230850Z/forward.py --reproduce
.venv/bin/python research/experiments/20261008T230850Z/evaluate.py --reproduce
.venv/bin/python research/experiments/20261008T230850Z/audit.py
.venv/bin/python research/experiments/20261008T230850Z/audit_forward.py
.venv/bin/python checks/strategy_registry.py
