"""Freeze the next original-account windows and reuse actual public settlement fields."""
import copy,json,sys,subprocess
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
P=ROOT/'research/experiments/20261112T193458Z'
assert not (R/'code_binding_before_evaluation.json').exists()
(R/'bootstrap_receipt.json').write_bytes((R/'review/native_bootstrap.py_receipt.json').read_bytes())
receipts=[]
for cmd in [['git','rev-parse','HEAD'],['git','rev-parse','origin/main']]:
 a=now();z=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);receipts.append({'command':cmd,'cwd':str(ROOT),'started_utc':a,'finished_utc':now(),'exit_code':z.returncode,'stdout':z.stdout,'stderr':z.stderr});assert z.returncode==0
assert receipts[0]['stdout']==receipts[1]['stdout'];put(R/'remote_sync_receipts.json',receipts)
for n in ['funding16_source_verification.json','funding00_source_verification.json','funding08_source_verification.json','funding08_public_reuse_verification.json']:
 z=json.loads((P/n).read_text());z['recorded_utc']=now();put(R/n,z)
fresh=json.loads((R/'window_funding_preflight.json').read_text());old=json.loads((P/'funding16_nov12_preflight.json').read_text());assert fresh['passed'] and fresh['public_fields_by_asset']=={'BTC':[],'ETH':[]}
(R/'funding16_nov12_preflight.json').write_bytes((P/'funding16_nov12_preflight.json').read_bytes())
z=json.loads((P/'funding16_nov12_source_verification.json').read_text());z.update(recorded_utc=now(),source=rel(R/'funding16_nov12_preflight.json'),source_sha256=sha(R/'funding16_nov12_preflight.json'),current_unique_public_GETs=fresh['new_GETs'],fresh_complete_window_preflight=rel(R/'window_funding_preflight.json'),original_capture_source=rel(P/'funding16_nov12_preflight.json'),scope='Original public16+3ms fields/capture UTC preserved. Fresh complete union-window GET confirms these fields. All three already booked16; current complete union window contains no actual settlement, no repeat.');put(R/'funding16_nov12_source_verification.json',z)
ms=lambda t:int(datetime.fromisoformat(t.replace('Z','+00:00')).timestamp()*1000);w={}
for a,st,cut in [('SMA','16:30','18:30'),('candidate','16:30','18:30'),('l4h02','18:10','20:10'),('fewm','18:10','20:10')]:
 begin,end=f'2026-11-12T{st}:00Z',f'2026-11-12T{cut}:00Z';fields={asset:[] if a=='SMA' else [z for z in fresh['public_fields_by_asset'][asset] if ms(begin)<z['fundingTime']<=ms(end)] for asset in ['BTC','ETH']};times=sorted({z['fundingTime'] for xs in fields.values() for z in xs});w[a]={'start_utc':begin,'cutoff_utc':end,'expected_daily_events_utc':[],'expected_funding_utc':[datetime.fromtimestamp(t/1000,timezone.utc).isoformat().replace('+00:00','Z') for t in times],'expected_funding_by_asset':fields,'expected_funding_records':3*sum(map(len,fields.values())),'next_daily_decision_utc':'2026-11-13T00:01:00Z'}
assert [w[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']]==[0,0,0,0]
w.update(recorded_utc=now(),rules='SMA/single16:30to18:30, L4/FEWM18:10to20:10, marks/risk only. All3 already booked16+3ms; no repeat. No fills/daily/reset/adoption. SMA SPOT/full65authority033054 unchanged.');put(R/'account_windows.json',w)
l=json.loads((P/'l4h02_resume_plan.json').read_text());point=ROOT/'research/automation/l4h02_forward_latest.json';l.update(frozen_at_utc=now(),recorded_utc=now(),round=R.name,previous_pointer=json.loads(point.read_text()),previous_pointer_sha256=sha(point),cutoff_utc=w['l4h02']['cutoff_utc'],cutoff_ns=ms(w['l4h02']['cutoff_utc'])*1000000,branch_lock_broker_pid=1071430,rules=w['rules']);put(R/'l4h02_resume_plan.json',l)
print('PASS original windows frozen, funding records0/0/0/0, original16capture preserved;0calculations')
