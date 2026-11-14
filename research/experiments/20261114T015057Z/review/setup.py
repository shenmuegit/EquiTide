"""Freeze actual next windows and source bindings before account calculation."""
import json,sys,subprocess
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
P=ROOT/'research/experiments/20261113T234922Z'
assert not (R/'code_binding_before_evaluation.json').exists()
(R/'bootstrap_receipt.json').write_bytes((R/'review/native_bootstrap.py_receipt.json').read_bytes())
receipts=[]
for cmd in [['git','rev-parse','HEAD'],['git','rev-parse','origin/main']]:
 a=now();z=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);receipts.append({'command':cmd,'cwd':str(ROOT),'started_utc':a,'finished_utc':now(),'exit_code':z.returncode,'stdout':z.stdout,'stderr':z.stderr});assert z.returncode==0
assert receipts[0]['stdout']==receipts[1]['stdout'];put(R/'remote_sync_receipts.json',receipts)
fresh=json.loads((R/'window_funding_preflight.json').read_text());assert fresh['passed'];(R/'funding16_nov13_preflight.json').write_bytes((P/'funding16_nov13_preflight.json').read_bytes());(R/'funding08_nov13_preflight.json').write_bytes((P/'funding08_nov13_preflight.json').read_bytes())
for name in ['funding00_nov13_preflight.json','funding00_public_reuse.json']:(R/name).write_bytes((P/name).read_bytes())
ms=lambda t:int(datetime.fromisoformat(t.replace('Z','+00:00')).timestamp()*1000);w={}
for a,begin,end in [('SMA','2026-11-13T20:30:00Z','2026-11-13T22:30:00Z'),('candidate','2026-11-13T20:30:00Z','2026-11-13T22:30:00Z'),('l4h02','2026-11-13T22:10:00Z','2026-11-14T00:10:00Z'),('fewm','2026-11-13T22:10:00Z','2026-11-14T00:10:00Z')]:
 fields={asset:[] if a=='SMA' else [z for z in fresh['public_fields_by_asset'][asset] if ms(begin)<z['fundingTime']<=ms(end)] for asset in ['BTC','ETH']};times=sorted({z['fundingTime'] for xs in fields.values() for z in xs});w[a]={'start_utc':begin,'cutoff_utc':end,'expected_daily_events_utc':['2026-11-14T00:01:00Z'] if a in ['l4h02','fewm'] else [],'expected_funding_utc':[datetime.fromtimestamp(t/1000,timezone.utc).isoformat().replace('+00:00','Z') for t in times],'expected_funding_by_asset':fields,'expected_funding_records':3*sum(map(len,fields.values())),'next_daily_decision_utc':'2026-11-15T00:01:00Z' if a in ['l4h02','fewm'] else '2026-11-14T00:01:00Z'}
assert [w[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']]==[0,0,6,6]
prior=json.loads((P/'funding08_nov13_preflight.json').read_text());assert all(len(xs)==1 and xs[0]['fundingTime']<ms('2026-11-14T00:01:00Z') for xs in fresh['public_fields_by_asset'].values()) and prior['public_fields_by_asset']==json.loads((R/'funding08_nov13_preflight.json').read_text())['public_fields_by_asset']
put(R/'funding00_nov14_preflight.json',fresh)
w.update(recorded_utc=now(),rules='All3 perp accounts booked Nov13 actual00/08/16 once. L4/FEWM now cover Nov14 actual00 and original00:01 decisions, using own q/cash and completed1440minute dailyvolume. SMA/single end22:30 before midnight. No reset/forcedexit/research-rule adoption. Funding actual timestamps determine records;original sources retained. SMA full65 authority033939 unchanged.');put(R/'account_windows.json',w)
l=json.loads((P/'l4h02_resume_plan.json').read_text());point=ROOT/'research/automation/l4h02_forward_latest.json';l.update(frozen_at_utc=now(),recorded_utc=now(),round=R.name,previous_pointer=json.loads(point.read_text()),previous_pointer_sha256=sha(point),cutoff_utc=w['l4h02']['cutoff_utc'],cutoff_ns=ms(w['l4h02']['cutoff_utc'])*1000000,branch_lock_broker_pid=1552430,rules=w['rules']);put(R/'l4h02_resume_plan.json',l)
paths=[R/name for name in ['observe_l4h02.py','observe_fewm.py','observe_candidate.py','forward.py','forward_registry.py','audit_incremental.py','audit_l4h02.py','audit_fewm.py','audit_candidate.py','audit_forward.py']]
paths += [ROOT/x for x in l['source_sha256']]
put(R/'original_accounts_binding.json',{'recorded_utc':now(),'sources_sha256':{rel(x):sha(x) for x in paths},'frozen_before_current_account_calculation':True,'original_kernels_unchanged':True,'SMA_full65_authority':'research/experiments/20261113T033939Z/forward_inputs.json.gz'})
print('PASS frozen actual funding0/0/6/6 and L4FEWM original daily, before0calculations')
