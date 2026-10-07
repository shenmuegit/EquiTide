"""Synthetic money/timing fixtures; never paper performance. Also replay actual observation artifacts."""
import copy,importlib.util,json,sys
from decimal import Decimal as D
from pathlib import Path
T=Path(__file__).resolve().parent
assert (T/'run.py').exists(),'paper10 forward executor is not implemented'
s=importlib.util.spec_from_file_location('paper10_runtime',T/'run.py');m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
F={'PRICE_FILTER':{'minPrice':'.01','maxPrice':'1000000','tickSize':'.01'},'LOT_SIZE':{'minQty':'.001','maxQty':'10000','stepSize':'.001'},'NOTIONAL':{'minNotional':'1','maxNotional':'1000000'}}
Q={'bid':'99','ask':'101','bid_qty':'100','ask_qty':'100','observed_at_utc':'2026-10-07T17:00:01Z'}
def fixtures():
 # A removed spread, fee or state guard must fail these literal, hand-checked expectations.
 cash,units,t=m.paper_fill(D('101.12102'),D(0),True,Q,D('1000000000'),D(0),1,F,D(100))
 assert cash==0 and units==1 and D(t['execution'])==D('101.02')
 assert D(t['cost_parts']['fee'])==D('.10102') and D(t['cost_usdt'])==D('1.12102')
 cash2,units2,sell=m.paper_fill(cash,units,False,Q,D('1000000000'),D(0),1,F,D(100))
 assert cash2==D('98.88102') and units2==0 and D(sell['execution'])==D('98.98')
 c3,u3,t3=m.paper_fill(D('101.12102'),D(0),True,Q,D('1000000000'),D(0),3,F,D(100))
 assert c3>=0 and 0<u3<1 and D(t3['cost_usdt'])>D(t['cost_usdt'])
 c,u,reject=m.paper_fill(D('.1'),D(0),True,Q,D('1000000000'),D(0),1,F,D(100))
 assert c==D('.1') and u==0 and reject['status']=='rejected'
 try:m.paper_fill(D(100),D(0),True,{**Q,'bid':'102'},D('1000000000'),D(0),1,F,D(100))
 except ValueError:pass
 else:raise AssertionError('crossed or stale quote accepted')
 channel={'family':'daily-close-range-breakout','parameters':{'entry_lookback_days':15,'exit_lookback_days':30}}
 assert m.signal_step(channel,['1']*80+['999'],False)['long'] is False
 assert m.signal_step(channel,['1']*80+['0'],True)['long'] is True
 assert m.signal_step(channel,['1']*79+['2','0'],False)['long'] is True
 assert m.signal_step(channel,['1']*79+['.5','999'],True)['long'] is False
 assert m.signal_step(channel,['1']*79+['.5','999'],True)['action']=='exit'
 assert m.signal_step(channel,['1']*79+['2','0'],True)['action']=='hold'
 sma={'family':'daily-sma-asymmetric-hysteresis','parameters':{'lookback_days':65,'entry_band_fraction':.015,'exit_band_fraction':.005}}
 ema={'family':'daily-ema-hysteresis','parameters':{'span_days':65,'symmetric_band_fraction':.015}}
 filtered={'family':'daily-channel-ema-confirmation','parameters':{'entry_lookback_days':15,'exit_lookback_days':30,'EMA_span_days':25,'EMA_symmetric_band':.03}}
 for sp in (sma,ema,filtered):
  assert m.signal_step(sp,['1']*80+['0'],True)['long'] is True
  assert m.signal_step(sp,['1']*79+['2','0'],False)['long'] is True
  assert m.signal_step(sp,['1']*79+['.5','999'],True)['long'] is False
 plan={'_sha256':'synthetic-fixture-only','components':{'btc':{**channel,'asset':'BTC'},'eth':{**channel,'asset':'ETH'}},'portfolios':[{'id':'P01','capital_usdt':2000,'components':[{'source_fingerprint':'btc','asset':'BTC','weight':.75},{'source_fingerprint':'eth','asset':'ETH','weight':.25}],'label':'synthetic channel'}],'cost_multipliers':[1,2,3],'duration_days':180,'maximum_observation_gap_seconds':10800}
 daily=[{'open_ms':i*86400000,'available_ms':(i+1)*86400000,'close':'1' if i<79 else '2','quote_volume':'1000000000'} for i in range(80)]+[{'open_ms':80*86400000,'available_ms':81*86400000,'close':'999','quote_volume':'0'}]
 market={'quote_capture_start_utc':'2026-10-07T17:00:01Z','evaluated_at_utc':'2026-10-07T17:00:02Z','quotes':{'BTC':Q,'ETH':Q},'daily':{'BTC':daily,'ETH':daily},'filters':{'BTC':F,'ETH':F},'average_prices':{'BTC':'100','ETH':'100'},'mode':'synthetic_fixture_only'}
 state,report=m.advance(plan,None,market,'fixture1')
 assert len(report['trades'])==6 and state['observations']==1
 again,r2=m.advance(plan,state,market,'fixture1');assert again==state and r2['already_applied'] and not r2['trades']
 later={**market,'evaluated_at_utc':'2026-10-07T19:00:02Z','quote_capture_start_utc':'2026-10-07T19:00:01Z','quotes':{a:{**Q,'observed_at_utc':'2026-10-07T19:00:01Z','bid':'100','ask':'102'} for a in ('BTC','ETH')}}
 kept,r3=m.advance(plan,state,later,'fixture2');assert not r3['trades'] and kept['observations']==2
 for k in ('1','2','3'):
  for a in ('BTC','ETH'):
   old=state['portfolios']['P01']['scenarios'][k]['sleeves'][a];new=kept['portfolios']['P01']['scenarios'][k]['sleeves'][a]
   assert (old['cash_usdt'],old['units'],old['cost_usdt'])==(new['cash_usdt'],new['units'],new['cost_usdt'])
   assert D(new['units'])>0
 assert hasattr(m,'qualify'),'180day paper qualification is not implemented'
 good={'NAV_usdt':'2200','net_return_pct':10.,'observed_sample_max_drawdown_pct':10.,'round_trips':2,'cost_usdt':'5','sleeves':{'BTC':{'cash_usdt':'1650','units':'0'},'ETH':{'cash_usdt':'550','units':'0'}},'fold_milestones':[{'NAV_usdt':str(x),'boundary_late_seconds':60} for x in (2020,2040,2060,2100,2150,2200)]}
 scenes={k:copy.deepcopy(good) for k in ('1','2','3')}
 assert not all(m.qualify(scenes,2000,179*86400,1.)[0].values()),'early qualification'
 assert all(m.qualify(scenes,2000,180*86400,1.)[0].values())
 assert not all(m.qualify(scenes,2000,180*86400,.94)[0].values()),'missing observations hidden'
 bad=copy.deepcopy(scenes);bad['1']['fold_milestones']=[{'NAV_usdt':str(x),'boundary_late_seconds':60} for x in (1990,1980,1970,1960,2100,2200)]
 assert not m.qualify(bad,2000,180*86400,1.)[0]['four_positive_folds1']
 print(json.dumps({'synthetic_fixture_checks':'PASS','spread_and_fee_not_double_counted':True,'lot_and_balance_guard':True,'all_four_signal_families_causal':True,'same_observation_idempotent':True,'same_closed_day_does_not_retrade':True,'not_performance_evidence':True}))
if __name__=='__main__':
 if len(sys.argv)>1: m.audit_observation(Path(sys.argv[1]))
 else: fixtures()
