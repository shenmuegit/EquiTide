"""Read-only final binding of the frozen volume/span batch and preserved accounts."""
from pathlib import Path
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
assert (prior['lines'], prior['preserved_ids'], prior['canonical']) == (6847, 3376, 3374)
canonical = len({registry.fingerprint(v['spec']) for v in records.values()})
assert (len(lines), len(records), canonical) == (6901, 3403, 3401)
assert hashlib.sha256(b''.join(lines[:prior['lines']])).hexdigest() == prior['ledger_sha256']
for fp, rec in prior['records'].items():
    assert records[fp] == rec, fp
assert not [v for v in records.values() if v['status'] == 'reserved']
hist, fb, grid = [read(T / n) for n in ('batch.json', 'forward_batch.json', 'grid_batch.json')]
assert (len(hist), len(fb), len(grid)) == (24, 3, 38)
assert sum(x['role'] == 'component' for x in hist) == 12
assert all(x.get('asset') == 'BTC' for x in hist if x['role'] == 'component')
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
assert len((T / 'finish.log').read_text().splitlines()) == 27

fresh = [c for c in r['configs'].values() if c['is_new']]
summary = r['summary']
assert (summary['new_configs'], summary['new_component_configs'], summary['new_combination_configs'],
        summary['new_cost_scenes'], summary['new_minute_NAV_points']) == (24, 12, 12, 72, 18675504)
assert summary['positive_1x'] == sum(c['scenes']['1']['net_return_pct'] > 0 for c in fresh)
assert summary['positive_3x'] == sum(c['scenes']['3']['net_return_pct'] > 0 for c in fresh)
assert set(summary['passed']) == {c['name'] for c in fresh if all(c['criteria'].values())}
assert set(summary['rejected']) == {c['name'] for c in fresh if not all(c['criteria'].values())}
for b in hist:
    c, sp = r['configs'][b['name']], read(R / b['spec'])
    assert all(len(z['folds']) == 6 and z['NAV_points'] == 259382 for z in c['scenes'].values())
    assert (c['status'] == 'passed') == all(c['criteria'].values())
    assert c['raw_weights'] == [.5, .5] and c['BTC_volume_lookback_days'] in (20, 30, 40) and c['BTC_minimum_volume_ratio'] in (.9, 1.1)
    if c['role'] == 'component':
        assert c['asset'] == 'BTC' and c['capital_usdt'] == sp['parameters']['initial_capital_usdt'] == 1000
        assert sp['family'] == 'daily-close-range-relative-quote-volume' and sp['universe'] == ['BTC/USDT']
        assert sp['parameters']['volume_lookback_days'] == c['BTC_volume_lookback_days']
        assert sp['parameters']['minimum_volume_ratio'] == c['BTC_minimum_volume_ratio'] in (.9, 1.1)
        assert sp['parameters']['entry_lookback_days'] == 15 and sp['parameters']['exit_lookback_days'] == 30
        assert c['EMA_span_days'] is None
    else:
        assert [q['weight'] for q in sp['components']] == [.5, .5]
        assert sp['parameters']['initial_capital_usdt'] == c['capital_usdt'] == 2000
        children = [records[q['fingerprint']]['spec'] for q in sp['components']]
        assert [x['parameters']['initial_capital_usdt'] for x in children] == [1000, 1000]
        assert children[0]['universe'] == ['BTC/USDT'] and children[1]['universe'] == ['ETH/USDT']
        assert children[0]['parameters']['volume_lookback_days'] == c['BTC_volume_lookback_days']
        assert children[0]['parameters']['minimum_volume_ratio'] == c['BTC_minimum_volume_ratio']
        assert children[1]['parameters']['EMA_span_days'] == c['EMA_span_days'] == 30
        assert children[1]['parameters']['EMA_symmetric_band'] == .0125
for mapping in (r['source_hashes'], plan['reused_code_sha256']):
    for path, hsh in mapping.items():
        assert sha(R / path) == hsh, path
