"""Synthetic units,non-normalization and money attribution only;not market PnL."""
import copy
import numpy as np
from run import WEIGHTS,owned_parts
A=np.array([10000.,10010.,9990.,10020.]);B=np.array([10000.,9990.,10020.,10040.])
money=['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','gross_reference_price_PnL_usdt']
p=[{**{f:float(i+1) for f in money},'cost_parts_usdt':{k:float(i+1) for k in ['fee','half_spread','slippage','impact','tick_rounding']},'margin':{'minimum_equity_minus_maintenance_usdt':1000.},'executions':4+i,'round_trips':2} for i in range(2)];before=copy.deepcopy(p)
for w in WEIGHTS:
 q=owned_parts(p,[w,2-w]);v=w*A+(2-w)*B;assert v[0]==20000 and not np.array_equal(v,v/2)
 for i,factor in enumerate([w,2-w]):
  for f in money:assert q[i][f]==p[i][f]*factor
  assert q[i]['cost_parts_usdt']=={k:x*factor for k,x in p[i]['cost_parts_usdt'].items()} and q[i]['executions']==p[i]['executions'] and q[i]['round_trips']==p[i]['round_trips']
 assert np.array_equal(v[:2],w*A[:2]+(2-w)*B[:2])
assert p==before
print('PASS5 rawweight-pairs;capital20000,future-prefix invariant,money/cost attribution,unchanged source eventcounts;no order resizing or market evaluation')
