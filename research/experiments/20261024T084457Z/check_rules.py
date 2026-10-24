"""Synthetic tests of signed perpetual cash, funding direction, caps and signal causality."""
from decimal import Decimal as D
from engine import trade,funding_amount,target

def main():
 meta={'tick_size':D('.1'),'lot_size':D('.001'),'min_notional':D(50)};flat={'cash':'10000','signed_units':'0','entry_price':'0','entry_reference':'0'}
 for side in [-1,1]:
  s,t=trade(flat,D(side)*2,D(100),D(1000000),D('.01'),meta,1,True);assert t['status']=='filled' and D(s['cash'])>9990 and D(s['signed_units'])==side*2 and flat['cash']=='10000'
  # Entrynotional is not a spotcash debit;closing at favorable20pointmove must realize profit.
  s2,t2=trade(s,-D(side)*2,D(100+side*20),D(1000000),D('.01'),meta,1,False);assert t2['status']=='filled' and D(s2['cash'])>10030 and D(s2['signed_units'])==0
  snapshot=t['state_after']['cash'];s['cash']='1';assert t['state_after']['cash']==snapshot
 assert funding_amount(D(2),D(100),D('.001'),3)==(D('-.2'),D('-.6'))
 assert funding_amount(D(-2),D(100),D('.001'),3)==(D('.2'),D('.2'))
 assert funding_amount(D(-2),D(100),D('-.001'),3)==(D('-.2'),D('-.6'))
 assert funding_amount(D(0),D(100),D('.001'),3)==(D(0),D(0))
 s,t=trade(flat,D(200),D(100),D(100000000),D('.01'),meta,1,True);assert s==flat and t['reason']=='fully_collateralized_1x_entry_cap'
 s,t=trade(flat,D(20),D(100),D(100),D('.01'),meta,1,True);assert s==flat and t['reason']=='participation'
 vals=[D(100)]*21;vals[-1]=D(102);assert target(vals,21,20,.02)[0]==0;vals[-1]=D('102.001');assert target(vals,21,20,.02)[0]==1;vals[-1]=D(98);assert target(vals,21,20,.02)[0]==0;vals[-1]=D('97.999');assert target(vals,21,20,.02)[0]==-1
 for L in [5,10,20]:
  for H in [.01,.02,.04]:assert target(vals,21,L,H)==target(vals+[D(1),D(1000000)],21,L,H)
 # A positive weak trend preserves a long but cannot enter a new long;mirror for a short.
 cases=[('101',1,1),('101',0,0),('99',-1,-1),('99',0,0),('100',1,0),('100',-1,0),('99.9',1,0),('100.1',-1,0),('97',1,-1),('103',-1,1),('102',0,0),('102',1,1),('98',0,0),('98',-1,-1)]
 for close,current,expected in cases:
  z=[D(100)]*21;z[-1]=D(close);assert target(z,21,20,.02,current)[0]==expected,(close,current,expected)
  for current0 in [-1,0,1]:assert target(z,21,20,.02,current0)==target(z+[D(1),D(1000000)],21,20,.02,current0)
 # The existing33-day context covers the new32-day lookback without negative indexing.
 z=[D(100)]*33;z[-1]=D(103)
 for L in [28,29,30,31,32]:
  assert 32-L>=0
  for H in [.01,.02,.04]:
   for current in [-1,0,1]:assert target(z,33,L,H,current)==target(z+[D(1),D(1000000)],33,L,H,current)
 from run import validate_lookback,ROOT,sha
 assert sha(ROOT/'research/experiments/20261023T184400Z/engine.py')==sha(ROOT/'research/experiments/20261024T084457Z/engine.py')
 for L in [28,29,30,31,32]:validate_lookback(L)
 try:validate_lookback(33)
 except AssertionError:pass
 else:raise AssertionError('L33 must be rejected before any financial evaluation')
 print('PASS: unchangedsignedledger/cashcap/funding;zeroexithysteresis;strictbandsandzeroexit;28/29/30/31/32lookbacks fit33daycontext and ignore futuretail;syntheticonly',flush=True)

if __name__=='__main__':main()
