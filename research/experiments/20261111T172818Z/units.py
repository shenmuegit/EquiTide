"""Synthetic actual-simulator sizing/cost causality tests; no historical market/account evaluation."""
import ast,copy,json,sys
from decimal import Decimal as D,ROUND_FLOOR,ROUND_CEILING
import numpy as np
from common import *
import engine
from portfolio import sum_aligned_full_banks
if '--doubleweight' in sys.argv:assert (.2*np.array([3750.,4000.])+.8*np.array([15000.,15100.]))[0]==18750,'Double weighted fullbanks'
if '--fixed-N' in sys.argv:
 src=(R/'engine.py').read_text();needle="notional=D(str(p['fixed_entry_notional_usdt']))";assert src.count(needle)==1;exec(compile(src.replace(needle,"notional=D('1000') if m['asset']=='BTC' else D('4500')"),str(R/'engine.py'),'exec'),engine.__dict__)
if '--future-open' in sys.argv:
 src=(R/'engine.py').read_text();needle="quantity=(notional/m['closes'][ref-1]/lot)";assert src.count(needle)==1;exec(compile(src.replace(needle,"quantity=(notional/m['frame']['open'][ref*1440+1]/lot)"),str(R/'engine.py'),'exec'),engine.__dict__)
if '--linear-impact' in sys.argv:
 src=CORE_PATH.read_text();fn=next(n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name=='trade');body=ast.get_source_segment(src,fn);assert 'participation.sqrt()' in body;engine.__dict__['ROUND_CEILING']=ROUND_CEILING;exec(compile(body.replace('participation.sqrt()','participation'),str(CORE_PATH),'exec'),engine.__dict__)
# One synthetic decision,one actual funding event,one terminal exit. Policy/summary stubs isolate N execution.
engine.DAYS=1;engine.END=34;engine.decide=lambda sp,m,i,actual:(1,{'synthetic_policy_stub':True});engine.summary=lambda *args:{'synthetic_no_historical_statistics':True};cases=0;sn=33*DAY;close=D('100.123');ref=D('100.37');exitref=D('102.13');adv=D('10000000');sigma=D('.02');lot=D('.001');tick=D('.01')
for asset,C,Ns in [('BTC',3750,[750,1000,1250]),('ETH',15000,[4000,4500,5000])]:
 for N in Ns:
  for k in [1,2,3]:
   for rate in [D('-.0001'),D('.0001')]:
    spec={'parameters':{'fixed_entry_notional_usdt':N,'initial_capital_usdt':C}};m={'asset':asset,'ts':np.array([sn+MIN,sn+MIN+1,sn+HOUR,sn+DAY+MIN],dtype=np.int64),'controls':np.arange(4),'codes':np.array([6,7,4,9]),'refs':np.array([33,33,0,34]),'axis_prices':np.array([float(ref),float(ref),100.42,float(exitref)]),'frame':{'available_ts':{33*1440-1:sn},'open':{33*1440+1:ref,34*1440+1:exitref}},'closes':[close]*34,'meta':{'lot_size':str(lot),'tick_size':str(tick),'min_notional':'5'},'cost_inputs':{33:(adv,sigma),34:(adv,sigma)},'funds':[{'source_index':0,'settlement_ts':sn+HOUR,'available_ts':sn+2*HOUR,'mark_price_at_settlement':D('100.42'),'realized_rate':rate,'actual_interval_hours':D('8.000000555555555555555555556')}]}
    v,z=engine.simulate(spec,m,k);q=(D(N)/close/lot).to_integral_value(rounding=ROUND_FLOOR)*lot;op,cl=z['trades'];assert op['status']==cl['status']=='filled' and D(op['change_signed_units'])==q and D(cl['change_signed_units'])==-q and z['decisions'][0]['fixed_entry_notional_usdt']==N
    for t,r in [(op,ref),(cl,exitref)]:
     sign=1 if D(t['change_signed_units'])>0 else -1;part=q*r/adv;impact=D('.5')*sigma*part.sqrt()*k;theory=r*(1+(D('.0001')*k+D('.0002')*k+impact)*sign);px=(theory/tick).to_integral_value(rounding=ROUND_CEILING if sign>0 else ROUND_FLOOR)*tick;expected={'fee':q*px*D('.0005')*k,'half_spread':q*r*D('.0001')*k,'slippage':q*r*D('.0002')*k,'impact':q*r*impact,'tick_rounding':q*abs(px-theory)};assert D(t['execution'])==px and D(t['impact_rate'])==impact and all(D(t['cost_parts'][a])==b for a,b in expected.items())
    f=z['funding_events'][0];base=-q*D('100.42')*rate;amount=base*k if base<0 else base;assert D(f['amount_usdt'])==amount and D(f['base_amount_usdt'])==base and D(f['signed_units'])==q and D(z['terminal_state']['signed_units'])==0;cash=D(C)-D(op['cost_parts']['fee'])+amount+q*(D(cl['execution'])-D(op['execution']))-D(cl['cost_parts']['fee']);assert D(z['terminal_state']['cash'])==cash and float(v[-1])==float(cash);cases+=1
btc=np.array([3750.,3900.,3800.]);eth=np.array([15000.,14900.,15500.]);axis=np.array([0,1,2]);assert np.array_equal(sum_aligned_full_banks([btc,eth],[axis,axis]),btc+eth)
try:sum_aligned_full_banks([btc,eth],[axis,axis+1])
except AssertionError:pass
else:raise AssertionError('Misalignedaxesaccepted')
if len(sys.argv)==1:put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'cases':cases,'actual_simulate_sizing_code_executed_with_synthetic_market_only':True,'policy_and_summary_stubbed_to_isolate_sizing':True,'N_grid_actual_LOT_quantity':True,'future_OPEN_not_used_for_quantity':True,'Decimal_full_cost_stack_independent':True,'funding_outflow_stressed_income_unboosted':True,'raw_wholebank_sum_and_axis_guards':True,'real_market_or_original_account_valuations':0})
print('PASS',cases,'syntheticnativeN/LOT/fee/spread/slip/volumeimpact/tick/fund/cash cases;rawbankaxis,sumguards;0realmarket/accountvaluations')
