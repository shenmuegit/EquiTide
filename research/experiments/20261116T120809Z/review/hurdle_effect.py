"""Readonly decomposition of saved tiny incremental PnL;no new configuration valuation."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
rd=lambda p:json.loads(p.read_text());r=rd(R/'report.json');h=sha(R/'report.json');btc={c['W']:c for c in r['all_current_native_grid'].values() if c['asset']=='BTC'};center=btc[0];rows=[]
for A in [.0025,.005]:
 c=btc[A]
 for k,z in c['scenes'].items():
  o=center['scenes'][k];dg=z['gross_reference_price_PnL_usdt']-o['gross_reference_price_PnL_usdt'];df=z['funding_usdt']-o['funding_usdt'];dc=z['cost_usdt']-o['cost_usdt'];dn=z['final_NAV_usdt']-o['final_NAV_usdt'];assert abs(dn-(dg+df-dc))<1e-8 and abs(100*dn/c['capital_usdt']-(z['net_return_pct']-o['net_return_pct']))<1e-10
  rows.append({'A':A,'cost':k,'BTC_incremental_PnL_usdt':dn,'BTC_gross_price_PnL_change_usdt':dg,'BTC_funding_change_usdt':df,'BTC_execution_cost_change_usdt':dc,'BTC_execution_count_change':z['executions']-o['executions'],'parent_incremental_return_pp_same_ETH':100*dn/18750,'parent_same_ETH_incremental_PnL_usdt':dn})
assert sha(R/'report.json')==h
put(R/'minimum_hurdle_effect_decomposition.json',{'passed':True,'recorded_utc':now(),'financial_report_sha256':h,'old_zero_hurdle_source_fingerprint':center['fingerprint'],'saved_rows':rows,'all_PnL_components_reconciled':True,'data_and_strategies_not_recomputed':True,'no_new_market_account_or_registry_execution':True,'small_increment_not_statistical_significance':True});print('PASS saved tinyincrement decomposition',json.dumps(rows[:3]))
