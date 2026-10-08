#!/bin/sh
set -eu
cd "$(dirname "$0")/../../.."
.venv/bin/python research/experiments/20261008T210819Z/restore_cache.py
.venv/bin/python research/experiments/20261008T210819Z/forward.py --reproduce
.venv/bin/python research/experiments/20261008T210819Z/evaluate.py --reproduce
.venv/bin/python research/experiments/20261008T210819Z/audit.py
.venv/bin/python research/experiments/20261008T210819Z/audit_forward.py
.venv/bin/python checks/strategy_registry.py
