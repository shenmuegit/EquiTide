"""Final read-only binding of the frozen BTCvolume+EMA batch and protected accounts."""
from pathlib import Path
from decimal import Decimal as D
from datetime import datetime,timezone
from collections import Counter
import csv,gzip,hashlib,json,subprocess,sys
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text())
sys.path.insert(0,str(R/'research/automation'));import registry
sys.path.insert(0,str(T));from design import definitions
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));r,f,plan=[read(T/n)for n in('report.json','forward_report.json','spec.json')];cmp,h=[read(T/n)for n in('comparison.json','history_paths.json')]
L=R/'research/automation/registry.jsonl';lines=L.read_bytes().splitlines(keepends=True);raw=[json.loads(x)for x in lines];records=registry.read_records(L);canonical=len({registry.fingerprint(v['spec'])for v in records.values()})
assert r['plan']==plan and(prior['lines'],prior['preserved_ids'],prior['canonical'])==(7907,3906,3904)and(len(lines),len(records),canonical)==(7985,3945,3943)
assert hashlib.sha256(b''.join(lines[:prior['lines']])).hexdigest()==prior['ledger_sha256']
for fp,rec in prior['records'].items():assert records[fp]==rec,fp
assert not[v for v in records.values()if v['status']=='reserved']
hist,fb,grid=[read(T/n)for n in('batch.json','forward_batch.json','grid_batch.json')];assert(len(hist),len(fb),len(grid))==(36,3,38)
assert sum(b['role']=='component'for b in hist)==18 and sum(b.get('asset')=='ETH'for b in hist)==18 and not any(b.get('asset')=='BTC'for b in hist)
expected={registry.fingerprint(sp):fields for sp,fields in definitions(registry.fingerprint)};assert set(expected)=={b['fingerprint']for b in grid}
for b in grid:assert all(b[k]==v for k,v in expected[b['fingerprint']].items())
for batch,report,filename in((hist,r,'report.json'),(fb,f,'forward_report.json')):
 for b in batch:
  sp=read(R/b['spec']);fp=registry.fingerprint(sp);assert fp==b['fingerprint']and fp not in prior['records'];events=[x for x in raw[prior['lines']:]if x['fingerprint']==fp]
  assert len(events)==2 and events[0]['status']=='reserved'and events[1]['status']==report['configs'][b['name']]['status']and events[1]['result_available']and events[1]['report_sha256']==sha(T/filename)
  started=report['evaluation_started_utc']if batch is hist else report['observation_started_utc'];assert plan['frozen_at_utc']<=events[0]['recorded_at_utc']<started
