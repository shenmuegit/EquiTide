"""Freeze the next original-account windows and reuse actual public settlement fields."""
import copy,json,sys,subprocess
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
P=ROOT/'research/experiments/20261113T053941Z'
assert not (R/'code_binding_before_evaluation.json').exists()
(R/'bootstrap_receipt.json').write_bytes((R/'review/native_bootstrap.py_receipt.json').read_bytes())
receipts=[]
for cmd in [['git','rev-parse','HEAD'],['git','rev-parse','origin/main']]:
 a=now();z=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);receipts.append({'command':cmd,'cwd':str(ROOT),'started_utc':a,'finished_utc':now(),'exit_code':z.returncode,'stdout':z.stdout,'stderr':z.stderr});assert z.returncode==0
assert receipts[0]['stdout']==receipts[1]['stdout'];put(R/'remote_sync_receipts.json',receipts)
fresh=json.loads((R/'window_funding_preflight.json').read_text());assert fresh['passed'] and fresh['public_fields_by_asset']=={'BTC':[],'ETH':[]};old00=json.loads((P/'funding00_nov13_preflight.json').read_text())
(R/'funding00_nov13_preflight.json').write_bytes((P/'funding00_nov13_preflight.json').read_bytes());put(R/'funding00_public_reuse.json',{'passed':True,'original_source':rel(P/'funding00_nov13_preflight.json'),'original_source_sha256':sha(P/'funding00_nov13_preflight.json'),'copied_source':rel(R/'funding00_nov13_preflight.json'),'original_capture_recorded_utc':old00['recorded_utc'],'fresh_window_capture_utc':fresh['recorded_utc'],'current_complete_union_window_empty':True,'all3_already_booked_once':True})
ms=lambda t:int(datetime.fromisoformat(t.replace('Z','+00:00')).timestamp()*1000);w={}
for a,begin,end in [('SMA','2026-11-13T02:30:00Z','2026-11-13T04:30:00Z'),('candidate','2026-11-13T02:30:00Z','2026-11-13T04:30:00Z'),('l4h02','2026-11-13T04:10:00Z','2026-11-13T06:10:00Z'),('fewm','2026-11-13T04:10:00Z','2026-11-13T06:10:00Z')]:
 w[a]={'start_utc':begin,'cutoff_utc':end,'expected_daily_events_utc':[],'expected_funding_utc':[],'expected_funding_by_asset':{'BTC':[],'ETH':[]},'expected_funding_records':0,'next_daily_decision_utc':'2026-11-14T00:01:00Z'}
w.update(recorded_utc=now(),rules='All4mark/riskonly,currentcompletefundwindowempty. SMAfull65authority033939retained. All3perpsactualNov13_00alreadybookedonce,no repeat/no daily/reset/forcedexit/researchadoption.');put(R/'account_windows.json',w)
l=json.loads((P/'l4h02_resume_plan.json').read_text());point=ROOT/'research/automation/l4h02_forward_latest.json';l.update(frozen_at_utc=now(),recorded_utc=now(),round=R.name,previous_pointer=json.loads(point.read_text()),previous_pointer_sha256=sha(point),cutoff_utc=w['l4h02']['cutoff_utc'],cutoff_ns=ms(w['l4h02']['cutoff_utc'])*1000000,branch_lock_broker_pid=1237293,rules=w['rules']);put(R/'l4h02_resume_plan.json',l)
print('PASS4original windowsmark/riskonly,actualfund0/0/0/0,full65authority033939retained;0calculations')
