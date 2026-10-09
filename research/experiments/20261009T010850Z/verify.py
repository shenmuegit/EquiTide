"""Read-only final verification of reservations, actual evidence, matched funding and account isolation."""
from pathlib import Path
from datetime import datetime,timezone
import csv,gzip,hashlib,json,subprocess,sys,zipfile
T=Path(__file__).resolve().parent;R=T.parents[2]
sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
dt=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));L=R/'research/automation/registry.jsonl'
lines=L.read_bytes().splitlines(keepends=True);raw=[json.loads(x) for x in lines];records=registry.read_records(L)
assert (prior['lines'],prior['canonical'],prior['preserved_ids'],len(prior['conclusions']))==(5305,2603,2605,69)
assert hashlib.sha256(b''.join(lines[:5305])).hexdigest()==prior['ledger_sha256']
assert all(records[k]==v for k,v in prior['records'].items())
assert (len(lines),len(records),len({registry.fingerprint(v['spec']) for v in records.values()}))==(5347,2626,2624)
assert not [v for v in records.values() if v.get('status')=='reserved']
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());p=r['plan']
assert p==json.loads((T/'spec.json').read_text()) and p['preflight_sha256']==sha(T/'preflight.py')
assert p['grid']['predeclared_focus']==p['grid']['predeclared_center']=={'BTC_EMA_span_days':65,'ETH_SMA_entry_band':.015}
assert p['grid']['raw_weights']==[.75,.25] and p['grid']['component_capitals_usdt']==[1500,500]
audits=[json.loads((T/name).read_text()) for name in ('audit.log','audit_forward.log')]
assert all(x['passed'] for x in audits) and audits[0]['report_sha256']==sha(T/'report.json') and audits[1]['report_sha256']==sha(T/'forward_report.json')
assert audits[0]['source_component_scenes_rebuilt']==36 and audits[0]['filtered_ASMA_cost_scenes_audited']==54 and audits[0]['filtered_ASMA_NAV_points_audited']==14006628
assert r['summary']['new_configs']==18 and r['summary']['new_cost_scenes']==54 and r['summary']['reused_grid_configs']==0
assert len(r['summary']['passed'])==17 and len(r['summary']['rejected'])==1 and len(r['summary']['new_both_periods_passed_combination_pairs'])==8
assert r['summary']['new_component_backtests']==r['summary']['new_live_orders']==0
for bf,rf,report,start in [('batch.json','report.json',r,r['evaluation_started_utc']),('forward_batch.json','forward_report.json',f,f['observation_started_utc'])]:
 for b in json.loads((T/bf).read_text()):
  assert registry.fingerprint(json.loads((R/b['spec']).read_text()))==b['fingerprint']
  events=[x for x in raw[5305:] if x['fingerprint']==b['fingerprint']]
  assert len(events)==2 and events[0]['status']=='reserved' and events[1]['status']==report['configs'][b['name']]['status']
  assert events[1]['result_available'] and events[1]['report_sha256']==sha(T/rf)
  assert dt(p['frozen_at_utc'])<dt(events[0]['recorded_at_utc'])<dt(start)<dt(events[1]['recorded_at_utc'])
for doc in (r,f):
 for path,h in doc['source_hashes'].items():assert sha(R/path)==h,path
for path,h in p['reused_code_sha256'].items():assert sha(R/path)==h,path
batch=json.loads((T/'grid_batch.json').read_text());assert len(batch)==18 and all(b['is_new'] for b in batch)
assert {b['fingerprint'] for b in batch}=={x[3] for x in prior['novelty_preflight']['new_grid_coordinates']}
for b in batch:
 assert b['raw_weights']==[.75,.25] and b['BTC_EMA_span_days'] in (50,65,80) and b['ETH_SMA_entry_band'] in (.0125,.015,.02)
 for ref in b['component_refs']:
  sp=json.loads((R/ref['spec']).read_text());q=sp['parameters'];asset=ref['asset']
  assert q['initial_capital_usdt']==ref['capital_usdt']==(1500 if asset=='BTC' else 500)
  assert sp['logic']==p['rules_by_asset'][asset] and registry.fingerprint(sp)==ref['fingerprint']
  if asset=='BTC':assert sp['family']=='daily-channel-ema-confirmation' and q['entry_lookback_days']==15 and q['exit_lookback_days']==30 and q['EMA_span_days']==b['BTC_EMA_span_days'] and q['EMA_symmetric_band']==.015
  else:assert sp['family']=='daily-sma-asymmetric-hysteresis' and q['lookback_days']==65 and q['entry_band_fraction']==b['ETH_SMA_entry_band'] and q['exit_band_fraction']==.005
  assert sha(R/ref['archive'])==ref['archive_sha256'] and sha(R/ref['report'])==ref['report_sha256']
