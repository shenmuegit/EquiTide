"""Prepare unfitted adverse-price-path entry-efficiency experiment and original account windows."""
import ast,copy,json,subprocess,sys
from pathlib import Path
from datetime import datetime
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261112T133154Z';A=ROOT/'research/experiments/20261111T212846Z';sys.path.insert(0,str(R));from common import *
assert not (R/'code_binding_before_evaluation.json').exists()
for f in P.glob('*.py'):
 if f.name in ['bootstrap.py','common.py']:continue
 s=f.read_text().replace(P.name,R.name).replace('947813','979157')
 if f.name in ['forward_registry.py','checks.py','finalize.py']:s=s.replace('20261112T113123Z',P.name)
 (R/f.name).write_text(s)
for n in ['negative_parent_controls.py','negative_policy_controls.py','staged_whitespace.py']:(R/'review'/n).write_bytes((P/'review'/n).read_bytes())
(R/'bootstrap_receipt.json').write_bytes((R/'review/native_bootstrap.py_receipt.json').read_bytes());receipts=[]
for cmd in [['git','rev-parse','HEAD'],['git','rev-parse','origin/main']]:
 a=now();z=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);receipts.append({'command':cmd,'cwd':str(ROOT),'started_utc':a,'finished_utc':now(),'exit_code':z.returncode,'stdout':z.stdout,'stderr':z.stderr});assert z.returncode==0
assert receipts[0]['stdout']==receipts[1]['stdout'];put(R/'remote_sync_receipts.json',receipts)
for n in ['funding16_source_verification.json','funding00_source_verification.json','funding08_source_verification.json']:
 z=json.loads((P/n).read_text());assert sha(ROOT/z['source'])==z['source_sha256'];z['recorded_utc']=now();put(R/n,z)
