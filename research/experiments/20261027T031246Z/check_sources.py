"""Check every exported cell, source lineage, budget alias and append-only registry receipt."""
import ast,copy,csv,gzip,io,itertools,json,subprocess
from decimal import Decimal as D
from run import ROOT,R,reg,sha,put,grid_configs,axes,neighbors

def main():
 report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');batch=json.loads((R/'batch.json').read_text());cs=report['configs'];grid=grid_configs(cs);assert len(cs)==108 and len(grid)==162 and len(batch)==108
 refs=[*plan['component_sources'].values(),*plan['read_only_anchor_references'].values(),*plan['read_only_hold_references'].values()];old={};unique={}
 for ref in refs:
  fp=ref['fingerprint'];assert records[fp]['result_available'] and records[fp]['status']==ref['original_status'] and records[fp]['report_sha256']==ref['report_sha256'] and sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['spec'])==ref['spec_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'];assert reg.fingerprint(json.loads((ROOT/ref['spec']).read_text()))==fp;unique[fp]=ref
  if ref['report'] not in old:old[ref['report']]=json.loads((ROOT/ref['report']).read_text())
 assert len(unique)==90;oldby={c['name']:c for doc in old.values() for c in doc['configs'].values()};allby={**oldby,**cs};allcells={**grid,**{c['name']:c for c in cs.values() if c['role']=='benchmark'},**{x['name']:oldby[x['name']] for x in plan['read_only_hold_references'].values()}};assert len(allcells)==171
 for row in batch:
  c=cs[row['name']];sp=json.loads((ROOT/row['spec']).read_text());p=sp['parameters'];assert reg.fingerprint(sp)==row['fingerprint']==c['fingerprint'] and records[c['fingerprint']]['result_available'] is True and records[c['fingerprint']]['status']==c['status'] and records[c['fingerprint']]['report_sha256']==sha(R/'report.json');assert c['capital_usdt']==p['initial_capital_usdt']==20000 and p['start_utc']==plan['time_boundaries']['oos_start_utc'] and p['end_utc']==plan['time_boundaries']['oos_end_exclusive_utc']
  assert p['component_capitals_usdt']==[10000,10000] and p['raw_component_multipliers']==[1,1] and [x['weight'] for x in sp['components']]==[1,1] and [x['fingerprint'] for x in sp['components']]==c['source_fingerprints'];assert p['component_initial_entry_notionals_usdt']==[c['BTC_fixed_entry_notional_usdt'],c['ETH_fixed_entry_notional_usdt']]
  if c['role']=='candidate':
   assert p['BTC_return_hurdle']==.02;assert p['BTC_exit_buffer_fraction']==p['trend_exit_buffer_fraction']==c['trend_exit_buffer_fraction'] in [.005,.02];assert p['trend_filter_lookback_days']==p['ETH_trend_lookback_days']==c['trend_filter_lookback_days'] in [28,31] and p['ETH_lookback_days']==p['reversal_lookback_days']==c['reversal_lookback_days']==3 and p['ETH_return_hurdle']==p['reversal_return_hurdle']==c['reversal_return_hurdle'];ns=neighbors(c,grid);assert c['sensitivity']['neighbor_names']==[x['name'] for x in ns] and c['sensitivity']['dimension_count']==5 and c['sensitivity']['local_3x_neighbor_positive_fraction']==sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)
  else:assert c['status']=='rejected' and c['criteria']=={'reference_only_no_alpha_qualification':False}
 dims=axes(next(iter(grid.values())));assert {tuple(c[p] for p in dims) for c in grid.values()}==set(itertools.product(*dims.values())) and sum(c.get('read_only_anchor',False) for c in grid.values())==54
 def read(n):return list(csv.DictReader((R/n).open()))
 cost,folds,recent,edges,comp=(read(n) for n in ['sensitivity.csv','fold_results.csv','recent40_fold_results.csv','joint_edges.csv','reference_comparisons.csv']);daily=list(csv.DictReader(io.StringIO(gzip.decompress((R/'daily_equity.csv.gz').read_bytes()).decode())));assert [len(x) for x in [cost,folds,recent,daily,edges,comp]]==[513,6669,4104,120204,513,648]
 def eq(text,value):assert (text=='' if value is None else float(text)==value),(text,value)
 for row in cost:
  c=allcells[row['name']];z=c['scenes'][row['cost_multiplier']];assert row['NAV_sha256_f64le']==z['NAV_sha256_f64le'] and float(row['capital_usdt'])==20000 and row['role']==c['role']
  for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt']:eq(row[p],z[p])
  for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:eq(row['recent40_'+p],z['recent40'][p])
 for rows,isrecent in [(folds,False),(recent,True)]:
  for row in rows:
   z=allcells[row['name']]['scenes'][row['cost_multiplier']];z=(z['recent40'] if isrecent else z)['folds'][int(row['fold'])-1]
   for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:eq(row[p],z[p])
 for row in daily:assert row['name'] in cs and float(row['equity_usdt'])==cs[row['name']]['scenes'][row['cost_multiplier']]['daily_equity_usdt'][int(row['boundary_index'])]
 for row in edges:
  a,b=grid[row['from']],grid[row['to']];p=row['axis'];assert dims[p].index(b[p])-dims[p].index(a[p])==1 and all(a[q]==b[q] for q in dims if q!=p)
  for field,key in [('return3_delta_pp','net_return_pct'),('DD3_delta_pp','max_drawdown_pct'),('sharpe3_delta','sharpe_365')]:eq(row[field],b['scenes']['3'][key]-a['scenes']['3'][key] if a['scenes']['3'][key] is not None and b['scenes']['3'][key] is not None else None)
  eq(row['recent40_return3_delta_pp'],b['scenes']['3']['recent40']['net_return_pct']-a['scenes']['3']['recent40']['net_return_pct'])
 for row in comp:
  c=cs[row['name']];y=allby[row['reference_name']];z,a=c['scenes'][row['cost_multiplier']],y['scenes'][row['cost_multiplier']];assert y['fingerprint']==row['reference_fingerprint'] and y['status']==row['reference_original_status'] and a['NAV_sha256_f64le']==row['reference_NAV_sha256'] and z['NAV_sha256_f64le']==row['new_NAV_sha256'];eq(row['return_delta_pp'],z['net_return_pct']-a['net_return_pct']);eq(row['DD_delta_pp'],z['max_drawdown_pct']-a['max_drawdown_pct']);eq(row['recent40_return_delta_pp'],z['recent40']['net_return_pct']-a['recent40']['net_return_pct']);eq(row['execution_count_delta'],z['executions']-a['executions']);eq(row['cost_delta_usdt'],z['cost_usdt']-a['cost_usdt'])
  yp=json.loads((ROOT/y['spec']).read_text())['parameters']
  if row['reference_kind']=='same_budget_constant_long':assert y['role']=='benchmark' and yp['component_initial_entry_notionals_usdt']==[c['BTC_fixed_entry_notional_usdt'],c['ETH_fixed_entry_notional_usdt']]
  else:assert row['reference_kind']=='same_budget_BTCexit1_old' and yp['BTC_return_hurdle']==.02 and yp['BTC_exit_buffer_fraction']==.01 and yp['component_initial_entry_notionals_usdt']==[c['BTC_fixed_entry_notional_usdt'],c['ETH_fixed_entry_notional_usdt']] and json.loads((ROOT/y['spec']).read_text())['components'][1]['fingerprint']==c['source_fingerprints'][1]
 assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items());base=json.loads((R/'startup.json').read_text())['head_after_successful_SSH_fetch'];prefix=subprocess.check_output(['git','show',base+':research/automation/registry.jsonl'],cwd=ROOT);raw=(ROOT/'research/automation/registry.jsonl').read_bytes();assert raw.startswith(prefix);events=[json.loads(x) for x in raw[len(prefix):].splitlines()];fps={x['fingerprint'] for x in batch+json.loads((R/'forward_batch.json').read_text())+json.loads((R/'candidate_batch.json').read_text())};assert len(events)==228 and len(fps)==114 and {x['fingerprint'] for x in events}==fps
 for fp in fps:assert sum(x['fingerprint']==fp and x['status']=='reserved' for x in events)==1 and sum(x['fingerprint']==fp and x['status'] in ['passed','rejected'] for x in events)==1
 for p,h in ctx['ledger_fragments_before'].items():
  if p!='research/automation/registry.jsonl':assert sha(ROOT/p)==h
 for fs in plan['data']['assets'].values():
  for x in fs:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 best=max(grid.values(),key=lambda c:c['scenes']['3']['net_return_pct']);new=[c for c in cs.values() if c['role']=='candidate'];surface={'candidate_cell_count':162,'positive_full_grid_3x_net_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in grid.values())/162,'positive_full_grid_3x_Sharpe_fraction':sum(c['scenes']['3']['sharpe_365'] is not None and c['scenes']['3']['sharpe_365']>0 for c in grid.values())/162,'new_local_positive_fraction_range':[min(c['sensitivity']['local_3x_neighbor_positive_fraction'] for c in new),max(c['sensitivity']['local_3x_neighbor_positive_fraction'] for c in new)],'best_full_grid3_config':best['name'],'best_boundary_axes':[p for p,v in dims.items() if best[p] in [v[0],v[-1]]],'full_Sharpe_cliff_edges':sum(x['full_sharpe_cliff']=='True' for x in edges),'recent_Sharpe_cliff_edges':sum(x['recent40_sharpe_cliff']=='True' for x in edges),'old_qualification_unchanged':True};put(R/'surface_diagnostics.json',surface)
 for name in ['run.py','audit.py']:
  tree=ast.parse((R/name).read_text());assert not any(isinstance(x,ast.Call) and ((isinstance(x.func,ast.Attribute) and x.func.attr in ['simulate','target','trade','funding_amount']) or (isinstance(x.func,ast.Name) and x.func.id in ['simulate','target','trade','funding_amount'])) for x in ast.walk(tree))
 assert sha(R/'report.json')==json.loads((R/'verification.json').read_text())['report_sha256'] and len(json.loads((R/'reserve.json').read_text()))==len(json.loads((R/'finish.json').read_text()))==108
 out={'passed':True,'new_financial_configs':108,'new_candidate_configs':108,'new_benchmark_configs':0,'new_native_backtests':0,'new_passive_parents':108,'readonly_native_components':27,'readonly_old_parent_cells':54,'readonly_matched_holds':9,'readonly_unique_results_unchanged':90,'full5D_parent_cells':162,'cost_rows_verified':513,'fold_rows_verified':6669,'recent40_fold_rows_verified':4104,'daily_NAV_rows_verified':120204,'edges_verified':513,'reference_comparisons_verified':648,'registry_append_only_events':228,'new_finished_IDs':114,'protected_files_unchanged':len(ctx['account_hashes_before']),'old_original_qualification_preserved':True,'source_models_not_rerun':True,'finished_report_original_SHA_preserved':sha(R/'report.json')};put(R/'source_verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
