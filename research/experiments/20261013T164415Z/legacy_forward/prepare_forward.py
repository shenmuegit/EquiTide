#!/usr/bin/env python3
"""Prepare and reserve a one-hour mark-only delayed legacy SMA shadow continuation."""
import hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
T=Path(__file__).resolve().parent;R=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(R/'research/automation'));import registry
S=R/'research/experiments/20261011T235327Z';src_report_path=S/'forward_report.json';src_state_path=S/'forward_state.json'
old=json.loads(src_report_path.read_text());state=json.loads(src_state_path.read_text());cut='2026-10-12T00:00:00Z';begin=old['cutoff_utc'];
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp(s):return datetime.fromisoformat(s.replace('Z','+00:00'))
assert begin=='2026-10-11T23:00:00Z' and state['next_daily_decision_utc']=='2026-10-12T00:01:00Z'
assert (stamp(cut)-stamp(begin)).total_seconds()==3600 and stamp(cut)<stamp(state['next_daily_decision_utc']) and stamp(cut)<datetime.now(timezone.utc)
scene=old['configs']['forward_snapshot_combo']['scenes']['1'];old_points=len(scene['equity_usdt']);new_minutes=60
plan={'round':T.name,'mode':'delayed historical minute shadow only; independent of paper10 and lead-lag backtest','forward_resume':{'source_state':str(src_state_path.relative_to(R)),'state_sha256':sha(src_state_path),'source_report':str(src_report_path.relative_to(R)),'report_sha256':sha(src_report_path),'resume_utc':begin,'cutoff_utc':cut,'next_daily_decision_utc':state['next_daily_decision_utc'],'new_minutes':new_minutes,'cumulative_minutes':scene['elapsed_minutes']+new_minutes,'prior_NAV_points':old_points,'total_NAV_points':old_points+new_minutes,'new_reference_points':0,'action':'Append only the 60 already-closed minute marks before the next 2026-10-12 00:01 UTC daily decision. No order, signal evaluation, forced exit, or past open fill is reconstructed. Beyond that missed decision, leave this shadow state unchanged until separately authorized/eligible input.'},'limitations':'Retrieved after the historical cutoff; label every mark delayed-shadow reconstruction. This is not the 10-strategy live-public-quote simulator and contributes no BTC/ETH research backtest outcome.'}
(T/'spec.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n')
old_batch=json.loads((S/'forward_batch.json').read_text());new=[]
for b in old_batch:
 sp=json.loads((R/b['spec']).read_text());sp['parameters']['end_utc']=cut;sp['validation_plan']=str((T/'spec.json').relative_to(R));path=T/'specs'/(b['name']+'.json');path.write_text(json.dumps(sp,indent=2,ensure_ascii=False)+'\n')
 result=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(path.relative_to(R))],cwd=R,capture_output=True,text=True)
 if result.returncode:raise SystemExit('reserve failed '+b['name']+' '+result.stdout+result.stderr)
 new.append({'name':b['name'],'fingerprint':registry.fingerprint(sp),'spec':str(path.relative_to(R)),'asset':b.get('asset'),'capital_usdt':b['capital_usdt']})
(T/'forward_batch.json').write_text(json.dumps(new,indent=2)+'\n')
print(json.dumps({'reserved':len(new),'resume':begin,'cutoff':cut,'new_minute_marks':new_minutes,'next_daily_decision':state['next_daily_decision_utc']}))
