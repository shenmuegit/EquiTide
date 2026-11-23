from pathlib import Path
import json,sys
ROOT=Path.cwd();R=ROOT/"research/experiments/20261123T132905Z";sys.path.insert(0,str(ROOT/"research/automation"));import registry as reg
records=reg.read_records(ROOT/"research/automation/registry.jsonl");put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n")
# Metadata only; no outcome calculations.
from decimal import Decimal
B={1000:'41de4309229b892489a07574af07a73ae93229a35c118558ed60362285e90c89',1500:'4198c65ac7ee9be4eef44d98e08ce6fcad2d9b9a802ed6cbe862a836e0903f59',1750:'adea37647c03a5347a4bb10f5d142370c6580117314b24cb78b7e6829a5456e2'}
E={0.00625:'c8c7129233c49140e3048443091d00ed34ee1a6c708ef82c50e584684b6d57b8',0.0075:'a34c0bd6e523db4188b1b6f27d2e8efec9b679106ae19d9cd97438b6dbae3984',0.00875:'f575d44c61da75ad3b08d7e2c26e73633c2397624750013990fbfa71f316851b',0.01:'eb1edaafae243a252dcf93400f5bb161bb0f2778f555e44bc9168dae3a39ff95',7:'5cd3e65984c4a723e3c8291811f0f9a2aed2486ce1f219eaf4bd6b580f96e143',10:'70c164999e5f439bd54ca3cac05a1d65ae0546dfcb2a5dea5ffc9cdb2ba3439d',0.0525:'d7cbaea5d5bcfc7387a551a07a28cf3b9de619a0c4195203d410836e09262320',0.06:'cf85e6e76f1c6de286388065252d1384c12b7e193bd66184ffbcbb6cb50fec63'}
index={}
for fp,z in records.items():
 sp=z.get('spec',{});q=sp.get('parameters',{})
 if sp.get('kind')=='combination' and q.get('start_utc')=='2025-10-19T00:01:00Z' and q.get('end_utc')=='2026-11-14T00:01:00Z' and (z.get('result_available') or z['status']=='reserved'):
  sig=tuple(sorted((a['fingerprint'],Decimal(str(a['weight']))) for a in sp.get('components',[])));index.setdefault(sig,[]).append(fp)
rows=[{'BTC_N':n,'ETH_axis_value':e,'matches':index.get(tuple(sorted([(b,Decimal(1)),(fp,Decimal(1))])),[])} for n,b in B.items() for e,fp in E.items()]
put(R/'additional_graph_metadata_lookup.json',{'passed':True,'full_registry_IDs':len(records),'rows':rows,'no_market_or_account_calculations':True});print('CURRENT_GRAPH_METADATA',json.dumps(rows),flush=True)
