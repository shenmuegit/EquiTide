"""Render the entire frozen carry grid, including negative outcomes and comparators."""
import json, math
from collections import Counter
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from run import csvput,put

R=Path(__file__).resolve().parent
def main():
    r=json.loads((R/'report.json').read_text());p=json.loads((R/'plan.json').read_text());ctx=json.loads((R/'context.json').read_text())
    candidates=[x for x in r['configs'].values() if x['role']=='candidate'];rows=[];folds=[];edges=[]
    for x in r['configs'].values():
        for m,z in x['scenarios'].items():
            rows.append({'name':x['name'],'role':x['role'],'asset':x['asset'],'holding_hours':x.get('holding_hours'),'per_leg_fraction':x.get('per_leg_fraction'),'cost_multiplier':m,
                'net_return_pct':z['net_return_pct'],'full_minute_traded_price_drawdown_pct':z['max_drawdown_pct'],'hourly_sampled_drawdown_pct':z['hourly_sampled_max_drawdown_pct'],
                'hourly_sharpe_annualized':z['sharpe_annualized'],'minute_sampled_calmar':z['calmar_1m_sampled'],'execution_cost_usdt':z['execution_cost_usdt'],
                'funding_paid_usdt':z['funding_paid_usdt'],'funding_income_usdt':z['funding_income_usdt'],'total_cost_pct_initial':z['cost_usdt']/100,
                'gross_reference_pnl_to_total_cost':z['gross_reference_pnl_to_cost'],'round_trips':z['round_trips'],'executions':z['executions'],'positive_folds':z['positive_folds'],
                'cash_order_rejections':z['rejected_orders'],'original_margin_violations':len(z['cash_margin_violations']),'independent_margin_violations':len(z['independent_cash_margin_violations']),
                'local_3x_positive_fraction':x['sensitivity'].get('local_3x_neighbor_positive_fraction'),'status':x['status']})
            for f in z['folds']:
                folds.append({'name':x['name'],'role':x['role'],'asset':x['asset'],'cost_multiplier':m,'fold':f['fold'],'start_utc':f['test_start_utc'],'end_exclusive_utc':f['test_end_utc'],
                    'start_nav':f['start_nav'],'end_nav':f['end_nav'],'net_return_pct':f['net_return_pct'],'hourly_sampled_drawdown_pct':f['max_drawdown_pct'],'hourly_sharpe_annualized':f['sharpe_annualized'],'hourly_sampled_calmar':f['calmar']})
    hs=p['grid']['holding_hours'];fs=p['grid']['per_leg_fraction'];by={(x['asset'],x['holding_hours'],x['per_leg_fraction']):x for x in candidates}
    for asset in ('BTC','ETH'):
        for i,h in enumerate(hs):
            for j,f in enumerate(fs):
                a=by[asset,h,f]
                for ii,jj,axis in [(i+1,j,'holding_hours'),(i,j+1,'per_leg_fraction')]:
                    if ii>=3 or jj>=3:continue
                    b=by[asset,hs[ii],fs[jj]];v=a['scenarios']['3']['sharpe_annualized'];w=b['scenarios']['3']['sharpe_annualized']
                    if v is not None and w is not None:edges.append({'from':a['name'],'to':b['name'],'axis':axis,'absolute_sharpe_difference':abs(v-w)})
    threshold=2*float(np.std([x['absolute_sharpe_difference'] for x in edges],ddof=1)) if len(edges)>1 else None
    r.update(failure_counts=dict(Counter(k for x in candidates for k,v in x['gates'].items() if not v)),sensitivity_cliffs={'threshold':threshold,'heuristic':'Adjacent3x hourly-Sharpe difference>2sampleSD;descriptive,not significance.',
        'edges':[{**x,'flagged':threshold is not None and x['absolute_sharpe_difference']>threshold} for x in edges]},
        research_context={'prior_canonical_research_definitions':ctx['canonical_research_definitions_excluding_observations'],'new_candidate_configs':18,'new_comparators':0,'prior_configs_reused_read_only':20,'independent_final_holdout':False,'DSR_PBO_computed':False})
    put(R/'report.json',r);csvput(R/'sensitivity.csv',rows);csvput(R/'fold_results.csv',folds)
    fig,axes=plt.subplots(1,2,figsize=(10,4),constrained_layout=True);limit=max(abs(x['scenarios']['3']['net_return_pct']) for x in candidates) or 1
    for asset,ax in zip(('BTC','ETH'),axes):
        values=np.array([[by[asset,h,f]['scenarios']['3']['net_return_pct'] for f in fs] for h in hs]);im=ax.imshow(values,cmap='RdYlGn',vmin=-limit,vmax=limit)
        ax.set(xticks=range(3),xticklabels=fs,yticks=range(3),yticklabels=hs,xlabel='Raw per-leg NAV fraction',ylabel='Holding hours',title=asset+': 3x cost net return')
        for i in range(3):
            for j in range(3):ax.text(j,i,f'{values[i,j]:+.2f}%',ha='center',va='center')
    fig.colorbar(im,ax=axes,label='Net return %',shrink=.8);fig.savefig(R/'sensitivity_surface.png',dpi=140);plt.close(fig)
    s=r['summary'];best=r['configs'][s['ranked_by_1x_net_return'][0]];a,b,c=[best['scenarios'][str(m)] for m in (1,2,3)]
    lines=['# BTC/ETH长持有上限B1资金费筛选：预登记历史回测','',
        f"轮次`{R.name}`；冻结UTC`{p['frozen_at_utc']}`，计划SHA256`{r['frozen_plan_sha256']}`。18项新候选先独立reserve，共54成本场景；既往18项B0及2项同窗现货基准只读复用，未重新计算、登记或finish。",'',
        '## 固定规则与资金含义','',
        '复用20261001T053425Z/carry.py原始B1核算，内核字节未改。每小时T只用已闭合报价与available_ts≤T的最近21次已公布实际资金费，各rate除以真实结算间隔小时后取中位数。空仓且完整H小时能在已知OOS终点前结束时，预计perp名义额×小时中位数×H减去基础1倍预计往返成本严格大于1USDT才尝试入场。持仓每小时按剩余期限预计资金费减去仅未来退出成本，不足或等于1USDT则退出；入场成本是沉没成本，不再扣一次。固定H到期也退出。',
        '所有决策使用基础1倍费用估算；真实成交、费用和负资金费支付分别承受1/2/3倍压力。成本场景的实际NAV可改变数量，因此不是同一成交清单乘常数。信号T后下一分钟真实开盘为执行参考；T至T+1分钟资金费先结算旧仓，不进入T已定数量预算。不在折边界重置账户；末端计成本平仓。',
        '每配置10,000USDT，初始现货现金5,000与永续抵押5,000，不转账、不借币、现金零收益。H={672,1008,1344}小时是最长持有上限，实际可能提前退出。f={0.15,0.25,0.35}是每条腿名义额/已知总NAV的原值，毛名义敞口约2f，不是归一化资金权重。q按f×已知NAV/已知spot价向共同lot下取整，两腿基币数量完全匹配。BTC/ETH独立，共18具体配置。',
        '## 数据、时序与三项验证','',
        '来源：[Binance官方归档](https://github.com/binance/binance-public-data)及[资金费历史接口](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History)，2026-10-23只读核对。每币525,600现货/永续分钟、8,760小时mark及1,095实际资金费，10个原始归一化文件SHA、纳秒单位、可得时间、收盘与连续性全部核对；数据存于忽略data，路径及哈希留档。Oct1现货元数据快照与原perp元数据是历史代理。',
        '- Walk-forward：输入2025-09-16至2026-09-16，21日费用上下文和3日初始间隔；不拟合模型、无预测标签，purge不适用。固定OOS为2025-10-10 00:01至2026-09-11 00:01UTC，336天、12连续28日折。已反复研发历史，不是未触碰最终留出。保存全部逐折指标及连续OOS小时净值，独立重建初始本金、全部闭合分钟spot/perp成交价NAV和原子成交后参考NAV的整体回撤。',
        '- 敏感性：H×单腿f二维3×3，每币相邻格包含中心；全部54场景的净收益、完整分钟代理DD、原小时Sharpe、分钟Calmar、邻域3倍正比均保留。邻接Sharpe差>2样本标准差仅为描述性陡变标记，不是显著性检验。网格边界表现不触发同一OOS事后加格。',
        '- 成本：现货单侧10bp、perp5bp、半价差1bp、滑点2bp，加0.5×先前20完整日log收益样本波动×sqrt(本腿名义额/先前20日quote ADV)，参与率≤0.1%；不利tick与共同lot/最小名义额限制。实际负资金费乘压力倍数，正收入不放大。永续独立抵押及1%小时mark高点包络、独立事件前后现金/保证金检查；末端无完整小时只用最后闭合分钟perp成交high代理，不读OOS后高点。无自动强平或真实历史阶梯模型。',
        '冻结门槛：全成本净正，1倍至少8/12正折，3倍连续分钟DD≤25%，相邻3倍净正≥60%，1倍至少4完整往返，毛参考盈亏/总模型成本≥2.5，所有成本无现金/保证金违例及现金拒单，终点空仓。费用加回不是独立零成本反事实。各组件手续费/价差/滑点/冲击/取整残差及支付/收入资金费分开保存。', '',
        '## 真实结果','',f"通过{s['passed']}、淘汰{s['rejected']}；1/2/3倍净正配置数{s['positive_configs_by_cost']['1']}/{s['positive_configs_by_cost']['2']}/{s['positive_configs_by_cost']['3']}。",'',
        f"1倍收益最高`{best['name']}`：三成本{a['net_return_pct']:+.6f}%/{b['net_return_pct']:+.6f}%/{c['net_return_pct']:+.6f}%；1倍正折{a['positive_folds']}/12，完整往返{a['round_trips']}，3倍完整分钟代理回撤{c['max_drawdown_pct']:.6f}%，邻域3倍正比{best['sensitivity']['local_3x_neighbor_positive_fraction']:.1%}。",'',
        '|候选|H上限小时|单腿f|1倍|2倍|3倍|1倍正折|往返|3倍分钟DD|邻域3倍正比|结论|','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
    for name in s['ranked_by_1x_net_return']:
        x=r['configs'][name];aa,bb,cc=[x['scenarios'][str(m)] for m in (1,2,3)]
        lines.append(f"|{name}|{x['holding_hours']}|{x['per_leg_fraction']}|{aa['net_return_pct']:+.4f}%|{bb['net_return_pct']:+.4f}%|{cc['net_return_pct']:+.4f}%|{aa['positive_folds']}/12|{aa['round_trips']}|{cc['max_drawdown_pct']:.4f}%|{x['sensitivity']['local_3x_neighbor_positive_fraction']:.0%}|{x['status']}|")
    lines+=['','逐项失败数量：`'+json.dumps(r['failure_counts'],ensure_ascii=False)+'`。','','## 只读对照与局限','',
        f"旧报告`{r['source_report']}` SHA256`{r['source_report_sha256']}`。18项B0所有成本、折和完整事件仍由原报告/原gzip负责；本轮仅核对原哈希并读取比较，不映射为新结果。以下2项现货持有基准同窗同本金、4500目标名义，其余现金，不是等风险carry。现金零收益解析参考为0。",'',
        '|只读基准|1倍|2倍|3倍|3倍分钟DD|','|---|---:|---:|---:|---:|']
    for x in r['benchmark_read_only'].values():
        aa,bb,cc=[x['scenarios'][str(m)] for m in (1,2,3)];lines.append(f"|{x['name']}|{aa['net_return_pct']:+.4f}%|{bb['net_return_pct']:+.4f}%|{cc['net_return_pct']:+.4f}%|{cc['max_drawdown_pct']:.4f}%|")
    lines+=['',f"完整登记{ctx['registry_events']}事件、{ctx['registry_ids']}ID、{ctx['canonical_research_definitions_excluding_observations']}规范研究定义及{len(ctx['prior_conclusions_read'])}份既往结论已读。初始16项已有实际证据，无未补回测；部分legacy旧字段缺省不是result_available=false。新B1参数不同于旧8/24/48h配置，不能仅因策略族相同排除，也未重算精确旧配置。多重选择偏差存在，未计算DSR/PBO。",'',
        '小时NAV用hh:01开盘参考，分钟NAV用闭合分钟收盘与原子成交后参考，采样集合不是严格超集，不能断言分钟DD必≥小时DD。分别保留原值；分钟交易价代理不等于分钟mark价或分钟内极值。缺历史L2/TCA、真实清算阶梯、初始保证金及托管/USDT锚校准。任何正回测都不代表稳定实盘盈利。', '',
        '原冻结SMA从上一轮22UTC续至本轮00:30，按原65日±1%规则执行到期00:01日决策，保留现金、数量、desired、费用和完整NAV前缀；实际延迟公开bar重建单独见forward_result.md，不是paper10真实报价模拟。十策略计划/状态只读不改；不下真实单，不重置账户，不强制提前平仓。', '',
        f"完整逐场景曲线/成交/资金费/决策保留results/*.json.gz；同哈希原始分钟重建连续分钟NAV，保存其SHA与样本数。核验命令：`PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/{R.name}/run.py verify`。已finish报告原字节与登记SHA优先，只核验后清理重复checkpoint和本轮缓存。",'']
    (R/'result.md').write_text('\n'.join(lines));print(json.dumps({'summary':s,'failure_counts':r['failure_counts']},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
