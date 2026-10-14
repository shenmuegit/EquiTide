#!/usr/bin/env python3
"""Independent reservation, cost, balance, fold and sensitivity audit."""
import ast,csv,gzip,hashlib,json,math,os,sys,importlib.util
import numpy as np
from datetime import datetime,timedelta,timezone
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def close(a,b,tol=D('1e-7')):return abs(D(str(a))-D(str(b)))<=tol
def clean(x):return json.loads(json.dumps(x,default=str,ensure_ascii=False,allow_nan=False))
def pct(s):return f'{s:.2f}%'
def write_json(path,obj):path.write_text(json.dumps(clean(obj),indent=2,ensure_ascii=False,allow_nan=False)+'\n')
batch=json.loads((R/'batch.json').read_text());report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text())
assert len(batch)==9 and len(report['configs'])==9 and report['plan_sha256']==sha(R/'plan.json')
ledger=Path(os.environ.get('CMF_REGISTRY_LEDGER',ROOT/'research/automation/registry.jsonl'));records=registry.read_records(ledger)
for row in batch:
 spec=json.loads((ROOT/row['spec']).read_text());fp=registry.fingerprint(spec);rec=records.get(fp)
 assert report['configs'][row['name']]['fingerprint']==fp and rec and rec['status']=='reserved' and rec['result_available'] is False,(row['name'],rec)
 assert spec['parameters']['capital_usdt']==2000 and spec['parameters']['raw_initial_weights']=={'BTC':.5,'ETH':.5}
 cfg=report['configs'][row['name']]
 for mult in ('1','2','3'):
  scene=cfg['cost_scenarios'][mult];assert len(scene['folds'])==12
  for i,f in enumerate(scene['folds']):
   assert math.isfinite(f['net_return_pct']) and f['end_exclusive_utc']>f['start_utc']
   assert f['end_exclusive_utc']==(datetime.fromisoformat(f['start_utc'].replace('Z','+00:00'))+timedelta(days=30)).isoformat().replace('+00:00','Z')
   if i<11:assert f['end_exclusive_utc']==scene['folds'][i+1]['start_utc']
  parts=sum((D(str(v)) for v in scene['cost_parts_usdt'].values()),D(0));assert close(parts,scene['cost_usdt'])
  assert close(D(scene['terminal_nav_usdt']),D(2000)+D(scene['net_pnl_usdt']))
  assert all(D(v)==0 for v in scene['terminal_units_by_asset'].values())
  assert scene['minute_nav_samples']>=518400
  assert 0<=scene['max_drawdown_1m_sampled_pct']<100
# Rebuild source bars and verify that every logged signal and trade is causal.
sys.path.insert(0,str(R));spec=importlib.util.spec_from_file_location('cmf_evaluator',R/'evaluate.py');ev=importlib.util.module_from_spec(spec);spec.loader.exec_module(ev)
plan['_sha256']=sha(R/'plan.json');markets,market_filters=ev.load_market(plan)
spec_by_name={x['name']:json.loads((ROOT/x['spec']).read_text()) for x in batch}
decisions_path=R/'decisions.csv' if (R/'decisions.csv').exists() else R/'decisions.csv.gz'
decision_open=open if decisions_path.suffix=='.csv' else gzip.open
with decision_open(decisions_path,'rt',newline='') as f:
 for drow in csv.DictReader(f):
  asset=drow['asset'];m=markets[asset];params=spec_by_name[drow['configuration']]['parameters']
  signal_ms=int(datetime.fromisoformat(drow['signal_day_utc'].replace('Z','+00:00')).timestamp()*1000);idx=(signal_ms-int(m['day_ts'][0]))//86_400_000
  assert m['day_ts'][idx]==signal_ms
  assert int(datetime.fromisoformat(drow['signal_available_at_utc'].replace('Z','+00:00')).timestamp()*1000)==signal_ms+86_400_000
  sim_ms=int(datetime.fromisoformat(drow['simulated_decision_at_utc'].replace('Z','+00:00')).timestamp()*1000)
  assert sim_ms-signal_ms-86_400_000==60_000
  n=params['cmf_lookback_days'];cmfv=ev.cmf_at(m,idx,n);entry=params['channel_entry_lookback_days'];exitn=params['channel_exit_lookback_days']
  high=float(np.max(m['high'][idx-entry:idx]));low=float(np.min(m['low'][idx-exitn:idx]));cl=float(m['close'][idx])
  assert abs(cmfv-float(drow['cmf']))<1e-12 and abs(high-float(drow['prior_channel_entry_high']))<1e-8 and abs(low-float(drow['prior_channel_exit_low']))<1e-8
  assert (drow['entry_channel_breakout'].lower()=='true')==(cl>high)
  assert (drow['entry_flow_confirmation'].lower()=='true')==(cmfv>params['cmf_entry_threshold'])
  assert (drow['exit_channel_breakdown'].lower()=='true')==(cl<low)
