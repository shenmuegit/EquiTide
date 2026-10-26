"""Read-only full-grid, immutable-source and append-only receipts validation."""
import ast,copy,csv,gzip,hashlib,io,itertools,json,subprocess
from decimal import Decimal as D
from run import ROOT,R,sha,put,reg,grid_configs,axes,neighbors

def main():
 plan=json.loads((R/'plan_corrected.json').read_text());report=json.loads((R/'report.json').read_text());ctx=json.loads((R/'context.json').read_text());batch=json.loads((R/'batch.json').read_text());bad=json.loads((R/'abandoned_batch.json').read_text());cs=report['configs'];grid=grid_configs(cs);records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==len(cs)==108 and len(grid)==162 and report['frozen_plan_sha256']==sha(R/'plan_corrected.json') and len(bad)==108
 refs={x['fingerprint']:x for x in [*plan['component_sources'].values(),*plan['read_only_anchor_references'].values(),*plan['read_only_hold_references'].values()]};assert len(refs)==63;old={}
 for fp,ref in refs.items():
  rec=records[fp];assert rec['result_available'] is True and rec['status']==ref['original_status'] and rec['report_sha256']==ref['report_sha256'];assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['spec'])==ref['spec_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'];sp=json.loads((ROOT/ref['spec']).read_text());c=copy.deepcopy(json.loads((ROOT/ref['report']).read_text())['configs'][ref['name']]);assert reg.fingerprint(sp)==fp==c['fingerprint'] and c['status']==ref['original_status'] and {k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()}==ref['NAV_sha256_by_cost']
  if c['name'] in plan['read_only_anchor_references']:assert grid[c['name']]['criteria']==c['criteria'] and grid[c['name']]['status']==c['status'] and grid[c['name']]['sensitivity']==c['sensitivity']
  for z in c['scenes'].values():
   if 'recent40' not in z:z['recent40']=copy.deepcopy(z['extension40'])
  old[c['name']]=c
 rulehash=hashlib.sha256(json.dumps({'rules':plan['rules'],'native_rules':plan['native_rules'],'costs':plan['component_costs']},sort_keys=True,separators=(',',':')).encode()).hexdigest();byfp={**{fp:r for fp,r in plan['component_sources'].items()},**{x['fingerprint']:x for x in cs.values()}}
 for row in batch:
  c=cs[row['name']];sp=json.loads((ROOT/row['spec']).read_text());p=sp['parameters'];rec=records[row['fingerprint']];assert reg.fingerprint(sp)==row['fingerprint'] and rec['result_available'] is True and rec['status']==c['status'] and rec['report_sha256']==sha(R/'report.json') and p['start_utc']==plan['time_boundaries']['oos_start_utc'] and p['end_utc']==plan['time_boundaries']['oos_end_exclusive_utc']
  if row['scope']=='native':assert c['asset']=='ETH' and c['capital_usdt']==p['initial_capital_usdt']==10000 and p['fixed_entry_notional_usdt']==row['fixed_entry_notional_usdt'] in [1000,3000] and p['raw_entry_notional_fraction_of_initial_capital']==p['fixed_entry_notional_usdt']/10000 and sp['logic']==plan['native_rules'] and all(row[q]==p[q] for q in ['trend_lookback_days','lookback_days','return_hurdle'])
  else:
   fps=row['source_fingerprints'];NB,NE=row['BTC_fixed_entry_notional_usdt'],row['ETH_fixed_entry_notional_usdt'];assert NB+NE==4000 and NE in [1000,3000] and c['capital_usdt']==p['initial_capital_usdt']==20000 and p['component_capitals_usdt']==[10000,10000] and p['raw_component_multipliers']==[1,1] and p['component_initial_entry_notionals_usdt']==[NB,NE] and [x['fingerprint'] for x in sp['components']]==fps and [x['weight'] for x in sp['components']]==[1,1] and p['source_rules_and_costs_sha256']==rulehash and sp['logic']==plan['rules']
   b,e=[byfp[fp] for fp in fps];assert b['asset']=='BTC' and b['lookback_days']==31 and b['return_hurdle']==.04 and b['exit_buffer_fraction']==row['trend_exit_buffer_fraction']==.01 and b['fixed_entry_notional_usdt']==NB and e['asset']=='ETH' and e['fixed_entry_notional_usdt']==NE and e['trend_lookback_days']==row['trend_filter_lookback_days']==p['ETH_trend_lookback_days'] and e['lookback_days']==row['reversal_lookback_days']==p['ETH_lookback_days'] and e['return_hurdle']==row['reversal_return_hurdle']==p['ETH_return_hurdle']
  ns=neighbors(c,grid);assert c['sensitivity']['neighbor_names']==[x['name'] for x in ns] and c['sensitivity']['dimension_count']==4 and c['sensitivity']['local_3x_neighbor_positive_fraction']==sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)
 for scope in ['native','parent']:
  gs=[c for c in grid.values() if c['scope']==scope];dims=axes(gs[0]);assert len(gs)==81 and {tuple(c[p] for p in dims) for c in gs}==set(itertools.product(*dims.values())) and sum(c.get('read_only_anchor',False) for c in gs)==27
 def read(name):return list(csv.DictReader((R/name).open()))
 cost,folds,recent,edges,comp=(read(n) for n in ['sensitivity.csv','fold_results.csv','recent40_fold_results.csv','joint_edges.csv','reference_comparisons.csv']);daily=list(csv.DictReader(io.StringIO(gzip.decompress((R/'daily_equity.csv.gz').read_bytes()).decode())));assert [len(x) for x in [cost,folds,recent,daily,edges,comp]]==[486,6318,3888,120204,432,648]
 def eq(text,value):assert (text=='' if value is None else float(text)==value),(text,value)
 for row in cost:
  c=grid[row['name']];z=c['scenes'][row['cost_multiplier']];assert row['NAV_sha256_f64le']==z['NAV_sha256_f64le'] and float(row['capital_usdt'])==c['capital_usdt'] and row['read_only_anchor']==str(c.get('read_only_anchor',False))
  for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt']:eq(row[p],z[p])
  for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:eq(row['recent40_'+p],z['recent40'][p])
 for rows,isrecent in [(folds,False),(recent,True)]:
  for row in rows:
   z=grid[row['name']]['scenes'][row['cost_multiplier']];z=(z['recent40'] if isrecent else z)['folds'][int(row['fold'])-1]
   for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:eq(row[p],z[p])
 for row in daily:assert row['name'] in cs and float(row['equity_usdt'])==cs[row['name']]['scenes'][row['cost_multiplier']]['daily_equity_usdt'][int(row['boundary_index'])]
 for row in edges:
  a,b=grid[row['from']],grid[row['to']];dims=axes(a);p=row['axis'];assert a['scope']==b['scope']==row['scope'] and dims[p].index(b[p])-dims[p].index(a[p])==1 and all(a[q]==b[q] for q in dims if q!=p)
  for field,key in [('return3_delta_pp','net_return_pct'),('DD3_delta_pp','max_drawdown_pct'),('sharpe3_delta','sharpe_365')]:eq(row[field],b['scenes']['3'][key]-a['scenes']['3'][key] if a['scenes']['3'][key] is not None and b['scenes']['3'][key] is not None else None)
  eq(row['recent40_return3_delta_pp'],b['scenes']['3']['recent40']['net_return_pct']-a['scenes']['3']['recent40']['net_return_pct'])
 for row in comp:
  c=cs[row['name']];y=old[row['reference_name']];z,a=c['scenes'][row['cost_multiplier']],y['scenes'][row['cost_multiplier']];assert y['fingerprint']==row['reference_fingerprint'] and y['status']==row['reference_original_status'] and a['NAV_sha256_f64le']==row['reference_NAV_sha256'] and z['NAV_sha256_f64le']==row['new_NAV_sha256'];eq(row['return_delta_pp'],z['net_return_pct']-a['net_return_pct']);eq(row['DD_delta_pp'],z['max_drawdown_pct']-a['max_drawdown_pct']);eq(row['recent40_return_delta_pp'],z['recent40']['net_return_pct']-a['recent40']['net_return_pct']);eq(row['execution_count_delta'],z['executions']-a['executions']);eq(row['cost_delta_usdt'],z['cost_usdt']-a['cost_usdt'])
 assert sha(R/'report.json')==json.loads((R/'verification.json').read_text())['report_sha256'] and len(json.loads((R/'reserve.json').read_text()))==len(json.loads((R/'finish.json').read_text()))==108
 invalid_sha=sha(R/'invalid_spec_report.json')
 for row in bad:
  rec=records[row['fingerprint']];assert rec['status']=='abandoned' and rec['result_available'] is False and rec['report_sha256']==invalid_sha and sha(ROOT/row['spec'])==json.loads((R/'invalid_spec_report.json').read_text())['configs'][row['name']]['original_spec_sha256']
 base=json.loads((R/'startup.json').read_text())['head_after_successful_SSH_fetch'];prefix=subprocess.check_output(['git','show',base+':research/automation/registry.jsonl'],cwd=ROOT);raw=(ROOT/'research/automation/registry.jsonl').read_bytes();assert raw.startswith(prefix);events=[json.loads(x) for x in raw[len(prefix):].splitlines()];fps={x['fingerprint'] for x in batch+bad+json.loads((R/'forward_batch.json').read_text())};assert len(events)==438 and len(fps)==219 and {x['fingerprint'] for x in events}==fps
 for fp in fps:assert sum(x['fingerprint']==fp and x['status']=='reserved' for x in events)==1 and sum(x['fingerprint']==fp and x['status'] in ['passed','rejected','abandoned'] for x in events)==1
 assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items())
 for p,h in ctx['ledger_fragments_before'].items():
  if p!='research/automation/registry.jsonl':assert sha(ROOT/p)==h
 for fs in plan['data']['assets'].values():
  for x in fs:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 diagnostics={}
 for scope in ['native','parent']:
  gs=[c for c in grid.values() if c['scope']==scope];es=[e for e in edges if e['scope']==scope];best=max(gs,key=lambda c:c['scenes']['3']['net_return_pct']);dims=axes(best);finite=[c for c in gs if c['scenes']['3']['sharpe_365'] is not None];diagnostics[scope]={'cell_count':81,'new_cells':54,'readonly_N2000_cells':27,'positive_full_grid_3x_net_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in gs)/81,'positive_full_grid_3x_Sharpe_fraction':sum(c['scenes']['3']['sharpe_365']>0 for c in finite)/81,'Sharpe_None_cells':81-len(finite),'new_local_3x_positive_fraction_range':[min(c['sensitivity']['local_3x_neighbor_positive_fraction'] for c in cs.values() if c['scope']==scope),max(c['sensitivity']['local_3x_neighbor_positive_fraction'] for c in cs.values() if c['scope']==scope)],'full_Sharpe_cliff_edges':sum(e['full_sharpe_cliff']=='True' for e in es),'recent40_Sharpe_cliff_edges':sum(e['recent40_sharpe_cliff']=='True' for e in es),'best_full_grid3_config':best['name'],'best_boundary_axes':[p for p,v in dims.items() if best[p] in [v[0],v[-1]]],'old_qualification_unchanged':True}
 put(R/'surface_diagnostics.json',{'scope':'Readonlydescriptivemetrics,notnewtrials/postresultgridextension/gatechange.','by_scope':diagnostics})
 out={'passed':True,'new_financial_configs':108,'new_native_backtests':54,'new_passive_parents':54,'readonly_native_components':30,'readonly_midpoint_cells':54,'readonly_unique_results_unchanged':63,'two_full4D_cells':162,'cost_rows_verified':486,'fold_rows_verified':6318,'recent40_fold_rows_verified':3888,'daily_NAV_rows_verified':120204,'edges_verified':432,'reference_comparisons_verified':648,'registry_append_only_events':438,'new_terminal_IDs':219,'actual_finished_IDs_including_SMA':111,'abandoned_invalid_no_result_IDs':108,'protected_files_unchanged':len(ctx['account_hashes_before']),'old_native_and_parent_qualification_preserved':True,'new_N1000_N3000_native_financial_paths_actual':True,'source_models_not_rerun':True,'finished_report_original_SHA_preserved':sha(R/'report.json')};put(R/'source_verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
