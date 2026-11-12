"""Known target-zero directional_adverseRMS, allV divisor, independent ETHHorner policy and future guards."""
import ast,copy,math,statistics,sys
from decimal import Decimal as D
from fractions import Fraction as F
from common import *
import engine
def run():
 if '--future-close' in sys.argv or '--ignore-direction' in sys.argv:
  src=(R/'engine.py').read_text();fn=next(n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name=='adverse_sigma');body=ast.get_source_segment(src,fn)
  if '--future-close' in sys.argv:needle='for j in range(i-window,i)';assert body.count(needle)==1;changed=body.replace(needle,'for j in range(i-window+1,i+1)')
  else:needle='min(direction*math.log';assert body.count(needle)==1;changed=body.replace(needle,'min(math.log')
  exec(compile(src.replace(body,changed),str(R/'engine.py'),'exec'),engine.__dict__)
 i=33;known=[-.10,.02,-.03,.04,0,.01];closes=[D(100)]*50
 for j,x in enumerate(known,start=i-6):closes[j]=closes[j-1]*D(str(math.exp(x)))
 for d,expected in [(1,.0109),(-1,.0021)]:assert abs(engine.adverse_sigma(closes,i,6,d)-math.sqrt(expected/6))<1e-12,'Known direction-aware adverse RMS uses raw candidate direction and all V observations'
 positive=[.10,.01,.20,0,.05,.03];up=[D(100)]*50
 for j,x in enumerate(positive,start=i-6):up[j]=up[j-1]*D(str(math.exp(x)))
 assert engine.adverse_sigma(up,i,6,1)==0 and abs(engine.adverse_sigma(up,i,6,-1)-math.sqrt(.0535/6))<1e-12 and engine.adverse_sigma(up,i,6,0)==0 and engine.budget_sigma(up,i,8)>0,'Long and short adverse sides differ; unchanged original funding budget remains samplevol'
 cases=longs=shorts=blocked=allowed=0;template=json.loads((ROOT/'research/experiments/20261112T093127Z/plan.json').read_text());sys.path.insert(0,str(ROOT/'research/automation'));spbase=reg.read_records(ROOT/'research/automation/registry.jsonl')['d2188e34f6d96f2205823e74b834003e1b5d5dd8c2994f0ccd8b72062fed4a53']['spec']
 for V in [5,6,7]:
  for cap in [.035,.045,.055]:
   sp=copy.deepcopy(spbase);sp['parameters'].update(entry_volatility_window_days=V,entry_volatility_ceiling=cap,entry_risk_estimator='candidate_direction_zero_target_adverse_root_mean_square_daily_log_returns',entry_risk_gate_scope='new_or_reversed_position_only');p=sp['parameters']
   for direction in [1,-1]:
    cls=[D(200+direction*4*j) for j in range(50)]
    for j,x in zip([28,29,30,31,32],([312,316,320,290,295] if direction==1 else [88,84,80,98,96])):cls[j]=D(x)
    sn=i*DAY;funds=[{'source_index':j,'settlement_ts':sn-(33-8*j)*HOUR,'available_ts':sn-(32-8*j)*HOUR,'realized_rate':D(0),'entry_interval_hours':D(8)} for j in range(5)];m={'asset':'ETH','closes':cls,'frame':{'available_ts':{i*1440-1:sn}},'signal_funds':funds}
    for actual in [-1,0,1]:
     rr=F(cls[i-1])/F(cls[i-6])-1;h=F('.02');e=F('.0075');base=-1 if rr>h else 1 if rr<-h else actual if actual==1 and rr<e or actual==-1 and rr>-e else 0;beta=F(15,17);total=past=mass=F(0)
     for j in range(i-16,i):total=F(cls[j])+beta*total;mass=1+beta*mass
     for j in range(i-19,i-3):past=F(cls[j])+beta*past
     slow=total/past-1;gate=1 if slow>F('.0075') else -1 if slow<-F('.0075') else 0;raw=base if base==actual or base==gate else 0;xs=[math.log(float(cls[j])/float(cls[j-1])) for j in range(i-V,i)];risk=math.sqrt(sum((raw*x)**2 for x in xs if raw*x<0)/V);want=0 if raw and raw!=actual and risk>cap else raw;wanted,z=engine.decide(sp,m,i,actual)
     assert wanted==want and z['raw_desired_before_entry_filter']==raw and abs(z['observed_directional_adverse_RMS']-risk)<1e-12 and z['adverse_divisor']==V and z['adverse_risk_direction']==raw and z['adverse_target_logreturn']==0,'IndependentETHHorner/directional_adverse/entryscope guard'
     future=copy.deepcopy(m)
     for j in range(i,len(cls)):future['closes'][j]=D('.0001') if j%2 else D('9999999')
     assert engine.decide(sp,future,i,actual)==(wanted,z),'Future closes influenced directional_adverse entry risk'
     cases+=1;longs+=raw==1;shorts+=raw==-1;blocked+=bool(raw and raw!=actual and want==0);allowed+=bool(raw and raw!=actual and want!=0)
 assert longs and shorts and blocked and allowed,(longs,shorts,blocked,allowed)
 for raw in [-1,1]:assert engine.entry_filter(raw,0,.045,.045)==raw and engine.entry_filter(raw,raw,.9,.045)==raw
 assert engine.entry_filter(0,1,.9,.045)==0
 put(R/'policy_primitive_verification.json',{'passed':True,'synthetic_only':True,'independent_ETH_policy_cases':cases,'long_raw_cases':longs,'short_raw_cases':shorts,'blocked_new_reverse_cases':blocked,'allowed_new_reverse_cases':allowed,'known_RMS_sqrt_0109_over6':True,'divisor_allV_and_raw_candidate_direction':True,'positive_variation_longzero_shortrisk_nonzero_originalbudget_nonzero':True,'future_closes_changed_no_effect':True,'strict_equality_and_same_direction_hold_normal_exit_guards':True,'actual_market_or_account_evaluations':0});print('PASS',cases,'syntheticETHHorner/directional_adversepolicycases',longs,shorts,blocked,allowed,'knownRMS/allV/future/scopeguards')
if __name__=='__main__':run()
