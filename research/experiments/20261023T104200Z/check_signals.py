"""Synthetic exact-boundary and state/cause checks;no financial config evaluated."""
from decimal import Decimal as D
from fractions import Fraction as F
from run import decision,SPAN,POINTS

def main():
 # Exact3daydrop boundary is excluded;strictly larger drop enters.
 v=[D(100),D(99),D(98),D(94)];assert decision(v,4,.06,4,None)['action']=='cash'
 v[-1]=D('93.999');assert decision(v,4,.06,4,None)['action']=='entry'
 pos={'entry_index':4,'entry_signal_close':'90','shock_start_close':'100'}
 # Half recovery is arithmetic price95,not a5% return off90; equality exits.
 v=[D(100)]*8;v[4]=D(95);z=decision(v,5,.06,4,pos);assert z['action']=='exit' and z['half_recovery_hit'] and z['holding_age_days']==1
 v[4]=D('94.999');z=decision(v,5,.06,4,pos);assert z['action']=='hold' and not z['half_recovery_hit']
 # Timeout counts actual execution intervals,not signal bars;it can exit into a new shock.
 v=[D(100)]*9;v[6]=D(70);assert decision(v,7,.06,4,pos)['action']=='hold';v[7]=D(60);z=decision(v,8,.06,4,pos);assert z['action']=='exit' and z['timeout_hit'] and F(z['three_day_return_exact'])<-F('.06')
 # Frozen entry anchors survive a different latest3dayanchor;position input is not mutated.
 v=[D(100)]*8;v[1]=D(1000);v[4]=D(94);before=dict(pos);assert decision(v,5,.06,8,pos)['action']=='hold' and pos==before
 # Future suffix cannot change an available decision;allactualparameter axes checked.
 for drop in [.03,.06,.09]:
  for hold in [2,4,8]:
   a=decision(v,5,drop,hold,pos);b=decision(v+[D(1),D(1000000)],5,drop,hold,pos);assert a==b
 assert SPAN==1442 and POINTS==519123==360*SPAN+3
 print('PASS: strictloss boundary,exact half arithmetic recovery,frozen anchors,actual-execution-age timeout,no same-decision reentry action,future-prefix invariance and nativeOPEN event axis;synthetic only',flush=True)

if __name__=='__main__':main()
