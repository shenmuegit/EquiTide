"""Synthetic causal regression and two-leg economic behavior checks, no real strategy trial."""
import copy,json,math
from decimal import Decimal as D
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parent
try:
 import features,pair_model
except ModuleNotFoundError as e:
 raise AssertionError('Hourly regression and coupled-bank behavior are not implemented yet') from e
x=np.linspace(9,10,1000);y=2+1.5*x+.001*np.sin(np.arange(1000));h=800;f=features.fit_at(x,y,h);j=h-1;lo,hi=j-24-720,j-24;X=np.column_stack([np.ones(720),x[lo:hi]]);coef=np.linalg.lstsq(X,y[lo:hi],rcond=None)[0];res=y[lo:hi]-X@coef;std=float(np.std(res,ddof=1));z=(y[j]-coef[0]-coef[1]*x[j]-float(res.mean()))/std
assert f['train_start']==lo and f['train_stop_exclusive']==hi and f['tested_hour_index']==j and abs(f['beta']-coef[1])<1e-10 and abs(f['z']-z)<1e-8 and f['eligible']
xx=x.copy();yy=y.copy();xx[h:]+=100;yy[h:]-=100;assert features.fit_at(xx,yy,h)==f
xx=x.copy();yy=y.copy();xx[hi:j]+=50;yy[hi:j]-=50;assert features.fit_at(xx,yy,h)==f
zz=y.copy();zz[j]+=.1;g=features.fit_at(x,zz,h);assert g['beta']==f['beta'] and g['alpha']==f['alpha'] and abs(g['z']-f['z']-.1/f['residual_std'])<1e-8
assert not features.fit_at(np.ones(1000),y,h)['eligible']
HOUR=3600000000000;n=100*HOUR;valid={'eligible':True,'z':0,'beta':1.5};cases=0
for E in [2,2.5,3]:
 for X0 in [.5,1,1.5]:
  for side in [-1,0,1]:
   for zz in [-5,-X0,0,X0,5]:
    ff={**valid,'z':zz};got=pair_model.decide(side,n-HOUR if side else None,False,ff,E,X0,n);fresh=1 if zz<=-E else -1 if zz>=E else 0
    expected_close=bool(side and (fresh and fresh!=side or side==1 and zz>=-X0 or side==-1 and zz<=X0));expected_open=fresh if not side or fresh and fresh!=side else 0
    assert got['close']==expected_close and got['open_side']==expected_open;cases+=1
  assert pair_model.decide(1,n-48*HOUR,False,{**valid,'z':-5},E,X0,n)=={'close':True,'open_side':0,'reason':'timeout'}
  assert pair_model.decide(1,n-HOUR,False,{**valid,'eligible':False},E,X0,n)['close'] and pair_model.decide(0,None,True,valid,E,X0,n)['reason']=='recovery'
def bank():return {'cash':'10000','signed_units':'0','entry_price':'0','entry_reference':'0'}
contexts={a:{'reference':D(px),'prior_close':D(px),'ADV':D('1000000000'),'sigma':D('.01'),'meta':{'lot_size':'0.001','tick_size':'.1','min_notional':'50'}} for a,px in [('BTC','10000'),('ETH','2000')]}
books={a:bank() for a in contexts};trades={a:[] for a in contexts};bad=copy.deepcopy(contexts);bad['ETH']['meta']['min_notional']='1000000000';out=pair_model.open_pair(books,bad,1,D('1.5'),D(2000),1,n,0,trades)
assert not out['opened'] and not out['recovery'] and all(D(b['signed_units'])==0 for b in books.values()) and D(books['BTC']['cash'])<10000 and D(books['ETH']['cash'])==10000 and len(trades['BTC'])==2 and trades['ETH'][0]['status']=='rejected' and trades['ETH'][0]['reason']=='lot_or_min_notional' and trades['ETH'][0]['decision_reason']=='open_second'
cost=sum(D(t['cost_usdt']) for t in trades['BTC']);assert abs(D(10000)-D(books['BTC']['cash'])-cost)<D('1e-18')
books={a:bank() for a in contexts};trades={a:[] for a in contexts};ok=pair_model.open_pair(books,contexts,1,D('1.5'),D(2000),1,n,0,trades);assert ok['opened']
assert not pair_model.close_pair(books,bad,1,n+HOUR,1,trades,'synthetic_reject') and D(books['BTC']['signed_units'])==0 and D(books['ETH']['signed_units'])>0
assert pair_model.close_pair(books,contexts,1,n+2*HOUR,2,trades,'recovery') and all(D(b['signed_units'])==0 for b in books.values())
print(json.dumps({'passed':True,'synthetic_policy_fixtures':cases,'future_mutation_and_embargo_tested':True,'known_regression_coefficients_checked':True,'second_leg_rejection_costed_unwind_checked':True,'actual_partial_close_and_recovery_checked':True,'financial_evaluations':0}))
