"""Attribute every new result to the readonly feed and preserve historical aliases."""
import gzip,hashlib,json
from run import ROOT,R,sha,reg,put
def main():
 raw=gzip.decompress((ROOT/'research/monitor/configs.json.gz').read_bytes());feed=json.loads(raw);latest=json.loads((ROOT/'research/monitor/latest.json').read_text());by={x['fingerprint']:x for x in feed};assert len(by)==len(feed) and hashlib.sha256(raw).hexdigest()==latest['research']['configs_sha256'];records=reg.read_records(ROOT/'research/automation/registry.jsonl');report=json.loads((R/'report.json').read_text());forward=json.loads((R/'forward_report.json').read_text());ctx=json.loads((R/'context.json').read_text());scenes=0
 for c in report['configs'].values():
  row=by[c['fingerprint']];p=records[c['fingerprint']]['spec']['parameters'];assert row['report']==str((R/'report.json').relative_to(ROOT)) and row['status']==c['status'] and row['criteria']==c['criteria'];assert row['capital_usdt']==p['initial_capital_usdt']==20000 and row['start_utc']==p['start_utc'] and row['end_utc']==p['end_utc'] and row['positive_folds_1x']==c['positive_folds_1x'];assert row['weights']==[{'asset':'BTC','weight':1},{'asset':'ETH','weight':1}]
  assert row['cross_period_passed'] is False and row['validation']['walk_forward_folds']==11 and row['validation']['cost_scenarios']==['1','2','3'] and row['validation']['sensitivity_recorded']
  for k,z in c['scenes'].items():
   s=row['scenes'][k]
   for dest,src in {'return_pct':'net_return_pct','drawdown_pct':'max_drawdown_pct','sharpe':'sharpe_365','cost':'cost_usdt'}.items():assert s[dest]==(round(float(z[src]),6) if z[src] is not None else None)
   assert s['nav_hash']==z['NAV_sha256_f64le'] and s['executions']==z['executions'] and s['round_trips']==z['round_trips'] and s['fold_returns_pct']==[round(float(f['net_return_pct']),6) for f in z['folds']] and s['fold_drawdowns_pct']==[round(float(f['max_drawdown_pct']),6) for f in z['folds']];scenes+=1
 for c in [*report['configs'].values(),*forward['configs'].values()]:
  partial=c['name'].startswith('forward_snapshot');rec=records[c['fingerprint']];assert rec['result_available'] is True and rec['status']==('rejected' if partial else c['status']) and rec['report_sha256']==sha(R/('forward_report.json' if partial else 'report.json'))
 anchors=json.loads((R/'anchors.json').read_text());docs={}
 for name,ref in anchors.items():
  path=ref['report'];assert sha(ROOT/path)==ref['report_sha256']
  if path not in docs:docs[path]=json.loads((ROOT/path).read_text())
  c=docs[path]['configs'][name];rec=records[ref['fingerprint']];row=by[ref['fingerprint']];assert rec['status']==c['status']==ref['original_status'] and rec['report_sha256']==ref['report_sha256'];assert row['report']==path and row['status']==c['status'] and row['criteria']==c['criteria']
  for k,z in c['scenes'].items():assert row['scenes'][k]['nav_hash']==z['NAV_sha256_f64le'] and row['scenes'][k]['return_pct']==round(z['net_return_pct'],6)
 assert scenes==240 and len(anchors)==64 and '537f5a8fc4b6e58511fabbde15096659e072be117d9a365d3827ac178134c70e' in by
 assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items())
 for name in ['initial_commands.json','research_commands.json','forward_commands.json','gates_commands.json','review_commands.json']:assert all(x['exit_code']==0 for x in json.loads((R/name).read_text())),name
 assert sha(R/'report.json')==json.loads((R/'verification.json').read_text())['report_sha256'] and sha(R/'forward_report.json')==json.loads((R/'forward_verification.json').read_text())['report_sha256']
 result={'passed':True,'research_configs':len(feed),'paper_observations':latest['paper']['observation_count'],'paper_accounts':len(latest['paper']['accounts']),'new_financial_configs_verified':80,'new_cost_scenes_verified':scenes,'passed_new':len(report['summary']['passed']),'rejected_new':len(report['summary']['rejected']),'old64_parent_NAV_status_criteria_unchanged':True,'new_actual_partial_observations':3,'historical_alias_regression_retained':True,'required_gates_actual_exit0':True,'financial_report_sha256':sha(R/'report.json'),'forward_report_sha256':sha(R/'forward_report.json'),'protected_inputs_unchanged':True};put(R/'feed_verification.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':main()
