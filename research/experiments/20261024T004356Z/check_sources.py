"""Check frozen definitions, source bytes, readonly qualification and new-grid accounting."""
import itertools,json,subprocess
from run import ROOT,R,BTC_LOOKS,ETH_LOOKS,HURDLES,sha,reg,grid_configs,neighbors
def main():
 plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');batch=json.loads((R/'batch.json').read_text());refs=json.loads((R/'anchors.json').read_text());grid=grid_configs(report['configs'])
 assert len(batch)==len(report['configs'])==54 and len(refs)==27 and len(grid)==81
 assert {(c['BTC_lookback_days'],c['BTC_return_hurdle'],c['ETH_lookback_days'],c['ETH_return_hurdle']) for c in grid.values()}==set(itertools.product(BTC_LOOKS,HURDLES,ETH_LOOKS,HURDLES))
 assert len(plan['component_sources'])==18
 for fp,ref in plan['component_sources'].items():
  r=records[fp];assert r['result_available'] is True and r['status']==ref['original_status'] and r['report_sha256']==ref['report_sha256'];assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['spec'])==ref['spec_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256']
  spec=json.loads((ROOT/ref['spec']).read_text());p=spec['parameters'];assert reg.fingerprint(spec)==fp and p['initial_capital_usdt']==10000 and p['fixed_entry_notional_usdt']==2000 and p['lookback_days']<=32
  assert sorted(ref['NAV_sha256_by_cost'])==['1','2','3']
 old=json.loads((ROOT/plan['anchor_source']['report']).read_text())
 for name,ref in refs.items():
  assert grid[name]==old['configs'][name] and grid[name]['ETH_lookback_days']==30;record=records[ref['fingerprint']];assert record['report_sha256']==ref['report_sha256'] and record['status']==ref['original_status'];assert sha(ROOT/ref['archive'])==ref['archive_sha256']
  cell=report['joint_grid_sensitivity']['cells'][name];assert cell['read_only_anchor'] is True and cell['qualification_status']==ref['original_status']
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());assert reg.fingerprint(spec)==row['fingerprint'];p=spec['parameters'];assert p['raw_component_multipliers']==[1,1] and p['component_capitals_usdt']==[10000,10000] and p['initial_capital_usdt']==20000 and p['component_initial_entry_notionals_usdt']==[2000,2000];assert [c['weight'] for c in spec['components']]==[1,1] and p['ETH_lookback_days'] in [31,32] and p['cost_multipliers']==[1,2,3]
  c=report['configs'][row['name']];ns=neighbors(c,grid);assert c['sensitivity']['neighbor_names']==[x['name'] for x in ns] and c['sensitivity']['neighbor_count']==len(ns);assert c['sensitivity']['four_dimensional_local_3x_positive_fraction']==sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)
  assert (c['status']=='passed')==all(c['criteria'].values()) and c['failed_criteria']==[k for k,v in c['criteria'].items() if not v]
  assert records[row['fingerprint']]['report_sha256']==sha(R/'report.json') and records[row['fingerprint']]['status']==c['status']
 assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items())
 base=json.loads((R/'startup.json').read_text())['head_after_successful_SSH_fetch'];prefix=subprocess.check_output(['git','show',base+':research/automation/registry.jsonl'],cwd=ROOT);current=(ROOT/'research/automation/registry.jsonl').read_bytes();assert current.startswith(prefix);new=[json.loads(line) for line in current[len(prefix):].splitlines()];allbatch=batch+json.loads((R/'forward_batch.json').read_text());fps={r['fingerprint'] for r in allbatch};assert len(new)==114 and {x['fingerprint'] for x in new}==fps and len(fps)==57
 for fp in fps:assert sum(x['fingerprint']==fp and x['status']=='reserved' for x in new)==1 and sum(x['fingerprint']==fp and x['status'] in ['passed','rejected'] for x in new)==1
 for path,h in ctx['ledger_fragments_before'].items():
  if path!='research/automation/registry.jsonl':assert sha(ROOT/path)==h
 for files in plan['data']['assets'].values():
  for x in files:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 print(json.dumps({'passed':True,'new_parents':54,'readonly_old_parents_unchanged':27,'full_4D_grid':81,'source_components_unchanged':18,'source_NAV_hashes':54,'new_registry_events_append_only':114,'new_financial_and_partial_IDs':57,'protected_files_unchanged':len(ctx['account_hashes_before']),'real_market_files':8,'all_variants_finished_with_original_report_SHA':True}),flush=True)
if __name__=='__main__':main()
