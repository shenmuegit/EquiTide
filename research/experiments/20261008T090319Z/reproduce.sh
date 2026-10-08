#!/bin/sh
set -eu
cd "$(dirname "$0")/../../.."
.venv/bin/python research/experiments/20261008T090319Z/restore_cache.py
.venv/bin/python research/experiments/20261008T090319Z/forward.py --reproduce
.venv/bin/python research/experiments/20261008T090319Z/evaluate.py --reproduce
.venv/bin/python research/experiments/20261008T090319Z/audit.py
.venv/bin/python research/experiments/20261008T090319Z/audit_forward.py
.venv/bin/python checks/strategy_registry.py
