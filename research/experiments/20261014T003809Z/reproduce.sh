#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
round=research/experiments/20261014T003809Z
scratch=$(mktemp -d)
files=(report.json trades.csv.gz daily_equity.csv.gz decisions.csv.gz sensitivity.csv sensitivity_surface.svg data_manifest.json result.md)
restore() { for f in "${files[@]}"; do cp "$scratch/original/$f" "$round/$f"; done; rm -rf "$scratch"; }
mkdir -p "$scratch/original"
for f in "${files[@]}"; do cp "$round/$f" "$scratch/original/$f"; done
trap restore EXIT
while IFS= read -r spec_path; do
  .venv/bin/python research/automation/registry.py --ledger "$scratch/registry.jsonl" reserve "$spec_path" >/dev/null
done < <(.venv/bin/python - <<'PY'
import json
for row in json.load(open('research/experiments/20261014T003809Z/batch.json')):
    print(row['spec'])
PY
)
export VOLMANAGED_REGISTRY_LEDGER="$scratch/registry.jsonl"
.venv/bin/python "$round/evaluate.py" > "$scratch/evaluate.log"
.venv/bin/python "$round/audit.py" > "$scratch/audit.log"
.venv/bin/python - "$scratch/original/report.json" "$round/report.json" <<'PY'
import json,sys

def stable(path):
    x=json.load(open(path,encoding='utf-8'))
    x.pop('evaluation_started_utc',None)
    x.get('data_manifest',{}).pop('built_at_utc',None)
    return x
assert stable(sys.argv[1])==stable(sys.argv[2]), 'reproduced economic report differs from published report'
print('Reproduction comparison passed.')
PY
echo "Reproduced the frozen grid with isolated temporary reservations; published evidence and the main registry were restored unchanged."
