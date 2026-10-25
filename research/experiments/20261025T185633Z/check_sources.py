"""Read-only exact definitions, original controls, grid tables and ledger checks."""
import ast,csv,gzip,hashlib,io,itertools,json,subprocess
from run import ROOT,R,LOOKS,HURDLES,BUFFERS,SLOWS,axes,neighbors,sha,put,reg

def main():
 plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());ctx=json.loads((R/'context.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');cs=report['configs'];assert len(batch)==len(cs)==108 and report['frozen_plan_sha256']==sha(R/'plan.json');assert report['read_only_anchor_references']==plan['read_only_anchor_references'] and report['read_only_hold_references']==plan['read_only_hold_references'];assert sha(ROOT/plan['native_engine_base']['path'])==plan['native_engine_base']['sha256'] and sha(R/'engine.py')==plan['new_engine_sha256']
 base=(ROOT/plan['native_engine_base']['path']).read_text();new=(R/'engine.py').read_text();a,b=new.index('def target('),new.index('\ndef funding_amount');aa,bb=base.index('def target('),base.index('\ndef funding_amount');restored=new[:a]+base[aa:bb]+new[b:];restored=restored.replace('wanted,r,slow_r=(1,None,None)','wanted,r=(1,None)').replace(",p['exit_buffer_fraction'],p['trend_lookback_days']);q=",",p['exit_buffer_fraction']);q=").replace("'lookback_return_exact':r,'trend_return_exact':slow_r,'trend_lookback_days':p['trend_lookback_days'],'desired_direction'","'lookback_return_exact':r,'desired_direction'");assert restored==base,'Execution,quantity,cost,funding,clockandNAVcodeoutsidefrozenruleeditmustbeexactbasebytes'
 refs=[*plan['component_sources'].values(),*plan['read_only_anchor_references'].values(),*plan['read_only_hold_references'].values()];assert len(refs)==len({r['fingerprint'] for r in refs})==41;old={}
 for ref in refs:
  fp=ref['fingerprint'];rec=records[fp];assert rec['result_available'] is True and rec['status']==ref['original_status'] and rec['report_sha256']==ref['report_sha256'];assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['spec'])==ref['spec_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'];sp=json.loads((ROOT/ref['spec']).read_text());c=json.loads((ROOT/ref['report']).read_text())['configs'][ref['name']];assert reg.fingerprint(sp)==fp==c['fingerprint'] and c['status']==ref['original_status'] and {k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()}==ref['NAV_sha256_by_cost'];old[c['name']]=c
 rulehash=hashlib.sha256(json.dumps({'rules':plan['rules'],'costs':plan['component_costs']},sort_keys=True,separators=(',',':')).encode()).hexdigest();byfp={**{fp:old[r['name']] for fp,r in plan['component_sources'].items()},**{c['fingerprint']:c for c in cs.values()}}
 for row in batch:
  c=cs[row['name']];sp=json.loads((ROOT/row['spec']).read_text());p=sp['parameters'];rec=records[row['fingerprint']];assert reg.fingerprint(sp)==row['fingerprint'] and p['initial_capital_usdt']==row['capital_usdt'] and p['start_utc']==plan['time_boundaries']['oos_start_utc'] and p['end_utc']==plan['time_boundaries']['oos_end_exclusive_utc'];assert p.get('continuous_oos_days',370)==370 and p['walk_forward_folds']==13;assert rec['result_available'] is True and rec['status']==c['status'] and rec['report_sha256']==sha(R/'report.json')
  if row['scope']=='native':assert sp['universe']==['ETH/USDT'] and p['fixed_entry_notional_usdt']==2000 and p['initial_capital_usdt']==10000 and p['raw_entry_notional_fraction_of_initial_capital']==.2 and sp['logic']==plan['native_rules'] and p['exit_buffer_fraction']==0 and p['lookback_days']==row['lookback_days'] and p['return_hurdle']==row['return_hurdle'] and p['trend_lookback_days']==row['trend_lookback_days'] in SLOWS and p['signal_mode']=='short_roc_zero_exit_slow_trend_gate'
  else:
   fps=row['source_fingerprints'];assert [x['fingerprint'] for x in sp['components']]==fps and [x['weight'] for x in sp['components']]==[1,1] and p['raw_component_multipliers']==[1,1] and p['component_capitals_usdt']==[10000,10000] and p['initial_capital_usdt']==20000 and p['component_initial_entry_notionals_usdt']==[2000,2000] and sp['logic']==plan['rules'] and p['source_rules_and_costs_sha256']==rulehash
   for asset,fp in zip(['BTC','ETH'],fps):
    x=byfp[fp];assert x['asset']==asset
    for field in ['lookback_days','return_hurdle','exit_buffer_fraction','fixed_entry_notional_usdt']:assert p[asset+'_'+field]==x[field]
   assert fps[0] in plan['component_sources'] and fps[1] in {x['fingerprint'] for x in batch if x['scope']=='native'} and p['ETH_trend_lookback_days']==p['trend_filter_lookback_days']==row['trend_filter_lookback_days']==byfp[fps[1]]['trend_lookback_days']
  ns=neighbors(c,cs);assert c['sensitivity']['neighbor_names']==[x['name'] for x in ns] and c['sensitivity']['dimension_count']==len(axes(c)) and c['sensitivity']['local_3x_neighbor_positive_fraction']==sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)
 for scope in ['native','parent']:
  grp=[c for c in cs.values() if c['scope']==scope];dims=axes(grp[0]);assert {tuple(c[p] for p in dims) for c in grp}==set(itertools.product(*dims.values()))
 def read(n):return list(csv.DictReader((R/n).open()))
 cost,folds,recent,edges,comp=(read(n) for n in ['sensitivity.csv','fold_results.csv','recent40_fold_results.csv','joint_edges.csv','reference_comparisons.csv']);daily=list(csv.DictReader(io.StringIO(gzip.decompress((R/'daily_equity.csv.gz').read_bytes()).decode())));assert [len(x) for x in [cost,folds,recent,daily,edges,comp]]==[324,4212,2592,120204,270,648]
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
  if row['reference_kind']=='unfiltered':
   match=['lookback_days','return_hurdle'] if c['scope']=='native' else ['trend_exit_buffer_fraction','reversal_lookback_days','reversal_return_hurdle'];assert y['scope']==c['scope'] and all(y[p]==c[p] for p in match)
 assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items());base=json.loads((R/'startup.json').read_text())['head_after_successful_SSH_fetch'];prefix=subprocess.check_output(['git','show',base+':research/automation/registry.jsonl'],cwd=ROOT);raw=(ROOT/'research/automation/registry.jsonl').read_bytes();assert raw.startswith(prefix);events=[json.loads(x) for x in raw[len(prefix):].splitlines()];fps={x['fingerprint'] for x in batch+json.loads((R/'forward_batch.json').read_text())};assert len(events)==222 and len(fps)==111 and {x['fingerprint'] for x in events}==fps
 for fp in fps:assert sum(x['fingerprint']==fp and x['status']=='reserved' for x in events)==1 and sum(x['fingerprint']==fp and x['status'] in ['passed','rejected'] for x in events)==1
 for p,h in ctx['ledger_fragments_before'].items():
  if p!='research/automation/registry.jsonl':assert sha(ROOT/p)==h
 for fs in plan['data']['assets'].values():
  for x in fs:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 inactive=[]
 for c in cs.values():
  if c['scope']!='native':continue
  assert sha(ROOT/c['archive'])==c['archive_sha256'];arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));scene=arc['scenes']['1'];z=scene['summary'];start=z['NAV_points']-z['recent40']['NAV_points'];fully_cash=all(__import__('decimal').Decimal(seg['signed_units'])==0 for seg in scene['state_segments'] if seg['axis_end_exclusive']>start);recent_trades=[t for t in scene['trades'] if t['axis_index']>=start]
  if fully_cash:
   assert not recent_trades and z['recent40']['net_return_pct']==0 and len(set(z['recent40']['daily_equity_usdt']))==1;inactive.append(c['fingerprint'])
 recent_activity={'scope':'Read-only existingstate/tradeevidence,notnewfinancialconfigorbacktest. 1xcoststateaudit;nocashyieldinvented.','native_recent40_fully_cash_fingerprints':inactive,'native_recent40_fully_cash_configs_1x':len(inactive),'parent_configs_with_fully_cash_recent_ETH_leg_1x':sum(c['scope']=='parent' and c['source_fingerprints'][1] in inactive for c in cs.values()),'interpretation':'IntheseparentsrecentabsoluteNAVchangescomefromBTClegonly;cashETHlegdoesnotproveongoingreversalalpha. Qualificationunchanged.'};put(R/'recent_activity.json',recent_activity)
 assert sha(R/'report.json')==json.loads((R/'verification.json').read_text())['report_sha256'];assert len(json.loads((R/'reserve.json').read_text()))==len(json.loads((R/'finish.json').read_text()))==108;out={'passed':True,'new_financial_configs':108,'new_native_backtests':27,'new_passive_parents':81,'readonly_BTC_components':3,'readonly_unfiltered_controls':36,'readonly_holds':2,'readonly_unique_results_unchanged':41,'cost_rows_verified':324,'fold_rows_verified':4212,'recent40_fold_rows_verified':2592,'daily_NAV_rows_verified':120204,'edges_verified':270,'reference_comparisons_verified':648,'registry_append_only_events':222,'new_finished_IDs':111,'protected_files_unchanged':len(ctx['account_hashes_before']),'real_market_files':8,'execution_quantity_cost_funding_clock_code_exact_base_bytes':True,'finished_report_original_SHA_preserved':sha(R/'report.json')};put(R/'source_verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
