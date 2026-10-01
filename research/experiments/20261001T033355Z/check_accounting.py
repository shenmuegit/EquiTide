"""Catch funding paid to entrants after settlement, future volume and cost rounding bugs."""
import importlib.util
from pathlib import Path
import sys
s=importlib.util.spec_from_file_location('kernel_test',Path(__file__).with_name('evaluate.py'))
m=importlib.util.module_from_spec(s)
sys.modules[s.name]=m
s.loader.exec_module(m)
# A settlement before entry cannot later be credited to the new position.
events=[{'ts':500,'leg':0,'rate':.001,'mark':100},{'ts':1001,'leg':0,'rate':.001,'mark':100}]
i,amount,detail=m.settle(events,0,1000,[0,0],1)
assert i==1 and amount==0 and detail==[]
i,amount,detail=m.settle(events,i,2000,[10,0],1)
assert i==2 and abs(amount+1)<1e-12
# Positive receipt unchanged under funding stress; outgoing costs scaled only.
assert m.settle(events,1,2000,[-10,0],3)[1]==1
assert m.settle(events,1,2000,[10,0],3)[1]==-3
# A costly roundtrip on unchanged prices cannot manufacture profit.
pb=m.execution_price(100,1,.001,.0001,.0002,0,.1)
ps=m.execution_price(100,-1,.001,.0001,.0002,0,.1)
assert abs(pb-100.1)<1e-9 and abs(ps-99.9)<1e-9
assert ps*(1-.001)-pb*(1+.001)<0
# Complete prior days only: tomorrow's and current incomplete day's volumes excluded.
rows=[{'date':i,'close':100+i,'quote':1000000} for i in range(30)]
v1=m.cost_inputs(rows,20)
changed=[dict(x) for x in rows];changed[20]['quote']=1
assert m.cost_inputs(changed,20)==v1 and v1[0]==1000000
print('PASS: funding settlement ordering/sign/stress, adverse tick rounding, no positive flat-price roundtrip, lagged-only ADV')
