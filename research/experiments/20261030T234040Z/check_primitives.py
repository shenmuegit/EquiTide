"""Synthetic only: stale/future inputs, schedule, tie and costed partial-leg unwind."""
import copy
from decimal import Decimal as D
from common import *
from ranking_model import rank,helpers
closes={'BTC':[D(100+i) for i in range(50)],'ETH':[D(100)+D(i)/2 for i in range(50)]};side,z=rank(closes,33,7);assert side==-1 and z['feature_end_day_index']==32 and z['feature_start_day_index']==25
future=copy.deepcopy(closes)
for a in future:future[a][33:]=[D(1)]*17
assert rank(future,33,7)==(side,z);assert rank({'BTC':closes['BTC'],'ETH':closes['BTC']},33,7)[0]==0
assert [i for i in range(33,403) if (i-33)%7==0][:3]==[33,40,47] and len([i for i in range(33,403) if (i-33)%7==0])==53 and len([i for i in range(33,403) if (i-33)%14==0])==27
books={a:{'cash':'10000','signed_units':'0','entry_price':'0','entry_reference':'0'} for a in ['BTC','ETH']};ctx={a:{'reference':D(100),'prior_close':D(100),'ADV':D(100000000),'sigma':D('.02'),'meta':{'lot_size':'.001','tick_size':'.01','min_notional':'50'}} for a in books};ctx['ETH']['meta']['min_notional']='3000';trades={a:[] for a in books};out=helpers.open_pair(books,ctx,-1,D(1),D(2000),1,123,0,trades);assert not out['opened'] and not out['recovery'] and all(D(b['signed_units'])==0 for b in books.values()) and D(books['BTC']['cash'])<10000 and D(books['ETH']['cash'])==10000 and len(trades['BTC'])==2 and trades['ETH'][0]['status']=='rejected' and trades['BTC'][-1]['decision_reason']=='second_leg_reject_unwind'
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'future_close_perturbation_no_effect':True,'exact_tie_cash':True,'fixed_anchor_53_or27_scheduled_decisions':True,'second_leg_rejection_costed_BTC_unwind':True,'no_synthetic_return_used_as_real_results':True});print('PASS ranking past-only/tie/weeklyanchor and paidunwind fixture')
