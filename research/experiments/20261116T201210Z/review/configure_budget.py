"""Preregister ETH budget-volatility horizons crossed with readonly BTC H banks."""
import ast,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261116T181238Z';sys.path.insert(0,str(R));from common import *
assert not (R/'code_binding_before_evaluation.json').exists()
def edit(n,a,b):
 f=R/n;s=f.read_text();assert a in s,(n,a);f.write_text(s.replace(a,b))
edit('engine.py','assert window in [8,10,12]','assert window in [7,8,9,10,12]');edit('audit.py','assert VW in [8,10,12]','assert VW in [7,8,9,10,12]')
for n in ['run.py','audit.py','exports.py']:
 f=R/n;s=f.read_text().replace('BTC_EXIT_BUFFER','ETH_BUDGET_VW').replace('ETH_FUND_R','BTC_MAIN_ENTRY_H')
 s=s.replace("axis='ETH_BUDGET_VW' if c['asset']=='BTC' else 'BTC_MAIN_ENTRY_H';key='W' if c['asset']=='BTC' else 'K'","axis='ETH_BUDGET_VW' if c['asset']=='ETH' else 'BTC_MAIN_ENTRY_H';key='W' if c['asset']=='ETH' else 'K'")
 if n=='exports.py':
  s=s.replace("scope=='parent' or a['asset']=='BTC'","scope=='parent' or a['asset']=='ETH'").replace("else 0;dE=",'else 0;dE=')
  # Second axis belongs to BTC, after both expressions are identified independently.
  s=s.replace("dE=abs(p['axes']['BTC_MAIN_ENTRY_H'].index(a['K'])-p['axes']['BTC_MAIN_ENTRY_H'].index(b['K'])) if scope=='parent' or a['asset']=='ETH' else 0","dE=abs(p['axes']['BTC_MAIN_ENTRY_H'].index(a['K'])-p['axes']['BTC_MAIN_ENTRY_H'].index(b['K'])) if scope=='parent' or a['asset']=='BTC' else 0")
  s=s.replace('Readonly ETH funding budget R','Readonly BTC main entry H').replace('BTC ROC holding/exit buffer E (fraction)','ETH funding-budget volatility window (days)').replace("['0.00875','0.01000']","['0.03000','0.03250']").replace("['0.00375','0.00500 (old)','0.00625']","['7','8 (old)','9']").replace('BTC ROC exit buffers / reused ETH funding budget','ETH funding-budget volatility horizon / reused BTC main entry H')
 if n=='run.py':s=s.replace("'read_only_ETH_banks_reused':True,'read_only_BTC_center_reused':True,'new_native_asset':'BTC'","'read_only_ETH_center_reused':True,'read_only_BTC_banks_reused':True,'new_native_asset':'ETH'")
 f.write_text(s)
f=R/'parent_units.py';s=f.read_text().replace("g['W']==.005","g['W']==8").replace("g['asset']=='BTC' and g['W']==8","g['asset']=='ETH' and g['W']==8").replace('for VW in [8,10,12]:','for VW in [7,8,9,10,12]:');f.write_text(s)
for n in ['checks.py','finalize.py']:
 f=R/n;s=f.read_text().replace("'new_native_asset':'BTC'","'new_native_asset':'ETH'").replace("new_native_asset='BTC'","new_native_asset='ETH'");f.write_text(s)
f=R/'review/setup_confirmation.py';s=f.read_text().replace('2026-11-16T18:12:38.341Z','2026-11-16T20:12:10.193Z').replace("'9df04e'","'aab4c3'").replace("'c66ac0'","'6b9784'").replace("'branch_lock_native_session':49690","'branch_lock_native_session':45734").replace('55907e8f784dc8972c6ec987a20224c08f157636','d8744140a9c547d6f5d7f8e1600875dd7fae9774')
s=s.replace("('SMA','2026-11-16T08:30:00Z','2026-11-16T10:30:00Z')","('SMA','2026-11-16T10:30:00Z','2026-11-16T12:30:00Z')").replace("('candidate','2026-11-16T08:30:00Z','2026-11-16T10:30:00Z')","('candidate','2026-11-16T10:30:00Z','2026-11-16T12:30:00Z')").replace("'2026-11-16T10:10:00Z','2026-11-16T12:10:00Z'","'2026-11-16T12:10:00Z','2026-11-16T14:10:00Z'")
a=s.index("rules='");b=s.index('\nw={}',a);s=s[:a]+"rules='SMA/singleNov16_10:30to12:30;L4/FEWM12:10to14:10. Freshcomplete10:30to14:10actualfundinglookup isempty forbothassets;nominal8hschedule notassumed. All3perps08previouslybookedonce,no currentcashflows/daily/fills. Preservefrozenbooks/fullNAV/SMA65Float/full68SPOT;allnextdailyNov17_00:01,newresearchneveradopted.'"+s[b:];f.write_text(s)
put(R/'read_failures.json',{'round':R.name,'facts':[],'no_completed_model_or_account_window_replays':True});put(R/'stdout_label_notes.json',{'round':R.name,'notes':[{'phase':'review/setup_confirmation.py','clarification':'Legacyactual08stdout refers preserved historical08source;currentfresh query10:30to14:10 isempty if actualpreflightconfirms;account_windows and rawresponse are authoritative.'}],'financial_or_account_reruns':0})
put(R/'primary_source_reads_current.json',{'round':R.name,'recorded_utc':now(),'reads':[{'url':u,'web_reference':v,'access_UTC_date':'2026-11-16','read_success':True} for u,v in [('https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data','turn300view0'),('https://github.com/binance/binance-public-data/blob/master/README.md','turn300view1')]]})
(R/'implementation_plan.md').write_text('固定ETH long-only L5/H.02/E.0075/EWMS16D3K.0075/V6cap.05625/M4/R.01，只改变资金费预算样本logvol窗口VW7/8/9；VW8只读。交叉BTC旧H.03/.0325（L29/E.005/V10cap.0275/recent5min.0025）原银行。W=ETH预算VW，K=BTC主H，资产只沿自身轴；两新ETH+四新父，8旧配置只读。代表VW7/BTCH.03事前固定。完整spec/reserve先于391日实际计算，WF/两轴/1-3成本/事件审计/finish全部正负；货币/模型公式不变，仅VW验证白名单。原账户冻结两小时续接，完整新查资金费，保持08唯一账/full68SPOT/NAV前缀。锁内monitor/check/main提交push/远端核验再解锁；无新分支、子代理、真实订单。\n')
for f in R.rglob('*.py'):ast.parse(f.read_text())
print('PASS prepared ETHbudgetVW7/8old/9 xreadonlyBTCH.03/.0325;onlyVWallowlist extended;asset-specificaxes;0market/accountvaluations')
