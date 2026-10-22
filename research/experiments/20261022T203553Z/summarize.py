"""Summarize all IBS reversal results and sensitivity cells without parameter selection."""
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
    looks, hurdles = plan['grid']['exit_ibs_threshold'], plan['grid']['entry_ibs_threshold']
    by = {(c['asset'], c['exit_ibs_threshold'], c['entry_ibs_threshold']): c for c in r['configs'].values()}
    rows, edges = [], []
    for c in r['configs'].values():
        for k in (1, 2, 3):
            z = c['scenarios'][str(k)]
            rows.append({'configuration': c['name'], 'asset': c['asset'], 'exit_ibs_threshold': c['exit_ibs_threshold'], 'entry_ibs_threshold': c['entry_ibs_threshold'], 'cost_multiplier': k, 'net_return_pct': z['net_return_pct'], 'max_drawdown_1m_sampled_pct': z['max_drawdown_1m_sampled_pct'], 'daily_sharpe_annualized': z['daily_sharpe_annualized'], 'calmar_daily_sampled': z['calmar_daily_sampled'], 'cost_usdt': z['cost_usdt'], 'cost_pct_initial_capital': float(z['cost_usdt']) / 20, 'gross_reference_pnl_to_cost': z['gross_reference_pnl_to_cost'], 'round_trips': z['round_trips'], 'local_3x_positive_fraction': c['sensitivity']['local_3x_neighbor_positive_fraction'], 'status': c['status']})
    for asset in ('BTC', 'ETH'):
        for i, look in enumerate(looks):
            for j, hurdle in enumerate(hurdles):
                c = by[asset, look, hurdle]
                for ii, jj, axis in [(i + 1, j, 'exit_ibs_threshold'), (i, j + 1, 'entry_ibs_threshold')]:
                    if ii >= len(looks) or jj >= len(hurdles): continue
                    other = by[asset, looks[ii], hurdles[jj]]
                    a, b = c['scenarios']['3']['daily_sharpe_annualized'], other['scenarios']['3']['daily_sharpe_annualized']
                    if a is not None and b is not None: edges.append({'from': c['name'], 'to': other['name'], 'axis': axis, 'absolute_3x_Sharpe_difference': abs(a - b)})
    threshold = 2 * float(np.std([e['absolute_3x_Sharpe_difference'] for e in edges], ddof=1)) if len(edges) > 1 else None
    r['sensitivity_cliffs'] = {'heuristic': 'Adjacent absolute3x daily-Sharpe difference >2 sample SD of adjacent differences; descriptive only.', 'threshold': threshold, 'edges': [{**e, 'flagged': threshold is not None and e['absolute_3x_Sharpe_difference'] > threshold} for e in edges]}
    r['grid_boundary_note']='All boundary cells retained; a boundary maximum is descriptive, not a reason for OOS-selected extension or independent validation claims.'
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
        ax.set(xticks=range(3), xticklabels=[f'{h:g}' for h in hurdles], yticks=range(3), yticklabels=looks, xlabel='Entry IBS threshold', ylabel='Exit IBS threshold', title=f'{asset}: 3x cost net return')
        for i in range(3):
            for j in range(3): ax.text(j, i, f'{values[i,j]:+.2f}%', ha='center', va='center')
    fig.colorbar(im, ax=axes, label='Net return %', shrink=.8); fig.savefig(R / 'sensitivity_surface.png', dpi=140); plt.close(fig)
    s = r['summary']; best = r['configs'][s['ranked_by_1x_net_return'][0]]; a, b, z = [best['scenarios'][str(k)] for k in (1, 2, 3)]
    lines = ['# BTC/ETH 日线IBS收盘区间均值回归：预登记历史回测', '',
        f"轮次 `{R.name}`；冻结UTC `{plan['frozen_at_utc']}`。18个具体配置先reserve，后执行54个成本场景；所有结果包括负收益永久保留。", '',
        '## 经济假设与完整规则', '',
        '检验日内收盘靠近低点后，能否通过后续反弹覆盖成本。UTC日H/L/最后C取1440闭合分钟极值和最后收盘。IBS=(C−L)/(H−L)，H=L设0.5；只用一根完整日线，不需要递推种子、成交量加权、RSI或趋势过滤。精确Fraction从日聚合Float64十进制字符串计算，阈值不舍入；Decimal60仅显示，决策存规范比率SHA，会计Decimal28不变。空仓仅IBS<E入场；持仓仅IBS>X退出，等于入场阈值保持现金，等于退出阈值保持多头，无前置穿越要求。定义及零振幅0.5约定已核对[QuantConnect LEAN原实现](https://raw.githubusercontent.com/QuantConnect/Lean/master/Indicators/InternalBarStrength.cs)与[官方指标文档](https://www.quantconnect.com/docs/v2/writing-algorithms/indicators/supported-indicators/internal-bar-strength)；不安装库或复制源码，不声称小数库逐位等价或来源背书盈利。IBS忽略前收盘缺口并依赖UTC日边界，不代表真实主动资金流。',
        'BTC、ETH每配置独立2,000 USDT现货账户，原始资产资金占比1，不归一化、不跨币转账。预设资产×退出IBS{0.6,0.7,0.8}×入场IBS{0.1,0.2,0.3}，一根日线周期和零振幅中性0.5固定。仅闭合日线信号，60秒后下一UTC日00:01分钟开盘参考成交；终点计成本清仓。无趋势过滤、杠杆、做空、借币、加仓、持仓期限或现金收益。区别于多日RSI回撤和成交量CMF强势入场，本轮为单日位置低入高出的反转规则。',
        '## 三项验证', '',
        '- Walk-forward：真实Binance归档1分钟数据，输入2024-09-16至2026-09-16，OOS为2025-09-19 00:01至2026-09-14 00:01 UTC，360天；365日上下文及3日初始间隔，12连续30日窗，账户跨折连续。IBS只用当时完整日HLC，无未来填充、递推种子、拟合标签、OOS选参或折重置，标签purge不适用。逐折收益及日采样回撤保留；整体回撤来自初始本金及完整OOS分钟收盘/成交后参考标记，不包含分钟内极值。',
        '- 敏感性：同时变化入场和退出阈值；同资产相邻索引3×3邻域含中心。逐格收益、整体回撤、Sharpe、Calmar、邻域盈利比例在sensitivity.csv，完整表面在sensitivity_surface.png。相邻Sharpe突变仅作描述，不是显著性或独立验证。',
        '- 成本：每侧手续费10bp、估算半价差1bp、滑点2bp，加0.5×前20个完整日样本波动率×sqrt(订单预算/前20日quote ADV)冲击，参与率≤0.1%；全部项同时施加1/2/3倍压力。Decimal价格tick、数量步长、名义额和前置5分钟VWAP代理检查；冻结过滤器与本轮公开查询比较一致。历史L2、历史过滤器和真实IOC成交不可得。现货无空头，资金费及借币约束不适用。成本占比与毛参考盈亏/成本比均保留；成本加回不是独立零成本策略或相对持有alpha。', '',
        '## 实际结果', '',
        f"- 18配置通过{s['passed']}、淘汰{s['rejected']}。1/2/3倍净正数量为{s['positive_configs_by_cost']['1']}/{s['positive_configs_by_cost']['2']}/{s['positive_configs_by_cost']['3']}；三倍净正比例{s['global_3x_positive_neighbor_fraction']:.1%}，三倍Sharpe正比例{r['positive_sharpe_3x_fraction']:.1%}。",
        f"- 1倍收益最高的`{best['name']}`：1/2/3倍{a['net_return_pct']:+.4f}%/{b['net_return_pct']:+.4f}%/{z['net_return_pct']:+.4f}%，1倍正折{a['positive_folds']}/12、往返{a['round_trips']}次，3倍整体回撤{z['max_drawdown_1m_sampled_pct']:.4f}%，局部三倍盈利比例{best['sensitivity']['local_3x_neighbor_positive_fraction']:.1%}。",
        '- 冻结门槛要求所有成本净正、1倍至少8/12盈利折、三倍回撤≤25%、邻域三倍正收益≥60%、至少8次往返、1倍毛参考盈亏/成本≥2.5、无容量/过滤器拒单且终点平仓。逐项失败见report.json的gates/failure_counts，未依据结果放宽。同期持有基准只读复用20261014T084051Z原报告，现金基准0；优于基准不替代门槛。', '',
        '|配置|资产|退出阈值|入场阈值|1倍|2倍|3倍|1倍正折|3倍回撤|往返|3倍邻域正比|状态|', '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
    for name in s['ranked_by_1x_net_return']:
        c = r['configs'][name]; x, y, z = [c['scenarios'][str(k)] for k in (1, 2, 3)]
        lines.append(f"|{name}|{c['asset']}|{c['exit_ibs_threshold']}|{c['entry_ibs_threshold']:g}|{x['net_return_pct']:+.3f}%|{y['net_return_pct']:+.3f}%|{z['net_return_pct']:+.3f}%|{x['positive_folds']}/12|{z['max_drawdown_1m_sampled_pct']:.3f}%|{x['round_trips']}|{c['sensitivity']['local_3x_neighbor_positive_fraction']:.0%}|{c['status']}|")
    lines += ['', '## 局限、连续账户与复现', '',
        f"计算前读取完整登记及片段共{context['registry_events']}事件、{context['registry_ids']}登记ID，排除观察并合并等价定义后为{context['canonical_research_definitions_excluding_observations']}个既往研究定义，本轮新增18；初始16项已有真实结果，无待补项。",
        '2025–2026历史反复用于策略研发，本轮不是未触碰最终留出；存在多重比较与选择偏差，没有DSR/PBO或稳定实盘盈利结论。指标边界自检只验证公式，不当作行情回测证据。',
        '原SMA冻结账户按原现金、数量、desired及成本继续分钟估值，独立说明见forward_result.md；paper10的冻结计划、账户状态和观察由独立任务维护，本轮只读、不重置、不补单。',
        f"实际重放与独立信号/时序、余额、完整分钟回撤核验见verification.json。离线复核：`/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/{R.name}/run.py verify`。输入SHA、代码与产物哈希见data_manifest.json；已finish报告原字节与登记SHA优先，核验后只清理可重建checkpoint及本轮字节码。", '']
    (R / 'result.md').write_text('\n'.join(lines))
    print(json.dumps({'summary': s, 'failure_counts': r['failure_counts']}, ensure_ascii=False))

if __name__ == '__main__': main()
