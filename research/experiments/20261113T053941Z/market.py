import copy,gzip,json
import numpy as np
import polars as pl
from common import *
from recent import recent
aligner=module(ROOT/'research/experiments/20261025T145537Z/run.py','immutable_full_axis_alignment')
def load(plan):
 ms={a:core.load_market(a,fs) for a,fs in plan['data']['assets'].items()}
 for a,m in ms.items():
  f=next(x for x in plan['data']['assets'][a] if x['path'].endswith('funding_settlement.parquet'));assert sha(ROOT/f['path'])==f['sha256'];events=pl.read_parquet(ROOT/f['path']).to_dicts();assert len(events)==1267 and all(e['available_ts']-e['settlement_ts']==HOUR for e in events);m.update(signal_funds=[{**e,'source_index':j,'entry_interval_hours':(core.D(e['settlement_ts']-events[j-1]['settlement_ts'])/core.D(HOUR)) if j and events[j-1]['available_ts']<=e['available_ts'] else None} for j,e in enumerate(events)],first_ns=int(m['frame']['open_ts'][0]),fund_lookup={x['settlement_ts']:x for x in m['funds']},terminal_reference_decimal=m['frame']['open'][422*1440+1])
 btc,eth=ms['BTC'],ms['ETH'];assert len(btc['closes'])==len(eth['closes'])==422 and [int(btc['frame']['open_ts'][i*1440]) for i in range(422)]==[int(eth['frame']['open_ts'][i*1440]) for i in range(422)]
 btc['cross_closes']=eth['closes'];btc['cross_close_available']=[int(eth['frame']['available_ts'][i*1440+1439]) for i in range(422)]
 return ms,aligner.align(ms)
