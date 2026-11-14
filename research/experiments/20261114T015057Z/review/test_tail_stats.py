"""One-day Sharpe is unavailable; multi-day saved formulas must stay bitwise equal."""
import importlib.util,statistics,sys
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2]
path=R/(sys.argv[1] if len(sys.argv)>1 else 'core391.py');sp=importlib.util.spec_from_file_location('tailstatstest',path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
try:z=m.stats(np.array([100.,80.,110.]),[100.,110.],1)
except statistics.StatisticsError:raise AssertionError('A one-day fold must retain net10%, fullDD20%, Sharpe=None rather than crash') from None
assert abs(z['net_return_pct']-10)<1e-12 and abs(z['max_drawdown_pct']-20)<1e-12 and z['sharpe_365'] is None
sp=importlib.util.spec_from_file_location('priorstats',ROOT/'research/experiments/20261113T234922Z/core390.py');old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
for days in [2,5,6,21,30,40,391]:
 v=np.array([100.+j*.02+(-1)**j*.2 for j in range(days+1)]);assert m.stats(v,v.tolist(),days)==old.stats(v,v.tolist(),days)
print('PASS one-day undefinedSharpe,fullpathDD and unchanged multi-day formulas;syntheticonly,0marketbacktests')
