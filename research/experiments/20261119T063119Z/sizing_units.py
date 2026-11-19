"""Synthetic sizing primitives only: LOT, nonlinear impact and exact funding stress; no market backtests."""
import copy,json
from decimal import Decimal as D,ROUND_FLOOR
from common import *
p=json.loads((R/'plan.json').read_text());assert p['axes']=={'BTC_ENTRY_N':[1000,1250,1500],'ETH_ENTRY_CAP':[.0525,.05625]};meta={'tick_size':'.1','lot_size':'.001','min_notional':'5'};ref=D('63111.57293103');adv=D('20000000');sigma=D('.02');q0=(D(1000)/ref/D('.001')).to_integral_value(rounding=ROUND_FLOOR)*D('.001');cases=[]
for N in [1000,1250,1500]:
 q=(D(N)/ref/D('.001')).to_integral_value(rounding=ROUND_FLOOR)*D('.001');assert q*ref<=N<(q+D('.001'))*ref
 if N!=1000:assert q!=q0*D(N)/D(1000)
 for sign in [-1,1]:
  for k in [1,2,3]:
   state={'cash':'3750','signed_units':'0','entry_price':'0','entry_reference':'0'};after,t=core.trade(state,D(sign)*q,ref,adv,sigma,meta,k,True);assert t['status']=='filled' and D(after['signed_units'])==sign*q and D(after['cash'])==D(3750)-D(t['cost_parts']['fee'])
   part=q*ref/adv;impact=D('.5')*sigma*part.sqrt()*k;assert D(t['participation'])==part and D(t['impact_rate'])==impact and D(t['cost_parts']['impact'])==q*ref*impact and D(t['cost_parts']['fee'])==q*D(t['execution'])*D('.0005')*k
   if N!=1000:
    baseimpact=q0*ref*D('.5')*sigma*(q0*ref/adv).sqrt()*k;assert D(t['cost_parts']['impact'])!=baseimpact*D(N)/1000
   base,amount=core.funding_amount(D(sign)*q,ref,D('.0001'),k);assert base==-sign*q*ref*D('.0001') and amount==(base*k if base<0 else base)
   end,closed=core.trade(after,-D(sign)*q,ref,adv,sigma,meta,k,False);assert closed['status']=='filled' and D(end['signed_units'])==0
   cases.append({'N':N,'direction':sign,'cost':k,'LOT_quantity':str(q),'impact_usdt':t['cost_parts']['impact'],'funding_amount':str(amount)})
assert len(cases)==18
put(R/'sizing_primitive_verification.json',{'passed':True,'synthetic_cases':cases,'no_market_or_account_backtests':True,'synthetic_order_primitives_not_paper_fills':True,'LOT_floor_and_naive_linear_quantity_rejected':True,'nonlinear_impact_vs_naive_linear_NAV_scaling_rejected':True,'fees_and_funding_outflow_stress_income_unboosted':True,'same_N_holding_reference_map':p['benchmark_by_W'],'matched_holds_preregistered_in_batch':True});print('PASS18 synthetic sizing/LOT/impact/funding/close cases;0marketbacktests;no account mutation')
