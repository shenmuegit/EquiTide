"""Synthetic accounting guards only,not a strategy evaluation or market observation."""
import copy
import numpy as np
from run import owned_parts,summarize_parent
money=['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','gross_reference_price_PnL_usdt'];counts=['executions','round_trips','rejected_orders','cash_or_units_violations','funding_settlements','nonzero_funding_settlements'];x={k:8. for k in money};x.update({k:0 for k in counts});x.update(executions=7,round_trips=3,funding_settlements=11,terminal_units='0',cost_parts_usdt={'fee':4.,'half_spread':0.,'slippage':0.,'impact':4.,'tick_rounding':0.},margin={'violations':0,'minimum_equity_minus_maintenance_usdt':90.});original=copy.deepcopy(x)
for a in [.25,.5,.75]:
 weights=[1,a,1-a];parts=owned_parts([x,x,x],weights);assert x==original and sum(z['cost_usdt'] for z in parts)==16 and sum(z['funding_usdt'] for z in parts)==16 and sum(z['executions'] for z in parts)==21 and parts[1]['cost_parts_usdt']['impact']==4*a
 v=weights[0]*np.asarray([10000.,10030.,9990.])+weights[1]*np.asarray([10000.,9990.,10050.])+weights[2]*np.asarray([10000.,10020.,9980.]);assert v[0]==20000 and sum(weights)==2 and v[0]!=10000
 v=20000+np.linspace(0,16,371);common={'daily_indices':np.arange(371),'fold_indices':np.asarray([0,*range(30,370,30),370]),'sha256':'synthetic-only'};z=summarize_parent(v,parts,common,20000);assert z['initial_capital_usdt']==20000 and z['NAV_points']==371 and len(z['folds'])==13 and len(z['recent40']['folds'])==8 and z['funding_settlements']==33
print('PASS:three-bank raw[1,a,1-a],capital20k,money weighted/nativecounts unweighted,no normalization/resizing;full summary/folds exercised on synthetic curves only')
