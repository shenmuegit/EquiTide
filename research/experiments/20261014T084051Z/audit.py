#!/usr/bin/env python3
"""Independent source, causality, filter, balance, fold and sensitivity audit."""
import ast,csv,gzip,hashlib,json,math,os,sys
from datetime import datetime,timedelta,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sys.path.insert(0,str(R));import evaluate
MIN_MS=evaluate.MIN_MS;DAY_MS=evaluate.DAY_MS
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def close(a,b,tol=D('1e-8')):return abs(D(str(a))-D(str(b)))<=tol
def readcsv(path):
 if path.is_file():
  with path.open(newline='') as f:return list(csv.DictReader(f))
 with gzip.open(path.with_suffix(path.suffix+'.gz'),'rt',newline='') as f:return list(csv.DictReader(f))
def readgzjson(path):
 with gzip.open(path,'rt',encoding='utf-8') as f:return json.load(f)
def writecsv(path,rows):
 with path.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def write_json(path,obj):path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());report=json.loads((R/'report.json').read_text())
assert len(batch)==18 and len(report['configs'])==18 and report['plan_sha256']==sha(R/'plan.json')
ledger=Path(os.environ.get('EMA_CROSS_REGISTRY_LEDGER',ROOT/'research/automation/registry.jsonl'));events=registry.read_events(ledger);records=registry.read_records(ledger)
reserved={x['fingerprint'] for x in events if x.get('status')=='reserved' and x.get('result_available') is False}
ex=json.loads((R/'exchange_filters.json').read_text());assert ex['raw_sha256']==plan['exchange_rules']['raw_sha256']==sha(R/'exchange_info_raw.json')
exchange=json.loads((R/'exchange_info_raw.json').read_text());assert {x['symbol'] for x in exchange['symbols']}=={'BTCUSDT','ETHUSDT'}
filters=ex['filters'];markets={a:evaluate.load_asset(a,plan) for a in ('BTC','ETH')};
for a in ('BTC','ETH'):
 sym=next(x for x in exchange['symbols'] if x['symbol']==a+'USDT');assert sym['status']=='TRADING' and sym.get('isSpotTradingAllowed',True)
 assert sha(R/'exchange_info_raw.json')==ex['raw_sha256']
for a,meta in report['data_manifest']['assets'].items():
 assert [x['sha256'] for x in meta['source_files']]==[x['sha256'] for x in markets[a]['files']]
