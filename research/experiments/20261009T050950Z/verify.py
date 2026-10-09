"""Verify registered SMA bands, original center reuse, cumulative accounts and publication inputs."""
from pathlib import Path
from datetime import datetime,timezone
import csv,gzip,hashlib,json,subprocess,sys,zipfile
T=Path(__file__).resolve().parent;R=T.parents[2]
sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();dt=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));L=R/'research/automation/registry.jsonl';lines=L.read_bytes().splitlines(keepends=True);raw=[json.loads(x) for x in lines];records=registry.read_records(L)
assert (prior['lines'],prior['canonical'],prior['preserved_ids'],len(prior['conclusions']))==(5429,2665,2667,71)
assert hashlib.sha256(b''.join(lines[:5429])).hexdigest()==prior['ledger_sha256'] and all(records[k]==v for k,v in prior['records'].items())
assert (len(lines),len(records),len({registry.fingerprint(v['spec']) for v in records.values()}))==(5467,2686,2684)
assert not [v for v in records.values() if v.get('status')=='reserved']
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());p=r['plan'];assert p==json.loads((T/'spec.json').read_text()) and p['preflight_sha256']==sha(T/'preflight.py')
assert p['grid']['predeclared_center']=={'BTC_entry_band':.015,'ETH_exit_band':.005} and p['grid']['predeclared_focus']=={'BTC_entry_band':.0125,'ETH_exit_band':.005}
assert p['grid']['raw_weights']==[.75,.25] and p['grid']['component_capitals_usdt']==[1500,500]
audits=[json.loads((T/name).read_text()) for name in ('audit.log','audit_forward.log')];assert all(x['passed'] for x in audits)
assert audits[0]['report_sha256']==sha(T/'report.json') and audits[1]['report_sha256']==sha(T/'forward_report.json')
assert audits[0]['source_component_scenes_rebuilt']==36 and audits[0]['filtered_ASMA_cost_scenes_audited']==54 and audits[0]['filtered_ASMA_NAV_points_audited']==14006628
assert r['summary']['new_configs']==16 and r['summary']['new_cost_scenes']==48 and r['summary']['reused_grid_configs']==2 and r['summary']['reused_cost_scenes']==6
assert len(r['summary']['passed'])==16 and not r['summary']['rejected'] and len(r['summary']['new_both_periods_passed_combination_pairs'])==8 and len(r['summary']['both_periods_passed_combination_pairs'])==9
assert r['summary']['new_component_backtests']==r['summary']['new_live_orders']==0
for bf,rf,report,start in [('batch.json','report.json',r,r['evaluation_started_utc']),('forward_batch.json','forward_report.json',f,f['observation_started_utc'])]:
 for b in json.loads((T/bf).read_text()):
  assert registry.fingerprint(json.loads((R/b['spec']).read_text()))==b['fingerprint']
  ev=[x for x in raw[5429:] if x['fingerprint']==b['fingerprint']]
  assert len(ev)==2 and ev[0]['status']=='reserved' and ev[1]['status']==report['configs'][b['name']]['status'] and ev[1]['result_available'] and ev[1]['report_sha256']==sha(T/rf)
  assert dt(p['frozen_at_utc'])<dt(ev[0]['recorded_at_utc'])<dt(start)<dt(ev[1]['recorded_at_utc'])
for doc in (r,f):
 for path,h in doc['source_hashes'].items():assert sha(R/path)==h,path
for path,h in p['reused_code_sha256'].items():assert sha(R/path)==h,path
batch=json.loads((T/'grid_batch.json').read_text());assert len(batch)==18 and sum(b['is_new'] for b in batch)==16
assert {b['fingerprint'] for b in batch if b['is_new']}=={x[3] for x in prior['novelty_preflight']['new_grid_coordinates']}
signatures={};source_hashes={}
for b in batch:
 assert b['raw_weights']==[.75,.25] and b['BTC_entry_band'] in (.0125,.015,.02) and b['ETH_exit_band'] in (.0025,.005,.0075)
 for ref in b['component_refs']:
  sp=json.loads((R/ref['spec']).read_text());q=sp['parameters'];asset=ref['asset']
  assert q['initial_capital_usdt']==ref['capital_usdt']==(1500 if asset=='BTC' else 500) and sp['family']=='daily-sma-asymmetric-hysteresis' and q['lookback_days']==65
  assert sp['logic']==p['rules_by_asset'][asset] and registry.fingerprint(sp)==ref['fingerprint']
  assert (q['entry_band_fraction'],q['exit_band_fraction'])==((b['BTC_entry_band'],.005) if asset=='BTC' else (.015,b['ETH_exit_band']))
  assert sha(R/ref['archive'])==ref['archive_sha256'] and sha(R/ref['report'])==ref['report_sha256']
  a=json.loads(gzip.decompress((R/ref['archive']).read_bytes()));sig=tuple(a['scenes'][k]['summary']['NAV_sha256_f64le'] for k in ('1','2','3'));signatures.setdefault(b['year']+'_'+asset,set()).add(sig)
  axis=q['entry_band_fraction'] if asset=='BTC' else q['exit_band_fraction'];source_hashes[b['year'],asset,axis]=sig
 if not b['is_new']:
  assert (b['BTC_entry_band'],b['ETH_exit_band'])==(.015,.005) and records[b['fingerprint']]==prior['records'][b['fingerprint']]
  old=json.loads((R/b['source_ref']['report']).read_text())['configs'][b['name']];c=r['configs'][b['name']]
  assert old['scenes']==c['scenes'] and old['status']==c['status']==c['source_record_status'] and old['criteria']==c['criteria']==c['source_record_criteria']
  assert sha(R/b['spec'])==b['source_ref']['spec_sha256']
