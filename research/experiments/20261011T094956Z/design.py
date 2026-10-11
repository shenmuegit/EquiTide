"""BTC asymmetric EMA entry/exit bands at span20;ETH and original funds fixed."""
from pathlib import Path
from copy import deepcopy
import json
R=Path(__file__).resolve().parents[3];SOURCE=R/'research/experiments/20261011T014626Z';BASE=json.loads((SOURCE/'spec.json').read_text())
BTC_SOURCE={y:json.loads((SOURCE/f'specs/allocvol_{y}_BTC_n40_r1.1_c1100.json').read_text())for y in('2025','2026')}
ETH_SOURCE={y:json.loads((SOURCE/f'specs/allocvol_{y}_ETH_s30_b0.0125_c900.json').read_text())for y in('2025','2026')}
OLD_PARENT={y:json.loads((SOURCE/f'specs/allocvol_{y}_btcN40r1.1_ethS30_b0.0125_btc0.55.json').read_text())for y in('2025','2026')}
AXES={'BTC_EMA_entry_band_fraction':[.005,.01,.015],'BTC_EMA_exit_band_fraction':[.02,.03,.04]}
def fields(year,role,asset=None,entry=None,exit=None,member=False):
 return {'year':year,'role':role,**({'asset':asset}if role=='component'else{}),'capital_usdt':2000 if role=='combination'else 1100 if asset=='BTC'else 900,'raw_weights':[.55,.45],'BTC_initial_weight':.55,'BTC_volume_lookback_days':40 if asset!='ETH'else None,'BTC_minimum_volume_ratio':1.1 if asset!='ETH'else None,'EMA_span_days':30 if asset!='BTC'else 20 if entry is not None else None,'EMA_symmetric_band':.0125 if asset!='BTC'else None,'BTC_EMA_span_days':20 if entry is not None else None,'BTC_EMA_entry_band_fraction':entry,'BTC_EMA_exit_band_fraction':exit,'sensitivity_member':member,'BTC_entry_lookback_days':15 if asset!='ETH'else None,'ETH_entry_lookback_days':15 if asset!='BTC'else None}
def definitions(fingerprint):
 out=[];fps={};eth={}
 for year in('2025','2026'):
  for asset,sp in [('BTC',BTC_SOURCE[year]),('ETH',ETH_SOURCE[year])]:
   out.append((deepcopy(sp),fields(year,'component',asset,member=asset=='ETH')))
   if asset=='ETH':eth[year]=fingerprint(sp)
 for year in('2025','2026'):
  for entry in AXES['BTC_EMA_entry_band_fraction']:
   for exit in AXES['BTC_EMA_exit_band_fraction']:
    sp=deepcopy(BTC_SOURCE[year]);sp['family']='daily-channel-volume-asymmetric-ema-confirmation';sp['parameters'].update(EMA_span_days=20,EMA_entry_band_fraction=entry,EMA_exit_band_fraction=exit)
    sp['logic']['EMA']='alpha=2/(20+1);E[0]=float(first completed daily close),E[j]=(1-alpha)*E[j-1]+alpha*float(C[j]);Python float,adjust=False from datasetday0;never reset across folds.'
    sp['logic']['entry']='At daily decision i,use only completed C[i-1]. Set desired-long only if C[i-1]>max(C[i-16:i-1]) AND Q[i-1]>=1.1*mean(Q[i-41:i-1]) with positive reference mean AND float(C[i-1])>EMA20[i-1]*(1+entry_band). Price/quote reference ranges end i-2,exclude tested close/volume. All three conditions must hold on the same decision;no delayed arming. Quote volume is USDT turnover.'
    sp['logic']['exit']='Set desired-cash if C[i-1]<min(C[i-31:i-1]) OR float(C[i-1])<EMA20[i-1]*(1-exit_band),regardless of volume. Exit takes precedence;otherwise joint entry sets long;all other cases/price or EMA equality preserve desired. Low volume alone never liquidates;volume threshold equality qualifies. Entry and exit bands are independent.'
    fps[year,entry,exit]=fingerprint(sp);out.append((sp,fields(year,'component','BTC',entry,exit,True)))
 for year in('2025','2026'):out.append((deepcopy(OLD_PARENT[year]),fields(year,'combination')))
 for year in('2025','2026'):
  for entry in AXES['BTC_EMA_entry_band_fraction']:
   for exit in AXES['BTC_EMA_exit_band_fraction']:
    sp=deepcopy(OLD_PARENT[year]);sp['family']='btc-volume-asymmetric-ema-eth-ema-initial-funds';sp['components']=[{'fingerprint':fps[year,entry,exit],'weight':.55},{'fingerprint':eth[year],'weight':.45}];out.append((sp,fields(year,'combination',entry=entry,exit=exit,member=True)))
 assert len(out)==42
 return out
