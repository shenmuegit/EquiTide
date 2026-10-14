#!/usr/bin/env python3
"""Causal setup replay, Decimal ledger, cost, fold and parameter-surface audit."""
import ast,csv,gzip,hashlib,importlib.util,json,math,os,sys
from datetime import datetime,timedelta,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def close(a,b,tol=D('1e-7')):return abs(D(str(a))-D(str(b)))<=tol
def clean(x):return json.loads(json.dumps(x,default=str,ensure_ascii=False,allow_nan=False))
def drawdown(x):
 a=np.asarray(x,dtype=float);peak=np.maximum.accumulate(a);return float(np.max(np.where(peak>0,100*(1-a/peak),0),initial=0))
def write_json(p,x):p.write_text(json.dumps(clean(x),indent=2,ensure_ascii=False,allow_nan=False)+'\n')
batch=json.loads((R/'batch.json').read_text());report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());assert len(batch)==9 and len(report['configs'])==9 and report['plan_sha256']==sha(R/'plan.json')
ledger=Path(os.environ.get('RECLAIM_REGISTRY_LEDGER',ROOT/'research/automation/registry.jsonl'));records=registry.read_records(ledger)
for row in batch:
 spec=json.loads((ROOT/row['spec']).read_text());fp=registry.fingerprint(spec);rec=records.get(fp)
 assert report['configs'][row['name']]['fingerprint']==fp and rec
 if rec['status']=='reserved':assert rec['result_available'] is False
 else:
  assert rec['status']=='rejected' and rec['result_available'] is True
  assert rec.get('report_sha256')==sha(R/'report.json')
 assert spec['parameters']['initial_capital_usdt']==2000 and spec['parameters']['raw_asset_weights']==[.5,.5]
 cfg=report['configs'][row['name']]
 for mult in ('1','2','3'):
  sc=cfg['cost_scenarios'][mult];assert len(sc['folds'])==12 and len(sc['minute_nav_sha256'])==64
  for i,f in enumerate(sc['folds']):
   assert math.isfinite(f['net_return_pct']) and f['end_exclusive_utc']>f['start_utc']
   assert f['end_exclusive_utc']==(datetime.fromisoformat(f['start_utc'].replace('Z','+00:00'))+timedelta(days=30)).isoformat().replace('+00:00','Z')
   if i<11:assert f['end_exclusive_utc']==sc['folds'][i+1]['start_utc']
  assert close(sum((D(str(x)) for x in sc['cost_parts_usdt'].values()),D(0)),sc['cost_usdt'])
  assert close(D(sc['terminal_nav_usdt']),D(2000)+D(sc['net_pnl_usdt'])) and all(D(v)==0 for v in sc['terminal_units_by_asset'].values())
  assert sc['minute_nav_samples']>=518400 and 0<=sc['max_drawdown_1m_sampled_pct']<100
# Rebuild the exact daily inputs used by the signal and execution clock.
sys.path.insert(0,str(R));spec=importlib.util.spec_from_file_location('reclaim_evaluator',R/'evaluate.py');ev=importlib.util.module_from_spec(spec);spec.loader.exec_module(ev)
markets,market_filters=ev.load_market(plan);params={x['name']:json.loads((ROOT/x['spec']).read_text())['parameters'] for x in batch}
decision_path=R/'decisions.csv' if (R/'decisions.csv').exists() else R/'decisions.csv.gz';op=open if decision_path.suffix=='.csv' else gzip.open
trade_path=R/'trades.csv' if (R/'trades.csv').exists() else R/'trades.csv.gz';top=open if trade_path.suffix=='.csv' else gzip.open
trades={}
with top(trade_path,'rt',newline='') as f:
 for t in csv.DictReader(f):trades.setdefault((t['configuration'],t['cost_multiplier'],t['asset'],t['simulated_at_utc']),[]).append(t)
# Replay the complete pending-break, reclaim, and five-day exit state machine for every cost scene and asset.
with op(decision_path,'rt',newline='') as f:
 decision_rows=list(csv.DictReader(f))