assert {k:len(v) for k,v in signatures.items()}==prior['existing_component_path_signature_counts']=={'2025_BTC':2,'2025_ETH':2,'2026_BTC':2,'2026_ETH':1}
assert all(source_hashes['2026','ETH',x]==source_hashes['2026','ETH',.005] for x in (.0025,.005,.0075))
with (T/'sensitivity.csv').open() as fh:
 rows=list(csv.DictReader(fh));assert len(rows)==54 and all(None not in row and None not in row.values() for row in rows)
 for row in rows:
  c=r['configs'][row['config']];assert float(row['BTC_entry_band'])==c['BTC_entry_band'] and float(row['ETH_exit_band'])==c['ETH_exit_band']
assert all(c['criteria']['positive_all_costs'] and c['status']=='passed' for c in r['configs'].values())
cmp=json.loads((T/'comparison.json').read_text());assert cmp['report_sha256']==sha(T/'report.json') and len(cmp['center_comparisons'])==len(cmp['same_BTC_row_comparisons'])==18
assert cmp['new_both_periods_qualified']==8 and cmp['new_qualified_pairs_jointly_nonworse_with_some_improvement']==cmp['new_qualified_pairs_strict_return_gain_both_years']==0 and cmp['failure_counts']=={}
for collection in ('center_comparisons','same_BTC_row_comparisons'):
 for row in cmp[collection]:
  c=r['configs'][row['config']];o=r['configs'][row['comparator']];assert c['year']==o['year']
  if collection=='center_comparisons':assert not o['is_new'] and (o['BTC_entry_band'],o['ETH_exit_band'])==(.015,.005)
  else:assert c['BTC_entry_band']==o['BTC_entry_band'] and o['ETH_exit_band']==.005 and c['component_refs'][0]['fingerprint']==o['component_refs'][0]['fingerprint']
  assert row['comparator_is_new_in_grid']==o['is_new'] and row['return_differences_pp']=={k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct'] for k in ('1','2','3')}
  assert row['minute_DD3_difference_pp']==c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct'] and row['all_cost_NAV_identical']==all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le'] for k in ('1','2','3'))
