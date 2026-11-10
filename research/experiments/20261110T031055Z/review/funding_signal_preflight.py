"""Inspect actual funding warmup/availability and eligible median inputs; no returns/valuation."""
import sys,json
from pathlib import Path
import polars as pl
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import *
p=json.loads((R/'plan.json').read_text());out={}
for a,fs in p['data']['assets'].items():
 f=next(x for x in fs if x['path'].endswith('funding_settlement.parquet'));assert sha(ROOT/f['path'])==f['sha256'];q=pl.read_parquet(ROOT/f['path']);rows=q.to_dicts();assert len(rows)==1212 and all(e['available_ts']-e['settlement_ts']==HOUR for e in rows);first=int(pl.read_parquet(ROOT/fs[0]['path'],columns=['open_ts'])['open_ts'][0]);selections=[]
 for i in range(core.START,core.END):
  sn=first+i*DAY;past=sorted([(j,e) for j,e in enumerate(rows) if HOUR<=sn-e['settlement_ts']<=36*HOUR and e['available_ts']<=sn],key=lambda z:z[1]['settlement_ts'],reverse=True);assert len(past)>=4;chosen=past[:4];assert len({e['settlement_ts'] for j,e in chosen})==4
  selections.append({'decision_index':i,'signal_ns':sn,'latest4_source_indices':[j for j,e in chosen],'settlement_ns':[e['settlement_ts'] for j,e in chosen],'available_ns':[e['available_ts'] for j,e in chosen],'actual_signed_rates':[str(e['realized_rate']) for j,e in chosen],'age_ns':[sn-e['settlement_ts'] for j,e in chosen]})
 out[a]={'source':f,'source_schema':str(q.schema),'total_real_settlements':len(rows),'publication_delay_ns':HOUR,'covered_decisions':len(selections),'missing_required4_records':0,'all_source_selections':selections}
put(R/'funding_signal_preflight.json',{'passed':True,'recorded_utc':now(),'strategy_or_account_valuations':0,'assets':out,'warmup_has_at_least4_real_eligible_settlements_for_first_OOS':True,'availability_delay_is_assumption_not_historical_arrival_evidence':True,'actual_cashflow_events_unchanged':True,'no_strategy_median_returns_or_NAV_computed':True});print('PASS1212actualsettlements/asset,370decisionswith4matureeligiblepastsourcefieldsincludingwarmup;0valuations')
