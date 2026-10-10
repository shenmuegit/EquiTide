"""Frozen weight/span batch definitions only;no result calculation."""
from pathlib import Path
from copy import deepcopy
from decimal import Decimal as D
import json
R=Path(__file__).resolve().parents[3]
PRIOR=R/'research/experiments/20261010T134355Z'
BASE=json.loads((PRIOR/'spec.json').read_text())
BTC_SOURCE={ref['year']:json.loads((R/ref['spec']).read_text()) for ref in BASE['read_only_component_refs'] if ref['asset']=='BTC'}
ETH_SOURCE={year:json.loads((R/f'research/experiments/20261010T114325Z/specs/confirm_middle_{year}_ETH_s30_b0.0125_e15_x30_c500.json').read_text()) for year in ('2025','2026')}
PARENT=json.loads((PRIOR/'specs/vol_filter_local_2026_btcN30r1_ethS33_b0.0125_btc0.75.json').read_text())
AXES={'EMA_span_days':[30,33,35],'raw_initial_weights':[[.6,.4],[.675,.325],[.75,.25]],'ETH_symmetric_band':.0125}
def component_spec(asset,year,capital,span=None):
 sp=deepcopy((BTC_SOURCE if asset=='BTC'else ETH_SOURCE)[year]);sp['parameters']['initial_capital_usdt']=capital
 if asset=='ETH':sp['parameters'].update(EMA_span_days=span,EMA_symmetric_band=.0125)
 elif capital!=1500:sp['logic']['sizing']=sp['logic']['sizing'].replace('same1500USDT funds',f'same{capital}USDT funds')
 return sp
def definitions(fingerprint):
 out=[];fps={}
 for year in ('2025','2026'):
  for weights in AXES['raw_initial_weights']:
   assert sum(D(str(w)) for w in weights)==D(1)
   for asset,w in zip(('BTC','ETH'),weights):
    capital=int(D(2000)*D(str(w)))
    for span in ([None] if asset=='BTC'else AXES['EMA_span_days']):
     sp=component_spec(asset,year,capital,span);fp=fingerprint(sp);fps[asset,year,weights[0],span]=fp
     out.append((sp,{'year':year,'role':'component','asset':asset,'capital_usdt':capital,'BTC_initial_weight':weights[0],'raw_weights':weights,'EMA_span_days':span,'EMA_symmetric_band':.0125 if asset=='ETH'else None}))
 for year in ('2025','2026'):
  for weights in AXES['raw_initial_weights']:
   for span in AXES['EMA_span_days']:
    sp=deepcopy(PARENT);sp['parameters']['start_utc']=ETH_SOURCE[year]['parameters']['start_utc'];sp['parameters']['end_utc']=ETH_SOURCE[year]['parameters']['end_utc'];sp['components']=[{'fingerprint':fps['BTC',year,weights[0],None],'weight':weights[0]},{'fingerprint':fps['ETH',year,weights[0],span],'weight':weights[1]}]
    out.append((sp,{'year':year,'role':'combination','capital_usdt':2000,'BTC_initial_weight':weights[0],'raw_weights':weights,'EMA_span_days':span,'EMA_symmetric_band':.0125}))
 assert len(out)==42
 return out
