"""Fixed50/50:BTC quote-volume reference window x ETH EMA span;definitions only."""
from pathlib import Path
from copy import deepcopy
import json
R=Path(__file__).resolve().parents[3];SOURCE=R/'research/experiments/20261010T194428Z'
BASE=json.loads((SOURCE/'spec.json').read_text())
BTC_SOURCE={y:json.loads((SOURCE/f'specs/fundalloc_{y}_BTC_vol30_r1_c1000.json').read_text())for y in('2025','2026')}
ETH_SOURCE={y:json.loads((SOURCE/f'specs/fundalloc_{y}_ETH_s30_b0.0125_c1000.json').read_text())for y in('2025','2026')}
PARENT=json.loads((SOURCE/'specs/fundalloc_2026_btc0.5_ethS30_b0.0125.json').read_text())
AXES={'BTC_volume_lookback_days':[20,30,40],'EMA_span_days':[30,33,35]}
def definitions(fingerprint):
 out=[];fps={}
 for year in('2025','2026'):
  for n in AXES['BTC_volume_lookback_days']:
   sp=deepcopy(BTC_SOURCE[year]);sp['parameters']['volume_lookback_days']=n;fps['BTC',year,n]=fingerprint(sp);out.append((sp,{'year':year,'role':'component','asset':'BTC','capital_usdt':1000,'raw_weights':[.5,.5],'BTC_volume_lookback_days':n,'EMA_span_days':None,'EMA_symmetric_band':None}))
  for span in AXES['EMA_span_days']:
   sp=deepcopy(ETH_SOURCE[year]);sp['parameters']['EMA_span_days']=span;fps['ETH',year,span]=fingerprint(sp);out.append((sp,{'year':year,'role':'component','asset':'ETH','capital_usdt':1000,'raw_weights':[.5,.5],'BTC_volume_lookback_days':None,'EMA_span_days':span,'EMA_symmetric_band':.0125}))
 for year in('2025','2026'):
  for n in AXES['BTC_volume_lookback_days']:
   for span in AXES['EMA_span_days']:
    sp=deepcopy(PARENT);sp['parameters']['start_utc']=BTC_SOURCE[year]['parameters']['start_utc'];sp['parameters']['end_utc']=BTC_SOURCE[year]['parameters']['end_utc'];sp['components']=[{'fingerprint':fps['BTC',year,n],'weight':.5},{'fingerprint':fps['ETH',year,span],'weight':.5}];out.append((sp,{'year':year,'role':'combination','capital_usdt':2000,'raw_weights':[.5,.5],'BTC_volume_lookback_days':n,'EMA_span_days':span,'EMA_symmetric_band':.0125}))
 assert len(out)==30
 return out
