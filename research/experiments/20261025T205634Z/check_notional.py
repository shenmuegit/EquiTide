"""Synthetic engineering check: size-dependent impact cannot be copied by NAV scaling."""
from decimal import Decimal as D
import engine
def main():
 meta={'tick_size':'.01','lot_size':'.001','min_notional':'5'};initial={'cash':'10000','signed_units':'0','entry_price':'0','entry_reference':'0'};by={}
 for N in [1000,3000]:
  q=(D(N)/D(100)/D('.001')).to_integral_value(rounding=engine.ROUND_FLOOR)*D('.001');state,t=engine.trade(initial,q,D(110),D(10000000),D('.02'),meta,1,True);assert t['status']=='filled' and D(t['change_signed_units'])==D(N)/100 and state['signed_units']==str(q);assert D(state['cash'])==D(10000)-D(t['cost_parts']['fee']) and abs(q)*D(t['execution'])<=D(state['cash']);by[N]=t
 assert D(by[3000]['cost_parts']['impact'])>3*D(by[1000]['cost_parts']['impact'])
 assert initial=={'cash':'10000','signed_units':'0','entry_price':'0','entry_reference':'0'}
 print('PASS:two rawNfixtures,priorclosequantityratherthanfutureOPEN,fee-onlycashdebit,postfeecollateralcap,nonlinearvolumeimpact;syntheticengineeringonly,no marketbacktest')
if __name__=='__main__':main()
