"""ETH period/band grid at own900;fixed archived BTC asymmetricEMA15 own1100."""
from pathlib import Path
from copy import deepcopy
import json
R=Path(__file__).resolve().parents[3];SOURCE=R/'research/experiments/20261011T115056Z'
BTC_SOURCE={y:json.loads((SOURCE/f'specs/fastasym_{y}_BTC_s15_e0.01_x0.03_c1100.json').read_text())for y in('2025','2026')}
ETH_SOURCE={y:json.loads((R/f'research/experiments/20261011T014626Z/specs/allocvol_{y}_ETH_s30_b0.0125_c900.json').read_text())for y in('2025','2026')}
OLD_PARENT={y:json.loads((SOURCE/f'specs/fastasym_{y}_btcS15_E0.01_X0.03_btc0.55.json').read_text())for y in('2025','2026')}
AXES={'ETH_EMA_span_days':[20,30,40],'ETH_EMA_symmetric_band':[.01,.0125,.015]}
def fields(year,role,asset=None,span=None,band=None):
 has_btc=asset!='ETH';has_eth=asset!='BTC'
 return {'year':year,'role':role,**({'asset':asset}if role=='component'else{}),'capital_usdt':2000 if role=='combination'else 1100 if asset=='BTC'else 900,'raw_weights':[.55,.45],'BTC_initial_weight':.55,'BTC_volume_lookback_days':40 if has_btc else None,'BTC_minimum_volume_ratio':1.1 if has_btc else None,'EMA_span_days':15 if asset=='BTC'else span,'EMA_symmetric_band':band if has_eth else None,'BTC_EMA_span_days':15 if has_btc else None,'BTC_EMA_entry_band_fraction':.01 if has_btc else None,'BTC_EMA_exit_band_fraction':.03 if has_btc else None,'ETH_EMA_span_days':span if has_eth else None,'ETH_EMA_symmetric_band':band if has_eth else None,'sensitivity_member':True,'BTC_entry_lookback_days':15 if has_btc else None,'ETH_entry_lookback_days':15 if has_eth else None}
def definitions(fingerprint):
 out=[];btc={};eth={}
 for year in('2025','2026'):
  sp=deepcopy(BTC_SOURCE[year]);btc[year]=fingerprint(sp);out.append((sp,fields(year,'component','BTC')))
 for year in('2025','2026'):
  for span in AXES['ETH_EMA_span_days']:
   for band in AXES['ETH_EMA_symmetric_band']:
    sp=deepcopy(ETH_SOURCE[year]);sp['parameters'].update(EMA_span_days=span,EMA_symmetric_band=band);eth[year,span,band]=fingerprint(sp);out.append((sp,fields(year,'component','ETH',span,band)))
 for year in('2025','2026'):
  for span in AXES['ETH_EMA_span_days']:
   for band in AXES['ETH_EMA_symmetric_band']:
    sp=deepcopy(OLD_PARENT[year]);sp['components']=[{'fingerprint':btc[year],'weight':.55},{'fingerprint':eth[year,span,band],'weight':.45}];out.append((sp,fields(year,'combination',span=span,band=band)))
 assert len(out)==38
 return out
