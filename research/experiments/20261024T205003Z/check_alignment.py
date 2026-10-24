"""Synthetic millisecond/event order and raw funded-value sum checks."""
import numpy as np
from run import keys,align

def main():
 # Epoch values would overflow if multiplied directly;only relative keys may be packed.
 S=1750000000000000000;ta=np.asarray([S,S+1000000,S+1000000,S+60000000000],dtype=np.int64);ca=np.asarray([0,3,4,9],dtype=np.int8);tb=np.asarray([S,S+2000000,S+2000000,S+60000000000],dtype=np.int64);cb=ca.copy();va=np.asarray([10000,10010,10009,10100]);vb=np.asarray([10000,9990,9989,9900]);axis={'BTC':{'start_ns':S,'ts':ta,'codes':ca,'daily_indices':np.asarray([0,3]),'fold_indices':np.asarray([0,3])},'ETH':{'start_ns':S,'ts':tb,'codes':cb,'daily_indices':np.asarray([0,3]),'fold_indices':np.asarray([0,3])}};u=align(axis);a,b=va[u['projections']['BTC']],vb[u['projections']['ETH']];assert len(u['keys'])==6 and a.tolist()==[10000,10010,10009,10009,10009,10100] and b.tolist()==[10000,10000,10000,9990,9989,9900];v=a+b;assert v[0]==20000 and v[-1]==20000 and v[1]==20010 and v[3]==19999
 assert np.all(keys(ta,ca,S)>=0) and u['projections']['ETH'][1]==0
 assert not np.array_equal(v,.5*a+.5*b),'AlreadyfundedNAVmustnotbeweightedagain'
 print('PASS: nanosecondrelative-keyoverflowguard,millisecondasynchronousfundingpre/postorder,last-knowncausalcarry,nofutureinterpolation,raw1/1funded20000sum;syntheticonly',flush=True)

if __name__=='__main__':main()