# Replay every sleeve's Decimal transaction ledger, cost components and order constraints.
trades_path=R/'trades.csv' if (R/'trades.csv').exists() else R/'trades.csv.gz'
open_trade=open if trades_path.suffix=='.csv' else gzip.open
trades={}
with open_trade(trades_path,'rt',newline='') as f:
 for t in csv.DictReader(f):trades.setdefault((t['configuration'],t['cost_multiplier'],t['asset']),[]).append(t)
for eventset in trades.values():
 for t in eventset:
  asset=t['asset'];m=markets[asset];mi=int(t['minute_index'])
  assert int(m['minute_ts'][mi])==int(datetime.fromisoformat(t['simulated_at_utc'].replace('Z','+00:00')).timestamp()*1000)
  assert D(str(m['minute_open'][mi]))==D(t['reference'])
exchange=json.loads((R/'exchange_info_raw.json').read_text());filters={}
for asset in ('BTC','ETH'):
 sym=next(x for x in exchange['symbols'] if x['symbol']==asset+'USDT');filters[asset]={x['filterType']:x for x in sym['filters']}
for row in batch:
 name=row['name'];cfg=report['configs'][name]
 for mult in ('1','2','3'):
  sc=cfg['cost_scenarios'][mult]
  for asset in ('BTC','ETH'):
   cash=D('1000');units=D(0);costs={k:D(0) for k in ('fee','half_spread','slippage','impact','tick_rounding')};fills=rejects=rounds=0
   rows=trades.get((name,mult,asset),[])
   rows.sort(key=lambda x:(x['simulated_at_utc'],x['trade_id']))
   for t in rows:
    assert t['signal_available_at_utc']<=t['simulated_at_utc']
    assert (datetime.fromisoformat(t['simulated_at_utc'].replace('Z','+00:00'))-datetime.fromisoformat(t['signal_available_at_utc'].replace('Z','+00:00'))).total_seconds()==60
    assert (D(t['cash_before'])==cash and D(t['units_before'])==units) if 'cash_before' in t else True
    if t['status']=='filled':
     q=D(t['quantity']);px=D(t['execution']);ref=D(t['reference']);parts=ast.literal_eval(t['cost_parts']);fee=D(parts['fee'])
     for k in costs:costs[k]+=D(parts[k])
     assert abs(px-D(t['theoretical_execution']))<=D(filters[asset]['PRICE_FILTER']['tickSize'])
     assert abs(D(t['participation']))<=D('.001')
     k=D(mult);ref=D(t['reference']);adv=D(t['lagged_ADV']);sigma=D(t['lagged_sigma']);part=D(t['participation']);spread=D('.0001')*k;slip=D('.0002')*k;impact=D('.5')*sigma*part.sqrt()*k
     theoretical=ref*(1+(spread+slip+impact)*(1 if t['side']=='buy' else -1))
     assert theoretical==D(t['theoretical_execution'])
     assert ev.kernel.adverse_tick(theoretical,D(filters[asset]['PRICE_FILTER']['tickSize']),t['side']=='buy')==px
     assert abs(sum((D(v) for v in parts.values()),D(0))-D(t['cost_usdt']))<D('1e-18')
     assert D(t['cost_multiplier'])==D(mult)
     fs=filters[asset];assert q%D(fs['LOT_SIZE']['stepSize'])==0 and D(fs['PRICE_FILTER']['minPrice'])<=px<=D(fs['PRICE_FILTER']['maxPrice']) and D(fs['NOTIONAL']['minNotional'])<=q*px<=D(fs['NOTIONAL']['maxNotional'])
     if t['side']=='buy':assert D(t['cash_after'])==cash-q*px-fee and D(t['units_after'])==units+q
     else:assert D(t['cash_after'])==cash+q*px-fee and D(t['units_after'])==units-q
     assert D(t['cash_after'])>=0 and D(t['units_after'])>=0
     assert abs(cash+units*ref-D(t['cash_after'])-D(t['units_after'])*ref-sum((D(v) for v in parts.values()),D(0)))<D('1e-18')
     cash,units=D(t['cash_after']),D(t['units_after']);fills+=1;rounds+=int(t['side']=='sell' and units==0)
    else:
     assert t['status']=='rejected' and D(t['cash_after'])==cash and D(t['units_after'])==units
     rejects+=1
   sleeve=sc['asset_sleeves'][asset]
   assert D(sleeve['terminal_cash_usdt'])==cash and D(sleeve['terminal_units'])==units==0
   assert close(sum(costs.values(),D(0)),sleeve['cost_usdt'])
   assert fills==sleeve['fills'] and rejects==sleeve['rejected_orders'] and rounds==sleeve['round_trips']
 assert len(sleeve['fold_nav'])==13 and len(sleeve['folds'])==12
