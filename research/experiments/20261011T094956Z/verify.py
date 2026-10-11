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
assert r['plan']==plan and(prior['lines'],prior['preserved_ids'],prior['canonical'])==(7253,3579,3577)and(len(lines),len(records),canonical)==(7331,3618,3616)
assert hashlib.sha256(b''.join(lines[:prior['lines']])).hexdigest()==prior['ledger_sha256']
for fp,rec in prior['records'].items():assert records[fp]==rec,fp
assert not[v for v in records.values()if v['status']=='reserved']
hist,fb,grid=[read(T/n)for n in('batch.json','forward_batch.json','grid_batch.json')];assert(len(hist),len(fb),len(grid))==(36,3,42)
assert sum(b['role']=='component'for b in hist)==18 and sum(b.get('asset')=='BTC'for b in hist)==18 and not any(b.get('asset')=='ETH'for b in hist)
expected={registry.fingerprint(sp):fields for sp,fields in definitions(registry.fingerprint)};assert set(expected)=={b['fingerprint']for b in grid}
for b in grid:assert all(b[k]==v for k,v in expected[b['fingerprint']].items())
for batch,report,filename in((hist,r,'report.json'),(fb,f,'forward_report.json')):
 for b in batch:
  sp=read(R/b['spec']);fp=registry.fingerprint(sp);assert fp==b['fingerprint']and fp not in prior['records'];events=[x for x in raw[prior['lines']:]if x['fingerprint']==fp]
  assert len(events)==2 and events[0]['status']=='reserved'and events[1]['status']==report['configs'][b['name']]['status']and events[1]['result_available']and events[1]['report_sha256']==sha(T/filename)
  started=report['evaluation_started_utc']if batch is hist else report['observation_started_utc'];assert plan['frozen_at_utc']<=events[0]['recorded_at_utc']<started
assert len((T/'finish.log').read_text().splitlines())==39 and read(T/'preparation_execution.json')['exit_code']==0
fresh=[c for c in r['configs'].values()if c['is_new']];summary=r['summary'];assert(summary['new_configs'],summary['new_component_configs'],summary['new_combination_configs'],summary['new_cost_scenes'],summary['new_minute_NAV_points'])==(36,18,18,108,28013256)
assert summary['positive_1x']==sum(c['scenes']['1']['net_return_pct']>0 for c in fresh)==36 and summary['positive_3x']==sum(c['scenes']['3']['net_return_pct']>0 for c in fresh)==36
assert set(summary['passed'])=={c['name']for c in fresh if all(c['criteria'].values())}and len(summary['passed'])==21
assert set(summary['rejected'])=={c['name']for c in fresh if not all(c['criteria'].values())}and len(summary['rejected'])==15
assert cmp['failure_counts']==dict(Counter(k for c in fresh for k in c['failed_criteria']))=={'four_positive_1x_folds':15}
for b in hist:
 c,sp=r['configs'][b['name']],read(R/b['spec']);assert all(len(z['folds'])==6 and z['NAV_points']==259382 for z in c['scenes'].values())
 assert c['sensitivity_member']and c['raw_weights']==[.55,.45]and c['BTC_initial_weight']==.55 and c['BTC_EMA_span_days']==20 and c['BTC_EMA_entry_band_fraction']in(.005,.01,.015)and c['BTC_EMA_exit_band_fraction']in(.02,.03,.04)
 if c['role']=='component':
  p=sp['parameters'];assert c['asset']=='BTC'and sp['family']=='daily-channel-volume-asymmetric-ema-confirmation'and sp['universe']==['BTC/USDT']and c['capital_usdt']==p['initial_capital_usdt']==1100
  assert p['entry_lookback_days']==15 and p['exit_lookback_days']==30 and p['volume_lookback_days']==40 and p['minimum_volume_ratio']==1.1
  assert p['EMA_span_days']==c['BTC_EMA_span_days']==20 and p['EMA_entry_band_fraction']==c['BTC_EMA_entry_band_fraction']and p['EMA_exit_band_fraction']==c['BTC_EMA_exit_band_fraction']and sp['logic']==plan['complete_rules']['BTC']
 else:
  assert sp['family']=='btc-volume-asymmetric-ema-eth-ema-initial-funds'and sp['parameters']['initial_capital_usdt']==c['capital_usdt']==2000 and [x['weight']for x in sp['components']]==[.55,.45]
  children=[records[x['fingerprint']]['spec']for x in sp['components']];assert [x['parameters']['initial_capital_usdt']for x in children]==[1100,900]
  assert children[0]['family']=='daily-channel-volume-asymmetric-ema-confirmation'and children[0]['parameters']['EMA_span_days']==c['BTC_EMA_span_days']==20 and children[0]['parameters']['EMA_entry_band_fraction']==c['BTC_EMA_entry_band_fraction']and children[0]['parameters']['EMA_exit_band_fraction']==c['BTC_EMA_exit_band_fraction']
  assert children[1]['family']=='daily-channel-ema-confirmation'and children[1]['parameters']['EMA_span_days']==30 and children[1]['parameters']['EMA_symmetric_band']==.0125
  assert all(x['parameters']['entry_lookback_days']==15 and x['parameters']['exit_lookback_days']==30 for x in children)
  assert sp['components'][1]['fingerprint']in{q['fingerprint']for q in plan['read_only_component_refs']if q['asset']=='ETH'}
 other=r['configs'][c['other_period_config']];assert other['year']!=c['year']
 for key in('role','asset','capital_usdt','raw_weights','BTC_EMA_span_days','BTC_EMA_entry_band_fraction','BTC_EMA_exit_band_fraction','EMA_span_days','EMA_symmetric_band','BTC_volume_lookback_days','BTC_minimum_volume_ratio'):assert c.get(key)==other.get(key),(c['name'],key)
