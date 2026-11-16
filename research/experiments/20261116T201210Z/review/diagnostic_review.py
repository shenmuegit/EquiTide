"""Clarify saved decomposition labels after swapping the active native asset."""
import ast,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
h=sha(R/'report.json');f=R/'budget_window_days_effect_decomposition.json';x=json.loads(f.read_text());original=sha(f)
x['old_VW8_ETH_source_fingerprint']=x.pop('old_VW8_minimum25bp_source_fingerprint')
for z in x['saved_rows']:
 z['parent_incremental_return_pp_same_BTC']=z.pop('parent_incremental_return_pp_same_ETH');z['parent_same_BTC_incremental_PnL_usdt']=z.pop('parent_same_ETH_incremental_PnL_usdt')
put(f,x)
for n in ['review/budget_effect.py','collect.py']:
 p=R/n;s=p.read_text().replace('parent_incremental_return_pp_same_ETH','parent_incremental_return_pp_same_BTC').replace('parent_same_ETH_incremental_PnL_usdt','parent_same_BTC_incremental_PnL_usdt').replace('old_VW8_minimum25bp_source_fingerprint','old_VW8_ETH_source_fingerprint');ast.parse(s);p.write_text(s)
notes=json.loads((R/'stdout_label_notes.json').read_text());notes['notes'].append({'phase':'review/budget_effect.py','clarification':'Original savedcapPnL and same_ETH labels were inherited from previous BTC-active readonly decomposition. This round changes ETH while BTC is held fixed. Review renames JSON keys to same_BTC without changing any values, calculations or financial report; original native stdout retained.'});put(R/'stdout_label_notes.json',notes)
assert sha(R/'report.json')==h;put(R/'diagnostic_label_review.json',{'passed':True,'recorded_utc':now(),'original_decomposition_sha256':original,'clarified_decomposition_sha256':sha(f),'financial_report_sha256_unchanged':h,'numeric_values_unchanged':True,'market_account_registry_or_model_evaluations':0});print('PASS readonly ETHdelta/fixedBTC labels clarified, all actual numeric evidence unchanged')
