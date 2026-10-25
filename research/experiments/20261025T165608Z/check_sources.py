"""Read-only exact evidence, spec/grid and append-only status gate."""
import ast,csv,gzip,hashlib,io,itertools,json,subprocess
from run import ROOT,R,LOOKS,HURDLES,BUFFERS,NEWN,axes,grid_configs,neighbors,sha,put,reg

def main():
 plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());ctx=json.loads((R/'context.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');cs=report['configs'];grid=grid_configs(cs);assert len(batch)==len(cs)==72 and len(grid)==108 and report['frozen_plan_sha256']==sha(R/'plan.json');assert report['read_only_anchor_references']==plan['read_only_anchor_references'] and report['read_only_hold_references']==plan['read_only_hold_references'];assert sha(R/'engine.py')==sha(ROOT/plan['native_engine_base']['path'])==plan['new_engine_sha256']==plan['native_engine_base']['sha256'];assert ast.dump(ast.parse((R/'engine.py').read_text()))==ast.dump(ast.parse((ROOT/plan['native_engine_base']['path']).read_text()))
 refs=[*plan['component_sources'].values(),*plan['read_only_anchor_references'].values(),*plan['read_only_hold_references'].values()];assert len(refs)==len({r['fingerprint'] for r in refs})==46;old={}
 for ref in refs:
  fp=ref['fingerprint'];rec=records[fp];assert rec['result_available'] is True and rec['status']==ref['original_status'] and rec['report_sha256']==ref['report_sha256'];assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['spec'])==ref['spec_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'];sp=json.loads((ROOT/ref['spec']).read_text());c=json.loads((ROOT/ref['report']).read_text())['configs'][ref['name']];assert reg.fingerprint(sp)==fp==c['fingerprint'] and c['status']==ref['original_status'] and {k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()}==ref['NAV_sha256_by_cost'];old[c['name']]=c
  if c['name'] in plan['read_only_anchor_references']:assert grid[c['name']]['criteria']==c['criteria'] and grid[c['name']]['status']==c['status']
 rulehash=hashlib.sha256(json.dumps({'rules':plan['rules'],'costs':plan['component_costs']},sort_keys=True,separators=(',',':')).encode()).hexdigest();byfp={**{fp:old[r['name']] for fp,r in plan['component_sources'].items()},**{c['fingerprint']:c for c in cs.values()}}
 for row in batch:
  c=cs[row['name']];sp=json.loads((ROOT/row['spec']).read_text());p=sp['parameters'];rec=records[row['fingerprint']];assert reg.fingerprint(sp)==row['fingerprint'] and p['initial_capital_usdt']==row['capital_usdt'] and p['start_utc']==plan['time_boundaries']['oos_start_utc'] and p['end_utc']==plan['time_boundaries']['oos_end_exclusive_utc'];assert p.get('continuous_oos_days',370)==370 and p['walk_forward_folds']==13;assert rec['result_available'] is True and rec['status']==c['status'] and rec['report_sha256']==sha(R/'report.json')
  if row['scope']=='native':assert sp['universe']==['ETH/USDT'] and p['fixed_entry_notional_usdt'] in NEWN and p['initial_capital_usdt']==10000 and p['raw_entry_notional_fraction_of_initial_capital']==p['fixed_entry_notional_usdt']/10000 and sp['logic']==plan['rules']['reversal_rule'] and p['exit_buffer_fraction']==0 and p['lookback_days']==row['lookback_days'] and p['return_hurdle']==row['return_hurdle']
  else:
   fps=row['source_fingerprints'];assert [x['fingerprint'] for x in sp['components']]==fps and [x['weight'] for x in sp['components']]==[1,1] and p['raw_component_multipliers']==[1,1] and p['component_capitals_usdt']==[10000,10000] and p['initial_capital_usdt']==20000 and p['component_initial_entry_notionals_usdt']==[row['BTC_fixed_entry_notional_usdt'],row['ETH_fixed_entry_notional_usdt']] and sum(p['component_initial_entry_notionals_usdt'])==4000 and sp['logic']==plan['rules'] and p['source_rules_and_costs_sha256']==rulehash
   for asset,fp in zip(['BTC','ETH'],fps):
    x=byfp[fp];assert x['asset']==asset
    for field in ['lookback_days','return_hurdle','exit_buffer_fraction','fixed_entry_notional_usdt']:assert p[asset+'_'+field]==x[field]
   assert fps[0] in plan['component_sources'] and fps[1] in {x['fingerprint'] for x in batch if x['scope']=='native'}
  ns=neighbors(c,grid);assert c['sensitivity']['neighbor_names']==[x['name'] for x in ns] and c['sensitivity']['dimension_count']==len(axes(c)) and c['sensitivity']['local_3x_neighbor_positive_fraction']==sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)
 for scope in ['native','parent']:
  grp=[c for c in grid.values() if c['scope']==scope];dims=axes(grp[0]);assert {tuple(c[p] for p in dims) for c in grp}==set(itertools.product(*dims.values()))
 def read(n):return list(csv.DictReader((R/n).open()))
 cost,folds,recent,edges,comp=(read(n) for n in ['sensitivity.csv','fold_results.csv','recent40_fold_results.csv','joint_edges.csv','reference_comparisons.csv']);daily=list(csv.DictReader(io.StringIO(gzip.decompress((R/'daily_equity.csv.gz').read_bytes()).decode())));assert [len(x) for x in [cost,folds,recent,daily,edges,comp]]==[324,4212,2592,80136,270,432]
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
  a,b=grid[row['from']],grid[row['to']];dims=axes(a);field=row['axis'];assert a['scope']==b['scope']==row['scope'] and dims[field].index(b[field])-dims[field].index(a[field])==1 and all(a[p]==b[p] for p in dims if p!=field)
  for p,q in [('return3_delta_pp','net_return_pct'),('DD3_delta_pp','max_drawdown_pct'),('sharpe3_delta','sharpe_365')]:eq(row[p],b['scenes']['3'][q]-a['scenes']['3'][q] if b['scenes']['3'][q] is not None and a['scenes']['3'][q] is not None else None)
  eq(row['recent40_return3_delta_pp'],b['scenes']['3']['recent40']['net_return_pct']-a['scenes']['3']['recent40']['net_return_pct'])
 for row in comp:
  c=cs[row['name']];y=old[row['reference_name']];z,a=c['scenes'][row['cost_multiplier']],y['scenes'][row['cost_multiplier']];assert y['fingerprint']==row['reference_fingerprint'] and y['status']==row['reference_original_status'] and a['NAV_sha256_f64le']==row['reference_NAV_sha256'] and z['NAV_sha256_f64le']==row['new_NAV_sha256'];eq(row['return_delta_pp'],z['net_return_pct']-a['net_return_pct']);eq(row['DD_delta_pp'],z['max_drawdown_pct']-a['max_drawdown_pct']);eq(row['recent40_return_delta_pp'],z['recent40']['net_return_pct']-a.get('recent40',a.get('extension40'))['net_return_pct'])
  if row['reference_kind']=='midpoint':
   dims=axes(c);field=next(iter(dims));assert y.get(field,2000)==2000 and all(y[p]==c[p] for p in dims if p!=field)
 assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items());base=json.loads((R/'startup.json').read_text())['head_after_successful_SSH_fetch'];prefix=subprocess.check_output(['git','show',base+':research/automation/registry.jsonl'],cwd=ROOT);raw=(ROOT/'research/automation/registry.jsonl').read_bytes();assert raw.startswith(prefix);events=[json.loads(x) for x in raw[len(prefix):].splitlines()];fps={x['fingerprint'] for x in batch+json.loads((R/'forward_batch.json').read_text())};assert len(events)==150 and len(fps)==75 and {x['fingerprint'] for x in events}==fps
 for fp in fps:assert sum(x['fingerprint']==fp and x['status']=='reserved' for x in events)==1 and sum(x['fingerprint']==fp and x['status'] in ['passed','rejected'] for x in events)==1
 for p,h in ctx['ledger_fragments_before'].items():
  if p!='research/automation/registry.jsonl':assert sha(ROOT/p)==h
 for fs in plan['data']['assets'].values():
  for x in fs:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 assert sha(R/'report.json')==json.loads((R/'verification.json').read_text())['report_sha256'];assert len(json.loads((R/'reserve.json').read_text()))==len(json.loads((R/'finish.json').read_text()))==72;out={'passed':True,'new_financial_configs':72,'new_native_backtests':18,'new_passive_parents':54,'readonly_BTC_components':6,'readonly_midpoint_anchors':36,'readonly_holds':4,'readonly_unique_results_unchanged':46,'cost_rows_verified':324,'fold_rows_verified':4212,'recent40_fold_rows_verified':2592,'daily_NAV_rows_verified':80136,'edges_verified':270,'reference_comparisons_verified':432,'registry_append_only_events':150,'new_finished_IDs':75,'protected_files_unchanged':len(ctx['account_hashes_before']),'real_market_files':8,'native_engine_exact_original_bytes':True,'finished_report_original_SHA_preserved':sha(R/'report.json')};put(R/'source_verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
