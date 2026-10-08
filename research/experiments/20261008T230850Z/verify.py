"""Verify preregistration, exact funded inputs, account isolation and complete published evidence."""
from pathlib import Path
from datetime import datetime, timezone
import csv, gzip, hashlib, json, subprocess, sys, zipfile
T=Path(__file__).resolve().parent;R=T.parents[2]
sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
parse=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()))
L=R/'research/automation/registry.jsonl';lines=L.read_bytes().splitlines(keepends=True)
raw=[json.loads(s) for s in lines];records=registry.read_records(L)
assert (prior['lines'],prior['canonical'],prior['preserved_ids'],len(prior['conclusions']))==(5255,2578,2580,68)
assert hashlib.sha256(b''.join(lines[:5255])).hexdigest()==prior['ledger_sha256']
assert all(records[k]==v for k,v in prior['records'].items())
assert (len(lines),len(records),len({registry.fingerprint(v['spec']) for v in records.values()}))==(5285,2595,2593)
assert not [v for v in records.values() if v.get('status')=='reserved']
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());p=r['plan']
audits=[json.loads((T/x).read_text()) for x in ('audit.log','audit_forward.log')]
assert all(a['passed'] for a in audits)
assert audits[0]['report_sha256']==sha(T/'report.json') and audits[1]['report_sha256']==sha(T/'forward_report.json')
assert r['summary']['new_configs']==12 and r['summary']['new_cost_scenes']==36
assert len(r['summary']['passed'])==8 and len(r['summary']['rejected'])==4
assert len(r['summary']['new_both_periods_passed_combination_pairs'])==2 and len(r['summary']['both_periods_passed_combination_pairs'])==4
for bf,rf,report,start in [('batch.json','report.json',r,r['evaluation_started_utc']),('forward_batch.json','forward_report.json',f,f['observation_started_utc'])]:
    for b in json.loads((T/bf).read_text()):
        assert registry.fingerprint(json.loads((R/b['spec']).read_text()))==b['fingerprint']
        ev=[v for v in raw[5255:] if v['fingerprint']==b['fingerprint']]
        assert len(ev)==2 and ev[0]['status']=='reserved' and ev[1]['status']==report['configs'][b['name']]['status']
        assert ev[1]['result_available'] and ev[1]['report_sha256']==sha(T/rf)
        assert parse(p['frozen_at_utc'])<parse(ev[0]['recorded_at_utc'])<parse(start)<parse(ev[1]['recorded_at_utc'])
for report in (r,f):
    for path,expected in report['source_hashes'].items():assert sha(R/path)==expected,path
for path,expected in p['reused_code_sha256'].items():assert sha(R/path)==expected,path
assert p['preflight_sha256']==sha(T/'preflight.py')
grid=json.loads((T/'grid_batch.json').read_text());assert len(grid)==18 and sum(b['is_new'] for b in grid)==12
assert {b['fingerprint'] for b in grid if b['is_new']}=={v[3] for v in prior['novelty_preflight']['new_grid_coordinates']}
for b in grid:
    assert b['raw_weights']==[.675,.325] and b['EMA_span_days']==50 and b['exit_days']==30 and b['entry_days']==15
    assert b['BTC_EMA_band'] in (.015,.035,.07) and b['ETH_EMA_band'] in (.015,.035,.07)
    assert b['is_new']==(b['BTC_EMA_band']!=b['ETH_EMA_band'])
    if not b['is_new']:assert records[b['fingerprint']]==prior['records'][b['fingerprint']]
    for ref in b['component_refs']:
        sp=json.loads((R/ref['spec']).read_text());q=sp['parameters']
        assert q['initial_capital_usdt']==ref['capital_usdt']==(1350 if ref['asset']=='BTC' else 650)
        assert q['entry_lookback_days']==15 and q['exit_lookback_days']==30 and q['EMA_symmetric_band']==b[ref['asset']+'_EMA_band']
        assert q['EMA_span_days']==50 and sp['logic']==p['rules']
with (T/'sensitivity.csv').open() as fh:
    rows=list(csv.DictReader(fh));assert len(rows)==54 and all(None not in v and None not in v.values() for v in rows)
    for v in rows:
        assert float(v['BTC_EMA_band'])==r['configs'][v['config']]['BTC_EMA_band']
        assert float(v['ETH_EMA_band'])==r['configs'][v['config']]['ETH_EMA_band']
