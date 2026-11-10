"""Synthetic independent finite-normalized EWM S/D, fixed H/E boundaries and budget causality."""
import copy,json,math,statistics,sys
from fractions import Fraction as F
from decimal import Decimal as D
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));import engine
P=ROOT/'research/experiments/20261110T131400Z';p=json.loads((P/'plan.json').read_text());ref=p['read_only_references'][p['current_center']['native']];spec=json.loads((ROOT/ref['spec']).read_text());sn=33*engine.DAY
m={'asset':'ETH','closes':[D(100)+D(j%7)*D('.03') for j in range(33)],'frame':{'available_ts':{33*1440-1:sn}},'signal_funds':[{'settlement_ts':sn-age*engine.HOUR,'available_ts':sn-(age-1)*engine.HOUR,'realized_rate':D('.00008'),'entry_interval_hours':D(8),'source_index':j} for j,age in enumerate([8,16,24,32])]}
probe=copy.deepcopy(spec);probe['parameters'].update(trend_lookback_days=12,trend_window_days=12,trend_decay_numerator=11,trend_decay_denominator=13,trend_slope_lag_days=1)
try:engine.decide(probe,m,33,0)
except AssertionError:raise AssertionError('Missing finite S/D parameter domains')
if '--fixed-old-lag-bug' in sys.argv:
 code=(R/'engine.py').read_text();needle='i-1-lag-j';assert needle in code;exec(compile(code.replace(needle,'i-1-3-j'),str(R/'engine.py'),'exec'),engine.__dict__)
checked=0;fixed_budget_by_return={};h,e=F('.02'),F('.0075')
for S in [12,16,20]:
 for lag in [1,3,5]:
  for rr in [-h-F('0.000000001'),-h,-h+F('0.000000001'),-e-F('0.000000001'),-e,-e+F('0.000000001'),F(0),e-F('0.000000001'),e,e+F('0.000000001'),h-F('0.000000001'),h,h+F('0.000000001')]:
   mm=copy.deepcopy(m);mm['closes'][27]=D(100);mm['closes'][32]=D(100)*(D(1)+D(rr.numerator)/D(rr.denominator));sp=copy.deepcopy(spec);sp['parameters'].update(trend_lookback_days=S,trend_window_days=S,trend_decay_numerator=S-1,trend_decay_denominator=S+1,trend_slope_lag_days=lag)
   for actual in [-1,0,1]:
    want,a=engine.decide(sp,mm,33,actual);r=F(mm['closes'][32])/F(mm['closes'][27])-1;assert r==rr
    base=-1 if r>h else 1 if r<-h else actual if actual==1 and r<e or actual==-1 and r>-e else 0;beta=F(S-1,S+1);left=right=mass=F(0)
    for j in range(33-S,33):left=F(mm['closes'][j])+beta*left;mass=1+beta*mass
    for j in range(33-S-lag,33-lag):right=F(mm['closes'][j])+beta*right
    slow=left/right-1;gate=(slow>F('.0075'))-(slow<F('-.0075'));raw=base if base==actual or base==gate else 0;sigma=statistics.stdev([math.log(float(mm['closes'][j])/float(mm['closes'][j-1])) for j in range(23,33)]);pre=0 if raw and raw!=actual and sigma>.05 else raw;fa=a['funding_filter'];out=max(D(pre)*D('.00008'),D(0));expected=0 if pre and pre!=actual and out>D(fa['cap_fraction_per_settlement']) else pre
    assert a['slow_mean_exact']==str(left/mass) and a['slow_reference_mean_exact']==str(right/mass) and F(a['slow_distance_exact'])==slow,'Finite normalized EWM S/D mismatch'
    assert a['ungated_desired']==base and a['slowgate_direction']==gate and a['raw_desired_before_entry_filter']==raw and a['raw_desired_before_funding_filter']==pre and want==expected
    assert a['slow_lookback_days']==S and a['slope_lag_days']==lag and a['long_entry_return_hurdle']==a['short_entry_return_hurdle']==.02 and a['exit_buffer_fraction']==.0075 and fa['budget_volatility_window_days']==8 and fa['budget_ratio']=='0.00875'
    unchanged={k:fa[k] for k in ['budget_sigma_daily','budget_ratio','latest_past_interval_hours','cap_fraction_per_settlement','median_realized_rate','selected_settlements']};key=str(rr)
    if key not in fixed_budget_by_return:fixed_budget_by_return[key]=unchanged
    assert unchanged==fixed_budget_by_return[key]
    future=copy.deepcopy(mm);future['closes']+=[D(1),D(99999)];future['signal_funds']+=[{**m['signal_funds'][0],'settlement_ts':sn+engine.HOUR,'available_ts':sn-engine.HOUR,'realized_rate':D('999')}];assert engine.decide(sp,future,33,actual)==(want,a);checked+=1
assert max(S+lag for S in [12,16,20] for lag in [1,3,5])==25<33
print('PASS',checked,'synthetic Fraction/Horner finiteS12/16/20_D1/3/5;normalizedbeta,width,strictfixedH/E,retention/reversal,futureinvariance,25daycontext;fixedM4/VW8/R.00875 acrossall9;0market/accountvaluations')
