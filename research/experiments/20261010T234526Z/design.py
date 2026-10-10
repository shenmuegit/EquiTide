"""BTC disjoint quote-turnover reference N x minimum ratio; fixed ETH and raw50/50."""
from pathlib import Path
from copy import deepcopy
import json
R=Path(__file__).resolve().parents[3];SOURCE=R/'research/experiments/20261010T194428Z'
BASE=json.loads((R/'research/experiments/20261010T214426Z/spec.json').read_text())
BTC_SOURCE={y:json.loads((SOURCE/f'specs/fundalloc_{y}_BTC_vol30_r1_c1000.json').read_text())for y in('2025','2026')}
ETH_SOURCE={y:json.loads((SOURCE/f'specs/fundalloc_{y}_ETH_s30_b0.0125_c1000.json').read_text())for y in('2025','2026')}
PARENT=json.loads((SOURCE/'specs/fundalloc_2026_btc0.5_ethS30_b0.0125.json').read_text())
AXES={'BTC_volume_lookback_days':[20,30,40],'BTC_minimum_volume_ratio':[.9,1,1.1]}
def definitions(fingerprint):
 out=[];fps={}
 for year in('2025','2026'):
  for n in AXES['BTC_volume_lookback_days']:
   for ratio in AXES['BTC_minimum_volume_ratio']:
    sp=deepcopy(BTC_SOURCE[year]);sp['parameters'].update(volume_lookback_days=n,minimum_volume_ratio=ratio);fps['BTC',year,n,ratio]=fingerprint(sp);out.append((sp,{'year':year,'role':'component','asset':'BTC','capital_usdt':1000,'raw_weights':[.5,.5],'BTC_volume_lookback_days':n,'BTC_minimum_volume_ratio':ratio,'EMA_span_days':None,'EMA_symmetric_band':None}))
  sp=deepcopy(ETH_SOURCE[year]);fps['ETH',year]=fingerprint(sp);out.append((sp,{'year':year,'role':'component','asset':'ETH','capital_usdt':1000,'raw_weights':[.5,.5],'BTC_volume_lookback_days':None,'BTC_minimum_volume_ratio':None,'EMA_span_days':30,'EMA_symmetric_band':.0125}))
 for year in('2025','2026'):
  for n in AXES['BTC_volume_lookback_days']:
   for ratio in AXES['BTC_minimum_volume_ratio']:
    sp=deepcopy(PARENT);sp['parameters']['start_utc']=BTC_SOURCE[year]['parameters']['start_utc'];sp['parameters']['end_utc']=BTC_SOURCE[year]['parameters']['end_utc'];sp['components']=[{'fingerprint':fps['BTC',year,n,ratio],'weight':.5},{'fingerprint':fps['ETH',year],'weight':.5}];out.append((sp,{'year':year,'role':'combination','capital_usdt':2000,'raw_weights':[.5,.5],'BTC_volume_lookback_days':n,'BTC_minimum_volume_ratio':ratio,'EMA_span_days':30,'EMA_symmetric_band':.0125}))
 assert len(out)==38
 return out
