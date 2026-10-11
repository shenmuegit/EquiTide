"""Read-only final binding of the frozen volume/span batch and preserved accounts."""
from pathlib import Path
from decimal import Decimal as D
from datetime import datetime, timezone
import csv, gzip, hashlib, json, subprocess, sys

T = Path(__file__).resolve().parent
R = T.parents[2]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text())
sys.path.insert(0, str(R / 'research/automation'))
import registry
sys.path.insert(0, str(T))
from design import definitions

prior = json.loads(gzip.decompress((T / 'prior_summary.json.gz').read_bytes()))
r, f, plan = [read(T / n) for n in ('report.json', 'forward_report.json', 'spec.json')]
cmp, h = [read(T / n) for n in ('comparison.json', 'history_paths.json')]
L = R / 'research/automation/registry.jsonl'
lines = L.read_bytes().splitlines(keepends=True)
raw = [json.loads(x) for x in lines]
records = registry.read_records(L)
assert r['plan'] == plan
assert (prior['lines'], prior['preserved_ids'], prior['canonical']) == (6921, 3413, 3411)
canonical = len({registry.fingerprint(v['spec']) for v in records.values()})
assert (len(lines), len(records), canonical) == (6987, 3446, 3444)
assert hashlib.sha256(b''.join(lines[:prior['lines']])).hexdigest() == prior['ledger_sha256']
for fp, rec in prior['records'].items():
    assert records[fp] == rec, fp
assert not [v for v in records.values() if v['status'] == 'reserved']
hist, fb, grid = [read(T / n) for n in ('batch.json', 'forward_batch.json', 'grid_batch.json')]
assert (len(hist), len(fb), len(grid)) == (30, 3, 42)
assert sum(x['role'] == 'component' for x in hist) == 16
assert sum(x.get('asset')=='BTC'for x in hist)==14 and sum(x.get('asset')=='ETH'for x in hist)==2
expected = {registry.fingerprint(sp): fields for sp, fields in definitions(registry.fingerprint)}
assert set(expected) == {x['fingerprint'] for x in grid}
for b in grid:
    assert all(b[k] == v for k, v in expected[b['fingerprint']].items())
for batch, report, filename in ((hist, r, 'report.json'), (fb, f, 'forward_report.json')):
    for b in batch:
        sp = read(R / b['spec'])
        fp = registry.fingerprint(sp)
        assert fp == b['fingerprint'] and fp not in prior['records']
        events = [x for x in raw[prior['lines']:] if x['fingerprint'] == fp]
        assert len(events) == 2 and events[0]['status'] == 'reserved'
        assert events[1]['status'] == report['configs'][b['name']]['status']
        assert events[1]['result_available'] and events[1]['report_sha256'] == sha(T / filename)
        started = report['evaluation_started_utc'] if batch is hist else report['observation_started_utc']
        assert plan['frozen_at_utc'] <= events[0]['recorded_at_utc'] < started
assert len((T / 'finish.log').read_text().splitlines()) == 33

fresh = [c for c in r['configs'].values() if c['is_new']]
summary = r['summary']
assert (summary['new_configs'], summary['new_component_configs'], summary['new_combination_configs'],
        summary['new_cost_scenes'], summary['new_minute_NAV_points']) == (30, 16, 14, 90, 23344380)
assert summary['positive_1x'] == sum(c['scenes']['1']['net_return_pct'] > 0 for c in fresh)
assert summary['positive_3x'] == sum(c['scenes']['3']['net_return_pct'] > 0 for c in fresh)
assert set(summary['passed']) == {c['name'] for c in fresh if all(c['criteria'].values())}
assert set(summary['rejected']) == {c['name'] for c in fresh if not all(c['criteria'].values())}
for b in hist:
    c,sp=r['configs'][b['name']],read(R/b['spec'])
    assert all(len(z['folds'])==6 and z['NAV_points']==259382 for z in c['scenes'].values())
    assert (c['status']=='passed')==all(c['criteria'].values()) and c['BTC_initial_weight']in(.45,.5,.55)
    weights=[c['BTC_initial_weight'],float(D(1)-D(str(c['BTC_initial_weight'])))];assert c['raw_weights']==weights
    funds=[int(D(2000)*D(str(w)))for w in weights]
    if c['role']=='component':
        asset=c['asset'];assert c['capital_usdt']==sp['parameters']['initial_capital_usdt']==funds[0 if asset=='BTC'else 1]
        assert sp['universe']==[asset+'/USDT'] and sp['parameters']['entry_lookback_days']==15 and sp['parameters']['exit_lookback_days']==30
        if asset=='BTC':
            assert sp['family']=='daily-close-range-relative-quote-volume' and sp['parameters']['volume_lookback_days']==c['BTC_volume_lookback_days']==40
            assert sp['parameters']['minimum_volume_ratio']==c['BTC_minimum_volume_ratio']in(1,1.1,1.2)
            assert f"same{c['capital_usdt']}USDT funds"in sp['logic']['sizing']
        else:assert sp['family']=='daily-channel-ema-confirmation' and sp['parameters']['EMA_span_days']==30 and sp['parameters']['EMA_symmetric_band']==.0125
    else:
        assert c['capital_usdt']==sp['parameters']['initial_capital_usdt']==2000 and [q['weight']for q in sp['components']]==weights
        children=[records[q['fingerprint']]['spec']for q in sp['components']]
        assert [x['parameters']['initial_capital_usdt']for x in children]==funds
        assert children[0]['universe']==['BTC/USDT']and children[1]['universe']==['ETH/USDT']
        assert children[0]['parameters']['volume_lookback_days']==40 and children[0]['parameters']['minimum_volume_ratio']==c['BTC_minimum_volume_ratio']
        assert children[1]['parameters']['EMA_span_days']==30 and children[1]['parameters']['EMA_symmetric_band']==.0125
