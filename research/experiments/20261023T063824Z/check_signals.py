"""Synthetic timing, source-rule and numeric-encoding checks,not financial backtest evidence."""
from decimal import Decimal as D
import json
import numpy as np,polars as pl
from run import ROOT,btc_signal,eth_signal,START,END,DAYS,SPAN,POINTS,core
values=['100']*367+['102','98','9999']
for cap in [.4,.5,.6]:
 a=btc_signal.volatility_guarded_asymmetric_sma(values,65,.0125,.005,20,cap,start=368,end=370)
 assert [x['long'] for x in a]==[True,False]
 assert a==btc_signal.volatility_guarded_asymmetric_sma(values[:-1]+['.0001'],65,.0125,.005,20,cap,start=368,end=370)
 assert all(x['volatility_eligible'] for x in a)
blocked=btc_signal.volatility_guarded_asymmetric_sma(values,65,.0125,.005,20,.00001,start=368,end=370);assert all(not x['long'] for x in blocked)
for span in [25,30,35]:
 a=eth_signal.filtered_channel(values,15,30,span,.0125,start=368,end=370)
 assert [x['long'] for x in a]==[True,False] and a[0]['entry_channel_prior']=='100'
 assert a==eth_signal.filtered_channel(values[:-1]+['.0001'],15,30,span,.0125,start=368,end=370)
flat=eth_signal.filtered_channel(['100']*400,15,30,30,.0125,start=368,end=370);assert all(not x['long'] for x in flat)
case=json.loads((ROOT/'research/experiments/20261023T043854Z/recovery_failure.json').read_text())['regression_case'];px=pl.Series([D(case['price'])],dtype=pl.Decimal(38,18));cash,qty=D(case['cash']),D(case['units']);assert float(cash+qty*px[0])==case['original_native_Decimal_NAV'] and float(cash+qty*D(str(px.cast(pl.Float64)[0])))!=case['original_native_Decimal_NAV']
a=np.array([1500.,1450.,1490.]);b=np.array([500.,550.,510.]);assert (a+b)[0]==2000 and (.75*a+.25*b)[0]==1250 and core.dd(a+b)==0
assert END-START==DAYS==360 and POINTS==360*1441+2==518762
print('PASS: six reused leaf parameter fixtures,closed-prior channel/volatility and future-prefix causality,native Decimal OPEN regression,funded NAV sum and continuous360dayaxis;synthetic only')
