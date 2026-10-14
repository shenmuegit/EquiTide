#!/usr/bin/env python3
"""Independent ledger and reservation checks; publish compact sensitivity evidence."""
import ast,csv,gzip,hashlib,json,math,os,sys
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def close(a,b,tol=D('1e-7')):return abs(D(str(a))-D(str(b)))<=tol
def clean(x):return json.loads(json.dumps(x,default=str,ensure_ascii=False,allow_nan=False))
batch=json.loads((R/'batch.json').read_text());report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text())
assert len(batch)==9 and len(report['configs'])==9 and report['plan_sha256']==sha(R/'plan.json')
records=registry.read_records(Path(os.environ.get('VOLMANAGED_REGISTRY_LEDGER',ROOT/'research/automation/registry.jsonl')))
for row in batch:
 spec=json.loads((ROOT/row['spec']).read_text());fp=registry.fingerprint(spec);rec=records.get(fp)
 assert report['configs'][row['name']]['fingerprint']==fp
 assert rec and rec['status']=='reserved' and rec['result_available'] is False,(row['name'],rec)
 cfg=report['configs'][row['name']]
 for mult in ('1','2','3'):
  s=cfg['cost_scenarios'][mult];assert len(s['folds'])==12
  for i,f in enumerate(s['folds']):
   assert math.isfinite(f['net_return_pct']) and f['end_exclusive_utc']>f['start_utc']
   if i<11:assert f['end_exclusive_utc']==s['folds'][i+1]['start_utc']
  parts=sum((D(str(v)) for v in s['cost_parts_usdt'].values()),D(0));assert close(parts,s['cost_usdt'])
  assert close(D(s['terminal_nav_usdt']),D(2000)+D(s['net_pnl_usdt']))
  assert all(D(x)==0 for x in s['terminal_units_by_asset'].values())
for row in batch:
 assert len(report['configs'][row['name']]['cost_scenarios'])==3

# Replay each independent asset sleeve from its 1,000 USDT start and check every balance/cost identity.
groups={}
trades_path=R/'trades.csv' if (R/'trades.csv').exists() else R/'trades.csv.gz'
trade_open=open if trades_path.suffix=='.csv' else gzip.open
with trade_open(trades_path,'rt',newline='') as f:
 for t in csv.DictReader(f):groups.setdefault((t['configuration'],t['cost_multiplier'],t['asset']),[]).append(t)
for (name,mult,asset),rows in groups.items():
 cash=D('1000');units=D(0);costs={k:D(0) for k in ('fee','half_spread','slippage','impact','tick_rounding')};fills=0;rejects=0;skips=0
 for t in rows:
  after_cash=D(t['cash_after']);after_units=D(t['units_after']);status=t['status']
  if status=='filled':
   q=D(t['quantity']);ref=D(t['reference']);price=D(t['execution']);parts=ast.literal_eval(t['cost_parts'])
   for k in costs:costs[k]+=D(parts[k])
   fee=D(parts['fee']);assert after_cash==(cash-q*price-fee if t['side']=='buy' else cash+q*price-fee)
   assert after_units==(units+q if t['side']=='buy' else units-q)
   assert after_cash>=0 and after_units>=0
   assert abs(cash+units*ref-after_cash-after_units*ref-sum((D(parts[k]) for k in parts),D(0)))<D('1e-18')
   fills+=1
  elif status=='rejected':assert after_cash==cash and after_units==units;rejects+=1
  elif status=='skipped_below_lot':assert after_cash==cash and after_units==units;skips+=1
  else:raise AssertionError((name,mult,asset,status))
  cash,units=after_cash,after_units
 s=report['configs'][name]['cost_scenarios'][mult]['asset_sleeves'][asset]
 assert D(s['terminal_cash_usdt'])==cash and D(s['terminal_units'])==units
 assert sum(costs.values(),D(0))==D(s['cost_usdt'])
 assert fills==s['fills'] and rejects==s['rejected_orders'] and skips==s['skipped_below_lot']

