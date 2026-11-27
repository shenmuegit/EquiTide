"""Preplanned read-only verification for the original candidate's first completed 30-day fold.
The previously bound auditor is unchanged; only its zero-fold assumption and
its diagnostic count are replaced in memory. All ledger/signal/risk checks run.
"""
import ast,copy,hashlib,json,math
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rel=lambda p:str(p.relative_to(ROOT));put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
b=rd(R/'candidate_30day_recovery_binding.json');assert b['bound_before_readonly_execution'] and sha(Path(__file__))==b['source_sha256']
for p,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/p)==h,p
source=ROOT/b['previous_auditor'];text=source.read_text();assert sha(source)==b['previous_auditor_sha256'];assert text.count("len(z['folds'])==0")==1 and text.count("'complete30day_folds':0")==1
checks=[]
def near(a,c):assert abs(float(a)-float(c))<=1e-11*max(1,abs(float(a)),abs(float(c))),(a,c)
def verify_folds(z,rows,daily,asset,cost,start,cut,day,terminal):
 expected=min(6,(cut-start)//(30*day));assert expected==1 and len(z['folds'])==expected
 anchors={int(x['timestamp_ns']):float(x['equity_usdt']) for x in daily[asset][cost]}
 for j,fold in enumerate(z['folds']):
  lo=start+j*30*day;hi=lo+30*day;assert fold['fold']==j+1 and fold['start_ns']==lo and fold['end_exclusive_ns']==hi and fold['duration_days']==30
  vals=[float(x['NAV'][asset][cost]) for x in rows if (lo,0 if j==0 else 5)<=(int(x['timestamp_ns']),int(x['event_code']))<=(hi,9 if hi==terminal else 5)];assert vals and all(math.isfinite(v) and v>0 for v in vals);assert lo in anchors and hi in anchors
  expected_return=100*(anchors[hi]/anchors[lo]-1);peak=vals[0];dd=0.
  for v in vals:peak=max(peak,v);dd=max(dd,100*(1-v/peak))
  near(fold['net_return_pct'],expected_return);near(fold['max_drawdown_pct'],dd)
  checks.append({'asset':asset,'cost':int(cost),'fold':j+1,'start_ns':lo,'end_exclusive_ns':hi,'NAV_points':len(vals),'net_return_pct':expected_return,'max_drawdown_pct':dd})
 return expected
patched=text.replace("len(z['folds'])==0","len(z['folds'])==_verify_completed_folds(z,full,daily,a,k,c.START,cut,c.DAY,c.END)").replace("'complete30day_folds':0","'complete30day_folds':min(6,(cut-c.START)//(30*c.DAY))")
assert hashlib.sha256(patched.encode()).hexdigest()==b['adapted_auditor_sha256'];assert (R/'candidate_30day_adapted_auditor.py.txt').read_text()==patched
ns={'__file__':str(source),'__name__':'readonly_candidate_30day_auditor','_verify_completed_folds':verify_folds};exec(compile(patched,str(source)+'[readonly_completed_fold_check]','exec'),ns);ns['main']('candidate');assert len(checks)==9 and len({(x['asset'],x['cost'],x['fold']) for x in checks})==9
# The fold checker must reject corrupted return, drawdown and time-boundary fields.
report=rd(R/'candidate_observation/report.json');scene=next(iter(next(iter(report['configs'].values()))['scenes'].values()));faults=[]
for field,delta in [('net_return_pct',.1),('max_drawdown_pct',.1),('start_ns',1)]:
 bad=copy.deepcopy(scene);bad['folds'][0][field]+=delta
 # Use the actual fold's independently checked expected quantities for a narrow corruption check.
 q=checks[0]
 try:
  f=bad['folds'][0];assert f['start_ns']==q['start_ns'] and f['end_exclusive_ns']==q['end_exclusive_ns'];near(f['net_return_pct'],q['net_return_pct']);near(f['max_drawdown_pct'],q['max_drawdown_pct'])
 except AssertionError:faults.append(field)
assert faults==['net_return_pct','max_drawdown_pct','start_ns']
for p,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/p)==h,p
put(R/'candidate_30day_recovery_verification.json',{'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'previous_auditor_kept_byteexact':True,'previous_auditor_sha256':b['previous_auditor_sha256'],'adapted_auditor_sha256':b['adapted_auditor_sha256'],'only_legacy_zero_fold_predicate_and_output_count_changed':True,'all_previous_signal_cash_quantity_funding_cost_risk_fullNAV_and_registration_checks_executed':True,'independently_verified_completed_30day_folds':checks,'fault_injection_rejections':faults,'planned_first_audit_attempt':True,'immutable_report_state_delta_pointer_and_registry_hashes_unchanged':True,'new_financial_strategy_or_account_window_executions':0,'completed_candidate_window_replays':0})
print(json.dumps({'passed':True,'original_candidate_complete_folds':1,'independent_asset_cost_fold_checks':len(checks),'corruption_cases_rejected':faults,'financial_or_account_window_replays':0}))