batch_by={x['name']:x for x in batch};scenarios={};trades=readcsv(R/'trades.csv');decisions=readcsv(R/'decisions.csv');daily_rows=readcsv(R/'daily_equity.csv');daily_expected=[]
trade_groups={};decision_groups={}
for t in trades:trade_groups.setdefault((t['configuration'],t['cost_multiplier'],t['asset']),[]).append(t)
for d in decisions:decision_groups.setdefault((d['configuration'],d['cost_multiplier'],d['asset']),[]).append(d)
assert len({x['trade_id'] for x in trades})==len(trades)
replays=0
for item in batch:
 spec=json.loads((ROOT/item['spec']).read_text());fp=registry.fingerprint(spec);rec=records[fp]
 assert fp==item['fingerprint']==report['configs'][item['name']]['fingerprint'] and fp in reserved
 if rec['status']=='reserved':assert rec['result_available'] is False
 else:assert rec['status']=='rejected' and rec['result_available'] is True and rec.get('report_sha256')==sha(R/'report.json')
 cfg=report['configs'][item['name']];assert cfg['spec_path']==item['spec'] and cfg['asset']==item['asset']
 market=markets[item['asset']];f=spec['parameters']['fast_ema_span_days'];s=spec['parameters']['slow_ema_span_days'];ef=evaluate.ema(market['daily_close'],f);es=evaluate.ema(market['daily_close'],s)
 for mult in ('1','2','3'):
  scen=cfg['scenarios'][mult];assert len(scen['folds'])==12 and D(scen['terminal_units'])==0 and scen['terminal_flat']
  for ix,fold in enumerate(scen['folds']):
   start=datetime.fromisoformat(fold['start_utc'].replace('Z','+00:00'));end=datetime.fromisoformat(fold['end_exclusive_utc'].replace('Z','+00:00'))
   assert end-start==timedelta(days=30)
   if ix<11:assert fold['end_exclusive_utc']==scen['folds'][ix+1]['start_utc']
  assert close(sum((D(v) for v in scen['cost_parts_usdt'].values()),D(0)),scen['cost_usdt'])
  assert close(D(scen['terminal_nav_usdt']),D(2000)+D(scen['net_pnl_usdt']))
  assert scen['minute_nav_samples']>=518400 and 0<=scen['max_drawdown_1m_sampled_pct']<100
  # Recompute one complete asset/cost scenario from frozen inputs and compare trade and NAV hashes.
  replay=evaluate.evaluate_one(item['name'],item['asset'],spec['parameters'],int(mult),market,filters,plan)
  for key in ('net_return_pct','cost_usdt','fills','rejected_orders','round_trips','minute_nav_sha256_f64le','daily_nav_sha256_f64le'):
   assert replay[key]==scen[key],(item['name'],mult,key,replay[key],scen[key])
  arc=readgzjson(ROOT/'data/runs'/R.name/f"{item['name']}_cost{mult}.json.gz")
  assert replay['trades']==arc['trades'] and replay['decisions']==arc['decisions'] and replay['daily_nav']==arc['daily_nav']
  trows=sorted(trade_groups.get((item['name'],mult,item['asset']),[]),key=lambda x:x['execution_utc'])
  assert len(trows)==len(replay['trades'])
  for t,row in zip(replay['trades'],trows):
   for key in ('trade_id','side','status','execution_utc','signal_available_utc','quantity','execution','reference','cash_before','units_before','cash_after','units_after'):
    if key in t:assert row[key]==str(t[key]),(item['name'],mult,key,row[key],t[key])
  drows=sorted(decision_groups.get((item['name'],mult,item['asset']),[]),key=lambda x:x['simulated_decision_at_utc'])
  assert len(drows)==len(replay['decisions'])
  for d,row in zip(replay['decisions'],drows):
   assert row['signal_day_utc']==d['signal_day_utc'] and row['signal_available_at_utc']==d['signal_available_at_utc'] and row['simulated_decision_at_utc']==d['simulated_decision_at_utc']
  for i,value in enumerate(replay['daily_nav']):daily_expected.append((item['name'],item['asset'],int(mult),i,float(value)))
  replays+=1
  # Independently replay Decimal ledger identities, exact historical 00:01 prices and signal availability.
  cash=D('2000');units=D(0);cost_parts={k:D(0) for k in ('fee','half_spread','slippage','impact','tick_rounding')};fills=rejects=roundtrips=0
  rows=sorted(trade_groups.get((item['name'],mult,item['asset']),[]),key=lambda x:(x['execution_utc'],x['trade_id']))
  for t in rows:
   available=datetime.fromisoformat(t['signal_available_utc'].replace('Z','+00:00'));executed=datetime.fromisoformat(t['execution_utc'].replace('Z','+00:00'));assert (executed-available).total_seconds()==60
   mi=int(t['minute_index']);assert int(market['minute_ts'][mi])==int(executed.timestamp()*1000) and D(str(market['minute_open'][mi]))==D(t['reference'])
   assert D(t['cash_before'])==cash and D(t['units_before'])==units
   if t['status']!='filled':assert D(t['cash_after'])==cash and D(t['units_after'])==units;rejects+=1;continue
   q=D(t['quantity']);px=D(t['execution']);ref=D(t['reference']);parts=ast.literal_eval(t['cost_parts']);fee=D(parts['fee']);fx=filters[item['asset']]
   assert q%D(fx['LOT_SIZE']['stepSize'])==0 and px%D(fx['PRICE_FILTER']['tickSize'])==0
   assert D(t['participation'])<=D('0.001') and D(fx['NOTIONAL']['minNotional'])<=q*px<=D(fx['NOTIONAL']['maxNotional'])
   k=D(mult);adv=D(t['lagged_ADV']);sigma=D(t['lagged_sigma']);part=D(t['participation'])
   # The historical feed has no bid/ask; the declared half-spread is used as an estimate.
   spread_rate=D('.0001')*k;slip_rate=D('.0002')*k;impact_rate=D('.5')*sigma*part.sqrt()*k;spread=q*ref*spread_rate;slip=q*ref*slip_rate;impact=q*ref*impact_rate
   sign=1 if t['side']=='buy' else -1;theory=ref*(D(1)+(spread_rate+slip_rate+impact_rate)*sign)
   assert theory==D(t['theoretical_execution'])
   for key in cost_parts:
    val=D(parts[key]);cost_parts[key]+=val
   assert abs(sum((D(x) for x in parts.values()),D(0))-D(t['cost_usdt']))<D('1e-18')
   c2=D(t['cash_after']);u2=D(t['units_after'])
   if t['side']=='buy':assert c2==cash-q*px-fee and u2==units+q
   else:assert c2==cash+q*px-fee and u2==units-q;roundtrips+=int(u2==0)
   assert c2>=0 and u2>=0 and abs(cash+units*ref-(c2+u2*ref)-sum((D(x) for x in parts.values()),D(0)))<D('1e-16')
   cash,units=c2,u2;fills+=1
  assert units==0 and close(cash,scen['terminal_nav_usdt'])
  assert fills==scen['fills'] and rejects==scen['rejected_orders'] and roundtrips==scen['round_trips']
