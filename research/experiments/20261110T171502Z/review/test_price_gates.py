"""Independent Fraction ROC / Horner EWM / sample PRICE vol; funding window is separate."""
import copy,json,math,statistics,sys
from fractions import Fraction as F
from decimal import Decimal as D
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));import engine
P=ROOT/'research/experiments/20261110T151431Z';p=json.loads((P/'plan.json').read_text());ref=p['read_only_references'][p['current_center']['native']];spec=json.loads((ROOT/ref['spec']).read_text());sn=33*engine.DAY
m={'asset':'ETH','closes':[D(100)+D(j%7)*D('.03') for j in range(33)],'frame':{'available_ts':{33*1440-1:sn}},'signal_funds':[{'settlement_ts':sn-age*engine.HOUR,'available_ts':sn-(age-1)*engine.HOUR,'realized_rate':D('.00008'),'entry_interval_hours':D(8),'source_index':j} for j,age in enumerate([8,16,24,32])]}
probe=copy.deepcopy(spec);probe['parameters'].update(lookback_days=4,entry_volatility_window_days=8)
try:engine.decide(probe,m,33,0)
except AssertionError:raise AssertionError('Missing fast ROC L / PRICE volatility V parameter domains')
if '--fixed-old-fast-bug' in sys.argv:
 code=(R/'engine.py').read_text();needle='i-1-L';assert needle in code;exec(compile(code.replace(needle,'i-1-5'),str(R/'engine.py'),'exec'),engine.__dict__)
if '--fixed-old-price-vol-bug' in sys.argv:
 code=(R/'engine.py').read_text();needle='range(i-V,i)';assert needle in code;exec(compile(code.replace(needle,'range(i-10,i)'),str(R/'engine.py'),'exec'),engine.__dict__)
checked=0;budget_checks=0;fixed_budget={};h,e=F('.02'),F('.0075');S,lag=16,3
for L in [4,5,6]:
 for V in [8,10,12]:
  for rr in [-h-F('0.000000001'),-h,-h+F('0.000000001'),-e-F('0.000000001'),-e,-e+F('0.000000001'),F(0),e-F('0.000000001'),e,e+F('0.000000001'),h-F('0.000000001'),h,h+F('0.000000001')]:
   mm=copy.deepcopy(m);mm['closes'][32-L]=D(100);mm['closes'][32]=D(100)*(D(1)+D(rr.numerator)/D(rr.denominator));sp=copy.deepcopy(spec);sp['parameters'].update(lookback_days=L,entry_volatility_window_days=V)
   for actual in [-1,0,1]:
    want,a=engine.decide(sp,mm,33,actual);r=F(mm['closes'][32])/F(mm['closes'][32-L])-1;assert F(a['return_exact'])==r==rr,'Independent fast ROC mismatch'
    base=-1 if r>h else 1 if r<-h else actual if actual==1 and r<e or actual==-1 and r>-e else 0;beta=F(15,17);left=right=mass=F(0)
    for j in range(33-S,33):left=F(mm['closes'][j])+beta*left;mass=1+beta*mass
    for j in range(33-S-lag,33-lag):right=F(mm['closes'][j])+beta*right
    slow=left/right-1;gate=(slow>F('.0075'))-(slow<F('-.0075'));raw=base if base==actual or base==gate else 0
    xs=[math.log(float(mm['closes'][j])/float(mm['closes'][j-1])) for j in range(33-V,33)];mean=math.fsum(xs)/V;sigma=math.sqrt(math.fsum((x-mean)**2 for x in xs)/(V-1));assert math.isclose(a['observed_sample_logvol'],sigma,rel_tol=1e-12,abs_tol=1e-12),'Independent PRICE V sample volatility mismatch'
    pre=0 if raw and raw!=actual and sigma>.05 else raw;fa=a['funding_filter'];bx=[math.log(float(mm['closes'][j])/float(mm['closes'][j-1])) for j in range(25,33)];budget=min(D('.0002'),D('.00875')*D(str(statistics.stdev(bx)))*D(8)/D(24));out=max(D(pre)*D('.00008'),D(0));expected=0 if pre and pre!=actual and out>budget else pre
    assert a['slow_mean_exact']==str(left/mass) and a['slow_reference_mean_exact']==str(right/mass) and F(a['slow_distance_exact'])==slow
    assert a['ungated_desired']==base and a['slowgate_direction']==gate and a['raw_desired_before_entry_filter']==raw and a['raw_desired_before_funding_filter']==pre and want==expected
    assert a['fast_lookback_days']==L and a['volatility_window_days']==V and a['slow_lookback_days']==16 and a['slope_lag_days']==3 and fa['budget_volatility_window_days']==8 and fa['budget_ratio']=='0.00875' and D(fa['cap_fraction_per_settlement'])==budget
    unchanged={k:fa[k] for k in ['budget_sigma_daily','budget_ratio','latest_past_interval_hours','cap_fraction_per_settlement','median_realized_rate','selected_settlements']};key=(L,str(rr))
    if key not in fixed_budget:fixed_budget[key]=unchanged
    assert unchanged==fixed_budget[key];budget_checks+=1
    future=copy.deepcopy(mm);future['closes']+=[D(1),D(99999)];future['signal_funds']+=[{**m['signal_funds'][0],'settlement_ts':sn+engine.HOUR,'available_ts':sn-engine.HOUR,'realized_rate':D('999')}];assert engine.decide(sp,future,33,actual)==(want,a);checked+=1
# Identical past prices => identical funding BUDGET_VW8 for every L/PRICE_V.
fixed=None
for L in [4,5,6]:
 for V in [8,10,12]:
  sp=copy.deepcopy(spec);sp['parameters'].update(lookback_days=L,entry_volatility_window_days=V);fa=engine.decide(sp,m,33,0)[1]['funding_filter'];z=[fa[k] for k in ['budget_sigma_daily','budget_volatility_window_days','budget_ratio','cap_fraction_per_settlement','median_realized_rate','selected_settlements']]
  if fixed is None:fixed=z
  assert z==fixed;budget_checks+=1
assert max(16+3,12+1,21)==21<33
print('PASS',checked,'independent fastL4/5/6_PRICE_V8/10/12 FractionROC/HornerEWM/samplevol/strictH_E/retention/reversal/futureinvariance;',budget_checks,'fundingVW8 separation checks;ETH max19signal/21cost covered33;0market/accountvaluations')
