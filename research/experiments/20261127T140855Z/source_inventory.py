"""Metadata-only one-axis source inventory; no backtest or curve calculations."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');bases={'BTC':'41de4309229b892489a07574af07a73ae93229a35c118558ed60362285e90c89','ETH':'a34c0bd6e523db4188b1b6f27d2e8efec9b679106ae19d9cd97438b6dbae3984'};out={};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for asset,fp in bases.items():
 base=rs[fp]['spec'];q0=base['parameters'];rows=[]
 for f,z in rs.items():
  sp=z.get('spec',{});q=sp.get('parameters',{})
  if sp.get('kind')!=base['kind'] or sp.get('universe')!=base['universe'] or not z.get('result_available'):continue
  diff={k:[q0.get(k),q.get(k)] for k in set(q0)|set(q) if k not in {'persistence','prior_370day_source_fingerprint'} and q0.get(k)!=q.get(k)}
  if len(diff)<=1:
   assert sha(ROOT/z['report'])==z['report_sha256'];rows.append({'fingerprint':f,'differences':diff,'parameters':q,'report':z['report'],'report_sha256':z['report_sha256']})
 out[asset]={'baseline_parameters':q0,'rows':rows};print(asset,json.dumps([{'fingerprint':z['fingerprint'],'differences':z['differences']} for z in rows]),flush=True)
(R/'source_inventory.json').write_text(json.dumps({'full_registry_IDs':len(rs),'assets':out,'new_financial_or_account_calculations':0},ensure_ascii=False,indent=2)+'\n')
