"""Derive this round's narrative and handoff from saved results without model execution."""
import ast,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'collect.py';lines=p.read_text().splitlines();out=[]
rules='本轮SMA/single14:30→16:30，仅single按自身原持仓计入Nov15_16真实资金费6条（含ETH零仓位）；L4/FEWM16:10→18:10已在此前记16，本窗不重复。BTC空仓遇负费率为支付，支出按原1/2/3倍压力。日决策与新成交全0，原q/入场价/desired/本金/冻结规则保持，现金只按自己的结算变化，完整NAV前缀核验。下轮SMA/single16:30→18:30、18:31后闭合，L4/FEWM18:10→20:10、20:11后闭合；三账户均已记16各一次，不得重复，所有新窗口仍需完整实际资金费查询，不假定八小时或零。日事件仍Nov16_00:01，原67日权威/66与65前缀保持；新E0/E0.25研究不采用到原账户，旧shadow与十策略真实报价分开。'
action='All3perps booked actualNov15_16 exactly once using their own frozen q/cash;only single books it in this current window. Nextsingle16:30to18:30 and nextL4/FEWM18:10to20:10 must not repeat16;fresh full-window actual-settlement lookup still required,no nominal8hour or zero assumption. Allold08/midnight/daily keys remain once;no daily beforeNov16_00:01,preserve67daily authority andfullNAVprefix.'
for l in lines:
 if l.startswith('h.update(current_daily_event_counts='):
  l=l.split('next_window_funding_action=')[0]+'next_window_funding_action='+repr(action)+',rules='+repr(rules)+')'
 elif l.startswith('h.update(L4_FEWM_actualNov15_16_booked_once='):
  l="h.update(L4_FEWM_actualNov15_16_booked_once=True,single_actualNov15_16_not_yet_booked=False,all3_perp_actualNov15_16_booked_once=True,next_SMA_single_requires_fresh_actual16_lookup=False,next_L4_FEWM_window_requires_fresh_actual16_boundary_lookup=False,all_next_windows_require_complete_fresh_actual_settlement_lookup=True)"
 elif l.startswith("put(R/'next_research_state.json',ns)"):
  l="ns['research']['next_proposal_only']='本轮E0/E0.25及四父已实际finish，所有状态、失败项及旧参考保留，不精确重跑。按本轮多指标配对和参数边界判断收益风险代价，不改门槛或代表；后续只采用预声明的新参数/机制或新闭合研究日，仍待独立未来，不改原账户。'\n"+l
 elif l.startswith('  values=list('):l=l.replace("c['W'] in [.005,.015]","c['W'] in [0.,.005]")
 elif l.startswith('para(f"本轮完成6个新金融配置：'):
  l=l.replace('BTC退出缓冲E1%/E1.5%','BTC退出缓冲E0%/E0.25%')
 elif l.startswith("para('假设与预设："):
  l="para('假设与预设：固定ROC L29/入场H3%/风险V10/cap2.75%，预声明BTC退出缓冲E=[0%,0.25%,0.5%]×ETH R=[.00875,.01]。更窄滞回可能减少不利持仓，也可能带来过早退出、换手和成本；旧E0.5%只读且位于上边界，不能宣称宽平台或全局最优。事前代表E0.25%/R.01固定；完整新定义先reserve再计算，不事后扩批或换代表，仍为复用开发历史。')"
 elif l.startswith("para('BTC规则："):
  l=l.replace('E为0.5%/1%/1.5%','E为0%/0.25%/0.5%').replace('新E1/E1.5','新E0/E0.25')
 elif l.startswith('para(\'\');para(f"事前代表E1%'):
  l=l.replace('事前代表E1%','事前代表E0.25%')
 elif l.startswith("para('BTC E1%组件"):
  l="para('各新组件与父组合的真实通过状态、完整正月、近期正折和失败项按上表/逐项结果保存。组合资格不能替代组件资格；ETH扩展21日PnL若为0，该段父利润仅来自BTC，旧ETH状态不改。代表始终E0.25%/R.01，不事后换成其他格。')"
 elif l.startswith("para('E1%两个新父"):
  l="para(f\"相对匹配ETH预算的旧E0.5%，四项指标同时严格改善（净收益增、整体DD降、Sharpe增、Calmar增）的新父数量{sum(z['net_difference_pp']>0 and z['whole_DD_difference_pp']<0 and z['Sharpe_difference']>0 and z['Calmar_difference']>0 for z in vis['paired_differences_to_old_exit0p5percent'])}/4。所有收益/回撤代价按上述原数值披露，不能只选单一最好格；各指标及并列最优的边界信息另存sensitivity_metric_boundaries.json。小3×2邻域、两档ETH及重复历史不能证明宽平台，全部启发标记保留，待独立未来。\")"
 elif l.startswith('para(f"匹配持有3倍净'):
  l=l.replace('81个严格阈值',"{len(rd(R/'prebinding_parameter_guard_verification.json')['synthetic_checks'])}个严格阈值")
 elif l.startswith('para(f"原账户：'):
  l="para(f\"原账户：SMA/single14:30→16:30、L4/FEWM16:10→18:10；日事件{aw['current_daily_event_counts']}、新成交{aw['current_fills_by_account']}、资金费记录{aw['current_funding_records_by_account']}。真实Nov15_16 fundingTime=1794758400000，BTC/ETH各一笔；仅single在本窗计6条，L4/FEWM此前已记而不重复，三账户全链16UTC各6条且所有键唯一。BTC负费率空仓支付按原1/2/3成本压力，ETH零仓位零金额行保留；各自q/入场价/本金/规则不变，现金按自己的结算改变。\")"
 elif l=="for stem in ['l4h02','fewm']:":l="for stem in ['candidate']:"
 elif l.startswith("para(h['rules']);para(f\"旧午夜源"):
  l="para(h['rules']);para(f\"旧午夜源捕获UTC{h['original_Nov15_00_capture_utc']}、08源捕获UTC{h['original_Nov15_08_capture_utc']}及哈希保持；原16源首次捕获UTC{h['original_Nov15_16_capture_utc']}原字节不改，本轮新查询捕获UTC{fresh['recorded_utc']}，实际公开字段核对完全相等。两次捕获分别留档，不重标原UTC，不复制其他账户现金流。\")"
 elif l.startswith('para(f"有包公共GET '):
  l=l.replace('本轮官方文档两次读取成功，初始未应用的patch格式错误和所有真实失败/恢复','本轮官方文档初次两项读取成功、补充find检索两项timeout，缺rg与过早读取未完成文件等所有真实失败/恢复')
 elif l.startswith("para('复现："):
  l=l.replace('review/configure.py review/prepare.py review/setup.py','review/configure_current.py review/prepare_current.py review/setup_current.py')
 out.append(l)
s='\n'.join(out)+'\n';ast.parse(s)
assert 'single_actualNov15_16_not_yet_booked=True' not in s
assert '81个严格阈值' not in s
assert '本轮16源首次捕获UTC' not in s
p.write_text(s)
print('PASS collection uses actual current axes,own-single funding,new handoff and dynamic outcomes;no model/account calculation')
