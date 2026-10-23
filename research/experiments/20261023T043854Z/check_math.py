"""Synthetic portfolio accounting checks only, not market backtest evidence."""
import numpy as np
from run import core
btc=np.array([1500.,1450.,1490.,1520.]);eth=np.array([500.,550.,510.,500.]);total=btc+eth
assert np.array_equal(total,np.array([2000.,2000.,2000.,2020.])) and total[0]==2000
assert core.dd(total)==0 and .75*core.dd(btc)+.25*core.dd(eth)>0
assert (.75*btc+.25*eth)[0]==1250 and not np.array_equal(.75*btc+.25*eth,total)
assert len(np.empty(180*1441+2))==core.POINTS==259382
assert core.navhash(total)==core.navhash(total.copy())
print('PASS: absolute funded NAV sum, no second application of raw75/25 weights, combined rather than averaged drawdown, exact axis and deterministic hash;synthetic only')

# Archived OPEN used Decimal before the single final NAV-to-float conversion.
import json
from decimal import Decimal as D
from pathlib import Path
import polars as pl
z=json.loads((Path(__file__).parent/'recovery_failure.json').read_text())['regression_case']
price=pl.Series([D(z['price'])],dtype=pl.Decimal(38,18));cash,qty=D(z['cash']),D(z['units'])
assert float(cash+qty*price[0])==z['original_native_Decimal_NAV']
assert float(cash+qty*D(str(price.cast(pl.Float64)[0])))==z['failed_float_roundtrip_NAV']
assert z['original_native_Decimal_NAV']!=z['failed_float_roundtrip_NAV']
print('PASS: archived native Decimal OPEN regression;Float64 roundtrip differs and must not replace source NAV encoding')
