"""Prepare close-location entry confirmation and actual Nov12_16 funding windows."""
import ast,copy,json,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261112T153255Z';A=ROOT/'research/experiments/20261111T212846Z';sys.path.insert(0,str(R));from common import *
assert not (R/'code_binding_before_evaluation.json').exists()
for f in P.glob('*.py'):
 if f.name in ['bootstrap.py','common.py','audit_retry1.py']:continue
 s=f.read_text().replace(P.name,R.name).replace('979157','1012211')
 if f.name in ['forward_registry.py','checks.py','finalize.py']:s=s.replace('20261112T133154Z',P.name)
 (R/f.name).write_text(s)
# Use the corrected old independent checker as the new baseline, leaving every old file unchanged.
(R/'audit.py').write_text((P/'audit_retry1.py').read_text())
for n in ['negative_parent_controls.py','negative_policy_controls.py','staged_whitespace.py']:(R/'review'/n).write_bytes((P/'review'/n).read_bytes())
(R/'bootstrap_receipt.json').write_bytes((R/'review/native_bootstrap.py_receipt.json').read_bytes());receipts=[]
for cmd in [['git','rev-parse','HEAD'],['git','rev-parse','origin/main']]:
 a=now();z=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);receipts.append({'command':cmd,'cwd':str(ROOT),'started_utc':a,'finished_utc':now(),'exit_code':z.returncode,'stdout':z.stdout,'stderr':z.stderr});assert z.returncode==0
assert receipts[0]['stdout']==receipts[1]['stdout'];put(R/'remote_sync_receipts.json',receipts)
for n in ['funding16_source_verification.json','funding00_source_verification.json','funding08_source_verification.json']:
 z=json.loads((P/n).read_text());assert sha(ROOT/z['source'])==z['source_sha256'];z['recorded_utc']=now();put(R/n,z)
fresh=json.loads((R/'window_funding_preflight.json').read_text());assert fresh['passed'] and all(len(fresh['public_fields_by_asset'][a])==1 and fresh['public_fields_by_asset'][a][0]['fundingTime']==1794499200003 for a in ['BTC','ETH']);put(R/'funding16_nov12_preflight.json',fresh)
put(R/'funding16_nov12_source_verification.json',{'passed':True,'recorded_utc':now(),'source':rel(R/'funding16_nov12_preflight.json'),'source_sha256':sha(R/'funding16_nov12_preflight.json'),'original_capture_recorded_utc':fresh['recorded_utc'],'public_fields_by_asset':fresh['public_fields_by_asset'],'raw_responses':fresh['raw_responses'],'original_native_capture_receipt':rel(R/'review/native_preflight.py_receipt.json'),'current_unique_public_GETs':fresh['new_GETs'],'scope':'One actual full-union-window official capture,used for preflight and own L4/FEWM funding only;no second GET and no cashflow reuse. Actual+3ms preserved.'})
u=json.loads((P/'funding08_public_reuse_verification.json').read_text());u.update(recorded_utc=now(),fresh_complete_window_preflight=rel(R/'window_funding_preflight.json'),fresh_preflight_sha256=sha(R/'window_funding_preflight.json'),fresh_official_GETs=fresh['new_GETs'],current_window_contains_no_settlement=False,old08_not_current_and_not_repeated=True);put(R/'funding08_public_reuse_verification.json',u)
ms=lambda t:int(datetime.fromisoformat(t.replace('Z','+00:00')).timestamp()*1000);w={}
for a,st,cut in [('SMA','12:30','14:30'),('candidate','12:30','14:30'),('l4h02','14:10','16:10'),('fewm','14:10','16:10')]:
 begin,end=f'2026-11-12T{st}:00Z',f'2026-11-12T{cut}:00Z';fields={asset:[] if a=='SMA' else [z for z in fresh['public_fields_by_asset'][asset] if ms(begin)<z['fundingTime']<=ms(end)] for asset in ['BTC','ETH']};times=sorted({z['fundingTime'] for xs in fields.values() for z in xs});w[a]={'start_utc':begin,'cutoff_utc':end,'expected_daily_events_utc':[],'expected_funding_utc':[datetime.fromtimestamp(t/1000,timezone.utc).isoformat().replace('+00:00','Z') for t in times],'expected_funding_by_asset':fields,'expected_funding_records':3*sum(map(len,fields.values())),'next_daily_decision_utc':'2026-11-13T00:01:00Z'}
