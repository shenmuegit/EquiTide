"""Render every registered close-channel timeout result, without selecting parameters."""
import csv, json
from collections import Counter
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

R = Path(__file__).resolve().parent

def main():
    r = json.loads((R / 'report.json').read_text())
    plan = json.loads((R / 'plan.json').read_text())
    context = json.loads((R / 'context.json').read_text())
    looks, hurdles = plan['grid']['entry_lookback_days'], plan['grid']['max_holding_days']
    by = {(c['asset'], c['entry_lookback_days'], c['max_holding_days']): c for c in r['configs'].values()}
    rows, edges = [], []
    for c in r['configs'].values():
        for k in (1, 2, 3):
            z = c['scenarios'][str(k)]
            rows.append({'configuration': c['name'], 'asset': c['asset'], 'entry_lookback_days': c['entry_lookback_days'], 'max_holding_days': c['max_holding_days'], 'cost_multiplier': k, 'net_return_pct': z['net_return_pct'], 'max_drawdown_1m_sampled_pct': z['max_drawdown_1m_sampled_pct'], 'daily_sharpe_annualized': z['daily_sharpe_annualized'], 'calmar_daily_sampled': z['calmar_daily_sampled'], 'cost_usdt': z['cost_usdt'], 'cost_pct_initial_capital': float(z['cost_usdt']) / 20, 'gross_reference_pnl_to_cost': z['gross_reference_pnl_to_cost'], 'round_trips': z['round_trips'], 'local_3x_positive_fraction': c['sensitivity']['local_3x_neighbor_positive_fraction'], 'status': c['status']})
    for asset in ('BTC', 'ETH'):
        for i, look in enumerate(looks):
            for j, hurdle in enumerate(hurdles):
                c = by[asset, look, hurdle]
                for ii, jj, axis in [(i + 1, j, 'entry_lookback_days'), (i, j + 1, 'max_holding_days')]:
                    if ii >= len(looks) or jj >= len(hurdles): continue
                    other = by[asset, looks[ii], hurdles[jj]]
                    a, b = c['scenarios']['3']['daily_sharpe_annualized'], other['scenarios']['3']['daily_sharpe_annualized']
                    if a is not None and b is not None: edges.append({'from': c['name'], 'to': other['name'], 'axis': axis, 'absolute_3x_Sharpe_difference': abs(a - b)})
    threshold = 2 * float(np.std([e['absolute_3x_Sharpe_difference'] for e in edges], ddof=1)) if len(edges) > 1 else None
    r['sensitivity_cliffs'] = {'heuristic': 'Adjacent absolute3x daily-Sharpe difference >2 sample SD of adjacent differences; descriptive only.', 'threshold': threshold, 'edges': [{**e, 'flagged': threshold is not None and e['absolute_3x_Sharpe_difference'] > threshold} for e in edges]}
    r['grid_boundary_note'] = 'All cells retained, including boundary cells. A boundary maximum is descriptive only; do not extend or select a new grid using these same OOS results as independent validation.'
    r['source_access_failures'] = plan['source_access_failures']
    r['research_context'] = {'prior_canonical_research_definitions': context['canonical_research_definitions_excluding_observations'], 'new_predeclared_configurations': 18, 'initial_16_missing_actual_results': 0, 'independent_final_holdout': False, 'parameter_selection_on_current_OOS': False}
    r['failure_counts'] = dict(Counter(k for c in r['configs'].values() for k, passed in c['gates'].items() if not passed))
    r['positive_sharpe_3x_fraction'] = sum((c['scenarios']['3']['daily_sharpe_annualized'] or 0) > 0 for c in r['configs'].values()) / len(r['configs'])
    r['artifacts'].update(sensitivity='sensitivity.csv', surface='sensitivity_surface.png', verification='verification.json')
    (R / 'report.json').write_text(json.dumps(r, ensure_ascii=False, indent=2, allow_nan=False) + '\n')
    with (R / 'sensitivity.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n'); w.writeheader(); w.writerows(rows)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    limit = max(abs(c['scenarios']['3']['net_return_pct']) for c in by.values()) or 1
    for asset, ax in zip(('BTC', 'ETH'), axes):
        values = np.array([[by[asset, look, h]['scenarios']['3']['net_return_pct'] for h in hurdles] for look in looks])
        im = ax.imshow(values, cmap='RdYlGn', vmin=-limit, vmax=limit)
        ax.set(xticks=range(3), xticklabels=[f'{h:g}' for h in hurdles], yticks=range(3), yticklabels=looks, xlabel='Maximum holding days', ylabel='Entry channel lookback days', title=f'{asset}: 3x cost net return')
        for i in range(3):
            for j in range(3): ax.text(j, i, f'{values[i,j]:+.2f}%', ha='center', va='center')
    fig.colorbar(im, ax=axes, label='Net return %', shrink=.8); fig.savefig(R / 'sensitivity_surface.png', dpi=140); plt.close(fig)
    s = r['summary']; best = r['configs'][s['ranked_by_1x_net_return'][0]]; a, b, z = [best['scenarios'][str(k)] for k in (1, 2, 3)]
    lines = ['# BTC/ETH 收盘通道突破与最长持仓期限：预登记历史回测', '',
        f"轮次 `{R.name}`；冻结UTC `{plan['frozen_at_utc']}`。18个具体配置先reserve，后执行54个成本场景；所有结果包括负收益永久保留。", '',
        '## 经济假设与完整规则', '',
        '检验突破后限制持仓期限能否改善不利漂移或收益集中，同时承认额外换手与截断趋势可能降低收益。已闭合信号日j的上轨为此前L个日收盘最大值、下轨为此前10个日收盘最小值，均不含当前信号日。空仓仅close[j]>上轨才入场。持仓优先在自实际成功买入参考时刻起满H个UTC日退出，否则仅close[j]<下轨退出；上下轨相等不触发价格交易，退出优先且同日不重入。仅成功成交改变持仓时钟；拒单保持真实状态。参考[TradingView通道定义](https://www.tradingview.com/support/solutions/43000502253-donchian-channels-dc/)与[官方策略FAQ的持仓时限说明](https://www.tradingview.com/pine-script-docs/faq/strategies/)。本轮使用收盘通道而非传统高低价通道，且保留60秒延迟，不复制即时同收盘成交示例；来源不背书盈利。',
        'BTC、ETH各配置为独立2,000 USDT现货账户，原始资产资金占比1，不归一化、不跨币转账。预设网格资产×L{10,20,40}日入场通道×H{5,10,20}日最长持仓；退出通道10日固定。信号闭合后60秒于下一UTC日00:01分钟开盘参考成交；持仓时钟跨折连续；终点计成本清仓。无杠杆、做空、借币、加仓或现金收益。',
        '## 三项验证', '',
        '- Walk-forward：真实Binance归档1分钟数据，输入2024-09-16至2026-09-16，OOS为2025-09-19 00:01至2026-09-14 00:01 UTC，共360天；365日上下文及3日初始间隔，12个连续30日窗口，账户跨折连续。通道仅用信号日前已知闭合收盘，实际持仓时钟跨折连续，无预测拟合、未来标签或OOS选参，标签purge不适用。全部逐折收益与日采样回撤保留，并用初始本金及完整OOS分钟收盘/成交后参考标记计算整体回撤；不包含分钟内极值。',
        '- 敏感性：同时变化入场回看期L与最长持仓H；同资产相邻索引构成3×3邻域，包含中心。逐格收益、整体回撤、Sharpe、Calmar及邻域盈利比例见sensitivity.csv，完整表面见sensitivity_surface.png。相邻Sharpe突变只作描述性标记，不是显著性或独立验证结论。',
        '- 成本：每侧手续费10bp、估算半价差1bp、滑点2bp，加0.5×前20个完整日样本波动率×sqrt(订单预算/前20日quote ADV)冲击，参与率≤0.1%；全部项同时施加1/2/3倍压力。Decimal价格tick、数量步长、名义额和前置5分钟VWAP代理检查；冻结过滤器与本轮公开查询比较一致。历史L2、历史过滤器和真实IOC成交不可得。现货无空头，资金费及借币约束不适用。成本占比与毛参考盈亏/成本比均保留；成本加回不是独立零成本策略或相对持有alpha。', '',
        '## 实际结果', '',
        f"- 18配置通过{s['passed']}、淘汰{s['rejected']}。1/2/3倍净正数量为{s['positive_configs_by_cost']['1']}/{s['positive_configs_by_cost']['2']}/{s['positive_configs_by_cost']['3']}；三倍净正比例{s['global_3x_positive_neighbor_fraction']:.1%}，三倍Sharpe正比例{r['positive_sharpe_3x_fraction']:.1%}。",
        f"- 1倍收益最高的`{best['name']}`：1/2/3倍{a['net_return_pct']:+.4f}%/{b['net_return_pct']:+.4f}%/{z['net_return_pct']:+.4f}%，1倍正折{a['positive_folds']}/12、往返{a['round_trips']}次，3倍整体回撤{z['max_drawdown_1m_sampled_pct']:.4f}%，局部三倍盈利比例{best['sensitivity']['local_3x_neighbor_positive_fraction']:.1%}。",
        '- 冻结门槛要求所有成本净正、1倍至少8/12盈利折、三倍回撤≤25%、邻域三倍正收益≥60%、至少8次往返、1倍毛参考盈亏/成本≥2.5、无容量/过滤器拒单且终点平仓。逐项失败见report.json的gates/failure_counts，未依据结果放宽。同期持有基准只读复用20261014T084051Z原报告，现金基准0；优于基准不替代门槛。', '',
        '|配置|资产|L|最长持仓日|1倍|2倍|3倍|1倍正折|3倍回撤|往返|3倍邻域正比|状态|', '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
    for name in s['ranked_by_1x_net_return']:
        c = r['configs'][name]; x, y, z = [c['scenarios'][str(k)] for k in (1, 2, 3)]
        lines.append(f"|{name}|{c['asset']}|{c['entry_lookback_days']}|{c['max_holding_days']:g}|{x['net_return_pct']:+.3f}%|{y['net_return_pct']:+.3f}%|{z['net_return_pct']:+.3f}%|{x['positive_folds']}/12|{z['max_drawdown_1m_sampled_pct']:.3f}%|{x['round_trips']}|{c['sensitivity']['local_3x_neighbor_positive_fraction']:.0%}|{c['status']}|")
    lines += ['', '## 局限、连续账户与复现', '',
        f"计算前读取完整登记及片段共{context['registry_events']}事件、{context['registry_ids']}登记ID，排除观察并合并等价定义后为{context['canonical_research_definitions_excluding_observations']}个既往研究定义，本轮新增18；初始16项已有真实结果，无待补项。",
        '既往通道策略的不同参数继续允许新配置；本轮按完整规则指纹逐一reserve，无精确已完成配置重跑。最高点若在网格边界只作描述，不据此扩大本轮网格或声称独立验证。',
        '2025–2026历史反复用于策略研发，本轮不是未触碰最终留出；存在多重比较与选择偏差，没有DSR/PBO或稳定实盘盈利结论。指标边界自检只验证公式，不当作行情回测证据。',
        '原SMA冻结账户按原现金、数量、desired及成本继续分钟估值，独立说明见forward_result.md；paper10的冻结计划、账户状态和观察由独立任务维护，本轮只读、不重置、不补单。',
        f"实际重放与独立信号/时序、余额、完整分钟回撤核验见verification.json。离线复核：`/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/{R.name}/run.py verify`。输入SHA、代码与产物哈希见data_manifest.json；已finish报告原字节与登记SHA优先，核验后只清理可重建checkpoint及本轮字节码。", '']
    (R / 'result.md').write_text('\n'.join(lines))
    print(json.dumps({'summary': s, 'failure_counts': r['failure_counts']}, ensure_ascii=False))

if __name__ == '__main__': main()