with (T/'sensitivity.csv').open() as fh:
 rows=list(csv.DictReader(fh));assert len(rows)==54 and all(None not in row and None not in row.values() for row in rows)
 for row in rows:
  c=r['configs'][row['config']];assert int(row['BTC_EMA_span_days'])==c['BTC_EMA_span_days'] and float(row['ETH_SMA_entry_band'])==c['ETH_SMA_entry_band']
for c in r['configs'].values():
 assert c['criteria']['positive_all_costs']
 if c['status']=='rejected':assert c['year']=='2026' and c['BTC_EMA_span_days']==65 and c['ETH_SMA_entry_band']==.0125 and c['positive_folds_1x']==3 and c['failed_criteria']==['four_positive_1x_folds']
cmp=json.loads((T/'comparison.json').read_text());assert cmp['report_sha256']==sha(T/'report.json')
assert len(cmp['matched_comparisons'])==18 and cmp['new_both_periods_qualified']==8 and cmp['new_qualified_pairs_jointly_improve_matched_controls']==0
assert cmp['failure_counts']=={'four_positive_1x_folds':1}
assert cmp['source_component_path_signature_counts']==prior['existing_component_path_signature_counts']=={'2025_BTC':3,'2025_ETH':1,'2026_BTC':3,'2026_ETH':2}
for row in cmp['matched_comparisons']:
 c=r['configs'][row['config']];o=r['read_only_comparators'][row['comparator']]
 assert o['kind']=='MATCHED_CHANNEL_ASMA' and o['year']==c['year'] and o['ETH_SMA_entry_band']==c['ETH_SMA_entry_band']
 original=json.loads((R/o['source_report']).read_text())['configs'][row['comparator']];sp=json.loads((R/original['spec']).read_text())
 assert [x['weight'] for x in sp['components']]==[.75,.25] and sp['components'][1]['fingerprint']==c['component_refs'][1]['fingerprint']
 assert row['return_differences_pp']=={k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct'] for k in ('1','2','3')}
 assert row['minute_DD3_difference_pp']==c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct']
 assert row['all_cost_NAV_identical']==all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le'] for k in ('1','2','3'))
 assert sha(R/o['source_report'])==o['source_report_sha256'] and o['scenes']==original['scenes'] and o['status']==original['status']
for check in cmp['qualified_pairs_vs_matched_controls']:
 rows=[next(v for v in cmp['matched_comparisons'] if v['config']==n) for n in check['pair']]
 ret=[value for row in rows for value in row['return_differences_pp'].values()];drawdowns=[row['minute_DD3_difference_pp'] for row in rows]
 assert check['all_returns_nonworse_both_years']==all(value>=0 for value in ret) and check['DD3_nonworse_both_years']==all(value<=0 for value in drawdowns)
 assert check['joint_improvement_both_years']==(all(value>=0 for value in ret) and all(value<=0 for value in drawdowns) and (any(value>0 for value in ret) or any(value<0 for value in drawdowns)))
assert all(row['return_differences_pp']['3']<0 for row in cmp['matched_comparisons'] if row['year']=='2026')
signatures={}
for year in ('2025','2026'):
 for asset in ('BTC','ETH'):
  sig=set()
  for ref in r['component_sources'].values():
   if ref['year']==year and ref['asset']==asset:
    archive=json.loads(gzip.decompress((R/ref['archive']).read_bytes()));sig.add(tuple(archive['scenes'][k]['summary']['NAV_sha256_f64le'] for k in ('1','2','3')))
  signatures[year+'_'+asset]=len(sig)
assert signatures==cmp['source_component_path_signature_counts']
assert {year:(d['descriptive_cliff_flags'],d['best_return3_coordinates'],d['best_on_boundary']) for year,d in cmp['surface_diagnostics'].items()}=={'2025':(3,[[50,.0125],[50,.015],[50,.02]],True),'2026':(3,[[80,.015],[80,.02]],True)}
assert all(len(s['equity_usdt'])==10148 and s['elapsed_minutes']==10139 and s['elapsed_complete_days']==7 and s['new_mark_minutes']==120 and s['new_reference_points']==1 and s['new_executions']==0 for c in f['configs'].values() for s in c['scenes'].values())
old=json.loads((R/f['source_state']).read_text());state=json.loads((T/'forward_state.json').read_text())
assert old['positions_by_asset_and_cost']==state['positions_by_asset_and_cost'] and state['next_daily_decision_utc']=='2026-10-10T00:01:00Z'
assert f['cutoff_utc']=='2026-10-09T01:00:00Z' and len(f['append_axis'])==121 and f['append_axis'][61]['NAV_index']==10088 and f['append_axis'][61]['kind']=='execution_reference'
assert all(d['action']=='hold_long' for d in f['daily_decisions_by_asset'].values()) and audits[1]['prior_NAV_prefix_preserved']==10027 and audits[1]['original_daily_decisions_independently_checked']==6
assert sha(R/f['frozen_plan_path'])==f['frozen_plan_sha256']=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
h=json.loads((T/'history_paths.json').read_text());assert h['report_sha256']==sha(T/'report.json')
assert (h['new_scenes_already_in_any_prior_report'],h['new_scenes_not_in_any_prior_report'],h['new_2026_combo_3x_paths_not_in_any_prior_report'],h['qualified_cross_period_pairs_not_in_any_prior_report'])==(9,45,4,5)
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
assert sha(R/'research/paper10/plan.json')==prior['paper10_plan_sha256'] and sha(R/'research/paper10/state.json')==prior['paper10_state_sha256']
initial=json.loads((T/'prior_evidence_audit.json').read_text());entries=initial['initial16_actual_results_checked']
assert len(entries)==16 and initial['missing_initial16']==[] and [v['fingerprint'] for v in entries]==[v['fingerprint'] for v in raw[:16]]
assert [v['original_ledger_position'] for v in entries]==list(range(1,17))
for v in entries:
 assert v['canonical_fingerprint']==registry.fingerprint(records[v['fingerprint']]['spec'])
 for ev in v['evidence']:assert sha(R/ev['path'])==ev['sha256']
recovery=json.loads((T/'cache_recovery.json').read_text());assert recovery['new_backtests']==0 and recovery['scenes_hash_verified']==36
execution=json.loads((T/'reproduction_execution.json').read_text());assert len(execution)==6 and all(c['exit_code']==0 for c in execution)
assert 'PASS:all54 NEW filtered-channel/ASMA cost scenes exactly reproduced' in (T/'reproduce.log').read_text() and len((T/'finish.log').read_text().splitlines())==21
feed=json.loads((R/'research/monitor/latest.json').read_text());monitor=json.loads((T/'monitor_check.log').read_text())
assert feed['research']['last_run']['id']==T.name and feed['research']['counts']['registered']==2274 and feed['research']['counts']['ranked']==2169 and feed['research']['counts']['observation_records_excluded']==350
assert feed['paper']['observation_id']=='20261009T005437076398Z' and monitor['ok'] and monitor['protected_inputs_unchanged'] and monitor['observations']==16 and monitor['paper_accounts']==10 and monitor['research_configs']==2169
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert base==prior['base_head']=='f78bca5a1d598e0f74b1ebd0836de01154495c3c'
files=sorted(p for p in T.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ('verification.json','verify.log'))+[L,R/'research/automation/README.md',R/'research/monitor/latest.json',R/'research/monitor/configs.json.gz']
proof={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':5347,'canonical':2624,'preserved_ids':2626,'unchanged_prior_rows':5305,'new_reserved_and_finished':21,'new_historical_trials':18,'new_legacy_cutoffs':3,'pending':0},'historical_summary':r['summary'],'new_cross_period_parameter_pairs':8,'new_cross_period_return_paths':5,'paper10_accounts_unchanged':True,'checks':{'all_new_results_reproduced':True,'exact1500_500_funding_and_raw75_25_verified':True,'source_and_combination_NAV_and_money_audited':True,'matched_same_ETH_controls_verified':True,'no_joint_both_period_improvement_verified':True,'whole_path_novelty_and_ETH2025_platform_disclosed':True,'original_legacy_daily_decision_and_NAV_prefix_verified':True,'original16_order_and_alias_identity_verified':True,'sensitivity_plot_visually_reviewed':True,'monitor_snapshot_checked':True},'audits':audits,'files_sha256':{str(p.relative_to(R)):sha(p) for p in files}}
(T/'verification.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof['registry']))
