#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../.."
round=research/experiments/20261013T224056Z
scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
while IFS= read -r spec_path; do
  python3 research/automation/registry.py --ledger "$scratch/registry.jsonl" reserve "$spec_path" >/dev/null
done < <(.venv/bin/python - <<'PY'
import json
for row in json.load(open('research/experiments/20261013T224056Z/batch.json')):
    print(row['spec'])
PY
)
VOLMANAGED_REGISTRY_LEDGER="$scratch/registry.jsonl" .venv/bin/python "$round/evaluate.py" > "$round/evaluate_reproduction_stdout.log"
VOLMANAGED_REGISTRY_LEDGER="$scratch/registry.jsonl" .venv/bin/python "$round/audit.py"
echo "Reproduced the frozen grid with an isolated temporary reservation ledger; no repository registry events were appended."
