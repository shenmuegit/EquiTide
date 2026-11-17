"""Read-only parameter/axis and fixed-BTC decomposition-label review."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
r=json.loads((R/'report.json').read_text());h=sha(R/'report.json');effect=json.loads((R/'funding_count_effect_decomposition.json').read_text());assert effect['passed'] and effect['financial_report_sha256']==h
assert {z['median_settlement_count'] for z in effect['saved_rows']}=={2,3} and all('parent_incremental_return_pp_same_BTC' in z for z in effect['saved_rows'])
for c in r['configs'].values():
 if c['scope']=='native':q=json.loads((ROOT/c['spec']).read_text())['parameters'];assert q['entry_funding_budget_volatility_window_days']==8 and q['entry_funding_volatility_ratio']==.0075 and q['entry_funding_settlement_count']==c['W']
assert sha(R/'report.json')==h;put(R/'diagnostic_label_review.json',{'passed':True,'recorded_utc':now(),'financial_report_sha256_unchanged':h,'numeric_values_unchanged':True,'W':'ETH median settlement count M','K':'readonly BTC mainH','fixed_ETH_budget_VW':8,'parent_PnL_delta_holds_BTC_fixed':True,'market_account_registry_or_model_evaluations':0});print('PASS mediancount/scalar/fixedBTC-label review,financial report unchanged')
