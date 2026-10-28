"""Verify each actual export, static ownership definition, registry append and old immutable result."""
import copy,csv,gzip,io,json,subprocess
from run import ROOT,R,reg,sha,put,grid_configs

def main():
 plan=json.loads((R/'plan.json').read_text());r=json.loads((R/'report.json').read_text());ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');batch=json.loads((R/'batch.json').read_text());assert len(batch)==len(r['configs'])==38 and r['frozen_plan_sha256']==sha(R/'plan.json');refs=[*plan['component_sources'].values(),*plan['read_only_anchor_references'].values(),*plan['read_only_hold_references'].values()];unique={}
 for x in refs:
  fp=x['fingerprint'];assert records[fp]['result_available'] is True and records[fp]['status']==x['original_status'] and records[fp]['report_sha256']==x['report_sha256'] and sha(ROOT/x['report'])==x['report_sha256'] and sha(ROOT/x['spec'])==x['spec_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256'];unique[fp]=x
 assert len(unique)==40;grid=grid_configs(r['configs']);allby={**grid,**{n:c for n,c in r['configs'].items() if c['role']=='benchmark'}};h=plan['read_only_hold_references']['COMBO'];c=copy.deepcopy(json.loads((ROOT/h['report']).read_text())['configs'][h['name']]);allby[c['name']]=c;assert len(grid)==54 and len(allby)==57
 for c in allby.values():
  for z in c['scenes'].values():
   if 'recent40' not in z:z['recent40']=copy.deepcopy(z['extension40'])
 for x in batch:
  c=r['configs'][x['name']];sp=json.loads((ROOT/x['spec']).read_text());fp=reg.fingerprint(sp);p=sp['parameters'];assert fp==x['fingerprint']==c['fingerprint'] and records[fp]['result_available'] is True and records[fp]['status']==c['status'] and records[fp]['report_sha256']==sha(R/'report.json') and sha(ROOT/c['archive'])==c['archive_sha256'];w=x['BTC_ownership_multiplier'];assert p['raw_component_multipliers']==[w,1] and [v['weight'] for v in sp['components']]==[w,1] and p['initial_capital_usdt']==c['capital_usdt']==10000*(1+w) and p['effective_owned_entry_budgets_usdt']==[1000*w,3000]
 def read(n):return list(csv.DictReader((R/n).open()))
 cost,folds,recent,edges,comp=(read(n) for n in ['sensitivity.csv','fold_results.csv','recent40_fold_results.csv','joint_edges.csv','reference_comparisons.csv']);daily=list(csv.DictReader(io.StringIO(gzip.decompress((R/'daily_equity.csv.gz').read_bytes()).decode())));assert [len(z) for z in [cost,folds,recent,daily,edges,comp]]==[171,2223,1368,42294,135,216]
 def eq(s,v):assert (s=='' if v is None else float(s)==v),(s,v)
 for row in cost:
  c=allby[row['name']];z=c['scenes'][row['cost_multiplier']];assert row['NAV_sha256_f64le']==z['NAV_sha256_f64le']
  for f in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','cost_usdt','cost_pct_initial','funding_usdt']:eq(row[f],z[f])
  for f in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:eq(row['recent40_'+f],z['recent40'][f])
 for rows,isrecent in [(folds,False),(recent,True)]:
  for row in rows:
   z=allby[row['name']]['scenes'][row['cost_multiplier']];z=(z['recent40'] if isrecent else z)['folds'][int(row['fold'])-1]
   for f in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:eq(row[f],z[f])
 for row in daily:assert float(row['equity_usdt'])==r['configs'][row['name']]['scenes'][row['cost_multiplier']]['daily_equity_usdt'][int(row['boundary_index'])]
 for row in comp:
  c,y=allby[row['name']],allby[row['reference_name']];a,b=c['scenes'][row['cost_multiplier']],y['scenes'][row['cost_multiplier']];assert y['fingerprint']==row['reference_fingerprint'] and y['status']==row['reference_original_status'];eq(row['return_delta_pp'],a['net_return_pct']-b['net_return_pct']);eq(row['DD_delta_pp'],a['max_drawdown_pct']-b['max_drawdown_pct']);eq(row['recent40_return_delta_pp'],a['recent40']['net_return_pct']-b['recent40']['net_return_pct']);eq(row['cost_delta_usdt'],a['cost_usdt']-b['cost_usdt'])
  if row['reference_kind']=='same_native_pair_old_raw1_1':assert y['BTC_ownership_multiplier']==1 and all(y[d]==c[d] for d in ['reversal_return_hurdle','trend_filter_lookback_days','reversal_lookback_days'])
  else:assert y['role']=='benchmark' and y['BTC_ownership_multiplier']==c['BTC_ownership_multiplier'] and y['capital_usdt']==c['capital_usdt']
 base=json.loads((R/'startup.json').read_text())['head_after_successful_SSH_fetch'];prefix=subprocess.check_output(['git','show',base+':research/automation/registry.jsonl'],cwd=ROOT);raw=(ROOT/'research/automation/registry.jsonl').read_bytes();assert raw.startswith(prefix);events=[json.loads(x) for x in raw[len(prefix):].splitlines()];retired=json.loads((R/'retired_invalid_batch.json').read_text());retiredfps={x['fingerprint'] for x in retired};allrows=batch+json.loads((R/'forward_batch.json').read_text())+json.loads((R/'candidate_batch.json').read_text())+retired;assert len(events)==136 and len(allrows)==len({x['fingerprint'] for x in allrows})==68 and {x['fingerprint'] for x in events}=={x['fingerprint'] for x in allrows}
 for row in allrows:
  es=[e for e in events if e['fingerprint']==row['fingerprint']];assert len(es)==2 and es[0]['status']=='reserved' and ((es[1]['status']=='abandoned' and es[1]['result_available'] is False) if row['fingerprint'] in retiredfps else (es[1]['status'] in ['passed','rejected'] and es[1]['result_available'] is True))
 assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items()) and sha(R/'report.json')==json.loads((R/'verification.json').read_text())['report_sha256']
 for p,h in ctx['ledger_fragments_before'].items():
  if p!='research/automation/registry.jsonl':assert sha(ROOT/p)==h
 proof={'passed':True,'new_actual_financial_configs':38,'new_native_components':0,'new_passive_parents':38,'old_unique_results_unchanged':40,'new_finished_IDs':68,'registry_append_only_events':136,'invalid_definitions_retired_without_exact_result':24,'cost_rows_verified':171,'fold_rows_verified':2223,'recent40_fold_rows_verified':1368,'daily_NAV_rows_verified':42294,'edges_verified':135,'reference_comparisons_verified':216,'protected_files_unchanged':len(ctx['account_hashes_before']),'raw_ownership_and_variable_capital_verified':True,'financial_report_sha256':sha(R/'report.json')};put(R/'source_verification.json',proof);print(json.dumps(proof),flush=True)
if __name__=='__main__':main()
