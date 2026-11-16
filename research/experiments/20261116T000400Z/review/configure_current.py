"""Freeze narrower exits and correct current-window metadata before any reservation."""
import ast,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R))
from common import put,now,sha,rel
assert not any((R/n).exists() for n in ['plan.json','batch.json','report.json','code_binding_before_evaluation.json'])
def edit(name,pairs):
 p=R/name;s=p.read_text()
 for a,b in pairs:
  assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);p.write_text(s)
edit('freeze.py',[
 ('[.005,.01,.015]','[0.,.0025,.005]'),('[.01,.015]','[0.,.0025]'),
 ('(.01,.01)','(.0025,.01)'),("{'W':.01,'K':.01}","{'W':.0025,'K':.01}"),
 ('Does wider BTC actual-position exit buffer E1/1.5percent','Does narrower BTC actual-position exit buffer E0/0.25percent'),
 ('Wider hysteresis may reduce premature exits/turnover but tolerate more adverse movement. Preset E.01/R.01','Narrower hysteresis may reduce adverse retention but increase premature exits and turnover. Preset E.0025/R.01'),
 ('E=.005/.01/.015 (0.5/1/1.5percent)','E=0/.0025/.005 (0/0.25/0.5percent)'),
 ('New BTC exit buffers E.01/.015','New BTC exit buffers E0/.0025'),
 ('Old E.005 reference is a boundary','Old E.005 reference is the upper boundary'),
 ('old E.005 at grid boundary','old E.005 at upper grid boundary'),
 ('explicit3BTCexitbuffersx2ETHR','explicit3narrowBTCexitbuffersx2ETHR')])
edit('definitions.py',[
 ('[.005,.01,.015]','[0.,.0025,.005]'),('[.01,.015]','[0.,.0025]')])
edit('parent_units.py',[
 ("[F('.005'),F('.01'),F('.015')]","[F(0),F('.0025'),F('.005')]"),
 ("g['W']==.01","g['W']==.0025")])
edit('audit.py',[('[.005,.01,.015]','[0.,.0025,.005]')])
edit('exports.py',[("['0.5%','1.0%','1.5%']","['0%','0.25%','0.5%']")])
edit('review/diagnostics.py',[
 ('for V in [.01,.015]:','for V in [0.,.0025]:'),
 ("best['W'] in [.005,.015]","best['W'] in [0.,.005]")])
edit('review/visual_review.py',[
 ('{.005,.01,.015}','{0.,.0025,.005}'),('[.01,.015]','[0.,.0025]'),
 ('old0.5percent reference at a boundary','old0.5percent reference at the upper boundary')])
split="{'SMA':0,'candidate':6,'l4h02':0,'fewm':0}"
edit('checks.py',[
 ("{'SMA':0,'candidate':0,'l4h02':6,'fewm':6} and len(cashflows)==12",split+' and len(cashflows)==6'),
 ("z['account'] in ['l4h02','fewm']","z['account']=='candidate'"),
 ('actualNov15_16fundsplit0/0/6/6','actualNov15_16fundsplit0/6/0/0')])
edit('review/account_continuity.py',[
 ("{'SMA':0,'candidate':0,'l4h02':6,'fewm':6}",split),
 ("actual16==(0 if stem=='candidate' else 6)",'actual16==6'),
 ('len(cashflows)==12','len(cashflows)==6'),
 ('ownL4/FEWMactual16fund12rows','ownSingleActual16fund6rows')])
edit('forward_registry.py',[
 ('Nov14dailyalreadybooked; next daily event2026-11-15UTC00:01','Nov15dailyalreadybooked; next daily event2026-11-16UTC00:01')])