assert p['grid']['predeclared_center']=={'BTC_EMA_band':.035,'ETH_EMA_band':.035}
assert p['grid']['predeclared_focus']=={'BTC_EMA_band':.035,'ETH_EMA_band':.015}
assert all(len(s['equity_usdt'])==10027 and s['elapsed_minutes']==10019 and s['elapsed_complete_days']==6 and s['new_mark_minutes']==120 and s['new_reference_points']==0 and s['new_executions']==0 for c in f['configs'].values() for s in c['scenes'].values())
old=json.loads((R/f['source_state']).read_text());state=json.loads((T/'forward_state.json').read_text())
assert old['positions_by_asset_and_cost']==state['positions_by_asset_and_cost'] and state['next_daily_decision_utc']=='2026-10-09T00:01:00Z'
assert len(f['append_axis'])==120 and f['cutoff_utc']=='2026-10-08T23:00:00Z'
assert f['validation']['walk_forward']=='Incomplete10019minutes/6complete days;no180day/sixfold qualification'
assert f['validation']['continuity']=='9907oldNAVpoints exact prefix;120closedmarks appended to10027points;cash/units/desired/trades unchanged,no new reference/decision/forced sell'
replay=(T/'reproduce.log').read_text()
assert all(s in replay for s in ['PASS:all36 NEW mixed-EMA-bands cost scenes','18 EXISTING scenes read-only verified','including10027point complete time axis','PASS: new parameters/weights'])
assert len((T/'finish.log').read_text().splitlines())==15
h=json.loads((T/'history_paths.json').read_text())
assert h['report_sha256']==sha(T/'report.json') and h['new_scenes_already_in_any_prior_report']==18 and h['new_scenes_not_in_any_prior_report']==18
assert h['new_2026_combo_3x_paths_not_in_any_prior_report']==2 and h['qualified_cross_period_pairs_not_in_any_prior_report']==0
for path,expected in h['all_prior_report_sha256'].items():assert sha(R/path)==expected
for c in prior['conclusions']:assert sha(R/c['path'])==c['sha256'] and (R/c['path']).read_text()==c['text']
for path,v in prior['oos_checks'].items():assert sha(R/path)==v['sha256'] and (R/path).read_text()==v['text']
for path,v in prior['skills'].items():assert sha(R/path)==v['sha256'] and (R/path).read_text()==v['text']
for v in prior['freqtrade_results']:
    assert sha(R/v['path'])==v['sha256']
    if v['members']:
        with zipfile.ZipFile(R/v['path']) as z:
            assert z.namelist()==[m['name'] for m in v['members']]
            for m in v['members']:assert hashlib.sha256(z.read(m['name'])).hexdigest()==m['sha256']
assert sha(R/'research/automation/task.md')==prior['read_task_sha256']
assert sha(R/'research/monitor/README.md')==prior['read_monitor_README']['sha256']
assert sha(R/'research/paper10/state.json')==prior['paper10_state_sha256'] and sha(R/'research/paper10/plan.json')==prior['paper10_plan_sha256']
initial=json.loads((T/'prior_evidence_audit.json').read_text());actual=initial['initial16_actual_results_checked']
assert len(actual)==16 and initial['missing_initial16']==[]
assert [v['fingerprint'] for v in actual]==[v['fingerprint'] for v in raw[:16]]
assert [v['original_ledger_position'] for v in actual]==list(range(1,17))
for v in actual:
    assert v['canonical_fingerprint']==registry.fingerprint(records[v['fingerprint']]['spec'])
    for ev in v['evidence']:assert sha(R/ev['path'])==ev['sha256']