assert [w[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']]==[0,0,6,6]
w.update(recorded_utc=now(),rules='SMA/single12:30to14:30 marks/risk only. L4/FEWM14:10to16:10 each book actualNov12_16:00:00.003 once from own preexisting q/cash;no fills/day events/reset/adoption. Single has not reached16 yet,old00/08 allthree alreadybooked once. SMA SPOT/full65authority033054 unchanged.');put(R/'account_windows.json',w)
l=json.loads((P/'l4h02_resume_plan.json').read_text());point=ROOT/'research/automation/l4h02_forward_latest.json';l.update(frozen_at_utc=now(),recorded_utc=now(),round=R.name,previous_pointer=json.loads(point.read_text()),previous_pointer_sha256=sha(point),cutoff_utc=w['l4h02']['cutoff_utc'],cutoff_ns=ms(w['l4h02']['cutoff_utc'])*1000000,branch_lock_broker_pid=1012211,rules=w['rules']);put(R/'l4h02_resume_plan.json',l)
# Retain the original two-sided pricevol and funding gates; append a bounded exact close-location score.
s=(A/'engine.py').read_text();needle=' before_funding=wanted;sn=';assert s.count(needle)==1
s=s.replace(needle," before_clv=wanted;W=int(p['entry_close_location_window_days']);score=candidate_clv(m,i,W,raw);minimum=F(str(p['entry_close_location_minimum']));assert W in [1,2,3] and minimum in [F(0),F('.25'),F('.5')] and p['entry_close_location_filter']=='candidate_signed_mean_completed_daily_CLV' and p['entry_close_location_scope']=='new_or_reversed_position_only';wanted=0 if wanted and wanted!=actual and score<minimum else wanted\n before_funding=wanted;sn=")
s=s.replace("'kind':'ETH_finite_EWMslope_entry_gate_reversal_entry_vol'","'kind':'ETH_finite_EWMslope_entry_gate_reversal_entry_vol_daily_CLV'").replace("'short_entry_return_hurdle':H}","'short_entry_return_hurdle':H,'raw_desired_before_CLV_filter':before_clv,'CLV_candidate_direction':raw,'observed_candidate_CLV_exact':str(score),'close_location_window_days':W,'close_location_minimum_exact':str(minimum),'CLV_filter_applied':bool(before_clv and before_clv!=actual)}")
helper='''def candidate_clv(m,i,window,direction):
 from fractions import Fraction as F
 assert direction in [-1,0,1] and window in [1,2,3] and i-window>=0
 f=m['frame'];sn=int(f['available_ts'][i*1440-1]);scores=[]
 for j in range(i-window,i):
  assert int(f['available_ts'][(j+1)*1440-1])<=sn,'Completed UTC daily range is not available at signal'
  high=f['high'].slice(j*1440,1440);low=f['low'].slice(j*1440,1440);assert len(high)==len(low)==1440
  H,L,C=F(high.max()),F(low.min()),F(m['closes'][j]);assert H>=C>=L>0
  scores.append((2*C-H-L)/(H-L) if H!=L else F(0))
 return direction*sum(scores,F(0))/window

'''
s=s.replace('def latest_funding(',helper+'def latest_funding(');(R/'engine.py').write_text(s)
for n in ['run.py','exports.py','checks.py','audit.py','definitions.py','freeze.py']:
 f=R/n;s=f.read_text().replace('ETH_ER_W','ETH_CLV_W').replace('ETH_ER_CAP','ETH_CLV_MIN').replace('ER_CAP','CLV_MIN').replace('entry_path_efficiency_window_days','entry_close_location_window_days').replace('entry_path_efficiency_ceiling','entry_close_location_minimum').replace('entry_path_efficiency_filter','entry_close_location_filter').replace('entry_path_efficiency_scope','entry_close_location_scope').replace('entry_path_efficiency_direction_source','entry_close_location_direction_source').replace('adverse_candidate_price_efficiency','candidate_signed_mean_completed_daily_CLV')
 for x,y in [('ETH_path_efficiency_window','ETH_close_location_window'),('ETH_adverse_path_efficiency_cap','ETH_close_location_minimum'),('ETH_adverse_path_efficiency_CAP','ETH_close_location_MIN')]:s=s.replace(x,y)
 f.write_text(s)
s=(R/'commands.py').read_text().replace("if phase=='audit_retry1':jobs=[('audit_retry1.log',['audit_retry1.py'])]\n",'');(R/'commands.py').write_text(s)
s=(R/'finalize.py').read_text();s='\n'.join(line for line in s.splitlines() if not line.startswith("repair=rd(R/'audit_repair_binding.json')"))+'\n';s=s.replace("'audit_retry1'","'audit'").replace(";frozen.update(rd(R/'audit_repair_binding.json')['supplemental_readonly_source_sha256'])",'').replace("'readonly_audit_incomplete_failed_attempts':1","'readonly_audit_incomplete_failed_attempts':0")
s=s.replace("['2026-11-12T12:30:00Z','2026-11-12T14:30:00Z']","['2026-11-12T14:30:00Z','2026-11-12T16:30:00Z']").replace("['2026-11-12T14:10:00Z','2026-11-12T16:10:00Z']","['2026-11-12T16:10:00Z','2026-11-12T18:10:00Z']").replace("{'SMA':0,'candidate':0,'l4h02':0,'fewm':0}","{'SMA':0,'candidate':0,'l4h02':6,'fewm':6}")
s=s.replace("rd(R/'window_funding_preflight.json')['public_fields_by_asset']=={'BTC':[],'ETH':[]}","rd(R/'window_funding_preflight.json')['public_fields_by_asset']==rd(R/'funding16_nov12_source_verification.json')['public_fields_by_asset']")
s=s.replace("R/'window_funding_preflight.json',ROOT/'checks/monitor_snapshot.py'","R/'window_funding_preflight.json',R/'funding16_nov12_preflight.json',R/'funding16_nov12_source_verification.json',ROOT/'checks/monitor_snapshot.py'")
(R/'finalize.py').write_text(s)
print('Prepared original accounting kernels,CLV entry helper,actual +3ms16fund windows;0 reservations/evaluations')
