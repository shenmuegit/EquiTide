"""Independent table attribution, immutable prior results and exact append-only finishes."""
import csv,gzip,io,itertools,json,subprocess
from run import ROOT,R,LOOKS_BY_ASSET,HURDLES,EXITS,NOTIONALS,sha,reg,put,grid_configs,neighbors

def main():
 plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');batch=json.loads((R/'batch.json').read_text());refs=json.loads((R/'anchors.json').read_text());grid=grid_configs(report['configs']);allcs={**grid,**report['configs']};assert len(batch)==42 and len(refs)==0 and len(grid)==36
 assert {(c['asset'],c['fixed_entry_notional_usdt'],c['return_hurdle'],c['exit_buffer_fraction']) for c in grid.values()}==set(itertools.product(['BTC','ETH'],NOTIONALS,HURDLES,EXITS))
 docs={}
 for name,ref in refs.items():
  path=ref['source_report'];assert sha(ROOT/path)==ref['source_report_sha256'] and sha(ROOT/ref['source_spec'])==ref['source_spec_sha256'] and sha(ROOT/ref['source_archive'])==ref['source_archive_sha256']
  if path not in docs:docs[path]=json.loads((ROOT/path).read_text())
  c=docs[path]['configs'][name];rec=records[ref['fingerprint']];assert rec['result_available'] is True and rec['status']==c['status']==ref['original_status'] and rec['report_sha256']==ref['source_report_sha256'];assert report['joint_grid_sensitivity']['cells'][name]['read_only_anchor'] is True and grid[name]['criteria']==c['criteria']
 for row in batch:
  c=report['configs'][row['name']];sp=json.loads((ROOT/row['spec']).read_text());p=sp['parameters'];rec=records[row['fingerprint']];assert reg.fingerprint(sp)==row['fingerprint'];assert p['initial_capital_usdt']==10000 and p['fixed_entry_notional_usdt']==row['fixed_entry_notional_usdt'] in [1000,2000,3000] and p['raw_entry_notional_fraction_of_initial_capital']==row['fixed_entry_notional_usdt']/10000;assert rec['result_available'] is True and rec['report_sha256']==sha(R/'report.json') and rec['status']==c['status']
  if row['role']=='candidate':
   assert p['lookback_days']==LOOKS_BY_ASSET[row['asset']][0] and p['return_hurdle'] in HURDLES and p['exit_buffer_fraction'] in EXITS and p['exit_buffer_fraction']<=p['return_hurdle'];assert p['start_utc']=='2026-09-14T00:01:00Z' and p['end_utc']=='2026-10-24T00:01:00Z' and p['walk_forward_folds']==8 and p['walk_forward_test_days']==5 and p['input_hashes']=={x['path']:x['sha256'] for x in plan['data']['assets'][row['asset']]};ns=neighbors(c,grid);assert c['sensitivity']['neighbor_names']==[x['name'] for x in ns] and c['sensitivity']['local_3x_neighbor_positive_fraction']==sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);assert c['status']=='rejected' and c['criteria']['minimum180days_evidence'] is False
  else:assert p['signal_mode']=='constant_long_reference' and c['status']=='rejected' and c['criteria']=={'reference_only_no_alpha_qualification':False}
 def read(name):return list(csv.DictReader((R/name).open()))
 cost,folds,edges,capacity,hold,comp=(read(x) for x in ['sensitivity.csv','fold_results.csv','joint_edges.csv','cost_capacity.csv','hold_comparison.csv','notional_comparison.csv']);daily=list(csv.DictReader(io.StringIO(gzip.decompress((R/'daily_equity.csv.gz').read_bytes()).decode())));assert [len(x) for x in [cost,folds,daily,edges,capacity,hold,comp]]==[126,1008,5166,66,126,108,108]
 for row in cost:
  c=allcs[row['name']];z=c['scenes'][row['cost_multiplier']];assert row['NAV_sha256_f64le']==z['NAV_sha256_f64le'] and row['read_only_anchor']==str(row['name'] in refs)
  for key in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt']:assert float(row[key])==z[key] if z[key] is not None else row[key]==''
 for row in folds:
  z=allcs[row['name']]['scenes'][row['cost_multiplier']]['folds'][int(row['fold'])-1]
  for key in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:assert float(row[key])==z[key] if z[key] is not None else row[key]==''
 for row in daily:assert float(row['equity_usdt'])==report['configs'][row['name']]['scenes'][row['cost_multiplier']]['daily_equity_usdt'][int(row['boundary_index'])]
 for row in edges:
  a,b=grid[row['from']],grid[row['to']];levels={'fixed_entry_notional_usdt':NOTIONALS,'return_hurdle':HURDLES,'exit_buffer_fraction':EXITS};axis=row['axis'];assert a['asset']==b['asset'] and levels[axis].index(b[axis])-levels[axis].index(a[axis])==1 and all(a[p]==b[p] for p in levels if p!=axis)
  for p,q in [('return3_delta_pp','net_return_pct'),('DD3_delta_pp','max_drawdown_pct'),('sharpe3_delta','sharpe_365')]:assert float(row[p])==b['scenes']['3'][q]-a['scenes']['3'][q] if a['scenes']['3'][q] is not None and b['scenes']['3'][q] is not None else row[p]==''
 for row in comp:
  a,b=grid[row['name']],grid[row['same_period_N2000_name']];assert b['fixed_entry_notional_usdt']==2000 and all(a[p]==b[p] for p in ['asset','lookback_days','return_hurdle','exit_buffer_fraction']);z,y=a['scenes'][row['cost_multiplier']],b['scenes'][row['cost_multiplier']];scale=a['fixed_entry_notional_usdt']/2000
  for p,v in [('return_delta_pp',z['net_return_pct']-y['net_return_pct']),('DD_delta_pp',z['max_drawdown_pct']-y['max_drawdown_pct']),('actual_minus_linear_scaled_return_pp',z['net_return_pct']-scale*y['net_return_pct']),('actual_minus_linear_scaled_execution_cost_usdt',z['cost_usdt']-scale*y['cost_usdt']),('actual_minus_linear_scaled_impact_usdt',z['cost_parts_usdt']['impact']-scale*y['cost_parts_usdt']['impact']),('actual_minus_linear_scaled_funding_usdt',z['funding_usdt']-scale*y['funding_usdt'])]:assert float(row[p])==v
  assert row['new_NAV_sha256']==z['NAV_sha256_f64le'] and row['old_NAV_sha256']==y['NAV_sha256_f64le']
 for row in hold:
  a,h=report['configs'][row['name']],report['configs'][row['matched_hold_name']];assert a['asset']==h['asset'] and a['capital_usdt']==h['capital_usdt']==10000 and a['fixed_entry_notional_usdt']==h['fixed_entry_notional_usdt'];z,y=a['scenes'][row['cost_multiplier']],h['scenes'][row['cost_multiplier']];assert float(row['excess_return_vs_hold_pp'])==z['net_return_pct']-y['net_return_pct']
 for row in capacity:
  assert 0<=float(row['largest_actual_order_participation'])<=.001
  if row['minimum_actual_lagged_ADV_usdt']:assert float(row['conservative_per_order_capacity_from_min_ADV_usdt'])==float(row['minimum_actual_lagged_ADV_usdt'])*.001
  else:assert row['conservative_per_order_capacity_from_min_ADV_usdt']=='' and report['configs'][row['name']]['scenes'][row['cost_multiplier']]['executions']==0
 assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items());base=json.loads((R/'startup.json').read_text())['head_after_successful_SSH_fetch'];prefix=subprocess.check_output(['git','show',base+':research/automation/registry.jsonl'],cwd=ROOT);raw=(ROOT/'research/automation/registry.jsonl').read_bytes();assert raw.startswith(prefix);events=[json.loads(x) for x in raw[len(prefix):].splitlines()];fps={x['fingerprint'] for x in batch+json.loads((R/'forward_batch.json').read_text())};assert len(events)==90 and len(fps)==45 and {x['fingerprint'] for x in events}==fps
 for fp in fps:assert sum(x['fingerprint']==fp and x['status']=='reserved' for x in events)==1 and sum(x['fingerprint']==fp and x['status'] in ['passed','rejected'] for x in events)==1
 for path,h in ctx['ledger_fragments_before'].items():
  if path!='research/automation/registry.jsonl':assert sha(ROOT/path)==h
 for files in plan['data']['assets'].values():
  for x in files:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 assert sha(R/'report.json')==json.loads((R/'verification.json').read_text())['report_sha256'];out={'passed':True,'new_financial_configs':42,'new_candidates':36,'new_benchmarks':6,'readonly_old_results_unchanged':0,'full_joint_grid_configs':36,'cost_rows_verified':126,'fold_rows_verified':1008,'new_daily_NAV_rows_verified':5166,'edges_verified':66,'N2000_comparisons_verified':108,'matched_exposure_hold_comparisons_verified':108,'capacity_rows_verified':126,'append_only_registry_events':90,'new_finished_IDs':45,'protected_files_unchanged':len(ctx['account_hashes_before']),'real_market_files':8,'finished_report_original_SHA_preserved':sha(R/'report.json')};put(R/'source_verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
