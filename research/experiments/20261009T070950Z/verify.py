"""Verify new guarded components, original matched controls, full history and publication inputs."""
from pathlib import Path
from datetime import datetime,timezone
import csv,gzip,hashlib,json,subprocess,sys,zipfile
T=Path(__file__).resolve().parent;R=T.parents[2]
sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();dt=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));L=R/'research/automation/registry.jsonl';lines=L.read_bytes().splitlines(keepends=True);raw=[json.loads(x) for x in lines];records=registry.read_records(L)
assert (prior['lines'],prior['canonical'],prior['preserved_ids'],len(prior['conclusions']))==(5487,2694,2696,72)
assert hashlib.sha256(b''.join(lines[:5487])).hexdigest()==prior['ledger_sha256'] and all(records[k]==v for k,v in prior['records'].items())
assert (len(lines),len(records),len({registry.fingerprint(v['spec']) for v in records.values()}))==(5537,2721,2719)
assert not [v for v in records.values() if v.get('status')=='reserved']
r=json.loads((T/'report.json').read_text());cr=json.loads((T/'components_report.json').read_text());f=json.loads((T/'forward_report.json').read_text());p=r['plan'];assert p==json.loads((T/'spec.json').read_text())==cr['plan'] and p['preflight_sha256']==sha(T/'preflight.py')
assert p['grid']['predeclared_center']==p['grid']['predeclared_focus']=={'BTC_annual_volatility_ceiling':.5,'ETH_channel_entry_days':15}
assert p['grid']['raw_weights']==[.75,.25] and p['grid']['component_capitals_usdt']==[1500,500]
assert p['reused_component_configs']==8 and p['total_component_configs']==12 and p['total_new_historical_configs']==22 and p['total_new_historical_cost_scenes']==66
au=[json.loads((T/name).read_text()) for name in ('audit_components.log','audit.log','audit_forward.log')];assert all(x['passed'] for x in au)
assert [x['report_sha256'] for x in au]==[sha(T/name) for name in ('components_report.json','report.json','forward_report.json')]
assert (au[0]['actual_scenes_audited'],au[0]['NAV_points_audited'],au[0]['Decimal_volatility_guard_causal_decisions'],au[0]['Decimal_fills_independently_checked'])==(12,3112584,2160,114)
assert (au[1]['source_component_scenes_rebuilt'],au[1]['filtered_ASMA_cost_scenes_audited'],au[1]['filtered_ASMA_NAV_points_audited'])==(36,54,14006628)
assert (r['summary']['new_configs'],r['summary']['new_cost_scenes'],r['summary']['new_component_backtests'],r['summary']['new_component_cost_scenes'])==(18,54,4,12)
assert len(r['summary']['passed'])==13 and len(r['summary']['rejected'])==5 and len(r['summary']['new_both_periods_passed_combination_pairs'])==4 and r['summary']['new_live_orders']==0
assert len(cr['summary']['passed'])==len(cr['summary']['rejected'])==2 and cr['summary']['actual_component_fills']==114 and cr['summary']['real_orders']==0
for bf,rf,doc,start in [('component_batch.json','components_report.json',cr,cr['evaluation_started_utc']),('batch.json','report.json',r,r['evaluation_started_utc']),('forward_batch.json','forward_report.json',f,f['observation_started_utc'])]:
 for b in json.loads((T/bf).read_text()):
  assert registry.fingerprint(json.loads((R/b['spec']).read_text()))==b['fingerprint']
  ev=[x for x in raw[5487:] if x['fingerprint']==b['fingerprint']]
  assert len(ev)==2 and ev[0]['status']=='reserved' and ev[1]['status']==doc['configs'][b['name']]['status'] and ev[1]['result_available'] and ev[1]['report_sha256']==sha(T/rf)
  assert dt(p['frozen_at_utc'])<dt(ev[0]['recorded_at_utc'])<dt(start)<dt(ev[1]['recorded_at_utc'])
for doc in (r,cr,f):
 for path,h in doc['source_hashes'].items():assert sha(R/path)==h,path
