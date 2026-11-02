import numpy as np
from common import *
def recent(v,m):
 ix=m['daily_indices'];daily=v[ix].tolist();tail=v[ix[330]:];s=core.stats(tail,daily[330:],40);s.update(start_utc='2026-09-14T00:01:00Z',end_exclusive_utc='2026-10-24T00:01:00Z',initial_NAV_usdt=float(tail[0]),final_NAV_usdt=float(tail[-1]),NAV_points=len(tail),NAV_sha256_f64le=core.navhash(tail),daily_equity_usdt=daily[330:],state_policy='Inherited day330predecisionstate/cash,no resetor diagnosticorders.',folds=[])
 for j in range(8):
  l,h=330+5*j,335+5*j;a,b=ix[[l,h]];s['folds'].append({'fold':j+1,'start_utc':core.stamp(int(m['ts'][a])),'end_exclusive_utc':core.stamp(int(m['ts'][b])),'duration_days':5,**core.stats(v[a:b+1],daily[l:h+1],5)})
 return s