# Aggregate fold NAv directly from two independent 1,000-USDT sleeves.
for row in batch:
 for mult in ('1','2','3'):
  scene=report['configs'][row['name']]['cost_scenarios'][mult]
  for i,f in enumerate(scene['folds']):
   a=sum((D(scene['asset_sleeves'][z]['fold_nav'][i]) for z in ('BTC','ETH')),D(0));b=sum((D(scene['asset_sleeves'][z]['fold_nav'][i+1]) for z in ('BTC','ETH')),D(0))
   assert close(f['start_nav_usdt'],a) and close(f['end_nav_usdt'],b)
   assert close(f['net_return_pct'],(b/a-1)*100)
# Full predeclared 3x3 sensitivity surface and adjacent-grid robustness.
rows=[]
for row in batch:
 spec=json.loads((ROOT/row['spec']).read_text());p=spec['parameters'];c=report['configs'][row['name']]
 s={k:c['cost_scenarios'][k] for k in ('1','2','3')}
 rows.append({'name':row['name'],'entry_lookback_days':p['channel_entry_lookback_days'],'cmf_lookback_days':p['cmf_lookback_days'],'cmf_threshold':p['cmf_entry_threshold'],'return_1x_pct':s['1']['net_return_pct'],'return_2x_pct':s['2']['net_return_pct'],'return_3x_pct':s['3']['net_return_pct'],'drawdown_1x_sampled_pct':s['1']['max_drawdown_1m_sampled_pct'],'drawdown_3x_sampled_pct':s['3']['max_drawdown_1m_sampled_pct'],'sharpe_1x_daily':s['1']['daily_sharpe_annualized'],'calmar_1x_daily_sampled':s['1']['calmar_daily_sampled'],'positive_1x_folds':s['1']['positive_folds'],'cost_1x_usdt':float(s['1']['cost_usdt']),'gross_to_cost_1x':s['1']['gross_to_cost'],'positive_3x_neighbors':c['sensitivity']['local_3x_neighbor_positive_fraction'],'passed':c['status']=='passed'})
