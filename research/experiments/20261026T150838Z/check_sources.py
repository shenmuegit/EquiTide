"""Registry, metadata, every exported table and immutable controls verification."""
import ast,csv,gzip,io,itertools,json,subprocess
from decimal import Decimal as D
from run import ROOT,R,reg,sha,put,grid_configs,axes,neighbors

def main():
 report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');batch=json.loads((R/'batch.json').read_text());cs=report['configs'];grid=grid_configs(cs);assert len(cs)==168 and len(grid)==252 and len(batch)==168
 refs=[*plan['component_sources'].values(),*plan['read_only_anchor_references'].values(),*plan['read_only_hold_references'].values(),*json.loads((R/'native_holds.json').read_text())['references'].values()];old={};unique={}
 for ref in refs:
  fp=ref['fingerprint'];assert records[fp]['result_available'] and records[fp]['status']==ref['original_status'] and records[fp]['report_sha256']==ref['report_sha256'] and sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['spec'])==ref['spec_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'];sp=json.loads((ROOT/ref['spec']).read_text());assert reg.fingerprint(sp)==fp;unique[fp]=ref
  if ref['report'] not in old:old[ref['report']]=json.loads((ROOT/ref['report']).read_text())
 assert len(unique)==171
 oldby={c['name']:c for doc in old.values() for c in doc['configs'].values()}
 for row in batch:
  c=cs[row['name']];sp=json.loads((ROOT/row['spec']).read_text());assert reg.fingerprint(sp)==row['fingerprint']==c['fingerprint'] and records[c['fingerprint']]['result_available'] is True and records[c['fingerprint']]['status']==c['status'] and records[c['fingerprint']]['report_sha256']==sha(R/'report.json') and c['capital_usdt']==sp['parameters']['initial_capital_usdt']
  p=sp['parameters'];assert p['start_utc']==plan['time_boundaries']['oos_start_utc'] and p['end_utc']==plan['time_boundaries']['oos_end_exclusive_utc']
  if c['scope']=='native':assert c['asset']=='BTC' and c['lookback_days']==p['lookback_days'] and p['lookback_days'] in [25,28] and p['return_hurdle']==c['return_hurdle']==.04 and p['exit_buffer_fraction']==.01 and p['fixed_entry_notional_usdt']==c['fixed_entry_notional_usdt'] and p['raw_entry_notional_fraction_of_initial_capital']==p['fixed_entry_notional_usdt']/10000
  else:
   assert c['BTC_lookback_days']==p['BTC_lookback_days'] and p['BTC_lookback_days'] in [25,28] and c['BTC_return_hurdle']==p['BTC_return_hurdle']==.04 and c['trend_exit_buffer_fraction']==p['BTC_exit_buffer_fraction']==.01 and p['component_capitals_usdt']==[10000,10000] and p['raw_component_multipliers']==[1,1] and sum(p['component_initial_entry_notionals_usdt'])==4000
   assert [x['fingerprint'] for x in sp['components']]==c['source_fingerprints'] and all(x['weight']==1 for x in sp['components']) and p['ETH_fixed_entry_notional_usdt']==c['ETH_fixed_entry_notional_usdt'] and p['BTC_fixed_entry_notional_usdt']==c['BTC_fixed_entry_notional_usdt']
  ns=neighbors(c,grid);assert c['sensitivity']['neighbor_names']==[x['name'] for x in ns] and c['sensitivity']['dimension_count']==(2 if c['scope']=='native' else 5) and c['sensitivity']['local_3x_neighbor_positive_fraction']==sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)
 for scope,count,oldcount in [('native',9,3),('parent',243,81)]:
  sub=[c for c in grid.values() if c['scope']==scope];dims=axes(sub[0]);assert len(sub)==count and sum(c.get('read_only_anchor',False) for c in sub)==oldcount and {tuple(c[p] for p in dims) for c in sub}==set(itertools.product(*dims.values()))
 def read(n):return list(csv.DictReader((R/n).open()))
 cost,folds,recent,edges,comp=(read(n) for n in ['sensitivity.csv','fold_results.csv','recent40_fold_results.csv','joint_edges.csv','reference_comparisons.csv']);daily=list(csv.DictReader(io.StringIO(gzip.decompress((R/'daily_equity.csv.gz').read_bytes()).decode())));assert [len(x) for x in [cost,folds,recent,daily,edges,comp]]==[756,9828,6048,186984,822,1008]
 def eq(text,value):assert (text=='' if value is None else float(text)==value),(text,value)
 for row in cost:
  c=grid[row['name']];z=c['scenes'][row['cost_multiplier']];assert row['NAV_sha256_f64le']==z['NAV_sha256_f64le'] and float(row['capital_usdt'])==c['capital_usdt'] and row['read_only_anchor']==str(c.get('read_only_anchor',False)) and row['scope']==c['scope']
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
  c=cs[row['name']];y=oldby[row['reference_name']];z,a=c['scenes'][row['cost_multiplier']],y['scenes'][row['cost_multiplier']];a40=a.get('recent40',a.get('extension40'));assert y['fingerprint']==row['reference_fingerprint'] and y['status']==row['reference_original_status'] and a['NAV_sha256_f64le']==row['reference_NAV_sha256'] and z['NAV_sha256_f64le']==row['new_NAV_sha256'];eq(row['return_delta_pp'],z['net_return_pct']-a['net_return_pct']);eq(row['DD_delta_pp'],z['max_drawdown_pct']-a['max_drawdown_pct']);eq(row['recent40_return_delta_pp'],z['recent40']['net_return_pct']-a40['net_return_pct']);eq(row['execution_count_delta'],z['executions']-a['executions']);eq(row['cost_delta_usdt'],z['cost_usdt']-a['cost_usdt'])
  if row['reference_kind']=='matched_old_BTC_L31':
   assert y['name']==c['matched_old_BTC_L31']
   if c['scope']=='native':assert y['return_hurdle']==.04 and y['lookback_days']==31 and y['fixed_entry_notional_usdt']==c['fixed_entry_notional_usdt']
   else:assert all(y.get(p,2000 if 'notional' in p else None)==c[p] for p in ['ETH_fixed_entry_notional_usdt','trend_filter_lookback_days','reversal_lookback_days','reversal_return_hurdle'])
 assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items());base=json.loads((R/'startup.json').read_text())['head_after_successful_SSH_fetch'];prefix=subprocess.check_output(['git','show',base+':research/automation/registry.jsonl'],cwd=ROOT);raw=(ROOT/'research/automation/registry.jsonl').read_bytes();assert raw.startswith(prefix);events=[json.loads(x) for x in raw[len(prefix):].splitlines()];fps={x['fingerprint'] for x in batch+json.loads((R/'forward_batch.json').read_text())};assert len(events)==342 and len(fps)==171 and {x['fingerprint'] for x in events}==fps
 for fp in fps:assert sum(x['fingerprint']==fp and x['status']=='reserved' for x in events)==1 and sum(x['fingerprint']==fp and x['status'] in ['passed','rejected'] for x in events)==1
 for p,h in ctx['ledger_fragments_before'].items():
  if p!='research/automation/registry.jsonl':assert sha(ROOT/p)==h
 for fs in plan['data']['assets'].values():
  for x in fs:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 surface={}
 for scope in ['native','parent']:
  sub=[c for c in grid.values() if c['scope']==scope];new=[c for c in cs.values() if c['scope']==scope];dims=axes(sub[0]);best=max(sub,key=lambda c:c['scenes']['3']['net_return_pct']);surface[scope]={'cell_count':len(sub),'positive_full_grid_3x_net_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in sub)/len(sub),'positive_full_grid_3x_Sharpe_fraction':sum(c['scenes']['3']['sharpe_365'] is not None and c['scenes']['3']['sharpe_365']>0 for c in sub)/len(sub),'new_local_positive_fraction_range':[min(c['sensitivity']['local_3x_neighbor_positive_fraction'] for c in new),max(c['sensitivity']['local_3x_neighbor_positive_fraction'] for c in new)],'best_full_grid3_config':best['name'],'best_boundary_axes':[p for p,v in dims.items() if best[p] in [v[0],v[-1]]],'full_Sharpe_cliff_edges':sum(x['scope']==scope and x['full_sharpe_cliff']=='True' for x in edges),'recent_Sharpe_cliff_edges':sum(x['scope']==scope and x['recent40_sharpe_cliff']=='True' for x in edges),'old_qualification_unchanged':True}
 put(R/'surface_diagnostics.json',surface)
 inactive={'BTC':[],'ETH':[]};allnatives=[*plan['component_sources'].values(),*[c for c in cs.values() if c['scope']=='native']]
 for x in allnatives:
  arc=json.loads(gzip.decompress((ROOT/x['archive']).read_bytes()));s=arc['scenes']['1'];z=s['summary'];start=z['NAV_points']-z.get('recent40',z.get('extension40'))['NAV_points'];cash=all(D(seg['signed_units'])==0 for seg in s['state_segments'] if seg['axis_end_exclusive']>start)
  if cash:assert not [t for t in s['trades'] if t['axis_index']>=start] and z.get('recent40',z.get('extension40'))['net_return_pct']==0;inactive[x['asset']].append(x['fingerprint'])
 classes={'both_cash':0,'BTC_cash_ETH_active':0,'ETH_cash_BTC_active':0,'both_active':0}
 for c in cs.values():
  if c['scope']!='parent':continue
  b,e=c['source_fingerprints'];ib,ie=b in inactive['BTC'],e in inactive['ETH'];classes['both_cash' if ib and ie else 'BTC_cash_ETH_active' if ib else 'ETH_cash_BTC_active' if ie else 'both_active']+=1
 put(R/'recent_activity.json',{'scope':'Read-only source/newnative recorded ledger, no model rerun.','native_recent40_fully_cash_configs_1x_by_asset':{a:len(v) for a,v in inactive.items()},'parent_recent40_activity_classes_1x':classes})
 tree=ast.parse((R/'run.py').read_text());calls=[x for x in ast.walk(tree) if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=='simulate'];assert len(calls)==1 and sum(x['scope']=='native' for x in batch)==6
 assert sha(R/'report.json')==json.loads((R/'verification.json').read_text())['report_sha256'] and len(json.loads((R/'reserve.json').read_text()))==len(json.loads((R/'finish.json').read_text()))==168
 out={'passed':True,'new_financial_configs':168,'new_native_backtests':6,'new_passive_parents':162,'readonly_native_components':84,'readonly_old_parent_cells':81,'readonly_old_native_cells':3,'readonly_matched_holds':6,'readonly_unique_results_unchanged':171,'full5D_parent_cells':243,'full2D_native_cells':9,'cost_rows_verified':756,'fold_rows_verified':9828,'recent40_fold_rows_verified':6048,'daily_NAV_rows_verified':186984,'edges_verified':822,'reference_comparisons_verified':1008,'registry_append_only_events':342,'new_finished_IDs':171,'protected_files_unchanged':len(ctx['account_hashes_before']),'native_and_old_parent_original_qualification_preserved':True,'only6newnative_models_run':True,'finished_report_original_SHA_preserved':sha(R/'report.json')};put(R/'source_verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
