"""Independent L/S Fraction/Horner/sample-vol and causal checks on synthetic prices only."""
import copy,json,math,statistics,sys
from fractions import Fraction as F
from decimal import Decimal as D
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));import engine
P=ROOT/'research/experiments/20261110T191703Z';spec=json.loads((P/'specs/lowvolcarry_370_ETH_PV6_VC550.json').read_text());sn=33*engine.DAY
m={'asset':'ETH','closes':[D(100)+D(j%7)*D('.03') for j in range(33)],'frame':{'available_ts':{33*1440-1:sn}},'signal_funds':[{'settlement_ts':sn-age*engine.HOUR,'available_ts':sn-(age-1)*engine.HOUR,'realized_rate':D('.00008'),'entry_interval_hours':D(8),'source_index':j} for j,age in enumerate([8,16,24,32])]}
probe=copy.deepcopy(spec);probe['parameters'].update(lookback_days=4,trend_lookback_days=12,trend_window_days=12,trend_decay_numerator=11,trend_decay_denominator=13)
# Real prior executor already supports both axes; no missing-domain RED or disk edit.
engine.decide(probe,m,33,0)
if '--fixed-old-slow-window-bug' in sys.argv:
 code=(R/'engine.py').read_text();needle='weights=[beta**j for j in range(S)]';assert needle in code;exec(compile(code.replace(needle,'weights=[beta**j for j in range(16)]'),str(R/'engine.py'),'exec'),engine.__dict__)
if '--fixed-old-price-ceiling-bug' in sys.argv:
 original_filter=engine.entry_filter;engine.entry_filter=lambda raw,actual,sigma,cap:original_filter(raw,actual,sigma,.05)
if '--fixed-old-price-vol-bug' in sys.argv:
 code=(R/'engine.py').read_text();needle='range(i-V,i)';assert needle in code;exec(compile(code.replace(needle,'range(i-8,i)'),str(R/'engine.py'),'exec'),engine.__dict__)
boundaries=0;VC=.055;V=6;lag=3
for raw in [-1,0,1]:
 for actual in [-1,0,1]:
  for sigma in [VC-1e-9,VC,VC+1e-9]:
   want=0 if raw and raw!=actual and sigma>VC else raw;assert engine.entry_filter(raw,actual,sigma,VC)==want,'Independent fixedPRICE VC.055 boundary/retention mismatch';boundaries+=1
for strength in [F('.0075')]:
 for slow in [-strength-F('1e-12'),-strength,-strength+F('1e-12'),strength-F('1e-12'),strength,strength+F('1e-12')]:assert engine.slope_gate(slow,strength)==(slow>strength)-(slow<-strength);boundaries+=1
checked=0;budgets=0;fixed_budget={};h,e=F('.02'),F('.0075')
for L in [4,5,6]:
 for S in [12,16,20]:
  for rr in [-h-F('1e-9'),-h,-h+F('1e-9'),-e-F('1e-9'),-e,-e+F('1e-9'),F(0),e-F('1e-9'),e,e+F('1e-9'),h-F('1e-9'),h,h+F('1e-9')]:
   mm=copy.deepcopy(m);mm['closes'][32-L]=D(100);mm['closes'][32]=D(100)*(1+D(rr.numerator)/D(rr.denominator));sp=copy.deepcopy(spec);sp['parameters'].update(lookback_days=L,trend_lookback_days=S,trend_window_days=S,trend_decay_numerator=S-1,trend_decay_denominator=S+1)
   for actual in [-1,0,1]:
    want,a=engine.decide(sp,mm,33,actual);r=F(mm['closes'][32])/F(mm['closes'][32-L])-1;assert F(a['return_exact'])==r==rr,'Independent L ROC mismatch';base=-1 if r>h else 1 if r<-h else actual if actual==1 and r<e or actual==-1 and r>-e else 0
    beta=F(S-1,S+1);left=right=mass=F(0)
    for j in range(33-S,33):left=F(mm['closes'][j])+beta*left;mass=1+beta*mass
    for j in range(33-S-lag,33-lag):right=F(mm['closes'][j])+beta*right
    assert a['slow_mean_exact']==str(left/mass) and a['slow_reference_mean_exact']==str(right/mass),'Independent finite S normalized mean mismatch';slow=left/right-1;assert F(a['slow_distance_exact'])==slow;gate=(slow>F('.0075'))-(slow<F('-.0075'));raw=base if base==actual or base==gate else 0
    xs=[math.log(float(mm['closes'][j])/float(mm['closes'][j-1])) for j in range(33-V,33)];mean=math.fsum(xs)/V;sigma=math.sqrt(math.fsum((x-mean)**2 for x in xs)/(V-1));assert math.isclose(a['observed_sample_logvol'],sigma,rel_tol=1e-12,abs_tol=1e-12),'Independent fixedPRICE V6 sample-vol mismatch';pre=0 if raw and raw!=actual and sigma>VC else raw
    fa=a['funding_filter'];bx=[math.log(float(mm['closes'][j])/float(mm['closes'][j-1])) for j in range(25,33)];budget=min(D('.0002'),D('.00875')*D(str(statistics.stdev(bx)))*D(8)/D(24));out=max(D(pre)*D('.00008'),D(0));expected=0 if pre and pre!=actual and out>budget else pre
    assert a['fast_lookback_days']==L and a['slow_lookback_days']==S and a['slope_lag_days']==3 and a['volatility_window_days']==6 and a['entry_volatility_ceiling']==.055 and a['ungated_desired']==base and a['slowgate_direction']==gate and a['raw_desired_before_entry_filter']==raw and a['raw_desired_before_funding_filter']==pre and want==expected and D(fa['cap_fraction_per_settlement'])==budget
    key=(L,str(rr));z=[fa[k] for k in ['budget_sigma_daily','budget_volatility_window_days','budget_ratio','cap_fraction_per_settlement','median_realized_rate','selected_settlements']]
    if key not in fixed_budget:fixed_budget[key]=z
    assert z==fixed_budget[key];budgets+=1
    future=copy.deepcopy(mm);future['closes']+=[D(1),D(99999)];future['signal_funds']+=[{**m['signal_funds'][0],'settlement_ts':sn+engine.HOUR,'available_ts':sn-engine.HOUR,'realized_rate':D('999')}];assert engine.decide(sp,future,33,actual)==(want,a);checked+=1
fixed=None
for L in [4,5,6]:
 for S in [12,16,20]:
  sp=copy.deepcopy(spec);sp['parameters'].update(lookback_days=L,trend_lookback_days=S,trend_window_days=S,trend_decay_numerator=S-1,trend_decay_denominator=S+1);fa=engine.decide(sp,m,33,0)[1]['funding_filter'];z=[fa[k] for k in ['budget_sigma_daily','budget_volatility_window_days','budget_ratio','cap_fraction_per_settlement','median_realized_rate','selected_settlements']]
  if fixed is None:fixed=z
  assert z==fixed;budgets+=1
assert max(20+3,6+1,21)==23<33
print('PASS',checked,'independent L4/5/6_S12/16/20 FractionROC/Horner finite normalized EWM,beta,width,strict H/E,retention/reversal/futureinvariance;',boundaries,'PRICE/slopestrict boundaries;',budgets,'funding VW8 separation checks;maxETH23days covered33;unchanged executor,0market/accountvaluations')
