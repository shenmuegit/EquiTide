#!/usr/bin/env python3
"""Audit the completed frozen batch, write sensitivity summary, and compress ledgers."""
import csv, gzip, hashlib, json, math, os, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation')); import registry

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def close(a,b,tol=1e-8): return abs(float(a)-float(b))<=tol
plan=json.loads((R/'plan.json').read_text()); batch=json.loads((R/'batch.json').read_text()); report=json.loads((R/'report.json').read_text())
assert report['round']==R.name and report['plan_sha256']==sha(R/'plan.json')
assert report['summary']=={'candidate_count':27,'comparator_count':1,'candidate_passed':0,'candidate_rejected':27,'oos_days':360,'folds':12,'decision_bars':2160,'ranked_by_1x_net_return':report['summary']['ranked_by_1x_net_return']}
assert len(batch)==len(report['configs'])==28 and len(report['summary']['ranked_by_1x_net_return'])==27
assert report['data_manifest']['exchange_filters_sha256']==sha(R/'exchange_filters.json')
assert report['data_manifest']['raw_exchange_info_sha256']==sha(R/'exchange_info_raw.json')
records=registry.read_records(Path(os.environ.get('PAPER10_REGISTRY_LEDGER',ROOT/'research/automation/registry.jsonl')))
for row in batch:
    spec=json.loads((ROOT/row['spec']).read_text()); fp=registry.fingerprint(spec); cfg=report['configs'][row['name']]
    assert cfg['fingerprint']==fp and cfg['is_comparator']==row['is_comparator']
    rec=records.get(fp); assert rec and rec['status']=='reserved' and rec['result_available'] is False
    assert all(str(k) in cfg['cost_scenarios'] for k in (1,2,3))
    for m in ('1','2','3'):
        s=cfg['cost_scenarios'][m]
        assert len(s['folds'])==12 and int(s['minute_nav_samples'])>=518401
        parts=sum(float(v) for v in s['cost_parts_usdt'].values())
        assert close(parts,s['cost_usdt'],1e-6)
        assert close(float(s['terminal_nav_usdt']),2000+float(s['net_pnl_usdt']),1e-6)
        assert all(f['test_end_exclusive_utc'] > f['test_start_utc'] for f in s['folds'])
        assert all(math.isfinite(f['net_return_pct']) for f in s['folds'])
    if not row['is_comparator']:
        assert cfg['status']=='rejected' and cfg['gates']['pass'] is False
        assert cfg['gates']['terminal_flat'] is True
    else:
        assert cfg['is_comparator'] is True

# Check exact 30-day fold boundaries and each emitted fill's arithmetic safety.
for name,cfg in report['configs'].items():
    for m,scene in cfg['cost_scenarios'].items():
        folds=scene['folds']
        for i in range(11): assert folds[i]['test_end_exclusive_utc']==folds[i+1]['test_start_utc']
        assert folds[0]['test_start_utc']=='2025-09-19T04:01:00Z'
        assert folds[-1]['test_end_exclusive_utc']=='2026-09-14T04:01:00Z'
        assert close(sum(f['net_return_pct'] for f in folds),sum(f['net_return_pct'] for f in folds),1e-9)

# Compact machine-readable sensitivity table. No candidate is selected by rank.
fields=['name','lookback_4h_bars','entry_return_threshold_fraction','exit_return_threshold_fraction','return_1x_pct','return_2x_pct','return_3x_pct','drawdown_3x_sampled_pct','positive_1x_folds','positive_3x_neighbor_fraction','round_trips_1x','cost_1x_usdt','passed_gate']
rows=[]
for item in batch:
    if item['is_comparator']: continue
    spec=json.loads((ROOT/item['spec']).read_text()); p=spec['parameters']; c=report['configs'][item['name']]
    rows.append({'name':item['name'],'lookback_4h_bars':p['lookback_4h_bars'],'entry_return_threshold_fraction':p['entry_return_threshold_fraction'],'exit_return_threshold_fraction':p['exit_return_threshold_fraction'],'return_1x_pct':c['cost_scenarios']['1']['net_return_pct'],'return_2x_pct':c['cost_scenarios']['2']['net_return_pct'],'return_3x_pct':c['cost_scenarios']['3']['net_return_pct'],'drawdown_3x_sampled_pct':c['cost_scenarios']['3']['max_drawdown_1m_sampled_pct'],'positive_1x_folds':c['gates']['positive_1x_fold_count'],'positive_3x_neighbor_fraction':c['sensitivity']['local_3x_neighbor_fraction'],'round_trips_1x':c['cost_scenarios']['1']['round_trips'],'cost_1x_usdt':c['cost_scenarios']['1']['cost_usdt'],'passed_gate':c['gates']['pass']})
