"""Adversarial checks: deadband state, strict boundaries and future-price independence."""
from decimal import Decimal as D
from pathlib import Path
from importlib.util import spec_from_file_location,module_from_spec
p=Path(__file__).with_name('signals.py'); s=spec_from_file_location('signals_check',p);m=module_from_spec(s);s.loader.exec_module(m)
x=list(map(D,['100','100','104','102','97','97','120','106','106']))
a=m.hysteresis(x,3,0.02,3,9)
assert [r['long'] for r in a]==[True,True,False,False,True,True]
assert a[1]['action']=='hold_long' and a[4]['action']=='enter'
# A signal at decision4 cannot depend on close4 or anything later.
y=x[:4]+list(map(D,['1','900','1','1','1']))
b=m.hysteresis(y,3,0.02,3,9)
assert a[:2]==b[:2]
# Exact upper/lower boundaries do not switch; start flat, including on a fold boundary.
assert m.hysteresis([D(100)]*4+[D(102)],4,0.02,4,5)[0]['long'] is False
assert m.step(True,D(98),D(100),D('0.02'))==(True,'hold_long')
assert m.step(False,D(102),D(100),D('0.02'))==(False,'hold_cash')
assert m.step(True,D('97.999'),D(100),D('0.02'))==(False,'exit')
print('PASS: strict bands, flat OOS initialization, state persists in deadband; current/future close cannot affect decision')
