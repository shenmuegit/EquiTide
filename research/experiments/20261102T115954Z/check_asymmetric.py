"""Synthetic variable-volcap admission, actual-position retention and old-grid metadata regression."""
import copy,math,statistics,sys
from decimal import Decimal as D
from common import *
import engine
if '--legacy-cap-range' in sys.argv:engine=module(ROOT/'research/experiments/20261102T095853Z/engine.py','legacy_fixed45cap_policy')
base={'parameters':{'lookback_days':3,'trend_lookback_days':28,'entry_volatility_window_days':10,'entry_volatility_ceiling':.04,'exit_buffer_fraction':.0025,'return_hurdle':.025,'long_entry_return_hurdle':.015}}
def fixture(target_sigma,side):
 a=math.sqrt((9*target_sigma*target_sigma-.00096)/6);xs=[a,-a,a,-a,a,-a,-.02,-.02,-.02,-.02];xs=xs if side==1 else [-x for x in xs];closes=[D(60 if side==1 else 200)]*25+[D(100)]*10
 for x in xs:closes.append(D(str(float(closes[-1])*math.exp(x))))
 assert len(closes)==45;return {'asset':'ETH','closes':closes}
m=fixture(.0375,1)
try:w,_=engine.decide(base,m,45,0)
except AssertionError as e:raise AssertionError('Predeclared VC4% must be admitted by engine; old fixed4.5% range is insufficient') from e
assert w==1
cases=[]
for L in [3,4,5]:
 for VC in [.04,.045,.05]:
  sp=copy.deepcopy(base);sp['parameters'].update(lookback_days=L,entry_volatility_ceiling=VC)
  for sigma in [.0375,.0425,.0475,.0525]:
   for side in [1,-1]:
    z=fixture(sigma,side);wanted,a=engine.decide(sp,z,45,0);assert wanted==(side if sigma<VC else 0);assert abs(a['observed_sample_logvol']-sigma)<1e-12 and a['entry_volatility_ceiling']==VC and a['long_entry_return_hurdle']==.015 and a['short_entry_return_hurdle']==.025
    assert engine.decide(sp,z,45,side)[0]==side and engine.decide(sp,z,45,-side)[0]==wanted
    future=copy.deepcopy(z);future['closes'].extend([D('999999'),D('.001')]);assert engine.decide(sp,future,45,0)==(wanted,a)
    cases.append({'L':L,'VC':VC,'observed_sigma':sigma,'direction':side,'fresh_and_flip':wanted,'same_position_retained':True,'future_invariant':True})
  assert engine.entry_filter(1,0,VC,VC)==1 and engine.entry_filter(-1,0,VC+1e-8,VC)==0 and engine.entry_filter(1,1,VC+1e-8,VC)==1
# Exercise old source records lacking the new axis before any market valuation.
import run
plan={'lookbacks':[3,4,5],'volatility_caps':[.04,.045,.05]};grid=[{'L':L,'VC':VC,'H':.025,'readonly':VC==.045,'fingerprint':str((L,VC))} for L in plan['lookbacks'] for VC in plan['volatility_caps']];plan.update(grid=grid,native_grid=grid);full={g['fingerprint']:{'name':g['fingerprint']} for g in grid};metadata=[]
for scope in ['native','parent']:
 for g in grid:
  old={'L':g['L'],'criteria':{'sentinel':False},'sensitivity':{'sentinel':17},'HS':.025,'HL':.015};preserved=copy.deepcopy(old);cur=run.current_grid_row(old,g,scope);assert cur['VC']==g['VC'] and old==preserved and cur['criteria']==old['criteria'] and cur['sensitivity']==old['sensitivity'];n=run.neighborhood(cur,plan,full);expected=(2 if g['L'] in [3,5] else 3)*(2 if g['VC'] in [.04,.05] else 3);assert len(n)==expected;metadata.append({'scope':scope,'L':g['L'],'VC':g['VC'],'old_axis_absent_handled':True,'neighbors':len(n),'canonical_fields_unchanged':True})
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'policy_cases':cases,'old_grid_metadata_cases':metadata,'extra_checks':['VCrange4/4.5/5admitted','samplelogvol fourstraddlingregimes','fresh/flipfilter vsactualsame-positionretention','VCequality admitted','futurebars nochange','18old-row metadata fixtures preservecanonicalqualifications']})
print('PASS72volcap/side/lookback/regime cases,9exactcapboundaries,18old-row neighborhood fixtures; nofinancialvaluation')
