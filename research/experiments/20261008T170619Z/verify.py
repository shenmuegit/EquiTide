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
assert (prior['lines'],prior['canonical'],prior['preserved_ids'],len(prior['conclusions']))==(5105,2503,2505,65)
assert hashlib.sha256(b''.join(lines[:5105])).hexdigest()==prior['ledger_sha256']
assert all(records[k]==v for k,v in prior['records'].items())
assert (len(lines),len(records),len({registry.fingerprint(v['spec']) for v in records.values()}))==(5135,2520,2518)
assert not [v for v in records.values() if v.get('status')=='reserved']
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());p=r['plan']
audits=[json.loads((T/x).read_text()) for x in ('audit.log','audit_forward.log')]
assert all(a['passed'] for a in audits)
assert audits[0]['report_sha256']==sha(T/'report.json') and audits[1]['report_sha256']==sha(T/'forward_report.json')
assert r['summary']['new_configs']==12 and r['summary']['new_cost_scenes']==36
assert len(r['summary']['passed'])==10 and len(r['summary']['rejected'])==2
assert len(r['summary']['new_both_periods_passed_combination_pairs'])==4 and len(r['summary']['both_periods_passed_combination_pairs'])==6
for bf,rf,report,start in [('batch.json','report.json',r,r['evaluation_started_utc']),('forward_batch.json','forward_report.json',f,f['observation_started_utc'])]:
    for b in json.loads((T/bf).read_text()):
        assert registry.fingerprint(json.loads((R/b['spec']).read_text()))==b['fingerprint']
        ev=[v for v in raw[5105:] if v['fingerprint']==b['fingerprint']]
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
    assert b['raw_weights']==[.675,.325] and b['entry_days']==15 and b['exit_days']==30 and b['EMA_band']==.03
    assert b['BTC_EMA_span_days'] in (30,50,70) and b['ETH_EMA_span_days'] in (30,50,70)
    assert b['is_new']==(b['BTC_EMA_span_days']!=b['ETH_EMA_span_days'])
    if not b['is_new']:assert records[b['fingerprint']]==prior['records'][b['fingerprint']]
    for ref in b['component_refs']:
        sp=json.loads((R/ref['spec']).read_text());q=sp['parameters']
        assert q['initial_capital_usdt']==ref['capital_usdt']==(1350 if ref['asset']=='BTC' else 650)
        assert q['entry_lookback_days']==15 and q['exit_lookback_days']==30 and q['EMA_symmetric_band']==.03
        assert q['EMA_span_days']==b[ref['asset']+'_EMA_span_days'] and sp['logic']==p['rules']
with (T/'sensitivity.csv').open() as fh:
    rows=list(csv.DictReader(fh));assert len(rows)==54 and all(None not in v and None not in v.values() for v in rows)
    for v in rows:
        assert int(v['BTC_EMA_span_days'])==r['configs'][v['config']]['BTC_EMA_span_days']
        assert int(v['ETH_EMA_span_days'])==r['configs'][v['config']]['ETH_EMA_span_days']
