#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
repo_root="$PWD"
round="research/experiments/20261013T204253Z"
scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
.venv/bin/python "$round/prepare.py"
while IFS= read -r spec_path; do
  python3 research/automation/registry.py --ledger "$scratch/registry.jsonl" reserve "$spec_path" >/dev/null
done < <(.venv/bin/python - <<'PY'
import json
for row in json.load(open('research/experiments/20261013T204253Z/batch.json')):
    print(row['spec'])
PY
)
PAPER10_REGISTRY_LEDGER="$scratch/registry.jsonl" .venv/bin/python "$round/evaluate.py"
PAPER10_REGISTRY_LEDGER="$scratch/registry.jsonl" .venv/bin/python "$round/audit.py"
echo "Reproduced outputs; the committed registry already contains final records, so no finish events were appended."
