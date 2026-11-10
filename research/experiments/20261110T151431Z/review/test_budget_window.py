"""Synthetic-only independent budget horizon, default equivalence and causality checks."""
import copy,math,statistics,sys,json
from pathlib import Path
from decimal import Decimal as D
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));import engine
assert hasattr(engine,'budget_sigma'), 'Missing separate funding budget volatility window'
base=[D(100)+D(j%7)*D('.3') for j in range(33)];i=33
for vw in [8,10,12]:
 expected=statistics.stdev([math.log(float(base[j])/float(base[j-1])) for j in range(i-vw,i)])
 assert engine.budget_sigma(base,i,vw)==expected
 assert engine.budget_sigma(base+[D(1),D(999999)],i,vw)==expected
changed=copy.deepcopy(base);changed[23]=D(140)
assert engine.budget_sigma(changed,i,8)==engine.budget_sigma(base,i,8)
assert engine.budget_sigma(changed,i,12)!=engine.budget_sigma(base,i,12)
if '--wrong-budget-window' in sys.argv:
 original=engine.budget_sigma;engine.budget_sigma=lambda closes,i,vw:original(closes,i,10)
 assert engine.budget_sigma(changed,i,8)==engine.budget_sigma(base,i,8), 'Incorrect fixed10 budget leaks older shock into VW8'
old=engine.module(ROOT/'research/experiments/20261110T051156Z/engine.py','prior_budget_engine_for_synthetic_check');row=next(z for z in json.loads((ROOT/'research/experiments/20261110T051156Z/batch.json').read_text()) if z['scope']=='native' and z['M']==4 and z['R']==.0075);spec=json.loads((ROOT/row['spec']).read_text());sn=33*engine.DAY;fund=[{'settlement_ts':sn-age*engine.HOUR,'available_ts':sn-(age-1)*engine.HOUR,'realized_rate':D('.00007'),'entry_interval_hours':D(8),'source_index':j} for j,age in enumerate([8,16,24,32])];m={'asset':'ETH','closes':base,'frame':{'available_ts':{i*1440-1:sn}},'signal_funds':fund}
for actual in [-1,0,1]:
 want,audit=engine.decide(spec,m,i,actual);owant,oa=old.decide(spec,m,i,actual);assert want==owant
 assert {k:v for k,v in audit.items() if k!='funding_filter'}=={k:v for k,v in oa.items() if k!='funding_filter'}
 assert {k:v for k,v in audit['funding_filter'].items() if k!='budget_volatility_window_days'}==oa['funding_filter']
 for vw in [8,10,12]:
  sp=copy.deepcopy(spec);sp['parameters']['entry_funding_budget_volatility_window_days']=vw;got=engine.decide(sp,m,i,actual);assert got[1]['volatility_window_days']==10 and got[1]['funding_filter']['budget_volatility_window_days']==vw
  fresh=copy.deepcopy(m);fresh['closes']+=[D(1),D(99999)];fresh['signal_funds']+=[{**fund[0],'settlement_ts':sn+engine.HOUR,'available_ts':sn-engine.HOUR,'realized_rate':D('99')}];assert engine.decide(sp,fresh,i,actual)==got
print('PASS synthetic separateVW8/10/12,strict historical horizon/future invariance,defaultVW10 exact original behavior and pricegateV10 unchanged;0 market/account valuations')
