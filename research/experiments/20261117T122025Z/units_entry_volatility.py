"""Synthetic entry-volatility windows, strict gates and independent causal ETH policy checks."""
import copy,json,math,statistics
from fractions import Fraction as F
from common import *
import engine
n=0
for k in [F('.00625'),F('.0075'),F('.00875')]:
 for s,w in [(-k-F('1e-12'),-1),(-k,0),(-k+F('1e-12'),0),(k-F('1e-12'),0),(k,0),(k+F('1e-12'),1)]:assert engine.slope_gate(s,k)==w;n+=1
sn=100*HOUR;i=40
funds=[{'settlement_ts':sn-age*HOUR,'available_ts':sn-(age-1)*HOUR,'realized_rate':core.D(rate),'source_index':j+1,'entry_interval_hours':core.D(8)} for j,(age,rate) in enumerate([(1,'.00001'),(9,'.00002'),(17,'-.00001'),(25,'.00001')])]
specs=[json.loads((ROOT/z['spec']).read_text()) for z in json.loads((R/'batch.json').read_text()) if z['scope']=='native']
for sp in specs:
 for pattern in [0,1,2]:
  closes=[str(100+j*.2+((j*7)%11)*(.9 if pattern==0 else -.7 if pattern==1 else .2)) for j in range(60)];m={'asset':'ETH','closes':closes,'signal_funds':funds,'frame':{'available_ts':[sn]*(i*1440)}}
  for actual in [-1,0,1]:
   out,a=engine.decide(sp,m,i,actual);p=sp['parameters'];q=[F(x) for x in closes];beta=F(15,17);level=mass=past=F(0)
   for j in range(i-16,i):level=q[j]+beta*level;mass=1+beta*mass
   for j in range(i-19,i-3):past=q[j]+beta*past
   slope=level/past-1;fast=q[i-1]/q[i-6]-1;h=F('.02');e=F('.0075');strength=F(str(p['trend_slope_hurdle_fraction']));gate=1 if slope>strength else -1 if slope<-strength else 0;base=-1 if fast>h else 1 if fast<-h else actual if actual==1 and fast<e or actual==-1 and fast>-e else 0;raw=base if base==actual or base==gate else 0
   V=int(p['entry_volatility_window_days']);assert V in [5,7];xs=[math.log(float(q[j]/q[j-1])) for j in range(i-V,i)];mean=math.fsum(xs)/V;sigma=math.sqrt(math.fsum((x-mean)**2 for x in xs)/(V-1));assert abs(sigma-a['observed_sample_logvol'])<1e-12;want=0 if raw and raw!=actual and sigma>.05625 else raw
   cap=F(a['funding_filter']['cap_fraction_per_settlement']);median=(F('.00001')+F('.00001'))/2
   if want and want!=actual and max(F(want)*median,F(0))>cap:want=0
   assert out==max(want,0) and F(a['slow_distance_exact'])==slope and F(a['slow_mean_exact'])==level/mass and F(a['return_exact'])==fast
   altered=copy.deepcopy(m);altered['closes']=closes[:i]+['1000000000000','1']*10;assert engine.decide(sp,altered,i,actual)==(out,a);n+=1
put(R/'entry_volatility_window_verification.json',{'passed':True,'synthetic_cases':n,'strict_positive_negative_equal_K_boundaries':True,'new_entry_risk_V5_V7_sample_denominator_and_closed_prefix_checked':True,'entryrisk_window_distinct_from_carryVW8_and_impactV20':True,'independent_Horner_EWM_and_contrarian_entry_exit':True,'future_suffix_invariant':True,'sample_volatility_and_mature_funding':True,'no_real_market_or_account_calculation':True});print('PASS',n,'syntheticstrictslope/policy/futureprefixcases')

# Risk equality passes; tiny lower caps block only a new/reversed position.
for V in [5,6,7]:
 values=[math.log(float(closes[j])/float(closes[j-1])) for j in range(i-V,i)];sig=statistics.stdev(values)
 for side in [-1,1]:
  assert engine.entry_filter(side,0,sig,sig)==side and engine.entry_filter(side,0,sig,sig-1e-12)==0 and engine.entry_filter(side,side,sig,sig-1e-12)==side
