"""Synthetic finite EWM slope lags, causal support, strict fast/trend gates and fixed risk/carry checks."""
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
   out,a=engine.decide(sp,m,i,actual);p=sp['parameters'];q=[F(x) for x in closes];S=int(p['trend_lookback_days']);lag=int(p['trend_slope_lag_days']);beta=F(S-1,S+1);level=mass=past=F(0)
   for j in range(i-S,i):level=q[j]+beta*level;mass=1+beta*mass
   for j in range(i-S-lag,i-lag):past=q[j]+beta*past
   slope=level/past-1;L=int(p['lookback_days']);fast=q[i-1]/q[i-1-L]-1;h=F(str(p['return_hurdle']));e=F(str(p['exit_buffer_fraction']));strength=F(str(p['trend_slope_hurdle_fraction']));gate=1 if slope>strength else -1 if slope<-strength else 0;base=-1 if fast>h else 1 if fast<-h else actual if actual==1 and fast<e or actual==-1 and fast>-e else 0;raw=base if base==actual or base==gate else 0
   V=int(p['entry_volatility_window_days']);assert V==6 and strength==F('.0075') and p['entry_volatility_ceiling']==.05625 and p['entry_funding_settlement_count'] in [2,3] and p['entry_funding_volatility_ratio']==.0075 and p['entry_funding_budget_volatility_window_days']==9 and p['return_hurdle']==.02 and S==16 and lag==3 and p['exit_buffer_fraction']==.0075 and L==5 and a['slope_lag_days']==lag and p['trend_window_days']==S and p['trend_decay_numerator']==S-1 and p['trend_decay_denominator']==S+1;xs=[math.log(float(q[j]/q[j-1])) for j in range(i-V,i)];mean=math.fsum(xs)/V;sigma=math.sqrt(math.fsum((x-mean)**2 for x in xs)/(V-1));assert abs(sigma-a['observed_sample_logvol'])<1e-12;want=0 if raw and raw!=actual and sigma>float(p['entry_volatility_ceiling']) else raw
   budget_sigma=statistics.stdev([math.log(float(closes[j])/float(closes[j-1])) for j in range(i-int(p['entry_funding_budget_volatility_window_days']),i)]);expected=min(core.D('.0002'),core.D(str(p['entry_funding_volatility_ratio']))*core.D(str(budget_sigma))*core.D(8)/core.D(24));assert core.D(a['funding_filter']['cap_fraction_per_settlement'])==expected;cap=F(str(expected));M=int(p['entry_funding_settlement_count']);selected_rates=sorted(F(x['realized_rate']) for x in funds[:M]);median=selected_rates[M//2] if M%2 else (selected_rates[M//2-1]+selected_rates[M//2])/2;assert a['funding_filter']['settlement_count']==M and F(a['funding_filter']['median_realized_rate'])==median
   if want and want!=actual and max(F(want)*median,F(0))>cap:want=0
   assert out==max(want,0) and F(a['slow_distance_exact'])==slope and F(a['slow_mean_exact'])==level/mass and F(a['return_exact'])==fast
   altered=copy.deepcopy(m);altered['closes']=closes[:i]+['1000000000000','1']*10;assert engine.decide(sp,altered,i,actual)==(out,a);n+=1
   older=copy.deepcopy(m);older['closes'][i-S-lag-1]='1000000000000';assert engine.decide(sp,older,i,actual)==(out,a)
put(R/'exit_buffer_verification.json',{'passed':True,'synthetic_cases':n,'strict_positive_negative_equal_K_boundaries':True,'new_funding_M_fixedL5E0p0075S16D3K0p0075V6cap0p05625_H2_R0p0075_VW9_checked':True,'entryrisk_window_distinct_from_carryVW9_and_impactV20':True,'independent_Horner_EWM_and_contrarian_entry_exit':True,'future_suffix_invariant':True,'sample_volatility_and_mature_funding':True,'no_real_market_or_account_calculation':True});print('PASS',n,'syntheticstrictslope/policy/futureprefixcases')

# Risk equality passes; tiny lower caps block only a new/reversed position.
for V in [5,6,7]:
 values=[math.log(float(closes[j])/float(closes[j-1])) for j in range(i-V,i)];sig=statistics.stdev(values)
 for side in [-1,1]:
  assert engine.entry_filter(side,0,sig,sig)==side and engine.entry_filter(side,0,sig,sig-1e-12)==0 and engine.entry_filter(side,side,sig,sig-1e-12)==side

for ratio in [.00625,.0075,.00875]:
 event={'events':[{'entry_interval_hours':core.D(8),'settlement_ts':sn-HOUR,'available_ts':sn,'realized_rate':core.D(0),'source_index':1}], 'median_rate':core.D(0),'count':1}
 for sigma in [0,.001,.05,1]:
  cap=engine.carry_cap(sigma,ratio,event);assert cap==min(core.D('.0002'),core.D(str(ratio))*core.D(str(sigma))*core.D(8)/core.D(24))
  event['median_rate']=cap;assert engine.funding_filter(1,0,event,sn,cap)[0]==1
  event['median_rate']=cap+core.D('1e-12');assert engine.funding_filter(1,0,event,sn,cap)[0]==0 and engine.funding_filter(1,1,event,sn,cap)[0]==1
 for invalid in [0,37]:assert engine.carry_cap(.05,ratio,{'events':[{'entry_interval_hours':core.D(invalid)}]}) is None

# Exact fast-ROC strict boundaries for every new H, independent of downstream gates.
checks=0
for sp in specs:
 h=F(str(sp['parameters']['return_hurdle']));e=F(str(sp['parameters']['exit_buffer_fraction']))
 for rr in [-h-F('1e-12'),-h,-h+F('1e-12'),h-F('1e-12'),h,h+F('1e-12')]:
  for actual in [-1,0,1]:
   close=['100']*60;close[i-1]=str(core.D(100)*(core.D(1)+core.D(rr.numerator)/core.D(rr.denominator)));m={'asset':'ETH','closes':close,'signal_funds':funds,'frame':{'available_ts':[sn]*(i*1440)}};out,a=engine.decide(sp,m,i,actual);base=-1 if rr>h else 1 if rr<-h else actual if actual==1 and rr<e or actual==-1 and rr>-e else 0;assert F(a['return_exact'])==rr and a['ungated_desired']==base and a['long_entry_return_hurdle']==a['short_entry_return_hurdle']==float(h);checks+=1
z=json.loads((R/'exit_buffer_verification.json').read_text());z.update(exact_fast_H_boundary_cases=checks,strict_positive_negative_equality_all_new_H_checked=True,closed_prefix_only=True);put(R/'exit_buffer_verification.json',z);print('PASS',checks,'exact fast ROC strict/equality cases across new lagD;no marketbacktest')

# Independent strict exit-E equality tests, separate from fast H and trend K.
exit_cases=0
for sp in specs:
 e=F(str(sp['parameters']['exit_buffer_fraction']));h=F('.02')
 for rr in [e-F('1e-12'),e,e+F('1e-12'),-e-F('1e-12'),-e,-e+F('1e-12')]:
  for actual in [-1,0,1]:
   close=['100']*60;close[i-1]=str(core.D(100)*(core.D(1)+core.D(rr.numerator)/core.D(rr.denominator)));m={'asset':'ETH','closes':close,'signal_funds':funds,'frame':{'available_ts':[sn]*(i*1440)}};out,a=engine.decide(sp,m,i,actual);base=-1 if rr>h else 1 if rr<-h else actual if actual==1 and rr<e or actual==-1 and rr>-e else 0;assert a['ungated_desired']==base and a['exit_buffer_fraction']==float(e) and a['slope_lag_days']==3;exit_cases+=1
z=json.loads((R/'exit_buffer_verification.json').read_text());z.update(strict_exit_E_cases=exit_cases,exit_E_equals_boundary_exits=True,fastH_and_exitE_and_lag_fixed=True);put(R/'exit_buffer_verification.json',z);print('PASS',exit_cases,'independent strict exitE/equality cases;no marketbacktest')
