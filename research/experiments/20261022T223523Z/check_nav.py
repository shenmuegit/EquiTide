"""Synthetic event ordering and initial-capital drawdown check, not market evidence."""
import hashlib
import numpy as np
import polars as pl
from nav_audit import augment, MINUTE

spot=pl.DataFrame({'open_ts':[i*MINUTE for i in range(4)],'open':[100.]*4,'close':[100.]*4,'high':[100.]*4})
perp=pl.DataFrame({'open_ts':[i*MINUTE for i in range(4)],'open':[101.]*4,'close':[101.]*4,'high':[101.]*4})
event={'ts':MINUTE*3//2,'available':MINUTE*3//2+60*MINUTE,'rate':2/101,'mark':101.,'hours':8.}
trades=[]
for t,enter in [(MINUTE,True),(3*MINUTE,False)]:
    for leg,px,fee in [('spot',100.,1.),('perp',101.,.5)]:
        trades.append({'ts':t,'leg':leg,'quantity':1.,'side':('buy' if enter else 'sell') if leg=='spot' else ('sell' if enter else 'buy'),'execution':px,'fee_usdt':fee,'participation':.0001})
scene={'trades':trades,'funding_events':[{**event,'quantity':1.,'base_amount_usdt':2.,'amount_usdt':2.}],
       'equity_signal_times':[0,2*MINUTE],'equity':[10000.,9998.5,9999.],'final_NAV':9999.}
data={'frames':{'spot_bars':spot,'perp_bars':perp},'events':[event],
      'marks':{0:{'high':999999.}},'rows':[{'ts':t,'fill':100.,'fill_perp':101.} for t in (0,2*MINUTE)]}
r=augment(data,scene,MINUTE,3*MINUTE,1)
expected=np.array([10000.,9998.5,10000.5,10000.5,9999.],dtype='<f8')
assert r['minute_nav_sha256_f64le']==hashlib.sha256(expected.tobytes()).hexdigest()
assert r['minute_nav_samples']==5 and r['minute_close_samples']==2
assert abs(r['max_drawdown_1m_sampled_pct']-.015)<1e-10
assert not r['independent_cash_margin_violations']
assert r['terminal_spot_cash_usdt']==4998. and r['terminal_perp_collateral_usdt']==5001.
print('PASS: exact initial/post-fill/minute NAV ordering, funding within minute, isolated balances, initial-capital DD, no post-OOS mark leakage; synthetic only')