for mapping in(r['source_hashes'],plan['reused_code_sha256']):
 for p,hsh in mapping.items():assert sha(R/p)==hsh,p
assert sha(T/'preflight.py')==plan['preflight_sha256']and str((T/'volume_ema_signals.py').relative_to(R))in r['source_hashes']
g=plan['grid'];assert g['predeclared_focus']=={'BTC_EMA_entry_band_fraction':.005,'BTC_EMA_exit_band_fraction':.03}and g['BTC_EMA_span_days']==20 and g['BTC_EMA_entry_band_fraction']==[.005,.01,.015]and g['BTC_EMA_exit_band_fraction']==[.02,.03,.04]
assert g['raw_weights']==[.55,.45]and g['component_capitals_usdt']==[1100,900]and g['entry_lookback_days']==15 and g['exit_lookback_days']==30 and g['BTC_volume_lookback_days']==40 and g['BTC_minimum_volume_ratio']==1.1
assert len(plan['read_only_component_refs'])==4 and len(plan['read_only_grid_refs'])==2
for ref in plan['read_only_component_refs']+plan['read_only_grid_refs']:
 for field,key in(('spec','spec_sha256'),('report','report_sha256'),('archive','archive_sha256')):assert sha(R/ref[field])==ref[key]
 c,old=r['configs'][ref['name']],read(R/ref['report'])['configs'][ref['name']];assert not c['is_new']and c['scenes']==old['scenes']and c['criteria']==old['criteria']and c['status']==old['status']and records[ref['fingerprint']]==prior['records'][ref['fingerprint']]
 assert c['sensitivity_member']==(c.get('asset')=='ETH')
assert len(plan['read_only_background_refs'])==len(r['read_only_background'])==4
for ref in plan['read_only_background_refs']:
 for field,key in(('spec','spec_sha256'),('report','report_sha256'),('archive','archive_sha256')):assert sha(R/ref[field])==ref[key]
 old,bg=read(R/ref['report'])['configs'][ref['name']],r['read_only_background'][ref['name']];assert bg['status']==old['status']and bg['raw_weights']==old['raw_weights']
 for k,z in bg['scenes'].items():assert all(v==old['scenes'][k][key]for key,v in z.items())
