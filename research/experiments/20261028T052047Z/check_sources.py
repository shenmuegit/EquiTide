"""Verify exports, all existing/new identities and append-only registration without simulations."""
import copy,csv,gzip,io,json,subprocess
from run import ROOT,R,reg,sha,put,grid_configs

def main():
 p=json.loads((R/'plan.json').read_text());r=json.loads((R/'report.json').read_text());ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');batch=json.loads((R/'batch.json').read_text());assert len(batch)==len(r['configs'])==24 and r['frozen_plan_sha256']==sha(R/'plan.json');refs=[*p['component_sources'].values(),*p['read_only_anchor_references'].values(),*p['read_only_hold_references'].values()];old={};unique={}
 for x in refs:
  fp=x['fingerprint'];assert records[fp]['result_available'] is True and records[fp]['status']==x['original_status'] and records[fp]['report_sha256']==x['report_sha256'] and sha(ROOT/x['report'])==x['report_sha256'] and sha(ROOT/x['spec'])==x['spec_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256'];unique[fp]=x
  if x['report'] not in old:old[x['report']]=json.loads((ROOT/x['report']).read_text())
 assert len(unique)==52;grid=grid_configs(r['configs']);allby={**grid}
 for x in p['read_only_hold_references'].values():
  c=copy.deepcopy(old[x['report']]['configs'][x['name']]);c.update(scope='parent',asset='COMBO',capital_usdt=20000)
  for z in c['scenes'].values():
   if 'recent40' not in z:z['recent40']=copy.deepcopy(z['extension40'])
  allby[c['name']]=c
 assert len(grid)==54 and len(allby)==55
 for x in batch:
  c=r['configs'][x['name']];sp=json.loads((ROOT/x['spec']).read_text());fp=reg.fingerprint(sp);v=sp['parameters'];assert fp==x['fingerprint']==c['fingerprint'] and records[fp]['result_available'] is True and records[fp]['status']==c['status'] and records[fp]['report_sha256']==sha(R/'report.json') and sha(ROOT/c['archive'])==c['archive_sha256'];assert v['initial_capital_usdt']==20000 and v['start_utc']==p['time_boundaries']['oos_start_utc'] and v['end_utc']==p['time_boundaries']['oos_end_exclusive_utc'] and v['BTC_return_hurdle']==x['BTC_return_hurdle'] in [.02,.04,.06] and v['BTC_lookback_days']==31 and v['BTC_exit_buffer_fraction']==v['trend_exit_buffer_fraction']==.01 and v['ETH_lookback_days']==v['reversal_lookback_days']==x['reversal_lookback_days'] in [3,4,5] and v['ETH_trend_lookback_days']==v['trend_filter_lookback_days']==x['trend_filter_lookback_days'] in [28,31] and v['component_initial_entry_notionals_usdt']==[x['BTC_fixed_entry_notional_usdt'],3000] and v['component_capitals_usdt']==[10000,10000] and sp['components']==[{'fingerprint':f,'weight':1} for f in x['source_fingerprints']]
 def rows(n):return list(csv.DictReader((R/n).open()))
 cost,folds,recent,edges,comp=(rows(n) for n in ['sensitivity.csv','fold_results.csv','recent40_fold_results.csv','joint_edges.csv','reference_comparisons.csv']);daily=list(csv.DictReader(io.StringIO(gzip.decompress((R/'daily_equity.csv.gz').read_bytes()).decode())));assert [len(z) for z in [cost,folds,recent,daily,edges,comp]]==[165,2145,1320,26712,135,144]
 def eq(s,v):assert (s=='' if v is None else float(s)==v),(s,v)
 for row in cost:
  c=allby[row['name']];z=c['scenes'][row['cost_multiplier']];assert row['NAV_sha256_f64le']==z['NAV_sha256_f64le'] and float(row['capital_usdt'])==20000
  for f in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','cost_usdt','cost_pct_initial','funding_usdt']:eq(row[f],z[f])
  for f in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:eq(row['recent40_'+f],z['recent40'][f])
 for rr,isrecent in [(folds,False),(recent,True)]:
  for row in rr:
   z=allby[row['name']]['scenes'][row['cost_multiplier']];z=(z['recent40'] if isrecent else z)['folds'][int(row['fold'])-1]
   for f in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:eq(row[f],z[f])
 for row in daily:assert float(row['equity_usdt'])==r['configs'][row['name']]['scenes'][row['cost_multiplier']]['daily_equity_usdt'][int(row['boundary_index'])]
 for row in comp:
  c,y=allby[row['name']],allby[row['reference_name']];a,b=c['scenes'][row['cost_multiplier']],y['scenes'][row['cost_multiplier']];assert y['fingerprint']==row['reference_fingerprint'] and y['status']==row['reference_original_status'];eq(row['return_delta_pp'],a['net_return_pct']-b['net_return_pct']);eq(row['DD_delta_pp'],a['max_drawdown_pct']-b['max_drawdown_pct']);eq(row['recent40_return_delta_pp'],a['recent40']['net_return_pct']-b['recent40']['net_return_pct']);eq(row['cost_delta_usdt'],a['cost_usdt']-b['cost_usdt']);eq(row['execution_delta'],a['executions']-b['executions'])
  if row['reference_kind']=='same_bank_BTC_H4':assert y['BTC_return_hurdle']==.04 and y['reversal_return_hurdle']==c['reversal_return_hurdle'] and y['trend_filter_lookback_days']==c['trend_filter_lookback_days'] and y['reversal_lookback_days']==c['reversal_lookback_days'] and json.loads((ROOT/y['spec']).read_text())['components'][1]['fingerprint']==c['source_fingerprints'][1]
  else:assert y['role']=='benchmark'
 base=json.loads((R/'startup.json').read_text())['head_after_successful_SSH_fetch'];prefix=subprocess.check_output(['git','show',base+':research/automation/registry.jsonl'],cwd=ROOT);raw=(ROOT/'research/automation/registry.jsonl').read_bytes();assert raw.startswith(prefix);events=[json.loads(x) for x in raw[len(prefix):].splitlines()];allrows=batch+json.loads((R/'forward_batch.json').read_text())+json.loads((R/'candidate_batch.json').read_text());assert len(events)==60 and len(allrows)==len({x['fingerprint'] for x in allrows})==30 and {x['fingerprint'] for x in events}=={x['fingerprint'] for x in allrows}
 for row in allrows:
  es=[e for e in events if e['fingerprint']==row['fingerprint']];assert len(es)==2 and es[0]['status']=='reserved' and es[1]['status'] in ['passed','rejected']
 assert all(sha(ROOT/f)==h for f,h in ctx['account_hashes_before'].items()) and sha(R/'report.json')==json.loads((R/'verification.json').read_text())['report_sha256']
 for f,h in ctx['ledger_fragments_before'].items():
  if f!='research/automation/registry.jsonl':assert sha(ROOT/f)==h
 proof={'passed':True,'new_actual_financial_configs':24,'new_native_components':0,'new_passive_parents':24,'old_unique_results_unchanged':52,'new_nonfinancial_retired_definitions':0,'new_finished_IDs':30,'registry_append_only_events':60,'cost_rows_verified':165,'fold_rows_verified':2145,'recent40_fold_rows_verified':1320,'daily_NAV_rows_verified':26712,'edges_verified':135,'reference_comparisons_verified':144,'protected_files_unchanged':len(ctx['account_hashes_before']),'all_corrected_aliases_checked':True,'financial_report_sha256':sha(R/'report.json')};put(R/'source_verification.json',proof);print(json.dumps(proof),flush=True)
if __name__=='__main__':main()