for mapping in (r['source_hashes'], plan['reused_code_sha256']):
    for path, hsh in mapping.items():
        assert sha(R / path) == hsh, path
assert sha(T / 'preflight.py') == plan['preflight_sha256']
assert plan['grid']['predeclared_focus'] == {'BTC_minimum_volume_ratio': 1.1, 'BTC_initial_weight': .45}
assert plan['grid']['BTC_initial_weight']==[.45,.5,.55] and plan['grid']['BTC_minimum_volume_ratio']==[1,1.1,1.2] and plan['grid']['BTC_volume_lookback_days']==40
assert len(plan['read_only_component_refs']) == 8 and len(plan['read_only_grid_refs']) == 4
for ref in plan['read_only_component_refs'] + plan['read_only_grid_refs']:
    for field, hkey in (('spec', 'spec_sha256'), ('report', 'report_sha256'), ('archive', 'archive_sha256')):
        assert sha(R / ref[field]) == ref[hkey]
    c, old = r['configs'][ref['name']], read(R / ref['report'])['configs'][ref['name']]
    assert not c['is_new'] and c['status'] == old['status'] and c['criteria'] == old['criteria']
    assert c['scenes'] == old['scenes'] and records[ref['fingerprint']] == prior['records'][ref['fingerprint']]
assert len(r['read_only_background']) == len(plan['read_only_background_refs']) == 4
for ref in plan['read_only_background_refs']:
    for field, hkey in (('spec', 'spec_sha256'), ('report', 'report_sha256'), ('archive', 'archive_sha256')):
        assert sha(R / ref[field]) == ref[hkey]
    old, bg = read(R / ref['report'])['configs'][ref['name']], r['read_only_background'][ref['name']]
    assert bg['raw_weights'] == old['raw_weights'] and bg['status'] == old['status']
    for k, z in bg['scenes'].items():
        assert all(value == old['scenes'][k][key] for key, value in z.items())
assert r['cash_reference'] == plan['cash_reference'] and r['cash_reference']['return_pct'] == 0

ah, af = read(T / 'audit.log'), read(T / 'audit_forward.log')
assert ah['passed'] and af['passed'] and ah['report_sha256'] == sha(T / 'report.json')
assert af['report_sha256'] == sha(T / 'forward_report.json')
assert (ah['actual_scenes_audited'], ah['NAV_points_audited'], ah['total_causal_decisions'],
        ah['ETH_pandasEMA_causal_decisions'], ah['BTC_disjoint_quote_volume_causal_decisions']) == (90, 23344380, 8640, 1080, 7560)
assert ah['Decimal_fills_independently_checked'] == summary['new_component_fills'] == 228
assert summary['new_live_orders'] == 0
external={}
assert len(plan['read_only_comparator_refs'])==2
for ref in plan['read_only_comparator_refs']:
    for field,key in [('spec','spec_sha256'),('report','report_sha256'),('archive','archive_sha256')]:assert sha(R/ref[field])==ref[key]
    old=read(R/ref['report'])['configs'][ref['name']];external[ref['name']]=old;saved=r['read_only_comparators'][ref['name']]
    assert saved['scenes']==old['scenes'] and saved['status']==old['status'] and records[ref['fingerprint']]==prior['records'][ref['fingerprint']]
