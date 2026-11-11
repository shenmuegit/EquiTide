import sys
from pathlib import Path
from decimal import Decimal as D
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));import engine
assert hasattr(engine,'carry_cap'), 'Missing volatility-relative funding budget'
assert engine.carry_cap(.03,.0075,{'events':[{'entry_interval_hours':D(8)}]})==D('.000075')
assert engine.carry_cap(.2,.01,{'events':[{'entry_interval_hours':D(8)}]})==D('.0002')
assert engine.carry_cap(.03,.0075,None) is None
assert engine.carry_cap(.03,.0075,{'events':[{'entry_interval_hours':None}]}) is None
assert engine.carry_cap(.03,.0075,{'events':[{'entry_interval_hours':D('7.999999722222222222222222222')} ]}) < D('.000075')
print('PASS relative budget,hard ceiling,missing source,and actual interval jitter')
