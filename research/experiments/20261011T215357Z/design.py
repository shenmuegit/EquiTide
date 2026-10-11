"""ETH period/band grid at own900;fixed archived BTC asymmetricEMA15 own1100."""
from pathlib import Path
from copy import deepcopy
import json
R=Path(__file__).resolve().parents[3];SOURCE=R/'research/experiments/20261011T115056Z'
BTC_SOURCE={y:json.loads((SOURCE/f'specs/fastasym_{y}_BTC_s15_e0.01_x0.03_c1100.json').read_text())for y in('2025','2026')}
ETH_SOURCE={y:json.loads((R/f'research/experiments/20261011T014626Z/specs/allocvol_{y}_ETH_s30_b0.0125_c900.json').read_text())for y in('2025','2026')}
OLD_PARENT={y:json.loads((SOURCE/f'specs/fastasym_{y}_btcS15_E0.01_X0.03_btc0.55.json').read_text())for y in('2025','2026')}
AXES={'ETH_EMA_span_days':[40,45,50],'ETH_EMA_entry_band_fraction':[.01,.0125,.015]}
def fields(year,role,asset=None,span=None,band=None,entry=None,exit=None):
 has_btc=asset!='ETH';has_eth=asset!='BTC'
 return {'year':year,'role':role,**({'asset':asset}if role=='component'else{}),'capital_usdt':2000 if role=='combination'else 1100 if asset=='BTC'else 900,'raw_weights':[.55,.45],'BTC_initial_weight':.55,'BTC_volume_lookback_days':40 if has_btc else None,'BTC_minimum_volume_ratio':1.1 if has_btc else None,'EMA_span_days':15 if asset=='BTC'else span,'EMA_symmetric_band':band if has_eth else None,'BTC_EMA_span_days':15 if has_btc else None,'BTC_EMA_entry_band_fraction':.01 if has_btc else None,'BTC_EMA_exit_band_fraction':.03 if has_btc else None,'ETH_EMA_span_days':span if has_eth else None,'ETH_EMA_symmetric_band':band if has_eth else None,'ETH_EMA_entry_band_fraction':entry if has_eth else None,'ETH_EMA_exit_band_fraction':exit if has_eth else None,'sensitivity_member':True,'BTC_entry_lookback_days':15 if has_btc else None,'ETH_entry_lookback_days':15 if has_eth else None}
def definitions(fingerprint):
 out=[];btc={};eth={}
 for year in('2025','2026'):
  sp=deepcopy(BTC_SOURCE[year]);btc[year]=fingerprint(sp);out.append((sp,fields(year,'component','BTC')))
 for year in('2025','2026'):
  for span in AXES['ETH_EMA_span_days']:
   for entry in AXES['ETH_EMA_entry_band_fraction']:
    exit=.005
    sp=deepcopy(ETH_SOURCE[year]);sp['family']='daily-channel-asymmetric-ema-confirmation';sp['parameters'].pop('EMA_symmetric_band');sp['parameters'].update(EMA_span_days=span,EMA_entry_band_fraction=entry,EMA_exit_band_fraction=exit)
    sp['logic']['entry']='At decision i,enter only if prior completed C[i-1]>max(C[i-16:i-1]) AND float(C[i-1])>EMA[EMA_span_days][i-1]*(1+entry_band).Channel reference ends i-2,excludes tested close;both gates on same decision,no delayed arming.'
    sp['logic']['exit']='Set desired-cash if C[i-1]<min(C[i-31:i-1]) OR float(C[i-1])<EMA[EMA_span_days][i-1]*(1-exit_band).Exit priority;otherwise joint entry sets long;all other cases/equality preserve desired.Entry/exit bands independent.'
    eth[year,span,entry]=fingerprint(sp);out.append((sp,fields(year,'component','ETH',span=span,entry=entry,exit=exit)))
 for year in('2025','2026'):
  for span in AXES['ETH_EMA_span_days']:
   for entry in AXES['ETH_EMA_entry_band_fraction']:
    exit=.005
    sp=deepcopy(OLD_PARENT[year]);sp['family']='btc-volume-asymmetric-ema-eth-asymmetric-ema-initial-funds';sp['components']=[{'fingerprint':btc[year],'weight':.55},{'fingerprint':eth[year,span,entry],'weight':.45}];out.append((sp,fields(year,'combination',span=span,entry=entry,exit=exit)))
 assert len(out)==38
 return out