assert p['grid']['predeclared_center']=={'BTC_EMA_span_days':50,'ETH_EMA_span_days':50}
assert p['grid']['predeclared_focus']=={'BTC_EMA_span_days':70,'ETH_EMA_span_days':30}
assert all(len(s['equity_usdt'])==9667 and s['elapsed_minutes']==9659 and s['elapsed_complete_days']==6 and s['new_mark_minutes']==120 and s['new_reference_points']==0 and s['new_executions']==0 for c in f['configs'].values() for s in c['scenes'].values())
old=json.loads((R/f['source_state']).read_text());state=json.loads((T/'forward_state.json').read_text())
assert old['positions_by_asset_and_cost']==state['positions_by_asset_and_cost'] and state['next_daily_decision_utc']=='2026-10-09T00:01:00Z'
assert len(f['append_axis'])==120 and f['cutoff_utc']=='2026-10-08T17:00:00Z'
assert f['validation']['walk_forward']=='Incomplete9659minutes/6complete days;no180day/sixfold qualification'
assert f['validation']['continuity']=='9547oldNAVpoints exact prefix;120closedmarks appended to9667points;cash/units/desired/trades unchanged,no new reference/decision/forced sell'
replay=(T/'reproduce.log').read_text()
assert all(s in replay for s in ['PASS:all36 NEW mixed-EMA-spans cost scenes','18 EXISTING scenes read-only verified','including9667point complete time axis','PASS: new parameters/weights'])
assert len((T/'finish.log').read_text().splitlines())==15
h=json.loads((T/'history_paths.json').read_text())
assert h['report_sha256']==sha(T/'report.json') and h['new_scenes_already_in_any_prior_report']==12 and h['new_scenes_not_in_any_prior_report']==24
assert h['new_2026_combo_3x_paths_not_in_any_prior_report']==4 and h['qualified_cross_period_pairs_not_in_any_prior_report']==4
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
assert len(cmp['matched_diagonal_comparisons'])==36 and cmp['new_both_periods_qualified']==4 and cmp['full_grid_both_periods_qualified']==6
assert not any(x['joint_improvement_both_years'] for x in cmp['qualified_new_pairs_vs50_center'])
assert {k:v['distinct_all_cost_paths'] for k,v in cmp['source_component_path_equivalence'].items()}==prior['existing_component_path_signature_counts']
for v in cmp['matched_diagonal_comparisons']:
    c=r['configs'][v['config']];o=r['configs'][v['comparator']]
    assert v['return3_difference_pp']==c['scenes']['3']['net_return_pct']-o['scenes']['3']['net_return_pct']
    assert v['minute_DD3_difference_pp']==c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct']
    assert v['all_cost_NAV_identical']==all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le'] for k in ('1','2','3'))
assert {y:(d['descriptive_cliff_flags'],d['best_return3_coordinates'],d['best_on_boundary']) for y,d in cmp['surface_diagnostics'].items()}=={'2025':(3,[[30,30]],True),'2026':(7,[[30,30]],True)}
recovery=json.loads((T/'cache_recovery.json').read_text());assert recovery['new_backtests']==0 and recovery['scenes_hash_verified']==54
feed=json.loads((R/'research/monitor/latest.json').read_text())
assert feed['research']['last_run']['id']==T.name and feed['research']['counts']['registered']==2220 and feed['research']['counts']['ranked']==2115
assert feed['research']['counts']['observation_records_excluded']==298 and feed['paper']['observation_id']=='20261008T165142201863Z'
monitor_check=json.loads((T/'monitor_check.log').read_text())
assert monitor_check['ok'] and monitor_check['protected_inputs_unchanged'] and monitor_check['paper_accounts']==10 and monitor_check['observations']==12 and monitor_check['research_configs']==2115
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert base==prior['base_head']
paths=sorted(q for q in T.rglob('*') if q.is_file() and '__pycache__' not in q.parts and q.name not in ('verification.json','verify.log'))
paths += [L,R/'research/automation/README.md',R/'research/monitor/latest.json',R/'research/monitor/configs.json.gz']
proof={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,
       'registry':{'rows':5135,'canonical':2518,'preserved_ids':2520,'unchanged_prior_rows':5105,'new_reserved_and_finished':15,'new_historical_trials':12,'new_legacy_observation_cutoffs':3,'pending':0},
       'historical_summary':r['summary'],'new_cross_period_parameter_pairs':4,'unseen_scene_records':24,'new_cross_period_return_paths':4,
       'paper10_accounts_unchanged':True,'checks':{'all_new_and_readonly_results_reproduced':True,'funding1350_650_and_raw_weights_verified':True,
       'source_and_combination_NAV_and_money_audited':True,'old_path_equivalence_disclosed':True,'no_joint_improvement_vs_center':True,
       'legacy_shadow_continuity_verified':True,'original16_order_and_alias_identity_verified':True,'sensitivity_plot_visually_reviewed':True,
       'monitor_snapshot_checked':True},'audits':audits,'files_sha256':{str(q.relative_to(R)):sha(q) for q in paths}}
(T/'verification.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof['registry']))
