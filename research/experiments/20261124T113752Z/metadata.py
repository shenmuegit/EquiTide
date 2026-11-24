"""Read complete concrete source definitions and build canonical graph index before lookup."""
import hashlib,itertools,json,sys
from decimal import Decimal
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bases={'BTC':'41de4309229b892489a07574af07a73ae93229a35c118558ed60362285e90c89','ETH':'a34c0bd6e523db4188b1b6f27d2e8efec9b679106ae19d9cd97438b6dbae3984'}
axes={'BTC':('entry_volatility_window_days',[9,10,11]),'ETH':('entry_volatility_ceiling',[.0525,.05625,.06])};maps={};source_metadata=[]
for asset,fp in bases.items():
 base=rs[fp]['spec'];q0=base['parameters'];axis,values=axes[asset];selected={}
 for value in values:
  matches=[]
  for f,z in rs.items():
   sp=z.get('spec',{});q=sp.get('parameters',{})
   if sp.get('kind')!=base['kind'] or sp.get('universe')!=base['universe'] or not z.get('result_available') or q.get(axis)!=value:continue
   if any(q.get(k)!=q0.get(k) for k in set(q)|set(q0) if k not in {axis,'persistence','prior_370day_source_fingerprint'}):continue
   matches.append(f)
  assert len(matches)==1,(asset,value,matches);f=matches[0];z=rs[f];assert sha(ROOT/z['report'])==z['report_sha256'];selected[value]=f;source_metadata.append({'asset':asset,'coordinate':value,'fingerprint':f,'parameters':z['spec']['parameters'],'report':z['report'],'report_sha256':z['report_sha256']})
 maps[asset]=selected
def key(xs):
 totals={}
 for c in xs:totals[c['fingerprint']]=totals.get(c['fingerprint'],Decimal(0))+Decimal(str(c['weight']))
 return tuple(sorted(totals.items()))
index={}
for fp,z in rs.items():
 sp=z.get('spec',{});q=sp.get('parameters',{})
 if sp.get('kind')=='combination' and q.get('start_utc')=='2025-10-19T00:01:00Z' and q.get('end_utc')=='2026-11-14T00:01:00Z' and (z.get('result_available') or z['status']=='reserved'):index.setdefault(key(sp['components']),[]).append(fp)
rows=[]
for w,k in itertools.product(axes['BTC'][1],axes['ETH'][1]):
 fs=index.get(key([{'fingerprint':maps['BTC'][w],'weight':1},{'fingerprint':maps['ETH'][k],'weight':1}]),[]);rows.append({'W':w,'K':k,'BTC':maps['BTC'][w],'ETH':maps['ETH'][k],'matches':fs})
out={'recorded_utc':datetime.now(timezone.utc).isoformat(),'full_registry_IDs':len(rs),'canonical_component_graph_keys':len(index),'complete_index_built_before_grid_lookup':True,'axes':axes,'BTC':maps['BTC'],'ETH':maps['ETH'],'source_metadata':source_metadata,'rows':rows,'new_financial_or_account_calculations':0}
(R/'volwindow_riskcap_metadata_availability.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':True,'BTC':maps['BTC'],'ETH':maps['ETH'],'lookup':rows,'new_graphs':sum(not z['matches'] for z in rows),'new_financial_or_account_calculations':0}))
