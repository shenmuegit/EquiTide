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
 print('PASS: signedlong/shortpricePnL,feeonlyopeningcollateral,immutabletradehistory,fundingdirectionandoutflowstress,1xentrycap,participationrejection,strictbandsandfuture-prefixcausality;syntheticonly',flush=True)

if __name__=='__main__':main()
