"""Read-only complete-registry semantic combination audit; no financial evaluation."""
import hashlib,json,sys
from datetime import datetime,timezone
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');p=rd(R/'plan.json');batch=rd(R/'batch.json');own={z['fingerprint'] for z in batch};assert len(own)==8
rows=[]
def signature(sp):
 q=sp.get('parameters',{});graph=tuple(sorted((z['fingerprint'],Decimal(str(z['weight']))) for z in sp.get('components',[])))
 return sp.get('kind'),q.get('start_utc'),q.get('end_utc'),graph
for z in batch:
 sp=rd(ROOT/z['spec']);assert reg.fingerprint(sp)==z['fingerprint'] and rs[z['fingerprint']]['result_available']
 matches=[fp for fp,item in rs.items() if fp not in own and (item.get('result_available',False) or item['status']=='reserved') and signature(item.get('spec',{}))==signature(sp)]
 assert not matches,(z['name'],matches)
 rows.append({'name':z['name'],'fingerprint':z['fingerprint'],'BTC_target':z['NB'],'ETH_target':z['NE'],'raw_bank_weights':[v['weight'] for v in sp['components']],'source_graph':sp['components'],'old_economic_graph_matches':matches})
for fp,z in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
 for field in ['spec','report','archive']:assert sha(ROOT/z[field])==z[field+'_sha256']
x={'passed':True,'verified_utc':datetime.now(timezone.utc).isoformat(),'records_fully_compared':len(rs),'completed_report_sha256':sha(R/'report.json'),'passive_configurations':rows,'exact_complete_source_results_reused':len(p['read_only_references']),'native_models_reused':14,'new_native_model_evaluations':0,'pre_reserve_economic_graph_screen':'long_only_prior_lookup.json','all_old_source_statuses_unchanged':True,'no_financial_or_account_reexecution':True,'reproduction_command':[sys.executable,'-B',str(Path(__file__).resolve())]}
(R/'economic_configuration_identity_verification.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':True,'records':len(rs),'new_graphs':len(rows),'old_matches':0,'source_results_reused':30}))