for path,h in p['reused_code_sha256'].items():assert sha(R/path)==h,path
batch=json.loads((T/'grid_batch.json').read_text());leaf=json.loads((T/'component_batch.json').read_text());assert len(batch)==18 and all(b['is_new'] for b in batch) and len(leaf)==4
assert {b['fingerprint'] for b in batch}=={x[3] for x in prior['novelty_preflight']['new_grid_coordinates']} and {b['fingerprint'] for b in leaf}=={x[2] for x in prior['novelty_preflight']['new_component_coordinates']}
assert len(r['component_sources'])==12 and sum(ref['is_new_component'] for ref in r['component_sources'].values())==4
for b in batch:
 c=r['configs'][b['name']];assert b['raw_weights']==[.75,.25] and b['BTC_annual_volatility_ceiling'] in (.4,.5,.6) and b['ETH_channel_entry_days'] in (10,15,20)
 sp=json.loads((R/b['spec']).read_text());assert [x['weight'] for x in sp['components']]==[.75,.25]
 assert [x['fingerprint'] for x in sp['components']]==[x['fingerprint'] for x in b['component_refs']]
 for planned,ref in zip(b['component_refs'],c['component_refs']):
  assert all(ref[k]==v for k,v in planned.items() if k not in ('report_sha256','archive_sha256')) and all(r['component_sources'][ref['fingerprint']][k]==v for k,v in ref.items())
  s=json.loads((R/ref['spec']).read_text());q=s['parameters'];asset=ref['asset'];assert q['initial_capital_usdt']==ref['capital_usdt']==(1500 if asset=='BTC' else 500)
  assert registry.fingerprint(s)==ref['fingerprint'] and sha(R/ref['archive'])==ref['archive_sha256'] and sha(R/ref['report'])==ref['report_sha256'] and sha(R/ref['spec'])==r['component_sources'][ref['fingerprint']]['spec_sha256']
  assert s['logic']==p['rules_by_asset'][asset]
  if asset=='BTC':assert q['lookback_days']==65 and q['entry_band_fraction']==.0125 and q['exit_band_fraction']==.005 and q['volatility_lookback_days']==20 and q['annual_volatility_ceiling']==b['BTC_annual_volatility_ceiling']
  else:assert q['entry_lookback_days']==b['ETH_channel_entry_days'] and q['exit_lookback_days']==30
  if ref['is_new_component']:
   child=cr['configs'][ref['name']];assert child['fingerprint']==ref['fingerprint'] and planned['report_sha256'] is planned['archive_sha256'] is None and ref['report_sha256']==sha(T/'components_report.json')
  else:assert records[ref['fingerprint']]==prior['records'][ref['fingerprint']]
for c in cr['configs'].values():
 if not c['is_new']:
  ref=c['source_ref'];old=json.loads((R/ref['report']).read_text())['configs'][c['name']];assert c['scenes']==old['scenes'] and c['status']==old['status']==c['source_record_status'] and c['criteria']==old['criteria']==c['source_record_criteria']
for name,c in r['read_only_comparators'].items():
 old=json.loads((R/c['source_report']).read_text())['configs'][name];assert c['scenes']==old['scenes'] and c['status']==old['status'] and sha(R/c['source_report'])==c['source_report_sha256'] and records[c['fingerprint']]==prior['records'][c['fingerprint']]
 if c['kind']=='MATCHED_UNGUARDED_BTC':
  s=records[c['fingerprint']]['spec'];assert [q['weight'] for q in s['components']]==[.75,.25]
  for component in s['components']:
   q=records[component['fingerprint']]['spec'];params=q['parameters'];asset=q['universe'][0].split('/')[0]
   assert params['initial_capital_usdt']==(1500 if asset=='BTC' else 500)
   if asset=='BTC':assert params['lookback_days']==65 and params['entry_band_fraction']==.0125 and params['exit_band_fraction']==.005 and 'annual_volatility_ceiling' not in params
   else:assert params['entry_lookback_days']==c['ETH_channel_entry_days'] and params['exit_lookback_days']==30
for name,count in [('sensitivity.csv',54),('folds.csv',432)]:
 with (T/name).open() as fh:
  rows=list(csv.DictReader(fh));assert len(rows)==count and all(None not in row and None not in row.values() for row in rows)
  for row in rows:
   if name=='sensitivity.csv':
    c=r['configs'][row['config']];assert float(row['BTC_annual_volatility_ceiling'])==c['BTC_annual_volatility_ceiling'] and int(row['ETH_channel_entry_days'])==c['ETH_channel_entry_days']
   else:
    doc=cr if row['kind']=='BTC_component' else r;c=doc['configs'][row['config']];ff=c['scenes'][row['cost']]['folds'][int(row['fold'])-1];assert float(row['net_return_pct'])==ff['net_return_pct'] and float(row['minute_DD_pct'])==ff['max_drawdown_pct']
