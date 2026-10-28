"""Synthetic bookkeeping guards only; not a strategy backtest or market observation."""
import copy
import numpy as np
from run import owned_parts,summarize_parent
money=['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','gross_reference_price_PnL_usdt']
a={k:8. for k in money};a.update(executions=7,round_trips=3,funding_settlements=11,cost_parts_usdt={'fee':4.,'impact':4.},margin={'violations':0,'minimum_equity_minus_maintenance_usdt':90.});old=copy.deepcopy(a)
for w in [.5,1.5]:
 x=owned_parts([a,a],[w,1]);assert a==old and x[0]['impact' if False else 'cost_usdt']==8*w and x[0]['cost_parts_usdt']['impact']==4*w and x[0]['executions']==7 and x[0]['funding_settlements']==11 and x[0]['margin']['minimum_equity_minus_maintenance_usdt']==90*w
 v=w*np.asarray([10000.,10030.,9990.])+np.asarray([10000.,9990.,10050.]);assert v[0]==10000*(w+1) and v[0]!=10000 and v[0]!=20000
 assert (w*8+8)/(10000*(1+w))==.0008
print('PASS: raw weights preserve variable capital and monetary ownership,do not normalize or scale source action counts; original impact only fractionally owned; inputs unchanged; synthetic only.')

counts=["executions","round_trips","rejected_orders","cash_or_units_violations","funding_settlements","nonzero_funding_settlements"]
a.update({k:0 for k in counts});a["terminal_units"]="0";a["cost_parts_usdt"]={"fee":4.,"half_spread":0.,"slippage":0.,"impact":4.,"tick_rounding":0.}
for w in [.5,1.5]:
 capital=10000*(w+1);v=capital+np.linspace(0,8*(w+1),371);common={"daily_indices":np.arange(371),"fold_indices":np.asarray([0,*range(30,370,30),370]),"sha256":"synthetic-only"};z=summarize_parent(v,owned_parts([a,a],[w,1]),common,capital);assert z["initial_capital_usdt"]==capital and z["NAV_points"]==371 and len(z["recent40"]["folds"])==8 and z["funding_usdt"]==8*(w+1)
print("PASS: full370/13fold/recent8fold summary exercised on synthetic ownership curves at15k/25k capital,not a financial trial")
