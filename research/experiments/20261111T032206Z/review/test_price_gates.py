"""Independent synthetic PRICE_V/VC sample variance,strict cap/retention/reversal/future audit; no market valuations."""
import copy,json,math,statistics,sys
from fractions import Fraction as F
from decimal import Decimal as D
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));import engine
P=ROOT/'research/experiments/20261111T012135Z';pp=json.loads((P/'plan.json').read_text());spec=json.loads((ROOT/pp['read_only_references'][pp['current_center']['native']]['spec']).read_text());sn=33*engine.DAY
m={'asset':'ETH','closes':[D(100)+D(j%7)*D('.03') for j in range(33)],'frame':{'available_ts':{33*1440-1:sn}},'signal_funds':[{'settlement_ts':sn-age*engine.HOUR,'available_ts':sn-(age-1)*engine.HOUR,'realized_rate':D('.00008'),'entry_interval_hours':D(8),'source_index':j} for j,age in enumerate([8,16,24,32])]}
probe=copy.deepcopy(spec);probe['parameters'].update(entry_volatility_window_days=6 if '--probe-new-cap' in sys.argv else 5,entry_volatility_ceiling=.0525 if '--probe-new-cap' in sys.argv else .055);engine.decide(probe,m,33,0)
if '--fixed-old-price-ceiling-bug' in sys.argv:
 original_filter=engine.entry_filter;engine.entry_filter=lambda raw,actual,sigma,cap:original_filter(raw,actual,sigma,.05)
if '--fixed-old-price-vol-bug' in sys.argv:
 code=(R/'engine.py').read_text();needle='range(i-V,i)';assert needle in code;exec(compile(code.replace(needle,'range(i-8,i)'),str(R/'engine.py'),'exec'),engine.__dict__)
boundaries=0;VC=.055;V=6;L=5;S=16;lag=3
for cap in [.0525,.055,.0575]:
 for raw in [-1,0,1]:
  for actual in [-1,0,1]:
   for sigma in [cap-1e-9,cap,cap+1e-9]:
    want=0 if raw and raw!=actual and sigma>cap else raw;assert engine.entry_filter(raw,actual,sigma,cap)==want,'Independent variablePRICE VC boundary/retention mismatch';boundaries+=1
