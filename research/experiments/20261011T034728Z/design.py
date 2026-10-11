"""Joint BTC/ETH close-channel exit windows;raw55/45,entry and filters fixed."""
from pathlib import Path
from copy import deepcopy
import json
R=Path(__file__).resolve().parents[3];SOURCE=R/'research/experiments/20261011T014626Z'
BASE=json.loads((SOURCE/'spec.json').read_text())
BTC_SOURCE={y:json.loads((SOURCE/f'specs/allocvol_{y}_BTC_n40_r1.1_c1100.json').read_text())for y in('2025','2026')}
ETH_SOURCE={y:json.loads((SOURCE/f'specs/allocvol_{y}_ETH_s30_b0.0125_c900.json').read_text())for y in('2025','2026')}
PARENT=json.loads((SOURCE/'specs/allocvol_2026_btcN40r1.1_ethS30_b0.0125_btc0.55.json').read_text())
AXES={'BTC_exit_lookback_days':[20,30,40],'ETH_exit_lookback_days':[20,30,40]}
def definitions(fingerprint):
 out=[];fps={}
 for year in('2025','2026'):
  for asset,template,capital in [('BTC',BTC_SOURCE[year],1100),('ETH',ETH_SOURCE[year],900)]:
   for x in AXES[asset+'_exit_lookback_days']:
    sp=deepcopy(template);sp['parameters']['exit_lookback_days']=x
    if asset=='BTC':sp['logic']['exit']=sp['logic']['exit'].replace('min(C[i-31:i-1])',f'min(C[i-{x+1}:i-1])')
    fps[asset,year,x]=fingerprint(sp);out.append((sp,{'year':year,'role':'component','asset':asset,'capital_usdt':capital,'raw_weights':[.55,.45],'BTC_initial_weight':.55,'BTC_volume_lookback_days':40 if asset=='BTC'else None,'BTC_minimum_volume_ratio':1.1 if asset=='BTC'else None,'EMA_span_days':30 if asset=='ETH'else None,'EMA_symmetric_band':.0125 if asset=='ETH'else None,'BTC_exit_lookback_days':x if asset=='BTC'else None,'ETH_exit_lookback_days':x if asset=='ETH'else None}))
 for year in('2025','2026'):
  for bx in AXES['BTC_exit_lookback_days']:
   for ex in AXES['ETH_exit_lookback_days']:
    sp=deepcopy(PARENT);sp['parameters']['start_utc']=BTC_SOURCE[year]['parameters']['start_utc'];sp['parameters']['end_utc']=BTC_SOURCE[year]['parameters']['end_utc'];sp['components']=[{'fingerprint':fps['BTC',year,bx],'weight':.55},{'fingerprint':fps['ETH',year,ex],'weight':.45}];out.append((sp,{'year':year,'role':'combination','capital_usdt':2000,'raw_weights':[.55,.45],'BTC_initial_weight':.55,'BTC_volume_lookback_days':40,'BTC_minimum_volume_ratio':1.1,'EMA_span_days':30,'EMA_symmetric_band':.0125,'BTC_exit_lookback_days':bx,'ETH_exit_lookback_days':ex}))
 assert len(out)==30
 return out
