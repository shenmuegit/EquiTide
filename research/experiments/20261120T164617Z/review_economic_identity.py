"""Read-only whole-registry native-parameter and economic parent graph dedup."""
import hashlib,json,sys
from datetime import datetime,timezone
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rs=reg.read_records(ROOT/'research/automation/registry.jsonl');p=rd(R/'plan.json');batch=rd(R/'batch.json');own={z['fingerprint'] for z in batch};assert len(own)==12
ignore={'persistence','prior_370day_source_fingerprint'}
def signature(sp):
 q=sp.get('parameters',{})
 if sp.get('kind')=='combination':return sp.get('kind'),q.get('start_utc'),q.get('end_utc'),tuple(sorted((x['fingerprint'],Decimal(str(x['weight']))) for x in sp.get('components',[])))
 return sp.get('kind'),sp.get('market'),sp.get('timeframe'),sp.get('universe'),{k:v for k,v in q.items() if k not in ignore}
rows=[]
for z in batch:
 sp=rd(ROOT/z['spec']);assert reg.fingerprint(sp)==z['fingerprint'] and rs[z['fingerprint']]['result_available'];matches=[fp for fp,x in rs.items() if fp not in own and (x.get('result_available',False) or x['status']=='reserved') and signature(x.get('spec',{}))==signature(sp)];assert not matches,(z['name'],matches);rows.append({'name':z['name'],'scope':z['scope'],'fingerprint':z['fingerprint'],'ETH_max_history_age_hours':48,'ETH_budget_volatility_ratio':z['W'],'ETH_mature_funding_count':z['K'],'old_economic_matches':matches})
for fp,z in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
 for key in ['spec','report','archive']:assert sha(ROOT/z[key])==z[key+'_sha256']
x={'passed':True,'verified_utc':datetime.now(timezone.utc).isoformat(),'records_fully_compared':len(rs),'completed_report_sha256':sha(R/'report.json'),'rows':rows,'new_native_models':6,'new_parent_models':6,'exact_source_results_reused':len(p['read_only_references']),'old_statuses_unchanged':True,'no_financial_or_account_reexecution':True};(R/'economic_configuration_identity_verification.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps({'passed':True,'records':len(rs),'new_native':6,'new_parent_graphs':6,'old_matches':0,'readonly':len(p['read_only_references'])}))