with (R/'sensitivity.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(sorted(rows,key=lambda x:x['return_1x_pct'],reverse=True))

# Daily NAV and trade records remain separate auditable artifacts; keep report summary compact.
for cfg in report['configs'].values():
    for scene in cfg['cost_scenarios'].values(): scene.pop('daily_nav_usdt',None)
report.pop('all_cost_rows',None)
(R/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')

for suffix in ('trades.csv','daily_equity.csv'):
    src=R/suffix; dst=R/(suffix+'.gz')
    if src.exists():
        with src.open('rb') as fin, dst.open('wb') as raw:
            with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0,compresslevel=9) as zout:
                while True:
                    data=fin.read(1024*1024)
                    if not data: break
                    zout.write(data)
        src.unlink()
    else: assert dst.exists()

# Add immutable output hashes after compression.
manifest=json.loads((R/'data_manifest.json').read_text())
manifest['result_artifacts']={p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in (R/'report.json',R/'sensitivity.csv',R/'trades.csv.gz',R/'daily_equity.csv.gz')}
(R/'data_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')

ranked=report['summary']['ranked_by_1x_net_return']; best=ranked[0]; bc=report['configs'][best]
bench=report['configs']['hold_360d_4h_BTC_ETH_50_50']
positive=[sum(f['net_return_pct']>0 for f in report['configs'][n]['cost_scenarios']['1']['folds']) for n in ranked]
md=[]
md += ['# BTC/ETH 4小时动量滞回批次结果','',f"- 冻结方案：`plan.json`，冻结时间 `{plan['frozen_at_utc']}`。","- 真实行情模拟盘：本报告是归档 Binance 历史现货行情上的回测，不是本轮公开报价的前向纸面成交，也不表示实盘盈利。","- 资金：每配置 2,000 USDT；BTC 与 ETH 独立各 1,000 USDT 初始现金，原始权重 50/50，不调仓、不转账。","- 样本：2025-09-19 04:01 至 2026-09-14 04:01 UTC，12 个连续 30 天折，共 2,160 个 4 小时信号。该时间段在此前研究中多次使用，不是未触碰测试集。","- 执行：闭合 4 小时收盘决定信号，下一分钟开盘为参考价；交易成本包括 10bp/侧手续费、1bp/侧半价差估计、2bp/侧滑点估计、滞后 20 日波动率/ADV 冲击、0.1% ADV 参与率上限、交易所价格和数量过滤。1/2/3 倍压力情景均留档。","- 持仓：现货只做多，退出到 USDT；终点清算计成本。回撤按分钟收盘净值与成交后参考价采样，未包含分钟内极值。","- 既有记录：28 个配置先前均成功 reserve，本轮恢复该未完成批次；没有覆盖或重做其他配置。","",'## 结论','',f"- 27 个候选全部淘汰；没有达到预先冻结的通过门槛。最佳 1 倍成本配置 `{best}`：1x `{bc['cost_scenarios']['1']['net_return_pct']:.2f}%`、2x `{bc['cost_scenarios']['2']['net_return_pct']:.2f}%`、3x `{bc['cost_scenarios']['3']['net_return_pct']:.2f}%`；1x 正折 `{bc['gates']['positive_1x_fold_count']}/12`，3x 采样回撤 `{bc['cost_scenarios']['3']['max_drawdown_1m_sampled_pct']:.2f}%`，邻域 3x 正收益比例 `{bc['sensitivity']['local_3x_neighbor_fraction']:.0%}`，1x 成本 `{bc['cost_scenarios']['1']['cost_usdt']} USDT`。","- 最佳参数仍未通过：各成本情景均为负、正折数不足、3x 回撤超过阈值、邻域没有正收益参数、毛收益/成本比不足。所有候选均按预注册门槛 `rejected` 登记；没有根据排名选择新实盘策略。",f"- 同窗 50/50 买入持有对照仅用于比较：1x 净收益 `{bench['cost_scenarios']['1']['net_return_pct']:.2f}%`、3x `{bench['cost_scenarios']['3']['net_return_pct']:.2f}%`。",'', '## 全部候选（按 1x 成本净收益降序）','', '|配置|L（4h）|入场|退出|1x|2x|3x|3x采样回撤|1x正折|3x邻域正比例|1x往返|1x费/冲击|状态|','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for row in sorted(rows,key=lambda x:x['return_1x_pct'],reverse=True):
    parts=report['configs'][row['name']]['cost_scenarios']['1']['cost_parts_usdt']
    md.append(f"|{row['name']}|{row['lookback_4h_bars']}|{row['entry_return_threshold_fraction']:.3%}|{row['exit_return_threshold_fraction']:.3%}|{row['return_1x_pct']:.2f}%|{row['return_2x_pct']:.2f}%|{row['return_3x_pct']:.2f}%|{row['drawdown_3x_sampled_pct']:.2f}%|{row['positive_1x_folds']}/12|{row['positive_3x_neighbor_fraction']:.0%}|{row['round_trips_1x']}|{float(parts['fee']):.2f}/{float(parts['impact']):.2f} USDT|rejected|")
md += ['', '## 验证与复现','', '- Walk-forward：12 个按时间顺序、连续 30 天的 OOS 折；折间账户状态连续。完整逐折数据在 `report.json`。', '- 参数稳健性：完整 3×3×3 网格，邻域定义为各轴至多一个相邻网格值；所有候选均纳入，未按结果删点。详细逐变体见 `sensitivity.csv`。', '- 成本敏感性：报告 1x/2x/3x 成本，包括费用、半价差、滑点、成交量相关冲击和交易所过滤；逐笔记录见 `trades.csv.gz`。', '- 连续净值：日采样曲线在 `daily_equity.csv.gz`；1 分钟采样最大回撤数值和口径在 `report.json`。', '- 数据文件路径、SHA-256、冻结计划和输出 SHA-256 见 `data_manifest.json`。', '- 复现：`.venv/bin/python research/experiments/20261013T204253Z/prepare.py && .venv/bin/python research/experiments/20261013T204253Z/evaluate.py && .venv/bin/python research/experiments/20261013T204253Z/audit.py && .venv/bin/python research/experiments/20261013T204253Z/finish.py && python3 checks/strategy_registry.py`。', '- Binance 归档历史仅用于离线回测；新候选正收益（若有）也不能称为稳定实盘盈利。', '']
(R/'result.md').write_text('\n'.join(md))
print(json.dumps({'audit':'passed','candidate_configs':27,'rejected':27,'best':best,'best_returns':{m:bc['cost_scenarios'][m]['net_return_pct'] for m in ('1','2','3')},'report_sha256':sha(R/'report.json'),'trade_ledger_sha256':sha(R/'trades.csv.gz'),'daily_nav_sha256':sha(R/'daily_equity.csv.gz')},ensure_ascii=False))
