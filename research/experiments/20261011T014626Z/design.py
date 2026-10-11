"""FixedN40 volume confirmation ratio x explicit initial BTC funding,definitions only."""
from pathlib import Path
from copy import deepcopy
from decimal import Decimal as D
import json
R=Path(__file__).resolve().parents[3];SOURCE=R/'research/experiments/20261010T234526Z'
BASE=json.loads((SOURCE/'spec.json').read_text())
BTC_SOURCE={y:json.loads((SOURCE/f'specs/volratio_{y}_BTC_n40_r1.1_c1000.json').read_text())for y in('2025','2026')}
ETH_SOURCE={y:json.loads((R/f'research/experiments/20261010T194428Z/specs/fundalloc_{y}_ETH_s30_b0.0125_c1000.json').read_text())for y in('2025','2026')}
PARENT=json.loads((SOURCE/'specs/volratio_2026_btcN40_r1.1_ethS30_b0.0125_btc0.5.json').read_text())
AXES={'BTC_minimum_volume_ratio':[1,1.1,1.2],'BTC_initial_weight':[.45,.5,.55]}
def definitions(fingerprint):
 out=[];fps={}
 for year in('2025','2026'):
  for w in AXES['BTC_initial_weight']:
   weights=[w,float(D(1)-D(str(w)))];bc=int(D(2000)*D(str(weights[0])));ec=int(D(2000)*D(str(weights[1])))
   for ratio in AXES['BTC_minimum_volume_ratio']:
    sp=deepcopy(BTC_SOURCE[year]);sp['parameters'].update(initial_capital_usdt=bc,volume_lookback_days=40,minimum_volume_ratio=ratio);sp['logic']['sizing']=sp['logic']['sizing'].replace('same1000USDT funds',f'same{bc}USDT funds');fps['BTC',year,w,ratio]=fingerprint(sp);out.append((sp,{'year':year,'role':'component','asset':'BTC','capital_usdt':bc,'raw_weights':weights,'BTC_initial_weight':w,'BTC_volume_lookback_days':40,'BTC_minimum_volume_ratio':ratio,'EMA_span_days':None,'EMA_symmetric_band':None}))
   sp=deepcopy(ETH_SOURCE[year]);sp['parameters']['initial_capital_usdt']=ec;fps['ETH',year,w]=fingerprint(sp);out.append((sp,{'year':year,'role':'component','asset':'ETH','capital_usdt':ec,'raw_weights':weights,'BTC_initial_weight':w,'BTC_volume_lookback_days':None,'BTC_minimum_volume_ratio':None,'EMA_span_days':30,'EMA_symmetric_band':.0125}))
 for year in('2025','2026'):
  for w in AXES['BTC_initial_weight']:
   weights=[w,float(D(1)-D(str(w)))]
   for ratio in AXES['BTC_minimum_volume_ratio']:
    sp=deepcopy(PARENT);sp['parameters']['start_utc']=BTC_SOURCE[year]['parameters']['start_utc'];sp['parameters']['end_utc']=BTC_SOURCE[year]['parameters']['end_utc'];sp['components']=[{'fingerprint':fps['BTC',year,w,ratio],'weight':weights[0]},{'fingerprint':fps['ETH',year,w],'weight':weights[1]}];out.append((sp,{'year':year,'role':'combination','capital_usdt':2000,'raw_weights':weights,'BTC_initial_weight':w,'BTC_volume_lookback_days':40,'BTC_minimum_volume_ratio':ratio,'EMA_span_days':30,'EMA_symmetric_band':.0125}))
 assert len(out)==42
 return out
