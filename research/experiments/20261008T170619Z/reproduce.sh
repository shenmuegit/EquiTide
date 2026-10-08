#!/bin/sh
set -eu
cd "$(dirname "$0")/../../.."
.venv/bin/python research/experiments/20261008T170619Z/restore_cache.py
.venv/bin/python research/experiments/20261008T170619Z/forward.py --reproduce
.venv/bin/python research/experiments/20261008T170619Z/evaluate.py --reproduce
.venv/bin/python research/experiments/20261008T170619Z/audit.py
.venv/bin/python research/experiments/20261008T170619Z/audit_forward.py
.venv/bin/python checks/strategy_registry.py