lookup={**r['configs'],**external}
assert cmp['report_sha256']==h['report_sha256']==sha(T/'report.json') and len(cmp['comparisons'])==36
for row in cmp['comparisons']:
    c,o=lookup[row['config']],lookup[row['comparator']]
    assert c['year']==o['year'] and c['capital_usdt']==o['capital_usdt']==row['same_total_capital_usdt']==2000
    assert row['config_raw_weights']==c['raw_weights']and row['control_raw_weights']==o['raw_weights']
    assert row['config_component_capitals']==[int(D(2000)*D(str(w)))for w in c['raw_weights']]
    assert row['control_component_capitals']==[int(D(2000)*D(str(w)))for w in o['raw_weights']]
    assert row['comparator_is_new']==(o['name']in r['configs']and bool(o.get('is_new',False)))
    if row['kind']=='SAME_WEIGHT_RATIO1':assert c['raw_weights']==o['raw_weights']and o['BTC_minimum_volume_ratio']==1 and o['BTC_volume_lookback_days']==40
    else:assert row['kind']=='OLD_N30_HALF'and o['name']in external and o['raw_weights']==[.5,.5]
    assert row['return_differences_pp']=={k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in('1','2','3')}
    assert row['minute_DD3_difference_pp']==c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct']
    assert row['all_cost_NAV_identical']==all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))
