#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
# Python 3.12 with numpy/pandas (bundled runtime), polars==1.44.2 in ignored .venv.
.venv/bin/python research/experiments/20261001T013355Z/download_data.py --reproduce
.venv/bin/python research/experiments/20261001T013355Z/check_accounting.py
# Explicit audit replay: asserts completed ledger status and identical archived curves;
# output goes to ignored data/runs, leaving registered reports and hashes unchanged.
.venv/bin/python research/experiments/20261001T013355Z/evaluate.py --reproduce
python3 checks/strategy_registry.py
