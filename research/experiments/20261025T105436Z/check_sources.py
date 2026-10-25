"""Verify native/parent definitions, all tables, old controls and append-only records."""
import ast,csv,gzip,io,itertools,json,subprocess
from run import ROOT,R,WINDOWS,CAPS,sha,reg,put,neighbors
def main():
 plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');batch=json.loads((R/'batch.json').read_text());cs=report['configs'];assert len(batch)==27 and len(cs)==27 and report['frozen_plan_sha256']==sha(R/'plan.json') and sha(R/'engine.py')==plan['new_engine_sha256']
 oldast=ast.parse((ROOT/plan['native_engine_base']['path']).read_text());newast=ast.parse((R/'engine.py').read_text());oldfunc={f.name:ast.dump(f,include_attributes=False) for f in oldast.body if isinstance(f,ast.FunctionDef)};newfunc={f.name:ast.dump(f,include_attributes=False) for f in newast.body if isinstance(f,ast.FunctionDef)};unchanged=['target','funding_amount','trade','load_market','margin_audit','stats','summary'];assert all(oldfunc[n]==newfunc[n] for n in unchanged)
 for asset in ['BTC','ETH','COMBO']:assert {(c['volatility_lookback_days'],c['annualized_volatility_cap']) for c in cs.values() if c['asset']==asset}==set(itertools.product(WINDOWS,CAPS))
 docs={};reference_configs={}
 for label,ref in plan['read_only_references'].items():
  rec=records[ref['fingerprint']];assert rec['result_available'] is True and rec['status']==ref['original_status'] and rec['report_sha256']==ref['report_sha256'];assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['spec'])==ref['spec_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'];path=ref['report']
  if path not in docs:docs[path]=json.loads((ROOT/path).read_text())
  reference_configs[label]=docs[path]['configs'][ref['name']];assert reference_configs[label]['status']==ref['original_status']
 byfp={c['fingerprint']:c for c in cs.values()}
 for row in batch:
  c=cs[row['name']];sp=json.loads((ROOT/row['spec']).read_text());p=sp['parameters'];rec=records[row['fingerprint']];assert reg.fingerprint(sp)==row['fingerprint'];assert p['volatility_lookback_days']==row['volatility_lookback_days'] and p['annualized_volatility_cap']==row['annualized_volatility_cap'];assert p['start_utc']==plan['time_boundaries']['oos_start_utc'] and p['end_utc']==plan['time_boundaries']['oos_end_exclusive_utc'] and p['walk_forward_folds']==13
  if row['scope']=='native':
   assert p['initial_capital_usdt']==10000 and p['fixed_entry_notional_usdt']==2000 and p['lookback_days']==plan['grid'][row['asset']]['lookback_days'] and p['return_hurdle']==plan['grid'][row['asset']]['return_hurdle'] and p['exit_buffer_fraction']==.01 and p['volatility_ddof']==1 and p['annualization_days']==365
  else:
   assert p['initial_capital_usdt']==20000 and p['raw_component_multipliers']==[1,1] and p['component_capitals_usdt']==[10000,10000] and p['component_initial_entry_notionals_usdt']==[2000,2000] and [x['weight'] for x in sp['components']]==[1,1] and [x['fingerprint'] for x in sp['components']]==row['source_fingerprints'];assert [byfp[fp]['asset'] for fp in row['source_fingerprints']]==['BTC','ETH']
  assert rec['result_available'] is True and rec['status']==c['status'] and rec['report_sha256']==sha(R/'report.json');ns=neighbors(c,cs);assert c['sensitivity']['neighbor_names']==[x['name'] for x in ns] and c['sensitivity']['local_3x_neighbor_positive_fraction']==sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)
 def read(n):return list(csv.DictReader((R/n).open()))
 cost,folds,recent,edges,comp=(read(n) for n in ['sensitivity.csv','fold_results.csv','recent40_fold_results.csv','joint_edges.csv','reference_comparisons.csv']);daily=list(csv.DictReader(io.StringIO(gzip.decompress((R/'daily_equity.csv.gz').read_bytes()).decode())));assert [len(x) for x in [cost,folds,recent,daily,edges,comp]]==[81,1053,648,30051,36,162]
 for row in cost:
  c=cs[row['name']];z=c['scenes'][row['cost_multiplier']];assert row['NAV_sha256_f64le']==z['NAV_sha256_f64le'] and row['asset']==c['asset'] and row['capital_usdt']==str(c['capital_usdt'])
  for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt']:assert float(row[p])==z[p] if z[p] is not None else row[p]==''
  for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:assert float(row['recent40_'+p])==z['recent40'][p] if z['recent40'][p] is not None else row['recent40_'+p]==''
 for rows,isrecent in [(folds,False),(recent,True)]:
  for row in rows:
   z=cs[row['name']]['scenes'][row['cost_multiplier']];z=(z['recent40'] if isrecent else z)['folds'][int(row['fold'])-1]
   for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:assert float(row[p])==z[p] if z[p] is not None else row[p]==''
 for row in daily:assert float(row['equity_usdt'])==cs[row['name']]['scenes'][row['cost_multiplier']]['daily_equity_usdt'][int(row['boundary_index'])]
 from summarize import FIELDS,AXES,key
 for row in edges:
  a,b=cs[row['from']],cs[row['to']];i=FIELDS.index(row['axis']);pa,pb=key(a),key(b);assert a['asset']==b['asset']==row['asset'] and AXES[i].index(pb[i])-AXES[i].index(pa[i])==1 and all(pa[j]==pb[j] for j in range(2) if j!=i)
  for p,q in [('return3_delta_pp','net_return_pct'),('DD3_delta_pp','max_drawdown_pct'),('sharpe3_delta','sharpe_365')]:
   if a['scenes']['3'][q] is not None and b['scenes']['3'][q] is not None:assert float(row[p])==b['scenes']['3'][q]-a['scenes']['3'][q]
   else:assert row[p]==''
  assert float(row['recent40_return3_delta_pp'])==b['scenes']['3']['recent40']['net_return_pct']-a['scenes']['3']['recent40']['net_return_pct']
 for row in comp:
  c=cs[row['name']];old=reference_configs[row['reference_label']];assert old['fingerprint']==row['reference_fingerprint'] and old['status']==row['reference_original_status'];z,y=c['scenes'][row['cost_multiplier']],old['scenes'][row['cost_multiplier']];t=y.get('recent40',y.get('extension40'));assert float(row['return_delta_pp'])==z['net_return_pct']-y['net_return_pct'] and float(row['DD_delta_pp'])==z['max_drawdown_pct']-y['max_drawdown_pct'] and float(row['recent40_return_delta_pp'])==z['recent40']['net_return_pct']-t['net_return_pct'] and row['reference_NAV_sha256']==y['NAV_sha256_f64le'] and row['new_NAV_sha256']==z['NAV_sha256_f64le']
 assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items());base=json.loads((R/'startup.json').read_text())['head_after_successful_SSH_fetch'];prefix=subprocess.check_output(['git','show',base+':research/automation/registry.jsonl'],cwd=ROOT);raw=(ROOT/'research/automation/registry.jsonl').read_bytes();assert raw.startswith(prefix);events=[json.loads(x) for x in raw[len(prefix):].splitlines()];fps={x['fingerprint'] for x in batch+json.loads((R/'forward_batch.json').read_text())};assert len(events)==60 and len(fps)==30 and {x['fingerprint'] for x in events}==fps
 for fp in fps:assert sum(x['fingerprint']==fp and x['status']=='reserved' for x in events)==1 and sum(x['fingerprint']==fp and x['status'] in ['passed','rejected'] for x in events)==1
 for p,h in ctx['ledger_fragments_before'].items():
  if p!='research/automation/registry.jsonl':assert sha(ROOT/p)==h
 for fs in plan['data']['assets'].values():
  for x in fs:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 assert sha(R/'report.json')==json.loads((R/'verification.json').read_text())['report_sha256'];out={'passed':True,'new_financial_configs':27,'new_native_components':18,'new_passive_parents':9,'old_controls_status_report_and_NAV_unchanged':6,'unchanged_native_engine_functions':unchanged,'new_two_axis_cells_by_asset':9,'cost_rows_verified':81,'fold_rows_verified':1053,'recent40_fold_rows_verified':648,'daily_NAV_rows_verified':30051,'edges_verified':36,'reference_comparisons_verified':162,'registry_append_only_events':60,'new_finished_IDs':30,'protected_files_unchanged':len(ctx['account_hashes_before']),'real_market_files':8,'finished_report_original_SHA_preserved':sha(R/'report.json')};put(R/'source_verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
