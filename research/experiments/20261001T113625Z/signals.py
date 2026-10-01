"""Only the new causal signal; accounting stays in the existing daily engine."""
from decimal import Decimal as D

def step(long, close, sma, band):
    if not long and close > sma*(1+band): return True,'enter'
    if long and close < sma*(1-band): return False,'exit'
    return long,'hold_long' if long else 'hold_cash'

def hysteresis(closes, lookback, band, start, end):
    assert lookback>=2 and 0<band<1 and lookback<=start<end<=len(closes)
    band=D(str(band)); long=False; records=[]
    for i in range(start,end):
        prior=[D(str(v)) for v in closes[i-lookback:i]]
        sma=sum(prior)/lookback
        long,action=step(long,prior[-1],sma,band)
        records.append({'decision_index':i,'prior_close':str(prior[-1]),'sma':str(sma),
                        'long':long,'action':action})
    return records
