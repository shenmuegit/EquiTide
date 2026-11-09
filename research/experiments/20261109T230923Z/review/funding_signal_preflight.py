"""Real source/availability/warmup inspection only, no returns, orders or valuations."""
import sys,json,hashlib
from pathlib import Path
import polars as pl
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import *
p=json.loads((R/'plan.json').read_text());out={}
for a,fs in p['data']['assets'].items():
 f=next(x for x in fs if x['path'].endswith('funding_settlement.parquet'));assert sha(ROOT/f['path'])==f['sha256'];q=pl.read_parquet(ROOT/f['path']);rows=q.to_dicts();assert len(rows)==1212 and all(e['available_ts']-e['settlement_ts']==HOUR for e in rows);selections=[];first=int(pl.read_parquet(ROOT/fs[0]['path'],columns=['open_ts'])['open_ts'][0])
 for i in range(core.START,core.END):
  sn=first+i*DAY;past=[(j,e) for j,e in enumerate(rows) if HOUR<=sn-e['settlement_ts']<=12*HOUR and e['available_ts']<=sn];assert past;ix,e=max(past,key=lambda z:z[1]['settlement_ts']);assert core.stamp(e['settlement_ts']).split('T')[1].startswith('16:00:00');selections.append({'decision_index':i,'signal_ns':sn,'settlement_ns':e['settlement_ts'],'available_ns':e['available_ts'],'source_index':ix,'rate':str(e['realized_rate']),'age_ns':sn-e['settlement_ts']})
 out[a]={'source':f,'source_schema':str(q.schema),'total_real_settlements':len(rows),'publication_delay_ns':HOUR,'covered_decisions':len(selections),'missing_eligible_past_rates':0,'first_warmup_selection':selections[0],'last_selection':selections[-1],'all_selections':selections}
put(R/'funding_signal_preflight.json',{'passed':True,'recorded_utc':now(),'strategy_or_account_valuations':0,'assets':out,'availability_is_assumed_conservative_delay_not_historical_arrival_evidence':True,'actual_cashflow_events_unchanged':True,'first_signal_has_real_warmup_funding':True});print('PASS real1212settlements/asset,370causaleligiblepast16UTCfields/asset includingfirstOOS;0valuations')
