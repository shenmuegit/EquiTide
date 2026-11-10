"""Synthetic causal median M/F neighborhoods, boundaries and account-capital controls."""
import copy,sys
from decimal import Decimal as D
from fractions import Fraction as F
import numpy as np
from common import *
import engine,run
from portfolio import sum_aligned_full_banks
negative=any(x.startswith('--negative-control') for x in sys.argv);btc=np.array([3750.,4000.,3800.]);eth=np.array([15000.,14700.,15600.]);axis=np.array([0,16,32]);sn=33*DAY
if '--negative-control-double-weighting' in sys.argv:assert (.2*btc+.8*eth)[0]==18750,'Double weighting fails actual whole-bank capital'
original=engine.median_funding
if '--negative-control-mean-instead-of-median' in sys.argv:
 def wrong(events,sn,count):
  e=original(events,sn,count)
  if e:e['median_rate']=sum(x['realized_rate'] for x in e['events'])/D(count)
  return e
 engine.median_funding=wrong
if '--negative-control-future-funding' in sys.argv:
 def future(events,sn,count):
  chosen=sorted(events,key=lambda x:x['settlement_ts'],reverse=True)[:count];rates=sorted(e['realized_rate'] for e in chosen);mid=count//2
  return {'events':chosen,'count':count,'median_rate':rates[mid] if count%2 else (rates[mid-1]+rates[mid])/2}
 engine.median_funding=future
assert np.array_equal(sum_aligned_full_banks([btc,eth],[axis,axis]),btc+eth)
try:sum_aligned_full_banks([btc,eth],[axis,axis+1])
except AssertionError:pass
else:raise AssertionError('Shiftedaxisaccepted')
p={'funding_counts':[2,3,4],'carry_ratios':[.005,.0075,.01]};g=lambda m,f,sc:{'L':5,'H':.02,'E':.0075,'R':f,'M':m,'S':16,'K':.0075,'VC':.05,'D':3,'N':1000 if sc=='parent' else 4500,'fingerprint':f'{sc}/{m}/{f}','readonly':False};p['grid']=[g(m,f,'parent') for m in p['funding_counts'] for f in p['carry_ratios']];p['native_grid']=[g(m,f,'native') for m in p['funding_counts'] for f in p['carry_ratios']];full={z['fingerprint']:{'name':z['fingerprint']} for z in p['grid']+p['native_grid']};cases=[]
for sc,grid in [('parent',p['grid']),('native',p['native_grid'])]:
 for z in grid:
  old={'criteria':{'sentinel':False}};saved=copy.deepcopy(old);c=run.current_grid_row(old,z,sc);assert old==saved and c['M']==z['M'];ns=run.neighborhood(c,p,full);assert len(ns)==(2 if z['M'] in [2,4] else 3)*(3 if z['R']==.0075 else 2);cases.append({'scope':sc,'M':z['M'],'R':z['R'],'neighbors':len(ns)})