assert len((T/'finish.log').read_text().splitlines())==39 and read(T/'preparation_execution.json')['exit_code']==0
fresh=[c for c in r['configs'].values()if c['is_new']];summary=r['summary'];assert(summary['new_configs'],summary['new_component_configs'],summary['new_combination_configs'],summary['new_cost_scenes'],summary['new_minute_NAV_points'])==(36,18,18,108,28013256)
assert summary['positive_1x']==sum(c['scenes']['1']['net_return_pct']>0 for c in fresh) and summary['positive_3x']==sum(c['scenes']['3']['net_return_pct']>0 for c in fresh)
assert set(summary['passed'])=={c['name']for c in fresh if all(c['criteria'].values())}and len(summary['passed'])+len(summary['rejected'])==36
assert set(summary['rejected'])=={c['name']for c in fresh if not all(c['criteria'].values())}
assert cmp['failure_counts']==dict(Counter(k for c in fresh for k in c['failed_criteria']))
for b in hist:
 c,sp=r['configs'][b['name']],read(R/b['spec']);assert all(len(z['folds'])==6 and z['NAV_points']==259382 for z in c['scenes'].values())
 assert c['sensitivity_member']and c['raw_weights']==[.55,.45]and c['BTC_initial_weight']==.55 and c['ETH_EMA_span_days']in(32,34,36) and c['ETH_EMA_entry_band_fraction']in(.01,.0125,.015)and c['ETH_EMA_exit_band_fraction']==.005
 if c['role']=='component':
  p=sp['parameters'];assert c['asset']=='ETH'and sp['family']=='daily-channel-asymmetric-ema-confirmation'and sp['universe']==['ETH/USDT']and c['capital_usdt']==p['initial_capital_usdt']==900
  assert p['entry_lookback_days']==15 and p['exit_lookback_days']==30 and p['EMA_span_days']==c['ETH_EMA_span_days']and p['EMA_entry_band_fraction']==c['ETH_EMA_entry_band_fraction']and p['EMA_exit_band_fraction']==c['ETH_EMA_exit_band_fraction']and'EMA_symmetric_band'not in p and sp['logic']==plan['complete_rules']['ETH']
 else:
  assert sp['family']=='btc-volume-asymmetric-ema-eth-asymmetric-ema-initial-funds'and sp['parameters']['initial_capital_usdt']==c['capital_usdt']==2000 and [x['weight']for x in sp['components']]==[.55,.45]
  children=[records[x['fingerprint']]['spec']for x in sp['components']];assert [x['parameters']['initial_capital_usdt']for x in children]==[1100,900]
  bp,ep=children[0]['parameters'],children[1]['parameters'];assert children[0]['family']=='daily-channel-volume-asymmetric-ema-confirmation'and bp['EMA_span_days']==c['BTC_EMA_span_days']==15 and bp['EMA_entry_band_fraction']==c['BTC_EMA_entry_band_fraction']==.01 and bp['EMA_exit_band_fraction']==c['BTC_EMA_exit_band_fraction']==.03 and bp['volume_lookback_days']==40 and bp['minimum_volume_ratio']==1.1 and children[0]['logic']==plan['complete_rules']['BTC']
  assert children[1]['family']=='daily-channel-asymmetric-ema-confirmation'and ep['EMA_span_days']==c['ETH_EMA_span_days']and ep['EMA_entry_band_fraction']==c['ETH_EMA_entry_band_fraction']and ep['EMA_exit_band_fraction']==c['ETH_EMA_exit_band_fraction']and'EMA_symmetric_band'not in ep and children[1]['logic']==plan['complete_rules']['ETH']
  assert all(x['parameters']['entry_lookback_days']==15 and x['parameters']['exit_lookback_days']==30 for x in children)
  assert sp['components'][0]['fingerprint']in{q['fingerprint']for q in plan['read_only_component_refs']if q['asset']=='BTC'}
 other=r['configs'][c['other_period_config']];assert other['year']!=c['year']
 for key in('role','asset','capital_usdt','raw_weights','BTC_EMA_span_days','BTC_EMA_entry_band_fraction','BTC_EMA_exit_band_fraction','EMA_span_days','EMA_symmetric_band','BTC_volume_lookback_days','BTC_minimum_volume_ratio','ETH_EMA_span_days','ETH_EMA_symmetric_band','ETH_EMA_entry_band_fraction','ETH_EMA_exit_band_fraction'):assert c.get(key)==other.get(key),(c['name'],key)
for mapping in(r['source_hashes'],plan['reused_code_sha256']):
 for p,hsh in mapping.items():assert sha(R/p)==hsh,p
assert sha(T/'preflight.py')==plan['preflight_sha256']and str((T/'volume_ema_signals.py').relative_to(R))in r['source_hashes']
g=plan['grid'];assert g['predeclared_focus']=={'ETH_EMA_span_days':34,'ETH_EMA_entry_band_fraction':.0125,'ETH_EMA_exit_band_fraction':.005}and g['ETH_EMA_span_days']==[32,34,36]and g['ETH_EMA_entry_band_fraction']==[.01,.0125,.015]and g['ETH_EMA_exit_band_fraction']==.005
assert g['raw_weights']==[.55,.45]and g['component_capitals_usdt']==[1100,900]and g['entry_lookback_days']==15 and g['exit_lookback_days']==30 and g['BTC_volume_lookback_days']==40 and g['BTC_minimum_volume_ratio']==1.1 and g['BTC_EMA_span_days']==15 and g['BTC_EMA_entry_band_fraction']==.01 and g['BTC_EMA_exit_band_fraction']==.03
assert len(plan['read_only_component_refs'])==2 and len(plan['read_only_grid_refs'])==0
for ref in plan['read_only_component_refs']+plan['read_only_grid_refs']:
 for field,key in(('spec','spec_sha256'),('report','report_sha256'),('archive','archive_sha256')):assert sha(R/ref[field])==ref[key]
 c,old=r['configs'][ref['name']],read(R/ref['report'])['configs'][ref['name']];assert not c['is_new']and c['scenes']==old['scenes']and c['criteria']==old['criteria']and c['status']==old['status']and records[ref['fingerprint']]==prior['records'][ref['fingerprint']]
 assert c['sensitivity_member']
