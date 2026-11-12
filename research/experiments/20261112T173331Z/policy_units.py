"""Exact completed UTC daily CLV/sign/mean/flat-range and future-bar policy tests."""
import ast,copy,math,sys
from decimal import Decimal as D
from fractions import Fraction as F
import numpy as np
import polars as pl
from common import *
import engine
def frame(closes,profiles,width=D(20)):
 highs=[c+width*(1-z)/2 for c,z in zip(closes,profiles)];lows=[c-width*(1+z)/2 for c,z in zip(closes,profiles)];n=len(closes)*1440
 return pl.DataFrame({'high':pl.Series(np.repeat(np.array(highs,dtype=object),1440).tolist(),dtype=pl.Decimal(38,18)),'low':pl.Series(np.repeat(np.array(lows,dtype=object),1440).tolist(),dtype=pl.Decimal(38,18)),'available_ts':(np.arange(n,dtype=np.int64)+1)*MIN})
def run():
 if '--future-close' in sys.argv or '--ignore-direction' in sys.argv:
  src=(R/'engine.py').read_text();fn=next(n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name=='candidate_clv');body=ast.get_source_segment(src,fn)
  if '--future-close' in sys.argv:needle='for j in range(i-window,i)';assert body.count(needle)==1;changed=body.replace(needle,'for j in range(i-window+1,i+1)')
  else:needle='return direction*sum(scores,F(0))/window';assert body.count(needle)==1;changed=body.replace(needle,'return sum(scores,F(0))/window')
  exec(compile(src.replace(body,changed),str(R/'engine.py'),'exec'),engine.__dict__)
 i=33;cls=[D(115)]*50;bars=pl.DataFrame({'high':pl.Series([D(118)]*(50*1440),dtype=pl.Decimal(38,18)),'low':pl.Series([D(102)]*(50*1440),dtype=pl.Decimal(38,18)),'available_ts':(np.arange(50*1440,dtype=np.int64)+1)*MIN}).with_row_index('row')
 bars=bars.with_columns(pl.when(pl.col('row')%1440==719).then(pl.lit(D(120),dtype=pl.Decimal(38,18))).otherwise(pl.col('high')).alias('high'),pl.when(pl.col('row')%1440==1039).then(pl.lit(D(100),dtype=pl.Decimal(38,18))).otherwise(pl.col('low')).alias('low'));m={'closes':cls,'frame':bars}
 for W in [1,2,3]:
  for direction in [-1,0,1]:assert engine.candidate_clv(m,i,W,direction)==F(direction,2),'Known completed UTC daily CLV uses full intraday extrema and candidate sign'
 flat=[D(100)]*50
 for W in [1,2,3]:assert engine.candidate_clv({'closes':flat,'frame':frame(flat,[D(0)]*50,D(0))},i,W,1)==0
 profiles=[D(0)]*50;profiles[i-3:i]=[D('.5'),D('-.5'),D('.25')];assert engine.candidate_clv({'closes':cls,'frame':frame(cls,profiles)},i,3,1)==F(1,12),'Exact unweighted daily mean CLV,not range-weighted or summed'
 spbase=reg.read_records(ROOT/'research/automation/registry.jsonl')['d2188e34f6d96f2205823e74b834003e1b5d5dd8c2994f0ccd8b72062fed4a53']['spec'];fixtures=[]
 for direction in [1,-1]:
  cls=[D(100 if direction==1 else 600)]*50
  for k,j in enumerate(range(i-13,i)):cls[j]=D(500-3*k if direction==1 else 200+3*k)
  for profile in [D('-.5'),D('-.25'),D(0),D('.25'),D('.5')]:fixtures.append((direction,profile,cls,frame(cls,[profile]*50)))
 cases=longs=shorts=blocked=allowed=equal_allowed=0
 for W in [1,2,3]:
  for minimum in [0,.25,.5]:
   sp=copy.deepcopy(spbase);sp['parameters'].update(entry_close_location_filter='candidate_signed_mean_completed_daily_CLV',entry_close_location_window_days=W,entry_close_location_minimum=minimum,entry_close_location_scope='new_or_reversed_position_only');p=sp['parameters']
   for direction,profile,cls,bars in fixtures:
    sn=i*DAY;funds=[{'source_index':j,'settlement_ts':sn-(33-8*j)*HOUR,'available_ts':sn-(32-8*j)*HOUR,'realized_rate':D(0),'entry_interval_hours':D(8)} for j in range(5)];m={'asset':'ETH','closes':cls,'frame':bars,'signal_funds':funds}
    for actual in [-1,0,1]:
     rr=F(cls[i-1])/F(cls[i-6])-1;h=F('.02');e=F('.0075');base=-1 if rr>h else 1 if rr<-h else actual if actual==1 and rr<e or actual==-1 and rr>-e else 0;beta=F(15,17);total=past=mass=F(0)
     for j in range(i-16,i):total=F(cls[j])+beta*total;mass=1+beta*mass
     for j in range(i-19,i-3):past=F(cls[j])+beta*past
     slow=total/past-1;gate=1 if slow>F('.0075') else -1 if slow<-F('.0075') else 0;raw=base if base==actual or base==gate else 0;xs=[math.log(float(cls[j])/float(cls[j-1])) for j in range(i-6,i)];mu=math.fsum(xs)/6;sigma=math.sqrt(math.fsum((x-mu)**2 for x in xs)/5);before=0 if raw and raw!=actual and sigma>.05625 else raw;score=F(raw)*F(profile);want=0 if before and before!=actual and score<F(str(minimum)) else before;wanted,z=engine.decide(sp,m,i,actual)
     assert wanted==want and z['raw_desired_before_entry_filter']==raw and z['raw_desired_before_CLV_filter']==before and z['CLV_candidate_direction']==raw and F(z['observed_candidate_CLV_exact'])==score and abs(z['observed_sample_logvol']-sigma)<1e-12,'Independent ETH Horner/samplevol/known full-day CLV and strict lower threshold scope'
     future=copy.deepcopy(m)
     for j in range(i,len(cls)):future['closes'][j]=D('.0001') if j%2 else D('9999999')
     future['frame']=bars.with_row_index('row').with_columns(pl.when(pl.col('row')>=i*1440).then(pl.lit(D('99999999'),dtype=pl.Decimal(38,18))).otherwise(pl.col('high')).alias('high'),pl.when(pl.col('row')>=i*1440).then(pl.lit(D('.00001'),dtype=pl.Decimal(38,18))).otherwise(pl.col('low')).alias('low'))
     assert engine.decide(sp,future,i,actual)==(wanted,z),'Future day OHLC changed completed CLV entry decision'
     cases+=1;longs+=raw==1;shorts+=raw==-1;blocked+=bool(before and before!=actual and want==0);allowed+=bool(before and before!=actual and want!=0);equal_allowed+=bool(before and before!=actual and score==F(str(minimum)) and want==before)
 assert longs and shorts and blocked and allowed and equal_allowed,(longs,shorts,blocked,allowed,equal_allowed)
 normal_exits=0
 for W in [1,2,3]:
  for minimum in [0,.25,.5]:
   for actual in [-1,1]:
    cls=[D(100)+D('.3')*j for j in range(50)] if actual==1 else [D(200)-D('.5')*j for j in range(50)];bars=frame(cls,[D('.5')]*50);sp=copy.deepcopy(spbase);sp['parameters'].update(entry_close_location_filter='candidate_signed_mean_completed_daily_CLV',entry_close_location_window_days=W,entry_close_location_minimum=minimum,entry_close_location_scope='new_or_reversed_position_only');m={'asset':'ETH','closes':cls,'frame':bars,'signal_funds':funds};wanted,z=engine.decide(sp,m,i,actual);assert wanted==0 and z['raw_desired_before_CLV_filter']==0 and not z['CLV_filter_applied'],'CLV confirmation must not postpone the original normal exit';normal_exits+=1
 assert normal_exits==18
 put(R/'policy_primitive_verification.json',{'passed':True,'synthetic_only':True,'independent_ETH_policy_cases':cases+normal_exits,'entry_and_hold_cases':cases,'normal_exit_cases':normal_exits,'long_raw_cases':longs,'short_raw_cases':shorts,'blocked_new_reverse_cases':blocked,'allowed_new_reverse_cases':allowed,'exact_threshold_equal_allowed_cases':equal_allowed,'known_whole_day_extrema_long_half_short_minus_half':True,'known_three_day_mean_one_twelfth':True,'flat_range_zero':True,'original_pricevol_and_fundbudget_unchanged':True,'future_complete_OHLC_perturbation_no_effect':True,'all_cases_keep_normal_exit_and_same_direction_original_q_scope':True,'actual_market_or_account_evaluations':0});print('PASS',cases+normal_exits,'synthetic independent full daily CLV policy cases',longs,shorts,blocked,allowed,equal_allowed,'whole UTC extrema/mean/sign/zero/availability/equality/future scope')
if __name__=='__main__':run()
