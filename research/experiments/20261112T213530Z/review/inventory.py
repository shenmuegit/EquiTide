"""Definition-only exact native-bank inventory; no performance selection/evaluation."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');rows=[]
for fp,z in rs.items():
 sp=z.get('spec',{});q=sp.get('parameters',{});a=sp.get('universe',[])
 if sp.get('kind')!='strategy' or not z.get('result_available') or q.get('start_utc')!='2025-10-19T00:01:00Z' or q.get('end_utc')!='2026-10-24T00:01:00Z':continue
 if a==['BTC/USDT']:
  ok=q.get('initial_capital_usdt')==3750 and q.get('fixed_entry_notional_usdt')==1000 and q.get('entry_volatility_window_days')==10 and q.get('entry_volatility_ceiling') in [.03,.04,.05]
 elif a==['ETH/USDT']:
  ok=q.get('initial_capital_usdt')==15000 and q.get('fixed_entry_notional_usdt')==4000 and q.get('entry_funding_settlement_count')==4 and q.get('entry_funding_budget_volatility_window_days')==8 and q.get('entry_funding_volatility_ratio') in [.009375,.01,.010625] and not q.get('entry_close_location_filter') and not q.get('entry_path_efficiency_filter') and q.get('entry_volatility_window_days')==6 and q.get('entry_volatility_ceiling')==.05625
 else:ok=False
 if ok:rows.append({'fingerprint':fp,'name':sp['name'],'asset':a[0].split('/')[0],'parameters':q,'report':z['report'],'report_sha256':z['report_sha256']})
put(R/'definition_only_inventory.json',{'recorded_utc':now(),'rows':rows,'selection_uses_results':False,'axes_preference':{'BTC_VOL_CAP':[.03,.04,.05],'ETH_FUND_R':[.009375,.01,.010625]},'new_parent_representative_preset':{'BVC':.04,'R':.01},'financial_calculations':0,'source_reads':[{'url':'https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data','access_utc_date':'2026-11-12','read_with':'web.open','role':'Official closed klines, fundingTime/rate/mark fields; no alpha claim.'}]})
print('definition matches',len(rows))
for z in rows:print(z['asset'],z['fingerprint'],z['name'],z['parameters'].get('entry_volatility_ceiling'),z['parameters'].get('entry_funding_volatility_ratio'))