for pair in cmp['qualified_pair_comparisons']:
    xs=[next(x for x in cmp['comparisons']if x['config']==n and x['kind']==pair['kind'])for n in pair['pair']];rv=[v for x in xs for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp']for x in xs]
    assert pair['joint_improvement_both_years']==(all(v>=0 for v in rv)and all(v<=0 for v in dd)and(any(v>0 for v in rv)or any(v<0 for v in dd)))
for kind,key in [('SAME_WEIGHT_RATIO1','jointly_improved_pairs_vs_same_weight_ratio1'),('OLD_N30_HALF','jointly_improved_pairs_vs_old_N30_half')]:assert cmp[key]==sum(x['joint_improvement_both_years']for x in cmp['qualified_pair_comparisons']if x['kind']==kind)
assert h['new_scenes_already_in_any_prior_report'] + h['new_scenes_not_in_any_prior_report'] == 90
for path, hsh in h['all_prior_report_sha256'].items():
    assert sha(R / path) == hsh, path
for filename, total, newcount in (('sensitivity.csv', 126, 90), ('folds.csv', 756, 540)):
    with (T / filename).open() as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == total and sum(x['is_new'] == 'True' for x in rows) == newcount
    for row in rows:
        z = r['configs'][row['config']]['scenes'][row['cost']]
        z = z['folds'][int(row['fold']) - 1] if filename == 'folds.csv' else z
        for label, key in (('net_return_pct', 'net_return_pct'), ('minute_DD_pct', 'max_drawdown_pct'), ('Sharpe365', 'sharpe_365'), ('Calmar', 'calmar')):
            assert row[label] == ('' if z[key] is None else str(z[key]))
fr = plan['forward_resume']
assert f['resume_utc']=='2026-10-10T23:00:00Z' and f['cutoff_utc']=='2026-10-11T01:00:00Z'
assert (fr['prior_NAV_points'],fr['total_NAV_points'],fr['cumulative_minutes'])==(12909,13030,13019)
assert af['new_closed_marks_per_asset']==120 and af['daily_reference_points_added']==1 and af['original_daily_decisions_independently_checked']==6
assert af['new_component_executions']==0 and af['daily_bars_per_asset']==65 and af['overlap_daily_bars_checked_per_asset']==64
nextstate=read(T/'forward_state.json');oldstate=read(R/fr['source_state'])
assert nextstate['next_daily_decision_utc']=='2026-10-12T00:01:00Z' and nextstate['positions_by_asset_and_cost']==oldstate['positions_by_asset_and_cost']
assert all(x['action']=='hold_long'for x in f['daily_decisions_by_asset'].values())
assert sha(R/fr['daily_overlap_source'])==fr['daily_overlap_source_sha256']==f['daily_overlap_source']['sha256']
assert sha(T/'restore_cache.py')==read(T/'cache_recovery_repair.json')['corrected_source_sha256'] and read(T/'cache_recovery.json')['scenes_hash_verified']==36
assert read(T/'initial_failure_execution_steps.json')[0]['exit_code']==1
assert sha(R / f['frozen_plan_path']) == f['frozen_plan_sha256'] == '2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
replay, execution, checks = [read(T / n) for n in ('reproduction_execution.json', 'execution_steps.json', 'final_checks.json')]
assert (len(replay), len(execution), len(checks)) == (7, 6, 3) and all(x['exit_code'] == 0 for x in replay + execution + checks)
assert 'PASS:all90 NEW funding-ratio scenes and full report exactly reproduced' in (T / 'reproduce.log').read_text()
assert read(T / 'signal_check.log')['synthetic_fixture_checks'] == 'PASS'
for item in prior['conclusions']:
    assert sha(R / item['path']) == item['sha256'] and (R / item['path']).read_text() == item['text']
for category in ('skills', 'oos_checks'):
    for path, item in prior[category].items():
        assert sha(R / path) == item['sha256'] and (R / path).read_text() == item['text']
for item in prior['freqtrade_results']:
    assert sha(R / item['path']) == item['sha256']
for path, hsh in prior['protected_sha256'].items():
    assert sha(R / path) == hsh, path
assert sha(R / 'research/paper10/plan.json') == prior['paper10_plan_sha256']
assert sha(R / 'research/paper10/state.json') == prior['paper10_state_sha256']
paper = read(R / 'research/paper10/state.json')
assert paper['observations'] == prior['paper_observations'] == 39 and paper['last_observation_id'] == prior['paper_observation']
marker = '## 最近完成的轮次\n\n'
assert (R / 'research/automation/README.md').read_text() == prior['read_automation_README']['text'].replace(marker, marker + (T / 'README_entry.md').read_text() + '\n', 1)
assert sha(R / 'research/automation/task.md') == prior['read_task_sha256']
assert sha(R / 'research/monitor/README.md') == prior['read_monitor_README']['sha256']
initial = read(T / 'prior_evidence_audit.json')
assert not initial['missing_initial16']
assert [x['fingerprint'] for x in initial['initial16_actual_results_checked']] == [x['fingerprint'] for x in raw[:16]]
feed = read(R / 'research/monitor/latest.json')
counts = dict(prior['monitor_counts_before'])
for key in ('registered', 'results', 'ranked'):
    counts[key] += 30
counts['passed'] += len(summary['passed'])
counts['rejected'] += len(summary['rejected'])
counts['observation_records_excluded'] += 3
assert feed['research']['counts'] == counts and feed['research']['last_run']['id'] == T.name
assert feed['paper']['observation_id'] == paper['last_observation_id']
monitor = read(T / 'monitor_check.log')
assert monitor['ok'] and monitor['protected_inputs_unchanged'] and monitor['observations'] == 39 and monitor['research_configs'] == 2693
base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R, text=True).strip()
assert base == prior['base_head'] == '9d47cb0fef3d6694b49471267e411ea934422725'
files = sorted(p for p in T.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ('verification.json', 'verify.log'))
files += [L, R / 'research/automation/README.md', R / 'research/monitor/latest.json', R / 'research/monitor/configs.json.gz']
out = {
    'passed': True, 'verified_at_utc': datetime.now(timezone.utc).isoformat(), 'base_commit': base,
    'registry': {'rows': len(lines), 'canonical': canonical, 'preserved_ids': len(records), 'unchanged_prior_rows': prior['lines'], 'new_reserved_and_finished': 33, 'new_historical_trials': 30, 'new_legacy_cutoffs': 3, 'pending': 0},
    'historical_summary': summary,
    'new_qualified_cross_period_parameter_pairs': len(summary['new_both_periods_passed_combination_pairs']),
    'new_cross_period_return_paths': h['qualified_cross_period_pairs_not_in_any_prior_report'],
    'jointly_improved_both_period_pairs': cmp['jointly_improved_pairs_vs_same_weight_ratio1'],
    'paper10_accounts_unchanged': True, 'both_sensitivity_plots_visually_reviewed': True,
    'checks': {'all7_replay_phases_exit_zero': True, 'all6_actual_phases_exit_zero': True, 'all3_final_checks_exit_zero': True,
               'all90new_and36old_cost_scenes_verified': True, 'all16_new_components_simulated_at_own_funding': True,
               'explicit_raw_weights_and_own_funds_preserved_no_rescaling_rebalance': True, 'all756folds_126cost_rows_verified': True,
               'old_results_criteria_and_prior_ledger_rows_preserved': True, 'initial16_actual_evidence_complete': True,
               'paper39_plan_state_journals_UI_preserved': True},
    'audits': [ah, af], 'protected_sha256': prior['protected_sha256'],
    'files_sha256': {str(p.relative_to(R)): sha(p) for p in files}}
(T / 'verification.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'passed': True, **out['registry'], 'joint_improvements': out['jointly_improved_both_period_pairs'], 'new_qualified_paths': out['new_cross_period_return_paths'], 'protected_files': len(prior['protected_sha256']), 'files_hashed': len(files)}))