for d in decision_rows:
  cfg,asset,mult=d['configuration'],d['asset'],d['cost_multiplier'];p=params[cfg];m=markets[asset]
  sig_ms=int(datetime.fromisoformat(d['signal_day_utc'].replace('Z','+00:00')).timestamp()*1000);i=(sig_ms-int(m['day_ts'][0]))//86_400_000
  assert m['day_ts'][i]==sig_ms and int(datetime.fromisoformat(d['signal_available_at_utc'].replace('Z','+00:00')).timestamp()*1000)==sig_ms+86_400_000
  exec_ms=int(datetime.fromisoformat(d['simulated_decision_at_utc'].replace('Z','+00:00')).timestamp()*1000);assert exec_ms-sig_ms-86_400_000==60_000
  low=float(np.min(m['low'][i-p['breakdown_lookback_days']:i]));cl=float(m['close'][i]);assert abs(low-float(d['prior_N_day_low']))<1e-8 and abs(cl-float(d['close']))<1e-8
# Independently replay the one-shot pending-level state machine, including the rule
# that an order rejection consumes a reclaim and that signal processing resumes
# only on the day after a timed exit.
groups={}
for d in decision_rows:groups.setdefault((d['configuration'],d['cost_multiplier'],d['asset']),[]).append(d)
for (cfg,mult,asset),ds in groups.items():
 p=params[cfg];m=markets[asset];pending=None;position=None
 for d in sorted(ds,key=lambda x:x['simulated_decision_at_utc']):
  signal_ms=int(datetime.fromisoformat(d['signal_day_utc'].replace('Z','+00:00')).timestamp()*1000);i=(signal_ms-int(m['day_ts'][0]))//86_400_000
  exec_ms=int(datetime.fromisoformat(d['simulated_decision_at_utc'].replace('Z','+00:00')).timestamp()*1000);close_px=float(m['close'][i]);prior_low=float(np.min(m['low'][i-p['breakdown_lookback_days']:i]))
  before=None if pending is None else dict(pending);action='hold';breakdown=reclaim=expired=False
  if position is not None:
   if exec_ms>=position['exit_due_ms']:action='time_exit'
  else:
   if pending is not None and i>pending['expiry_day_index']:pending=None;expired=True
   if pending is not None and i>pending['breakdown_day_index'] and i<=pending['expiry_day_index'] and close_px>pending['break_level']:
    reclaim=True;action='reclaim_entry'
   elif pending is None and close_px<prior_low:
    pending={'break_level':prior_low,'breakdown_day_index':int(i),'expiry_day_index':int(i+p['reclaim_window_days'])};breakdown=True;action='arm_failed_breakdown'
  expected_after=None if pending is None else pending
  recorded_after=None if pending is None else dict(pending)
  assert d['action']==action and (d['setup_breakdown'].lower()=='true')==breakdown and (d['setup_reclaim'].lower()=='true')==reclaim and (d['setup_expired'].lower()=='true')==expired,(cfg,mult,asset,d['signal_day_utc'],action,d['action'])
  assert (None if d['pending_before'] in ('None','') else ast.literal_eval(d['pending_before']))==before
  order=next((t for key,items in trades.items() if key[:3]==(cfg,mult,asset) for t in items if t['simulated_at_utc']==d['simulated_decision_at_utc']),None)
  if reclaim:
   assert order is not None
   if order['status']=='filled':pending=None;position={'exit_due_ms':exec_ms+p['fixed_holding_days']*86_400_000}
   else:pending=None
  elif action=='time_exit' and order is not None and order['status']=='filled':position=None
  assert (None if d['pending_after'] in ('None','') else ast.literal_eval(d['pending_after']))==recorded_after
