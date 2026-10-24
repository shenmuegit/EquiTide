"""Check frozen definitions, source bytes, readonly qualification and new-grid accounting."""
import itertools,json,subprocess
from run import ROOT,R,BTC_LOOKS,ETH_LOOKS,HURDLES,sha,reg,put,grid_configs,neighbors
def main():
 plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');batch=json.loads((R/'batch.json').read_text());refs=json.loads((R/'anchors.json').read_text());grid=grid_configs(report['configs'])
 assert len(batch)==len(report['configs'])==198 and len(refs)==27 and len(grid)==225
 assert {(c['BTC_lookback_days'],c['BTC_return_hurdle'],c['ETH_lookback_days'],c['ETH_return_hurdle']) for c in grid.values()}==set(itertools.product(BTC_LOOKS,HURDLES,ETH_LOOKS,HURDLES))
 assert len(plan['component_sources'])==30
 for fp,ref in plan['component_sources'].items():
  r=records[fp];assert r['result_available'] is True and r['status']==ref['original_status'] and r['report_sha256']==ref['report_sha256'];assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['spec'])==ref['spec_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256']
  spec=json.loads((ROOT/ref['spec']).read_text());p=spec['parameters'];assert reg.fingerprint(spec)==fp and p['initial_capital_usdt']==10000 and p['fixed_entry_notional_usdt']==2000 and p['lookback_days']<=32
  assert sorted(ref['NAV_sha256_by_cost'])==['1','2','3']
 docs={}
 for name,ref in refs.items():
  path=ref['report'];assert sha(ROOT/path)==ref['report_sha256']
  if path not in docs:docs[path]=json.loads((ROOT/path).read_text())
  original=docs[path]['configs'][name];assert grid[name]==original;record=records[ref['fingerprint']];assert record['report_sha256']==ref['report_sha256'] and record['status']==ref['original_status'];assert sha(ROOT/ref['archive'])==ref['archive_sha256'];cell=report['joint_grid_sensitivity']['cells'][name];assert cell['read_only_anchor'] is True and cell['qualification_status']==ref['original_status']
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());assert reg.fingerprint(spec)==row['fingerprint'];p=spec['parameters'];assert p['raw_component_multipliers']==[1,1] and p['component_capitals_usdt']==[10000,10000] and p['initial_capital_usdt']==20000 and p['component_initial_entry_notionals_usdt']==[2000,2000];assert [c['weight'] for c in spec['components']]==[1,1] and p['ETH_lookback_days'] in ETH_LOOKS and p['BTC_lookback_days'] in BTC_LOOKS and p['cost_multipliers']==[1,2,3]
  c=report['configs'][row['name']];ns=neighbors(c,grid);assert c['sensitivity']['neighbor_names']==[x['name'] for x in ns] and c['sensitivity']['neighbor_count']==len(ns);assert c['sensitivity']['four_dimensional_local_3x_positive_fraction']==sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)
  assert (c['status']=='passed')==all(c['criteria'].values()) and c['failed_criteria']==[k for k,v in c['criteria'].items() if not v]
  assert records[row['fingerprint']]['report_sha256']==sha(R/'report.json') and records[row['fingerprint']]['status']==c['status']
 assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items())
 base=json.loads((R/'startup.json').read_text())['head_after_successful_SSH_fetch'];prefix=subprocess.check_output(['git','show',base+':research/automation/registry.jsonl'],cwd=ROOT);current=(ROOT/'research/automation/registry.jsonl').read_bytes();assert current.startswith(prefix);new=[json.loads(line) for line in current[len(prefix):].splitlines()];allbatch=batch+json.loads((R/'forward_batch.json').read_text());fps={r['fingerprint'] for r in allbatch};assert len(new)==402 and {x['fingerprint'] for x in new}==fps and len(fps)==201
 for fp in fps:assert sum(x['fingerprint']==fp and x['status']=='reserved' for x in new)==1 and sum(x['fingerprint']==fp and x['status'] in ['passed','rejected'] for x in new)==1
 for path,h in ctx['ledger_fragments_before'].items():
  if path!='research/automation/registry.jsonl':assert sha(ROOT/path)==h
 for files in plan['data']['assets'].values():
  for x in files:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 import csv,gzip,io
 cost=list(csv.DictReader((R/'sensitivity.csv').open()));folds=list(csv.DictReader((R/'fold_results.csv').open()));daily=list(csv.DictReader(io.StringIO(gzip.decompress((R/'daily_equity.csv.gz').read_bytes()).decode())));edges=list(csv.DictReader((R/'joint_edges.csv').open()));assert len(cost)==675 and len(folds)==7425 and len(daily)==196614 and len(edges)==660
 for row in cost:
  z=grid[row['name']]['scenes'][row['cost_multiplier']];assert row['NAV_sha256_f64le']==z['NAV_sha256_f64le']
  for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt']:assert float(row[p])==z[p]
 for row in folds:
  z=grid[row['name']]['scenes'][row['cost_multiplier']]['folds'][int(row['fold'])-1]
  for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:assert float(row[p])==z[p] if z[p] is not None else row[p]==''
 for row in daily:assert float(row['equity_usdt'])==report['configs'][row['name']]['scenes'][row['cost_multiplier']]['daily_equity_usdt'][int(row['boundary_index'])]
 assert sha(R/'report.json')==json.loads((R/'verification.json').read_text())['report_sha256']
 out={'passed':True,'new_parents':198,'readonly_old_parents_unchanged':27,'full_4D_grid':225,'source_components_unchanged':30,'source_NAV_hashes':90,'new_registry_events_append_only':402,'new_financial_and_partial_IDs':201,'protected_files_unchanged':len(ctx['account_hashes_before']),'real_market_files':8,'all_variants_finished_with_original_report_SHA':True,'cost_rows_verified':675,'fold_rows_verified':7425,'new_daily_NAV_rows_verified':196614,'edges_verified':660,'finished_report_sha256':sha(R/'report.json')}
 put(R/'source_verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
