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
        research_context={'prior_canonical_research_definitions':ctx['canonical_research_definitions_excluding_observations'],'new_candidate_configs':18,'new_comparators':2,'independent_final_holdout':False,'DSR_PBO_computed':False})
    put(R/'report.json',r);csvput(R/'sensitivity.csv',rows);csvput(R/'fold_results.csv',folds)
    fig,axes=plt.subplots(1,2,figsize=(10,4),constrained_layout=True);limit=max(abs(x['scenarios']['3']['net_return_pct']) for x in candidates) or 1
    for asset,ax in zip(('BTC','ETH'),axes):
        values=np.array([[by[asset,h,f]['scenarios']['3']['net_return_pct'] for f in fs] for h in hs]);im=ax.imshow(values,cmap='RdYlGn',vmin=-limit,vmax=limit)
        ax.set(xticks=range(3),xticklabels=fs,yticks=range(3),yticklabels=hs,xlabel='Raw per-leg NAV fraction',ylabel='Holding hours',title=asset+': 3x cost net return')
        for i in range(3):
            for j in range(3):ax.text(j,i,f'{values[i,j]:+.2f}%',ha='center',va='center')
    fig.colorbar(im,ax=axes,label='Net return %',shrink=.8);fig.savefig(R/'sensitivity_surface.png',dpi=140);plt.close(fig)
    s=r['summary'];best=r['configs'][s['ranked_by_1x_net_return'][0]];a,b,c=[best['scenarios'][str(m)] for m in (1,2,3)]
    lines=['# BTC/ETH低换手匹配现货多头/永续空头资金费：预登记回测','',f"轮次`{R.name}`，冻结UTC`{p['frozen_at_utc']}`。18候选＋2同窗现货持有基准先reserve后计算，共60成本场景；所有正负结果和保证金/拒单事实保留。",'',
        '## 完整规则、原值敞口与来源','',
        '复用20261001T053425Z/carry.py原账本、费用与B0执行规则，代码字节未改：小时T使用已闭合上一小时的分钟收盘，空仓且完整H小时可在已知终点前完成时强制尝试开仓，T+1分钟真实现货/永续开盘成交；固定T+H小时到期在下一分钟平仓，后续新小时才可再入。终点计成本平仓，不在折边界重开账户。',
        '每配置独立10,000USDT，初始现货现金5,000、永续抵押5,000，无跨账本转账、借币或现金收益。参数f={0.15,0.25,0.35}是每条腿名义额占决策已知总NAV的原始比例，毛名义敞口约2f；不是资金权重归一化。q按f×已知NAV/已知spot收盘向共同lot下取整，两腿相同基币数量。H={672,1008,1344}小时；BTC/ETH独立，共18具体配置。',
        '资金费按实际settlement纳秒时间、实际mark、当时旧持仓结算。T至T+1分钟间的资金费先归旧仓，但不进入T已固定的数量预算；available_ts忠实保留，B0不按未来资金费择时。1/2/3倍放大执行费用和负资金费支出，正收入不放大。现货无空头和借币，永续抵押与浮动损益另查；原1%小时mark高点包络及独立前后事件现金/保证金检查均保留，任何违例/现金不足拒单淘汰。完整OOS小时包络可能含入场前/退出后极值，仅用于事后资格判定，不作为信号；终端缺完整小时mark时用最后闭合分钟perp成交高点代理，不读OOS之后高点。未模拟自动强平和历史阶梯，不能声称实际可清算安全。',
        '来源为[Binance官方归档](https://github.com/binance/binance-public-data)、[实际资金费接口文档](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History)及仓库原账本。两币各525,600现货/永续分钟、8,760小时mark、1,095实际资金费和原始合约元数据，纳秒单位/收盘/连续性及10文件SHA核对。冻结Oct1 spot快照和归一化perp元数据为历史代理，不是新查到的历史规则。', '',
        '## 三项验证','',
        '- Walk-forward：真实输入2025-09-16至2026-09-16；21日成本上下文＋3日初始间隔，无拟合或未来标签、purge不适用。OOS为2025-10-10 00:01至2026-09-11 00:01UTC，336天，12连续28日折；账户/仓位跨折连续。不是未触碰最终留出。逐折收益及小时采样回撤完整保存；整体回撤额外用初始本金、所有闭合分钟spot/perp成交价NAV和原子成交后参考NAV独立重建。它是分钟成交价代理NAV，不是一分钟mark价或分钟内极值。',
        '- 敏感性：H×原始单腿f二维3×3，每币独立相邻索引邻域含中心。保留每格收益、完整分钟代理回撤、小时Sharpe、分钟采样Calmar与邻域3倍正收益比例。相邻Sharpe突变仅作描述，边界最高值不触发本轮OOS加格。',
        '- 成本：spot每侧10bp、perp5bp、半价差1bp、滑点2bp，加0.5×之前20完整日样本log波动率×sqrt(本腿名义额/本腿20日quote ADV)；参与率≤0.1%，不利tick与共同lot/最小名义额检查。1/2/3倍全场景包含终端两腿成本及实际支出资金费。费用/价差/滑点/冲击/取整残差、收入与支付分开报告。1倍毛参考盈亏/总模型成本需≥2.5；成本加回不是独立零成本策略或等风险alpha。历史L2/TCA、真实清算/托管/USDT锚风险未校准。', '',
        '## 实际结果','',f"18候选通过{s['passed']}、淘汰{s['rejected']}；1/2/3倍净正数量{s['positive_configs_by_cost']['1']}/{s['positive_configs_by_cost']['2']}/{s['positive_configs_by_cost']['3']}。2个同窗持有基准均为reference-only rejected，不代表其收益必然为负。",'',
        f"1倍收益最高`{best['name']}`：三成本{a['net_return_pct']:+.6f}%/{b['net_return_pct']:+.6f}%/{c['net_return_pct']:+.6f}%；1倍正折{a['positive_folds']}/12、完整往返{a['round_trips']}，3倍全分钟代理回撤{c['max_drawdown_pct']:.6f}%，邻域正比{best['sensitivity']['local_3x_neighbor_positive_fraction']:.1%}。",'',
        '冻结门槛：全成本净正、1倍至少8/12正折、3倍连续分钟代理DD≤25%、邻域3倍净正≥60%、至少4完整往返、1倍毛参考盈亏/总成本≥2.5、所有成本无现金/保证金违例和现金不足拒单、终点空仓。逐项gates和失败计数保留，不因结果放宽。两账本不转账可能造成高成本路径更少再入/拒单，从而总损益非单调；不是提高费用改善收益的证据。', '',
        '|候选|H小时|单腿f|1倍|2倍|3倍|1倍正折|往返|3倍全分钟DD|邻域正比|状态|','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
    for name in s['ranked_by_1x_net_return']:
        x=r['configs'][name];aa,bb,cc=[x['scenarios'][str(m)] for m in (1,2,3)]
        lines.append(f"|{name}|{x['holding_hours']}|{x['per_leg_fraction']}|{aa['net_return_pct']:+.4f}%|{bb['net_return_pct']:+.4f}%|{cc['net_return_pct']:+.4f}%|{aa['positive_folds']}/12|{aa['round_trips']}|{cc['max_drawdown_pct']:.4f}%|{x['sensitivity']['local_3x_neighbor_positive_fraction']:.0%}|{x['status']}|")
    lines+=['','## 同窗基准与限制','','|基准|1倍|2倍|3倍|3倍全分钟DD|','|---|---:|---:|---:|---:|']
    for x in r['configs'].values():
        if x['role']=='benchmark':
            aa,bb,cc=[x['scenarios'][str(m)] for m in (1,2,3)];lines.append(f"|{x['name']}|{aa['net_return_pct']:+.4f}%|{bb['net_return_pct']:+.4f}%|{cc['net_return_pct']:+.4f}%|{cc['max_drawdown_pct']:.4f}%|")
    lines+=['','基准为初始45%目标名义spot持有，其余现金；有方向敞口，与匹配carry不是等风险比较。现金零收益解析基准0。', '',
        f"计算前完整登记{ctx['registry_events']}事件、{ctx['registry_ids']}ID、{ctx['canonical_research_definitions_excluding_observations']}规范研究定义，{len(ctx['prior_conclusions_read'])}份既往结论已读；初始16项无缺结果。18新候选和2新同窗基准均独立登记，不能把较长持有期当旧8/24/48h精确重测。多重试验与复用历史限制所有显著性，未计算DSR/PBO，不证明稳定实盘盈利。",'',
        '原冻结SMA与paper10账户独立：SMA只按原现金/数量/desired继续20→22UTC分钟估值，见forward_result.md；paper10计划/状态只读，无真实订单、资金转移或账户重置。', '',
        f"完整逐场景小时曲线/成交/资金费/决策保存在results/*.json.gz，连续分钟NAV由相同哈希原始分钟及完整事件重建，保存逐场景SHA和样本数，不提交可重建大分钟曲线。实际重放核对见verification.json；命令：`PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/{R.name}/run.py verify`。该命令不写金融报告或登记。已finish报告原字节优先，仅核验后删除重复checkpoint；原始大行情留data并记录SHA/路径。",'']
    (R/'result.md').write_text('\n'.join(lines));print(json.dumps({'summary':s,'failure_counts':r['failure_counts']},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