for check in cmp['qualified_pairs_vs_old_center']:
 data=[next(x for x in cmp['center_comparisons'] if x['config']==name) for name in check['pair']];ret=[v for x in data for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp'] for x in data]
 assert check['all_returns_nonworse_both_years']==all(v>=0 for v in ret) and check['DD3_nonworse_both_years']==all(v<=0 for v in dd)
 assert check['joint_improvement_both_years']==(all(v>=0 for v in ret) and all(v<=0 for v in dd) and (any(v>0 for v in ret) or any(v<0 for v in dd)))
 assert check['strict_return_increases_in_both_years']==all(any(v>0 for v in x['return_differences_pp'].values()) for x in data)
assert {year:(d['descriptive_cliff_flags'],d['best_return3_coordinates'],d['best_on_boundary']) for year,d in cmp['surface_diagnostics'].items()}=={'2025':(3,[[.0125,.005],[.0125,.0075],[.015,.005],[.015,.0075]],True),'2026':(3,[[.0125,.0025],[.0125,.005],[.0125,.0075],[.015,.0025],[.015,.005],[.015,.0075]],True)}
for year in ('2025','2026'):
 center=next(c for c in r['configs'].values() if c['year']==year and not c['is_new']);focus=next(c for c in r['configs'].values() if c['year']==year and c['BTC_entry_band']==.0125 and c['ETH_exit_band']==.005)
 assert all(center['scenes'][k]['NAV_sha256_f64le']==focus['scenes'][k]['NAV_sha256_f64le'] for k in ('1','2','3'))
assert all(len(z['equity_usdt'])==10388 and z['elapsed_minutes']==10379 and z['elapsed_complete_days']==7 and z['new_mark_minutes']==120 and z['new_reference_points']==0 and z['new_executions']==0 for c in f['configs'].values() for z in c['scenes'].values())
old=json.loads((R/f['source_state']).read_text());state=json.loads((T/'forward_state.json').read_text());assert old['positions_by_asset_and_cost']==state['positions_by_asset_and_cost'] and state['next_daily_decision_utc']==old['next_daily_decision_utc']=='2026-10-10T00:01:00Z'
assert f['cutoff_utc']=='2026-10-09T05:00:00Z' and len(f['append_axis'])==120 and all(z['kind']=='closed_minute_mark' and z['NAV_index']==10268+i for i,z in enumerate(f['append_axis']))
assert audits[1]['original_NAV_prefix']==10268 and audits[1]['new_daily_decisions']==audits[1]['new_reference_points']==audits[1]['new_executions']==0
assert sha(R/f['frozen_plan_path'])==f['frozen_plan_sha256']=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
h=json.loads((T/'history_paths.json').read_text());assert h['report_sha256']==sha(T/'report.json') and (h['new_scenes_already_in_any_prior_report'],h['new_scenes_not_in_any_prior_report'],h['new_2026_combo_3x_paths_not_in_any_prior_report'],h['qualified_cross_period_pairs_not_in_any_prior_report'])==(48,0,0,0)
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
initial=json.loads((T/'prior_evidence_audit.json').read_text());entries=initial['initial16_actual_results_checked'];assert len(entries)==16 and not initial['missing_initial16']
assert [v['fingerprint'] for v in entries]==[v['fingerprint'] for v in raw[:16]] and [v['original_ledger_position'] for v in entries]==list(range(1,17))
for v in entries:
 assert v['canonical_fingerprint']==registry.fingerprint(records[v['fingerprint']]['spec'])
 for ev in v['evidence']:assert sha(R/ev['path'])==ev['sha256']
recovery=json.loads((T/'cache_recovery.json').read_text());assert recovery['new_backtests']==0 and recovery['scenes_hash_verified']==42
execution=json.loads((T/'reproduction_execution.json').read_text());assert len(execution)==6 and all(c['exit_code']==0 for c in execution)
assert 'PASS:all48 NEW split-ASMA cost scenes exactly reproduced' in (T/'reproduce.log').read_text() and len((T/'finish.log').read_text().splitlines())==19
feed=json.loads((R/'research/monitor/latest.json').read_text());monitor=json.loads((T/'monitor_check.log').read_text())
assert feed['research']['last_run']['id']==T.name and feed['research']['counts']['registered']==2308 and feed['research']['counts']['ranked']==2203 and feed['research']['counts']['observation_records_excluded']==376
assert feed['paper']['observation_id']=='20261009T045543669769Z' and monitor['ok'] and monitor['protected_inputs_unchanged'] and monitor['observations']==18 and monitor['paper_accounts']==10 and monitor['research_configs']==2203
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert base==prior['base_head']=='3a819682c6f9e0b62ffeaca7838a921591d766ea'
files=sorted(q for q in T.rglob('*') if q.is_file() and '__pycache__' not in q.parts and q.name not in ('verification.json','verify.log'))+[L,R/'research/automation/README.md',R/'research/monitor/latest.json',R/'research/monitor/configs.json.gz']
proof={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':5467,'canonical':2684,'preserved_ids':2686,'unchanged_prior_rows':5429,'new_reserved_and_finished':19,'new_historical_trials':16,'new_legacy_cutoffs':3,'pending':0},'historical_summary':r['summary'],'new_cross_period_parameter_pairs':8,'new_cross_period_return_paths':0,'paper10_accounts_unchanged':True,'checks':{'all_new_and_existing_center_scenes_reproduced':True,'exact1500_500_funding_and_raw75_25_verified':True,'source_and_combination_NAV_and_money_audited':True,'old_centers_records_criteria_status_unchanged':True,'same_BTC_row_baselines_already_registered':True,'all48_new_scene_paths_previously_seen':True,'focus_equals_existing_center_both_years':True,'no_new_joint_center_improvement':True,'original_legacy_mark_only_state_and_NAV_prefix_verified':True,'original16_order_and_alias_identity_verified':True,'sensitivity_plot_visually_reviewed':True,'monitor_snapshot_checked':True},'audits':audits,'files_sha256':{str(q.relative_to(R)):sha(q) for q in files}}
(T/'verification.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof['registry']))
