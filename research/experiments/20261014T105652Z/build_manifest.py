#!/usr/bin/env python3
"""Write compact provenance/hashes after all immutable experiment artifacts are finalized."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());frag=R/'registry_records.jsonl'
 if not frag.is_file():raise SystemExit('registry sidecar must be complete before data manifest')
 files=['plan.json','batch.json','reserve.json','exchange_info_raw.json','exchange_info_BTCUSDT_response.json','exchange_info_ETHUSDT_response.json','exchange_filters.json','evaluate.py','freeze.py','merge_exchange_info.py','audit.py','write_report.py','finish.py','reproduce.py','build_manifest.py','evaluate_stdout.log','evaluation_attempts.jsonl','setup_failure.log','audit.log','finish.json','finish.log','reproduce.log','report.json','result.md','fold_results.csv','cost_scenarios.csv','weekday_daily_returns.csv','sensitivity_surface.svg','trades.csv.gz','daily_equity.csv.gz','registry_records.jsonl']
 artifacts={p:{'sha256':sha(R/p),'bytes':(R/p).stat().st_size} for p in files}
 codes=['freeze.py','evaluate.py','audit.py','write_report.py','finish.py','reproduce.py','merge_exchange_info.py','build_manifest.py']
 rows=[json.loads(x) for x in frag.read_text().splitlines() if x.strip()]
 get_responses={}
 for asset,sym in [('BTC','BTCUSDT'),('ETH','ETHUSDT')]:
  p=R/f'exchange_info_{sym}_response.json';body=json.loads(p.read_text())
  get_responses[sym]={'method':'GET','url':f'https://data-api.binance.vision/api/v3/exchangeInfo?symbol={sym}','sha256':sha(p),'bytes':p.stat().st_size,'server_time_ms':body.get('serverTime'),'returned_symbol':body['symbols'][0]['symbol']}
 doc={'round':R.name,'plan_sha256':sha(R/'plan.json'),'report_sha256':sha(R/'report.json'),'exchange_info_raw_sha256':sha(R/'exchange_info_raw.json'),'exchange_info_get_responses':get_responses,'exchange_filters_sha256':sha(R/'exchange_filters.json'),'inputs':report['input_data'],'code_sha256':{p:sha(R/p) for p in codes},'artifacts':artifacts,'registry_fragment':{'path':'research/experiments/'+R.name+'/registry_records.jsonl','sha256':sha(frag),'events':len(rows),'reserve_events':sum(x['status']=='reserved' for x in rows),'finish_events':sum(x['status'] in ('passed','rejected','blocked','abandoned') for x in rows)}}
 (R/'data_manifest.json').write_text(json.dumps(doc,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
 print('manifest written',sha(R/'data_manifest.json'),'registry-events',len(rows))
if __name__=='__main__':main()
