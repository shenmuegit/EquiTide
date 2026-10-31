"""Synthetic alignment/raw-capital checks, never financial evidence."""
import numpy as np
from common import *
from market import parent
start=100;ts=np.array([100,101,101,102],dtype=np.int64);codes=np.array([0,3,4,1],dtype=np.int8);keys=parent.keys(ts,codes,start);assert keys.tolist()==[0,19,20,33]
other=np.array([0,20,33]);union=np.union1d(keys,other);ix=np.searchsorted(other,union,side='right')-1;assert ix.tolist()==[0,0,1,2] and np.all(other[ix]<=union)
b=np.array([10000,10100,9900,10200.]);e=np.array([10000,9900,10050,9800.]);w=[.5,1.5];v=w[0]*b+w[1]*e;assert v[0]==20000 and np.array_equal(v,np.array([20000,19900,20025,19800.]))
assert (.5*b+.5*e)[0]==10000 and (1.5*b+e)[0]==25000
assert np.allclose((.5*b+.5*e)/10000,(1.5*b+1.5*e)/30000)
assert max(1-v/np.maximum.accumulate(v))>0 and not np.isclose(max(1-v/np.maximum.accumulate(v)),.5*max(1-b/np.maximum.accumulate(b))+1.5*max(1-e/np.maximum.accumulate(e)))
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'cases':['integer pre/post funding key order','lastcompleted projection no future fill','raw funded interest capital not normalized','same source ratio dependent returns','whole combined DD not averaged component DD']});print('PASS5synthetic rawweight/alignment/risk cases')