fresh=json.loads((R/'window_funding_preflight.json').read_text());assert fresh['passed'] and fresh['public_fields_by_asset']=={'BTC':[],'ETH':[]};u=json.loads((P/'funding08_public_reuse_verification.json').read_text());u.update(recorded_utc=now(),fresh_complete_window_preflight=rel(R/'window_funding_preflight.json'),fresh_preflight_sha256=sha(R/'window_funding_preflight.json'),fresh_official_GETs=fresh['new_GETs']);put(R/'funding08_public_reuse_verification.json',u)
w={}
for a,st,cut in [('SMA','10:30','12:30'),('candidate','10:30','12:30'),('l4h02','12:10','14:10'),('fewm','12:10','14:10')]:w[a]={'start_utc':f'2026-11-12T{st}:00Z','cutoff_utc':f'2026-11-12T{cut}:00Z','expected_daily_events_utc':[],'expected_funding_utc':[],'expected_funding_by_asset':{'BTC':[],'ETH':[]},'expected_funding_records':0,'next_daily_decision_utc':'2026-11-13T00:01:00Z'}
w.update(recorded_utc=now(),rules='Official actual full union window (10:30,14:10] funding history empty; original four accounts append only closed marks/risk. No day/fill/funding/reset/adoption. All three perps already booked Nov12_00 and actual08+1ms once. SMA SPOT/full65authority033054 unchanged.');put(R/'account_windows.json',w)
l=json.loads((P/'l4h02_resume_plan.json').read_text());point=ROOT/'research/automation/l4h02_forward_latest.json';l.update(frozen_at_utc=now(),recorded_utc=now(),round=R.name,previous_pointer=json.loads(point.read_text()),previous_pointer_sha256=sha(point),cutoff_utc=w['l4h02']['cutoff_utc'],cutoff_ns=int(datetime.fromisoformat(w['l4h02']['cutoff_utc'].replace('Z','+00:00')).timestamp())*1000000000,branch_lock_broker_pid=979157,rules=w['rules']);put(R/'l4h02_resume_plan.json',l)
# Reuse original two-sided samplevol policy/ledger; only append exact-rational path efficiency gate.
s=(A/'engine.py').read_text();needle=' before_funding=wanted;sn=';assert s.count(needle)==1
s=s.replace(needle," before_efficiency=wanted;W=int(p['entry_path_efficiency_window_days']);er=adverse_efficiency(m['closes'],i,W,raw);er_cap=F(str(p['entry_path_efficiency_ceiling']));assert W in [8,10,12] and er_cap in [F('.45'),F('.60'),F('.75')] and p['entry_path_efficiency_filter']=='adverse_candidate_price_efficiency' and p['entry_path_efficiency_scope']=='new_or_reversed_position_only';wanted=entry_filter(wanted,actual,er,er_cap)\n before_funding=wanted;sn=")
s=s.replace("'kind':'ETH_finite_EWMslope_entry_gate_reversal_entry_vol'","'kind':'ETH_finite_EWMslope_entry_gate_reversal_entry_vol_adverse_efficiency'")
s=s.replace("'short_entry_return_hurdle':H}","'short_entry_return_hurdle':H,'raw_desired_before_efficiency_filter':before_efficiency,'efficiency_candidate_direction':raw,'observed_adverse_path_efficiency_exact':str(er),'path_efficiency_window_days':W,'path_efficiency_ceiling_exact':str(er_cap),'path_efficiency_filter_applied':bool(before_efficiency and before_efficiency!=actual)}")
helper='''def adverse_efficiency(closes,i,window,direction):
 from fractions import Fraction as F
 assert direction in [-1,0,1] and window in [8,10,12] and i-window-1>=0
 changes=[F(closes[j])-F(closes[j-1]) for j in range(i-window,i)]
 net=sum(changes,F(0));length=sum((abs(x) for x in changes),F(0))
 return max(-direction*net,F(0))/length if length else F(0)

'''
s=s.replace('def latest_funding(',helper+'def latest_funding(');(R/'engine.py').write_text(s)
# Preserve report accounting; give the two new grid coordinates explicit names.
for n in ['run.py','exports.py','checks.py']:
 s=(R/n).read_text().replace("['ETH_V']","['ETH_ER_W']").replace("['ETH_CAP']","['ETH_ER_CAP']").replace("['V']","['W']").replace("['CAP']","['ER_CAP']").replace("'ETH_V'","'ETH_ER_W'").replace("'ETH_CAP'","'ETH_ER_CAP'")
 for x,y in [('ETH_risk_window','ETH_path_efficiency_window'),('ETH_directional_adverse_RMS_cap','ETH_adverse_path_efficiency_cap'),('ETH_directional_adverse_RMS_CAP','ETH_adverse_path_efficiency_CAP'),('ETH_entry_risk_window','ETH_path_efficiency_window')]:s=s.replace(x,y)
 s=s.replace('ETH direction-aware adverse RMS new-entry gate','ETH adverse path efficiency new-entry gate').replace('ETH direction-aware adverse RMS cap','ETH adverse price-path efficiency cap').replace('ETH adverse risk window (days)','ETH path efficiency window (days)')
 (R/n).write_text(s)
# New read-only outcomes are derived after execution; no prior formatter retry is required.
s=(R/'finalize.py').read_text().replace("'final_checks_retry1'","'final_checks'").replace("'review/native_staged_whitespace_retry1.py_receipt.json'","'review/native_staged_whitespace.py_receipt.json'")
s=s.replace("['2026-11-12T10:30:00Z','2026-11-12T12:30:00Z']","['2026-11-12T12:30:00Z','2026-11-12T14:30:00Z']").replace("['2026-11-12T12:10:00Z','2026-11-12T14:10:00Z']","['2026-11-12T14:10:00Z','2026-11-12T16:10:00Z']")
(R/'finalize.py').write_text(s)
print('Prepared original four no-event account windows and immutable original execution kernels;0 reservations or evaluations')