events=[{'settlement_ts':sn-age*HOUR,'available_ts':sn-(age-1)*HOUR,'realized_rate':D(rate),'source_index':j,'entry_interval_hours':D(8)} for j,(age,rate) in enumerate([(8,'-.0002'),(16,'.0001'),(24,'.0003'),(32,'.0007')])];future={'settlement_ts':sn+HOUR,'available_ts':sn+2*HOUR,'realized_rate':D('999'),'source_index':9};maturity=0;median_cases=0
for count in [2,3,4]:
 z=engine.median_funding(events+[future],sn,count);picked=events[:count];rates=sorted(F(x['realized_rate']) for x in picked);expected=rates[count//2] if count%2 else (rates[count//2-1]+rates[count//2])/2;assert z['events']==picked and F(z['median_rate'])==expected and z['count']==count;median_cases+=1
 assert engine.median_funding(events[:count-1],sn,count) is None
 perm=list(reversed(events))+[{**future,'available_ts':sn-1}];assert engine.median_funding(perm,sn,count)==z;median_cases+=1
for age,delay,valid in [(HOUR,HOUR,True),(HOUR-1,0,False),(36*HOUR,HOUR,True),(36*HOUR+1,HOUR,False),(8*HOUR,9*HOUR,False),(8*HOUR,8*HOUR,True)]:
 e={**events[0],'settlement_ts':sn-age,'available_ts':sn-age+delay};other=[{**events[1],'settlement_ts':sn-2*HOUR,'available_ts':sn-HOUR}];z=engine.median_funding([e,*other],sn,2);assert (z is not None)==valid;maturity+=1
fund_cases=0
for count in [2,3,4]:
 for cap in [D('.00005'),D('.000075'),D('.0001')]:
  for raw in [-1,0,1]:
   for actual in [-1,0,1]:
    for rate in [-cap-D('.00000001'),-cap,D(0),cap,cap+D('.00000001')]:
     ev=engine.median_funding([{**x,'realized_rate':rate} for x in events],sn,count);want=0 if raw and raw!=actual and max(D(raw)*rate,D(0))>cap else raw;v,a=engine.funding_filter(raw,actual,ev,sn,cap);assert v==want and a['blocked']==bool(raw and raw!=actual and max(D(raw)*rate,D(0))>cap);fund_cases+=1
    assert engine.funding_filter(raw,actual,None,sn,cap)[0]==(0 if raw and raw!=actual else raw)
sp={'parameters':{'lookback_days':5,'trend_lookback_days':16,'trend_slope_lag_days':3,'trend_slope_hurdle_fraction':.0075,'entry_volatility_window_days':10,'entry_volatility_ceiling':.05,'exit_buffer_fraction':.0075,'return_hurdle':.02,'long_entry_return_hurdle':.02,'short_entry_return_hurdle':.02,'trend_estimator':'finite_normalized_exponentially_weighted_mean_slope','trend_decay_numerator':15,'trend_decay_denominator':17,'trend_window_days':16,'trend_gate_scope':'new_or_reversed_position_only','entry_funding_outflow_cap':.0002,'entry_funding_volatility_ratio':.0075,'entry_funding_settlement_count':3}};causal=boundary=0
for count in [2,3,4]:
 sp['parameters']['entry_funding_settlement_count']=count
 for actual in [-1,0,1]:
  m={'asset':'ETH','closes':[D(100)+D(j%8)*D('.2') for j in range(33)],'frame':{'available_ts':{33*1440-1:sn}},'signal_funds':copy.deepcopy(events)};got=engine.decide(sp,m,33,actual);m['closes'] += [D(1),D(999999)];m['signal_funds'] += [future];assert engine.decide(sp,m,33,actual)==got;causal+=1
 for roc,w in [(F('.019999'),0),(F('.02'),0),(F('.020001'),-1),(-F('.020001'),1),(-F('.02'),0),(-F('.019999'),0)]:
  m={'asset':'ETH','closes':[D(100)]*33,'frame':{'available_ts':{33*1440-1:sn}},'signal_funds':copy.deepcopy(events)};m['closes'][-1]=D(100)*(1+D(roc.numerator)/D(roc.denominator));assert engine.decide(sp,m,33,0)[1]['ungated_desired']==w;boundary+=1
if not negative:put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'raw_weights':[1,1],'fixed_capital':18750,'joint_M_F_neighborhoods':cases,'causal_cases':causal,'strict_entry_boundary_cases':boundary,'exact_median_and_permutation_cases':median_cases,'funding_age_availability_boundary_cases':maturity,'funding_entry_retention_threshold_cases':fund_cases,'missing_required_records_block_new_entry':True,'future_price_and_funding_invariance':True,'even_median_uses_arithmetic_middle_pair':True,'native_and_parent_two_axes':True})
print('PASS18M/Fneighborhoods,exactodd/evenmedian,6causalageboundaries,405fundthreshold/retentionandfutureinvariance;0marketvaluations')

exec((R/'review/test_relative_budget.py').read_text(),{'__file__':str(R/'review/test_relative_budget.py')})
