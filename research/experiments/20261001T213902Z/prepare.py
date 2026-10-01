"""Reserve off-diagonal BTC/ETH lookbacks before deriving any portfolio result."""
import copy
import gzip
import hashlib
import importlib.util
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROUND = Path(__file__).resolve().parent
ss = importlib.util.spec_from_file_location('registry', ROOT/'research/automation/registry.py')
reg = importlib.util.module_from_spec(ss); ss.loader.exec_module(reg)
ledger = ROOT/'research/automation/registry.jsonl'
records = reg.read_records(ledger)
assert len({reg.fingerprint(r['spec']) for r in records.values()}) == 248
assert all(r.get('result_available') and r['status'] != 'reserved' for r in records.values())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
sources = {'2025': '20261001T173606Z', '2026': '20261001T133655Z'}
reports = {y: json.loads((ROOT/'research/experiments'/s/'report.json').read_text()) for y,s in sources.items()}
base = reports['2026']['plan']
plan = {
 'round': ROUND.name, 'trigger_utc': '2026-10-01T21:39:02.432Z',
 'actual_first_tool_utc': '2026-10-01T21:40:14Z', 'frozen_at_utc': datetime.now(timezone.utc).isoformat(),
 'hypothesis': 'BTC and ETH need not use identical response windows; predefine the complete SMA60/65/70 cross grid and raw65/75/85%BTC initial allocations, testing robustness on two separately reported reused periods.',
 'grid': {'BTC_lookback_days': [60,65,70], 'ETH_lookback_days': [60,65,70], 'band': .01, 'raw_weight_pairs': [[.65,.35],[.75,.25],[.85,.15]], 'total_initial_usdt': 2000},
 'new_configs': 36, 'new_cost_scenes': 108, 'old_read_only_diagonal_configs': 18,
 'rules': base['rules'], 'walk_forward': base['walk_forward'], 'execution': base['execution'], 'costs': base['costs'],
 'gates': {'positive_all_costs': True, 'positive_1x_folds_min': 4, 'minute_DD3_max_pct': 25, 'neighbourhood_positive3_min_fraction': .6, 'round_trips1_min': 2, 'gross_reference_PnL_to_cost1_min': 2.5, 'no_balance_violations': True, 'terminal_flat': True},
 'sensitivity': 'For each year and rawweight pair, full3x3 BTC/ETH lookback grid: six newly reserved off-diagonals plus three finished diagonals read without recomputation. Publish all metrics and adjacent differences; weights form a third descriptive axis. Per-year/weight9-cell positive fraction is the frozen gate; do not tune from outcomes.',
 'allocation': 'Raw weights specify initial capital fractions of2000USDT; retrieve exact actual-sized BTC1300/1500/1700 and ETH700/500/300 costed components and add their absolute minute NAVs. Never multiply by weights again; no transfers/rebalancing/additional fills.',
 'confirmation': 'Matching BTClookback/ETHlookback/rawweights passes both periods only if each separately computed six-fold result passes every frozen gate. No concatenated long-period strategy or combined-period return is computed.',
 'development_history_reused': True, 'interpretation': 'Both histories already observed; 2026 outcomes influenced later exploration of2025. Multiple retrospective trials and correlated grid cells preclude pristine holdout, causal discovery or stable live profitability claims.',
 'forward_plan': {'path': 'research/experiments/20261001T113625Z/forward_plan.json', 'sha256': sha(ROOT/'research/experiments/20261001T113625Z/forward_plan.json'), 'status_at_freeze': 'not_started; originalOct2UTC00:01 start, unchanged; no forward outcomes'},
 'periods': {y: {'source_round': s, 'report': f'research/experiments/{s}/report.json', 'sha256': sha(ROOT/'research/experiments'/s/'report.json'), 'oos_start_utc': reports[y]['plan']['oos_start_utc'], 'terminal_exit_utc': reports[y]['plan']['terminal_exit_utc'], 'normalized_data': reports[y]['data']} for y,s in sources.items()},
 'prior_canonical_trials': 248,
}
(ROUND/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
snap = {'ledger_sha256': sha(ledger), 'lines': len(ledger.read_text().splitlines()), 'canonical':248, 'records': records, 'prior_conclusions': {str(p.relative_to(ROOT)): {'sha256':sha(p), 'text':p.read_text()} for p in sorted((ROOT/'research/experiments').glob('*/result.md'))}}
with (ROUND/'prior_summary.json.gz').open('wb') as f:
 with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z: z.write(json.dumps(snap,ensure_ascii=False,separators=(',',':')).encode())
batch = []
for y,report in reports.items():
 comps = {(r['asset'],r['parameters']['lookback_days'],r['parameters']['initial_capital_usdt']):(n,r) for n,r in report['configs'].items() if r['role']=='component'}
 template = next(r for r in report['configs'].values() if r['role']=='combination')
 for nb in (60,65,70):
  for ne in (60,65,70):
   if nb==ne: continue
   for wb,we in plan['grid']['raw_weight_pairs']:
    names_rows = [comps[('BTC',nb,round(2000*wb))],comps[('ETH',ne,round(2000*we))]]
    assert all(records[r['fingerprint']]['result_available'] for _,r in names_rows)
    sp = copy.deepcopy(json.loads((ROOT/template['spec_path']).read_text()))
    name = f'mixed_{y}_btc{nb}_eth{ne}_w{wb}'
    sp.update(name=name,validation_plan=str((ROUND/'spec.json').relative_to(ROOT)))
    sp['components'] = [{'fingerprint':r['fingerprint'],'weight':w} for (_,r),w in zip(names_rows,(wb,we))]
    fp=reg.fingerprint(sp)
    assert fp not in {reg.fingerprint(v['spec']) for v in records.values()}, name
    p=ROUND/'specs'/f'{name}.json';p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(sp,indent=2)+'\n')
    result=subprocess.run(['python3','research/automation/registry.py','reserve',str(p)],cwd=ROOT,capture_output=True,text=True)
    print(name,result.returncode,result.stdout.strip(),flush=True)
    if result.returncode: raise RuntimeError('STOP before calculation: '+result.stdout+result.stderr)
    batch.append({'name':name,'year':y,'BTC_lookback_days':nb,'ETH_lookback_days':ne,'raw_weights':[wb,we],'fingerprint':fp,'spec':str(p.relative_to(ROOT)),'component_names':[n for n,_ in names_rows]})
assert len(batch)==36 and len({b['fingerprint'] for b in batch})==36
(ROUND/'batch.json').write_text(json.dumps(batch,indent=2)+'\n')
print('PASS:36 distinct mixed-lookback combinations reserved before portfolio calculations;18 finished diagonal configurations read only.')
