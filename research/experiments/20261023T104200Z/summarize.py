"""Complete pre-finish outcome archive, sensitivity surface and Chinese evidence."""
import csv,gzip,io,json,statistics
from collections import Counter,defaultdict
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,DROPS,HOLDS,sha,put,readgz

def csvwrite(path,rows,compressed=False):
 fields=list(dict.fromkeys(k for x in rows for k in x));buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);raw=buf.getvalue().encode();path.write_bytes(gzip.compress(raw,mtime=0) if compressed else raw)

def main():
 report=json.loads((R/'report.json').read_text());ctx=json.loads((R/'context.json').read_text());plan=json.loads((R/'plan.json').read_text());cfgs=report['configs'];by={(x['asset'],x['entry_three_day_loss'],x['maximum_holding_days']):x for x in cfgs.values()};rows=[];folds=[];daily=[];costs=[];exits=[];edges=[];paths=defaultdict(list)
 for c in cfgs.values():
  paths[tuple(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3'])].append(c['name']);arc=readgz(ROOT/c['archive']);c['holding_outcomes']={}
  for k,z in c['scenes'].items():
   a=arc['scenes'][k];dec=a['decisions'];stats={'half_recovery_exits':sum(x['action']=='exit' and bool(x['half_recovery_hit']) for x in dec),'timeout_exits':sum(x['action']=='exit' and bool(x['timeout_hit']) for x in dec),'both_reasons_exits':sum(x['action']=='exit' and bool(x['half_recovery_hit']) and bool(x['timeout_hit']) for x in dec),'terminal_exits':sum(t['terminal'] and t['status']=='filled' for t in a['trades']),'days_held':sum(s['end_day_exclusive']-s['day_offset'] for s in a['position_segments'] if s['position'] is not None)};c['holding_outcomes'][k]=stats;meta={'configuration':c['name'],'asset':c['asset'],'entry_three_day_loss':c['entry_three_day_loss'],'maximum_holding_days':c['maximum_holding_days'],'cost_multiplier':k};rows.append({**meta,**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','cost_pct_initial','gross_reference_PnL_to_execution_cost','executions','round_trips']},'positive_folds':sum(f['net_return_pct']>0 for f in z['folds']),'local3_positive_fraction':c['sensitivity']['local_3x_neighbor_positive_fraction'],'status':c['status']});folds.extend({**meta,**f} for f in z['folds']);daily.extend({**meta,'boundary_index':i,'NAV_usdt':v} for i,v in enumerate(z['daily_equity_usdt']));costs.append({**meta,'total_cost_usdt':z['cost_usdt'],**z['cost_parts_usdt']});exits.append({**meta,**stats})
 for asset in ['BTC','ETH']:
  es=[]
  for i,drop in enumerate(DROPS):
   for j,hold in enumerate(HOLDS):
    a=by[asset,drop,hold]
    for ni,nj,axis in [(i+1,j,'entry_three_day_loss'),(i,j+1,'maximum_holding_days')]:
     if ni<3 and nj<3:
      b=by[asset,DROPS[ni],HOLDS[nj]];es.append({'asset':asset,'from':a['name'],'to':b['name'],'axis':axis,'absolute_3x_Sharpe_difference':abs(a['scenes']['3']['sharpe_365']-b['scenes']['3']['sharpe_365'])})
  threshold=2*statistics.stdev(e['absolute_3x_Sharpe_difference'] for e in es)
  for e in es:e.update(threshold=threshold,descriptive_cliff_flag=e['absolute_3x_Sharpe_difference']>threshold)
  edges+=es
 report['sensitivity_cliffs']={'heuristic':'Adjacent3x dailySharpe difference>2sampleSD within asset;descriptive only.','edges':edges};report['within_batch_path_equivalence']={'unique_full_three_cost_NAV_paths':len(paths),'parameter_definitions':18,'groups':[{'names':names,'NAV_sha256_by_cost':dict(zip(['1','2','3'],key))} for key,names in paths.items()],'scope':'Different rules remain separately registered;one reused market history is not18independent samples. New1442eventaxis is not directly SHA-comparable to older axes.'};report['failure_counts']=dict(Counter(k for c in cfgs.values() for k,v in c['criteria'].items() if not v));report['research_context']={'prior_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_canonical_research_definitions':ctx['canonical_research_definitions_excluding_observations'],'prior_conclusions_read':len(ctx['prior_conclusions_read']),'initial16_missing_actual_results':0,'independent_final_holdout':False,'DSR_PBO_computed':False};oldpath=ROOT/plan['read_only_context']['hold_reference_report']['path'];assert sha(oldpath)==plan['read_only_context']['hold_reference_report']['sha256'];old=json.loads(oldpath.read_text());report['read_only_holds']={name:{'name':name,'fingerprint':c['fingerprint'],'source_report':str(oldpath.relative_to(ROOT)),'source_report_sha256':sha(oldpath),'scenes':c['scenarios'],'role':c['role'],'scope':'Original2000USDT360dayhold reference,originalOct13filterandmetricconventions retained. Single-coin capital matches full account;50/50allocation differs. No rerun or strict matched-TCA alpha claim.'} for name,c in old['configs'].items() if name.startswith('hold_360d_')};report['artifacts']={'full_results':'results/*.json.gz','all_cost_scenes':'sensitivity.csv','fold_results':'fold_results.csv','daily_NAV':'daily_equity.csv.gz','cost_parts':'cost_scenarios.csv','holding_outcomes':'holding_outcomes.csv','surface':'sensitivity_surface.png','independent_verification':'verification.json'};put(R/'report.json',report)
 csvwrite(R/'sensitivity.csv',rows);csvwrite(R/'fold_results.csv',folds);csvwrite(R/'daily_equity.csv.gz',daily,True);csvwrite(R/'cost_scenarios.csv',costs);csvwrite(R/'holding_outcomes.csv',exits)
 fig,axes=plt.subplots(1,3,figsize=(15,4.5),constrained_layout=True);limit=max(abs(c['scenes']['3']['net_return_pct']) for c in cfgs.values())
 for asset,ax in zip(['BTC','ETH'],axes):
  values=np.asarray([[by[asset,d,h]['scenes']['3']['net_return_pct'] for h in HOLDS] for d in DROPS]);im=ax.imshow(values,cmap='RdYlGn',vmin=-limit,vmax=limit);ax.set(xticks=range(3),xticklabels=HOLDS,yticks=range(3),yticklabels=['3%','6%','9%'],xlabel='Maximum holding days',ylabel='Strict3day entry loss',title=asset+' shock rebound:3x costs')
  for i in range(3):
   for j in range(3):ax.text(j,i,f'{values[i,j]:+.2f}%',ha='center',va='center')
 fig.colorbar(im,ax=list(axes[:2]),label='3x net return %',shrink=.8)
 for asset in ['BTC','ETH']:
  values=by[asset,.06,4]['scenes']['3']['daily_equity_usdt'];axes[2].plot(np.arange(len(values)),np.asarray(values)/20,label=asset+' presetD6%/H4')
 axes[2].axhline(100,color='grey',linestyle=':',label='Cash,zero yield');axes[2].set(xlabel='Continuous OOS daily boundary',ylabel='NAV / initial capital %',title='Preset centers:3x costs');axes[2].legend(fontsize=8);fig.savefig(R/'sensitivity_surface.png',dpi=140);plt.close(fig)
 s=report['summary'];best=cfgs[max(cfgs,key=lambda n:cfgs[n]['scenes']['3']['net_return_pct'])];z=best['scenes']['3'];lines=['# BTC/ETH三日急跌反弹：固定半收复目标与持有上限','',f"轮次`{R.name}`，冻结计划SHA256`{report['frozen_plan_sha256']}`。18个候选各自reserve后实际计算54成本场景，另3个原SMA观察截止独立登记。候选通过{len(s['passed'])}、淘汰{len(s['rejected'])}，1/2/3倍成本净正数量{s['positive_configs_by_cost']['1']}/{s['positive_configs_by_cost']['2']}/{s['positive_configs_by_cost']['3']}。完整正负收益与原因全部保存。",'',
 '## 假设、精确规则与资金','',
 '检验三日累计大跌后是否有足以覆盖费用的短期反弹；与上一轮周一动量轮动相比，本轮是单币事件型逆势交易。不是用旧高收益参数改名。已有15分钟/4小时反弹、RSI2及IBS结果只读，不因相同“反转”词排除新周期/完整规则，也不把旧失败当本次实测。',
 '每UTC日i只读已闭合j=i−1收盘：r3=C[j]/C[j−3]−1。空仓且r3严格小于−D才尝试次日00:01OPEN买入；D∈{3%,6%,9%}，等于边界不入场，不要求首次穿越。每次真实买入成功于索引e时，冻结A=C[e−4]及B=C[e−1]。持仓仅当已闭合收盘满足2×C[j]≥A+B（算术跌幅半收复，等于即触发），或i−e≥H时退出；H∈{2,4,8}完整日成交间隔。退出在信号可得后的00:01真实OPEN，不假定触碰目标价成交。目标和时钟不随新跌幅或折边界移动。',
 '持仓日先判断退出，退出后不能同一决策重买，下一日才重新评估；无止损、摊低、加仓或OOS前仓位。新入场即使靠近已知终点也照常执行，终点计费平仓，截短持有如实留档。每配置独立2000USDT、单币现货最大原值敞口1，lot剩余留现金；无归一化、借币、空头、杠杆、现金利息、账户转账或组合指标平均。原冻结SMA1500/500及paper10账户不变。',
 '参考[DeNicola2021作者期刊摘要](https://doi.org/10.5195/ledger.2021.213)：原研究是BTC1/2/4小时自相关，不能直接证明三日规则。[Zaremba等2021出版方摘要](https://www.sciencedirect.com/science/article/pii/S1057521921002349)提示高流动性大币可能是动量而非反转，是相反先验；直接页403、仅使用可读索引摘要，不声称读取全文。[Binance官方过滤器](https://developers.binance.com/en/docs/products/spot/filters)仅作定义参考。访问2026-10-23，不复刻论文或将其称盈利背书。','',
 '## 三项验证','',
 '- Walk-forward：四份真实Binance现货分钟Parquet，输入2024-09-16至2026-09-16，每币730完整日；OOS2025-09-19 00:01至2026-09-14 00:01UTC，360日/12连续30日折，365日上下文＋3日初始间隔。固定因果规则，无模型拟合/未来标签，purge不适用；现金、数量及冻结入场状态跨折持续，信号至少延迟60秒执行参考。历史已反复使用，不能称未触碰最终测试。',
 '- 敏感性：两币各完整D×H3×3；邻域是同币相邻索引矩形含自身。54成本场景的648逐折收益、整体/逐折DD、日Sharpe及Calmar全部留档；24相邻Sharpe差描述断崖，不作显著性。未按最好收益扩展边界或更改门槛。',
 '- 成本：每侧10bp手续费、1bp半价差、2bp滑点，加0.5×过去20完整日样本波动×sqrt(订单预算/quote ADV)冲击；参与率≤0.1%，原Decimal28 tick/lot/notional与过去5闭合分钟VWAP代理过滤。1/2/3倍放大全部执行成本，各倍独立实际数量/现金路径，终点平仓计费。现货不涉及永续资金费/借币。Oct1过滤器和真实IOC接受仍为代理，缺历史L2/队列/延迟/TCA证明。触发跌幅不是预期alpha，不把3%跌幅除以费用冒充安全边际。',
 '预设门槛：各成本净正；1倍≥8/12正折；3倍整体DD≤25%；邻域3倍正比例≥60%；1倍≥4往返；毛参考PnL/成本≥2.5；无负余额/拒单；终点空仓。','',
 '## 全部实际结果','', '|币|跌幅D|最长H|1倍收益|2倍收益|3倍收益|1倍正折|3倍整体DD|往返|邻域3倍正比例|状态|','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
 for c in cfgs.values():
  a,b,z0=[c['scenes'][k] for k in ['1','2','3']];lines.append(f"|{c['asset']}|{c['entry_three_day_loss']:.0%}|{c['maximum_holding_days']}|{a['net_return_pct']:+.3f}%|{b['net_return_pct']:+.3f}%|{z0['net_return_pct']:+.3f}%|{c['positive_folds_1x']}/12|{z0['max_drawdown_pct']:.3f}%|{a['round_trips']}|{c['sensitivity']['local_3x_neighbor_positive_fraction']:.1%}|{c['status']}|")
 lines += ['',f"事后最高3倍设置{best['name']}收益{z['net_return_pct']:+.6f}%，整体DD{z['max_drawdown_pct']:.6f}%，1倍仅{best['positive_folds_1x']}/12正折、{best['scenes']['1']['round_trips']}往返，邻域正比例{best['sensitivity']['local_3x_neighbor_positive_fraction']:.2%}。其高跌幅/短持有位于网格边缘，稀疏交易和孤立正值不能构成稳健平台；不将其替代预设D6%/H4中心，不扩大同一OOS网格追逐峰值。",'',
 '预设中心：'+ '；'.join(a+' D6%/H4 的1/2/3倍为'+ '/'.join(f"{by[a,.06,4]['scenes'][k]['net_return_pct']:+.6f}%" for k in ['1','2','3']) for a in ['BTC','ETH'])+'。', '',
 '门槛失败计数：`'+json.dumps(report['failure_counts'])+'`。收益折数高也不能单独证明盈利：ETH3%/H2有8正折却整体大幅亏损，全部幅度和回撤仍须同时核验。所有18候选未能通过完整预设门槛；保留少数正收益，不称经稳健性验证的方法或稳定实盘盈利。', '',
 f"18个参数定义对应{len(paths)}种三成本完整NAV路径；同市场样本高度相关，不当作18个独立试验。每条519123点包含起始本金、每天成交前/后原生DecimalOPEN与1440闭合分钟、终点平仓前OPEN和成本后现金，完整回撤包括跳空及费用，不含分钟内极值。旧轴与旧历史指标原样保留。退出原因/持币日数见holding_outcomes.csv，target/timeout可同日重叠，终点退出单列。", '',
 '## 只读同期参考','', '|旧2000USDT持有参考|1倍|2倍|3倍|','|---|---:|---:|---:|']
 for n,c in report['read_only_holds'].items():lines.append('|'+n+'|'+'|'.join(f"{c['scenes'][k]['net_return_pct']:+.3f}%" for k in ['1','2','3'])+'|')
 lines += ['', '旧Oct13单币持有资本/时间匹配，仍保留原过滤器和指标口径；50/50参考分配不同。只读原结果，不重新计算/登记/finish，不声称严格匹配的风险/成本alpha。现金0利息为解析基准。','',
 '## 完整登记、审计及下轮输入','',f"运行前完整读取{ctx['registry_events']}事件/{ctx['registry_ids']}ID、{ctx['canonical_research_definitions_excluding_observations']}规范研究定义及{len(ctx['prior_conclusions_read'])}份既往结论，初始16项实际证据全有，无待补配置。18个新日线shock/目标/时钟具体定义均先reserve，54成本场景真实执行。",'',
 '独立审计以18位缩放整数交叉乘法复核入场边界、固定A/B半收复与实际成交年龄，逐笔验证tick/lot/notional、过去20日成本和5分钟代理、五项费用及现金数量守恒；从实际账本重建全部54条NAV和702组整体/逐折指标，明确禁止同日退出重入。完整原始决策/成交/持仓段、日NAV与全NAV哈希保留。不是用工程通过替代回测，审计实测结果见verification.json。',
 '本轮出版方直接网页403事实保留read_failures.json，作者期刊摘要和官方过滤器可读。所有实际命令returncode逐项留档，不把cat/管道外层exit0视为内层检查通过；不为监控重写历史收益。',
 '原冻结SMA从08:30继续至10:30，仅120个闭合分钟，旧30772点完整前缀保留，各场景30892点，累计30869分钟（21日＋629分钟）；无新日决策/参考点/成交/费用，原现金/数量/desired/历史账本完全延续。下一日事件Oct24 00:01UTC，原2027-03-31终点不变；旧延迟shadow不是十策略真实报价模拟，paper10计划/状态未动。', '',
 f"复核：`PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/{R.name}/audit.py`；原SMA重放同解释器`research/experiments/{R.name}/forward.py --reproduce`。不在正式登记重复reserve已完成ID；从零计算仅在保留源行情的独立审计副本执行freeze→evaluate→summarize→audit→finish。", '',
 '所有负收益与正收益、完整账户账本/状态/累计NAV、两份原始HTTP响应和下轮必需输入均保留，行情在忽略data、哈希和路径见data_manifest.json。无磁盘NPY/checkpoint；已finish报告原字节和登记SHA优先，不为压缩迁移格式或删损结果。下一轮不把这段旧历史称独立最终测试，优先不同机制或真正新增可验证数据。', '',
 '尚未验证：独立最终测试、完整365日、DSR/PBO、历史L2与实盘成交/TCA；原SMA仍仅21日部分观察。',''];(R/'result.md').write_text('\n'.join(lines));print(json.dumps({'configs':18,'cost_scenes':len(rows),'fold_rows':len(folds),'daily_NAV_rows':len(daily),'unique_full_three_cost_paths':len(paths),'passed':len(s['passed']),'rejected':len(s['rejected']),'failure_counts':report['failure_counts']}),flush=True)

if __name__=='__main__':main()