assert all(c['criteria']['positive_all_costs'] for c in r['configs'].values()) and all(c['criteria']['positive_all_costs'] for c in cr['configs'].values() if c['is_new'])
cmp=json.loads((T/'comparison.json').read_text());assert cmp['report_sha256']==sha(T/'report.json') and cmp['components_report_sha256']==sha(T/'components_report.json') and len(cmp['matched_comparisons'])==18
assert cmp['new_both_periods_qualified']==4 and cmp['new_qualified_pairs_jointly_improve_matched_controls']==0 and cmp['failure_counts']=={'four_positive_1x_folds':5} and cmp['new_component_failure_counts']=={'four_positive_1x_folds':2}
assert cmp['source_component_path_signature_counts']=={'2025_BTC':3,'2025_ETH':3,'2026_BTC':3,'2026_ETH':3}
for row in cmp['matched_comparisons']:
 c=r['configs'][row['config']];o=r['read_only_comparators'][row['comparator']];assert c['year']==o['year']==row['year'] and c['ETH_channel_entry_days']==o['ETH_channel_entry_days']==row['same_ETH_channel_entry_days'] and row['same_initial_funding']==[1500,500]
 assert row['return_differences_pp']=={k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct'] for k in ('1','2','3')}
 assert row['minute_DD3_difference_pp']==c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct'] and row['all_cost_NAV_identical']==all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le'] for k in ('1','2','3'))
 assert all(d<=0 for d in row['return_differences_pp'].values())
 if c['year']=='2026' and c['BTC_annual_volatility_ceiling']==.6:assert row['all_cost_NAV_identical']
for check in cmp['qualified_pairs_vs_matched_controls']:
 rows=[next(x for x in cmp['matched_comparisons'] if x['config']==name) for name in check['pair']];ret=[v for row in rows for v in row['return_differences_pp'].values()];dd=[row['minute_DD3_difference_pp'] for row in rows]
 assert check['joint_improvement_both_years']==(all(v>=0 for v in ret) and all(v<=0 for v in dd) and (any(v>0 for v in ret) or any(v<0 for v in dd)))
for name,x in cmp['guard_exposure'].items():
 c=cr['configs'][name];arc=json.loads(gzip.decompress((R/c['archive']).read_bytes()));expected={('2025',.4):50,('2025',.5):32,('2025',.6):17,('2026',.4):74,('2026',.5):16,('2026',.6):0}
 for k,z in x['cost_scenes'].items():assert z['daily_decisions']==180 and z['high_volatility_days']==sum(not d['volatility_eligible'] for d in arc['scenes'][k]['decisions'])==expected[c['year'],c['volatility_ceiling']] and z['invested_days']==sum(st['end_day_exclusive']-st['day_offset'] for st in arc['scenes'][k]['position_segments'] if float(st['units'])>0)
assert {y:(z['descriptive_cliff_flags'],z['best_return3_coordinates'],z['best_on_boundary']) for y,z in cmp['surface_diagnostics'].items()}=={'2025':(6,[[.6,20]],True),'2026':(3,[[.6,15]],True)}
assert all(len(z['equity_usdt'])==10508 and z['elapsed_minutes']==10499 and z['elapsed_complete_days']==7 and z['new_mark_minutes']==120 and z['new_reference_points']==0 and z['new_executions']==0 for c in f['configs'].values() for z in c['scenes'].values())
old=json.loads((R/f['source_state']).read_text());state=json.loads((T/'forward_state.json').read_text());assert old['positions_by_asset_and_cost']==state['positions_by_asset_and_cost'] and state['next_daily_decision_utc']==old['next_daily_decision_utc']=='2026-10-10T00:01:00Z'
assert f['cutoff_utc']=='2026-10-09T07:00:00Z' and len(f['append_axis'])==120 and all(z['kind']=='closed_minute_mark' and z['NAV_index']==10388+i for i,z in enumerate(f['append_axis']))
assert au[2]['original_NAV_prefix']==10388 and au[2]['new_daily_decisions']==au[2]['new_reference_points']==au[2]['new_executions']==0
assert sha(R/f['frozen_plan_path'])==f['frozen_plan_sha256']=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
h=json.loads((T/'history_paths.json').read_text());assert h['report_sha256']==sha(T/'report.json') and (h['new_scenes_already_in_any_prior_report'],h['new_scenes_not_in_any_prior_report'],h['new_2026_combo_3x_paths_not_in_any_prior_report'],h['qualified_cross_period_pairs_not_in_any_prior_report'])==(9,45,6,4)
for path,expected in h['all_prior_report_sha256'].items():assert sha(R/path)==expected,path
for c in prior['conclusions']:assert sha(R/c['path'])==c['sha256'] and (R/c['path']).read_text()==c['text']
for collection in ('oos_checks','skills'):
 for path,v in prior[collection].items():assert sha(R/path)==v['sha256'] and (R/path).read_text()==v['text']
