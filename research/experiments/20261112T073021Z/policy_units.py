"""Known synthetic closed-close volatility, entry scope, strict cap and future-value guards."""
import ast,copy,math,statistics,sys
from decimal import Decimal as D
from fractions import Fraction as F
from common import *
import engine
def run():
 if '--future-close' in sys.argv:
  src=(R/'engine.py').read_text();fn=next(n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name=='btc_entry_sigma');body=ast.get_source_segment(src,fn);needle='for j in range(i-window,i)])';assert body.count(needle)==1;exec(compile(src.replace(body,body.replace(needle,'for j in range(i-window+1,i+1)])')),str(R/'engine.py'),'exec'),engine.__dict__)
 if '--gate-existing' in sys.argv:
  src=(R/'engine.py').read_text();needle='wanted=entry_filter(raw,actual,sigma,cap)';assert src.count(needle)==2;exec(compile(src.replace(needle,'wanted=0 if raw and sigma>cap else raw',1),str(R/'engine.py'),'exec'),engine.__dict__)
 cases=0;i=33
 for V in [6,10,14]:
  for cap in [.03,.04,.05]:
   sp={'parameters':{'lookback_days':29,'return_hurdle':.03,'exit_buffer_fraction':.01,'entry_volatility_window_days':V,'entry_volatility_ceiling':cap,'entry_volatility_gate_scope':'new_or_reversed_position_only'}}
   for direction in [1,-1]:
    closes=[D('100')]*50
    for j in range(i-V,i):closes[j]=D('130' if j%2 else '80') if direction==1 else D('60' if j%2 else '90')
    closes[i-1]=D('130') if direction==1 else D('60');closes[i]=D('100');m={'asset':'BTC','closes':closes};xs=[math.log(float(closes[j])/float(closes[j-1])) for j in range(i-V,i)];mean=math.fsum(xs)/V;independent=math.sqrt(math.fsum((x-mean)**2 for x in xs)/(V-1));assert independent>cap
    for actual in [-1,0,1]:
     wanted,z=engine.decide(sp,m,i,actual);assert z['raw_desired_before_entry_filter']==direction and wanted==(actual if actual==direction else 0),'Known entry/hold direction';assert abs(z['observed_sample_logvol']-independent)<1e-12 and z['entry_filter_applied']==(actual!=direction),'Known unbiased closed-close volatility'
     future=copy.deepcopy(m)
     for j in range(i,len(closes)):future['closes'][j]=D('9999999') if j%2 else D('.0001')
     assert engine.decide(sp,future,i,actual)==(wanted,z),'Future closes influenced entry volatility';cases+=1
 # Exactly equal cap must pass, and existing position must survive high observed sigma.
 for raw in [-1,1]:
  assert engine.entry_filter(raw,0,.04,.04)==raw and engine.entry_filter(raw,0,.04000001,.04)==0 and engine.entry_filter(raw,raw,.50,.04)==raw
 assert engine.entry_filter(0,1,.50,.04)==0
 put(R/'policy_primitive_verification.json',{'passed':True,'synthetic_only':True,'known_scope_and_future_cases':cases,'both_directions_and_flat_new_reverse_hold_checked':True,'unbiased_sample_variance_independent_fsum':True,'strict_cap_equality_passes':True,'future_closes_changed_no_effect':True,'actual_market_or_account_evaluations':0});print('PASS',cases,'syntheticBTCvolpolicycases,strictcap/sameq/exit/futureguards')
if __name__=='__main__':run()