with (R/'sensitivity.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(sorted(rows,key=lambda x:x['return_1x_pct'],reverse=True))
# Standalone SVG surface: all cells shown, with 1x and 3x net returns.
cellw,cellh=220,92;width,height=900,430;vals=[x['return_1x_pct'] for x in rows];lo,hi=min(vals),max(vals)
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">','<rect width="100%" height="100%" fill="#fff"/>','<text x="20" y="26" font-family="sans-serif" font-size="18" font-weight="bold">CMF-confirmed daily channel: net-return surface</text>']
for j,n in enumerate((10,20,40)):svg.append(f'<text x="{180+j*cellw+cellw/2}" y="60" text-anchor="middle" font-family="sans-serif" font-size="14">CMF {n} days</text>')
by={(x['entry_lookback_days'],x['cmf_lookback_days']):x for x in rows}
for i,e in enumerate((10,20,40)):
 svg.append(f'<text x="82" y="{110+i*cellh+cellh/2}" text-anchor="middle" font-family="sans-serif" font-size="14">Entry {e}d</text>')
 for j,n in enumerate((10,20,40)):
  x=by[(e,n)];z=(x['return_1x_pct']-lo)/(hi-lo) if hi>lo else .5;red=int(244-100*z);green=int(205-105*z);blue=int(205-105*z);xp=180+j*cellw;yp=78+i*cellh
  svg.append(f'<rect x="{xp}" y="{yp}" width="{cellw}" height="{cellh}" fill="rgb({red},{green},{blue})" stroke="#444"/>')
  svg.append(f'<text x="{xp+cellw/2}" y="{yp+37}" text-anchor="middle" font-family="sans-serif" font-size="16">1x {x["return_1x_pct"]:.2f}%</text>')
  svg.append(f'<text x="{xp+cellw/2}" y="{yp+64}" text-anchor="middle" font-family="sans-serif" font-size="14">3x {x["return_3x_pct"]:.2f}%</text>')
svg.append('</svg>');(R/'sensitivity_surface.svg').write_text('\n'.join(svg)+'\n')
# Compress detailed but lightweight event and daily series deterministically.
for name in ('trades.csv','decisions.csv','daily_equity.csv'):
 src=R/name;dst=R/(name+'.gz')
 if src.exists():
  with src.open('rb') as f,dst.open('wb') as out:
   with gzip.GzipFile(filename='',mode='wb',fileobj=out,mtime=0,compresslevel=9) as gz:
    while chunk:=f.read(1<<20):gz.write(chunk)
  src.unlink()
 else:assert dst.exists()
# Replace verbose input arrays, if any, by their indexed archive hashes in the report.
for c in report['configs'].values():
 for s in c['cost_scenarios'].values():
  for asset in ('BTC','ETH'):s['asset_sleeves'][asset].pop('daily_nav',None)
report['summary']['positive_configs_by_cost_multiplier']={str(k):sum(c['cost_scenarios'][str(k)]['net_return_pct']>0 for c in report['configs'].values()) for k in (1,2,3)}
write_json(R/'report.json',report)
# Render concise Chinese report; per-fold data stays in report.json.
ranked=sorted(rows,key=lambda x:x['return_1x_pct'],reverse=True);best=ranked[0];bench=report['benchmark_read_only']['scenes'];all16=json.loads((ROOT/'research/experiments/20261012T035429Z/prior_evidence_audit.json').read_text())
lines=['# BTC/ETH：CMF资金流确认日线通道突破回测','',f"- 冻结轮次 `{R.name}`；计划 SHA256 `{sha(R/'plan.json')}`。9个配置在计算前已逐一 reserve。",'- 数据为 Binance 归档现货1分钟OHLCV聚合UTC日线；历史回测，不是本轮实时行情或实盘业绩。交易参考为信号日收盘可用后的下一UTC日00:01分钟开盘；绝不使用同日收盘补单。',f"- OOS {plan['data']['start_utc']} 至 {plan['data']['end_exclusive_utc']}，12个连续30日折。该窗口已被反复研究，不是未触碰留出集；初始16条配置的历史证据审计显示缺失{len(all16.get('missing_initial16',[]))}项。本轮首个reserve前登记簿有9436个事件、4614个唯一指纹；本轮另预登记9个变体，累计试验已产生明显多重选择偏差，本轮不作DSR/PBO声称。",'- 组合为每配置2000 USDT，BTC/ETH独立1000-USDT现金袖套，初始权重各50%；无跨袖套转账、杠杆、做空或现金利息。',f"- 进场：当日收盘严格高于此前E日最高价，且CMF_N严格大于0.05；CMF按TA-Lib原始[-1,1]比率，用Binance quote_volume计算。退出为当日收盘严格低于此前30日最低价。信号日不纳入比较通道。CMF公式按TA-Lib规格；原始公式与作者动机仅作指标背景，不能证明此策略有效。",'- 成本：每侧手续费10bp、估计半价差1bp、滑点2bp、0.5×前20个完整日收益样本σ×sqrt(订单预算/前20日quote ADV)；参与率上限0.1%，按当前PRICE/LOT/NOTIONAL/PERCENT_PRICE_BY_SIDE交易所规则和历史前5分钟参考价代理核验。真实历史L2盘口不可用；1x/2x/3x同倍放大成本。', '', '## 判定', '', f"- {len(ranked)}个配置全部 rejected；最佳1x为 `{best['name']}`，1x/2x/3x净收益 {best['return_1x_pct']:.2f}%/{best['return_2x_pct']:.2f}%/{best['return_3x_pct']:.2f}%，仅{best['positive_1x_folds']}/12个1x折为正；1x/3x采样回撤 {best['drawdown_1x_sampled_pct']:.2f}%/{best['drawdown_3x_sampled_pct']:.2f}%。尽管该网格角落在此历史OOS盈利，未通过一致性与邻域标准，不能作为正收益稳健方法。",f"- 1x/2x/3x净收益为正的配置数分别 {sum(x['return_1x_pct']>0 for x in ranked)}/9、{sum(x['return_2x_pct']>0 for x in ranked)}/9、{sum(x['return_3x_pct']>0 for x in ranked)}/9；邻域3x正比例见`sensitivity.csv`。同窗已登记50/50持有对照来自只读报告，1x/2x/3x净收益 {bench['1']['net_return_pct']:.2f}%/{bench['2']['net_return_pct']:.2f}%/{bench['3']['net_return_pct']:.2f}%；未在本轮重复回测。", '', '## 参数网格全部结果（按1x收益降序）','', '|配置|入场E天|CMF N天|1x|2x|3x|1x/3x采样回撤|1x正折|1x成交|1x成本USDT|3x邻域正比例|状态|','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for x in ranked:
 c=report['configs'][x['name']];s1=c['cost_scenarios']['1']
 lines.append(f"|{x['name']}|{x['entry_lookback_days']}|{x['cmf_lookback_days']}|{x['return_1x_pct']:.2f}%|{x['return_2x_pct']:.2f}%|{x['return_3x_pct']:.2f}%|{x['drawdown_1x_sampled_pct']:.2f}%/{x['drawdown_3x_sampled_pct']:.2f}%|{x['positive_1x_folds']}/12|{s1['fills']}|{s1['cost_usdt']}|{x['positive_3x_neighbors']:.0%}|rejected|")
lines+=['','## 三项验证与执行审计','', '- Walk-forward：12个连续30日折，组合每日净值和完整同步1分钟收盘/成交后参考标记用于最大回撤；分钟内极值不可得。无训练拟合；入场/退出通道只用signal_day之前的闭合日线。CMF_N包含signal_day当天的完整OHLCV，且只有日线闭合后才用于信号。', '- Sensitivity：预先固定Entry Lookback={10,20,40}和CMF Lookback={10,20,40}二维完整3×3网格；所有九格均保留，不按OOS择优。只有3x成本邻域中正收益比例达到60%、至少8/12折正收益等条件才过门。', '- Costs：逐资产逐单记录手续费/价差/滑点/冲击/取整、实际参考分钟、参与率、规则过滤和余额；1x/2x/3x全场景见`report.json`与`trades.csv.gz`。现金守恒和数量规则见`audit.log`。', '- 连续组合日净值在`daily_equity.csv.gz`，逐日信号与时间延迟在`decisions.csv.gz`，数据、交易所快照、代码和输出哈希在`data_manifest.json`。同窗持有对照只读复用，不作为新配置计数。', '- 早期实现错误已作为无效诊断报告保存在`diagnostics/invalid_terminal_cost_v1/`；该版终端冲击窗口越过OOS截止，未注册为结果。有效v2仅使用终端前可用数据并重跑。预约后的计划元数据时间格式曾标准化；经济规则、权重、边界和配置指纹未改变，说明留在`evaluation_attempts.log`。', '- Reproduction: `bash research/experiments/20261014T023722Z/reproduce.py`使用隔离临时登记账本，完整复跑并比对经济报告，不追加主登记簿；冻结计划不重建。', '- 本轮门槛：1x/2x/3x均正、至少8/12个1x正折、3x采样回撤≤25%、3x邻域正收益比例≥60%、毛收益/成本≥2.5、零容量/交易规则拒单且终点空仓。九格均未通过，全部结果保留；已反复使用历史与多重搜索限制所有推断。', '']
(R/'result.md').write_text('\n'.join(lines).rstrip()+'\n')
prior_manifest=json.loads((R/'data_manifest.json').read_text()) if (R/'data_manifest.json').exists() else {}
manifest={'plan_sha256':sha(R/'plan.json'),'exchange_info_raw_sha256':sha(R/'exchange_info_raw.json'),'source_data':report['data_manifest']['assets'],'output_hashes':{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in [R/'report.json',R/'result.md',R/'sensitivity.csv',R/'sensitivity_surface.svg',R/'trades.csv.gz',R/'decisions.csv.gz',R/'daily_equity.csv.gz']},'code_hashes':{'freeze.py':sha(R/'freeze.py'),'evaluate.py':sha(R/'evaluate.py'),'audit.py':sha(R/'audit.py'),'finish.py':sha(R/'finish.py') if (R/'finish.py').exists() else None,'reproduce.py':sha(R/'reproduce.py') if (R/'reproduce.py').exists() else None,'kernel.py':sha(ROOT/'research/experiments/20261001T133655Z/kernel.py')},'audit_sha256':sha(R/'audit.py')}
for key in ('registry_fragment','finish_log_sha256'):
 if key in prior_manifest:manifest[key]=prior_manifest[key]
(R/'data_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'audit':'passed','candidates':len(ranked),'passed':sum(x['passed'] for x in ranked),'rejected':sum(not x['passed'] for x in ranked),'best':best['name'],'returns_1_2_3':[best['return_1x_pct'],best['return_2x_pct'],best['return_3x_pct']],'positive_folds':best['positive_1x_folds'],'positive_3x_neighbors':best['positive_3x_neighbors'],'report_sha256':sha(R/'report.json')}))
