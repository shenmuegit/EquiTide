"""Read-only diagnostic source adaptation for ETH-window/BTC-bank axes."""
import ast,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
for name in ['diagnostics.py','visual_review.py']:
 f=R/'review'/name;s=f.read_text().replace("btc={c['W']:c for c in r['all_current_native_grid'].values() if c['asset']=='BTC'};center=btc[.005]","eth={c['W']:c for c in r['all_current_native_grid'].values() if c['asset']=='ETH'};center=eth[8]").replace("c=btc[V]","c=eth[V]").replace("for c in btc.values()","for c in eth.values()")
 s=s.replace('[.00375,.00625]','[7,9]').replace('{.00375,.005,.00625}','{7,8,9}').replace("c['W']==.005","c['W']==8").replace("buffer']==.005","buffer']==8").replace("slope']==.005","slope']==8")
 s=s.replace('BTC_exit_buffer','ETH_budget_window_days').replace('ETH_funding_R','BTC_main_entry_H').replace('{.00875,.01}','{.03,.0325}').replace('ETH_R','BTC_H').replace('E005','VW8').replace('exit-buffer','ETH-budget-window').replace('BTC main29day ROC exit buffers','ETH funding-budget volatility horizons').replace("old E.005/min5dayROC.0025 reference at center","old ETH VW8 reference at center").replace("old cap.0275/min5dayROC.0025 reference at center","old ETH VW8 reference at center")
 s=s.replace('Two ETH budget values and three conditional','Two readonly BTC mainH values and three conditional').replace('actual BTC recent-direction confirmation trade changes','actual ETH funding-budget entry changes')
 ast.parse(s);f.write_text(s)
f=R/'review/totalrisk_history_aliases.py';s=f.read_text().replace("'conditional_entry_vol_cap':c['W']","'ETH_budget_window_days':c['W']");f.write_text(s)
# Build saved-results-only ETH PnL decomposition; it never calls an engine.
source=(ROOT/'research/experiments/20261116T181238Z/review/exit_buffer_effect.py').read_text().replace('20261116T161211Z','20261116T181238Z')
source=source.replace("btc={c['W']:c for c in r['all_current_native_grid'].values() if c['asset']=='BTC'};center=btc[.005]","eth={c['W']:c for c in r['all_current_native_grid'].values() if c['asset']=='ETH'};center=eth[8]").replace('[.00375,.00625]','[7,9]').replace('c=btc[cap]','c=eth[cap]').replace('BTC_','ETH_').replace('exit_buffer','budget_window_days').replace('old_E005','old_VW8').replace('savedexit','savedETHbudget');ast.parse(source);(R/'review/budget_effect.py').write_text(source)
print('PASS read-only diagnostic sources use ETHVW/BTC-H axes, no financial/account evaluations')
