"""Past-only Float64 daily-return exposure fits;called only after all six reserves."""
import math
import numpy as np
def fit(closes,i,W):
 a,b=i-W-1,i-1;assert a>=1 and b-1==i-2
 x=np.log(np.array([float(closes['BTC'][j])/float(closes['BTC'][j-1]) for j in range(a,b)],dtype=np.float64));y=np.log(np.array([float(closes['ETH'][j])/float(closes['ETH'][j-1]) for j in range(a,b)],dtype=np.float64));mx,my=float(np.mean(x)),float(np.mean(y));den=float(np.dot(x-mx,x-mx));beta=float(np.dot(x-mx,y-my)/den) if den>1e-20 else None;alpha=my-beta*mx if beta is not None else None;eligible=bool(beta is not None and math.isfinite(beta) and math.isfinite(alpha) and .5<=beta<=2)
 return {'day_index':i,'beta_fit_window_days':W,'training_start_return_day':a,'training_stop_exclusive_return_day':b,'last_training_close_day':i-2,'latest_momentum_close_day':i-1,'training_observations':W,'x_mean':mx,'y_mean':my,'denominator':den,'alpha':alpha,'beta':beta,'eligible_beta':eligible}
def score(closes,i,L,beta):
 me=math.log(float(closes['ETH'][i-1])/float(closes['ETH'][i-1-L]));mb=math.log(float(closes['BTC'][i-1])/float(closes['BTC'][i-1-L]));z=me-beta*mb if beta is not None else None;return {'momentum_lookback_days':L,'momentum_start_close_day':i-1-L,'momentum_end_close_day':i-1,'ETH_logmomentum':me,'BTC_logmomentum':mb,'score':z,'alpha_subtracted':False}
def calculate(ms):
 closes={a:m['closes'] for a,m in ms.items()};fits={};scores={}
 for W in [20,30]:
  for i in range(33,403,7):
   f=fit(closes,i,W);fits[f'{W}:{i}']=f
   for L in [7,14,28]:scores[f'{W}:{L}:{i}']={**f,**score(closes,i,L,f['beta'])}
 assert len(fits)==106 and len(scores)==318;return {'fits':fits,'scores':scores}
