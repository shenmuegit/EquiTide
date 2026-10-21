"""Write the complete result table and sensitivity surface from saved results only."""
import csv, gzip, hashlib, json
from collections import Counter
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

R = Path(__file__).resolve().parent
ROOT = R.parents[2]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
put = lambda p, x: p.write_text(json.dumps(x, ensure_ascii=False, indent=2, allow_nan=False) + '\n')

def main():
    report = json.loads((R / 'report.json').read_text())
    plan = json.loads((R / 'plan.json').read_text())
    context = json.loads((R / 'context.json').read_text())
    looks, hurdles = plan['grid']['lookback_days'], plan['grid']['entry_hurdle_pct']
    by = {(c['asset'], c['lookback_days'], c['entry_hurdle_pct']): c for c in report['configs'].values()}
    rows, edges = [], []
    for c in report['configs'].values():
        for k in (1, 2, 3):
            z = c['scenarios'][str(k)]
            rows.append({'configuration': c['name'], 'asset': c['asset'], 'lookback_days': c['lookback_days'], 'entry_hurdle_pct': c['entry_hurdle_pct'], 'cost_multiplier': k, 'net_return_pct': z['net_return_pct'], 'max_drawdown_1m_sampled_pct': z['max_drawdown_1m_sampled_pct'], 'daily_sharpe_annualized': z['daily_sharpe_annualized'], 'calmar_daily_sampled': z['calmar_daily_sampled'], 'round_trips': z['round_trips'], 'cost_usdt': z['cost_usdt'], 'cost_pct_initial_capital': float(z['cost_usdt']) / 20, 'gross_reference_pnl_to_cost': z['gross_reference_pnl_to_cost'], 'local_3x_positive_fraction': c['sensitivity']['local_3x_neighbor_positive_fraction'], 'status': c['status']})
    for asset in ('BTC', 'ETH'):
        for i, look in enumerate(looks):
            for j, hurdle in enumerate(hurdles):
                c = by[asset, look, hurdle]
                for ii, jj, axis in [(i + 1, j, 'lookback_days'), (i, j + 1, 'entry_hurdle_pct')]:
                    if ii >= len(looks) or jj >= len(hurdles):
                        continue
                    other = by[asset, looks[ii], hurdles[jj]]
                    a, b = c['scenarios']['3']['daily_sharpe_annualized'], other['scenarios']['3']['daily_sharpe_annualized']
                    if a is not None and b is not None:
                        edges.append({'from': c['name'], 'to': other['name'], 'axis': axis, 'absolute_3x_Sharpe_difference': abs(a - b)})
    threshold = 2 * float(np.std([e['absolute_3x_Sharpe_difference'] for e in edges], ddof=1))
    report['sensitivity_cliffs'] = {'heuristic': 'Adjacent absolute 3x daily-Sharpe difference > twice sample SD of all adjacent differences. Descriptive, not a significance test.', 'threshold': threshold, 'edges': [{**e, 'flagged': e['absolute_3x_Sharpe_difference'] > threshold} for e in edges], 'best_is_grid_boundary': True, 'best_neighborhood_is_profitable_plateau': False}
    report['research_context'] = {'prior_canonical_research_definitions': context['canonical_research_definitions_excluding_observations'], 'new_predeclared_configurations': 18, 'independent_final_holdout': False, 'current_OOS_parameter_selection': False, 'initial_16_missing_actual_results': 0}
    report['benchmark_read_only']['source_sha256'] = sha(ROOT / report['benchmark_read_only']['source_report'])
    report['failure_counts'] = dict(Counter(k for c in report['configs'].values() for k, v in c['gates'].items() if not v))
    report['account_scope'] = plan['account_scope']
    report['artifacts'].update(sensitivity='sensitivity.csv', surface='sensitivity_surface.png', verification='verification.json')
    put(R / 'report.json', report)
    with (R / 'sensitivity.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n'); w.writeheader(); w.writerows(rows)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    limit = max(abs(c['scenarios']['3']['net_return_pct']) for c in by.values())
    for asset, ax in zip(('BTC', 'ETH'), axes):
        values = np.array([[by[asset, look, h]['scenarios']['3']['net_return_pct'] for h in hurdles] for look in looks])
        im = ax.imshow(values, cmap='RdYlGn', vmin=-limit, vmax=limit)
        ax.set(xticks=range(3), xticklabels=[f'{h:g}%' for h in hurdles], yticks=range(3), yticklabels=looks, xlabel='Entry hurdle', ylabel='Lookback days', title=f'{asset}: 3x cost net return')
        for i in range(3):
            for j in range(3): ax.text(j, i, f'{values[i,j]:+.2f}%', ha='center', va='center')
    fig.colorbar(im, ax=axes, label='Net return %', shrink=.8)
    fig.savefig(R / 'sensitivity_surface.png', dpi=140); plt.close(fig)
    summary = report['summary']; best = report['configs'][summary['ranked_by_1x_net_return'][0]]
    a, b, z = [best['scenarios'][str(k)] for k in (1, 2, 3)]
    lines = ['# BTC/ETH 长周期绝对动量：真实历史回测结果', '',
        f"- 轮次 `{R.name}`；冻结UTC `{plan['frozen_at_utc']}`；计划SHA256 `{sha(R/'plan.json')}`。18个具体配置都在计算前单独reserve。",
        '- 本轮为真实归档行情的离线回测，无真实订单。重复使用的2025–2026历史不是未触碰最终留出，也不能证明稳定实盘盈利。', '',
        '## 动机与规则', '',
        '此前7/14/28日动量批次全部淘汰，本轮事前固定更长的56/84/112日×入场门槛0/2.5/5%双轴网格，检验更慢信号是否改善成本与折一致性。只读引用旧结果，不重跑旧配置。动机来自[Liu与Tsyvinski，NBER WP 24877](https://www.nber.org/papers/w24877)；本规则不是论文复制，也不继承其收益结论。',
        'BTC、ETH各配置分别使用2,000 USDT独立现货账户，原始资产资金占比为1，不归一化或跨币转账。用已闭合UTC日线计算ROC_L=close[j]/close[j−L]−1；空仓时ROC严格超过入场门槛才入场，持仓时ROC≤0退出，其余维持状态。下一UTC日00:01分钟开盘参考执行，距信号可用60秒。无杠杆、做空、借币或现金收益；终点计成本清仓。', '',
        '## 三项验证', '',
        '- Walk-forward：输入2024-09-16至2026-09-16；OOS为2025-09-19 00:01至2026-09-14 00:01 UTC，共360天，12个连续30日折，账户跨折连续。固定规则无拟合、标签或OOS择参，标签purge不适用；365日预热及初始3日间隔。逐折收益/日采样回撤与连续OOS分钟采样整体回撤均留档。',
        '- 敏感性：各币完整3×3双轴网格，邻域为相邻索引组成的3×3区域，包含中心；逐变体收益、回撤、Sharpe和Calmar见sensitivity.csv，图见sensitivity_surface.png。相邻三倍Sharpe差值>全部相邻差值样本标准差的2倍作为描述性突变标记，详见report.json，不当作统计显著性检验。最高收益处在L=56、入场0%的网格边界，不能外推为最优参数。',
        '- 成本：每侧手续费10bp、估算半价差1bp、滑点2bp，另加0.5×前20个完整日收益样本波动率×sqrt(订单预算/前20日quote ADV)冲击，参与率≤0.1%。所有项同时按1/2/3倍放大，Decimal价格tick、数量步长及名义额校验。复用10月14日冻结过滤器，同本轮公开查询比较一致，避免仅因查询时间变化产生新指纹。历史盘口和历史过滤器不可得；成交是模型假设。现货无空头与借币，资金费/借币不适用。',
        '- 整体回撤取全OOS一分钟收盘与成交后参考点，不包含分钟内极值；Sharpe按日收益年化，Calmar明确使用日采样回撤。成本占初始资金比例及毛参考盈亏/成本比完整保留；后者是成本加回的诊断量，不是独立零成本策略或相对持有的alpha。', '',
        '## 结果与淘汰理由', '',
        f"- 18配置、54成本场景全部实算；通过{summary['passed']}、淘汰{summary['rejected']}。1/2/3倍成本净正数为{summary['positive_configs_by_cost']['1']}/{summary['positive_configs_by_cost']['2']}/{summary['positive_configs_by_cost']['3']}，全网格三倍净正比例{summary['global_3x_positive_neighbor_fraction']:.1%}。",
        f"- 收益最高的`{best['name']}`：1/2/3倍净收益{a['net_return_pct']:+.4f}%/{b['net_return_pct']:+.4f}%/{z['net_return_pct']:+.4f}%；1倍仅{a['positive_folds']}/12折盈利，9次往返；3倍整体回撤{z['max_drawdown_1m_sampled_pct']:.4f}%，局部邻域三倍净正比例{best['sensitivity']['local_3x_neighbor_positive_fraction']:.0%}，低于60%门槛。",
        '- 18/18未达至少8/12盈利折，18/18未达邻域60%盈利比例；16/18至少一档成本净亏、16/18三倍回撤超25%。正收益角落没有形成可接受平台，所有负收益、平收益折及淘汰结果全部保留。',
        '- 冻结门槛还要求至少8次往返、1倍毛参考盈亏/成本≥2.5、无容量/过滤器拒单和终点持仓为零，没有根据本轮结果改门槛。同期持有基准只读复用20261014T084051Z报告，现金基准为零；超过基准不能代替资格门槛。', '',
        '|配置|资产|L|入场|1倍|2倍|3倍|1倍正折|3倍回撤|往返|3倍邻域正比|状态|', '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
    for name in summary['ranked_by_1x_net_return']:
        c = report['configs'][name]; one, two, three = [c['scenarios'][str(k)] for k in (1, 2, 3)]
        lines.append(f"|{name}|{c['asset']}|{c['lookback_days']}|{c['entry_hurdle_pct']:g}%|{one['net_return_pct']:+.3f}%|{two['net_return_pct']:+.3f}%|{three['net_return_pct']:+.3f}%|{one['positive_folds']}/12|{three['max_drawdown_1m_sampled_pct']:.3f}%|{one['round_trips']}|{c['sensitivity']['local_3x_neighbor_positive_fraction']:.0%}|{c['status']}|")
    lines += ['', '## 留档、账户与复现', '',
        f"- 计算前读取完整主登记及片段，共{context['registry_events']}事件、{context['registry_ids']}登记ID；排除账户观察并合并等价定义后为{context['canonical_research_definitions_excluding_observations']}个历史研究定义，本轮新增18。初始16项均有实际结果，缺失0。",
        '- 大量历史参数比较存在选择偏差；未报告DSR/PBO或独立最终留出结论。两币、参数和时期的既往结果不被删除或重新命名复算。',
        '- 十策略冻结计划与状态未改；旧SMA延迟shadow按原规则连续续接至2026-10-21 10:00 UTC，新增13,620分钟和每币10次日决策，三倍累计收益−4.311980%，仍不足长期资格。所有旧源文件SHA保持，未倒填十策略交易，完整连续性证据与网络失败恢复见[续接说明](forward_result.md)。',
        '- 54场景精确重放，另核对19,440个ROC/信号可用时序及逐笔余额守恒；核验结果见verification.json。输入文件、必要代码和产物SHA见data_manifest.json。',
        f"- 离线核验：`/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/{R.name}/run.py verify`，从固定仓库根目录执行；不联网、不改登记或账户。",
        '- 保存完整report、spec、逐折、成本、敏感性、交易、决策及日净值证据。成功核验后仅清理本轮可重建checkpoint，不清理旧账户或大行情缓存。下轮优先研究不同经济假设或独立新增数据；不依据本轮最高收益角落直接扩展并宣称独立验证。', '']
    (R / 'result.md').write_text('\n'.join(lines))
    print(json.dumps({'summary': summary, 'failure_counts': report['failure_counts'], 'cliff_flags': sum(e['flagged'] for e in report['sensitivity_cliffs']['edges'])}))

if __name__ == '__main__': main()
