#!/bin/sh
set -eu
cd "$(dirname "$0")/../../.."
.venv/bin/python research/experiments/20261008T150549Z/restore_cache.py
.venv/bin/python research/experiments/20261008T150549Z/forward.py --reproduce
.venv/bin/python research/experiments/20261008T150549Z/evaluate.py --reproduce
.venv/bin/python research/experiments/20261008T150549Z/audit.py
.venv/bin/python research/experiments/20261008T150549Z/audit_forward.py
.venv/bin/python checks/strategy_registry.py