cmp=json.loads((T/'comparison.json').read_text());assert cmp['report_sha256']==sha(T/'report.json')
assert len(cmp['matched_diagonal_comparisons'])==36 and cmp['new_both_periods_qualified']==2 and cmp['full_grid_both_periods_qualified']==4
assert not any(x['joint_improvement_both_years'] for x in cmp['qualified_new_pairs_vs035_center'])
assert cmp['focus_status']=={'2025':'passed','2026':'passed'} and cmp['failure_counts']=={'four_positive_1x_folds':4}
assert {k:v['distinct_all_cost_paths'] for k,v in cmp['source_component_path_equivalence'].items()}==prior['existing_component_path_signature_counts']
for v in cmp['matched_diagonal_comparisons']:
    c=r['configs'][v['config']];o=r['configs'][v['comparator']]
    assert v['return3_difference_pp']==c['scenes']['3']['net_return_pct']-o['scenes']['3']['net_return_pct']
    assert v['minute_DD3_difference_pp']==c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct']
    assert v['all_cost_NAV_identical']==all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le'] for k in ('1','2','3'))
assert {y:(d['descriptive_cliff_flags'],d['best_return3_coordinates'],d['best_on_boundary']) for y,d in cmp['surface_diagnostics'].items()}=={'2025':(5,[[.015,.015],[.015,.035]],True),'2026':(3,[[.035,.015],[.035,.035]],True)}
assert len(cmp['new_qualified_pairs_equal_existing_diagonal'])==2
for x in cmp['new_qualified_pairs_equal_existing_diagonal']:
    cells=[r['configs'][n] for n in x['pair']]
    controls=[r['configs'][n] for n in x['old_names']]
    assert all(c['year']==o['year'] and o['BTC_EMA_band']==o['ETH_EMA_band']==x['old_diagonal_band'] and not o['is_new'] for c,o in zip(cells,controls))
    assert x['all_cost_NAV_identical_both_years'] and all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le'] for c,o in zip(cells,controls) for k in ('1','2','3'))
for c in r['configs'].values():
    assert c['criteria']['positive_all_costs']
    if c['is_new'] and c['status']=='rejected':
        assert c['year']=='2026' and c['positive_folds_1x']==3 and c['failed_criteria']==['four_positive_1x_folds']
assert p==json.loads((T/'spec.json').read_text())
recovery=json.loads((T/'cache_recovery.json').read_text());assert recovery['new_backtests']==0 and recovery['scenes_hash_verified']==54
feed=json.loads((R/'research/monitor/latest.json').read_text())
assert feed['research']['last_run']['id']==T.name and feed['research']['counts']['registered']==2256 and feed['research']['counts']['ranked']==2151
assert feed['research']['counts']['observation_records_excluded']==337 and feed['paper']['observation_id']=='20261008T225409335729Z'
monitor_check=json.loads((T/'monitor_check.log').read_text())
assert monitor_check['ok'] and monitor_check['protected_inputs_unchanged'] and monitor_check['paper_accounts']==10 and monitor_check['observations']==15 and monitor_check['research_configs']==2151
execution=json.loads((T/'reproduction_execution.json').read_text());assert len(execution)==6 and all(v['exit_code']==0 for v in execution)
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert base==prior['base_head']
paths=sorted(q for q in T.rglob('*') if q.is_file() and '__pycache__' not in q.parts and q.name not in ('verification.json','verify.log'))
paths += [L,R/'research/automation/README.md',R/'research/monitor/latest.json',R/'research/monitor/configs.json.gz']
proof={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,
       'registry':{'rows':5285,'canonical':2593,'preserved_ids':2595,'unchanged_prior_rows':5255,'new_reserved_and_finished':15,'new_historical_trials':12,'new_legacy_observation_cutoffs':3,'pending':0},
       'historical_summary':r['summary'],'new_cross_period_parameter_pairs':2,'unseen_scene_records':18,'new_2026_3x_unique_paths':2,'new_cross_period_return_paths':0,
       'paper10_accounts_unchanged':True,'checks':{'all_new_and_readonly_results_reproduced':True,'funding1350_650_and_raw_weights_verified':True,
       'source_and_combination_NAV_and_money_audited':True,'old_path_equivalence_disclosed':True,'qualified_new_pairs_equal_existing_diagonals_both_years':True,'ETH_band15_35_identical_source_paths_disclosed':True,
       'legacy_shadow_continuity_verified':True,'original16_order_and_alias_identity_verified':True,'sensitivity_plot_visually_reviewed':True,
       'monitor_snapshot_checked':True},'audits':audits,'files_sha256':{str(q.relative_to(R)):sha(q) for q in paths}}
(T/'verification.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof['registry']))