# Replay order balances/cost stack and verify every virtual reference is the corresponding archived 00:01 1m open.
ledger_groups={}
for key,rows in trades.items():ledger_groups.setdefault(key[:3],[]).extend(rows)
ex=json.loads((R/'exchange_info_raw.json').read_text());filters={a:{x['filterType']:x for x in next(s for s in ex['symbols'] if s['symbol']==a+'USDT')['filters']} for a in ('BTC','ETH')}
for b in batch:
 name=b['name'];cfg=report['configs'][name]
 for mult in ('1','2','3'):
  scene=cfg['cost_scenarios'][mult]
  for asset in ('BTC','ETH'):
   m=markets[asset];cash=D('1000');units=D(0);parts={x:D(0) for x in ('fee','half_spread','slippage','impact','tick_rounding')};fills=rejects=rounds=0
   rows=[t for key,items in trades.items() if key[:3]==(name,mult,asset) for t in items];rows.sort(key=lambda x:(x['simulated_at_utc'],x['trade_id']))
   for t in rows:
    sim=int(datetime.fromisoformat(t['simulated_at_utc'].replace('Z','+00:00')).timestamp()*1000);mi=int(t['minute_index'])
    assert sim==m['minute_ts'][mi] and D(str(m['minute_open'][mi]))==D(t['reference'])
    assert int(datetime.fromisoformat(t['signal_available_at_utc'].replace('Z','+00:00')).timestamp()*1000)+60_000==sim
    if t['status']=='filled':
     q=D(t['quantity']);px=D(t['execution']);ref=D(t['reference']);cost=ast.literal_eval(t['cost_parts']);fee=D(cost['fee']);k=D(mult);adv=D(t['lagged_ADV']);sigma=D(t['lagged_sigma']);part=D(t['budget'])/adv
     assert close(part,t['participation']) and part<=D('.001')
     spread=D('.0001')*k;slip=D('.0002')*k;impact=D('.5')*sigma*part.sqrt()*k;theory=ref*(1+(spread+slip+impact)*(1 if t['side']=='buy' else -1))
     assert theory==D(t['theoretical_execution']) and ev.kernel.adverse_tick(theory,D(filters[asset]['PRICE_FILTER']['tickSize']),t['side']=='buy')==px
     expected={'fee':q*px*D('.001')*k,'half_spread':q*ref*spread,'slippage':q*ref*slip,'impact':q*ref*impact,'tick_rounding':q*abs(px-theory)}
     assert all(abs(D(cost[x])-expected[x])<D('1e-18') for x in expected)
     if t['side']=='buy':assert D(t['cash_after'])==cash-q*px-fee and D(t['units_after'])==units+q
     else:assert D(t['cash_after'])==cash+q*px-fee and D(t['units_after'])==units-q
     fs=filters[asset];assert q%D(fs['LOT_SIZE']['stepSize'])==0 and D(fs['NOTIONAL']['minNotional'])<=q*px<=D(fs['NOTIONAL']['maxNotional'])
     assert D(t['cash_after'])>=0 and D(t['units_after'])>=0
     assert abs(cash+units*ref-D(t['cash_after'])-D(t['units_after'])*ref-sum(expected.values(),D(0)))<D('1e-18')
     cash,units=D(t['cash_after']),D(t['units_after']);fills+=1;rounds+=int(t['side']=='sell' and units==0)
     for x in parts:parts[x]+=D(cost[x])
    else:
     assert t['status']=='rejected' and D(t['cash_after'])==cash and D(t['units_after'])==units;rejects+=1
   sl=scene['asset_sleeves'][asset];assert close(D(sl['terminal_nav_usdt']),cash), (name,mult,asset,str(cash),sl['terminal_nav_usdt'],len(rows));assert D(sl['terminal_units'])==units==0
   assert close(sum(parts.values(),D(0)),sl['cost_usdt']) and fills==sl['fills'] and rejects==sl['rejected_orders'] and rounds==sl['round_trips']
# Aggregate fold equity directly from paired 1,000-USDT sleeves and retain the full 3x3 sensitivity surface.
rows=[]
for b in batch:
 p=params[b['name']];c=report['configs'][b['name']]
 for mult in ('1','2','3'):
  sc=c['cost_scenarios'][mult]
  for i,f in enumerate(sc['folds']):
   a=sum((D(sc['asset_sleeves'][asset]['fold_nav'][i]) for asset in ('BTC','ETH')),D(0));z=sum((D(sc['asset_sleeves'][asset]['fold_nav'][i+1]) for asset in ('BTC','ETH')),D(0))
   assert close(a,f['start_nav_usdt']) and close(z,f['end_nav_usdt']) and close(f['net_return_pct'],(z/a-1)*100)
 s1,s2,s3=(c['cost_scenarios'][x] for x in ('1','2','3'));rows.append({'name':b['name'],'breakdown_lookback_days':p['breakdown_lookback_days'],'reclaim_window_days':p['reclaim_window_days'],'holding_days':p['fixed_holding_days'],'return_1x_pct':s1['net_return_pct'],'return_2x_pct':s2['net_return_pct'],'return_3x_pct':s3['net_return_pct'],'drawdown_1x_sampled_pct':s1['max_drawdown_1m_sampled_pct'],'drawdown_3x_sampled_pct':s3['max_drawdown_1m_sampled_pct'],'sharpe_1x_daily':s1['daily_sharpe_annualized'],'calmar_1x_daily':s1['calmar_daily_sampled'],'positive_1x_folds':s1['positive_folds'],'rebalances_1x':s1['fills'],'cost_1x_usdt':float(s1['cost_usdt']),'gross_to_cost_1x':s1['gross_to_cost'],'neighbor_3x_positive_fraction':c['sensitivity']['local_3x_neighbor_positive_fraction'],'passed':c['status']=='passed'})
