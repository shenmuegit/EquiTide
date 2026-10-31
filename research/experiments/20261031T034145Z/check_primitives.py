"""Synthetic only:fit timing, past-only momentum,degenerate fit and paid unwind."""
import copy,math
from decimal import Decimal as D
from common import *
from features import fit,score
from ranking_model import helpers
closes={'BTC':[D(100)],'ETH':[D(100)]}
for j in range(1,50):
 x=(j%7-3)*.002;closes['BTC'].append(D(str(float(closes['BTC'][-1])*math.exp(x))));closes['ETH'].append(D(str(float(closes['ETH'][-1])*math.exp(.0002+1.3*x))))
f=fit(closes,33,30);assert f['training_start_return_day']==2 and f['training_stop_exclusive_return_day']==32 and f['last_training_close_day']==31 and abs(f['beta']-1.3)<1e-8 and f['eligible_beta'];z=score(closes,33,14,f['beta'])
latest=copy.deepcopy(closes);latest['BTC'][32]*=2;assert fit(latest,33,30)==f and score(latest,33,14,f['beta'])['score']!=z['score']
future=copy.deepcopy(closes)
for a in future:future[a][33:]=[D(1)]*17
assert fit(future,33,30)==f and score(future,33,14,f['beta'])==z
degenerate=fit({'BTC':[D(100)]*50,'ETH':[D(100)]*50},33,30);assert degenerate['beta'] is None and not degenerate['eligible_beta']
books={a:{'cash':'10000','signed_units':'0','entry_price':'0','entry_reference':'0'} for a in ['BTC','ETH']};ctx={a:{'reference':D(100),'prior_close':D(100),'ADV':D(100000000),'sigma':D('.02'),'meta':{'lot_size':'.001','tick_size':'.01','min_notional':'50'}} for a in books};ctx['ETH']['meta']['min_notional']='3000';trades={a:[] for a in books};out=helpers.open_pair(books,ctx,-1,D('1.5'),D(2000),1,123,0,trades);assert not out['opened'] and not out['recovery'] and all(D(b['signed_units'])==0 for b in books.values()) and D(books['BTC']['cash'])<10000 and D(books['ETH']['cash'])==10000 and D(trades['BTC'][0]['quantity'])==30 and len(trades['BTC'])==2 and trades['ETH'][0]['status']=='rejected' and trades['BTC'][-1]['decision_reason']=='second_leg_reject_unwind'
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'first30returnfit_within33daycontext':True,'latest_momentum_close_excluded_from_beta_training':True,'future_close_perturbation_no_effect':True,'degenerate_variance_invalid':True,'BTCbeta_sizing_and_secondleg_paidunwind':True,'synthetic_returns_not_financial_evidence':True});print('PASS withheldlatestclose/future/degeneratefit andbeta-sizedpaidunwind fixtures')