assert sha(T / 'preflight.py') == plan['preflight_sha256']
assert plan['grid']['predeclared_focus'] == {'BTC_volume_lookback_days': 30, 'BTC_minimum_volume_ratio': 1.1}
assert plan['grid']['raw_weights'] == [.5, .5] and plan['grid']['component_capitals_usdt'] == [1000, 1000]
assert len(plan['read_only_component_refs']) == 8 and len(plan['read_only_grid_refs']) == 6
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
        ah['ETH_pandasEMA_causal_decisions'], ah['BTC_disjoint_quote_volume_causal_decisions']) == (72, 18675504, 6480, 0, 6480)
assert ah['Decimal_fills_independently_checked'] == summary['new_component_fills'] == 204
assert summary['new_live_orders'] == 0
assert cmp['report_sha256'] == h['report_sha256'] == sha(T / 'report.json') and len(cmp['comparisons']) == 36
for row in cmp['comparisons']:
    c, o = r['configs'][row['config']], r['configs'][row['comparator']]
    assert row['same_raw_weights'] == c['raw_weights'] == o['raw_weights'] == [.5, .5]
    assert row['same_funded_capitals'] == [1000, 1000] and c['capital_usdt'] == o['capital_usdt'] == 2000
    assert o['BTC_minimum_volume_ratio'] == 1 and c['EMA_span_days'] == o['EMA_span_days'] == 30
    if row['kind'] == 'SAME_N_RATIO1':
        assert c['BTC_volume_lookback_days'] == o['BTC_volume_lookback_days']
    else:
        assert row['kind'] == 'N30_RATIO1_CENTER' and o['BTC_volume_lookback_days'] == 30
    assert row['return_differences_pp'] == {k: c['scenes'][k]['net_return_pct'] - o['scenes'][k]['net_return_pct'] for k in ('1', '2', '3')}
    assert row['minute_DD3_difference_pp'] == c['scenes']['3']['max_drawdown_pct'] - o['scenes']['3']['max_drawdown_pct']
    assert row['all_cost_NAV_identical'] == all(c['scenes'][k]['NAV_sha256_f64le'] == o['scenes'][k]['NAV_sha256_f64le'] for k in ('1', '2', '3'))
for pair in cmp['qualified_pair_comparisons']:
    xs = [next(x for x in cmp['comparisons'] if x['config'] == n and x['kind'] == pair['kind']) for n in pair['pair']]
    rv, dd = [v for x in xs for v in x['return_differences_pp'].values()], [x['minute_DD3_difference_pp'] for x in xs]
    assert pair['joint_improvement_both_years'] == (all(v >= 0 for v in rv) and all(v <= 0 for v in dd) and (any(v > 0 for v in rv) or any(v < 0 for v in dd)))
for kind, key in (('SAME_N_RATIO1', 'jointly_improved_pairs_vs_same_N_ratio1'), ('N30_RATIO1_CENTER', 'jointly_improved_pairs_vs_center')):
    assert cmp[key] == sum(x['joint_improvement_both_years'] for x in cmp['qualified_pair_comparisons'] if x['kind'] == kind)
assert h['new_scenes_already_in_any_prior_report'] + h['new_scenes_not_in_any_prior_report'] == 72
for path, hsh in h['all_prior_report_sha256'].items():
    assert sha(R / path) == hsh, path
for filename, total, newcount in (('sensitivity.csv', 114, 72), ('folds.csv', 684, 432)):
    with (T / filename).open() as file:
        rows = list(csv.DictReader(file))
    assert len(rows) == total and sum(x['is_new'] == 'True' for x in rows) == newcount
    for row in rows:
        z = r['configs'][row['config']]['scenes'][row['cost']]
        z = z['folds'][int(row['fold']) - 1] if filename == 'folds.csv' else z
        for label, key in (('net_return_pct', 'net_return_pct'), ('minute_DD_pct', 'max_drawdown_pct'), ('Sharpe365', 'sharpe_365'), ('Calmar', 'calmar')):
            assert row[label] == ('' if z[key] is None else str(z[key]))
