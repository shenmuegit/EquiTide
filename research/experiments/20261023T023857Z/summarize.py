"""Render every registered rolling-median result, without selecting parameters."""
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
    commands=json.loads((R/'research_commands.json').read_text());r['evaluation_started_utc']=commands[0]['started_utc']
    import hashlib
    root=R.parents[2];ref=root/r['benchmark_read_only']['source_report'];r['benchmark_read_only']['source_report_sha256']=hashlib.sha256(ref.read_bytes()).hexdigest()
    r['signal_arithmetic']='Exact Fraction from completed daily Float64decimal-string closes/base volumes;canonical ratioSHA,Decimal60 display only;accountingDecimal28 unchanged'
    for cfg in r['configs'].values():
        for scene in cfg['scenarios'].values():
            scene['executions']=scene['filled_orders']
            for fold in scene['folds']:fold['max_drawdown_pct']=fold['daily_sample_drawdown_pct'];fold['drawdown_scope']='Daily boundary NAV samples,not full minute fold extrema'
    r['fold_drawdown_scope']='Per-fold daily boundary NAV;whole-OOS drawdown uses all minute-close/post-fill marks and initial capital'
    looks, hurdles = plan['grid']['lookback_days'], plan['grid']['entry_hurdle_pct']
    by = {(c['asset'], c['lookback_days'], c['entry_hurdle_pct']): c for c in r['configs'].values()}
    rows, edges = [], []
    for c in r['configs'].values():
        for k in (1, 2, 3):
            z = c['scenarios'][str(k)]
            rows.append({'configuration': c['name'], 'asset': c['asset'], 'lookback_days': c['lookback_days'], 'entry_band_fraction': c['entry_hurdle_pct'] / 100, 'cost_multiplier': k, 'net_return_pct': z['net_return_pct'], 'max_drawdown_1m_sampled_pct': z['max_drawdown_1m_sampled_pct'], 'daily_sharpe_annualized': z['daily_sharpe_annualized'], 'calmar_daily_sampled': z['calmar_daily_sampled'], 'cost_usdt': z['cost_usdt'], 'cost_pct_initial_capital': float(z['cost_usdt']) / 20, 'gross_reference_pnl_to_cost': z['gross_reference_pnl_to_cost'], 'round_trips': z['round_trips'], 'local_3x_positive_fraction': c['sensitivity']['local_3x_neighbor_positive_fraction'], 'status': c['status']})
    for asset in ('BTC', 'ETH'):
        for i, look in enumerate(looks):
            for j, hurdle in enumerate(hurdles):
                c = by[asset, look, hurdle]
                for ii, jj, axis in [(i + 1, j, 'lookback_days'), (i, j + 1, 'entry_band_fraction')]:
                    if ii >= len(looks) or jj >= len(hurdles): continue
                    other = by[asset, looks[ii], hurdles[jj]]
                    a, b = c['scenarios']['3']['daily_sharpe_annualized'], other['scenarios']['3']['daily_sharpe_annualized']
                    if a is not None and b is not None: edges.append({'from': c['name'], 'to': other['name'], 'axis': axis, 'absolute_3x_Sharpe_difference': abs(a - b)})
    threshold = 2 * float(np.std([e['absolute_3x_Sharpe_difference'] for e in edges], ddof=1)) if len(edges) > 1 else None
    r['sensitivity_cliffs'] = {'heuristic': 'Adjacent absolute3x daily-Sharpe difference >2 sample SD of adjacent differences; descriptive only.', 'threshold': threshold, 'edges': [{**e, 'flagged': threshold is not None and e['absolute_3x_Sharpe_difference'] > threshold} for e in edges]}
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
        ax.set(xticks=range(3), xticklabels=[f'{h/100:g}' for h in hurdles], yticks=range(3), yticklabels=looks, xlabel='Symmetric VWMA band (fraction)', ylabel='Lookback days', title=f'{asset}: 3x cost net return')
        for i in range(3):
            for j in range(3): ax.text(j, i, f'{values[i,j]:+.2f}%', ha='center', va='center')
    fig.colorbar(im, ax=axes, label='Net return %', shrink=.8); fig.savefig(R / 'sensitivity_surface.png', dpi=140); plt.close(fig)
    s = r['summary']; best = r['configs'][s['ranked_by_1x_net_return'][0]]; a, b, z = [best['scenarios'][str(k)] for k in (1, 2, 3)]
    lines=['# BTC/ETH日线成交量加权均线与对称价格缓冲：预登记回测','',
        f"轮次`{R.name}`，冻结UTC`{plan['frozen_at_utc']}`，计划SHA256`{r['frozen_plan_sha256']}`。18项具体配置先reserve，再实际评估54个成本场景；正负收益、逐折和所有事件都保存。",'',
        '## 规则、资本与数据','',
        '检验高成交量日的收盘价具有更大权重后，趋势锚能否减少噪声并覆盖执行成本。VWMA_L[j]=Σ(C_i×V_i)/ΣV_i，i=j−L+1..j，C为已闭合UTC日最后分钟收盘，V为该日1440个闭合分钟的基币成交量之和。包含信号日j。它是成交量加权的日收盘均值，不是实际日成交VWAP或主动买卖流。公式参考[LEAN原始实现](https://raw.githubusercontent.com/QuantConnect/Lean/master/Indicators/VolumeWeightedMovingAverage.cs)与[官方指标文档](https://www.quantconnect.com/docs/v2/writing-algorithms/indicators/supported-indicators/volume-weighted-moving-average)，查阅2026-10-23；交易假设与参数独立冻结，不是文档背书的盈利策略。',
        '每日聚合价格/基币量先按既有引擎编码为Float64最短十进制串，特征用Fraction精确有理数递推，保存规范分子/分母SHA；Decimal60仅显示，不能用显示值或浮点阈值调仓。账本仍用原Decimal28。需要L个已闭合日，不填未来；窗口成交量全零时保持实际持仓/现金，不下单。独立整数缩放＋前缀和重建全部参考比率，和生产滚动Fraction实现分开核对。',
        '空仓在C_j>VWMA×(1+b)时入场；持仓在C_j<VWMA×(1−b)时退出，均严格比较，等值/缓冲内保持实际状态。L={20,40,80}日×b={0.5%,1%,2%}，BTC/ETH各9项。每配置独立2,000USDT单币现货现金账户，原始资金占比1，不合并成4000USDT回测、不归一化资金权重、不跨币转账。成交量除以总量只属于指标均值公式。无杠杆、做空、借币、加仓或现金收益。信号可得60秒后下一日00:01一分钟开盘参考执行，终点计成本清仓。',
        '真实Binance归档1分钟行情，四个Parquet输入SHA及ns单位、可得时刻、收盘状态、连续性核对。输入2024-09-16至2026-09-16，每币1,051,200分钟/730完整日，所有原始大行情仍在忽略data。只读持有基准复用既有2000USDT同窗报告，未重算。', '',
        '## 三项验证','',
        '- Walk-forward：365日上下文及3日初始间隔；固定OOS为2025-09-19 00:01至2026-09-14 00:01UTC，360日、12连续30日折，账户跨折连续。无拟合和未来收益标签，purge不适用；没有按当前OOS挑选后再称独立测试。逐折收益与日边界采样回撤保存，整体回撤用初始本金、所有OOS闭合分钟收盘NAV及成交后参考标记计算，包括终点成本，不含分钟内极值。',
        '- 敏感性：预设L×b二维3×3，每币相邻索引邻域含中心；保留全部变体净收益、分钟整体DD、日Sharpe、日Calmar和邻域3倍盈利比例，以及完整热图。相邻Sharpe差超2样本标准差仅作陡变描述，不是显著性检验。边界格不触发本轮OOS择优加格。',
        '- 成本：单侧手续费10bp、估算半价差1bp、滑点2bp，加0.5×前20完整UTC日log收益样本波动×sqrt(订单预算/前20日quote ADV)冲击，参与率≤0.1%，全部项按1/2/3倍压力。保留tick/lot、不利取整、名义额及前置分钟VWAP代理过滤；Oct14冻结交易规则代理与当前公开响应一致。真实历史L2、历史过滤器和IOC成交不可得。现货无永续资金费或空头借币；本轮不构造空头。',
        '冻结门槛：所有成本净正、1倍至少8/12正折、3倍完整分钟DD≤25%、相邻3倍净正≥60%、1倍至少8往返、毛参考盈亏/总模型成本≥2.5、无容量/规则拒单、终点空仓。成本加回是毛参考盈亏，不是独立零成本反事实或相对持有alpha。', '',
        '## 实际结果','',
        f"18项通过{s['passed']}、淘汰{s['rejected']}；1/2/3倍净正数{s['positive_configs_by_cost']['1']}/{s['positive_configs_by_cost']['2']}/{s['positive_configs_by_cost']['3']}，3倍净正比例{s['global_3x_positive_neighbor_fraction']:.1%}、3倍Sharpe正比例{r['positive_sharpe_3x_fraction']:.1%}。",'',
        f"1倍收益最高`{best['name']}`：三成本{a['net_return_pct']:+.4f}%/{b['net_return_pct']:+.4f}%/{z['net_return_pct']:+.4f}%，1倍正折{a['positive_folds']}/12、往返{a['round_trips']}，3倍分钟整体DD{z['max_drawdown_1m_sampled_pct']:.4f}%，邻域3倍正比{best['sensitivity']['local_3x_neighbor_positive_fraction']:.1%}。",'',
        '|配置|L|缓冲|1倍|2倍|3倍|1倍正折|往返|3倍分钟DD|邻域3倍正比|结论|','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
    for name in s['ranked_by_1x_net_return']:
        c=r['configs'][name];x,y,z=[c['scenarios'][str(k)] for k in (1,2,3)];lines.append(f"|{name}|{c['lookback_days']}|{c['entry_hurdle_pct']}%|{x['net_return_pct']:+.3f}%|{y['net_return_pct']:+.3f}%|{z['net_return_pct']:+.3f}%|{x['positive_folds']}/12|{x['round_trips']}|{z['max_drawdown_1m_sampled_pct']:.3f}%|{c['sensitivity']['local_3x_neighbor_positive_fraction']:.0%}|{c['status']}|")
    lines+=['','逐项失败：`'+json.dumps(r['failure_counts'],ensure_ascii=False)+'`。','','## 只读对照、限制与下轮状态','',
        f"同期持有基准只读来源`{r['benchmark_read_only']['source_report']}`，SHA256`{r['benchmark_read_only']['source_report_sha256']}`；每币各2000USDT，原收益/费用/分钟DD不改，现金解析参考0。",'',
        '|只读持有资产|1倍|2倍|3倍|3倍分钟DD|','|---|---:|---:|---:|---:|']
    for asset,ss in r['benchmark_read_only']['same_OOS_period_buy_hold'].items():
        x,y,z=[ss[str(k)] for k in (1,2,3)];lines.append(f"|{asset}|{x['net_return_pct']:+.3f}%|{y['net_return_pct']:+.3f}%|{z['net_return_pct']:+.3f}%|{z['max_drawdown_pct']:.3f}%|")
    lines+=['',f"计算前完整登记{context['registry_events']}事件、{context['registry_ids']}ID、{context['canonical_research_definitions_excluding_observations']}个规范研究定义及{len(context['prior_conclusions_read'])}份既往结论已读；初始16项实际证据完整，无待补回测。本轮18项新信号配置与旧SMA/EMA/中位数/成交量比过滤不同，未因改名或改来源制造新颖性。",'',
        '2025–2026历史已反复用于研发，存在多重选择偏差；本轮不是未触碰最终留出，未计算DSR/PBO，没有稳定实盘盈利结论。缺真实历史L2/TCA与成交校准。指标有理数“精确”仅指给定日聚合Float64十进制编码，不是原始交易序列无损或与LEAN Decimal库逐位相同。', '',
        '原冻结SMA从00:30续至02:30UTC，仅追加120闭合分钟估值，无日决策/参考点/新成交，现金/数量/desired/成本与旧NAV前缀保持。下一日事件Oct24 00:01，长期计划及原75/25资金不变；见forward_result.md。21日partial不是180日/六折资格，rejected观察不取消计划。paper10真实公开报价模拟账户与本轮独立，计划/状态只读。', '',
        f"实际完整重放、独立整数VWMA/时序、余额/成本及54条完整分钟DD核验见verification.json。只读复核：`PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/{R.name}/run.py verify`。完整结果分布于report.json、逐折/成本CSV、daily_equity/trades/decisions.csv.gz及同哈希原始分钟，可重建全部分钟NAV并核对SHA；不提交可重建大分钟曲线。已finish报告原字节与登记SHA优先，只核验后清理重复checkpoint及缓存。",'']
    (R/'result.md').write_text('\n'.join(lines));print(json.dumps({'summary':s,'failure_counts':r['failure_counts']},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
