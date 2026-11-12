"""Definition-only BTC source inventory, no saved performance selected."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');rows=[]
for fp,z in rs.items():
 sp=z.get('spec',{});q=sp.get('parameters',{})
 if sp.get('kind')!='strategy' or sp.get('universe')!=['BTC/USDT'] or not z.get('result_available'):continue
 if q.get('initial_capital_usdt')!=3750 or q.get('fixed_entry_notional_usdt')!=1000 or q.get('lookback_days')!=29:continue
 if q.get('end_utc')!='2026-10-24T00:01:00Z' or q.get('start_utc')!='2025-10-19T00:01:00Z':continue
 rows.append({'fingerprint':fp,'name':sp['name'],'parameters':q,'report':z['report'],'report_sha256':z['report_sha256']})
put(R/'definition_only_BTC_inventory.json',{'recorded_utc':now(),'rows':rows,'selection_uses_results':False,'axes_preference':{'BTC_H':[.0275,.03,.0325],'ETH_CLV_W':[1,2,3]},'new_parent_representative_preset':{'BTC_H':.0275,'ETH_CLV_W':2},'financial_calculations':0,'source_reads':[{'url':'https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data','access_utc_date':'2026-11-12','read_with':'web.open','role':'Funding-history actual fundingTime/rate/mark fields; no claim of paper replication.'}]})
print('BTC inventory',len(rows))
for z in rows:print(z['fingerprint'],z['parameters']['return_hurdle'],z['parameters']['exit_buffer_fraction'],z['parameters'].get('signal_mode'),z['name'])
