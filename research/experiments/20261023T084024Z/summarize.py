"""Freeze all outcomes and read-only references before individual finish calls."""
import csv,gzip,io,json,statistics
from collections import Counter,defaultdict
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,LOOKS,GAPS,SKIPS,sha,put

def csvwrite(path,rows,compressed=False):
 fields=list(dict.fromkeys(k for x in rows for k in x));buffer=io.StringIO(newline='');writer=csv.DictWriter(buffer,fieldnames=fields,lineterminator='\n');writer.writeheader();writer.writerows(rows);raw=buffer.getvalue().encode();path.write_bytes(gzip.compress(raw,mtime=0) if compressed else raw)

def main():
 report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());ctx=json.loads((R/'context.json').read_text());cfgs=report['configs'];by={(x['skip_recent_days'],x['formation_days'],x['switching_return_gap']):x for x in cfgs.values()};rows=[];folds=[];daily=[];costs=[];edges=[];pairs=[];paths=defaultdict(list)
 for c in cfgs.values():
  paths[tuple(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3'])].append(c['name'])
  for k,z in c['scenes'].items():
   meta={'configuration':c['name'],'skip_recent_days':c['skip_recent_days'],'formation_days':c['formation_days'],'switching_return_gap':c['switching_return_gap'],'cost_multiplier':k};rows.append({**meta,**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','cost_pct_initial','gross_reference_PnL_to_execution_cost','executions','round_trips']},'positive_folds':sum(f['net_return_pct']>0 for f in z['folds']),'local3_positive_fraction':c['sensitivity']['local_3x_neighbor_positive_fraction'],'status':c['status']});folds.extend({**meta,**f} for f in z['folds']);daily.extend({**meta,'boundary_index':i,'NAV_usdt':v} for i,v in enumerate(z['daily_equity_usdt']));costs.append({**meta,'total_cost_usdt':z['cost_usdt'],**z['cost_parts_usdt']})
 for skip in SKIPS:
  es=[]
  for i,L in enumerate(LOOKS):
   for j,G in enumerate(GAPS):
    a=by[skip,L,G]
    for ni,nj,axis in [(i+1,j,'formation_days'),(i,j+1,'switching_return_gap')]:
     if ni<3 and nj<3:
      b=by[skip,LOOKS[ni],GAPS[nj]];es.append({'skip_recent_days':skip,'from':a['name'],'to':b['name'],'axis':axis,'absolute_3x_Sharpe_difference':abs(a['scenes']['3']['sharpe_365']-b['scenes']['3']['sharpe_365'])})
  threshold=2*statistics.stdev(e['absolute_3x_Sharpe_difference'] for e in es)
  for e in es:e.update(threshold=threshold,descriptive_cliff_flag=e['absolute_3x_Sharpe_difference']>threshold)
  edges+=es
 for L in LOOKS:
  for G in GAPS:
   a,b=by[0,L,G],by[7,L,G];pairs.append({'formation_days':L,'switching_return_gap':G,'unskipped':a['name'],'skip7':b['name'],'differences_skip_minus_unskipped':{k:{'net_return_pct':b['scenes'][k]['net_return_pct']-a['scenes'][k]['net_return_pct'],'minute_DD_pct':b['scenes'][k]['max_drawdown_pct']-a['scenes'][k]['max_drawdown_pct'],'cost_usdt':b['scenes'][k]['cost_usdt']-a['scenes'][k]['cost_usdt'],'round_trips':b['scenes'][k]['round_trips']-a['scenes'][k]['round_trips']} for k in ['1','2','3']}})
 report['sensitivity_cliffs']={'heuristic':'Adjacent3x dailySharpe difference>2sampleSD within skip direction,descriptive only.','edges':edges};report['skip_pair_comparisons']=pairs;report['within_batch_path_equivalence']={'unique_full_three_cost_NAV_paths':len(paths),'parameter_definitions':18,'groups':[{'names':names,'NAV_sha256_by_cost':dict(zip(['1','2','3'],key))} for key,names in paths.items()],'scope':'Different parameter rules remain separately registered even when realized paths coincide. These are correlated paths on one reused market history,not18independent samples. New fixed1443event axis prevents direct SHA comparisons with old1441/variableevent conventions.'};report['failure_counts']=dict(Counter(k for c in cfgs.values() for k,v in c['criteria'].items() if not v));report['research_context']={'prior_full_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_canonical_research_definitions':ctx['canonical_research_definitions_excluding_observations'],'prior_conclusions_read':len(ctx['prior_conclusions_read']),'initial16_missing_actual_results':0,'independent_final_holdout':False,'DSR_PBO_computed':False}
 oldpath=ROOT/'research/experiments/20261013T123949Z/report.json';old=json.loads(oldpath.read_text());report['read_only_holds']={name:{'name':name,'fingerprint':c['fingerprint'],'source_report':str(oldpath.relative_to(ROOT)),'source_report_sha256':sha(oldpath),'scenes':c['scenarios'],'role':c['role'],'scope':'Original2000USDT360dayhold reference,originalOct13filterandmetricconventions retained. Single-coin capital matches full account;50/50allocation differs. No rerun or precise matched-TCA alpha claim.'} for name,c in old['configs'].items() if name.startswith('hold_360d_')};report['artifacts']={'full_results':'results/*.json.gz','all_cost_scenes':'sensitivity.csv','fold_results':'fold_results.csv','daily_NAV':'daily_equity.csv.gz','cost_parts':'cost_scenarios.csv','surface':'sensitivity_surface.png','independent_verification':'verification.json'};put(R/'report.json',report)
 csvwrite(R/'sensitivity.csv',rows);csvwrite(R/'fold_results.csv',folds);csvwrite(R/'daily_equity.csv.gz',daily,True);csvwrite(R/'cost_scenarios.csv',costs)
 fig,axes=plt.subplots(1,3,figsize=(15,4.5),constrained_layout=True);limit=max(abs(c['scenes']['3']['net_return_pct']) for c in cfgs.values())
 for S,ax in zip(SKIPS,axes):
  values=np.asarray([[by[S,L,G]['scenes']['3']['net_return_pct'] for G in GAPS] for L in LOOKS]);im=ax.imshow(values,cmap='RdYlGn',vmin=-limit,vmax=limit);ax.set(xticks=range(3),xticklabels=['0%','2%','4%'],yticks=range(3),yticklabels=LOOKS,xlabel='Switching return gap',ylabel='Formation days',title=f'Monday rotation: skip {S} days')
  for i in range(3):
   for j in range(3):ax.text(j,i,f'{values[i,j]:+.2f}%',ha='center',va='center')
 fig.colorbar(im,ax=list(axes[:2]),label='3x net return %',shrink=.8)
 for S in SKIPS:
  values=by[S,42,.02]['scenes']['3']['daily_equity_usdt'];axes[2].plot(np.arange(len(values)),np.asarray(values)/20,label=f'Preset L42/G2%,skip{S}')
 axes[2].axhline(100,color='grey',linestyle=':',label='Cash,zero yield');axes[2].set(xlabel='Continuous OOS daily boundary',ylabel='NAV / initial capital %',title='3x costs; shared 2000 USDT');axes[2].legend(fontsize=8);fig.savefig(R/'sensitivity_surface.png',dpi=140);plt.close(fig)
 summary=report['summary'];center=by[0,42,.02];skipcenter=by[7,42,.02];z=center['scenes']['3'];lines=['# BTC/ETH周一相对动量轮动：跳过近周与换币门槛','',f"轮次`{R.name}`，计划SHA256`{report['frozen_plan_sha256']}`。18候选分别reserve后实际计算54个成本场景；原SMA3个观察截止另行登记。候选通过{len(summary['passed'])}、淘汰{len(summary['rejected'])}，1/2/3倍成本净正数量{summary['positive_configs_by_cost']['1']}/{summary['positive_configs_by_cost']['2']}/{summary['positive_configs_by_cost']['3']}。所有正负结果完整保留。",'',
 '## 经济假设与完整冻结规则','',
 '先前连续360日的SMA/通道EMA全亏损，旧日线轮动也因成本、折数或回撤淘汰。本轮检验周频执行和换币滞回能否减少昂贵换手；跳过最近7日则检验短期波动是否污染排序。不是围绕上一轮SMA格点继续择优。',
 '仅UTC周一决策，以此前完整日j=i−1的收盘计算。L∈{21,42,84}日；当前绝对动量A=C[j]/C[j−L]−1严格大于0才有持仓资格。排序动量R=C[j−S]/C[j−S−L]−1，S∈{0,7}。无持仓或原资产资格失效时选择符合资格且R最高者，无合格资产则现金；精确平手BTC优先。原持仓仍合格时，只有另一合格资产R严格超过原资产R至少G（G∈{0,2%,4%}且严格>）才换币；恰等门槛保留原仓。S只影响排序，绝对现金过滤始终使用当前收盘。非周一完全保持实际仓位，周内风险不隐含提前止损。',
 '每配置共享2000USDT现货账户，最多持BTC或ETH一种，目标原值敞口1，另一币0。不是75/25袖套，不归一化、借币、杠杆、并持、转账或产生现金利息。换币按同一下一日00:01原生Decimal OPEN先卖旧币再买新币，两个真实腿分别收费，卖出失败禁止买入，lot余钱留共享现金；相同目标不重买。OOS周五现金起步，首个周一之前不抢先入场。共享现金和顺序状态无法由旧独立组件NAV相加代表，因此本轮实际重算18个新配置。',
 '主来源：[AQR作者2009原文](https://www.aqr.com/-/media/AQR/Documents/Insights/White-Papers/The-Case-for-Momentum-Investing.pdf)讨论股票动量排除最近一月与换手，不直接证明加密7日跳过；[Liu/Tsyvinski/Wu的NBER官方摘要](https://www.nber.org/papers/w25882)仅作加密动量动机，直接网页403、没有读取全文；[Binance官方过滤器](https://developers.binance.com/en/docs/products/spot/filters)用于定义参考。均2026-10-23查询，不把论文动量或换手结论当本轮盈利证据。','',
 '## 三项实际验证','',
 '- Walk-forward：真实4份Binance闭合分钟Parquet，输入2024-09-16至2026-09-16，730完整UTC日。OOS2025-09-19 00:01至2026-09-14 00:01，共360日/12个连续30日折；365日初始上下文＋3日初始间隔，固定规则无拟合或未来标签，purge不适用。账户现金/持币/数量全程跨折连续，信号可得后至少60秒成交参考。历史已多次研究，不是未触碰最终测试。',
 '- 敏感性：预设两种S各有完整L×G3×3，局部相邻索引矩形含自身；54场景648逐折收益/DD/Sharpe/Calmar全部报告。24条相邻Sharpe差描述陡变，9组同L/G的S配对保留收益、DD、费用和往返差。没有看到结果后扩网格或重新命名参数。',
 '- 成本：每侧手续费10bp、半价差1bp、滑点2bp，加0.5×前20完整日样本波动×sqrt(预算/quote ADV)冲击，参与率≤0.1%；原Oct1过滤快照、原Decimal28 tick/lot/notional与过去闭合5分钟VWAP接受代理。1/2/3倍同时放大全部执行成本，每倍独立现金和持币路径，终点计费卖出。现货无做空/资金费/借币；缺历史L2/队列/延迟与真实IOC/TCA证明。',
 '门槛：各成本净正、1倍至少8/12正折、3倍整体DD≤25%、邻域3倍正比例≥60%、1倍至少4往返、毛参考PnL/成本≥2.5、无负余额和拒单、终点空仓。', '',
 '## 实际结果','', '|跳过日|L|换币门槛|1倍收益|2倍收益|3倍收益|1倍正折|3倍整体DD|往返|邻域3倍正比例|状态|','|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
 for c in cfgs.values():
  a,b,z0=[c['scenes'][k] for k in ['1','2','3']];lines.append(f"|{c['skip_recent_days']}|{c['formation_days']}|{c['switching_return_gap']:.0%}|{a['net_return_pct']:+.3f}%|{b['net_return_pct']:+.3f}%|{z0['net_return_pct']:+.3f}%|{c['positive_folds_1x']}/12|{z0['max_drawdown_pct']:.3f}%|{a['round_trips']}|{c['sensitivity']['local_3x_neighbor_positive_fraction']:.1%}|{c['status']}|")
 lines += ['',f"预设S0/L42/G2%中心1/2/3倍收益为{center['scenes']['1']['net_return_pct']:+.6f}%/{center['scenes']['2']['net_return_pct']:+.6f}%/{z['net_return_pct']:+.6f}%。其3倍整体DD{z['max_drawdown_pct']:.6f}%，1倍仅{center['positive_folds_1x']}/12盈利折，邻域3倍正比例{center['sensitivity']['local_3x_neighbor_positive_fraction']:.2%}，仍未通过。S0/L42/G0与此中心为完全相同三成本NAV，不能算两个独立成功样本。S7/L42/G2%中心3倍{skipcenter['scenes']['3']['net_return_pct']:+.6f}%，跳过近周没有解决本批稳健性。",'',
 '候选失败计数：`'+json.dumps(report['failure_counts'])+'`。所有18候选均未达8正折及≤25%整体DD和邻域门槛；多数在1倍已亏损。保留两个全成本正收益设置，但不称合格方法，更不能称实盘稳定盈利。', '',
 f"18个合法不同规则定义实现{len(paths)}条不同三成本完整NAV路径，等价路径组完整保存在report.within_batch_path_equivalence；所有定义都逐项登记，不把参数数量当独立市场样本。新轴每天保留成交前OPEN、卖后OPEN、买后OPEN三标记与1440闭合分钟，终点再保留平仓前OPEN/平仓后现金。每条519483点，总体回撤包含隔夜gap及两腿中间峰值；不含分钟内高低极值。原历史轴不改。", '',
 '## 同期只读参考','', '|原始2000USDT持有参考|1倍|2倍|3倍|','|---|---:|---:|---:|']
 for name,c in report['read_only_holds'].items():lines.append('|'+name+'|'+'|'.join(f"{c['scenes'][k]['net_return_pct']:+.3f}%" for k in ['1','2','3'])+'|')
 lines += ['', '旧Oct13同窗/同总资本持有参考保留原始过滤器和指标口径；单币2000与本轮全账户资本匹配，50/50参考分配不同，不据此宣称严格匹配的风险/成本alpha。参考结果不重新计算、reserve或finish。现金0利息为解析0基准。', '',
 '## 登记、复核、失败与下轮状态','',f"完整读取{ctx['registry_events']}事件/{ctx['registry_ids']}ID、{ctx['canonical_research_definitions_excluding_observations']}规范研究定义及{len(ctx['prior_conclusions_read'])}份既往结论；初始16项实际证据已逐项核验，无待补历史配置。当前18项周一/跳周/换币规则此前未登记，正式计算前全部reserve成功，54场景均有实际结果。",'',
 '独立审核使用缩放整数交叉乘法复核每个周一排名和严格阈值（生产用Fraction），从实际卖买账本重建完整状态及所有519483点NAV，再独立核对702整体/逐折指标；校验每笔价格tick、lot、notional、过去20日成本输入、5分钟代理、费用与现金守恒，换币不得沿用旧币数量。保存全部实际决策、成交、持仓片段、日NAV及完整向量哈希，验证见verification.json。',
 '预登记前第一轮合成测试实际exit1：原样例ETH历史150/100本来强于BTC130/100，预期误写为跳过后BTC；只改合成中间ETH150为120后，严格排名/门槛/现金过滤/未来前缀测试实际exit0。生产规则与真实参数未改，没有金融配置在该错误前reserve或计算；原日志、命令、样例数据和SHA均保留signal_fixture_failure.json。另保存NBER直接访问403事实，不用外层cat或管道exit0冒充检查通过。',
 '原冻结SMA从06:30续到08:30，只追加120闭合分钟，旧30652点前缀完全延续，各场景完整30772点、累计30749分钟（21日＋509分钟）。无新日决策、参考点、成交或费用；原现金/数量/desired/成本保留，下一日事件Oct24 00:01UTC，原2027-03-31终点不变。paper10计划/状态只读，旧shadow不是十策略真实报价模拟。', '',
 f"复核：`PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/{R.name}/audit.py`；原SMA重放同解释器`research/experiments/{R.name}/forward.py --reproduce`。正式登记不重复reserve已完成ID；从零研究计算只可在保留源数据和独立登记的审计副本执行freeze→evaluate→summarize→audit→finish。", '',
 '保留完整正负结果及原SMA源状态连续性、完整累计账本/NAV和两份原始API响应；原始大行情在忽略data、固定路径/SHA/字节数见data_manifest.json。不提交NPY/checkpoint；已finish报告原字节优先，不为压缩迁移格式或删损结果。下轮不按事后最高点扩大同一OOS网格；优先经济机制不同或真正新数据，原SMA仅按冻结规则续接。', '',
 '未验证：独立最终测试、完整365日、DSR/PBO、历史L2与实盘成交/TCA；18参数高度相关且只反复使用同一360日历史。',''];(R/'result.md').write_text('\n'.join(lines));print(json.dumps({'configs':18,'cost_scenes':len(rows),'fold_rows':len(folds),'daily_NAV_rows':len(daily),'unique_full_three_cost_paths':len(paths),'passed':len(summary['passed']),'rejected':len(summary['rejected']),'failure_counts':report['failure_counts']}),flush=True)

if __name__=='__main__':main()
