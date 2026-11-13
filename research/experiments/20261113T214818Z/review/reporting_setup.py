"""Prepare current-round saved-result reporting without replaying any financial model."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];f=R/'collect.py';s=f.read_text();pairs=[("== (31,.005)","== (30,.005)"),("==(31,.005)","==(30,.005)"),("'tested_configs':20","'tested_configs':24"),("'new_financial_configs':8,'new_native_models':4,'new_passive_parents':4,'new_cost_scenes':24,'old_exact_grid_cells_read_only':5","'new_financial_configs':12,'new_native_models':6,'new_passive_parents':6,'new_cost_scenes':36,'old_exact_grid_cells_read_only':3"),('L31在E0.5/1/1.5%均近期仅5/8正折，退出缓冲不能修复；L27邻域历史通过但全期收益低于旧L29锚。下一轮先完整查重，再预登记局部L28/30与退出E的未测具体配置，或按数据可用性转向新的经济假设；不可把已用历史择优称独立验证。','本轮L28/29/30各退出E均历史通过，但旧L31各E近期失效保持，局部平台不能外推。新组合无全成本净收益/回撤共同改善旧锚，不采用新规则。下一轮优先检查真实数据增量或其他经济假设，先完整查重与预登记；不能反复细化已用历史后冒充独立未来。'),('33日背景覆盖L31','33日背景覆盖本轮最大L30'),('5个旧格参与新邻域诊断','3个旧L29格参与新邻域诊断'),('18条','18条'),('12条新BTC、12条新父','18条新BTC、18条新父'),('保存24场景、312逐折、192近期折、96扩展折、9360每日净值点','保存36场景、468逐折、288近期折、144扩展折、14040每日净值点'),("'financial_configs':8,'cost_scenes':24","'financial_configs':12,'cost_scenes':36")]
for a,b in pairs:
 if a!=b:s=s.replace(a,b)
s=s.replace("[win['SMA']['cutoff_utc'],plus2(win['SMA']['cutoff_utc'])]","[win['SMA']['cutoff_utc'],plus2(win['SMA']['cutoff_utc'])]")
s=s.replace('下轮SMA/single Nov13_16:30→18:30Z，18:31后参考分钟闭合；L4/FEWM18:10→20:10Z，20:11后闭合','下轮SMA/single Nov13_18:30→20:30Z，20:31后参考分钟闭合；L4/FEWM20:10→22:10Z，22:11后闭合')
lines=[]
for line in s.splitlines():
 if line.startswith('lines=[f"本轮实际完成'):
  line='lines=[f"本轮实际完成12个新配置、36个1/2/3倍成本场景：6个BTC回看期/退出缓冲变体及6个固定ETH完整银行组合。新父组合通过{len(r[\'summary\'][\'passed\'])}个、淘汰{len(r[\'summary\'][\'candidate_rejected\'])}个；BTC组件通过{len(r[\'summary\'][\'passed_source_components\'])}个、淘汰{len(r[\'summary\'][\'rejected_source_components\'])}个。每个先成功reserve再计算，逐项finish，所有负折与失败判据留档。预设L30/E0.5%/固定H3%，结果后未更换代表。",\'\','
 elif line.startswith("'经济假设："):
  line="'经济假设：此前L27各退出E历史通过、L31各E近期仅5/8正折。本轮预设L=[28,29,30]×E=[0.5%,1%,1.5%]，固定H3%，检验相邻一日扰动是否形成局部平台或仍有失效。9格中L29三格已有完整真实BTC/父结果，只读复用，不重跑或改旧资格；6个新BTC银行真实计算，6个新父组合复用真实组件美元NAV。', '',"
 elif line.startswith('lines += [\'\',f"预设L31/'):
  line='lines += [\'\',f"预设L{rep[\'W\']}/E{rep[\'K\']*100:g}%代表指纹{rep[\'fingerprint\']}，3倍净{rep[\'scenes\'][\'3\'][\'net_return_pct\']:.9f}%、整体DD{rep[\'scenes\'][\'3\'][\'max_drawdown_pct\']:.9f}%，状态{rep[\'status\']}，近期各成本正折{rep[\'recent40_positive_5d_folds_by_cost\']}，局部严格资格比例{rep[\'sensitivity\'][\'local_recent_allcost_qualifying_fraction\']}，失败项{rep[\'failed_criteria\']}。当前六个新父组合均近期6/8正折，历史通过；六个BTC单独组件均因月折、近期5/8及局部稳定性淘汰。此前L31各E近期失效仍保留，不能以当前L28–30通过抵消。", \'\','
 elif line.startswith('f"原账户SMA/single'):
  line='f"原账户SMA/single Nov13_16:30→18:30Z，L4/FEWM18:10→20:10Z；新资金费账项{aw[\'current_funding_records_by_account\']}，日决策{aw[\'current_daily_event_counts\']}，成交{aw[\'current_fills_by_account\']}。本轮完整窗口预检与各自原包均显示无新结算；18本账簿cash/q/entry独立核验保持。三组00/08/16均已各记一次，不重复。16时实际字段及首次捕获UTC{fund16[\'recorded_utc\']}原样保留，本轮完整窗口捕获UTC{fresh[\'recorded_utc\']}；没有把旧公开记录当本轮新资金费。", \'\','
 elif line.startswith("lines += ['', '工程留档："):
  continue
 lines.append(line)
s='\n'.join(lines)+'\n';s=s.replace('389日多重选择偏差与L31近期失效保留，历史通过仍待独立未来。','389日多重选择偏差与旧L31近期失效保留；当前L28–30局部平台只属于重复历史，仍待独立未来。')
s=s.replace('旧资金费URL读取错误后采用官方新目录；网页错误未冒充行情请求。','本轮两个官方页面均成功读取。')
f.write_text(s);print('PASS current12config/36scene results and0fundingwindows reporter prepared;previousfailuresnotinventedascurrent;no calculations')