for slow in [-F('.0075')-F('1e-12'),-F('.0075'),-F('.0075')+F('1e-12'),F('.0075')-F('1e-12'),F('.0075'),F('.0075')+F('1e-12')]:assert engine.slope_gate(slow,F('.0075'))==(slow>F('.0075'))-(slow<-F('.0075'));boundaries+=1
checked=budgets=0;fixed_budget={}
for V in [5,6,7]:
 for VC in [.0525,.055,.0575]:
  H,E,lag,K=.02,.0075,3,.0075
  assert E<H;h,e=F(str(H)),F(str(E))
  for rr in [-h-F('1e-9'),-h,-h+F('1e-9'),-e-F('1e-9'),-e,-e+F('1e-9'),F(0),e-F('1e-9'),e,e+F('1e-9'),h-F('1e-9'),h,h+F('1e-9')]:
   mm=copy.deepcopy(m);mm['closes'][27]=D(100);mm['closes'][32]=D(100)*(1+D(rr.numerator)/D(rr.denominator));sp=copy.deepcopy(spec);sp['parameters'].update(return_hurdle=H,long_entry_return_hurdle=H,short_entry_return_hurdle=H,exit_buffer_fraction=E,trend_slope_lag_days=lag,trend_slope_hurdle_fraction=K,entry_volatility_window_days=V,entry_volatility_ceiling=VC)
   for actual in [-1,0,1]:
    want,a=engine.decide(sp,mm,33,actual);r=F(mm['closes'][32])/F(mm['closes'][27])-1;assert F(a['return_exact'])==r==rr;expected_base=-1 if rr>h else 1 if rr<-h else actual if actual==1 and rr<e or actual==-1 and rr>-e else 0;assert a['ungated_desired']==expected_base,'Independent strict H/E entry/retention mismatch'
    beta=F(15,17);left=right=mass=F(0)
    for j in range(17,33):left=F(mm['closes'][j])+beta*left;mass=1+beta*mass
    for j in range(33-S-lag,33-lag):right=F(mm['closes'][j])+beta*right
    assert a['slow_mean_exact']==str(left/mass) and a['slow_reference_mean_exact']==str(right/mass);slow=left/right-1;assert F(a['slow_distance_exact'])==slow;gate=(slow>F(str(K)))-(slow<-F(str(K)));raw=expected_base if expected_base==actual or expected_base==gate else 0
    xs=[math.log(float(mm['closes'][j])/float(mm['closes'][j-1])) for j in range(33-V,33)];mean=math.fsum(xs)/V;sigma=math.sqrt(math.fsum((x-mean)**2 for x in xs)/(V-1));assert math.isclose(a['observed_sample_logvol'],sigma,rel_tol=1e-12,abs_tol=1e-12),'Independent fixedPRICE V6 sample-vol mismatch';pre=0 if raw and raw!=actual and sigma>VC else raw
    fa=a['funding_filter'];bx=[math.log(float(mm['closes'][j])/float(mm['closes'][j-1])) for j in range(25,33)];budget=min(D('.0002'),D('.00875')*D(str(statistics.stdev(bx)))*D(8)/24);out=max(D(pre)*D('.00008'),D(0));expected=0 if pre and pre!=actual and out>budget else pre
    assert a['long_entry_return_hurdle']==a['short_entry_return_hurdle']==H and a['exit_buffer_fraction']==E and a['fast_lookback_days']==5 and a['slow_lookback_days']==16 and a['slope_lag_days']==lag and a['slope_hurdle_fraction']==K and a['volatility_window_days']==V and a['entry_volatility_ceiling']==VC and a['slowgate_direction']==gate and a['raw_desired_before_entry_filter']==raw and a['raw_desired_before_funding_filter']==pre and want==expected and D(fa['cap_fraction_per_settlement'])==budget
    key=str(rr);z=[fa[k] for k in ['budget_sigma_daily','budget_volatility_window_days','budget_ratio','cap_fraction_per_settlement','median_realized_rate','selected_settlements']]
    if key not in fixed_budget:fixed_budget[key]=z
    assert z==fixed_budget[key];budgets+=1
    future=copy.deepcopy(mm);future['closes']+=[D(1),D(99999)];future['signal_funds']+=[{**m['signal_funds'][0],'settlement_ts':sn+engine.HOUR,'available_ts':sn-engine.HOUR,'realized_rate':D('999')}];assert engine.decide(sp,future,33,actual)==(want,a);checked+=1
fixed=None
for V in [5,6,7]:
 for VC in [.0525,.055,.0575]:
  H,E,lag,K=.02,.0075,3,.0075
  sp=copy.deepcopy(spec);sp['parameters'].update(return_hurdle=H,long_entry_return_hurdle=H,short_entry_return_hurdle=H,exit_buffer_fraction=E,trend_slope_lag_days=lag,trend_slope_hurdle_fraction=K,entry_volatility_window_days=V,entry_volatility_ceiling=VC);fa=engine.decide(sp,m,33,0)[1]['funding_filter'];z=[fa[k] for k in ['budget_sigma_daily','budget_volatility_window_days','budget_ratio','cap_fraction_per_settlement','median_realized_rate','selected_settlements']]
  if fixed is None:fixed=z
  assert z==fixed;budgets+=1
assert max(16+3,21)==21<33
print('PASS',checked,'independent PRICE_V5/6/7_VC5.25/5.5/5.75percent FractionROC/Horner/strict entry/actualretention/reversal/causality;',boundaries,'PRICE/slopestrict checks;',budgets,'fundingVW8 separation checks;ETHsignal19/cost21 covered33;unchanged accounting;PRICE window/cap guards expanded only,0market/accountvaluations')