# Recompute registered config/multiplier aggregates directly from per-asset reports.
for row in batch:
 cfg=report['configs'][row['name']]
 for mult in ('1','2','3'):
  sc=cfg['cost_scenarios'][mult]
  assert close(D(sc['terminal_nav_usdt']),sum((D(sc['asset_sleeves'][a]['terminal_cash_usdt'])+D(sc['asset_sleeves'][a]['terminal_units'])*D(sc['asset_sleeves'][a]['terminal_reference_price']) for a in ('BTC','ETH')),D(0)))
  assert sc['rejected_orders']==sum(sc['asset_sleeves'][a]['rejected_orders'] for a in ('BTC','ETH'))
  assert sc['fills']==sum(sc['asset_sleeves'][a]['fills'] for a in ('BTC','ETH'))

# Unbiased, fully reported 3x3 surface and per-fold data.
candidate_rows=[]
for row in batch:
 if row['role']!='candidate':continue
 s=json.loads((ROOT/row['spec']).read_text());p=s['parameters'];c=report['configs'][row['name']]
 candidate_rows.append({'name':row['name'],'lookback_days':p['realized_vol_lookback_days'],'target_annual_volatility':p['target_annual_volatility'],'return_1x_pct':c['cost_scenarios']['1']['net_return_pct'],'return_2x_pct':c['cost_scenarios']['2']['net_return_pct'],'return_3x_pct':c['cost_scenarios']['3']['net_return_pct'],'drawdown_3x_1m_sampled_pct':c['cost_scenarios']['3']['max_drawdown_1m_sampled_pct'],'daily_drawdown_3x_pct':c['cost_scenarios']['3']['daily_sample_drawdown_pct'],'positive_1x_folds':c['gates']['positive_1x_folds'],'neighbor_3x_positive_fraction':c['sensitivity']['local_3x_neighbor_positive_fraction'],'rebalances_1x':c['cost_scenarios']['1']['rebalances'],'cost_1x_usdt':c['cost_scenarios']['1']['cost_usdt'],'passed':c['status']=='passed'})
with (R/'sensitivity.csv').open('w',newline='') as f:
 fields=list(candidate_rows[0]);w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(sorted(candidate_rows,key=lambda x:x['return_1x_pct'],reverse=True))

