import gzip,hashlib,json,subprocess
from common import *
raw=gzip.decompress((ROOT/'research/monitor/configs.json.gz').read_bytes());feed=json.loads(raw);latest=json.loads((ROOT/'research/monitor/latest.json').read_text());by={x['fingerprint']:x for x in feed};assert len(by)==len(feed) and hashlib.sha256(raw).hexdigest()==latest['research']['configs_sha256'];records=reg.read_records(ROOT/'research/automation/registry.jsonl');r=json.loads((R/'report.json').read_text());scenes=0
for c in r['configs'].values():
 x=by[c['fingerprint']];p=records[c['fingerprint']]['spec']['parameters'];assert x['report']==rel(R/'report.json') and x['status']==c['status'] and x['criteria']==c['criteria'] and x['capital_usdt']==c['capital_usdt'] and x['start_utc']==p['start_utc'] and x['end_utc']==p['end_utc'] and x['validation']['walk_forward_folds']==13 and x['validation']['sensitivity_recorded']
 for k,s in c['scenes'].items():
  z=x['scenes'][k]
  for a,b in {'return_pct':'net_return_pct','drawdown_pct':'max_drawdown_pct','sharpe':'sharpe_365','cost':'cost_usdt'}.items():assert z[a]==(round(float(s[b]),6) if s[b] is not None else None)
  assert z['nav_hash']==s['NAV_sha256_f64le'] and z['executions']==s['executions'] and z['round_trips']==s['round_trips'] and z['fold_returns_pct']==[round(float(f['net_return_pct']),6) for f in s['folds']];scenes+=1
base=json.loads((R/'startup.json').read_text())['base_commit'];old=json.loads(gzip.decompress(subprocess.check_output(['git','show',base+':research/monitor/configs.json.gz'],cwd=ROOT)))
for x in old:assert by[x['fingerprint']]==x
assert len(feed)==len(old)+10 and scenes==30
for doc,path in [(r,R/'report.json'),(json.loads((R/'forward_report.json').read_text()),R/'forward_report.json'),(json.loads((R/'candidate_observation/report.json').read_text()),R/'candidate_observation/report.json')]:
 for c in doc['configs'].values():z=records[c['fingerprint']];assert z['result_available'] and z['status']==c['status'] and z['report_sha256']==sha(path)
ctx=json.loads((R/'context.json').read_text());assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items())
put(R/'feed_verification.json',{'passed':True,'research_configs':len(feed),'historical_rows_identical':len(old),'new_actual_financial_configs':10,'new_candidate_configs':10,'new_benchmark_configs':0,'new_cost_scenes':30,'passed_new_candidates':len(r['summary']['passed']),'rejected_new_candidates':len(r['summary']['rejected']),'paper_accounts':len(latest['paper']['accounts']),'paper_observations':latest['paper']['observation_count'],'new_partial_observations':6,'protected_inputs_unchanged':True,'financial_report_sha256':sha(R/'report.json')});print('PASS10 new rows/30 scenes and every oldmonitorrow unchanged')
