"""Adapt readonly reporting to the frozen gamma axis, including next midnight handoff."""
import ast,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'collect.py';s=p.read_text()
s=s.replace("next_L4_FEWM_expected_daily_events_utc=[]","next_L4_FEWM_expected_daily_events_utc=['2026-11-16T00:01:00Z']")
s=s.replace('NextSMA/single18:30to20:30 andL4/FEWM20:10to22:10','NextSMA/single20:30to22:30 andL4/FEWM22:10toNov16_00:10 (crosses00:01daily)')
s=s.replace('SMA/single16:30→18:30、L4/FEWM18:10→20:10','SMA/single18:30→20:30、L4/FEWM20:10→22:10')
s=s.replace('下轮SMA/single18:30→20:30、20:31后闭合；L4/FEWM20:10→22:10、22:11后闭合','下轮SMA/single20:30→22:30、22:31后闭合；L4/FEWM22:10→Nov16_00:10、00:11后闭合，后者跨00:01原日决策，需按原完整日线适配器取得新完成日线及执行参考')
s=s.replace('新研究cap不采纳到原账户','新研究blend不采纳到原账户')
s=s.replace("本轮cap2.625/2.875及四父实际finish后不精确重跑，所有失败项、负收益与旧参考保留。按多指标、净值路径和参数边界判断收益风险代价；事前代表2.625%/R.01不事后换格，原账户不采用新参数，仍待独立未来。","本轮gamma.25/.5及四父实际finish后不精确重跑，所有失败项、负收益与旧参考保留。按多指标、净值路径和边界判断收益风险代价；事前代表gamma.25/R.01不事后换格，原账户不采用新参数，仍待独立未来。")
s='\n'.join(l for l in s.splitlines() if not l.startswith("ca=rd(R/'known_cap_path_alias_verification.json')") and not l.startswith('para(f"额外只读既往固定规则的'))+'\n'
needle="ns['research'].update(signal_scalar_consistency=";idx=s.index(needle);s=s[:idx]+"put(R/'next_research_state.json',ns)\n"+s[idx:]
# Save the final metadata including the scalar consistency fields, after the old cap block was removed.
idx=s.index('\nboundary_rows=[]');s=s[:idx]+"\nput(R/'next_research_state.json',ns)"+s[idx:]
s=s.replace("'BTC_exit_buffer_axis_boundary':c['W'] in [.005,.015]","'BTC_adverse_blend_axis_boundary':c['W'] in [0,.5]")
s=s.replace('BTC入场波动率上限2.625%/2.875%两个组件','BTC方向性逆向波动混合gamma.25/.5两个组件')
s=s.replace('固定风险窗口V10、L29/H3%/E0.5%','固定风险窗口V10与上限2.75%、L29/H3%/E0.5%')
a=s.index("para('假设与预设：");b=s.index("para('ETH只读：",a)
s=s[:a]+'''para('假设与预设：过去10完成日logreturn的总样本波动率会同等惩罚顺势和逆势变化；混合逆期望持仓方向的RMS可能保留有利高波动趋势，也可能放入不利反转。固定gamma=[0,.25,.5]×ETH R=[.00875,.01]，旧gamma0直接复用、位于下边界；事前代表gamma.25/R.01。只在新/反手入场使用风险估计，不在结果后扩批或换代表，仍为复用开发历史。')
para('BTC规则：本金3750/固定名义1000；完成29日ROC严格>3%多、<−3%空，入场优先；带内实际多仅ROC>−0.5%、空仅ROC<0.5%保留，相等退出。完成V10日logreturn r_j，总sigma为无偏样本标准差；意向方向d对应adverse=sqrt(sum(min(d*r_j,0)^2)/10)，目标0、分母n。风险=(1-gamma)*sigma+gamma*adverse；仅新/反手风险≤2.75%才允许，同向q保持。gamma0等于旧总波动策略，只读；.25/.5从原现金完整计算391日。下一00:01 OPEN、不利tick、LOT向下；成交冲击仍用过去20日总波动，未使用更低风险估计减成本。')
'''+s[b:]
s=s.replace('BTC入场波动率上限三档','BTC逆向波动混合gamma三档').replace('BTC组件只沿上限轴','BTC组件只沿gamma轴')
s=s.replace('|BTC入场波动率上限|','|BTC逆向混合gamma|').replace('f"{100*c[\'W\']:g}%"','f"{c[\'W\']:g}"')
s=s.replace('事前代表cap2.625%/','事前代表gamma.25/').replace('代表始终cap2.625%/','代表始终gamma.25/')
s=s.replace("BTC入场cap{100*c['W']:g}%/","BTC逆向混合gamma{c['W']:g}/")
s=s.replace('paired_differences_to_old_cap2p75percent','paired_differences_to_old_gamma0').replace('BTC_entry_volatility_ceiling','BTC_adverse_volatility_blend')
s=s.replace('配对旧cap2.75%：新cap','配对旧gamma0：新gamma').replace("{100*z['BTC_adverse_volatility_blend']:g}%/","{z['BTC_adverse_volatility_blend']:g}/")
s=s.replace('相对匹配ETH预算的旧cap2.75%','相对匹配ETH预算的旧gamma0')
s=s.replace('策略引擎仅扩展预声明入场波动率上限的参数白名单，归一化该白名单后完整AST相同','策略引擎有意改变BTC入场风险公式并增加审计字段；simulate及其他既有辅助函数AST、ETH分支与资金核算核心保持。合成检查独立计算方向符号、RMS分母、严格阈值、gamma0等价、真实入口及未来后缀')
s=s.replace('review/configure_caps.py review/prepare_caps.py review/setup_caps.py','review/configure_blend_retry1.py review/prepare_blend.py review/setup_blend.py；首次configure失败原源/回执保留，恢复发生于reserve前')
ast.parse(s);p.write_text(s)
p=R/'finalize.py';s=p.read_text().replace("assert not h['next_SMA_single_expected_daily_events_utc'] and not h['next_L4_FEWM_expected_daily_events_utc']","assert not h['next_SMA_single_expected_daily_events_utc'] and h['next_L4_FEWM_expected_daily_events_utc']==['2026-11-16T00:01:00Z']")
s=s.replace("'preparation_failures_before_binding':0","'preparation_failures_before_binding':1").replace('invalid_preparation_attempts=0','invalid_preparation_attempts=1')
ast.parse(s);p.write_text(s)
print('PASS readonly gamma report, truthful intentional-policy-change metadata and next L4/FEWM midnight daily-event handoff configured')
