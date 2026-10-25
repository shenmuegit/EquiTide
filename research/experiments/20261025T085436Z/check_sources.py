"""Check immutable sources, complete result tables and append-only finished records."""
import csv,gzip,io,itertools,json,subprocess
from run import ROOT,R,BUFFERS,ALLOCATIONS,sha,reg,put,neighbors
def main():
 plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');batch=json.loads((R/'batch.json').read_text());cs={n:c for n,c in report['configs'].items() if c['role']=='candidate'};assert len(batch)==30 and len(cs)==27 and len(plan['component_sources'])==24
 assert {(c['BTC_fixed_entry_notional_usdt'],c['BTC_exit_buffer_fraction'],c['ETH_exit_buffer_fraction']) for c in cs.values()}==set(itertools.product(ALLOCATIONS,BUFFERS,BUFFERS));assert report['frozen_plan_sha256']==sha(R/'plan.json')
 for fp,ref in plan['component_sources'].items():
  rec=records[fp];assert rec['result_available'] is True and rec['status']==ref['original_status'] and rec['report_sha256']==ref['report_sha256'];assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['spec'])==ref['spec_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'];sp=json.loads((ROOT/ref['spec']).read_text());assert reg.fingerprint(sp)==fp and sp['parameters']['initial_capital_usdt']==10000 and sp['parameters']['fixed_entry_notional_usdt']==ref['fixed_entry_notional_usdt']
 for row in batch:
  c=report['configs'][row['name']];sp=json.loads((ROOT/row['spec']).read_text());p=sp['parameters'];rec=records[row['fingerprint']];assert reg.fingerprint(sp)==row['fingerprint'];assert p['initial_capital_usdt']==20000 and p['raw_component_multipliers']==[1,1] and p['component_capitals_usdt']==[10000,10000] and [x['weight'] for x in sp['components']]==[1,1];nb,ne=row['BTC_fixed_entry_notional_usdt'],row['ETH_fixed_entry_notional_usdt'];assert nb in ALLOCATIONS and ne==4000-nb and p['component_initial_entry_notionals_usdt']==[nb,ne] and p['BTC_fixed_entry_notional_usdt']==nb and p['ETH_fixed_entry_notional_usdt']==ne
  assert p['start_utc']==plan['time_boundaries']['oos_start_utc'] and p['end_utc']==plan['time_boundaries']['oos_end_exclusive_utc'] and p['walk_forward_folds']==13 and p['continuous_oos_days']==370
  for a,n,fp in zip(['BTC','ETH'],[nb,ne],row['source_fingerprints']):
   ref=plan['component_sources'][fp];assert ref['asset']==a and ref['fixed_entry_notional_usdt']==n and ref['role']==row['role'] and ref['return_hurdle']==row[a+'_return_hurdle'] and ref['exit_buffer_fraction']==row[a+'_exit_buffer_fraction']
  assert rec['result_available'] is True and rec['status']==c['status'] and rec['report_sha256']==sha(R/'report.json')
  if row['role']=='candidate':
   assert p['BTC_lookback_days']==31 and p['ETH_lookback_days']==28 and row['BTC_return_hurdle']==.04 and row['ETH_return_hurdle']==.02;ns=neighbors(c,cs);assert c['sensitivity']['neighbor_names']==[x['name'] for x in ns] and c['sensitivity']['three_dimensional_local_3x_positive_fraction']==sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)
  else:assert c['status']=='rejected' and c['criteria']=={'reference_only_no_alpha_qualification':False}
 def read(n):return list(csv.DictReader((R/n).open()))
 cost,folds,recent,edges,holds=(read(n) for n in ['sensitivity.csv','fold_results.csv','recent40_fold_results.csv','joint_edges.csv','hold_comparison.csv']);daily=list(csv.DictReader(io.StringIO(gzip.decompress((R/'daily_equity.csv.gz').read_bytes()).decode())));assert [len(x) for x in [cost,folds,recent,daily,edges,holds]]==[90,1170,720,33390,54,81]
 for row in cost:
  c=report['configs'][row['name']];z=c['scenes'][row['cost_multiplier']];assert row['NAV_sha256_f64le']==z['NAV_sha256_f64le']
  for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt']:assert float(row[p])==z[p] if z[p] is not None else row[p]==''
  for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:assert float(row['recent40_'+p])==z['recent40'][p] if z['recent40'][p] is not None else row['recent40_'+p]==''
 for rows,isrecent in [(folds,False),(recent,True)]:
  for row in rows:
   z=report['configs'][row['name']]['scenes'][row['cost_multiplier']];z=(z['recent40'] if isrecent else z)['folds'][int(row['fold'])-1]
   for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:assert float(row[p])==z[p] if z[p] is not None else row[p]==''
 for row in daily:assert float(row['equity_usdt'])==report['configs'][row['name']]['scenes'][row['cost_multiplier']]['daily_equity_usdt'][int(row['boundary_index'])]
 from summarize import FIELDS,AXES,key
 for row in edges:
  a,b=cs[row['from']],cs[row['to']];i=FIELDS.index(row['axis']);pa,pb=key(a),key(b);assert AXES[i].index(pb[i])-AXES[i].index(pa[i])==1 and all(pa[j]==pb[j] for j in range(3) if j!=i)
  for p,q in [('return3_delta_pp','net_return_pct'),('DD3_delta_pp','max_drawdown_pct'),('sharpe3_delta','sharpe_365')]:assert float(row[p])==b['scenes']['3'][q]-a['scenes']['3'][q]
  assert float(row['recent40_return3_delta_pp'])==b['scenes']['3']['recent40']['net_return_pct']-a['scenes']['3']['recent40']['net_return_pct']
 for row in holds:
  a,h=report['configs'][row['name']],report['configs'][row['matched_hold_name']];assert h['role']=='benchmark' and a['BTC_fixed_entry_notional_usdt']==h['BTC_fixed_entry_notional_usdt'] and a['ETH_fixed_entry_notional_usdt']==h['ETH_fixed_entry_notional_usdt'];z,y=a['scenes'][row['cost_multiplier']],h['scenes'][row['cost_multiplier']];assert float(row['return_advantage_pp'])==z['net_return_pct']-y['net_return_pct']
 assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items());base=json.loads((R/'startup.json').read_text())['head_after_successful_SSH_fetch'];prefix=subprocess.check_output(['git','show',base+':research/automation/registry.jsonl'],cwd=ROOT);raw=(ROOT/'research/automation/registry.jsonl').read_bytes();assert raw.startswith(prefix);events=[json.loads(x) for x in raw[len(prefix):].splitlines()];fps={x['fingerprint'] for x in batch+json.loads((R/'forward_batch.json').read_text())};assert len(events)==66 and len(fps)==33 and {x['fingerprint'] for x in events}==fps
 for fp in fps:assert sum(x['fingerprint']==fp and x['status']=='reserved' for x in events)==1 and sum(x['fingerprint']==fp and x['status'] in ['passed','rejected'] for x in events)==1
 for p,h in ctx['ledger_fragments_before'].items():
  if p!='research/automation/registry.jsonl':assert sha(ROOT/p)==h
 for fs in plan['data']['assets'].values():
  for x in fs:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 assert sha(R/'report.json')==json.loads((R/'verification.json').read_text())['report_sha256'];out={'passed':True,'new_financial_parent_configs':30,'new_candidates':27,'new_benchmarks':3,'source_components_unchanged':24,'source_cost_NAV_hashes':72,'new_component_backtests':0,'full_three_axis_grid':27,'cost_rows_verified':90,'fold_rows_verified':1170,'recent40_fold_rows_verified':720,'daily_NAV_rows_verified':33390,'edges_verified':54,'matched_hold_comparisons_verified':81,'registry_append_only_events':66,'new_finished_IDs':33,'protected_files_unchanged':len(ctx['account_hashes_before']),'real_market_files':8,'finished_report_original_SHA_preserved':sha(R/'report.json')};put(R/'source_verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