assert r['cash_reference']==plan['cash_reference']and r['cash_reference']['return_pct']==0
ah,af=read(T/'audit.log'),read(T/'audit_forward.log');assert ah['passed']and af['passed']and ah['report_sha256']==sha(T/'report.json')and af['report_sha256']==sha(T/'forward_report.json')
assert(ah['actual_scenes_audited'],ah['NAV_points_audited'],ah['total_causal_decisions'],ah['ETH_pandasEMA_causal_decisions'],ah['BTC_pandasEMA_causal_decisions'],ah['BTC_disjoint_quote_volume_causal_decisions'])==(108,28013256,9720,0,9720,9720)
assert ah['Decimal_fills_independently_checked']==summary['new_component_fills']==324 and summary['new_live_orders']==0 and ah['read_only_component_scenes']==12 and ah['read_only_portfolio_scenes']==6
for name,sens in r['sensitivity'].items():
 year,role=name.split('_');xs=[c for c in r['configs'].values()if c['year']==year and c['sensitivity_member']and c.get('asset','combination')==role];assert len(xs)==sens['cells']==(1 if role=='ETH'else 9)
 assert len(sens['adjacent_edges'])==(0 if role=='ETH'else 12)and sens['axes']==([]if role=='ETH'else['BTC_EMA_entry_band_fraction','BTC_EMA_exit_band_fraction'])
external={}
for ref in plan['read_only_comparator_refs']:
 for field,key in(('spec','spec_sha256'),('report','report_sha256'),('archive','archive_sha256')):assert sha(R/ref[field])==ref[key]
 old=read(R/ref['report'])['configs'][ref['name']];external[ref['name']]=old;assert r['read_only_comparators'][ref['name']]['scenes']==old['scenes']and records[ref['fingerprint']]==prior['records'][ref['fingerprint']]
assert len(external)==8;lookup={**r['configs'],**external};assert cmp['report_sha256']==h['report_sha256']==sha(T/'report.json')and len(cmp['comparisons'])==54 and len(cmp['qualified_pair_comparisons'])==27
for row in cmp['comparisons']:
 c,o=lookup[row['config']],lookup[row['comparator']];assert c['year']==o['year']and c['capital_usdt']==o['capital_usdt']==row['same_total_capital_usdt']==2000 and not row['comparator_is_new']
 assert row['config_raw_weights']==c['raw_weights']and row['control_raw_weights']==o['raw_weights']
 for stem,x in(('config',c),('control',o)):assert row[stem+'_component_capitals']==[int(D(2000)*D(str(w)))for w in x['raw_weights']]
 if row['kind']=='MATCHED_SYMMETRIC':
  assert c['raw_weights']==o['raw_weights']==[.55,.45]and o['name']in external and o['BTC_EMA_span_days']==20 and o['BTC_EMA_symmetric_band']==c['BTC_EMA_entry_band_fraction']
  oldspec=records[o['fingerprint']]['spec'];newspec=records[c['fingerprint']]['spec'];assert oldspec['components'][1]==newspec['components'][1]
 elif row['kind']=='OLD_NO_BTC_EMA':assert not o['is_new']and c['raw_weights']==o['raw_weights']==[.55,.45]and o['BTC_EMA_span_days']is None and o['BTC_EMA_entry_band_fraction']is None and o['BTC_EMA_exit_band_fraction']is None and o['BTC_volume_lookback_days']==40 and o['BTC_minimum_volume_ratio']==1.1
 else:assert row['kind']=='OLD_N30_HALF'and o['name']in external and o['raw_weights']==[.5,.5]
 assert row['return_differences_pp']=={k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in('1','2','3')}
 assert row['minute_DD3_difference_pp']==c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct']and row['all_cost_NAV_identical']==all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))
