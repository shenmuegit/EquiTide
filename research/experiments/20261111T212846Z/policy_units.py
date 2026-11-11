"""Synthetic two-horizon sample-volatility and complete-close/funding-publication causality."""
import ast,copy,itertools,json,math,sys
from decimal import Decimal as D
from common import *
import engine
if '--price-future' in sys.argv:
 src=(R/'engine.py').read_text();fn=next(n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name=='decide');body=ast.get_source_segment(src,fn);assert body.count('range(i-V,i)')==1;exec(compile(body.replace('range(i-V,i)','range(i-V+1,i+1)'),'<synthetic_price_future_mutant>','exec'),engine.__dict__)
if '--budget-future' in sys.argv or '--population' in sys.argv:
 src=(R/'engine.py').read_text();fn=next(n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name=='budget_sigma');body=ast.get_source_segment(src,fn);body=body.replace('range(i-window,i)','range(i-window+1,i+1)') if '--budget-future' in sys.argv else body.replace('statistics.stdev','statistics.pstdev');exec(compile(body,'<synthetic_budget_volatility_mutant>','exec'),engine.__dict__)
p=json.loads((R/'plan.json').read_text());sp0=json.loads((ROOT/p['read_only_references'][p['current_center']['native']]['spec']).read_text());closes=[D(100)+D('1.7')*i for i in range(35)];closes[28:33]=[D(150),D(148),D(146),D(144),D(142)];sn=100*DAY;interval=8*HOUR+1000000;latest=sn-HOUR;times=[latest,latest-interval,latest-interval-8*HOUR,latest-interval-16*HOUR];rates=['-.00011','-.00009','-.0002','.0001'];funds=[{'settlement_ts':t,'available_ts':t+HOUR,'realized_rate':D(rate),'source_index':j,'entry_interval_hours':D(interval)/D(HOUR) if j==0 else D(8)} for j,(t,rate) in enumerate(zip(times,rates))]
def independent_sigma(w):
 xs=[math.log(float(closes[j])/float(closes[j-1])) for j in range(33-w,33)];mean=math.fsum(xs)/w;return math.sqrt(math.fsum((x-mean)**2 for x in xs)/(w-1))
near=lambda a,b:abs(float(a)-float(b))<=1e-12
cases=0;active=0
for v,vw in itertools.product([5,6,7],[8,10,12]):
 for actual in [-1,0,1]:
  sp=copy.deepcopy(sp0);sp['parameters'].update(entry_volatility_window_days=v,entry_funding_budget_volatility_window_days=vw);m={'asset':'ETH','closes':closes[:],'frame':{'available_ts':{33*1440-1:sn}},'signal_funds':copy.deepcopy(funds)};wanted,a=engine.decide(sp,m,33,actual);fa=a['funding_filter'];assert a['volatility_window_days']==v and near(a['observed_sample_logvol'],independent_sigma(v)) and fa['budget_volatility_window_days']==vw and near(fa['budget_sigma_daily'],independent_sigma(vw));assert fa['budget_ratio']=='0.00875' and D(fa['latest_past_interval_hours'])==D(interval)/D(HOUR) and fa['settlement_count']==4 and D(fa['median_realized_rate'])==D('-.0001');assert wanted==1 and a['raw_desired_before_entry_filter']==1;active+=int(a['entry_filter_applied'])
  future=copy.deepcopy(m);future['closes'][33]=D('99999');future['closes'][34]=D('.001');future['signal_funds'].append({'settlement_ts':sn-HOUR-HOUR//2,'available_ts':sn+1,'realized_rate':D(10),'source_index':999,'entry_interval_hours':D(8)});assert engine.decide(sp,future,33,actual)==(wanted,a);cases+=1
assert active==18
if len(sys.argv)==1:put(R/'policy_primitive_verification.json',{'passed':True,'synthetic_only':True,'cases':cases,'active_new_or_reversed_entry_filter_cases':active,'actual_full_ETH_engine_decide_executed_for_all9_horizon_pairs_and3_directions':True,'price_entry_V_and_funding_budget_VW_distinct_sample_volatilities':True,'independent_sum_squared_deviation_sample_denominator':True,'future_complete_close_and_unpublished_funding_invariance':True,'actual8hour_plus1ms_funding_interval_preserved':True,'fixed_ratio_and_even_signed_median_verified':True,'real_market_or_account_calculations':0})
print('PASS',cases,'synthetic full ETH policy V/VW/direction cases;',active,'active entry filters;0realmarket/accountcalculations')
