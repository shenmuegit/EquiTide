"""Rolling OLS excludes the tested close and 24 intervening completed hourly bars."""
import math
import numpy as np

def fit_at(log_btc,log_eth,hour,window=720,gap=24):
 j=hour-1;stop=j-gap;start=stop-window;assert start>=0 and len(log_btc)==len(log_eth)>j
 x=np.asarray(log_btc[start:stop]);y=np.asarray(log_eth[start:stop]);assert len(x)==window and np.isfinite(x).all() and np.isfinite(y).all()
 out={'hour':hour,'tested_hour_index':j,'train_start':start,'train_stop_exclusive':stop,'training_bars':window,'embargo_bars':gap,'alpha':None,'beta':None,'residual_mean':None,'residual_std':None,'z':None,'eligible':False}
 dx=x-x.mean();dy=y-y.mean();den=float(dx@dx)
 if den<=1e-20:return out
 beta=float((dx@dy)/den);alpha=float(y.mean()-beta*x.mean());res=y-alpha-beta*x;mean=float(res.mean());std=float(res.std(ddof=1))
 out.update(alpha=alpha,beta=beta,residual_mean=mean,residual_std=std)
 if not math.isfinite(std) or std<=1e-12:return out
 z=float((log_eth[j]-alpha-beta*log_btc[j]-mean)/std);out.update(z=z,eligible=bool(math.isfinite(z) and .5<=beta<=2));return out

def calculate(markets):
 x=np.log(np.array([float(v) for v in markets['BTC']['hour_closes']]));y=np.log(np.array([float(v) for v in markets['ETH']['hour_closes']]))
 return [fit_at(x,y,h) for h in range(33*24,403*24)]
