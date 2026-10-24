"""Verify all exact definitions,immutable old results,table attribution and ledger append."""
import csv,gzip,io,itertools,json,subprocess
from run import ROOT,R,LOOKS_BY_ASSET,NEW_EXITS,HURDLES,EXITS,sha,reg,put,grid_configs,neighbors

def main():
 plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');batch=json.loads((R/'batch.json').read_text());refs=json.loads((R/'anchors.json').read_text());grid=grid_configs(report['configs']);assert len(batch)==16 and len(refs)==32 and len(grid)==48
 assert {(c['asset'],c['lookback_days'],c['return_hurdle'],c['exit_buffer_fraction']) for c in grid.values()}=={(a,L,H,E) for a in ['BTC','ETH'] for L,H,E in itertools.product(LOOKS_BY_ASSET[a],HURDLES,EXITS)}
 assert sha(R/'engine.py')==sha(ROOT/plan['source_engine']['path'])==plan['source_engine']['sha256'];assert plan['lookback_availability']['earliest_completed_close_index']==0
 base=json.loads((ROOT/'research/experiments/20261024T124528Z/report.json').read_text())
 for row in batch:
  c=report['configs'][row['name']];spec=json.loads((ROOT/row['spec']).read_text());p=spec['parameters'];rec=records[row['fingerprint']];assert reg.fingerprint(spec)==row['fingerprint'];assert p['initial_capital_usdt']==10000 and p['fixed_entry_notional_usdt']==2000 and p['raw_entry_notional_fraction_of_initial_capital']==.2 and p['lookback_days'] in LOOKS_BY_ASSET[row['asset']] and p['exit_buffer_fraction'] in NEW_EXITS and p['exit_buffer_fraction']<=p['return_hurdle']
  name=f"perp_bufferexit_{row['asset']}_L{row['lookback_days']}_H{int(row['return_hurdle']*100):02d}_E100bp";template=json.loads((ROOT/base['configs'][name]['spec']).read_text());expected={**template['parameters'],'exit_buffer_fraction':row['exit_buffer_fraction']};assert p==expected and spec['logic']==template['logic'] and spec['family']==template['family']
  assert rec['result_available'] is True and rec['status']==c['status'] and rec['report_sha256']==sha(R/'report.json');ns=neighbors(c,grid);assert c['sensitivity']['neighbor_names']==[x['name'] for x in ns] and c['sensitivity']['local_3x_neighbor_positive_fraction']==sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)
 for name,ref in refs.items():
  assert sha(ROOT/ref['source_report'])==ref['source_report_sha256'] and sha(ROOT/ref['source_archive'])==ref['source_archive_sha256'] and sha(ROOT/ref['source_spec'])==ref['source_spec_sha256'];c=json.loads((ROOT/ref['source_report']).read_text())['configs'][name];rec=records[ref['fingerprint']];assert rec['status']==c['status']==ref['original_status'] and rec['report_sha256']==ref['source_report_sha256'];cell=report['joint_grid_sensitivity']['cells'][name];assert cell['read_only_anchor'] and cell['qualification_status']==c['status'] and c['criteria']==grid[name]['criteria']
 cost=list(csv.DictReader((R/'sensitivity.csv').open()));folds=list(csv.DictReader((R/'fold_results.csv').open()));daily=list(csv.DictReader(io.StringIO(gzip.decompress((R/'daily_equity.csv.gz').read_bytes()).decode())));edges=list(csv.DictReader((R/'joint_edges.csv').open()));capacity=list(csv.DictReader((R/'cost_capacity.csv').open()));hold=list(csv.DictReader((R/'hold_comparison.csv').open()));zero=list(csv.DictReader((R/'zeroexit_comparison.csv').open()));assert [len(x) for x in [cost,folds,daily,edges,capacity,hold,zero]]==[144,1584,15888,88,48,48,16]
 for row in cost:
  z=grid[row['name']]['scenes'][row['cost_multiplier']];assert row['NAV_sha256_f64le']==z['NAV_sha256_f64le'] and row['read_only_anchor']==str(row['name'] in refs)
  for key in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt']:assert float(row[key])==z[key]
 for row in folds:
  z=grid[row['name']]['scenes'][row['cost_multiplier']]['folds'][int(row['fold'])-1]
  for key in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:assert float(row[key])==z[key] if z[key] is not None else row[key]==''
 for row in daily:assert float(row['equity_usdt'])==report['configs'][row['name']]['scenes'][row['cost_multiplier']]['daily_equity_usdt'][int(row['boundary_index'])]
 for row in edges:
  a,b=grid[row['from']]['scenes']['3'],grid[row['to']]['scenes']['3'];assert float(row['return3_delta_pp'])==b['net_return_pct']-a['net_return_pct'] and float(row['sharpe3_delta'])==b['sharpe_365']-a['sharpe_365'] and float(row['DD3_delta_pp'])==b['max_drawdown_pct']-a['max_drawdown_pct']
 for row in zero:
  c=grid[row['name']];old=grid[row['readonly_zeroexit_name']];assert (c['asset'],c['lookback_days'],c['return_hurdle'])==(old['asset'],old['lookback_days'],old['return_hurdle']) and old['exit_buffer_fraction']==0;assert float(row['return3_delta_pp'])==c['scenes']['3']['net_return_pct']-old['scenes']['3']['net_return_pct'] and int(row['positive_folds1_delta'])==c['positive_folds_1x']-old['positive_folds_1x']
 prior=list(csv.DictReader((R/'prior_edge_comparison.csv').open()));assert len(prior)==16
 for row in prior:
  c=grid[row['name']];old=grid[row['readonly_prior_upper_edge_name']];assert (c['asset'],c['lookback_days'],c['return_hurdle'])==(old['asset'],old['lookback_days'],old['return_hurdle']) and old['exit_buffer_fraction']==.01;assert float(row['return3_delta_pp'])==c['scenes']['3']['net_return_pct']-old['scenes']['3']['net_return_pct'] and int(row['positive_folds1_delta'])==c['positive_folds_1x']-old['positive_folds_1x']
 for ref in plan['read_only_hold_references'].values():assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'] and records[ref['fingerprint']]['status']==ref['original_status'] and records[ref['fingerprint']]['report_sha256']==ref['report_sha256']
 for row in hold:
  z=grid[row['name']]['scenes'][row['cost_multiplier']];ref=plan['read_only_hold_references'][row['asset']];h=json.loads((ROOT/ref['report']).read_text())['configs'][ref['name']]['scenes'][row['cost_multiplier']];assert float(row['excess_return_vs_hold_pp'])==z['net_return_pct']-h['net_return_pct'] and float(row['hold_DD_pct'])==h['max_drawdown_pct']
 assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items());gitbase=json.loads((R/'startup.json').read_text())['head_after_successful_SSH_fetch'];prefix=subprocess.check_output(['git','show',gitbase+':research/automation/registry.jsonl'],cwd=ROOT);current=(ROOT/'research/automation/registry.jsonl').read_bytes();assert current.startswith(prefix);new=[json.loads(x) for x in current[len(prefix):].splitlines()];allbatch=batch+json.loads((R/'forward_batch.json').read_text());fps={x['fingerprint'] for x in allbatch};assert len(new)==38 and len(fps)==19 and {x['fingerprint'] for x in new}==fps
 for fp in fps:assert sum(x['fingerprint']==fp and x['status']=='reserved' for x in new)==1 and sum(x['fingerprint']==fp and x['status'] in ['passed','rejected'] for x in new)==1
 for path,h in ctx['ledger_fragments_before'].items():
  if path!='research/automation/registry.jsonl':assert sha(ROOT/path)==h
 for files in plan['data']['assets'].values():
  for x in files:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 assert sha(R/'report.json')==json.loads((R/'verification.json').read_text())['report_sha256'];out={'passed':True,'new_financial_configs':16,'readonly_old_results_unchanged':32,'unchanged_source_engine':True,'full_joint_grid_configs':48,'cost_rows_verified':144,'fold_rows_verified':1584,'new_daily_NAV_rows_verified':15888,'edges_verified':88,'prior_edge_comparisons_verified':16,'append_only_registry_events':38,'new_finished_IDs':19,'protected_files_unchanged':len(ctx['account_hashes_before']),'real_market_files':8,'finished_report_original_SHA_preserved':sha(R/'report.json')};put(R/'source_verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
