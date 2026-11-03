"""Synthetic slow-window admission, strict boundaries, exact lag and causal warmup regression."""
import copy,math,sys
from decimal import Decimal as D
from common import *
import engine
if '--legacy-slow-range' in sys.argv:engine=module(ROOT/'research/experiments/20261102T220301Z/engine.py','legacy_S28_policy')
base={'parameters':{'lookback_days':3,'trend_lookback_days':26,'entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.005,'return_hurdle':.025,'long_entry_return_hurdle':.015}}
def fixture(L,S,r,side):
 closes=[D(100)]*45;closes[44-S]=D(60 if side==1 else 200);closes[-1]=D(100)*(1+D(str(r)));assert closes[44-L]==100
 return {'asset':'ETH','closes':closes}
try:w,_=engine.decide(base,fixture(3,26,0,1),45,1)
except AssertionError as e:raise AssertionError('Predeclared slow S26 must be admitted; old sparse S admission is insufficient') from e
assert w==1
cases=[];lagcases=[];eps=D('.000001');e=D('.005')
for L in [3,4,5]:
 for S in [26,28,30]:
  sp=copy.deepcopy(base);sp['parameters'].update(lookback_days=L,trend_lookback_days=S)
  tests=[(1,e-eps,1,1,'long_below_exit'),(1,e,1,0,'long_equal_exit'),(1,e+eps,1,0,'long_above_exit'),(-1,-e+eps,-1,-1,'short_above_exit'),(-1,-e,-1,0,'short_equal_exit'),(-1,-e-eps,-1,0,'short_below_exit'),(0,-D('.015'),1,0,'long_entry_equality'),(0,-D('.015')-eps,1,1,'long_strict_entry'),(0,D('.025'),-1,0,'short_entry_equality'),(0,D('.025')+eps,-1,-1,'short_strict_entry'),(1,D('.025')+eps,-1,-1,'flip_short_precedence'),(-1,-D('.015')-eps,1,1,'flip_long_precedence'),(1,0,-1,0,'wrong_slow_gate_exits_long'),(-1,0,1,0,'wrong_slow_gate_exits_short')]
  for actual,rr,side,expected,label in tests:
   m=fixture(L,S,rr,side);wanted,a=engine.decide(sp,m,45,actual);assert wanted==expected,(L,S,label,wanted,a);assert a['slow_lookback_days']==S and a['exit_buffer_fraction']==.005 and a['volatility_window_days']==10
   future=copy.deepcopy(m);future['closes'].extend([D('999999'),D('.001')]);assert engine.decide(sp,future,45,actual)==(wanted,a)
   outside=copy.deepcopy(m);outside['closes'][0]*=D(100);assert engine.decide(sp,outside,45,actual)==(wanted,a)
   cases.append({'L':L,'S':S,'actual':actual,'return':str(rr),'slow_sign':side,'expected':expected,'case':label,'future_and_unused_old_invariant':True})
  for side in [1,-1]:
   V=10;sigma=.0525;b=-.025;a=sigma*math.sqrt((V-1)/2);xs=[b+a,b-a]+[b]*(V-2);xs=xs if side==1 else [-x for x in xs];closes=[D(100)]*35;closes[44-S]=D(60 if side==1 else 200)
   for x in xs:closes.append(D(str(float(closes[-1])*math.exp(x))))
   m={'asset':'ETH','closes':closes};assert len(closes)==45
   assert engine.decide(sp,m,45,0)[0]==0 and engine.decide(sp,m,45,-side)[0]==0 and engine.decide(sp,m,45,side)[0]==side
   cases.append({'L':L,'S':S,'case':'highvol_fresh_flip_blocked_same_retained','side':side})
   rr=-D('.016') if side==1 else D('.026');m=fixture(L,S,rr,side);wanted,a=engine.decide(sp,m,45,0);assert wanted==side
   near=copy.deepcopy(m);near['closes'][44-S-1]=D(1000);near['closes'][44-S+1]=D('.1');assert engine.decide(sp,near,45,0)==(wanted,a)
   neutral=copy.deepcopy(m);neutral['closes'][44-S]=neutral['closes'][-1];assert engine.decide(sp,neutral,45,side)[0]==0
   lagcases.append({'L':L,'S':S,'side':side,'exact_slow_lag_only':True,'equal_slow_return_flat':True})
# Actual evaluation begins at i33; S30 needs exactly31 already completed closes.
warm=copy.deepcopy(base);warm['parameters']['trend_lookback_days']=30;m={'asset':'ETH','closes':[D(60)]+[D(100)]*29+[D(90)]};assert len(m['closes'])==31 and engine.decide(warm,m,31,0)[0]==1
try:engine.decide(warm,{'asset':'ETH','closes':m['closes'][:-1]},30,0)
except AssertionError:pass
else:raise AssertionError('S30 requires31 completed daily closes; no negative-index warmup allowed')
assert engine.decide(warm,{'asset':'ETH','closes':[D(1000),D(1000)]+m['closes']},33,0)[0]==1
assert engine.entry_filter(1,0,.045,.045)==1 and engine.entry_filter(-1,0,.045001,.045)==0 and engine.entry_filter(1,1,.045001,.045)==1
import run
plan={'lookbacks':[3,4,5],'slow_windows':[26,28,30]};grid=[{'L':L,'S':S,'H':.025,'readonly':S==28,'fingerprint':str((L,S))} for L in plan['lookbacks'] for S in plan['slow_windows']];plan.update(grid=grid,native_grid=grid);full={g['fingerprint']:{'name':g['fingerprint']} for g in grid};metadata=[]
for scope in ['native','parent']:
 for g in grid:
  old={'L':g['L'],'criteria':{'sentinel':False},'sensitivity':{'sentinel':17},'HS':.025,'HL':.015,'VC':.045};preserved=copy.deepcopy(old);cur=run.current_grid_row(old,g,scope);assert cur['S']==g['S'] and cur['E']==.005 and cur['VW']==10 and old==preserved and cur['criteria']==old['criteria'] and cur['sensitivity']==old['sensitivity'];ns=run.neighborhood(cur,plan,full);expected=(2 if g['L'] in [3,5] else 3)*(2 if g['S'] in [26,30] else 3);assert len(ns)==expected;metadata.append({'scope':scope,'L':g['L'],'S':g['S'],'old_axis_absent_handled':True,'neighbors':len(ns),'canonical_fields_unchanged':True})
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'policy_cases':cases,'slow_lag_cases':lagcases,'old_grid_metadata_cases':metadata,'S30_earliest_i31_uses31_completed_closes':True,'S30_insufficient30_closes_rejected':True,'extra_checks':['ExactS lag, adjacent older bars cannot change slow direction','Slow-return equality flat','StrictE.005 and entry thresholds, flip,vol gates reused','Future andunusedearlier prices invariant','Old qualification metadata unchanged']})
print('PASS',len(cases),'policy fixtures,',len(lagcases),'slow-lag/equality fixtures,',len(metadata),'old-grid fixtures, S30 warmup boundaries; nofinancialvaluation')
