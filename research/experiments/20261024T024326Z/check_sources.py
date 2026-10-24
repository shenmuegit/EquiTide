"""Readonly finished-result/CSV/source audit plus separate old-hold comparisons."""
import csv,gzip,io,itertools,json,subprocess
from pathlib import Path
from run import ROOT,R,HURDLES,EXITS,sha,reg,put,grid_configs,neighbors
def main():
 report=json.loads((R/'report.json').read_text());report_sha=sha(R/'report.json');plan=json.loads((R/'plan.json').read_text());ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');batch=json.loads((R/'batch.json').read_text());grid=grid_configs(report['configs']);refs=json.loads((R/'anchors.json').read_text())
 assert len(batch)==18 and len(grid)==24 and len(refs)==6
 assert {(c['asset'],c['return_hurdle'],c['exit_buffer_fraction']) for c in grid.values()}==set(itertools.product(['BTC','ETH'],HURDLES,EXITS))
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());c=report['configs'][row['name']];p=spec['parameters'];rec=records[row['fingerprint']];assert reg.fingerprint(spec)==row['fingerprint'] and p['lookback_days']==30 and p['initial_capital_usdt']==10000 and p['fixed_entry_notional_usdt']==2000 and p['raw_entry_notional_fraction_of_initial_capital']==.2 and p['exit_buffer_fraction'] in EXITS[1:] and p['exit_buffer_fraction']<=p['return_hurdle']
  assert 'exit_ROC' not in p and rec['result_available'] is True and rec['status']==c['status']=='rejected' and rec['report_sha256']==report_sha
  ns=neighbors(c,grid);assert c['sensitivity']['neighbor_names']==[x['name'] for x in ns] and c['sensitivity']['local_3x_neighbor_positive_fraction']==sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)
 source=plan['anchor_source'];assert sha(ROOT/source['report'])==source['report_sha256'];old=json.loads((ROOT/source['report']).read_text())
 for name,ref in refs.items():
  c=old['configs'][name];rec=records[ref['fingerprint']];assert c['lookback_days']==30 and c['status']==ref['original_status']==rec['status'] and rec['report_sha256']==source['report_sha256'];assert sha(ROOT/ref['source_archive'])==ref['source_archive_sha256'] and sha(ROOT/ref['source_spec'])==ref['source_spec_sha256'];cell=report['joint_grid_sensitivity']['cells'][name];assert cell['read_only_anchor'] is True and cell['qualification_status']==c['status']
 cost=list(csv.DictReader((R/'sensitivity.csv').open()));folds=list(csv.DictReader((R/'fold_results.csv').open()));daily=list(csv.DictReader(io.StringIO(gzip.decompress((R/'daily_equity.csv.gz').read_bytes()).decode())));edges=list(csv.DictReader((R/'joint_edges.csv').open()));assert len(cost)==72 and len(folds)==792 and len(daily)==17874 and len(edges)==34
 for row in cost:
  c=grid[row['name']];z=c['scenes'][row['cost_multiplier']];assert row['NAV_sha256_f64le']==z['NAV_sha256_f64le'] and row['read_only_anchor']==str(c.get('read_only_anchor',False))
  for key in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt']:assert float(row[key])==z[key]
 for row in folds:
  z=grid[row['name']]['scenes'][row['cost_multiplier']]['folds'][int(row['fold'])-1]
  for key in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:assert float(row[key])==z[key] if z[key] is not None else row[key]==''
 for row in daily:assert float(row['equity_usdt'])==report['configs'][row['name']]['scenes'][row['cost_multiplier']]['daily_equity_usdt'][int(row['boundary_index'])]
 # Numerical hold/cash comparisons stay separate; the finished main report is immutable.
 hold_returns={};hold_rows=[]
 for asset,ref in plan['read_only_hold_references'].items():
  assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'];doc=json.loads((ROOT/ref['report']).read_text());hold=doc['configs'][ref['name']];rec=records[ref['fingerprint']];assert rec['report_sha256']==ref['report_sha256'] and rec['status']==ref['original_status'];hp=rec['spec']['parameters'];assert hp['initial_capital_usdt']==10000 and hp['fixed_entry_notional_usdt']==2000 and hp['start_utc']==report['time_boundaries']['oos_start_utc'] and hp['end_utc']==report['time_boundaries']['oos_end_exclusive_utc'];hold_returns[asset]={k:z['net_return_pct'] for k,z in hold['scenes'].items()}
  for c in report['configs'].values():
   if c['asset']!=asset:continue
   for k,z in c['scenes'].items():hold_rows.append({'name':c['name'],'asset':asset,'cost_multiplier':int(k),'new_net_return_pct':z['net_return_pct'],'readonly_hold_net_return_pct':hold_returns[asset][k],'net_return_advantage_pp':z['net_return_pct']-hold_returns[asset][k],'cash_analytic_net_return_pct':0})
 buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=list(hold_rows[0]),lineterminator='\n');w.writeheader();w.writerows(hold_rows);(R/'hold_comparison.csv').write_text(buf.getvalue());put(R/'benchmark_comparison.json',{'finished_main_report_sha256_preserved':report_sha,'reference_policy':'Read existing same10000collateral/2000fixedentry constantlong books;no new backtest/reservation','reference_returns_by_asset_and_cost':hold_returns,'new_vs_old_comparison_rows':len(hold_rows),'cash_analytic_return_pct':0})
 assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items());base=json.loads((R/'startup.json').read_text())['head_after_successful_SSH_fetch'];prefix=subprocess.check_output(['git','show',base+':research/automation/registry.jsonl'],cwd=ROOT);current=(ROOT/'research/automation/registry.jsonl').read_bytes();assert current.startswith(prefix);new=[json.loads(line) for line in current[len(prefix):].splitlines()];allbatch=batch+json.loads((R/'forward_batch.json').read_text());fps={r['fingerprint'] for r in allbatch};assert len(new)==42 and {x['fingerprint'] for x in new}==fps and len(fps)==21
 for fp in fps:assert sum(x['fingerprint']==fp and x['status']=='reserved' for x in new)==1 and sum(x['fingerprint']==fp and x['status'] in ['passed','rejected'] for x in new)==1
 for path,h in ctx['ledger_fragments_before'].items():
  if path!='research/automation/registry.jsonl':assert sha(ROOT/path)==h
 for files in plan['data']['assets'].values():
  for x in files:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 # Readonly source parent results remain unrelated to this component-only batch.
 parents=ROOT/'research/experiments/20261024T004356Z/report.json';oldparents=json.loads(parents.read_text())
 for name in oldparents['summary']['passed']:
  c=oldparents['configs'][name];assert records[c['fingerprint']]['status']=='passed' and records[c['fingerprint']]['report_sha256']==sha(parents)
 assert sha(R/'report.json')==report_sha==json.loads((R/'verification.json').read_text())['report_sha256']
 proof={'passed':True,'new_financial_configs':18,'readonly_zero_exit_anchors_unchanged':6,'old_constant_long_references_not_rerun':2,'prior18qualified_parents_unchanged':True,'full_joint_grid_configs':24,'cost_rows_verified':72,'fold_rows_verified':792,'daily_NAV_rows_verified':17874,'new_registry_append_only_events':42,'new_financial_and_partial_IDs':21,'protected_files_unchanged':len(ctx['account_hashes_before']),'real_market_files':8,'finished_report_original_bytes_preserved':report_sha,'old_hold_numeric_comparison_rows':54};put(R/'source_verification.json',proof);print(json.dumps(proof),flush=True)
if __name__=='__main__':main()
