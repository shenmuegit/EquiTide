"""All signed-perpetual outcomes,cost/funding attribution and Chinese limitations."""
import csv,gzip,io,json,statistics
from collections import Counter,defaultdict
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,LOOKS,HURDLES,sha,put

def csvwrite(path,rows,compressed=False):
 fields=list(dict.fromkeys(k for x in rows for k in x));buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);raw=buf.getvalue().encode();path.write_bytes(gzip.compress(raw,mtime=0) if compressed else raw)

def main():
 report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());ctx=json.loads((R/'context.json').read_text());cfgs=report['configs'];candidates=[c for c in cfgs.values() if c.get('role')!='benchmark'];by={(x['asset'],x['lookback_days'],x['return_hurdle']):x for x in candidates};bench={x['asset']:x for x in cfgs.values() if x.get('role')=='benchmark'};rows=[];folds=[];daily=[];costs=[];fund=[];margins=[];edges=[];paths=defaultdict(list)
 for c in cfgs.values():
  paths[tuple(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3'])].append(c['name'])
  for k,z in c['scenes'].items():
   meta={'configuration':c['name'],'role':c.get('role','candidate'),'asset':c['asset'],'lookback_days':c['lookback_days'],'return_hurdle':c['return_hurdle'],'cost_multiplier':k};rows.append({**meta,**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','mark_observation_drawdown_pct','trade_proxy_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_reference_PnL_to_execution_cost','executions','round_trips']},'positive_folds':sum(f['net_return_pct']>0 for f in z['folds']),'local3_positive_fraction':c['sensitivity'].get('local_3x_neighbor_positive_fraction'),'status':c['status']});folds.extend({**meta,**f} for f in z['folds']);daily.extend({**meta,'boundary_index':i,'NAV_usdt':v} for i,v in enumerate(z['daily_equity_usdt']));costs.append({**meta,'total_cost_usdt':z['cost_usdt'],**z['cost_parts_usdt']});fund.append({**meta,**{p:z[p] for p in ['funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','funding_settlements','nonzero_funding_settlements']}});margins.append({**meta,**z['margin']})
  if c.get('role')!='benchmark':c['same_budget_hold_comparison']={k:{'return_difference_pct':z['net_return_pct']-bench[c['asset']]['scenes'][k]['net_return_pct'],'composite_DD_difference_pct':z['max_drawdown_pct']-bench[c['asset']]['scenes'][k]['max_drawdown_pct']} for k,z in c['scenes'].items()}
 for asset in ['BTC','ETH']:
  es=[]
  for i,L in enumerate(LOOKS):
   for j,H in enumerate(HURDLES):
    a=by[asset,L,H]
    for ni,nj,axis in [(i+1,j,'lookback_days'),(i,j+1,'return_hurdle')]:
     if ni<3 and nj<3:
      b=by[asset,LOOKS[ni],HURDLES[nj]];es.append({'asset':asset,'from':a['name'],'to':b['name'],'axis':axis,'absolute_3x_Sharpe_difference':abs(a['scenes']['3']['sharpe_365']-b['scenes']['3']['sharpe_365'])})
  threshold=2*statistics.stdev(x['absolute_3x_Sharpe_difference'] for x in es)
  for e in es:e.update(threshold=threshold,descriptive_cliff_flag=e['absolute_3x_Sharpe_difference']>threshold)
  edges+=es
 report['sensitivity_cliffs']={'heuristic':'Adjacent3xdailySharpe difference>2sampleSDwithinasset;descriptiveonly.','edges':edges};report['failure_counts']=dict(Counter(k for c in candidates for k,v in c['criteria'].items() if not v));report['within_batch_path_equivalence']={'unique_full_three_cost_NAV_paths':len(paths),'parameter_definitions':20,'groups':[{'names':names,'NAV_sha256_by_cost':dict(zip(['1','2','3'],key))} for key,names in paths.items()],'scope':'All paths on same reused330daymarket;new derivatives,timewindowandledger do not create independentmarket samples.'};report['research_context']={'prior_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_canonical_research_definitions':ctx['canonical_research_definitions_excluding_observations'],'prior_conclusions_read':len(ctx['prior_conclusions_read']),'initial16_missing_actual_results':0,'independent_final_holdout':False,'DSR_PBO_computed':False};report['benchmark_registration']={'plan':'research/experiments/'+R.name+'/benchmark_plan.json','sha256':sha(R/'benchmark_plan.json'),'reserved_before_any_real_financial_calculation':True,'initial18candidate_specs_or_main_plan_bytes_changed':False};report['artifacts']={'full_results':'results/*.json.gz','all_cost_scenes':'sensitivity.csv','fold_results':'fold_results.csv','daily_NAV':'daily_equity.csv.gz','execution_cost_parts':'cost_scenarios.csv','funding':'funding_scenarios.csv','margin':'margin_scenarios.csv','surface':'sensitivity_surface.png','independent_verification':'verification.json'};put(R/'report.json',report)
 for name,data,compressed in [('sensitivity.csv',rows,False),('fold_results.csv',folds,False),('daily_equity.csv.gz',daily,True),('cost_scenarios.csv',costs,False),('funding_scenarios.csv',fund,False),('margin_scenarios.csv',margins,False)]:csvwrite(R/name,data,compressed)
 fig,axes=plt.subplots(1,3,figsize=(15,4.5),constrained_layout=True);limit=max(abs(c['scenes']['3']['net_return_pct']) for c in candidates)
 for asset,ax in zip(['BTC','ETH'],axes):
  vals=np.asarray([[by[asset,L,H]['scenes']['3']['net_return_pct'] for H in HURDLES] for L in LOOKS]);im=ax.imshow(vals,cmap='RdYlGn',vmin=-limit,vmax=limit);ax.set(xticks=range(3),xticklabels=['1%','2%','4%'],yticks=range(3),yticklabels=LOOKS,xlabel='Absolute return band',ylabel='Perpetual return lookback days',title=asset+' signed trend:3x costs')
  for i in range(3):
   for j in range(3):ax.text(j,i,f'{vals[i,j]:+.2f}%',ha='center',va='center')
 fig.colorbar(im,ax=list(axes[:2]),label='3x net return % of10000collateral',shrink=.8)
 for asset,color in [('BTC','tab:blue'),('ETH','tab:orange')]:
  for c,label,style in [(by[asset,10,.02],asset+' L10/H2%','-'),(bench[asset],asset+' constantlong','--')]:
   vals=c['scenes']['3']['daily_equity_usdt'];axes[2].plot(np.arange(len(vals)),np.asarray(vals)/100,label=label,color=color,linestyle=style)
 axes[2].axhline(100,color='grey',linestyle=':',label='Cash,zero yield');axes[2].set(xlabel='OOS daily boundary (330days)',ylabel='NAV / initial collateral %',title='Preset centers and same-budget controls');axes[2].legend(fontsize=7);fig.savefig(R/'sensitivity_surface.png',dpi=140);plt.close(fig)
 s=report['summary'];near=by['BTC',20,.01];z=near['scenes']['3'];minbuffer=min(c['scenes'][k]['margin']['minimum_equity_minus_maintenance_usdt'] for c in cfgs.values() for k in ['1','2','3']);lines=['# BTC/ETH永续双向动量：真实资金费与独立保证金账本','',f"轮次`{R.name}`，主计划SHA256`{report['frozen_plan_sha256']}`。18候选＋2同资金恒多参考，全部先reserve再计算，60个成本场景/660逐折真实留档。候选通过{len(s['passed'])}、淘汰{len(s['rejected'])}，1/2/3倍成本净正{s['positive_configs_by_cost']['1']}/{s['positive_configs_by_cost']['2']}/{s['positive_configs_by_cost']['3']}。两参考单列，不计alpha资格；3原SMA截止另行登记。",'',
 '## 假设与事前固定规则','',
 '此前现货长仓与事件反弹常在持续下跌期受损，本轮检验永续双向自身收益动量能否覆盖跌势，同时扣除真实资金费。作者[AQR2012时序动量](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)是多资产期货12月研究，本批5/10/20日加密规则不是其复现或盈利背书。',
 '每日UTC00:00前一完整永续日收盘j=i−1，r=C[j]/C[j−L]−1；L={5,10,20}，H={1%,2%,4%}。严格r>H目标+1多头，严格r<−H目标−1空头，其他情况（含等于边界）目标现金。信号只用当时已闭合永续价格，不用资金费、未来mark或收益择优。下一00:01真实分钟OPEN先关旧向，再开新向；同方向保留原数量，不每日再平衡。',
 '每配置独立10000USDT抵押，原值20%表示固定入场名义额2000USDT；新仓q=方向×floor(2000/前日完整收盘/lot)×lot，不由未来OPEN、NAV或未公开资金费调整数量。lot/跳空会使实际名义额偏离20%。开仓名义额另限≤扣费后抵押（1倍上限）。不把20%归一为100%，不按已占保证金放大ROI；无现金利息、跨账户调拨、现货借币或空头借币费。',
 '线性永续开仓仅扣手续费，不按现货买入那样扣名义本金；账面PnL=带符号q×(估值价−实际入场价)。平仓结算q×(实际退出价−实际入场价)并再扣费。OOS仅一次空仓抵押起步，跨折保留数量、入场价格与抵押，终点成本清仓。所有币种合约乘数经真实元数据核对为1。',
 '在任何真实金融计算前补充了2个同窗、同10000抵押/2000原值名义额、同资金费和成本的恒定做多参考；benchmark_plan.json和两个reserve回执记录时序。主计划原字节与18候选spec未改。', '',
 '## 真实数据、资金费可得性和价格口径','',
 '8份实际归一化Parquet：每币525600根完整分钟永续bar、8760根标记小时bar、1095个真实资金费结算及1份lot/tick/minNotional/合约乘数元数据，原始字节数/哈希/路径见plan和data_manifest。输入2025-09-16至2026-09-16；OOS2025-10-19 00:01至2026-09-14 00:01UTC，330日/11连续30日折，30日初始上下文＋3日间隔，保证20完整日永续ADV/波动和信号回看均可用。未把只有现货上下文的前30天硬充永续回测。',
 '[Binance资金费定义](https://www.binance.com/en/support/faq/detail/360033525031)：在真实settlement纳秒时间，经济现金流=−带符号q×真实结算mark×真实rate，只计当时旧仓。00:00或00:00.001结算均在00:01换向之前，不将费用转给新仓。原available_ts通常延迟1小时，真实保留；费率只是事后经济记账，既不预测也不进入固定入场数量。交易接受按模型经纪抵押约束，未声称具有当时私人账户流证据。1/2/3成本压力放大负资金费支出，正收入不放大；平仓状态资金费0也保留以核验完整990次OOS结算。',
 '[Binance Mark/Last与保证金](https://www.binance.com/en/support/faq/detail/360033525271)：真实mark仅有小时及资金费结算点，不能伪造分钟mark。主NAV为明确的混合采样风险代理：分钟成交收盘代理、真实小时mark收盘/结算mark、成交前后OPEN参考和终点现金，逐场景486093点；另报纯mark观察DD与成交代理DD。它不是交易所逐tick mark权益或真实强平轨迹。原始采样/纳秒排序和全NAV SHA可重建，时间相同按minuteclose→hourmark→fundpre/post→tradepre/post顺序。',
 '保证金用1%名义额维护率作为显式研究代理（沿用既有carry保守约束），对每个状态覆盖的完整OOS已闭合小时应用不利mark高/低边界，可能重复覆盖同一小时，更为保守；首末不完整小时缺全mark极值。没有完整历史阶梯/清算费/逐tick强平引擎。任何代理越界都禁止晋级，不捏造强平成交。基础费率5bp/侧沿用旧carry.py假设，并非历史VIP费率已核验。','',
 '## 三项验证与门槛','',
 '- Walk-forward：11×30日因果验证，不拟合、无未来标签，purge不适用；初始上下文30日＋3日间隔，价格和账户跨折连续，信号可得后60秒才用OPEN执行参考。保存60场景/660折及连续整体混合采样DD；同一年度已被重复研究，不能称未触碰最终测试。',
 '- Sensitivity：两币各L×H3×3，局部相邻索引矩形含中心；54候选成本场景及6参考成本场景全部保存收益/DD/Sharpe/Calmar，24条邻接差描述断崖，无OOS自适应扩网格。',
 '- Costs：每侧手续费5bp、半价差1bp、滑点2bp，加0.5×过去20完整永续日日log收益样本波动×sqrt(名义额/永续quote ADV)冲击；参与率≤0.1%，原生Decimal28不利tick及真实lot/minNotional。1/2/3倍所有执行费用和负资金费支出，正资金费收入不增。缺历史L2、队列/延迟、完整maxQty/percentfilter、VIP费率及真实TCA，只能作条件性历史模型。',
 '门槛：三成本净正、1倍≥8/11正折、3倍混合采样DD≤25%、局部3倍净正比例≥60%、1倍≥4往返、1倍毛参考价格PnL加真实资金费/执行费≥2.5、无负抵押/拒单/保证金代理越界、终点空仓。毛加回不是独立零成本策略。', '',
 '## 全部候选结果','', '|币|L|H|1倍|2倍|3倍|1倍正折|3倍混合DD|3倍mark观察DD|3倍资金费USDT|1倍往返|邻域3倍正比例|状态|','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
 for c in candidates:
  a,b,z0=[c['scenes'][k] for k in ['1','2','3']];lines.append(f"|{c['asset']}|{c['lookback_days']}|{c['return_hurdle']:.0%}|{a['net_return_pct']:+.3f}%|{b['net_return_pct']:+.3f}%|{z0['net_return_pct']:+.3f}%|{c['positive_folds_1x']}/11|{z0['max_drawdown_pct']:.3f}%|{z0['mark_observation_drawdown_pct']:.3f}%|{z0['funding_usdt']:+.3f}|{a['round_trips']}|{c['sensitivity']['local_3x_neighbor_positive_fraction']:.1%}|{c['status']}|")
 lines+=['',f"BTC20日/1%在1/2/3倍成本下均净正，3倍{z['net_return_pct']:+.6f}%，混合采样DD{z['max_drawdown_pct']:.6f}%，1倍{near['positive_folds_1x']}/11正折、{near['scenes']['1']['round_trips']}往返；仅邻域正比例不足而淘汰。这比前轮仅2正折的稀疏反弹证据更完整，但不同市场/窗口/20%原值敞口，不作严格业绩改善归因。ETH20日/1%3倍约+4.03%，仅6正折。所有绿点处在最长20日边界，未形成≥60%邻域平台，不因最高值临时增加参数或提前称合格方法。",'',
 f"最低不利整小时保证金代理余量{minbuffer:.6f}USDT，实际无代理越界/拒单/负抵押；这仅证明声明模型的采样约束，不是真实逐tick清算安全保证。两预设10日/2%中心3倍分别{by['BTC',10,.02]['scenes']['3']['net_return_pct']:+.6f}%/{by['ETH',10,.02]['scenes']['3']['net_return_pct']:+.6f}%。",'',
 '失败计数：`'+json.dumps(report['failure_counts'])+'`。18候选全部rejected，保留所有正负结果，不称稳定实盘盈利。','',
 '## 同资金真实持有参考','', '|参考|1倍|2倍|3倍|3倍资金费|3倍混合DD|','|---|---:|---:|---:|---:|---:|']
 for asset,c in bench.items():lines.append('|'+asset+'恒多|'+'|'.join(f"{c['scenes'][k]['net_return_pct']:+.3f}%" for k in ['1','2','3'])+f"|{c['scenes']['3']['funding_usdt']:+.3f}|{c['scenes']['3']['max_drawdown_pct']:.3f}%|")
 lines+=['','同资金同窗恒多参考只作比较，不计候选资格；收益为占10000初始抵押比例，没有将2000名义额20%归一化。现金零利息为解析0基准。全部逐成本差额留report.same_budget_hold_comparison，不平均多币Sharpe或回撤。','',
 '## 完整登记、核验与续接','',f"计算前完整读取{ctx['registry_events']}事件/{ctx['registry_ids']}ID、{ctx['canonical_research_definitions_excluding_observations']}个规范研究定义、{len(ctx['prior_conclusions_read'])}份旧结论；初始16项均有真实证据。18新永续方向规则与2参考全部reserve成功才计算，没有把已有现货组件的NAV缩放成永续收益。",'',
 '新账本合成检查覆盖多空符号、开仓只扣费用、交易历史不可被后续资金费修改、资金费方向/支出压力、1倍抵押上限、参与率拒单、门槛严格比较和未来前缀不变。实际独立审核不调用生产trade/funding函数，以整数交叉乘法复核信号和已知价格数量，逐笔重算带符号盈亏/五项费用、59400次结算（含空仓0）、完整混合NAV、mark/成交代理子曲线及720整体/逐折指标；不将工程通过代替回测。',
 '初次独立钱账审计在报告渲染前完成，最终报告补入描述性表格后再次审计并以最终SHA独立finish；不改任何已finish历史报告字节。全部actual命令回执、数据哈希、完整trade/funding/state归档与复现代码保留。',
 '原冻结SMA从10:30续至12:30，仅新增120个闭合分钟，原30892点完整前缀保持，各场景31012点，累计30989分钟（21日＋749分钟）；无新增日决策/参考点/成交/费用，原现金/数量/desired/成本账本不变。下个日事件Oct24 00:01UTC，原2027-03-31终点保持。paper10冻结状态只读，旧延迟shadow不是十策略真实报价模拟。', '',
 f"复核：`PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/{R.name}/audit.py`；原SMA重放同解释器`research/experiments/{R.name}/forward.py --reproduce`。正式账本不重复reserve已完成ID；从零计算只在独立审计副本、原数据路径和单独登记下按freeze→benchmark_prepare→evaluate→summarize→audit→finish顺序执行。", '',
 '保留全部60场景正负结果、完整有符号成交/实际资金费/账户状态/逐折和日NAV、原SMA累计报告/源状态及2份原始HTTP响应。8份真实行情/资金费/元数据留忽略data，Git只留必要证据；无磁盘NPY/checkpoint，finished报告原字节和登记SHA优先。', '',
 '未验证：独立最终测试、全年365日、DSR/PBO、完整历史阶梯/逐tickmark强平、真实L2/成交/TCA；20个定义只复用一段330日市场。',''];(R/'result.md').write_text('\n'.join(lines));print(json.dumps({'financial_configs':20,'candidates':18,'benchmarks':2,'cost_scenes':len(rows),'fold_rows':len(folds),'daily_NAV_rows':len(daily),'passed_candidates':len(s['passed']),'rejected_candidates':len(s['rejected']),'failure_counts':report['failure_counts']}),flush=True)

if __name__=='__main__':main()
