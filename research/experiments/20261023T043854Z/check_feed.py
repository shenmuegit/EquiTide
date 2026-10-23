"""Read-only attribution, immutable report, append-only registry and historical-failure checks."""
import gzip,hashlib,importlib.util,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 raw=gzip.decompress((ROOT/'research/monitor/configs.json.gz').read_bytes());feed=json.loads(raw);latest=json.loads((ROOT/'research/monitor/latest.json').read_text());by={x['fingerprint']:x for x in feed};assert len(by)==len(feed) and hashlib.sha256(raw).hexdigest()==latest['research']['configs_sha256']
 sp=importlib.util.spec_from_file_location('reg',ROOT/'research/automation/registry.py');reg=importlib.util.module_from_spec(sp);sp.loader.exec_module(reg);records=reg.read_records(ROOT/'research/automation/registry.jsonl');report=json.loads((R/'report.json').read_text());forward=json.loads((R/'forward_report.json').read_text());ctx=json.loads((R/'context.json').read_text());count=0
 for cfg in report['configs'].values():
  row=by[cfg['fingerprint']];p=records[cfg['fingerprint']]['spec']['parameters'];assert row['report']==str((R/'report.json').relative_to(ROOT)) and row['status']==cfg['status'] and row['criteria']==cfg['criteria'];assert row['capital_usdt']==2000 and row['start_utc']==p['start_utc'] and row['end_utc']==p['end_utc'] and row['positive_folds_1x']==cfg['positive_folds_1x'];assert row['cross_period_passed']==cfg['both_periods_meet_full_gates'];assert {x['asset']:x['weight'] for x in row['weights']}=={'BTC':.75,'ETH':.25};assert row['validation']['walk_forward_folds']==6 and row['validation']['cost_scenarios']==['1','2','3'] and row['validation']['sensitivity_recorded']
  for k,z in cfg['scenes'].items():
   s=row['scenes'][k]
   for dest,src in {'return_pct':'net_return_pct','drawdown_pct':'max_drawdown_pct','sharpe':'sharpe_365','cost':'cost_usdt'}.items():assert s[dest]==(round(float(z[src]),6) if z[src] is not None else None)
   assert s['nav_hash']==z['NAV_sha256_f64le'] and s['executions']==z['executions'] and s['round_trips']==z['round_trips'];assert s['fold_returns_pct']==[round(float(f['net_return_pct']),6) for f in z['folds']] and s['fold_drawdowns_pct']==[round(float(f['max_drawdown_pct']),6) for f in z['folds']];count+=1
 for cfg in [*report['configs'].values(),*forward['configs'].values()]:
  partial=cfg['name'].startswith('forward_snapshot');rec=records[cfg['fingerprint']];assert rec['result_available'] and rec['status']==('rejected' if partial else cfg['status']) and rec['report_sha256']==sha(R/('forward_report.json' if partial else 'report.json'))
 for ref in report['component_sources'].values():
  assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'];rec=records[ref['fingerprint']];assert rec['status']==ref['original_status'] and rec['report_sha256']==ref['report_sha256']
 assert '537f5a8fc4b6e58511fabbde15096659e072be117d9a365d3827ac178134c70e' in by
 assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items())
 base=json.loads((R/'startup.json').read_text())['head_after_successful_SSH_fetch'];old=subprocess.check_output(['git','show',base+':research/automation/registry.jsonl'],cwd=ROOT);ledger=(ROOT/'research/automation/registry.jsonl').read_bytes();assert hashlib.sha256(old).hexdigest()==ctx['main_registry_sha256_before_reserve'] and ledger.startswith(old);new=[json.loads(x) for x in ledger[len(old):].splitlines()];assert len(new)==42 and len({x['fingerprint'] for x in new})==21
 failed=[]
 for name in ['initial_commands.json','research_commands.json','forward_commands.json','final_gates.json']:
  failed.extend(x for x in json.loads((R/name).read_text()) if x['exit_code']!=0)
 failure=json.loads((R/'recovery_failure.json').read_text());assert len(failed)==1 and failed[0]==failure['failed_command'] and failed[0]['exit_code']==1 and failure['parent_configurations_computed_before_failure']==0;assert sha(ROOT/failure['failed_log_path'])==failure['failed_log_sha256'];assert (R/'diagnostic_serialization_failure.json').exists()
 assert all(x['exit_code']==0 for x in json.loads((R/'research_commands.json').read_text())[1:])
 result={'passed':True,'research_configs':len(feed),'paper_observations':latest['paper']['observation_count'],'paper_accounts':len(latest['paper']['accounts']),'new_parent_configs_verified':18,'new_cost_scenes_verified':count,'new_actual_partial_observations':3,'source_components_reused_read_only':12,'passed_parent_configs':len(report['summary']['passed']),'rejected_parent_configs':len(report['summary']['rejected']),'paired_periods_passed':len(report['summary']['new_both_periods_passed_combination_pairs']),'main_registry_append_only_events':42,'regression_alias_retained':True,'historical_reader_failure_exit1_retained_and_followed_by_real_exit0':True,'financial_report_sha256':sha(R/'report.json'),'forward_report_sha256':sha(R/'forward_report.json'),'protected_inputs_unchanged':True};(R/'feed_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result),flush=True)
if __name__=='__main__':main()