assert len(plan['read_only_background_refs'])==len(r['read_only_background'])==4
for ref in plan['read_only_background_refs']:
 for field,key in(('spec','spec_sha256'),('report','report_sha256'),('archive','archive_sha256')):assert sha(R/ref[field])==ref[key]
 old,bg=read(R/ref['report'])['configs'][ref['name']],r['read_only_background'][ref['name']];assert bg['status']==old['status']and bg['raw_weights']==old['raw_weights']
 for k,z in bg['scenes'].items():assert all(v==old['scenes'][k][key]for key,v in z.items())
assert r['cash_reference']==plan['cash_reference']and r['cash_reference']['return_pct']==0
ah,af=read(T/'audit.log'),read(T/'audit_forward.log');assert ah['passed']and af['passed']and ah['report_sha256']==sha(T/'report.json')and af['report_sha256']==sha(T/'forward_report.json')
assert(ah['actual_scenes_audited'],ah['NAV_points_audited'],ah['total_causal_decisions'],ah['ETH_pandasEMA_causal_decisions'],ah['BTC_pandasEMA_causal_decisions'],ah['BTC_disjoint_quote_volume_causal_decisions'])==(108,28013256,9720,9720,0,0)
assert ah['Decimal_fills_independently_checked']==summary['new_component_fills'] and summary['new_live_orders']==0 and ah['read_only_component_scenes']==6 and ah['read_only_portfolio_scenes']==0
for name,sens in r['sensitivity'].items():
 year,role=name.split('_');xs=[c for c in r['configs'].values()if c['year']==year and c['sensitivity_member']and c.get('asset','combination')==role];assert len(xs)==sens['cells']==(1 if role=='BTC'else 9)
 assert len(sens['adjacent_edges'])==(0 if role=='BTC'else 12)and sens['axes']==([]if role=='BTC'else['ETH_EMA_span_days','ETH_EMA_entry_band_fraction'])
external={}
for ref in plan['read_only_comparator_refs']:
 for field,key in(('spec','spec_sha256'),('report','report_sha256'),('archive','archive_sha256')):assert sha(R/ref[field])==ref[key]
 old=read(R/ref['report'])['configs'][ref['name']];external[ref['name']]=old;assert r['read_only_comparators'][ref['name']]['scenes']==old['scenes']and records[ref['fingerprint']]==prior['records'][ref['fingerprint']]
assert len(external)==16;lookup={**r['configs'],**external};assert cmp['report_sha256']==h['report_sha256']==sha(T/'report.json')and len(cmp['comparisons'])==72 and len(cmp['qualified_pair_comparisons'])==4*len(summary['new_both_periods_passed_combination_pairs'])
for row in cmp['comparisons']:
 c,o=lookup[row['config']],lookup[row['comparator']];assert c['year']==o['year']and c['capital_usdt']==o['capital_usdt']==row['same_total_capital_usdt']==2000 and not row['comparator_is_new']
 assert row['config_raw_weights']==c['raw_weights']and row['control_raw_weights']==o['raw_weights']
 for stem,x in(('config',c),('control',o)):assert row[stem+'_component_capitals']==[int(D(2000)*D(str(w)))for w in x['raw_weights']]
 if row['kind']=='MATCHED_ETH_CENTER_TIGHT':
  assert c['raw_weights']==o['raw_weights']==[.55,.45]and o['name']in external
  oldspec=records[o['fingerprint']]['spec'];newspec=records[c['fingerprint']]['spec'];assert oldspec['components'][0]==newspec['components'][0]
  oldeth=records[oldspec['components'][1]['fingerprint']]['spec']['parameters'];assert oldeth['EMA_span_days']==35 and oldeth['EMA_entry_band_fraction']==c['ETH_EMA_entry_band_fraction']and oldeth['EMA_exit_band_fraction']==c['ETH_EMA_exit_band_fraction']==.005
 elif row['kind']=='MATCHED_ETH_SLOW_PERIOD':
  assert o['name']in external and c['raw_weights']==o['raw_weights']==[.55,.45]
  oldparent=records[o['fingerprint']]['spec'];newparent=records[c['fingerprint']]['spec'];assert oldparent['components'][0]==newparent['components'][0]
  oldeth=records[oldparent['components'][1]['fingerprint']]['spec']['parameters'];assert oldeth['EMA_span_days']==40 and oldeth['EMA_entry_band_fraction']==c['ETH_EMA_entry_band_fraction']and oldeth['EMA_exit_band_fraction']==.005
 elif row['kind']=='OLD_NO_BTC_EMA':
  assert o['name']in external and o.get('BTC_EMA_span_days')is None and c['raw_weights']==o['raw_weights']==[.55,.45]
  oldparent=records[o['fingerprint']]['spec'];oldbtc=records[oldparent['components'][0]['fingerprint']]['spec'];op=oldbtc['parameters']
  assert 'EMA_span_days'not in op and op['volume_lookback_days']==40 and op['minimum_volume_ratio']==1.1
 else:assert row['kind']=='OLD_N30_HALF'and o['name']in external and o['raw_weights']==[.5,.5]
 assert row['return_differences_pp']=={k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in('1','2','3')}
 assert row['minute_DD3_difference_pp']==c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct']and row['all_cost_NAV_identical']==all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))