assert len(daily_rows)==len(daily_expected)
actual_daily=sorted((x['configuration'],x['asset'],int(x['cost_multiplier']),int(x['day_index']),float(x['nav_usdt'])) for x in daily_rows)
assert actual_daily==sorted(daily_expected)
# Every daily signal uses a closed day and exactly the frozen recursive EMA values.
for (name,mult,asset),rows in decision_groups.items():
 p=json.loads((ROOT/batch_by[name]['spec']).read_text())['parameters'];m=markets[asset];fast=evaluate.ema(m['daily_close'],p['fast_ema_span_days']);slow=evaluate.ema(m['daily_close'],p['slow_ema_span_days']);day0=int(m['day_ts'][0])
 for d in rows:
  sig=int(datetime.fromisoformat(d['signal_day_utc'].replace('Z','+00:00')).timestamp()*1000);i=(sig-day0)//DAY_MS
  assert m['day_ts'][i]==sig and abs(fast[i]-float(d['EMA_fast']))<1e-10 and abs(slow[i]-float(d['EMA_slow']))<1e-10
  assert int(datetime.fromisoformat(d['signal_available_at_utc'].replace('Z','+00:00')).timestamp()*1000)==sig+DAY_MS
  assert int(datetime.fromisoformat(d['simulated_decision_at_utc'].replace('Z','+00:00')).timestamp()*1000)==sig+DAY_MS+MIN_MS
# Grid adjacency and the complete, predeclared sensitivity result surface.
for item in batch:
 c=report['configs'][item['name']];assert c['status']=='rejected'
 s=spec=json.loads((ROOT/item['spec']).read_text())
 assert s['parameters']['fast_ema_span_days'] in plan['grid']['fast_ema_spans_days'] and s['parameters']['slow_ema_span_days'] in plan['grid']['slow_ema_spans_days']
 assert c['sensitivity']['neighbor_count']>=4
fold_rows=[];cost_rows=[]
for item in batch:
 cfg=report['configs'][item['name']]
 for mult in ('1','2','3'):
  sc=cfg['scenarios'][mult]
  cost_rows.append({'name':item['name'],'asset':item['asset'],'fast_span_days':cfg['fast_span_days'],'slow_span_days':cfg['slow_span_days'],'cost_multiplier':mult,'net_return_pct':sc['net_return_pct'],'cost_usdt':sc['cost_usdt'],'cost_parts_usdt':json.dumps(sc['cost_parts_usdt'],sort_keys=True),'max_drawdown_1m_sampled_pct':sc['max_drawdown_1m_sampled_pct'],'daily_sample_drawdown_pct':sc['daily_sample_drawdown_pct'],'sharpe':sc['daily_sharpe_annualized'],'calmar':sc['calmar_daily_sampled'],'fills':sc['fills'],'round_trips':sc['round_trips'],'positive_folds':sc['positive_folds'],'rejected_orders':sc['rejected_orders'],'terminal_flat':sc['terminal_flat']})
  for f in sc['folds']:fold_rows.append({'name':item['name'],'asset':item['asset'],'fast_span_days':cfg['fast_span_days'],'slow_span_days':cfg['slow_span_days'],'cost_multiplier':mult,**f})
