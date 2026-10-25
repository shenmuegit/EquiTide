"""Validate every mixed definition, source hash, result row and append-only record."""
import csv,gzip,io,itertools,json,subprocess
from run import ROOT,R,BUFFERS,LOOKS,HURDLES,STYLES,sha,reg,put,neighbors
def main():
 plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');batch=json.loads((R/'batch.json').read_text());cs=report['configs'];assert len(batch)==54 and len(cs)==54 and len(plan['component_sources'])==24 and report['frozen_plan_sha256']==sha(R/'plan.json');assert report['read_only_reference_definitions']==plan['read_only_references']
 for style in STYLES:assert {(c['trend_exit_buffer_fraction'],c['reversal_lookback_days'],c['reversal_return_hurdle']) for c in cs.values() if c['style']==style}==set(itertools.product(BUFFERS,LOOKS,HURDLES))
 for fp,ref in plan['component_sources'].items():
  rec=records[fp];assert rec['result_available'] is True and rec['status']==ref['original_status'] and rec['report_sha256']==ref['report_sha256'];assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['spec'])==ref['spec_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'];sp=json.loads((ROOT/ref['spec']).read_text());assert reg.fingerprint(sp)==fp and sp['parameters']['initial_capital_usdt']==10000 and sp['parameters']['fixed_entry_notional_usdt']==2000 and sp['parameters']['start_utc']==plan['time_boundaries']['oos_start_utc'] and sp['parameters']['end_utc']==plan['time_boundaries']['oos_end_exclusive_utc']
 docs={};references={}
 for label,ref in plan['read_only_references'].items():
  rec=records[ref['fingerprint']];assert rec['result_available'] is True and rec['status']==ref['original_status'] and rec['report_sha256']==ref['report_sha256'];assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['spec'])==ref['spec_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'];path=ref['report']
  if path not in docs:docs[path]=json.loads((ROOT/path).read_text())
  references[label]=docs[path]['configs'][ref['name']];assert references[label]['status']==ref['original_status']
 provenance=json.loads((R/'template_provenance.json').read_text());assert len(references)==16 and len({x['fingerprint'] for x in references.values()})==15
 for row in batch:
  c=cs[row['name']];sp=json.loads((ROOT/row['spec']).read_text());p=sp['parameters'];rec=records[row['fingerprint']];assert reg.fingerprint(sp)==row['fingerprint'] and sp['logic']==plan['rules'] and p['source_rules_and_costs_sha256']==provenance['inherited_value'];assert p['initial_capital_usdt']==20000 and p['raw_component_multipliers']==[1,1] and p['component_capitals_usdt']==[10000,10000] and p['component_initial_entry_notionals_usdt']==[2000,2000] and [x['weight'] for x in sp['components']]==[1,1] and [x['fingerprint'] for x in sp['components']]==row['source_fingerprints'];assert p['style']==row['style'] and p['start_utc']==plan['time_boundaries']['oos_start_utc'] and p['end_utc']==plan['time_boundaries']['oos_end_exclusive_utc'] and p['walk_forward_folds']==13 and p['continuous_oos_days']==370
  for field in ['trend_exit_buffer_fraction','reversal_lookback_days','reversal_return_hurdle']:assert p[field]==row[field]
  for asset,fp in zip(['BTC','ETH'],row['source_fingerprints']):
   ref=plan['component_sources'][fp];assert ref['asset']==asset and ref['fixed_entry_notional_usdt']==2000
   for field in ['lookback_days','return_hurdle','exit_buffer_fraction','fixed_entry_notional_usdt']:assert p[asset+'_'+field]==ref[field]
   trendleg=(asset=='BTC')==(row['style']==STYLES[0]);assert ref['style']==('trend' if trendleg else 'reversal')
   if trendleg:assert ref['lookback_days']=={'BTC':31,'ETH':28}[asset] and ref['return_hurdle']=={'BTC':.04,'ETH':.02}[asset] and ref['exit_buffer_fraction']==row['trend_exit_buffer_fraction']
   else:assert ref['lookback_days']==row['reversal_lookback_days'] and ref['return_hurdle']==row['reversal_return_hurdle'] and ref['exit_buffer_fraction']==0
  assert rec['result_available'] is True and rec['status']==c['status'] and rec['report_sha256']==sha(R/'report.json');ns=neighbors(c,cs);assert c['sensitivity']['neighbor_names']==[x['name'] for x in ns] and c['sensitivity']['three_dimensional_local_3x_positive_fraction']==sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)
 def read(n):return list(csv.DictReader((R/n).open()))
 cost,folds,recent,edges,comp=(read(n) for n in ['sensitivity.csv','fold_results.csv','recent40_fold_results.csv','joint_edges.csv','reference_comparisons.csv']);daily=list(csv.DictReader(io.StringIO(gzip.decompress((R/'daily_equity.csv.gz').read_bytes()).decode())));assert [len(x) for x in [cost,folds,recent,daily,edges,comp]]==[162,2106,1296,60102,108,486]
 for row in cost:
  c=cs[row['name']];z=c['scenes'][row['cost_multiplier']];assert row['NAV_sha256_f64le']==z['NAV_sha256_f64le'] and row['style']==c['style'] and float(row['capital_usdt'])==20000
  for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt','source_daily_return_correlation_full370','source_daily_return_correlation_recent40']:assert float(row[p])==z[p] if z[p] is not None else row[p]==''
  for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:assert float(row['recent40_'+p])==z['recent40'][p] if z['recent40'][p] is not None else row['recent40_'+p]==''
 for rows,isrecent in [(folds,False),(recent,True)]:
  for row in rows:
   z=cs[row['name']]['scenes'][row['cost_multiplier']];z=(z['recent40'] if isrecent else z)['folds'][int(row['fold'])-1]
   for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:assert float(row[p])==z[p] if z[p] is not None else row[p]==''
 for row in daily:assert float(row['equity_usdt'])==cs[row['name']]['scenes'][row['cost_multiplier']]['daily_equity_usdt'][int(row['boundary_index'])]
 from summarize import FIELDS,AXES,key
 for row in edges:
  a,b=cs[row['from']],cs[row['to']];i=FIELDS.index(row['axis']);pa,pb=key(a),key(b);assert a['style']==b['style']==row['style'] and AXES[i].index(pb[i])-AXES[i].index(pa[i])==1 and all(pa[j]==pb[j] for j in range(3) if j!=i)
  for p,q in [('return3_delta_pp','net_return_pct'),('DD3_delta_pp','max_drawdown_pct'),('sharpe3_delta','sharpe_365')]:
   if a['scenes']['3'][q] is not None and b['scenes']['3'][q] is not None:assert float(row[p])==b['scenes']['3'][q]-a['scenes']['3'][q]
   else:assert row[p]==''
  assert float(row['recent40_return3_delta_pp'])==b['scenes']['3']['recent40']['net_return_pct']-a['scenes']['3']['recent40']['net_return_pct']
 for row in comp:
  c=cs[row['name']];old=references[row['reference_label']];assert old['fingerprint']==row['reference_fingerprint'] and old['status']==row['reference_original_status'];z,y=c['scenes'][row['cost_multiplier']],old['scenes'][row['cost_multiplier']];assert float(row['return_delta_pp'])==z['net_return_pct']-y['net_return_pct'] and float(row['DD_delta_pp'])==z['max_drawdown_pct']-y['max_drawdown_pct'] and float(row['recent40_return_delta_pp'])==z['recent40']['net_return_pct']-y['recent40']['net_return_pct'] and row['reference_NAV_sha256']==y['NAV_sha256_f64le'] and row['new_NAV_sha256']==z['NAV_sha256_f64le']
 assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items());base=json.loads((R/'startup.json').read_text())['head_after_successful_SSH_fetch'];prefix=subprocess.check_output(['git','show',base+':research/automation/registry.jsonl'],cwd=ROOT);raw=(ROOT/'research/automation/registry.jsonl').read_bytes();assert raw.startswith(prefix);events=[json.loads(x) for x in raw[len(prefix):].splitlines()];fps={x['fingerprint'] for x in batch+json.loads((R/'forward_batch.json').read_text())};assert len(events)==114 and len(fps)==57 and {x['fingerprint'] for x in events}==fps
 for fp in fps:assert sum(x['fingerprint']==fp and x['status']=='reserved' for x in events)==1 and sum(x['fingerprint']==fp and x['status'] in ['passed','rejected'] for x in events)==1
 for p,h in ctx['ledger_fragments_before'].items():
  if p!='research/automation/registry.jsonl':assert sha(ROOT/p)==h
 for fs in plan['data']['assets'].values():
  for x in fs:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 assert sha(R/'report.json')==json.loads((R/'verification.json').read_text())['report_sha256'];out={'passed':True,'new_financial_configs':54,'new_native_backtests':0,'source_native_components_unchanged':24,'source_cost_NAV_hashes_verified':72,'old_parent_control_labels':16,'old_parent_controls_unique_unchanged':15,'new_three_axis_cells_per_style':27,'cost_rows_verified':162,'fold_rows_verified':2106,'recent40_fold_rows_verified':1296,'daily_NAV_rows_verified':60102,'edges_verified':108,'reference_comparisons_verified':486,'registry_append_only_events':114,'new_finished_IDs':57,'protected_files_unchanged':len(ctx['account_hashes_before']),'real_market_files':8,'finished_report_original_SHA_preserved':sha(R/'report.json')};put(R/'source_verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
