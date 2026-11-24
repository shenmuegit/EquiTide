"""Read complete native parameter metadata only; no return, NAV or account calculation."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');out={}
for asset,fp in [('BTC','41de4309229b892489a07574af07a73ae93229a35c118558ed60362285e90c89'),('ETH','a34c0bd6e523db4188b1b6f27d2e8efec9b679106ae19d9cd97438b6dbae3984')]:
 base=rs[fp]['spec'];q0=base['parameters'];rows=[]
 for f,z in rs.items():
  sp=z.get('spec',{});q=sp.get('parameters',{})
  if sp.get('kind')!=base['kind'] or sp.get('universe')!=base['universe'] or not z.get('result_available'):continue
  diff={k:[q0.get(k),q.get(k)] for k in set(q0)|set(q) if k not in {'persistence','prior_370day_source_fingerprint'} and q0.get(k)!=q.get(k)}
  if len(diff)<=1:rows.append({'fingerprint':f,'differences':diff,'report':z['report'],'report_sha256':z['report_sha256']})
 out[asset]={'base':fp,'baseline_parameters':q0,'one_axis_actual_models':rows}
(R/'native_metadata_inventory.json').write_text(json.dumps({'full_registry_IDs':len(rs),'new_financial_or_account_calculations':0,'assets':out},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({a:d['one_axis_actual_models'] for a,d in out.items()},ensure_ascii=False))