writecsv(R/'fold_results.csv',fold_rows);writecsv(R/'cost_scenarios.csv',cost_rows)
writecsv(R/'equity_curves_daily.csv',[{'name':name,'asset':asset,'cost_multiplier':mult,'day_index':i,'nav_usdt':nav} for name,asset,mult,i,nav in daily_expected])
# Deterministic compression of event/equity details; original Parquet data remains outside Git.
for filename in ('trades.csv','decisions.csv','daily_equity.csv'):
 src=R/filename;dst=R/(filename+'.gz')
 if src.exists():
  with src.open('rb') as inp,dst.open('wb') as raw:
   with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0,compresslevel=9) as out:
    while chunk:=inp.read(1<<20):out.write(chunk)
  src.unlink()
 else:assert dst.exists()
# Lightweight table/heatmap for the full 3x3 fast/slow surface by asset.
summary_rows=[]
for item in batch:
 c=report['configs'][item['name']];p=json.loads((ROOT/item['spec']).read_text());s1,s2,s3=(c['scenarios'][x] for x in ('1','2','3'))
 summary_rows.append({'name':item['name'],'asset':item['asset'],'fast_span_days':p['parameters']['fast_ema_span_days'],'slow_span_days':p['parameters']['slow_ema_span_days'],'return_1x_pct':s1['net_return_pct'],'return_2x_pct':s2['net_return_pct'],'return_3x_pct':s3['net_return_pct'],'drawdown_1x_sampled_pct':s1['max_drawdown_1m_sampled_pct'],'drawdown_3x_sampled_pct':s3['max_drawdown_1m_sampled_pct'],'positive_1x_folds':s1['positive_folds'],'fills_1x':s1['fills'],'round_trips_1x':s1['round_trips'],'cost_1x_usdt':s1['cost_usdt'],'gross_to_cost_1x':s1['gross_reference_pnl_to_cost'],'neighbor_3x_positive_fraction':c['sensitivity']['local_3x_neighbor_positive_fraction'],'passed':c['status']=='passed'})