for pair in cmp['qualified_pair_comparisons']:
 xs=[next(x for x in cmp['comparisons']if x['config']==n and x['kind']==pair['kind'])for n in pair['pair']];rv=[v for x in xs for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp']for x in xs]
 assert pair['joint_improvement_both_years']==(all(v>=0 for v in rv)and all(v<=0 for v in dd)and(any(v>0 for v in rv)or any(v<0 for v in dd)))and pair['lower_DD3_both_years']==all(v<0 for v in dd)
for kind,key in(('MATCHED_ETH_CENTER_TIGHT','jointly_improved_pairs_vs_matched_eth_period'),('MATCHED_ETH_SLOW_PERIOD','jointly_improved_pairs_vs_slow_period'),('OLD_NO_BTC_EMA','jointly_improved_pairs_vs_old_no_BTC_EMA'),('OLD_N30_HALF','jointly_improved_pairs_vs_old_N30_half')):assert cmp[key]==sum(x['joint_improvement_both_years']for x in cmp['qualified_pair_comparisons']if x['kind']==kind)
assert cmp['lower_DD3_pairs_vs_old_no_BTC_EMA']==sum(x['lower_DD3_both_years']for x in cmp['qualified_pair_comparisons']if x['kind']=='OLD_NO_BTC_EMA')
expected_pairs=[[c['name'],c['other_period_config']]for c in fresh if c['year']=='2025'and c['role']=='combination'and c['both_periods_meet_full_gates']]
assert summary['new_both_periods_passed_combination_pairs']==expected_pairs
old_scene_paths=set();old_paired_paths=set()
for path,hsh in h['all_prior_report_sha256'].items():
 assert sha(R/path)==hsh,path
 oldconfigs=read(R/path).get('configs',{})
 for c in oldconfigs.values():
  old_scene_paths.update(z['NAV_sha256_f64le']for z in c.get('scenes',{}).values()if'NAV_sha256_f64le'in z)
  other=oldconfigs.get(c.get('other_period_config'),{})
  if c.get('year')=='2025'and c.get('role')=='combination'and other:
   try:old_paired_paths.add(tuple(x['scenes'][k]['NAV_sha256_f64le']for x in(c,other)for k in('1','2','3')))
   except KeyError:pass
new_paths=[z['NAV_sha256_f64le']for c in fresh for z in c['scenes'].values()]
new_pairs={tuple(r['configs'][n]['scenes'][k]['NAV_sha256_f64le']for n in pair for k in('1','2','3'))for pair in expected_pairs}
assert h['new_scenes_already_in_any_prior_report']==sum(x in old_scene_paths for x in new_paths)and h['new_scenes_not_in_any_prior_report']==sum(x not in old_scene_paths for x in new_paths)
assert h['distinct_new_scene_paths_not_in_prior']==len(set(new_paths)-old_scene_paths)and h['qualified_cross_period_pairs_not_in_any_prior_report']==len(new_pairs-old_paired_paths)
assert h['new_2026_combo_3x_paths_not_in_any_prior_report']==len({c['scenes']['3']['NAV_sha256_f64le']for c in fresh if c['role']=='combination'and c['year']=='2026'}-old_scene_paths)
for x in h['qualified_pair_histories']:assert x['whole_path_seen_before']==(tuple(r['configs'][n]['scenes'][k]['NAV_sha256_f64le']for n in x['pair']for k in('1','2','3'))in old_paired_paths)
for p,hsh in h['all_prior_report_sha256'].items():assert sha(R/p)==hsh,p
for filename,total,newcount in(('sensitivity.csv',114,108),('folds.csv',684,648)):
 with(T/filename).open()as file:xs=list(csv.DictReader(file))
 assert len(xs)==total and sum(x['is_new']=='True'for x in xs)==newcount
 for row in xs:
  c=r['configs'][row['config']];z=c['scenes'][row['cost']];z=z['folds'][int(row['fold'])-1]if filename=='folds.csv'else z
  for label,key in(('net_return_pct','net_return_pct'),('minute_DD_pct','max_drawdown_pct'),('Sharpe365','sharpe_365'),('Calmar','calmar')):assert row[label]==(''if z[key]is None else str(z[key]))
  for key in('BTC_EMA_span_days','BTC_EMA_entry_band_fraction','BTC_EMA_exit_band_fraction','ETH_EMA_span_days','ETH_EMA_symmetric_band','ETH_EMA_entry_band_fraction','ETH_EMA_exit_band_fraction'):assert row[key]==(''if c[key]is None else str(c[key]))
fr=plan['forward_resume'];assert f['resume_utc']=='2026-10-11T21:00:00Z'and f['cutoff_utc']=='2026-10-11T23:00:00Z'and(fr['prior_NAV_points'],fr['total_NAV_points'],fr['cumulative_minutes'])==(14230,14350,14339)
assert af['new_closed_marks_per_asset']==120 and af['new_daily_decisions']==af['new_reference_points']==af['new_executions']==0 and af['original_cash_units_desired_trades_costs_unchanged']and af['next_daily_decision_utc']=='2026-10-12T00:01:00Z'
assert read(T/'forward_state.json')['positions_by_asset_and_cost']==read(R/fr['source_state'])['positions_by_asset_and_cost']
assert sha(R/f['frozen_plan_path'])==f['frozen_plan_sha256']=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'and read(T/'cache_recovery.json')['scenes_hash_verified']==6
replay,execution,checks=[read(T/n)for n in('reproduction_execution.json','execution_steps.json','final_checks.json')];assert(len(replay),len(execution),len(checks))==(7,6,3)and all(x['exit_code']==0 for x in replay+execution+checks)
assert 'PASS:all108 NEW ETH-asymmetric-band scenes and full report exactly reproduced'in(T/'reproduce.log').read_text()and read(T/'signal_check.log')['synthetic_fixture_checks']=='PASS'
for item in prior['conclusions']:assert sha(R/item['path'])==item['sha256']and(R/item['path']).read_text()==item['text']
for cat in('skills','oos_checks'):
 for p,item in prior[cat].items():assert sha(R/p)==item['sha256']and(R/p).read_text()==item['text']
for item in prior['freqtrade_results']:assert sha(R/item['path'])==item['sha256']
for p,hsh in prior['protected_sha256'].items():assert sha(R/p)==hsh,p
assert sha(R/'research/paper10/plan.json')==prior['paper10_plan_sha256']and sha(R/'research/paper10/state.json')==prior['paper10_state_sha256'];paper=read(R/'research/paper10/state.json');assert paper['observations']==prior['paper_observations']==50 and paper['last_observation_id']==prior['paper_observation']=='20261011T222748990941Z'
marker='## 最近完成的轮次\n\n';assert(R/'research/automation/README.md').read_text()==prior['read_automation_README']['text'].replace(marker,marker+(T/'README_entry.md').read_text()+'\n',1)
assert sha(R/'research/automation/task.md')==prior['read_task_sha256']and sha(R/'research/monitor/README.md')==prior['read_monitor_README']['sha256'];initial=read(T/'prior_evidence_audit.json');assert not initial['missing_initial16']and [x['fingerprint']for x in initial['initial16_actual_results_checked']]==[x['fingerprint']for x in raw[:16]]
feed=read(R/'research/monitor/latest.json');counts=dict(prior['monitor_counts_before'])
for key in('registered','results','ranked'):counts[key]+=36
counts['passed']+=len(summary['passed']);counts['rejected']+=len(summary['rejected']);counts['observation_records_excluded']+=3
assert feed['research']['counts']==counts and feed['research']['last_run']['id']==T.name and feed['paper']['observation_id']==paper['last_observation_id'];monitor=read(T/'monitor_check.log');assert monitor['ok']and monitor['protected_inputs_unchanged']and monitor['observations']==50 and monitor['research_configs']==3049
assert sha(R/'research/monitor/snapshot.py')==prior['protected_sha256']['research/monitor/snapshot.py']
assert subprocess.check_output(['git','show','HEAD:research/monitor/snapshot.py'],cwd=R)==(R/'research/monitor/snapshot.py').read_bytes()
assert sum(x['kind']=='MATCHED_ETH_CENTER_TIGHT'for x in plan['read_only_comparator_refs'])==6 and sum(x['kind']=='MATCHED_ETH_SLOW_PERIOD'for x in plan['read_only_comparator_refs'])==6
plot=read(T/'plot_review.json');assert plot['visually_reviewed']and set(plot['files_sha256'])=={'sensitivity.png','sensitivity_ETH.png'}
for name,hsh in plot['files_sha256'].items():assert sha(T/name)==hsh
recovery=read(T/'execution_recovery.json');attempts=read(T/'execution_attempts.json');failures=recovery['network_failures']
assert recovery['all6_phases_completed']and recovery['network_failures_retained']and recovery['historical_evaluation_runs']==1 and not recovery['financial_code_parameters_or_prior_accounts_changed']
assert len(attempts)==6+len(failures)and len(execution)==6 and all(x['exit_code']==0 for x in execution)
assert len([x for x in attempts if x['command'][1].endswith('/evaluate.py')])==1 and [x for x in attempts if x['exit_code']]==failures
for attempt in failures:assert attempt['command'][1].endswith('/forward.py')and(R/attempt['log']).exists()
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert base==prior['base_head']=='af05103165187588ea0b167c499d5a78a14f663f'
files=sorted(p for p in T.rglob('*')if p.is_file()and '__pycache__'not in p.parts and p.name not in('verification.json','verify.log'))+[L,R/'research/automation/README.md',R/'research/monitor/latest.json',R/'research/monitor/configs.json.gz',R/'research/monitor/snapshot.py']
out={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':len(lines),'canonical':canonical,'preserved_ids':len(records),'unchanged_prior_rows':prior['lines'],'new_reserved_and_finished':39,'new_historical_trials':36,'new_legacy_cutoffs':3,'pending':0},'historical_summary':summary,'new_qualified_cross_period_parameter_pairs':len(expected_pairs),'new_cross_period_return_paths':h['qualified_cross_period_pairs_not_in_any_prior_report'],'jointly_improved_both_period_pairs':cmp['jointly_improved_pairs_vs_matched_eth_period'],'joint_improvements_vs_slow_period':cmp['jointly_improved_pairs_vs_slow_period'],'joint_improvements_vs_no_BTC_EMA':cmp['jointly_improved_pairs_vs_old_no_BTC_EMA'],'both_years_DD3_lower_pairs':cmp['lower_DD3_pairs_vs_old_no_BTC_EMA'],'paper10_accounts_unchanged':True,'monitor_source_unchanged':True,'network_capture_recovery':recovery,'both_sensitivity_plots_visually_reviewed':True,'checks':{'all7_replay_phases_exit_zero':True,'all6_actual_phases_completed_exit_zero':True,'first_forward_capture_exit_zero':not bool(failures),'all3_final_checks_exit_zero':True,'all108new_and6old_cost_scenes_verified':True,'all18_newETH_components_simulated_at_own900_funding':True,'BTC1100_source_reused_without_rescaling':True,'explicit_raw55_45_own1100_900_funds_preserved_no_rebalance':True,'all684folds_114cost_rows_verified':True,'old_results_and_prior_ledger_preserved':True,'initial16_actual_evidence_complete':True,'paper50_plan_state_journals_UI_preserved':True},'audits':[ah,af],'protected_sha256':prior['protected_sha256'],'files_sha256':{str(p.relative_to(R)):sha(p)for p in files}}
(T/'verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':True,**out['registry'],'joint_improvements':out['jointly_improved_both_period_pairs'],'DD3_lower_both_years':out['both_years_DD3_lower_pairs'],'new_qualified_paths':h['qualified_cross_period_pairs_not_in_any_prior_report'],'protected_files':len(prior['protected_sha256']),'files_hashed':len(files)}))