fr = plan['forward_resume']
assert f['resume_utc'] == '2026-10-10T21:00:00Z' and f['cutoff_utc'] == '2026-10-10T23:00:00Z'
assert (fr['prior_NAV_points'], fr['total_NAV_points'], fr['cumulative_minutes']) == (12789, 12909, 12899)
assert af['new_closed_marks_per_asset'] == 120 and af['new_daily_decisions'] == af['new_reference_points'] == af['new_executions'] == 0
assert sha(R / f['frozen_plan_path']) == f['frozen_plan_sha256'] == '2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
replay, execution, checks = [read(T / n) for n in ('reproduction_execution.json', 'execution_steps.json', 'final_checks.json')]
assert (len(replay), len(execution), len(checks)) == (7, 6, 3) and all(x['exit_code'] == 0 for x in replay + execution + checks)
assert 'PASS:all72 NEW volume-ratio scenes and full report exactly reproduced' in (T / 'reproduce.log').read_text()
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
assert paper['observations'] == prior['paper_observations'] == 38 and paper['last_observation_id'] == prior['paper_observation']
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
    counts[key] += 24
counts['passed'] += len(summary['passed'])
counts['rejected'] += len(summary['rejected'])
counts['observation_records_excluded'] += 3
assert feed['research']['counts'] == counts and feed['research']['last_run']['id'] == T.name
assert feed['paper']['observation_id'] == paper['last_observation_id']
monitor = read(T / 'monitor_check.log')
assert monitor['ok'] and monitor['protected_inputs_unchanged'] and monitor['observations'] == 38 and monitor['research_configs'] == 2663
base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R, text=True).strip()
assert base == prior['base_head'] == 'd96a4a72a7dff8cc2150d770d1fe14e6aae5bbe8'
files = sorted(p for p in T.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ('verification.json', 'verify.log'))
files += [L, R / 'research/automation/README.md', R / 'research/monitor/latest.json', R / 'research/monitor/configs.json.gz']
out = {
    'passed': True, 'verified_at_utc': datetime.now(timezone.utc).isoformat(), 'base_commit': base,
    'registry': {'rows': len(lines), 'canonical': canonical, 'preserved_ids': len(records), 'unchanged_prior_rows': prior['lines'], 'new_reserved_and_finished': 27, 'new_historical_trials': 24, 'new_legacy_cutoffs': 3, 'pending': 0},
    'historical_summary': summary,
    'new_qualified_cross_period_parameter_pairs': len(summary['new_both_periods_passed_combination_pairs']),
    'new_cross_period_return_paths': h['qualified_cross_period_pairs_not_in_any_prior_report'],
    'jointly_improved_both_period_pairs': cmp['jointly_improved_pairs_vs_same_N_ratio1'],
    'paper10_accounts_unchanged': True, 'both_sensitivity_plots_visually_reviewed': True,
    'checks': {'all7_replay_phases_exit_zero': True, 'all6_actual_phases_exit_zero': True, 'all3_final_checks_exit_zero': True,
               'all72new_and42old_cost_scenes_verified': True, 'only_new_BTC_components_simulated_ETH_read_only': True,
               'explicit_raw50_50_funds1000_1000_preserved_no_rebalance': True, 'all684folds_114cost_rows_verified': True,
               'old_results_criteria_and_prior_ledger_rows_preserved': True, 'initial16_actual_evidence_complete': True,
               'paper38_plan_state_journals_UI_preserved': True},
    'audits': [ah, af], 'protected_sha256': prior['protected_sha256'],
    'files_sha256': {str(p.relative_to(R)): sha(p) for p in files}}
(T / 'verification.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'passed': True, **out['registry'], 'joint_improvements': out['jointly_improved_both_period_pairs'], 'new_qualified_paths': out['new_cross_period_return_paths'], 'protected_files': len(prior['protected_sha256']), 'files_hashed': len(files)}))