for pair in cmp['qualified_pair_comparisons']:
 xs=[next(x for x in cmp['comparisons']if x['config']==n and x['kind']==pair['kind'])for n in pair['pair']];rv=[v for x in xs for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp']for x in xs]
 assert pair['joint_improvement_both_years']==(all(v>=0 for v in rv)and all(v<=0 for v in dd)and(any(v>0 for v in rv)or any(v<0 for v in dd)))and pair['lower_DD3_both_years']==all(v<0 for v in dd)
for kind,key in(('MATCHED_SYMMETRIC','jointly_improved_pairs_vs_matched_symmetric'),('OLD_NO_BTC_EMA','jointly_improved_pairs_vs_old_no_BTC_EMA'),('OLD_N30_HALF','jointly_improved_pairs_vs_old_N30_half')):assert cmp[key]==sum(x['joint_improvement_both_years']for x in cmp['qualified_pair_comparisons']if x['kind']==kind)
assert cmp['lower_DD3_pairs_vs_old_no_BTC_EMA']==sum(x['lower_DD3_both_years']for x in cmp['qualified_pair_comparisons']if x['kind']=='OLD_NO_BTC_EMA')
assert len(summary['new_both_periods_passed_combination_pairs'])==9 and h['qualified_cross_period_pairs_not_in_any_prior_report']==1 and h['new_scenes_already_in_any_prior_report']==90 and h['new_scenes_not_in_any_prior_report']==18
for p,hsh in h['all_prior_report_sha256'].items():assert sha(R/p)==hsh,p
for filename,total,newcount in(('sensitivity.csv',126,108),('folds.csv',756,648)):
 with(T/filename).open()as file:xs=list(csv.DictReader(file))
 assert len(xs)==total and sum(x['is_new']=='True'for x in xs)==newcount
 for row in xs:
  c=r['configs'][row['config']];z=c['scenes'][row['cost']];z=z['folds'][int(row['fold'])-1]if filename=='folds.csv'else z
  for label,key in(('net_return_pct','net_return_pct'),('minute_DD_pct','max_drawdown_pct'),('Sharpe365','sharpe_365'),('Calmar','calmar')):assert row[label]==(''if z[key]is None else str(z[key]))
  for key in('BTC_EMA_entry_band_fraction','BTC_EMA_exit_band_fraction'):assert row[key]==(''if c[key]is None else str(c[key]))
fr=plan['forward_resume'];assert f['resume_utc']=='2026-10-11T07:00:00Z'and f['cutoff_utc']=='2026-10-11T09:00:00Z'and(fr['prior_NAV_points'],fr['total_NAV_points'],fr['cumulative_minutes'])==(13390,13510,13499)
assert af['new_closed_marks_per_asset']==120 and af['new_daily_decisions']==af['new_reference_points']==af['new_executions']==0 and af['original_cash_units_desired_trades_costs_unchanged']and af['next_daily_decision_utc']=='2026-10-12T00:01:00Z'
assert read(T/'forward_state.json')['positions_by_asset_and_cost']==read(R/fr['source_state'])['positions_by_asset_and_cost']
assert sha(R/f['frozen_plan_path'])==f['frozen_plan_sha256']=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'and read(T/'cache_recovery.json')['scenes_hash_verified']==18
replay,execution,checks=[read(T/n)for n in('reproduction_execution.json','execution_steps.json','final_checks.json')];assert(len(replay),len(execution),len(checks))==(7,6,3)and all(x['exit_code']==0 for x in replay+execution+checks)
assert 'PASS:all108 NEW asymmetric-BTC-volume-EMA scenes and full report exactly reproduced'in(T/'reproduce.log').read_text()and read(T/'signal_check.log')['synthetic_fixture_checks']=='PASS'
for item in prior['conclusions']:assert sha(R/item['path'])==item['sha256']and(R/item['path']).read_text()==item['text']
for cat in('skills','oos_checks'):
 for p,item in prior[cat].items():assert sha(R/p)==item['sha256']and(R/p).read_text()==item['text']
for item in prior['freqtrade_results']:assert sha(R/item['path'])==item['sha256']
for p,hsh in prior['protected_sha256'].items():assert sha(R/p)==hsh,p
assert sha(R/'research/paper10/plan.json')==prior['paper10_plan_sha256']and sha(R/'research/paper10/state.json')==prior['paper10_state_sha256'];paper=read(R/'research/paper10/state.json');assert paper['observations']==prior['paper_observations']==43 and paper['last_observation_id']==prior['paper_observation']=='20261011T082211892738Z'
marker='## 最近完成的轮次\n\n';assert(R/'research/automation/README.md').read_text()==prior['read_automation_README']['text'].replace(marker,marker+(T/'README_entry.md').read_text()+'\n',1)
assert sha(R/'research/automation/task.md')==prior['read_task_sha256']and sha(R/'research/monitor/README.md')==prior['read_monitor_README']['sha256'];initial=read(T/'prior_evidence_audit.json');assert not initial['missing_initial16']and [x['fingerprint']for x in initial['initial16_actual_results_checked']]==[x['fingerprint']for x in raw[:16]]
feed=read(R/'research/monitor/latest.json');counts=dict(prior['monitor_counts_before'])
for key in('registered','results','ranked'):counts[key]+=36
counts['passed']+=len(summary['passed']);counts['rejected']+=len(summary['rejected']);counts['observation_records_excluded']+=3
assert feed['research']['counts']==counts and feed['research']['last_run']['id']==T.name and feed['paper']['observation_id']==paper['last_observation_id'];monitor=read(T/'monitor_check.log');assert monitor['ok']and monitor['protected_inputs_unchanged']and monitor['observations']==43 and monitor['research_configs']==2813
label=read(T/'monitor_label_checks.json');compat=read(T/'monitor_compatibility.json');assert label['passed']and compat['passed']and label['before_sha256']==sha(T/'monitor_snapshot_before.py')and label['after_sha256']==sha(R/'research/monitor/snapshot.py')
assert compat['all_prior_preserved_ids_labels_unchanged']==3579 and compat['all_new_actual_strategy_labels_verified']==36
assert (R/'research/monitor/snapshot.py').read_text()==(T/'monitor_snapshot_before.py').read_text().replace(label['literal_old_block'],label['literal_new_block'])
assert subprocess.check_output(['git','show','HEAD:research/monitor/snapshot.py'],cwd=R)==(T/'monitor_snapshot_before.py').read_bytes()
assert sum(x['kind']=='MATCHED_SYMMETRIC_BTC_EMA'for x in plan['read_only_comparator_refs'])==6
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert base==prior['base_head']=='022704a8c6526cb0e85b69c372cead10cc175031'
files=sorted(p for p in T.rglob('*')if p.is_file()and '__pycache__'not in p.parts and p.name not in('verification.json','verify.log'))+[L,R/'research/automation/README.md',R/'research/monitor/latest.json',R/'research/monitor/configs.json.gz',R/'research/monitor/snapshot.py']
out={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':len(lines),'canonical':canonical,'preserved_ids':len(records),'unchanged_prior_rows':prior['lines'],'new_reserved_and_finished':39,'new_historical_trials':36,'new_legacy_cutoffs':3,'pending':0},'historical_summary':summary,'new_qualified_cross_period_parameter_pairs':9,'new_cross_period_return_paths':1,'jointly_improved_both_period_pairs':cmp['jointly_improved_pairs_vs_matched_symmetric'],'joint_improvements_vs_no_BTC_EMA':cmp['jointly_improved_pairs_vs_old_no_BTC_EMA'],'both_years_DD3_lower_pairs':cmp['lower_DD3_pairs_vs_old_no_BTC_EMA'],'paper10_accounts_unchanged':True,'intentional_read_only_monitor_label_patch':compat,'both_sensitivity_plots_visually_reviewed':True,'checks':{'all7_replay_phases_exit_zero':True,'all6_actual_phases_first_execution_exit_zero':True,'all3_final_checks_exit_zero':True,'all108new_and18old_cost_scenes_verified':True,'all18_newBTC_components_simulated_at_own1100_funding':True,'ETH900_source_reused_without_rescaling':True,'explicit_raw55_45_own1100_900_funds_preserved_no_rebalance':True,'all756folds_126cost_rows_verified':True,'old_results_and_prior_ledger_preserved':True,'initial16_actual_evidence_complete':True,'paper43_plan_state_journals_UI_preserved':True},'audits':[ah,af],'protected_sha256':prior['protected_sha256'],'files_sha256':{str(p.relative_to(R)):sha(p)for p in files}}
(T/'verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':True,**out['registry'],'joint_improvements':out['jointly_improved_both_period_pairs'],'DD3_lower_both_years':out['both_years_DD3_lower_pairs'],'new_qualified_paths':1,'protected_files':len(prior['protected_sha256']),'files_hashed':len(files)}))
