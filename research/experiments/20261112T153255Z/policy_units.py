"""Exact path length/sign, independent ETH policy and future-close negative controls."""
import ast,copy,math,statistics,sys
from decimal import Decimal as D
from fractions import Fraction as F
from common import *
import engine
def run():
 if '--future-close' in sys.argv or '--ignore-direction' in sys.argv:
  src=(R/'engine.py').read_text();fn=next(n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name=='adverse_efficiency');body=ast.get_source_segment(src,fn)
  if '--future-close' in sys.argv:needle='for j in range(i-window,i)';assert body.count(needle)==1;changed=body.replace(needle,'for j in range(i-window+1,i+1)')
  else:needle='max(-direction*net,F(0))';assert body.count(needle)==1;changed=body.replace(needle,'abs(net)')
  exec(compile(src.replace(body,changed),str(R/'engine.py'),'exec'),engine.__dict__)
 i=33;seq=[100,102,101,104,103,106,105,108,107,110,109];cls=[D(100)]*50
 for j,x in enumerate(seq,start=i-11):cls[j]=D(x)
 for direction,expected in [(1,F(0)),(-1,F(9,19)),(0,F(0))]:assert engine.adverse_efficiency(cls,i,10,direction)==expected,'Known adverse path efficiency preserves candidate sign and exact total path denominator'
 for W in [8,10,12]:
  for d in [-1,1]:
   mono=[D(100+d*j) for j in range(50)];assert engine.adverse_efficiency(mono,i,W,-d)==1 and engine.adverse_efficiency(mono,i,W,d)==0
   assert engine.adverse_efficiency([D(100)]*50,i,W,d)==0
   assert engine.adverse_efficiency([x*D(37)+D(17) for x in cls],i,W,d)==engine.adverse_efficiency(cls,i,W,d)
 assert engine.entry_filter(1,0,F(3,5),F('.60'))==1 and engine.entry_filter(-1,1,F(1),F('.60'))==0 and engine.entry_filter(1,1,F(1),F('.60'))==1 and engine.entry_filter(0,1,F(1),F('.60'))==0
 spbase=reg.read_records(ROOT/'research/automation/registry.jsonl')['d2188e34f6d96f2205823e74b834003e1b5d5dd8c2994f0ccd8b72062fed4a53']['spec'];cases=longs=shorts=blocked=allowed=0
 for W in [8,10,12]:
  for cap in [.45,.60,.75]:
   sp=copy.deepcopy(spbase);sp['parameters'].update(entry_path_efficiency_filter='adverse_candidate_price_efficiency',entry_path_efficiency_window_days=W,entry_path_efficiency_ceiling=cap,entry_path_efficiency_scope='new_or_reversed_position_only');p=sp['parameters']
   for direction in [1,-1]:
    for pattern in ['ramp_pullback','jump_adverse_trend']:
     if pattern=='ramp_pullback':
      cls=[D(200+direction*4*j) for j in range(50)]
      for j,x in zip([28,29,30,31,32],([312,316,320,290,295] if direction==1 else [88,84,80,98,96])):cls[j]=D(x)
     else:
      cls=[D(100 if direction==1 else 600)]*50
      for k,j in enumerate(range(i-13,i)):cls[j]=D(500-3*k if direction==1 else 200+3*k)
     sn=i*DAY;funds=[{'source_index':j,'settlement_ts':sn-(33-8*j)*HOUR,'available_ts':sn-(32-8*j)*HOUR,'realized_rate':D(0),'entry_interval_hours':D(8)} for j in range(5)];m={'asset':'ETH','closes':cls,'frame':{'available_ts':{i*1440-1:sn}},'signal_funds':funds}
     for actual in [-1,0,1]:
      rr=F(cls[i-1])/F(cls[i-6])-1;h=F('.02');e=F('.0075');base=-1 if rr>h else 1 if rr<-h else actual if actual==1 and rr<e or actual==-1 and rr>-e else 0;beta=F(15,17);total=past=mass=F(0)
      for j in range(i-16,i):total=F(cls[j])+beta*total;mass=1+beta*mass
      for j in range(i-19,i-3):past=F(cls[j])+beta*past
      slow=total/past-1;gate=1 if slow>F('.0075') else -1 if slow<-F('.0075') else 0;raw=base if base==actual or base==gate else 0;xs=[math.log(float(cls[j])/float(cls[j-1])) for j in range(i-6,i)];mu=math.fsum(xs)/6;sigma=math.sqrt(math.fsum((x-mu)**2 for x in xs)/5);before=0 if raw and raw!=actual and sigma>.05625 else raw;length=sum((abs(F(cls[j])-F(cls[j-1])) for j in range(i-W,i)),F(0));er=max(-raw*(F(cls[i-1])-F(cls[i-1-W])),F(0))/length if length else F(0);want=0 if before and before!=actual and er>F(str(cap)) else before;wanted,z=engine.decide(sp,m,i,actual)
      assert wanted==want and z['raw_desired_before_entry_filter']==raw and z['raw_desired_before_efficiency_filter']==before and z['efficiency_candidate_direction']==raw and F(z['observed_adverse_path_efficiency_exact'])==er and abs(z['observed_sample_logvol']-sigma)<1e-12,'Independent ETH Horner/samplevol/exact path efficiency and entry scope guard'
      future=copy.deepcopy(m)
      for j in range(i,len(cls)):future['closes'][j]=D('.0001') if j%2 else D('9999999')
      assert engine.decide(sp,future,i,actual)==(wanted,z),'Future closes influenced exact path efficiency entry gate'
      cases+=1;longs+=raw==1;shorts+=raw==-1;blocked+=bool(before and before!=actual and want==0);allowed+=bool(before and before!=actual and want!=0)
 assert longs and shorts and blocked and allowed,(longs,shorts,blocked,allowed)
 put(R/'policy_primitive_verification.json',{'passed':True,'synthetic_only':True,'independent_ETH_policy_cases':cases,'long_raw_cases':longs,'short_raw_cases':shorts,'blocked_new_reverse_cases':blocked,'allowed_new_reverse_cases':allowed,'known_exact_adverse_short_9_over19_favorable_long0':True,'monotone_adverse1_favorable0_flat0':True,'scale_and_translation_invariant':True,'original_samplevol_gate_and_funding_budget_retained':True,'future_closes_changed_no_effect':True,'strict_Fraction_equality_and_same_direction_hold_normal_exit_guards':True,'actual_market_or_account_evaluations':0});print('PASS',cases,'synthetic independent ETH policy cases',longs,shorts,blocked,allowed,'exact path/sign/zero/future/scope guards')
if __name__=='__main__':run()
