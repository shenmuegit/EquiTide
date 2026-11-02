"""Synthetic strict exit boundaries, entry precedence, causal filtering and old-grid regressions."""
import copy,math,sys
from decimal import Decimal as D
from common import *
import engine
if '--legacy-exit-range' in sys.argv:engine=module(ROOT/'research/experiments/20261102T180230Z/engine.py','legacy_fixed_exit_policy')
base={'parameters':{'lookback_days':3,'trend_lookback_days':28,'entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.00375,'return_hurdle':.025,'long_entry_return_hurdle':.015}}
def fixture(L,r,side):
 closes=[D(100)]*45;closes[16]=D(60 if side==1 else 200);closes[-1]=D(100)*(1+D(str(r)));assert closes[44-L]==100
 return {'asset':'ETH','closes':closes}
try:w,_=engine.decide(base,fixture(3,0,1),45,1)
except AssertionError as e:raise AssertionError('Predeclared E0.375percent must be admitted; old sparse E range range is insufficient') from e
assert w==1
cases=[];eps=D('.000001')
for L in [3,4,5]:
 for E in [.00375,.005,.00625]:
  sp=copy.deepcopy(base);sp['parameters'].update(lookback_days=L,exit_buffer_fraction=E);e=D(str(E))
  tests=[(1,e-eps,1,1,'long_below_exit'),(1,e,1,0,'long_equal_exit'),(1,e+eps,1,0,'long_above_exit'),(-1,-e+eps,-1,-1,'short_above_exit'),(-1,-e,-1,0,'short_equal_exit'),(-1,-e-eps,-1,0,'short_below_exit'),(0,-D('.015'),1,0,'long_entry_equality'),(0,-D('.015')-eps,1,1,'long_strict_entry'),(0,D('.025'),-1,0,'short_entry_equality'),(0,D('.025')+eps,-1,-1,'short_strict_entry'),(1,D('.025')+eps,-1,-1,'flip_short_precedence'),(-1,-D('.015')-eps,1,1,'flip_long_precedence'),(1,0,-1,0,'wrong_slow_gate_exits_long'),(-1,0,1,0,'wrong_slow_gate_exits_short')]
  for actual,rr,side,expected,label in tests:
   m=fixture(L,rr,side);wanted,a=engine.decide(sp,m,45,actual);assert wanted==expected,(L,E,label,wanted,a);assert a['exit_buffer_fraction']==E and a['volatility_window_days']==10 and a['entry_volatility_ceiling']==.045
   future=copy.deepcopy(m);future['closes'].extend([D('999999'),D('.001')]);assert engine.decide(sp,future,45,actual)==(wanted,a)
   outside=copy.deepcopy(m);outside['closes'][0]*=D(100);assert engine.decide(sp,outside,45,actual)==(wanted,a)
   cases.append({'L':L,'E':E,'actual':actual,'return':str(rr),'slow_sign':side,'expected':expected,'case':label,'future_and_outside_invariant':True})
  for side in [1,-1]:
   V=10;sigma=.0525;b=-.025;a=sigma*math.sqrt((V-1)/2);xs=[b+a,b-a]+[b]*(V-2);xs=xs if side==1 else [-x for x in xs];closes=[D(60 if side==1 else 200)]*17+[D(100)]*18
   for x in xs:closes.append(D(str(float(closes[-1])*math.exp(x))))
   m={'asset':'ETH','closes':closes};assert len(closes)==45
   assert engine.decide(sp,m,45,0)[0]==0 and engine.decide(sp,m,45,-side)[0]==0 and engine.decide(sp,m,45,side)[0]==side
   cases.append({'L':L,'E':E,'case':'highvol_fresh_flip_blocked_same_retained','side':side})
assert engine.entry_filter(1,0,.045,.045)==1 and engine.entry_filter(-1,0,.045001,.045)==0 and engine.entry_filter(1,1,.045001,.045)==1
import run
plan={'lookbacks':[3,4,5],'exit_buffers':[.00375,.005,.00625]};grid=[{'L':L,'E':E,'H':.025,'readonly':E==.005,'fingerprint':str((L,E))} for L in plan['lookbacks'] for E in plan['exit_buffers']];plan.update(grid=grid,native_grid=grid);full={g['fingerprint']:{'name':g['fingerprint']} for g in grid};metadata=[]
for scope in ['native','parent']:
 for g in grid:
  old={'L':g['L'],'criteria':{'sentinel':False},'sensitivity':{'sentinel':17},'HS':.025,'HL':.015,'VC':.045};preserved=copy.deepcopy(old);cur=run.current_grid_row(old,g,scope);assert cur['E']==g['E'] and cur['VW']==10 and old==preserved and cur['criteria']==old['criteria'] and cur['sensitivity']==old['sensitivity'];n=run.neighborhood(cur,plan,full);expected=(2 if g['L'] in [3,5] else 3)*(2 if g['E'] in [.00375,.00625] else 3);assert len(n)==expected;metadata.append({'scope':scope,'L':g['L'],'E':g['E'],'old_axis_absent_handled':True,'neighbors':len(n),'canonical_fields_unchanged':True})
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'policy_cases':cases,'old_grid_metadata_cases':metadata,'extra_checks':['Strict positive exit-buffer equality exits, entry precedence and slowgate','fixedV10/cap.045 highvol fresh/flip blocked but actualsameposition retained','cap equality admitted','future andunusedolder prices cannot affectdecision','18old-gridfixtures preservequalifications']})
print('PASS',len(cases),'policy fixtures and',len(metadata),'old-grid fixtures; nofinancialvaluation')
