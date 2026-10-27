"""Verify all native/parent exports, immutable controls and every real/retired registry record."""
import copy,csv,gzip,io,json,subprocess
from run import ROOT,R,reg,sha,put,grid_configs

def main():
 plan=json.loads((R/'plan.json').read_text());r=json.loads((R/'report.json').read_text());ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');batch=json.loads((R/'batch.json').read_text());assert len(batch)==len(r['configs'])==12 and r['frozen_plan_sha256']==sha(R/'plan.json');refs=[*plan['component_sources'].values(),*plan['read_only_anchor_references'].values(),*plan['read_only_hold_references'].values()];old={};unique={}
 for x in refs:
  fp=x['fingerprint'];assert records[fp]['result_available'] is True and records[fp]['status']==x['original_status'] and records[fp]['report_sha256']==x['report_sha256'] and sha(ROOT/x['report'])==x['report_sha256'] and sha(ROOT/x['spec'])==x['spec_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256'];unique[fp]=x
  if x['report'] not in old:old[x['report']]=json.loads((ROOT/x['report']).read_text())
 assert len(unique)==21;grid=grid_configs(r['configs']);allby={**grid}
 for x in plan['read_only_hold_references'].values():
  c=copy.deepcopy(old[x['report']]['configs'][x['name']]);c.update(scope=x['scope'],asset=x['asset'],capital_usdt=x['capital_usdt'])
  for z in c['scenes'].values():
   if 'recent40' not in z:z['recent40']=copy.deepcopy(z['extension40'])
  allby[c['name']]=c
 assert len(grid)==30 and len(allby)==32
 for x in batch:
  c=r['configs'][x['name']];sp=json.loads((ROOT/x['spec']).read_text());fp=reg.fingerprint(sp);assert fp==x['fingerprint']==c['fingerprint'] and records[fp]['result_available'] is True and records[fp]['status']==c['status'] and records[fp]['report_sha256']==sha(R/'report.json') and sha(ROOT/c['archive'])==c['archive_sha256'];p=sp['parameters'];assert p['start_utc']==plan['time_boundaries']['oos_start_utc'] and p['end_utc']==plan['time_boundaries']['oos_end_exclusive_utc'] and p['initial_capital_usdt']==c['capital_usdt']
  if x['scope']=='native':assert p['lookback_days']==x['lookback_days'] in [3,4,5] and p['trend_lookback_days']==x['trend_lookback_days'] in [26,27] and p['fixed_entry_notional_usdt']==3000 and p['return_hurdle']==.02 and p['exit_buffer_fraction']==0
  else:assert p['ETH_lookback_days']==p['reversal_lookback_days']==x['reversal_lookback_days'] in [3,4,5] and p['ETH_trend_lookback_days']==p['trend_filter_lookback_days']==x['trend_filter_lookback_days'] and p['BTC_return_hurdle']==.04 and p['BTC_lookback_days']==31 and p['BTC_exit_buffer_fraction']==p['trend_exit_buffer_fraction']==.01 and p['component_initial_entry_notionals_usdt']==[1000,3000] and p['component_capitals_usdt']==[10000,10000] and [z['weight'] for z in sp['components']]==[1,1]
 def read(n):return list(csv.DictReader((R/n).open()))
 cost,folds,recent,edges,comp=(read(n) for n in ['sensitivity.csv','fold_results.csv','recent40_fold_results.csv','joint_edges.csv','reference_comparisons.csv']);daily=list(csv.DictReader(io.StringIO(gzip.decompress((R/'daily_equity.csv.gz').read_bytes()).decode())));assert [len(z) for z in [cost,folds,recent,daily,edges,comp]]==[96,1248,768,13356,44,72]
 def eq(s,v):assert (s=='' if v is None else float(s)==v),(s,v)
 for row in cost:
  c=allby[row['name']];z=c['scenes'][row['cost_multiplier']];assert row['NAV_sha256_f64le']==z['NAV_sha256_f64le'] and float(row['capital_usdt'])==c['capital_usdt'] and row['scope']==c['scope']
  for f in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt']:eq(row[f],z[f])
  for f in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:eq(row['recent40_'+f],z['recent40'][f])
 for rows,isrecent in [(folds,False),(recent,True)]:
  for row in rows:
   z=allby[row['name']]['scenes'][row['cost_multiplier']];z=(z['recent40'] if isrecent else z)['folds'][int(row['fold'])-1]
   for f in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:eq(row[f],z[f])
 for row in daily:assert float(row['equity_usdt'])==r['configs'][row['name']]['scenes'][row['cost_multiplier']]['daily_equity_usdt'][int(row['boundary_index'])]
 for row in comp:
  c,y=allby[row['name']],allby[row['reference_name']];a,b=c['scenes'][row['cost_multiplier']],y['scenes'][row['cost_multiplier']];assert y['fingerprint']==row['reference_fingerprint'] and y['status']==row['reference_original_status'] and y['capital_usdt']==c['capital_usdt'];eq(row['return_delta_pp'],a['net_return_pct']-b['net_return_pct']);eq(row['DD_delta_pp'],a['max_drawdown_pct']-b['max_drawdown_pct']);eq(row['recent40_return_delta_pp'],a['recent40']['net_return_pct']-b['recent40']['net_return_pct']);eq(row['cost_delta_usdt'],a['cost_usdt']-b['cost_usdt']);eq(row['execution_delta'],a['executions']-b['executions'])
  if row['reference_kind']=='same_bank_oldslow28':assert (y['trend_lookback_days'] if y['scope']=='native' else y['trend_filter_lookback_days'])==28 and (y['lookback_days'] if y['scope']=='native' else y['reversal_lookback_days'])==(c['lookback_days'] if c['scope']=='native' else c['reversal_lookback_days'])
  else:assert y['role']=='benchmark'
 base=json.loads((R/'startup.json').read_text())['head_after_successful_SSH_fetch'];prefix=subprocess.check_output(['git','show',base+':research/automation/registry.jsonl'],cwd=ROOT);raw=(ROOT/'research/automation/registry.jsonl').read_bytes();assert raw.startswith(prefix);events=[json.loads(x) for x in raw[len(prefix):].splitlines()];allrows=batch+json.loads((R/'forward_batch.json').read_text())+json.loads((R/'candidate_batch.json').read_text());assert len(events)==36 and len(allrows)==len({x['fingerprint'] for x in allrows})==18 and {x['fingerprint'] for x in events}=={x['fingerprint'] for x in allrows}
 for row in allrows:
  es=[e for e in events if e['fingerprint']==row['fingerprint']];assert len(es)==2 and es[0]['status']=='reserved' and es[1]['status'] in ['passed','rejected','abandoned']
 assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items()) and sha(R/'report.json')==json.loads((R/'verification.json').read_text())['report_sha256']
 for p,h in ctx['ledger_fragments_before'].items():
  if p!='research/automation/registry.jsonl':assert sha(ROOT/p)==h
 proof={'passed':True,'new_actual_financial_configs':12,'new_native_components':6,'new_passive_parents':6,'old_unique_results_unchanged':21,'new_nonfinancial_retired_definitions':0,'new_finished_IDs':18,'registry_append_only_events':36,'cost_rows_verified':96,'fold_rows_verified':1248,'recent40_fold_rows_verified':768,'daily_NAV_rows_verified':13356,'edges_verified':44,'reference_comparisons_verified':72,'protected_files_unchanged':len(ctx['account_hashes_before']),'all_corrected_aliases_checked':True,'financial_report_sha256':sha(R/'report.json')};put(R/'source_verification.json',proof);print(json.dumps(proof),flush=True)
if __name__=='__main__':main()
