"""Verify only capitalization/denominators changed;quantity,cost,funding,signals,risk unchanged."""
import ast,json
from decimal import Decimal as D
from run import ROOT,R,sha,put,engine,btc_engine
checks=[]
for name,path in [('engine.py','research/experiments/20261029T212831Z/engine.py'),('btc_engine.py','research/experiments/20261025T065405Z/engine.py')]:
 old=(ROOT/path).read_text();new=(R/name).read_text();funcs=lambda s:{x.name:ast.get_source_segment(s,x) for x in ast.parse(s).body if isinstance(x,ast.FunctionDef)};a,b=funcs(old),funcs(new);assert a.keys()==b.keys() and [k for k in a if a[k]!=b[k]]==['summary','simulate'];expected=old.replace("notional=D(str(p['fixed_entry_notional_usdt']));assert 0<notional<=CAPITAL;state={'cash':'10000'","notional=D(str(p['fixed_entry_notional_usdt']));capital=D(str(p['initial_capital_usdt']));assert 0<notional<=capital;state={'cash':str(capital)").replace('(v[-1]-10000)','(v[-1]-float(v[0]))').replace('initial_capital_usdt=10000','initial_capital_usdt=float(v[0])').replace('cost_pct_initial=cost/100','cost_pct_initial=100*cost/float(v[0])');assert new==expected;checks.append({'path':name,'source':path,'source_sha256':sha(ROOT/path),'new_sha256':sha(R/name),'only_changed_functions':['summary','simulate']})
# Actual synthetic quantity/tick/collateral cases at the new sizes;not market backtests.
meta={'lot_size':'0.001','tick_size':'0.1','min_notional':'50'};n=0
for model in [engine,btc_engine]:
 for capital,N,prior,ref in [(D('5000'),D('500'),D('80117.30'),D('80200')),(D('15000'),D('4500'),D('2367.59'),D('2370'))]:
  q=(N/prior/D(meta['lot_size'])).to_integral_value(rounding=__import__('decimal').ROUND_FLOOR)*D(meta['lot_size']);state={'cash':str(capital),'signed_units':'0','entry_price':'0','entry_reference':'0'};out,t=model.trade(state,q,ref,D('1000000000'),D('.02'),meta,3,True);assert t['status']=='filled' and D(out['cash'])==capital-D(t['cost_parts']['fee']) and D(out['signed_units'])==q and q*D(t['execution'])<=D(out['cash']);n+=1
put(R/'engine_change_verification.json',{'passed':True,'financial_evaluations':0,'engines':checks,'original_momentum_and_contrarian_targets_separate':True,'all_target_quantity_trade_funding_margin_and_data_functions_byte_identical':True,'exact_capital_substitution_only':True,'synthetic_new_size_cash_lot_tick_checks':n});print('PASS twoengine exactcapital-only changes',n)
