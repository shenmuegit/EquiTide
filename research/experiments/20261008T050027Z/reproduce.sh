set -e
cd "$(dirname "$0")/../../.."
.venv/bin/python research/experiments/20261008T050027Z/restore_cache.py
.venv/bin/python research/experiments/20261008T050027Z/forward.py --reproduce
.venv/bin/python research/experiments/20261008T050027Z/evaluate.py --reproduce
.venv/bin/python research/experiments/20261008T050027Z/audit.py
.venv/bin/python research/experiments/20261008T050027Z/audit_forward.py
.venv/bin/python checks/strategy_registry.py

.venv/bin/python research/experiments/20261008T050027Z/supplement.py
