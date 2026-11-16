"""Freeze conditional BTC entry-volatility cap neighborhood;all financial engine bytes unchanged."""
import ast,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261116T120809Z';sys.path.insert(0,str(R));from common import *
assert not (R/'plan.json').exists()
def edit(n,pairs):
 f=R/n;s=f.read_text()
 for a,b in pairs:assert a in s,(n,a);s=s.replace(a,b)
 ast.parse(s);f.write_text(s)
assert sha(P/'engine.py')==sha(R/'engine.py') and sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py')
for n in ['run.py','audit.py','exports.py']:edit(n,[('BTC_RECENT_CONFIRM_MIN_RETURN','BTC_CONFIRM_VOL_CAP')])
edit('parent_units.py',[("g['W']==.0025","g['W']==.0275")])
edit('exports.py',[("BTC minimum 5-day directional ROC (fraction)","BTC V10 entry-volatility ceiling (fraction)"),("['0 (old)','0.0025','0.0050']","['0.02625','0.02750 (old)','0.02875']"),('Preregistered BTC minimum5day directional confirmation','Preregistered conditional BTC entry-volatility caps')])
for n in ['review/diagnostics.py','review/visual_review.py']:
 f=R/n;s=f.read_text().replace('BTC_confirmation_min_return','BTC_entry_volatility_ceiling').replace('btc[0]','btc[.0275]').replace('for V in [.0025,.005]','for V in [.02625,.02875]').replace("c['W']==0","c['W']==.0275").replace("best['W'] in [0,.005]","best['W'] in [.02625,.02875]").replace('confirmation0','cap0275').replace('{0,.0025,.005}','{.02625,.0275,.02875}').replace('==[.0025,.005]','==[.02625,.02875]').replace("volatility_ceiling']==0","volatility_ceiling']==.0275").replace('three minimum5day confirmation hurdles','three conditional BTC V10 entry-volatility caps').replace('old zero-hurdle confirmation reference at lower boundary','old cap.0275/min5dayROC.0025 reference at center');ast.parse(s);f.write_text(s)
f=R/'review/totalrisk_history_aliases.py';s=f.read_text().replace("'confirmation_min_return':c['W']","'conditional_entry_vol_cap':c['W']");f.write_text(s)
# Publication metadata will use actual current nonfinancial failures,not the previous round's count.
f=R/'finalize.py';s=f.read_text().replace("'configure_hurdle_finish.py'","'configure_caps.py'").replace("'hurdle_effect.py'","'cap_effect.py'").replace('paired_differences_to_old_confirmation0','paired_differences_to_old_cap0275').replace("['2026-11-16T04:30:00Z','2026-11-16T06:30:00Z']","['2026-11-16T06:30:00Z','2026-11-16T08:30:00Z']").replace("['2026-11-16T06:10:00Z','2026-11-16T08:10:00Z']","['2026-11-16T08:10:00Z','2026-11-16T10:10:00Z']").replace("'BTC_recent_direction_confirmation_entry_policy_intentionally_changed':True","'BTC_recent_direction_confirmation_entry_policy_intentionally_changed':False").replace('fixed5dayminimumhurdle.0025/.005','fixed5daymin.0025BTCvolcap.02625/.02875').replace('minimum_hurdle_effect_decomposition.json','conditional_cap_effect_decomposition.json');ast.parse(s);f.write_text(s)
f=R/'publish.py';s=f.read_text().replace('research: test minimum BTC confirmation strength and preserve original accounts','research: test volatility caps with directional confirmation and book actual funding');f.write_text(s)
put(R/'primary_source_reads_current.json',{'round':R.name,'observed_reads_recorded_utc':now(),'reads':[{'url':u,'web_reference':v,'access_UTC_date':'2026-11-16','read_success':True} for u,v in [('https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data','turn296view0'),('https://github.com/binance/binance-public-data/blob/master/README.md','turn296view1')]],'HTTP_capture_timestamp_not_claimed':True})
put(R/'stdout_label_notes.json',{'round':R.name,'notes':[],'current_scalar_and_window_labels_checked_before_binding':True,'old_round_raw_logs_and_errata_preserved':True,'financial_or_account_reruns':0})
(R/'research_work_plan.md').write_text('事前固定确认5日/最低同向ROC0.25%，BTC总样本logvolV10上限C=[.02625,.0275,.02875]×只读ETH预算R=[.00875,.01]；旧C.0275只读，两新BTC+四父逐个reserve后完整391日计算，代表C.02625/R.01。引擎和money核心字节保持，仅参数变化；同向持仓/正常退出、rawwholebank[1,1]原规模不变。完成WF/两轴敏感性/1/2/3成本/独立审计并finish全部正负。原账户SMA/single04:30→06:30，L4/FEWM06:10→08:10；新查完整真实结算并按自身旧q记账，不假定8h时刻或复制现金流，full68SPOT权威保持。锁内monitor/check/main提交push与完整远端核验再解锁。\n')
print('PASS BTCvolcaps.02625/.0275old/.02875 x ETHbudget,fixed5daymin.0025,preset.02625/.01;engine/money unchanged;0financialcalls')