with (R/'sensitivity.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(summary_rows[0]),lineterminator='\n');w.writeheader();w.writerows(sorted(summary_rows,key=lambda x:x['return_1x_pct'],reverse=True))
cellw,cellh=160,75;svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="400" viewBox="0 0 1100 400"><rect width="100%" height="100%" fill="white"/><text x="18" y="24" font-family="sans-serif" font-size="18" font-weight="bold">EMA fast/slow daily crossover: 1× net return surface</text>']
for panel,asset in enumerate(('BTC','ETH')):
 base=45+panel*530;svg.append(f'<text x="{base+240}" y="52" text-anchor="middle" font-family="sans-serif" font-size="15">{asset}</text>')
 for j,slow in enumerate(plan['grid']['slow_ema_spans_days']):svg.append(f'<text x="{base+150+j*cellw}" y="78" text-anchor="middle" font-family="sans-serif" font-size="12">Slow {slow}</text>')
 for i,fast in enumerate(plan['grid']['fast_ema_spans_days']):
  y=92+i*cellh;svg.append(f'<text x="{base+85}" y="{y+38}" text-anchor="end" font-family="sans-serif" font-size="12">Fast {fast}</text>')
  for j,slow in enumerate(plan['grid']['slow_ema_spans_days']):
   row=next(x for x in summary_rows if x['asset']==asset and x['fast_span_days']==fast and x['slow_span_days']==slow);value=row['return_1x_pct'];x=base+100+j*cellw;color='#b42318' if value<0 else '#16803c';svg.extend([f'<rect x="{x}" y="{y}" width="154" height="70" rx="4" fill="{color}"/>',f'<text x="{x+77}" y="{y+42}" text-anchor="middle" font-family="sans-serif" fill="white">{value:.2f}%</text>'])
svg.append('</svg>');(R/'sensitivity_surface.svg').write_text('\n'.join(svg)+'\n')
ranked=sorted([dict(v,name=k) for k,v in report['configs'].items()],key=lambda c:c['scenarios']['1']['net_return_pct'],reverse=True);best=ranked[0]
report['integrity_audit']={'status':'passed','configs':18,'cost_scenes':54,'deterministic_replays':replays,'closed_daily_signal_inputs_verified':True,'next_day_plus_60s_execution_timing_verified':True,'decimal_balances_and_fees_verified':True,'exchange_LOT_tick_notional_and_participation_verified':True,'continuous_12x30d_folds':True,'oos_nav_samples_per_scene_minimum':518400,'history_is_not_untouched_holdout':True,'real_orders':0}
report['artifacts']={'trades':'research/experiments/'+R.name+'/trades.csv.gz','decisions':'research/experiments/'+R.name+'/decisions.csv.gz','daily_equity':'research/experiments/'+R.name+'/daily_equity.csv.gz','equity_curves_daily':'research/experiments/'+R.name+'/equity_curves_daily.csv.gz','fold_results':'research/experiments/'+R.name+'/fold_results.csv','cost_scenarios':'research/experiments/'+R.name+'/cost_scenarios.csv','sensitivity':'research/experiments/'+R.name+'/sensitivity.csv','sensitivity_surface':'research/experiments/'+R.name+'/sensitivity_surface.svg'}
report['code_hashes']={'freeze.py':sha(R/'freeze.py'),'evaluate.py':sha(R/'evaluate.py'),'audit.py':sha(R/'audit.py'),'kernel.py':sha(ROOT/'research/experiments/20261001T133655Z/kernel.py'),'lagged_cost_engine.py':sha(ROOT/'research/experiments/20261001T013355Z/evaluate.py')}
write_json(R/'report.json',report)
src=R/'equity_curves_daily.csv';dst=R/'equity_curves_daily.csv.gz'
if src.exists():
 with src.open('rb') as inp,dst.open('wb') as raw:
  with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0,compresslevel=9) as out:
   while chunk:=inp.read(1<<20):out.write(chunk)
 src.unlink()
