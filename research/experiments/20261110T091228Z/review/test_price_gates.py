"""Synthetic strict K/VC boundaries and fixed funding-budget invariance."""
import copy,json,sys
from fractions import Fraction as F
from decimal import Decimal as D
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));import engine
P=ROOT/'research/experiments/20261110T071157Z';row=next(z for z in json.loads((P/'batch.json').read_text()) if z['scope']=='native' and z['VW']==8 and z['R']==.00875);spec=json.loads((ROOT/row['spec']).read_text());sn=33*engine.DAY;m={'asset':'ETH','closes':[D(100)+D(j%7)*D('.3') for j in range(33)],'frame':{'available_ts':{33*1440-1:sn}},'signal_funds':[{'settlement_ts':sn-age*engine.HOUR,'available_ts':sn-(age-1)*engine.HOUR,'realized_rate':D('.00008'),'entry_interval_hours':D(8),'source_index':j} for j,age in enumerate([8,16,24,32])]}
probe=copy.deepcopy(spec);probe['parameters'].update(trend_slope_hurdle_fraction=.00625,entry_volatility_ceiling=.045)
try:engine.decide(probe,m,33,0)
except AssertionError:raise AssertionError('Missing parameterized K/VC price-gate domain')
if '--inclusive-volatility-bug' in sys.argv:engine.entry_filter=lambda raw,actual,sigma,cap:0 if raw and raw!=actual and sigma>=cap else raw
for K in [F('.00625'),F('.0075'),F('.00875')]:
 for s,w in [(-K-F('0.000000001'),-1),(-K,0),(F(0),0),(K,0),(K+F('0.000000001'),1)]:assert engine.slope_gate(s,K)==w
for cap in [.045,.05,.055]:
 for raw in [-1,0,1]:
  for actual in [-1,0,1]:
   for sig in [cap-1e-10,cap,cap+1e-10]:assert engine.entry_filter(raw,actual,sig,cap)==(0 if raw and raw!=actual and sig>cap else raw),'Price volatility equality must remain eligible'
for actual in [-1,0,1]:
 baseline=engine.decide(spec,m,33,actual)
 for K in [.00625,.0075,.00875]:
  for VC in [.045,.05,.055]:
   q=copy.deepcopy(spec);q['parameters'].update(trend_slope_hurdle_fraction=K,entry_volatility_ceiling=VC);got=engine.decide(q,m,33,actual);a=got[1];assert a['slope_hurdle_fraction']==K and a['entry_volatility_ceiling']==VC and a['volatility_window_days']==10 and a['funding_filter']['budget_volatility_window_days']==8 and a['funding_filter']['budget_ratio']=='.00875'.replace('.00875','0.00875')
   for f in ['budget_sigma_daily','budget_ratio','latest_past_interval_hours','cap_fraction_per_settlement','median_realized_rate','selected_settlements']:assert a['funding_filter'][f]==baseline[1]['funding_filter'][f]
   future=copy.deepcopy(m);future['closes']+=[D(1),D(99999)];future['signal_funds']+=[{**m['signal_funds'][0],'settlement_ts':sn+engine.HOUR,'available_ts':sn-engine.HOUR,'realized_rate':D('999')}];assert engine.decide(q,future,33,actual)==got
print('PASS synthetic K/VC strict boundaries,retention,future invariance and unchangedM4/VW8/R.00875budget;0 actual market/account valuations')