with (R/'sensitivity.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(sorted(rows,key=lambda x:x['return_1x_pct'],reverse=True))
cellw,cellh=220,92;width,height=900,430;vals=[r['return_1x_pct'] for r in rows];lo,hi=min(vals),max(vals);svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">','<rect width="100%" height="100%" fill="#fff"/>','<text x="18" y="25" font-family="sans-serif" font-size="18" font-weight="bold">Daily failed-breakdown reclaim: net-return surface</text>']
for j,k in enumerate((1,2,3)):svg.append(f'<text x="{180+j*cellw+cellw/2}" y="60" text-anchor="middle" font-family="sans-serif" font-size="14">Reclaim window {k}d</text>')
by={(r['breakdown_lookback_days'],r['reclaim_window_days']):r for r in rows}
for i,n in enumerate((10,20,40)):
 svg.append(f'<text x="80" y="{110+i*cellh+cellh/2}" text-anchor="middle" font-family="sans-serif" font-size="14">Prior low {n}d</text>')
 for j,k in enumerate((1,2,3)):
  r=by[(n,k)];x=180+j*cellw;y=78+i*cellh;z=(r['return_1x_pct']-lo)/(hi-lo) if hi>lo else .5;red=int(244-100*z);green=int(205-105*z);blue=int(205-105*z)
  svg.extend([f'<rect x="{x}" y="{y}" width="{cellw}" height="{cellh}" fill="rgb({red},{green},{blue})" stroke="#444"/>',f'<text x="{x+cellw/2}" y="{y+36}" text-anchor="middle" font-family="sans-serif" font-size="16">1x {r["return_1x_pct"]:.2f}%</text>',f'<text x="{x+cellw/2}" y="{y+64}" text-anchor="middle" font-family="sans-serif" font-size="14">3x {r["return_3x_pct"]:.2f}%</text>'])
svg.append('</svg>');(R/'sensitivity_surface.svg').write_text('\n'.join(svg)+'\n')
for name in ('trades.csv','decisions.csv','daily_equity.csv'):
 src=R/name;dst=R/(name+'.gz')
 if src.exists():
  with src.open('rb') as f,dst.open('wb') as out:
   with gzip.GzipFile(filename='',mode='wb',fileobj=out,mtime=0,compresslevel=9) as z:
    while chunk:=f.read(1<<20):z.write(chunk)
  src.unlink()
 else:assert dst.exists()
ranked=sorted(rows,key=lambda x:x['return_1x_pct'],reverse=True);best=ranked[0];bench=report['benchmark_read_only']['cost_scenarios'];initial=json.loads((ROOT/'research/experiments/20261012T035429Z/prior_evidence_audit.json').read_text())
lines=['# BTC/ETH：日线跌破后收盘收复长仓策略回测','',f"- 预注册轮次 `{R.name}`；9个完整配置均先登记，计划SHA256 `{sha(R/'plan.json')}`。",'- 本轮测试的是固定规则的 long-only failed-breakdown/reclaim 变体：跌破前N日低点后，在未来K个已闭合日内收盘重新站上同一低点，次日00:01 UTC开盘买入，持有5个完整日线间隔后退出。它借鉴了已发表的假突破反转思路，但不是Street Smarts原版规则，也不含其所有过滤、止损或资产选择。',f"- Binance归档现货1分钟OHLCV；每日规则只读取已闭合UTC bar，订单参考为信号可用后60秒的下一日00:01 1m开盘。OOS {plan['data']['start_utc']} 至 {plan['data']['end_exclusive_utc']}，12个连续30日折；此窗口已反复使用，不是未触碰留出。初始16条配置历史回测缺失数为{len(initial.get('missing_initial16',[]))}。",'- 每配置2000 USDT：BTC/ETH独立1000-USDT sleeve，原始权重50/50；不转移资金、不加杠杆、不做空、现金收益为0。', '- 成本：手续费10bp/侧、估计半价差1bp/侧、滑点2bp/侧，另加0.5×前20个完整UTC日收益样本σ×sqrt(订单预算/前20日quote ADV)冲击，最大参与率0.1%；使用当前PRICE/LOT/NOTIONAL/PERCENT_PRICE_BY_SIDE规则，percent-price参考用之前5根完整1m close代理。无历史L2或历史交易所规则，1x/2x/3x成本场景同时放大全部假设。', '', '## 结果与淘汰依据','',f"- 9个参数配置全部 rejected，三个成本倍数都亏损。表现最好的 `N={best['breakdown_lookback_days']}, K={best['reclaim_window_days']}` 1x/2x/3x收益 {best['return_1x_pct']:.2f}%/{best['return_2x_pct']:.2f}%/{best['return_3x_pct']:.2f}%，1x只有{best['positive_1x_folds']}/12折为正；3x采样回撤{best['drawdown_3x_sampled_pct']:.2f}%。敏感性网格中3x正收益配置0/9。",f"- 同窗只读50/50持有基准1x/2x/3x净收益 {bench['1']['net_return_pct']:.2f}%/{bench['2']['net_return_pct']:.2f}%/{bench['3']['net_return_pct']:.2f}%；未在本轮重新计算。", '', '## 参数网格（按1x净收益排序）','', '|配置|N低点|K收复天|持有天|1x|2x|3x|1x/3x采样DD|1x正折|成交数|1x成本USDT|3x邻域正比例|状态|','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for r in ranked:lines.append(f"|{r['name']}|{r['breakdown_lookback_days']}|{r['reclaim_window_days']}|{r['holding_days']}|{r['return_1x_pct']:.2f}%|{r['return_2x_pct']:.2f}%|{r['return_3x_pct']:.2f}%|{r['drawdown_1x_sampled_pct']:.2f}%/{r['drawdown_3x_sampled_pct']:.2f}%|{r['positive_1x_folds']}/12|{r['rebalances_1x']}|{r['cost_1x_usdt']:.2f}|{r['neighbor_3x_positive_fraction']:.0%}|rejected|")
lines+=['','## 三项验证与审计','', '- Walk-forward：按时间连续12×30日验证；逐折组合收益与同步OOS 1分钟收盘/成交参考标记最大回撤见report.json。该开发历史反复用于参数研究，有明显多重选择风险，不是终局验证。', '- Sensitivity：预注册N={10,20,40}、K={1,2,3}的完整3×3网格；固定5日持有，不按OOS挑选。所有9格按完整邻域计算3x正收益比例，结果无正平台。Sharpe、Calmar、整体回撤同时给出。', '- Costs：每个变体独立跑1x/2x/3x费用、spread、slippage、ADV相关impact、tick rounding和当前LOT/NOTIONAL/PERCENT_PRICE过滤；每笔现金守恒、费用分项、参考/执行时间、信号延迟、实际数量都留档。', '- `trades.csv.gz`为成交账本，`decisions.csv.gz`含每个每日arm/reclaim/expire/exit状态，`daily_equity.csv.gz`为连续组合日净值；数据与源哈希、代码哈希见data_manifest.json。', '- Reproduction：`.venv/bin/python research/experiments/20261014T043852Z/reproduce.py`通过独立临时登记簿重跑，不修改主登记。失败门槛含三种成本全正、≥8/12正折、DD3≤25%、邻域3x正比例≥60%、毛利/成本≥2.5、无拒单、终点空仓；全体淘汰。', '']
(R/'result.md').write_text('\n'.join(lines).rstrip()+'\n')
manifest={'plan_sha256':sha(R/'plan.json'),'exchange_info_raw_sha256':sha(R/'exchange_info_raw.json'),'source_data':report['data_manifest']['assets'],'output_hashes':{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in [R/'report.json',R/'result.md',R/'sensitivity.csv',R/'sensitivity_surface.svg',R/'trades.csv.gz',R/'decisions.csv.gz',R/'daily_equity.csv.gz']},'code_hashes':{'freeze.py':sha(R/'freeze.py'),'evaluate.py':sha(R/'evaluate.py'),'audit.py':sha(R/'audit.py'),'finish.py':sha(R/'finish.py') if (R/'finish.py').exists() else None,'reproduce.py':sha(R/'reproduce.py') if (R/'reproduce.py').exists() else None,'kernel.py':sha(ROOT/'research/experiments/20261001T133655Z/kernel.py')},'audit_sha256':sha(R/'audit.py')}
old=json.loads((R/'data_manifest.json').read_text()) if (R/'data_manifest.json').exists() else {}
for key in ('registry_fragment','finish_log_sha256'):
 if key in old:manifest[key]=old[key]
(R/'data_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'audit':'passed','candidates':len(ranked),'passed':sum(x['passed'] for x in ranked),'rejected':sum(not x['passed'] for x in ranked),'best':best['name'],'returns_1_2_3':[best['return_1x_pct'],best['return_2x_pct'],best['return_3x_pct']],'positive_folds':best['positive_1x_folds'],'report_sha256':sha(R/'report.json')}))
