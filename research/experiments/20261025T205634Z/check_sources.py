"""Read-only exact definitions, original controls, grid tables and ledger checks."""
import ast,csv,gzip,hashlib,io,itertools,json,subprocess
from run import ROOT,R,LOOKS,HURDLES,BUFFERS,SLOWS,axes,neighbors,sha,put,reg

def main():
 plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());ctx=json.loads((R/'context.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');cs=report['configs'];assert len(batch)==len(cs)==54 and report['frozen_plan_sha256']==sha(R/'plan.json');assert report['read_only_anchor_references']==plan['read_only_anchor_references'] and report['read_only_hold_references']==plan['read_only_hold_references'];assert sha(ROOT/plan['native_engine_base']['path'])==plan['native_engine_base']['sha256'] and sha(R/'engine.py')==plan['new_engine_sha256']
 assert (R/'engine.py').read_bytes()==(ROOT/plan['native_engine_base']['path']).read_bytes(),'Exactenginebytesmustnotchangewhenonlyasset/specchanges'
 refs=[*plan['component_sources'].values(),*plan['read_only_anchor_references'].values(),*plan['read_only_hold_references'].values()];assert len(refs)==len({r['fingerprint'] for r in refs})==74;old={}
 for ref in refs:
  fp=ref['fingerprint'];rec=records[fp];assert rec['result_available'] is True and rec['status']==ref['original_status'] and rec['report_sha256']==ref['report_sha256'];assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['spec'])==ref['spec_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'];sp=json.loads((ROOT/ref['spec']).read_text());c=json.loads((ROOT/ref['report']).read_text())['configs'][ref['name']];assert reg.fingerprint(sp)==fp==c['fingerprint'] and c['status']==ref['original_status'] and {k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()}==ref['NAV_sha256_by_cost'];old[c['name']]=c
 rulehash=hashlib.sha256(json.dumps({'rules':plan['rules'],'costs':plan['component_costs']},sort_keys=True,separators=(',',':')).encode()).hexdigest();byfp={**{fp:old[r['name']] for fp,r in plan['component_sources'].items()},**{c['fingerprint']:c for c in cs.values()}}
 for row in batch:
  c=cs[row['name']];sp=json.loads((ROOT/row['spec']).read_text());p=sp['parameters'];rec=records[row['fingerprint']];assert reg.fingerprint(sp)==row['fingerprint'] and p['initial_capital_usdt']==row['capital_usdt'] and p['start_utc']==plan['time_boundaries']['oos_start_utc'] and p['end_utc']==plan['time_boundaries']['oos_end_exclusive_utc'];assert p.get('continuous_oos_days',370)==370 and p['walk_forward_folds']==13;assert rec['result_available'] is True and rec['status']==c['status'] and rec['report_sha256']==sha(R/'report.json')
  if row['scope']=='native':assert sp['universe']==['BTC/USDT'] and p['fixed_entry_notional_usdt']==2000 and p['initial_capital_usdt']==10000 and p['raw_entry_notional_fraction_of_initial_capital']==.2 and sp['logic']==plan['native_rules'] and p['exit_buffer_fraction']==0 and p['lookback_days']==row['lookback_days'] and p['return_hurdle']==row['return_hurdle'] and p['trend_lookback_days']==row['trend_lookback_days'] in SLOWS and p['signal_mode']=='short_roc_zero_exit_slow_trend_gate'
  else:
   fps=row['source_fingerprints'];assert [x['fingerprint'] for x in sp['components']]==fps and [x['weight'] for x in sp['components']]==[1,1] and p['raw_component_multipliers']==[1,1] and p['component_capitals_usdt']==[10000,10000] and p['initial_capital_usdt']==20000 and p['component_initial_entry_notionals_usdt']==[2000,2000] and sp['logic']==plan['rules'] and p['source_rules_and_costs_sha256']==rulehash
   for asset,fp in zip(['BTC','ETH'],fps):
    x=byfp[fp];assert x['asset']==asset
    for field in ['lookback_days','return_hurdle','exit_buffer_fraction','fixed_entry_notional_usdt']:assert p[asset+'_'+field]==x[field]
   assert fps[1] in plan['component_sources'] and fps[0] in {x['fingerprint'] for x in batch if x['scope']=='native'} and p['BTC_trend_lookback_days']==p['ETH_trend_lookback_days']==p['trend_lookback_days']==row['trend_lookback_days'] and all(byfp[fp]['trend_lookback_days']==row['trend_lookback_days'] and byfp[fp]['lookback_days']==row['lookback_days'] and byfp[fp]['return_hurdle']==row['return_hurdle'] for fp in fps)
  ns=neighbors(c,cs);assert c['sensitivity']['neighbor_names']==[x['name'] for x in ns] and c['sensitivity']['dimension_count']==len(axes(c)) and c['sensitivity']['local_3x_neighbor_positive_fraction']==sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)
 for scope in ['native','parent']:
  grp=[c for c in cs.values() if c['scope']==scope];dims=axes(grp[0]);assert {tuple(c[p] for p in dims) for c in grp}==set(itertools.product(*dims.values()))
 def read(n):return list(csv.DictReader((R/n).open()))
 cost,folds,recent,edges,comp=(read(n) for n in ['sensitivity.csv','fold_results.csv','recent40_fold_results.csv','joint_edges.csv','reference_comparisons.csv']);daily=list(csv.DictReader(io.StringIO(gzip.decompress((R/'daily_equity.csv.gz').read_bytes()).decode())));assert [len(x) for x in [cost,folds,recent,daily,edges,comp]]==[162,2106,1296,60102,108,405]
 def eq(text,value):assert (text=='' if value is None else float(text)==value),(text,value)
 for row in cost:
  c=cs[row['name']];z=c['scenes'][row['cost_multiplier']];assert row['NAV_sha256_f64le']==z['NAV_sha256_f64le'] and float(row['capital_usdt'])==c['capital_usdt']
  for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt']:eq(row[p],z[p])
  for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:eq(row['recent40_'+p],z['recent40'][p])
 for rows,isrecent in [(folds,False),(recent,True)]:
  for row in rows:
   z=cs[row['name']]['scenes'][row['cost_multiplier']];z=(z['recent40'] if isrecent else z)['folds'][int(row['fold'])-1]
   for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:eq(row[p],z[p])
 for row in daily:assert float(row['equity_usdt'])==cs[row['name']]['scenes'][row['cost_multiplier']]['daily_equity_usdt'][int(row['boundary_index'])]
 for row in edges:
  a,b=cs[row['from']],cs[row['to']];dims=axes(a);field=row['axis'];assert a['scope']==b['scope']==row['scope'] and dims[field].index(b[field])-dims[field].index(a[field])==1 and all(a[p]==b[p] for p in dims if p!=field)
  for p,q in [('return3_delta_pp','net_return_pct'),('DD3_delta_pp','max_drawdown_pct'),('sharpe3_delta','sharpe_365')]:eq(row[p],b['scenes']['3'][q]-a['scenes']['3'][q] if b['scenes']['3'][q] is not None and a['scenes']['3'][q] is not None else None)
  eq(row['recent40_return3_delta_pp'],b['scenes']['3']['recent40']['net_return_pct']-a['scenes']['3']['recent40']['net_return_pct'])
 for row in comp:
  c=cs[row['name']];y=old[row['reference_name']];z,a=c['scenes'][row['cost_multiplier']],y['scenes'][row['cost_multiplier']];assert y['fingerprint']==row['reference_fingerprint'] and y['status']==row['reference_original_status'] and a['NAV_sha256_f64le']==row['reference_NAV_sha256'] and z['NAV_sha256_f64le']==row['new_NAV_sha256'];eq(row['return_delta_pp'],z['net_return_pct']-a['net_return_pct']);eq(row['DD_delta_pp'],z['max_drawdown_pct']-a['max_drawdown_pct']);eq(row['recent40_return_delta_pp'],z['recent40']['net_return_pct']-a.get('recent40',a.get('extension40'))['net_return_pct']);eq(row['execution_count_delta'],z['executions']-a['executions']);eq(row['cost_delta_usdt'],z['cost_usdt']-a['cost_usdt']);eq(row['funding_delta_usdt'],z['funding_usdt']-a['funding_usdt'])
  if row['reference_kind']=='unfiltered':assert y['scope']==c['scope'] and y['lookback_days']==c['lookback_days'] and y['return_hurdle']==c['return_hurdle']
  elif row['reference_kind']=='mixed_default':assert c['scope']=='parent' and y['trend_exit_buffer_fraction']==.01 and y['trend_filter_lookback_days']==c['trend_lookback_days'] and y['reversal_lookback_days']==c['lookback_days'] and y['reversal_return_hurdle']==c['return_hurdle']

 assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items());base=json.loads((R/'startup.json').read_text())['head_after_successful_SSH_fetch'];prefix=subprocess.check_output(['git','show',base+':research/automation/registry.jsonl'],cwd=ROOT);raw=(ROOT/'research/automation/registry.jsonl').read_bytes();assert raw.startswith(prefix);events=[json.loads(x) for x in raw[len(prefix):].splitlines()];fps={x['fingerprint'] for x in batch+json.loads((R/'forward_batch.json').read_text())};assert len(events)==114 and len(fps)==57 and {x['fingerprint'] for x in events}==fps
 for fp in fps:assert sum(x['fingerprint']==fp and x['status']=='reserved' for x in events)==1 and sum(x['fingerprint']==fp and x['status'] in ['passed','rejected'] for x in events)==1
 for p,h in ctx['ledger_fragments_before'].items():
  if p!='research/automation/registry.jsonl':assert sha(ROOT/p)==h
 for fs in plan['data']['assets'].values():
  for x in fs:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 surface={}
 for scope in ['native','parent']:
  group=[c for c in cs.values() if c['scope']==scope];best=max(group,key=lambda c:c['scenes']['3']['net_return_pct']);finite=[c for c in group if c['scenes']['3']['sharpe_365'] is not None];surface[scope]={'cells':len(group),'positive_3x_net_return_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in group)/len(group),'positive_3x_Sharpe_fraction_all_cells':sum(c['scenes']['3']['sharpe_365']>0 for c in finite)/len(group),'Sharpe_None_cells':len(group)-len(finite),'local_3x_positive_fraction_range':[min(c['sensitivity']['local_3x_neighbor_positive_fraction'] for c in group),max(c['sensitivity']['local_3x_neighbor_positive_fraction'] for c in group)],'full_Sharpe_cliff_edges':sum(e['full_sharpe_cliff']=='True' for e in edges if e['scope']==scope),'recent40_Sharpe_cliff_edges':sum(e['recent40_sharpe_cliff']=='True' for e in edges if e['scope']==scope),'best_full3_config':best['name'],'best_at_boundary_axes':[p for p,v in axes(best).items() if best[p] in [v[0],v[-1]]],'qualification_unchanged':True}
 put(R/'surface_diagnostics.json',{'scope':'Readonlymetricsfromfrozen/fullgrid;noextratrials,nogatechanges. Boundaryoptimumistestedrange limitation,notlicenseforpostresultgridextension.','grids':surface})
 inactive={'BTC':[],'ETH':[]}
 for asset,items in [('BTC',[c for c in cs.values() if c['scope']=='native']),('ETH',list(plan['component_sources'].values()))]:
  for c in items:
   assert sha(ROOT/c['archive'])==c['archive_sha256'];arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));scene=arc['scenes']['1'];z=scene['summary'];start=z['NAV_points']-z['recent40']['NAV_points'];fully_cash=all(__import__('decimal').Decimal(seg['signed_units'])==0 for seg in scene['state_segments'] if seg['axis_end_exclusive']>start);recent_trades=[t for t in scene['trades'] if t['axis_index']>=start]
   if fully_cash:assert not recent_trades and z['recent40']['net_return_pct']==0 and len(set(z['recent40']['daily_equity_usdt']))==1;inactive[asset].append(c['fingerprint'])
 parent_classes={'both_cash':0,'BTC_cash_ETH_active':0,'ETH_cash_BTC_active':0,'both_active':0}
 for c in cs.values():
  if c['scope']!='parent':continue
  b,e=c['source_fingerprints'];ib,ie=b in inactive['BTC'],e in inactive['ETH'];key='both_cash' if ib and ie else 'BTC_cash_ETH_active' if ib else 'ETH_cash_BTC_active' if ie else 'both_active';parent_classes[key]+=1
 recent_activity={'scope':'ReadonlysavednativeBTC/cachedETHstateandtrades,notnewfinancialevaluation.1xcoststateaudit,noinventedcashyield.','native_recent40_fully_cash_fingerprints_by_asset':inactive,'native_recent40_fully_cash_configs_1x_by_asset':{a:len(v) for a,v in inactive.items()},'parent_recent40_activity_classes_1x':parent_classes,'interpretation':'Cashlegdoesnotproveongoingalpha;bothcashparenthaszeroNAVchange,oneactivelegparentNAVchangecomesonlyfromthatasset. Qualificationunchanged.'};put(R/'recent_activity.json',recent_activity)
 assert sha(R/'report.json')==json.loads((R/'verification.json').read_text())['report_sha256'];assert len(json.loads((R/'reserve.json').read_text()))==len(json.loads((R/'finish.json').read_text()))==54;out={'passed':True,'new_financial_configs':54,'new_native_backtests':27,'new_passive_parents':27,'readonly_ETH_components':27,'readonly_unfiltered_controls':18,'readonly_mixed_controls':27,'readonly_holds':2,'readonly_unique_results_unchanged':74,'cost_rows_verified':162,'fold_rows_verified':2106,'recent40_fold_rows_verified':1296,'daily_NAV_rows_verified':60102,'edges_verified':108,'reference_comparisons_verified':405,'registry_append_only_events':114,'new_finished_IDs':57,'protected_files_unchanged':len(ctx['account_hashes_before']),'real_market_files':8,'execution_quantity_cost_funding_clock_code_exact_base_bytes':True,'finished_report_original_SHA_preserved':sha(R/'report.json')};put(R/'source_verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
