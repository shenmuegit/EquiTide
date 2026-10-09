#!/bin/sh
set -eu
cd "$(dirname "$0")/../../.."
.venv/bin/python research/experiments/20261009T070950Z/evaluate_components.py --reproduce
.venv/bin/python research/experiments/20261009T070950Z/restore_cache.py
.venv/bin/python research/experiments/20261009T070950Z/forward.py --reproduce
.venv/bin/python research/experiments/20261009T070950Z/evaluate.py --reproduce
.venv/bin/python research/experiments/20261009T070950Z/audit_components.py
.venv/bin/python research/experiments/20261009T070950Z/audit.py
.venv/bin/python research/experiments/20261009T070950Z/audit_forward.py
.venv/bin/python checks/strategy_registry.py
