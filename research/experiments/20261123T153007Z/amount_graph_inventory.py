"""Full metadata lookup only; no return computation or account execution."""
from pathlib import Path
from decimal import Decimal
import json,sys
ROOT=Path.cwd();R=ROOT/'research/experiments/20261123T153007Z';sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');base=rs['41de4309229b892489a07574af07a73ae93229a35c118558ed60362285e90c89']['spec'];q0=base['parameters'];ignored={'persistence','prior_370day_source_fingerprint','fixed_entry_notional_usdt','raw_entry_notional_fraction_of_initial_capital'};B={}
for fp,z in rs.items():
 sp=z.get('spec',{});q=sp.get('parameters',{})
 if sp.get('kind')==base['kind'] and sp.get('universe')==base['universe'] and z.get('result_available') and all(q0.get(k)==q.get(k) for k in (set(q0)|set(q))-ignored):B[q['fixed_entry_notional_usdt']]=fp
E={'VW8':'cb3c8bf2ba5106ebd505174ea724e4d767a6c738743e2418f527c39ea06863c1','BASE':'a34c0bd6e523db4188b1b6f27d2e8efec9b679106ae19d9cd97438b6dbae3984','VW12':'a4b17122bd98314bb52f9033edbd9a4240c5a399186b17e7f2eb86dbcd9ddf79','M2':'3c0d5ad1fb5045b2b2d2cf361fa246e5811de807aea0b3344db35d788b4e64c8','M6':'eded818583cd65a3261fd95488e9429a1d8fbc98c7c7a6db4d910f97434a0e15','CAP0525':'d7cbaea5d5bcfc7387a551a07a28cf3b9de619a0c4195203d410836e09262320','CAP06':'cf85e6e76f1c6de286388065252d1384c12b7e193bd66184ffbcbb6cb50fec63'};index={}
for fp,z in rs.items():
 sp=z.get('spec',{});q=sp.get('parameters',{})
 if sp.get('kind')=='combination' and q.get('start_utc')=='2025-10-19T00:01:00Z' and q.get('end_utc')=='2026-11-14T00:01:00Z' and (z.get('result_available') or z['status']=='reserved'):index.setdefault(tuple(sorted((a['fingerprint'],Decimal(str(a['weight']))) for a in sp.get('components',[]))),[]).append(fp)
rows=[{'BTC_N':n,'BTC_fingerprint':b,'ETH_axis':axis,'ETH_fingerprint':e,'matches':index.get(tuple(sorted([(b,Decimal(1)),(e,Decimal(1))])),[])} for n,b in sorted(B.items()) for axis,e in E.items()];(R/'amount_graph_inventory.json').write_text(json.dumps({'passed':True,'complete_registry_IDs':len(rs),'BTC_banks':B,'rows':rows,'no_market_or_account_calculations':True},indent=2)+'\n');print('BANKS',json.dumps(B));print('UNTESTED',json.dumps([{k:z[k] for k in ['BTC_N','ETH_axis']} for z in rows if not z['matches']]))