# Self-contained SVG heatmap: each cell shows 1x and 3x cost net returns.
cell_w=210;cell_h=88;width=190+3*cell_w;height=115+3*cell_h
vals=[x['return_1x_pct'] for x in candidate_rows];lo=min(vals);hi=max(vals)
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">','<rect width="100%" height="100%" fill="#fff"/>','<text x="20" y="28" font-family="sans-serif" font-size="20" font-weight="bold">Monthly inverse-variance scaling: net return sensitivity</text>']
for j,v in enumerate((.20,.30,.40)):svg.append(f'<text x="{190+j*cell_w+cell_w/2}" y="60" text-anchor="middle" font-family="sans-serif" font-size="14">Target vol {v:.0%}</text>')
by={(r['lookback_days'],r['target_annual_volatility']):r for r in candidate_rows}
for i,l in enumerate((20,60,120)):
 svg.append(f'<text x="90" y="{115+i*cell_h+cell_h/2}" text-anchor="middle" font-family="sans-serif" font-size="14">Lookback {l}d</text>')
 for j,v in enumerate((.20,.30,.40)):
  r=by[(l,v)];z=(r['return_1x_pct']-lo)/(hi-lo) if hi>lo else .5
  red=int(244-100*z);green=int(202-110*z);blue=int(202-110*z);x=190+j*cell_w;y=75+i*cell_h
  svg.append(f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" rx="4" fill="rgb({red},{green},{blue})" stroke="#444"/>')
  svg.append(f'<text x="{x+cell_w/2}" y="{y+34}" text-anchor="middle" font-family="sans-serif" font-size="16">1x {r["return_1x_pct"]:.2f}%</text>')
  svg.append(f'<text x="{x+cell_w/2}" y="{y+60}" text-anchor="middle" font-family="sans-serif" font-size="14">3x {r["return_3x_pct"]:.2f}%</text>')
svg.append('</svg>');(R/'sensitivity_surface.svg').write_text('\n'.join(svg)+'\n')

# Preserve daily OOS NAV outside JSON as a row-addressable continuous series; compress transaction details.
for suffix in ('trades.csv','daily_equity.csv','decisions.csv'):
 src=R/suffix;dst=R/(suffix+'.gz')
 if src.exists():
  with src.open('rb') as f, dst.open('wb') as out:
   with gzip.GzipFile(filename='',mode='wb',fileobj=out,mtime=0,compresslevel=9) as gz:
    while chunk:=f.read(1024*1024):gz.write(chunk)
  src.unlink()
 else:assert dst.exists()
for cfg in report['configs'].values():
 for scene in cfg['cost_scenarios'].values():scene.pop('daily_nav_usdt',None)
(R/'report.json').write_text(json.dumps(clean(report),indent=2,ensure_ascii=False)+'\n')
manifest={'plan_sha256':sha(R/'plan.json'),'exchange_info_raw_sha256':sha(R/'exchange_info_raw.json'),'exchange_filters_sha256':sha(R/'exchange_filters.json'),'source_data':report['data_manifest']['assets'],'output_hashes':{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in [R/'report.json',R/'sensitivity.csv',R/'sensitivity_surface.svg',R/'trades.csv.gz',R/'daily_equity.csv.gz',R/'decisions.csv.gz']},'code_hashes':{'freeze.py':sha(R/'freeze.py'),'evaluate.py':sha(R/'evaluate.py'),'audit.py':sha(R/'audit.py'),'reproduce.sh':sha(R/'reproduce.sh'),'kernel.py':sha(ROOT/'research/experiments/20261001T133655Z/kernel.py')}}
(R/'data_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')

# Chinese result summary from every pre-registered variant, with no post-result parameter selection.
ranked=sorted(candidate_rows,key=lambda x:x['return_1x_pct'],reverse=True);best=ranked[0];bench=report['comparison_reference']['cost_scenarios']
lines=['# BTC/ETH 月度波动率管理 + SMA200趋势门槛：回测结果','',f"- 冻结方案：`plan.json`，冻结UTC `{plan['frozen_at_utc']}`；{len(ranked)}个候选均在查看结果前登记。",'- 本报告是 Binance 归档现货行情的历史回测，不是本轮实时行情模拟或实盘收益证明。','- 每配置2000 USDT：BTC、ETH独立初始现金袖套各1000 USDT，原始初始权重50/50；不跨袖套转账或再平衡；现金收益为0，不加杠杆、不做空。',f"- OOS：{plan['data']['start_utc']}至{plan['data']['end_exclusive_utc']}，12个连续30日折。该2025–2026窗口在仓库已反复研究，不是未触碰留出集。",'- 规则：月初参考价仅在前一已闭合日线收盘高于包含当日收盘在内最近200个完整日收盘SMA时允许持仓，否则目标现金。合格时，以过去L个已闭合日对数收益样本波动估算实现波动，目标敞口=min(1,(目标年化波动/实现年化波动)^2)，其余现金；两袖套各自独立，仅月度再平衡。',f"- 成本：每侧手续费10bp、半价差估计1bp、滑点2bp，以及前20个完整UTC日σ/quote ADV平方根冲击；最大参与率0.1%，当前交易所PRICE/LOT/NOTIONAL/PERCENT_PRICE规则。缺历史L2，全部成本同倍放大至1x/2x/3x；回撤为1分钟收盘及成交后参考点采样，不含分钟内极值。",'', '## 结果与判定','',f"- {len(ranked)}个候选全部未通过预设门槛。最佳1x累计收益配置 `{best['name']}`（L={best['lookback_days']}日、目标年化波动{best['target_annual_volatility']:.0%}）仍亏损：1x `{best['return_1x_pct']:.2f}%`、2x `{best['return_2x_pct']:.2f}%`、3x `{best['return_3x_pct']:.2f}%`；1x正折`{best['positive_1x_folds']}/12`，3x采样回撤`{best['drawdown_3x_1m_sampled_pct']:.2f}%`。",f"- 1x/2x/3x净正配置数分别为 {sum(x['return_1x_pct']>0 for x in ranked)}/{len(ranked)}、{sum(x['return_2x_pct']>0 for x in ranked)}/{len(ranked)}、{sum(x['return_3x_pct']>0 for x in ranked)}/{len(ranked)}。同窗50/50买入持有基准复用已完成的对照报告，1x `{bench['1']['net_return_pct']:.2f}%`、3x `{bench['3']['net_return_pct']:.2f}%`；本轮没有重算这个比较配置。波动率缩放+趋势门槛不能抵消该历史区间的下跌，故不保留为盈利候选。",'', '## 全部候选（按1x净收益排序）','', '|配置|L天|目标年波动|1x|2x|3x|1x/3x回撤|1x正折|1x重平衡单|1x费用/冲击USDT|邻域3x正比例|状态|','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for r in ranked:
 s=report['configs'][r['name']]['cost_scenarios']['1'];parts=s['cost_parts_usdt']
 lines.append(f"|{r['name']}|{r['lookback_days']}|{r['target_annual_volatility']:.0%}|{r['return_1x_pct']:.2f}%|{r['return_2x_pct']:.2f}%|{r['return_3x_pct']:.2f}%|{s['max_drawdown_1m_sampled_pct']:.2f}%/{r['drawdown_3x_1m_sampled_pct']:.2f}%|{r['positive_1x_folds']}/12|{r['rebalances_1x']}|{float(parts['fee']):.2f}/{float(parts['impact']):.2f}|{r['neighbor_3x_positive_fraction']:.0%}|rejected|")
lines+=['','## 三项验证与审计','', '- Walk-forward：12个连续30日历史OOS折，袖套净值跨折连续；规则没有拟合参数，lookback仅用于过去已收盘数据估计波动。完整折值与整体采样回撤见`report.json`。','- Sensitivity：冻结的3×3二维网格，所有9格均报告，不在OOS按表现改参数；相邻一个网格步长的3x邻域正收益比例列于`sensitivity.csv`。','- Costs：每个候选与基准都完成1x/2x/3x成本场景，逐项手续费、半价差、滑点、冲击和tick rounding列于`report.json`；逐笔执行/拒绝/最小名义额跳过见`trades.csv.gz`。','- 连续日净值在`daily_equity.csv.gz`，月度决策及未交易/最小名义额跳过在`decisions.csv.gz`；输入路径、哈希、交易所快照和代码哈希见`data_manifest.json`。','- 复现：`bash research/experiments/20261014T003809Z/reproduce.sh`从仓库归档数据重跑冻结计划；脚本在临时登记账本运行并恢复发布结果文件，不会改写本轮已登记证据或主registry。','- 失败门槛包括所有成本倍数净收益为正、至少8/12个1x正折、3x采样回撤不超过25%、3x邻域正比例至少60%、毛收益/成本至少2.5、零拒单且终点空仓；本批候选全部拒绝。','- 历史被重复研究且存在多重选择偏差；缩放减少回撤但不代表稳定盈利。', '']
(R/'result.md').write_text('\n'.join(lines))
print(json.dumps({'audit':'passed','candidate_count':len(ranked),'passed':sum(r['passed'] for r in ranked),'rejected':sum(not r['passed'] for r in ranked),'best':best['name'],'returns_1_2_3':[best[x] for x in ('return_1x_pct','return_2x_pct','return_3x_pct')],'report_sha256':sha(R/'report.json'),'sensitivity_variants':len(ranked)},ensure_ascii=False))