else:assert dst.exists()
positive={k:sum(x['scenarios'][k]['net_return_pct']>0 for x in ranked) for k in ('1','2','3')}
lines=['# BTC/ETH 日线快速/慢速 EMA 交叉回测','',f"- 冻结轮次 `{R.name}`；18个具体配置均在首次收益计算前 reserve。计划 SHA256 `{sha(R/'plan.json')}`。",'- 数据为 Binance 归档现货 1 分钟 OHLCV，聚合为完整 UTC 日线。信号只取已闭合日线；执行参考是信号可得后60秒的下一日00:01分钟开盘，仅作历史回测价格，不是本轮实时报价或交易所真实成交。',f"- OOS {plan['data']['oos_start_utc']} 至 {plan['data']['oos_end_exclusive_utc']}，360天、12个连续30天折；该历史已反复研究，不是未触碰留出。初始16项此前审计均有实际报告，无缺项待补。",'- 每格为独立2000 USDT单币长仓账户，原始权重100%投向该格对应的BTC或ETH；无双币合并、交叉转账、杠杆、借币、资金费或现金利息。EMA从首个完整数据日收盘递推，alpha=2/(span+1)、adjust=False，不跨折重置。',f"- 预设参数面：fast EMA {plan['grid']['fast_ema_spans_days']}日 × slow EMA {plan['grid']['slow_ema_spans_days']}日，BTC/ETH各9格，共18格；每格1×/2×/3×成本。",'- 成本包括每侧10bp手续费、估计半价差1bp、滑点2bp、前20个完整UTC日波动率与quote ADV相关平方根冲击，参与率上限0.1%；按本轮公开GET交易规则快照检查价格tick、数量步长和名义额。历史盘口和历史过滤器规则不可用，点差/滑点/立即IOC成交是假设。','', '## 判定','',f"- {len(ranked)}个配置全部 rejected；1x/2x/3x有正收益的配置数为{positive['1']}/{positive['2']}/{positive['3']}。最佳配置 `{best['name']}`：净收益 {best['scenarios']['1']['net_return_pct']:.2f}%/{best['scenarios']['2']['net_return_pct']:.2f}%/{best['scenarios']['3']['net_return_pct']:.2f}%，1x正折 {best['scenarios']['1']['positive_folds']}/12，3x采样回撤 {best['scenarios']['3']['max_drawdown_1m_sampled_pct']:.2f}%；未通过盈利、折一致性或邻域门槛。",'- 同期单币买入持有基准由已有注册报告只读复用，未重新计算；完整指标和SHA见 report.json。', '', '## 全部变体（按1x收益排序）','', '|资产|fast|slow|1x|2x|3x|1x/3x采样DD|1x正折|1x往返|1x成本USDT|3x邻域正比例|状态|','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for c in ranked:
 a,b,d=(c['scenarios'][k] for k in ('1','2','3'));lines.append(f"|{c['asset']}|{c['fast_span_days']}|{c['slow_span_days']}|{a['net_return_pct']:.2f}%|{b['net_return_pct']:.2f}%|{d['net_return_pct']:.2f}%|{a['max_drawdown_1m_sampled_pct']:.2f}%/{d['max_drawdown_1m_sampled_pct']:.2f}%|{a['positive_folds']}/12|{a['round_trips']}|{a['cost_usdt']}|{c['sensitivity']['local_3x_neighbor_positive_fraction']:.0%}|rejected|")
lines+=['','## 三项验证','', '- Walk-forward：12个连续30天OOS折，持仓和本金跨折连续；比较每折及1分钟收盘/成交参考点采样回撤。历史反复使用，有明显多重选择偏差；不作独立最终留出声明。', '- Sensitivity：fast/slow两轴完整3×3网格，BTC与ETH各自评估；检查Sharpe、Calmar、回撤、正收益比例及相邻3x盈利平台。全网格没有成本后盈利候选。', '- Costs：54个配置/成本场景纳入手续费、估计价差、滑点、成交量冲击及取整；费用分项、成交数量和余额守恒审计留在账本。无历史L2，不能证明真实IOC成交。', '- 精确重放：`.venv/bin/python research/experiments/20261014T084051Z/audit.py`；完整复现：`.venv/bin/python research/experiments/20261014T084051Z/reproduce.py`。报告、逐折、NAV、成交及决策压缩明细与数据/代码SHA均留档；本轮没有证明稳定实盘盈利。','']
(R/'result.md').write_text('\n'.join(lines).rstrip()+'\n')
manifest={'round':R.name,'plan_sha256':sha(R/'plan.json'),'exchange_info_raw_sha256':sha(R/'exchange_info_raw.json'),'exchange_filter_snapshot_sha256':sha(R/'exchange_filters.json'),'sources':report['data_manifest']['assets'],'output_hashes':{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in [R/'report.json',R/'result.md',R/'sensitivity.csv',R/'sensitivity_surface.svg',R/'fold_results.csv',R/'cost_scenarios.csv',R/'equity_curves_daily.csv.gz',R/'trades.csv.gz',R/'decisions.csv.gz',R/'daily_equity.csv.gz']},'code_hashes':report['code_hashes'],'source_paper':plan['literature_context']}
write_json(R/'data_manifest.json',manifest)
print(json.dumps({'audit':'passed','configs':len(ranked),'passed':report['summary']['passed'],'rejected':report['summary']['rejected'],'positive_1x_2x_3x':positive,'best':best['name'],'best_returns':[best['scenarios'][k]['net_return_pct'] for k in ('1','2','3')],'replays':replays,'report_sha256':sha(R/'report.json')}))