for v in prior['freqtrade_results']:
 assert sha(R/v['path'])==v['sha256']
 if v['members']:
  with zipfile.ZipFile(R/v['path']) as z:
   assert z.namelist()==[x['name'] for x in v['members']]
   for x in v['members']:assert hashlib.sha256(z.read(x['name'])).hexdigest()==x['sha256']
assert sha(R/'research/automation/task.md')==prior['read_task_sha256'] and sha(R/'research/monitor/README.md')==prior['read_monitor_README']['sha256']
assert sha(R/'research/paper10/plan.json')==prior['paper10_plan_sha256']=='383cbfe8544627e05ff498ae4f803dbc3ccfd24753311add9cba2f5aa064e34f'
assert sha(R/'research/paper10/state.json')==prior['paper10_state_sha256']=='a1430b09fb44889fada559597b07cde01b54e04c19853519247e0db0ea2e9d9a'
initial=json.loads((T/'prior_evidence_audit.json').read_text());entries=initial['initial16_actual_results_checked'];assert len(entries)==16 and not initial['missing_initial16'] and [v['fingerprint'] for v in entries]==[v['fingerprint'] for v in raw[:16]] and [v['original_ledger_position'] for v in entries]==list(range(1,17))
for v in entries:
 assert v['canonical_fingerprint']==registry.fingerprint(records[v['fingerprint']]['spec'])
 for ev in v['evidence']:assert sha(R/ev['path'])==ev['sha256']
recovery=json.loads((T/'cache_recovery.json').read_text());assert recovery['new_backtests']==0 and recovery['source_components']==8 and recovery['scenes_hash_verified']==24
execution=json.loads((T/'reproduction_execution.json').read_text());assert len(execution)==8 and all(c['exit_code']==0 for c in execution)
assert 'PASS:all54 NEW guarded-BTC/ETH-channel cost scenes exactly reproduced' in (T/'reproduce.log').read_text() and len((T/'finish.log').read_text().splitlines())==25
feed=json.loads((R/'research/monitor/latest.json').read_text());monitor=json.loads((T/'monitor_check.log').read_text())
assert feed['research']['last_run']['id']==T.name and feed['research']['counts']['registered']==2330 and feed['research']['counts']['ranked']==2225 and feed['research']['counts']['observation_records_excluded']==389
assert feed['paper']['observation_id']=='20261009T065510828752Z' and monitor['ok'] and monitor['protected_inputs_unchanged'] and monitor['observations']==19 and monitor['paper_accounts']==10 and monitor['research_configs']==2225
fix=json.loads((T/'monitor_fix_check.json').read_text());assert fix['passed'] and fix['old_ranked_rows_preserved']==2221 and fix['new_actual_component_rows']==4 and fix['paper_state_unchanged'] and fix['existing_rounds_unchanged']
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert base==prior['base_head']=='da350f09c91e3699dbdfd596bc2e780dcc28d5d0'
files=sorted(q for q in T.rglob('*') if q.is_file() and '__pycache__' not in q.parts and q.name not in ('verification.json','verify.log'))+[L,R/'research/automation/README.md',R/'research/monitor/latest.json',R/'research/monitor/configs.json.gz',R/'research/monitor/snapshot.py',R/'checks/monitor_snapshot.py']
proof={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':5537,'canonical':2719,'preserved_ids':2721,'unchanged_prior_rows':5487,'new_reserved_and_finished':25,'new_historical_trials':22,'new_legacy_cutoffs':3,'pending':0},'historical_summary':r['summary'],'new_components_summary':cr['summary'],'new_cross_period_parameter_pairs':4,'new_cross_period_return_paths':4,'new_joint_improvements_over_matched_controls':0,'paper10_accounts_unchanged':True,'checks':{'new_components_causal_guard_and_Decimal_cash_fills_audited':True,'all_new_component_and_portfolio_scenes_reproduced':True,'exact1500_500_funding_and_raw75_25_verified':True,'source_and_combination_full_minute_NAV_money_and_folds_audited':True,'old_components_controls_records_criteria_status_unchanged':True,'planned_source_refs_frozen_before_hash_resolution':True,'all_18_matched_unguarded_controls_nonworse_return':True,'old_60cap_has_zero2026_guard_days_and_matched_NAV':True,'original_legacy_mark_only_state_and_NAV_prefix_verified':True,'original16_order_and_alias_identity_verified':True,'sensitivity_plot_visually_reviewed':True,'monitor_snapshot_checked':True},'audits':au,'files_sha256':{str(q.relative_to(R)):sha(q) for q in files}}
(T/'verification.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof['registry']))
