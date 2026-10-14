#!/usr/bin/env python3
"""Create hashes and provenance after result and registry fragments are finalized."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());frag=R/'registry_records.jsonl'
 if not frag.exists():raise SystemExit('registry finish sidecar not complete')
 files=['plan.json','batch.json','reserve.json','exchange_info_raw.json','exchange_filters.json','freeze.py','evaluate.py','audit.py','write_report.py','finish.py','reproduce.py','build_manifest.py','evaluate_stdout.log','implementation_attempts.jsonl','audit_failure.log','audit.log','finish.json','finish.log','reproduce.log','report.json','result.md','sensitivity_surface.svg','fold_results.csv','cost_scenarios.csv','trades.csv.gz','decisions.csv.gz','daily_equity.csv.gz','registry_records.jsonl']
 artifacts={p:{'sha256':sha(R/p),'bytes':(R/p).stat().st_size} for p in files}
 codes=['freeze.py','evaluate.py','audit.py','write_report.py','finish.py','reproduce.py','build_manifest.py']
 rows=[json.loads(x) for x in frag.read_text().splitlines() if x.strip()]
 doc={'round':R.name,'plan_sha256':sha(R/'plan.json'),'report_sha256':sha(R/'report.json'),'exchange_info_raw_sha256':sha(R/'exchange_info_raw.json'),'exchange_filters_sha256':sha(R/'exchange_filters.json'),'input_data':report['input_data'],'code_sha256':{p:sha(R/p) for p in codes},'artifacts':artifacts,'registry_fragment':{'path':'research/experiments/'+R.name+'/registry_records.jsonl','sha256':sha(frag),'events':len(rows),'reserve_events':sum(x['status']=='reserved' for x in rows),'finish_events':sum(x['status'] in ('passed','rejected','blocked','abandoned') for x in rows)}}
 (R/'data_manifest.json').write_text(json.dumps(doc,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
 print('data manifest sha256',sha(R/'data_manifest.json'),'registry events',len(rows))
if __name__=='__main__':main()
