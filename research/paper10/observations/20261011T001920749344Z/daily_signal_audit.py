"""Independent new-UTC-day audit of existing actual inputs; no HTTP or new fills."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal as D
from collections import Counter
import hashlib, json
T=Path(__file__).resolve().parent;R=T.parents[3]
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
dt=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
plan=read(R/'research/paper10/plan.json');before=read(T/'state_before.json')
after=read(T/'state_after.json');market=read(T/'market.json');report=read(T/'report.json')
portfolios={p['id']:p for p in plan['portfolios']}
assert len(report['decisions'])==60 and not report['trades'] and report['new_filled_virtual_orders']==0
assert report['mode']=='live_public_quotes' and report['real_orders']==0
keys=set();families=set();delays=[];actions=Counter()
for decision in report['decisions']:
 name,k,asset=decision['portfolio'],str(decision['cost_multiplier']),decision['asset']
 key=(name,k,asset);assert key not in keys;keys.add(key)
 sleeve=next(c for c in portfolios[name]['components']if c['asset']==asset)
 spec=plan['components'][sleeve['source_fingerprint']];p=spec['parameters'];family=spec['family'];families.add(family)
 rows=market['daily'][asset];values=[D(x['close'])for x in rows];i=len(values)-1;last=values[i-1]
 assert all(row['available_ms']<=market['server_time_before_ms']for row in rows[:i])
 assert rows[i]['available_ms']>market['server_time_after_ms']
 prev=before['portfolios'][name]['scenarios'][k]['sleeves'][asset]
 curr=after['portfolios'][name]['scenarios'][k]['sleeves'][asset];ctx=decision['context']
 assert curr['last_signal_open_ms']==rows[i-1]['open_ms']==prev['last_signal_open_ms']+86400000
 assert ctx['decision_index']==i
 if family=='daily-ema-hysteresis':assert isinstance(ctx['prior_close'],(int,float)) and ctx['prior_close']==float(last)
 else:assert isinstance(ctx['prior_close'],str) and D(ctx['prior_close'])==last
 if family in('daily-close-range-breakout','daily-channel-ema-confirmation'):
  upper=max(values[i-p['entry_lookback_days']-1:i-1]);lower=min(values[i-p['exit_lookback_days']-1:i-1])
  assert D(ctx['entry_channel_prior'])==upper and D(ctx['exit_channel_prior'])==lower
  channel_up,channel_down=last>upper,last<lower
 if family=='daily-sma-asymmetric-hysteresis':
  n=p['lookback_days'];mean=sum(values[i-n:i])/n
  assert D(ctx['SMA_prior'])==mean
  up=last>mean*(1+D(str(p['entry_band_fraction'])))
  down=last<mean*(1-D(str(p['exit_band_fraction'])))
 elif family in('daily-ema-hysteresis','daily-channel-ema-confirmation'):
  span=p['span_days']if family=='daily-ema-hysteresis'else p['EMA_span_days']
  band=p['symmetric_band_fraction']if family=='daily-ema-hysteresis'else p['EMA_symmetric_band']
  alpha=2/(span+1);ema=float(values[0])
  for value in values[1:i]:ema=alpha*float(value)+(1-alpha)*ema
  assert abs(ctx['EMA_prior']-ema)<1e-7
  ema_up,ema_down=float(last)>ema*(1+band),float(last)<ema*(1-band)
  if family=='daily-channel-ema-confirmation':
   assert ctx['channel_entry']==channel_up and ctx['channel_exit']==channel_down
   assert ctx['EMA_entry']==ema_up and ctx['EMA_exit']==ema_down
   up,down=channel_up and ema_up,channel_down or ema_down
  else:up,down=ema_up,ema_down
 else:
  assert family=='daily-close-range-breakout';up,down=channel_up,channel_down
 want=prev['desired_long']
 if family=='daily-channel-ema-confirmation'and down:want=False
 elif up:want=True
 elif down:want=False
 action='entry'if want and not prev['desired_long']else'exit'if prev['desired_long']and not want else'hold'
 assert ctx['forcing_entry']==bool(up) and ctx['forcing_exit']==bool(down)
 assert ctx['previous_desired_long']==prev['desired_long'] and ctx['long']==curr['desired_long']==want
 assert ctx['action']==action=='hold';actions[action]+=1
 assert {q:v for q,v in prev.items()if q!='last_signal_open_ms'}=={q:v for q,v in curr.items()if q!='last_signal_open_ms'}
 available=datetime.fromtimestamp(rows[i-1]['available_ms']/1000,timezone.utc).isoformat().replace('+00:00','Z')
 assert available==decision['signal_available_at_utc']=='2026-10-11T00:00:00Z'
 assert decision['simulated_decision_at_utc']==report['observed_at_utc']
 delay=(dt(report['observed_at_utc'])-dt(available)).total_seconds()
 assert decision['execution_delay_seconds']==delay>=0;delays.append(delay)
assert len(keys)==60 and len(families)==4 and actions=={'hold':60}
result={'passed':True,'report_sha256':sha(T/'report.json'),'state_after_sha256':sha(T/'state_after.json'),
        'new_closed_daily_open_ms':1791590400000,'signal_available_at_utc':'2026-10-11T00:00:00Z',
        'unique_portfolio_cost_asset_decisions':60,'source_rule_families_independently_checked':sorted(families),
        'channel_reference_excludes_compared_close':True,'SMA_mean_includes_latest_closed_close':True,
        'EMA_seed_first_warmup_close_recursive_adjust_false':True,'unfinished_daily_not_used':True,
        'all60_processed_days_advanced_exactly_once':True,'cash_units_desired_costs_trade_counts_unchanged':True,
        'decision_actions':dict(actions),'decision_delay_seconds_range':[min(delays),max(delays)],
        'new_virtual_fills':0,'real_orders':0,'scope':'Actual closed-day decisions audited;no fill occurred,so recorded delay is signal availability to actual decision,not execution proof.'}
(T/'daily_signal_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