p=R/'finalize.py';s=p.read_text()
s=s.replace(", 'collect_retry1', 'final_checks_retry1', 'collect_retry2', 'final_checks_retry2'",'')
s=s.replace("'configure.py'","'configure_current.py'")
s=s.replace("'prepare.py'","'prepare_current.py'")
s=s.replace("'setup.py'","'setup_current.py'")
s=s.replace(", 'correct_visual_label.py', 'validate_sources_axes.py', 'fix_seal_daily_assertion.py', 'validate_sources_seal.py'",'')
s=s.replace("{'SMA':0,'candidate':0,'l4h02':6,'fewm':6}",split)
s=s.replace("['2026-11-15T14:30:00Z','2026-11-15T16:30:00Z']","['2026-11-15T16:30:00Z','2026-11-15T18:30:00Z']")
s=s.replace("['2026-11-15T16:10:00Z','2026-11-15T18:10:00Z']","['2026-11-15T18:10:00Z','2026-11-15T20:10:00Z']")
s=s.replace("'initial_freeze_patch_format_error':1,'setup_patch_error_resolved_before_binding':True","'search_utility_unavailable':1,'premature_dependent_read':1,'all_resolved_before_financial_binding':True")
s=s.replace("'only_L4_FEWM_booked_current_window':True,'single_still_pending16':True","'only_single_booked_current_window':True,'all3_perps_actual16_booked_once':True")
s='\n'.join(l for l in s.splitlines() if not l.startswith("assert rd(R/'visual_axes_label_correction.json')") and not l.startswith("assert rd(R/'seal_daily_assertion_fix.json')"))+'\n'
ast.parse(s);p.write_text(s)
edit('publish.py',[('research: validate BTC exit buffers and settle original L4 FEWM funding','research: validate narrow BTC exits and settle original single funding')])
edit('collect.py',[
 ('research/experiments/20261115T220354Z/signal_description_erratum.json','research/experiments/20261115T200222Z/signal_description_erratum.json')])
put(R/'stdout_label_notes.json',{'round':R.name,'notes':[],'current_scalar_and_funding_split_labels_checked_before_binding':True,'old_round_raw_logs_and_errata_preserved':True,'financial_or_account_reruns':0})
put(R/'primary_source_reads_current.json',{'round':R.name,'observed_reads_recorded_utc':now(),'reads':[
 {'requested_url':'https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History','actual_url':'https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data','web_reference':'turn288view0','access_UTC_date':'2026-11-16','read_success':True,'redirected':True},
 {'requested_url':'https://github.com/binance/binance-public-data/blob/master/README.md','actual_url':'https://github.com/binance/binance-public-data/blob/master/README.md','web_reference':'turn288view1','access_UTC_date':'2026-11-16','read_success':True}],
 'tool_timeouts':0,'HTTP_capture_timestamp_not_claimed':True})
plan=['本轮预先固定BTC退出缓冲E0%/0.25%/0.5% × ETH预算R .00875/.01；L29/H .03/V10/cap .0275、BTC3750/1000及ETH15000/4000固定，raw[1,1]不归一化。旧E0.5%和ETH银行只读，新2原生+4父；预设E0.25%/R.01，不看结果后换代表。',
 '检验更窄退出带能否减少不利持仓，同时如实承担更早退出、换手与成本的代价。沿用原引擎/Decimal资金核心，所有新spec独立reserve后一次实际计算；391日仍为反复开发历史，逐折、敏感性、多指标和三倍成本不替代独立未来。',
 'SMA/single14:30→16:30，L4/FEWM16:10→18:10。新查完整窗口资金费并对比上轮原16UTC公开字段与首次捕获UTC；仅single按自身原q入账一次，L4/FEWM已入账不得重复，不复制现金流。原67日SMA权威及66/65前缀不改，无新日决策/成交。',
 '本轮应用Ponytail复用现有核算和Verification-before-completion实际核验；用户已明确授权预设参数探索和直接完成，不另开审批或委派子代理。完成登记、checks、锁内只读snapshot/check、main提交push、整树远端核验后释锁。']
(R/'research_work_plan.md').write_text('\n\n'.join(plan)+'\n')
print('PASS current narrower-exit rules,axes,raw weights and own funding expectations configured before any reservation')
