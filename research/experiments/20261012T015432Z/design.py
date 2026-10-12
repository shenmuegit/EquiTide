"""Two-axis BTC initial-budget / ETH EMA-entry experiment; initial capital only, no rebalance."""
from pathlib import Path
from copy import deepcopy
from decimal import Decimal as D
from decimal import Decimal as D
import json
ROOT=Path(__file__).resolve().parents[3]
BTC_SOURCE_ROOT=ROOT/'research/experiments/20261011T115056Z'
BTC_SOURCE={y:json.loads((BTC_SOURCE_ROOT/f'specs/fastasym_{y}_BTC_s15_e0.01_x0.03_c1100.json').read_text()) for y in ('2025','2026')}
ETH_SOURCE={y:json.loads((ROOT/f'research/experiments/20261011T014626Z/specs/allocvol_{y}_ETH_s30_b0.0125_c900.json').read_text()) for y in ('2025','2026')}
COMBO_SOURCE={y:json.loads((BTC_SOURCE_ROOT/f'specs/fastasym_{y}_btcS15_E0.01_X0.03_btc0.55.json').read_text()) for y in ('2025','2026')}
BTC_WEIGHTS=[0.50,0.55,0.60]
ETH_WEIGHT_BY_BTC={0.50:0.50,0.55:0.45,0.60:0.40}
def eth_weight(weight):return ETH_WEIGHT_BY_BTC[weight]
ETH_ENTRIES=[0.01,0.0125,0.015]
ETH_EMA_SPAN=34
ETH_EMA_EXIT=0.005
AXES={'BTC_initial_weight':BTC_WEIGHTS,'ETH_EMA_entry_band_fraction':ETH_ENTRIES}
def allocations(weight):
    return [int(D(2000)*D(str(weight))),int(D(2000)*(D(1)-D(str(weight))))]
def fields(year,role,asset,weight,entry=None):
    btc,eth=allocations(weight)
    cap=2000 if role=='combination' else btc if asset=='BTC' else eth
    return {'year':year,'role':role,**({'asset':asset} if role=='component' else {}),'capital_usdt':cap,'raw_weights':[weight,eth_weight(weight)],'BTC_initial_weight':weight,'ETH_initial_weight':eth_weight(weight),'BTC_volume_lookback_days':40 if asset!='ETH' else None,'BTC_minimum_volume_ratio':1.1 if asset!='ETH' else None,'EMA_span_days':15 if asset=='BTC' else ETH_EMA_SPAN if asset=='ETH' else None,'EMA_symmetric_band':None,'BTC_EMA_span_days':15 if asset!='ETH' else None,'BTC_EMA_entry_band_fraction':0.01 if asset!='ETH' else None,'BTC_EMA_exit_band_fraction':0.03 if asset!='ETH' else None,'ETH_EMA_span_days':ETH_EMA_SPAN if asset!='BTC' else None,'ETH_EMA_symmetric_band':None,'ETH_EMA_entry_band_fraction':entry if asset!='BTC' else None,'ETH_EMA_exit_band_fraction':ETH_EMA_EXIT if asset!='BTC' else None,'sensitivity_member':True,'BTC_entry_lookback_days':15 if asset!='ETH' else None,'ETH_entry_lookback_days':15 if asset!='BTC' else None}
def definitions(fingerprint):
    out=[];btc={};eth={}
    for year in ('2025','2026'):
        for weight in BTC_WEIGHTS:
            spec=deepcopy(BTC_SOURCE[year]);spec['parameters']['initial_capital_usdt']=allocations(weight)[0];spec['name']=f'budgetbtc_{year}_{weight}'
            fp=fingerprint(spec);btc[year,weight]=fp;out.append((spec,fields(year,'component','BTC',weight)))
    for year in ('2025','2026'):
        for weight in BTC_WEIGHTS:
            for entry in ETH_ENTRIES:
                spec=deepcopy(ETH_SOURCE[year]);p=spec['parameters'];spec['family']='daily-channel-asymmetric-ema-confirmation';p.pop('EMA_symmetric_band',None);p.update(initial_capital_usdt=allocations(weight)[1],entry_lookback_days=15,exit_lookback_days=30,EMA_span_days=ETH_EMA_SPAN,EMA_entry_band_fraction=entry,EMA_exit_band_fraction=ETH_EMA_EXIT)
                if 'At decision i,enter only if prior completed' not in spec['logic']['entry']:
                    spec['logic']['entry']='At decision i,enter only if prior completed C[i-1]>max(C[i-16:i-1]) AND float(C[i-1])>EMA[EMA_span_days][i-1]*(1+entry_band).Channel reference ends i-2,excludes tested close;both gates on same decision,no delayed arming.'
                    spec['logic']['exit']='Set desired-cash if C[i-1]<min(C[i-31:i-1]) OR float(C[i-1])<EMA[EMA_span_days][i-1]*(1-exit_band).Exit priority;otherwise joint entry sets long;all other cases/equality preserve desired.Entry/exit bands independent.'
                spec['name']=f'budgeteth_{year}_btc{weight}_entry{entry}_c{allocations(weight)[1]}'
                fp=fingerprint(spec);eth[year,weight,entry]=fp;out.append((spec,fields(year,'component','ETH',weight,entry)))
    for year in ('2025','2026'):
        for weight in BTC_WEIGHTS:
            for entry in ETH_ENTRIES:
                spec=deepcopy(COMBO_SOURCE[year]);spec['family']='btc-volume-asymmetric-ema-eth-asymmetric-ema-initial-funds';spec['components']=[{'fingerprint':btc[year,weight],'weight':weight},{'fingerprint':eth[year,weight,entry],'weight':eth_weight(weight)}];spec['name']=f'budgetcombo_{year}_BTC{weight}_ETH{eth_weight(weight)}_entry{entry}'
                out.append((spec,fields(year,'combination','BTC/ETH',weight,entry)))
    assert len(out)==42 and len({fingerprint(s) for s,_ in out})==42
    return out
