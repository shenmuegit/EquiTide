"""Decimal cash/lot accounting under the explicitly frozen IOC fill assumption."""
from decimal import Decimal as D, ROUND_FLOOR, ROUND_CEILING

def floor_step(value,step):
    return (value/step).to_integral_value(rounding=ROUND_FLOOR)*step

def adverse_tick(value,tick,buy):
    return (value/tick).to_integral_value(rounding=ROUND_CEILING if buy else ROUND_FLOOR)*tick

def fill(cash,units,buy,ref,adv,sigma,mult,filters,avg_price):
    budget=cash if buy else units*ref
    participation=budget/adv
    t={'side':'buy' if buy else 'sell','reference':str(ref),'budget':str(budget),'lagged_ADV':str(adv),'lagged_sigma':str(sigma),'participation':str(participation),'cost_multiplier':mult,'proxy_VWAP5':str(avg_price)}
    def reject(reason):
        return cash,units,{**t,'status':'rejected','reason':reason,'cash_after':str(cash),'units_after':str(units)}
    if participation>D('.001'):return reject('participation')
    fee=D('.001')*mult;spread=D('.0001')*mult;slip=D('.0002')*mult
    impact=D('.5')*sigma*participation.sqrt()*mult
    pf=filters['PRICE_FILTER'];lf=filters['LOT_SIZE'];nf=filters['NOTIONAL']
    theoretical=ref*(1+(spread+slip+impact)*(1 if buy else -1))
    price=adverse_tick(theoretical,D(pf['tickSize']),buy)
    if not D(pf['minPrice'])<=price<=D(pf['maxPrice']):return reject('price')
    q=floor_step(cash/(price*(1+fee)) if buy else units,D(lf['stepSize']))
    if not D(lf['minQty'])<=q<=D(lf['maxQty']):return reject('quantity')
    notional=q*price
    if not D(nf['minNotional'])<=notional<=D(nf['maxNotional']):return reject('notional')
    percent=filters.get('PERCENT_PRICE_BY_SIDE')
    if percent:
        prefix='bid' if buy else 'ask'
        if not avg_price*D(percent[prefix+'MultiplierDown'])<=price<=avg_price*D(percent[prefix+'MultiplierUp']):return reject('percent_price_proxy')
    fee_usdt=notional*fee
    components={'fee':fee_usdt,'half_spread':q*ref*spread,'slippage':q*ref*slip,'impact':q*ref*impact,'tick_rounding':q*abs(price-theoretical)}
    cost=sum(components.values())
    cash2=cash-notional-fee_usdt if buy else cash+notional-fee_usdt
    units2=units+q if buy else units-q
    assert cash2>=0 and units2>=0
    # Reference-mark wealth difference must equal all five execution costs.
    assert abs(cash+units*ref-(cash2+units2*ref)-cost)<D('1e-20')
    return cash2,units2,{**t,'status':'filled','execution':str(price),'theoretical_execution':str(theoretical),'quantity':str(q),'fee_rate':str(fee),'half_spread_rate':str(spread),'slippage_rate':str(slip),'impact_rate':str(impact),'cost_usdt':str(cost),'cost_parts':{k:str(v) for k,v in components.items()},'cash_after':str(cash2),'units_after':str(units2)}
