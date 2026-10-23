"""Preserve complete annual outcomes, sensitivity, fold and same-funded references."""
import csv,gzip,io,json,statistics
from collections import Counter
from datetime import datetime,timezone,timedelta
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,CAPS,EMAS,sha,put

def csvwrite(path,rows,compressed=False):
 fields=list(dict.fromkeys(k for x in rows for k in x));b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);raw=b.getvalue().encode();path.write_bytes(gzip.compress(raw,mtime=0) if compressed else raw)

def main():
 report=json.loads((R/'report.json').read_text());ctx=json.loads((R/'context.json').read_text());plan=json.loads((R/'plan.json').read_text());rows=[];folds=[];daily=[];costs=[];edges=[];cfgs=report['configs'];by={(x['BTC_annual_volatility_ceiling'],x['ETH_EMA_span_days']):x for x in cfgs.values() if x['role']=='combination'}
 for c in cfgs.values():
  for k,z in c['scenes'].items():
   meta={'configuration':c['name'],'role':c['role'],'asset':c.get('asset'),'capital_usdt':c['capital_usdt'],'axis':c.get('axis'),'BTC_annual_volatility_ceiling':c.get('BTC_annual_volatility_ceiling'),'ETH_EMA_span_days':c.get('ETH_EMA_span_days'),'cost_multiplier':k}
   rows.append({**meta,**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','cost_pct_initial','gross_reference_PnL_to_execution_cost','executions','round_trips']},'positive_folds':sum(f['net_return_pct']>0 for f in z['folds']),'local3_positive_fraction':c['sensitivity'].get('local_3x_neighbor_positive_fraction'),'status':c['status']})
   folds.extend({**meta,**f} for f in z['folds']);daily.extend({**meta,'boundary_index':i,'NAV_usdt':v} for i,v in enumerate(z['daily_equity_usdt']));costs.append({**meta,'total_cost_usdt':z['cost_usdt'],**z['cost_parts_usdt']})
 for i,cap in enumerate(CAPS):
  for j,span in enumerate(EMAS):
   a=by[cap,span]
   for ni,nj,axis in [(i+1,j,'BTC_volatility_ceiling'),(i,j+1,'ETH_EMA_span')]:
    if ni<3 and nj<3:
     b=by[CAPS[ni],EMAS[nj]];edges.append({'from':a['name'],'to':b['name'],'axis':axis,'absolute_3x_Sharpe_difference':abs(a['scenes']['3']['sharpe_365']-b['scenes']['3']['sharpe_365'])})
 threshold=2*statistics.stdev(e['absolute_3x_Sharpe_difference'] for e in edges)
 for e in edges:e.update(threshold=threshold,descriptive_cliff_flag=e['absolute_3x_Sharpe_difference']>threshold)
 report['sensitivity_cliffs']={'heuristic':'Adjacent3x dailySharpe difference>2sampleSD;descriptive only,not significance or profitability.','edges':edges}
 report['failure_counts']=dict(Counter(k for c in cfgs.values() if not c['role'].startswith('benchmark') for k,v in c['criteria'].items() if not v))
 oldpath=ROOT/plan['prior_read_only']['report'];assert sha(oldpath)==plan['prior_read_only']['sha256'];old=json.loads(oldpath.read_text())
 report['prior_seasonal_context']={'report':str(oldpath.relative_to(ROOT)),'report_sha256':sha(oldpath),'scope':'Read-only old2025/2026March-September results,not financially stitched into continuous annual account. Different start/history;no matched path improvement claim.','preset_central_3x_return_pct':{y:old['configs'][f'guard_ema_combo_{y}_V0.5_E30']['scenes']['3']['net_return_pct'] for y in ['2025','2026']},'prior_both_seasonal_periods_passed_pairs':old['summary']['new_both_periods_passed_combination_pairs']}
 report['research_context']={'prior_canonical_definitions':ctx['canonical_research_definitions_excluding_observations'],'prior_full_registry_events_read':ctx['registry_events'],'prior_conclusions_read':len(ctx['prior_conclusions_read']),'initial_16_missing_actual_results':0,'independent_final_holdout':False,'DSR_PBO_computed':False,'all_18_configs_have_real_results':True}
 report['artifacts']={'full_results':'results/*.json.gz','all_scenes':'sensitivity.csv','fold_results':'fold_results.csv','daily_NAV':'daily_equity.csv.gz','cost_parts':'cost_scenarios.csv','surface':'sensitivity_surface.png','independent_verification':'verification.json'}
 put(R/'report.json',report);csvwrite(R/'sensitivity.csv',rows);csvwrite(R/'fold_results.csv',folds);csvwrite(R/'daily_equity.csv.gz',daily,True);csvwrite(R/'cost_scenarios.csv',costs)
 fig,axes=plt.subplots(1,2,figsize=(10,4),constrained_layout=True)
 vals=np.array([[by[c,e]['scenes']['3']['net_return_pct'] for e in EMAS] for c in CAPS]);limit=max(abs(vals.flatten()));im=axes[0].imshow(vals,cmap='RdYlGn',vmin=-limit,vmax=limit)
 axes[0].set(xticks=range(3),xticklabels=EMAS,yticks=range(3),yticklabels=CAPS,xlabel='ETH EMA span days',ylabel='BTC annual volatility ceiling',title='360 continuous days: 3x net return')
 for i in range(3):
  for j in range(3):axes[0].text(j,i,f'{vals[i,j]:+.2f}%',ha='center',va='center')
 fig.colorbar(im,ax=axes[0],label='Return %',shrink=.8)
 for n,label in [('annual_combo_V0.5_E30','Preset center'),('annual_hold_75_25','Same-funded buy-hold')]:
  z=cfgs[n]['scenes']['3']['daily_equity_usdt'];axes[1].plot(range(len(z)),np.asarray(z)/2000*100,label=label)
 axes[1].set(xlabel='Continuous OOS daily boundary (last=costed terminal)',ylabel='NAV / initial capital %',title='3x costs; raw BTC/ETH 75/25');axes[1].legend();fig.savefig(R/'sensitivity_surface.png',dpi=140);plt.close(fig)
 lines=['# 连续360日反证：BTC波动门槛SMA＋ETH通道EMA','',f"轮次`{R.name}`，计划SHA256`{report['frozen_plan_sha256']}`。18项真实金融配置（6个参数组件、9个新组合、3个同资金持有参考）及3个原SMA观察截止，均先成功reserve后计算，各自finish。15项研究候选在1/2/3倍成本下全部亏损，全部淘汰；3个买入持有参考单列、仅作参考。",'',
 '## 固定规则与时间','',
 '真实分钟行情输入2024-09-16至2026-09-16，两币各730个完整日，4份Parquet原字节哈希见plan.json；不提交原始大行情。OOS2025-09-19 00:01至2026-09-14 00:01UTC，共360日，12个连续30日折。365日上下文＋3日初始间隔，固定因果规则不拟合，purge不适用；OOS仅起点现金/desired-cash初始化一次，跨冬季及全部折保留现金、数量与desired，无每折重置、无春夏账户拼接。历史已反复用于研发，不能称未触碰最终测试。',
 'BTC固定SMA65、入场上方1.25%/退出下方0.5%；过去21个闭合收盘产生20个log收益，Decimal28样本年化波动，高于40%/50%/60%门槛置现金。ETH固定15日入场/30日退出通道（排除被比较的最后收盘）并联合EMA25/30/35日及对称1.25%缓冲；入场两条件同日成立，退出任一成立。EMA保留原Float adjust=False，从2024-09-16首日收盘递推，不在折间重新种子。',
 '原值BTC75%/ETH25%表示2000USDT中真实1500/500的独立资金袖套，同金额组件完整NAV逐点相加一次；不再乘权重、不归一化、不调仓、无转账、杠杆、借币、空头或现金利息。三个新持有参考恰以BTC1500、ETH500及合计2000计费成交，不能把2000金额旧组件等比缩放来代替。组合指标从总NAV求得，不平均组件Sharpe或DD。',
 '主来源：[Binance公开数据](https://github.com/binance/binance-public-data)、[官方过滤器](https://developers.binance.com/en/docs/products/spot/filters)、[EMA递推文档](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)，2026-10-23读取。文档不代表收益保证。','',
 '## 三项验证','',
 '- Walk-forward已实际完成12折，报告54成本场景的648个逐折指标及连续整体分钟回撤。每条完整NAV518762点，含起点、每日原生Decimal成交后OPEN、1440个闭合分钟标记与终点计费清仓；保存可无损重建的持仓片段、决策、成交及全NAV哈希，日NAV单独留档。回撤不含分钟内极值。',
 '- 敏感性已完成预设BTC门槛3档×ETH EMA3档、组件各轴邻域；组合含中心的相邻矩形、组件同币相邻轴。所有参数分别登记，无事后扩网格。各邻域3倍净正比例均0，说明此格内没有正收益平台；12条相邻Sharpe陡变启发仅描述，不作显著性或合格判断。',
 '- 1/2/3倍成本已各走真实独立现金/数量路径：每侧手续费10bp、半价差1bp、滑点2bp，加0.5×过去20完整日样本波动×sqrt(预算/quote ADV)冲击；参与率≤0.1%，Decimal价格tick/数量lot/notional、过去闭合5分钟VWAP过滤代理，终点平仓计费。现货无永续资金费或借币。Oct1过滤器、VWAP与IOC成交仍是代理，未做历史L2、排队、延迟与实盘TCA验证。',
 '预设失败门槛：各成本净正、1倍≥8/12正折、3倍整体DD≤25%、局部3倍正比例≥60%、1倍≥4往返、毛参考PnL/执行成本≥2.5、无负余额/拒单、终点空仓。毛成本加回不是独立零成本策略。','',
 '## 实际结果','',
 '|配置|1倍收益|2倍收益|3倍收益|1倍正折|3倍整体DD|1倍往返|状态|','|---|---:|---:|---:|---:|---:|---:|---|']
 for c in cfgs.values():
  a,b,z=[c['scenes'][k] for k in ['1','2','3']];lines.append(f"|{c['name']}|{a['net_return_pct']:+.3f}%|{b['net_return_pct']:+.3f}%|{z['net_return_pct']:+.3f}%|{c['positive_folds_1x']}/12|{z['max_drawdown_pct']:.3f}%|{a['round_trips']}|{'仅参考' if c['role'].startswith('benchmark') else c['status']}|")
 center=cfgs['annual_combo_V0.5_E30'];z=center['scenes']['3'];lines+=['',f"事前中心（波动上限50%、EMA30）1/2/3倍收益分别{center['scenes']['1']['net_return_pct']:+.6f}%/{center['scenes']['2']['net_return_pct']:+.6f}%/{z['net_return_pct']:+.6f}%，3倍整体DD{z['max_drawdown_pct']:.6f}%，1倍仅{center['positive_folds_1x']}/12正折。原春夏两段中心3倍为+42.538710%/+19.699928%，现覆盖其间冬季的连续账户亏损；时间起点/EMA上下文不同，不声称严格配对因果或将旧收益相乘。",'',
 '候选失败计数：`'+json.dumps(report['failure_counts'])+'`。虽然所有组合较同分配持有亏损更小，仍落后解析现金0收益，不能据此称盈利方法。收益较高的网格点仅事后描述，不替换预设中心或冻结SMA。', '',
 '## 完整登记、复核与续接','',f"计算前完整读取{ctx['registry_events']}事件/{ctx['registry_ids']}ID、{ctx['canonical_research_definitions_excluding_observations']}个规范研究定义及{len(ctx['prior_conclusions_read'])}份既往结论；初始16项均有实际证据。所有新18金融定义包含同一规则的新连续时间/真实资金配置，无等价名称重复。原历史报告与登记SHA保持。",'',
 '独立审计从实际成交重建24条叶成本NAV，逐点相加30条父成本NAV，复核全部54条完整哈希、702组整体/逐折指标、8640个因果决策；另用50位Decimal替代公式复核BTC波动/ETH EMA，独立验证真实填单价格、数量、5项费用和现金守恒。审计仅验证已完成配置，不增加或调参。实测结果见verification.json。',
 '只读初始化发生过两次诊断错误：猜测不存在文件的sed失败被后续cat的shell exit0掩盖，以及未使用登记探针values解包ValueError实际exit1；均先于reserve/计算，真实失败及修正保留read_failures.json。不能把cat的exit0称门禁通过。',
 '原冻结SMA从04:30续接到06:30，仅新增120个闭合分钟，每成本场景完整30652点、累计30629分钟（21完整日＋389分钟）；无新日决策/参考点/成交，现金/数量/desired/累计成本与原30532点前缀逐字/逐值保留。下一日事件2026-10-24 00:01UTC，终点2027-03-31不变。原shadow不是paper10真实报价模拟；paper10计划/状态只读。', '',
 f"复核命令：`PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/{R.name}/audit.py`。原SMA重放：同解释器`research/experiments/{R.name}/forward.py --reproduce`。从零复现须先在隔离审计副本保留源数据路径和登记，按run.py freeze→evaluate→summarize.py→audit.py→run.py finish顺序；正式仓库不重新reserve已完成ID。",'',
 '保留所有负收益、完整决策/成交/持仓片段、逐折与日NAV、原SMA完整报告/账户状态/输入和两份原始API响应；行情留忽略data并固定路径/SHA。无磁盘NPY/checkpoint，完成后只清理本轮可重建缓存。finished报告原字节优先，不为压缩重写。下一轮以连续区间亏损为结论，优先考虑经济机制不同的新方向，不继续围绕本轮亏损格点做测试集追涨。', '',
 '尚未验证：独立最终测试、365日完整年度、多重比较校正、实盘成交/TCA；原SMA仍只是未成熟延迟历史观察。','']
 (R/'result.md').write_text('\n'.join(lines));print(json.dumps({'financial_configs':18,'cost_scenes':len(rows),'fold_rows':len(folds),'daily_NAV_rows':len(daily),'passed':0,'rejected_candidates':15,'benchmarks':3,'failure_counts':report['failure_counts']}),flush=True)

if __name__=='__main__':main()
