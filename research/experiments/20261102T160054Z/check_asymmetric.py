"""Synthetic variable-volatility-window admission and causal/old-grid regressions."""
import copy,math,sys
from decimal import Decimal as D
from common import *
import engine
if '--legacy-window-range' in sys.argv:engine=module(ROOT/'research/experiments/20261102T115954Z/engine.py','legacy_fixed_V10_policy')
base={'parameters':{'lookback_days':3,'trend_lookback_days':28,'entry_volatility_window_days':5,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.0025,'return_hurdle':.025,'long_entry_return_hurdle':.015}}
def fixture(V,sigma,side):
 b=-.025;a=sigma*math.sqrt((V-1)/2);xs=[b+a,b-a]+[b]*(V-2);xs=xs if side==1 else [-x for x in xs];closes=[D(60 if side==1 else 200)]*17+[D(100)]*(45-V-17)
 for x in xs:closes.append(D(str(float(closes[-1])*math.exp(x))))
 assert len(closes)==45;return {'asset':'ETH','closes':closes}
m=fixture(5,.0375,1)
try:w,_=engine.decide(base,m,45,0)
except AssertionError as e:raise AssertionError('Predeclared volatilitywindow V5 must be admitted; old V10-only range is insufficient') from e
assert w==1
cases=[]
for L in [3,4,5]:
 for VW in [5,10,20]:
  sp=copy.deepcopy(base);sp['parameters'].update(lookback_days=L,entry_volatility_window_days=VW)
  for sigma in [.0375,.0425,.0475,.0525]:
   for side in [1,-1]:
    z=fixture(VW,sigma,side);wanted,a=engine.decide(sp,z,45,0);assert wanted==(side if sigma<.045 else 0);assert abs(a['observed_sample_logvol']-sigma)<1e-12 and a['volatility_window_days']==VW and a['entry_volatility_ceiling']==.045 and a['long_entry_return_hurdle']==.015 and a['short_entry_return_hurdle']==.025
    assert engine.decide(sp,z,45,side)[0]==side and engine.decide(sp,z,45,-side)[0]==wanted
    future=copy.deepcopy(z);future['closes'].extend([D('999999'),D('.001')]);assert engine.decide(sp,future,45,0)==(wanted,a)
    earlier=copy.deepcopy(z);earlier['closes'][45-VW-2]*=D(100);assert engine.decide(sp,earlier,45,0)==(wanted,a)
    cases.append({'L':L,'VW':VW,'observed_sigma':sigma,'side':side,'fresh_and_flip':wanted,'same_position_retained':True,'future_and_out_of_window_invariant':True})
assert engine.entry_filter(1,0,.045,.045)==1 and engine.entry_filter(-1,0,.045001,.045)==0 and engine.entry_filter(1,1,.045001,.045)==1
import run
plan={'lookbacks':[3,4,5],'volatility_windows':[5,10,20]};grid=[{'L':L,'VW':VW,'H':.025,'readonly':VW==10,'fingerprint':str((L,VW))} for L in plan['lookbacks'] for VW in plan['volatility_windows']];plan.update(grid=grid,native_grid=grid);full={g['fingerprint']:{'name':g['fingerprint']} for g in grid};metadata=[]
for scope in ['native','parent']:
 for g in grid:
  old={'L':g['L'],'criteria':{'sentinel':False},'sensitivity':{'sentinel':17},'HS':.025,'HL':.015,'VC':.045};preserved=copy.deepcopy(old);cur=run.current_grid_row(old,g,scope);assert cur['VW']==g['VW'] and cur['VC']==.045 and old==preserved and cur['criteria']==old['criteria'] and cur['sensitivity']==old['sensitivity'];n=run.neighborhood(cur,plan,full);expected=(2 if g['L'] in [3,5] else 3)*(2 if g['VW'] in [5,20] else 3);assert len(n)==expected;metadata.append({'scope':scope,'L':g['L'],'VW':g['VW'],'old_axis_absent_handled':True,'neighbors':len(n),'canonical_fields_unchanged':True})
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'policy_cases':cases,'old_grid_metadata_cases':metadata,'extra_checks':['V5/10/20 admitted','samplevol usesexactlyVW dailylogreturns','fresh/flipfilter vsactualsame-positionretention','fixedcap equality admitted','future andout-of-windowbars cannot changeoutput','18old-gridfixtures preservecanonicalqualification']})
print('PASS72volwindow/side/fastlookback/regime cases and18old-gridfixtures; nofinancialvaluation')
