"""Concrete checks for causality, terminal fees, sleeve weights and fold accounting."""
from datetime import datetime, timezone
from decimal import Decimal as D
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
p=Path(__file__).with_name('evaluate.py')
s=spec_from_file_location('round_evaluate',p)
m=module_from_spec(s)
s.loader.exec_module(m)
base=int(datetime(2026,1,1,tzinfo=timezone.utc).timestamp())*10**9
rows=[{'date':f'2026-01-{i+1:02}', 'close':D(100),'volume':D(1),'quote_volume':D(1000000),'trade_open':D(100),'trade_ts':base+i*m.DAY_NS+m.MINUTE_NS,'close_available_ts':base+(i+1)*m.DAY_NS} for i in range(30)]
# Two executions on unchanged price must lose exactly multiplicative buy/sell costs.
r=m.backtest(rows,[True]*30,20,22,1000,1,1,impact=False)
expected=1000*(1-.0003)*(1-.001)/((1+.0003)*(1+.001))
assert abs(r['equity_usdt'][-1]-expected)<1e-9
assert r['executions']==2 and r['cost_usdt']>0
# Permanent cash sleeve must never be exposed; terminal outcome is affine, not rebalance.
h=m.backtest(rows,[True]*30,20,22,1000,.5,1,impact=False)
assert abs(h['equity_usdt'][-1]-(500+.5*expected))<1e-9
# Entry uses only prior close; change today's close cannot change today's decision.
x=[D(v) for v in [1,2,3,4,100]]
y=x[:4]+[D(-100)]
assert m.sma_signals(x,3)[4]==m.sma_signals(y,3)[4]
# Costs must use historical ADV/volatility: modifying today's/future volume has no effect.
r2=[dict(x) for x in rows]
r2[20]['quote_volume']=D(1)
assert m.lagged_cost_inputs(rows,20)==m.lagged_cost_inputs(r2,20)
assert m.lagged_cost_inputs(rows,20)[0]==1000000
bad=[dict(x) for x in rows]
bad[19]['close_available_ts']=bad[20]['trade_ts']+1
try:
 m.backtest(bad,[True]*30,20,22,1000,1,1,impact=False)
 raise AssertionError('future close accepted')
except ValueError as e:
 assert 'available' in str(e)
# Fold returns telescope over the continuous OOS curve and include final liquidation.
a=m.fold_metrics([100,110,99,105,103],[{'test_start_index':0,'test_end_exclusive_index':2},{'test_start_index':2,'test_end_exclusive_index':4}],0)
assert abs((1+a[0]['net_return_pct']/100)*(1+a[1]['net_return_pct']/100)-1.03)<1e-12
print('PASS: prior-only signals/cost inputs, next executable quote, exact terminal accounting, fixed sleeves, continuous folds')
