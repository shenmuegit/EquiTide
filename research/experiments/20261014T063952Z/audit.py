#!/usr/bin/env python3
"""Hash, timing, accounting and deterministic replay audit for this grid."""
import csv,gzip,hashlib,json,math,os,sys
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sys.path.insert(0,str(ROUND));import evaluate

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def readgz(p):
 with gzip.open(p,'rt') as f:return json.load(f)
def writecsv(path,rows):
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def same_core(a,b):return all(a[k]==b[k] for k in b)
plan=json.loads((ROUND/'plan.json').read_text());batch=json.loads((ROUND/'batch.json').read_text());report=json.loads((ROUND/'report.json').read_text())
assert len(batch)==18 and len({x['fingerprint'] for x in batch})==18 and report['summary']['cost_scenes']==54
assert report['summary']['candidate_configs']==18 and report['summary']['directions']==2
filters=json.loads((ROUND/'exchange_filters.json').read_text());assert filters['raw_sha256']==plan['exchange_rules']['sha256']==sha(ROUND/'exchange_info_raw.json')
assert filters['received_at_utc']==plan['exchange_rules']['received_at_utc']
filter_map={a+'USDT':rows for a,rows in filters['filters'].items()}
ledger=Path(os.environ.get('LEADLAG_REGISTRY_LEDGER',ROOT/'research/automation/registry.jsonl'));records=registry.read_records(ledger);events=registry.read_events(ledger);reserved={x['fingerprint'] for x in events if x.get('status')=='reserved'}
for asset,rows in report['data_manifest']['assets'].items():
 for r in rows['source_files']:
  p=ROOT/r['path'];assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
markets={a:evaluate.load_asset(a) for a in ('BTC','ETH')};manifest=report['data_manifest'];assert {a:[f['sha256'] for f in markets[a]['files']] for a in markets}=={a:[f['sha256'] for f in manifest['assets'][a]['source_files']] for a in markets}
folds=[];scenes=[];sensitivity=[];n_replays=0;run_dir=ROOT/'data/runs'/ROUND.name
for row in batch:
 spec=json.loads((ROOT/row['spec']).read_text());fp=registry.fingerprint(spec);assert fp==row['fingerprint'] and fp in reserved
 rec=records[fp]
 if rec['status']=='reserved':assert rec['result_available'] is False
 else:assert rec['status']=='rejected' and rec['result_available'] is True and rec.get('report_sha256')==sha(ROUND/'report.json')
 cfg=report['configs'][row['name']];assert cfg['fingerprint']==fp and cfg['spec']==row['spec']
 reserve_event=next(x for x in reversed(events) if x['fingerprint']==fp and x['status']=='reserved');finish_times=[]
 assert reserve_event['recorded_at_utc']<report['evaluation_started_utc']
 for mult in (1,2,3):
  arc=readgz(run_dir/f"{row['name']}_cost{mult}.json.gz");actual=arc['summary'];s=cfg['scenarios'][str(mult)]
  assert arc['fingerprint']==fp and arc['name']==row['name'] and all(s[k]==actual[k] for k in actual)
  nav=arc['daily_nav_usdt'];assert len(nav)==361 and all(math.isfinite(x) and x>0 for x in nav) and abs(nav[-1]-float(actual['terminal_nav_usdt']))<1e-8
  assert len(actual['folds'])==12 and all(f['observations']==30 for f in actual['folds'])
  assert actual['cost_multiplier']==mult
  # Every accepted fill respects the exact Decimal cash/units and execution cost identity.
  position=D(0);cash=D('2000');last_time=None
  for t in arc['trades']:
   if last_time is not None:assert t['execution_utc']>=last_time
   last_time=t['execution_utc'];cb,ub,ca,ua,ref=(D(t[k]) for k in ('cash_before','units_before','cash_after','units_after','reference'))
   if t['status']!='filled':assert cb==ca and ub==ua;continue
   q,px=(D(t[k]) for k in ('quantity','execution'));cost=D(t['cost_usdt']);parts=sum((D(v) for v in t['cost_parts'].values()),D(0));assert abs(parts-cost)<D('1e-18')
   assert abs((cb+ub*ref)-(ca+ua*ref)-cost)<D('1e-10') and ca>=0 and ua>=0
   fx=filter_map[t['asset']+'USDT'];assert q%D(fx['LOT_SIZE']['stepSize'])==0 and px%D(fx['PRICE_FILTER']['tickSize'])==0
   assert D(t['participation'])<=D(plan['cost_model']['maximum_participation'])
   assert abs((evaluate.datetime.fromisoformat(t['execution_utc'].replace('Z','+00:00'))-evaluate.datetime.fromisoformat(t['signal_available_utc'].replace('Z','+00:00'))).total_seconds()-60)<1e-6
   assert t['signal_to_execution_seconds']==60
   if t['side']=='buy':assert ub==0 and ua==q
   else:assert ub==q and ua==0
  # Deterministic re-execution on source bars must reproduce every fill and fold summary.
  rerun=evaluate.run(spec,markets,filter_map,mult)
  assert rerun['trades']==arc['trades'] and rerun['daily_nav_usdt']==nav and rerun['summary']['minute_nav_sha256_f64le']==actual['minute_nav_sha256_f64le'];n_replays+=1
  scenes.append({'name':row['name'],'role':'candidate','direction':row['leader']+'>'+row['follower'],'lookback_minutes':row['lookback_minutes'],'hold_minutes':row['hold_minutes'],'leader_threshold':row['leader_threshold'],'relative_gap_threshold':row['relative_gap_threshold'],'cost_multiplier':mult,'net_return_pct':actual['net_return_pct'],'net_pnl_usdt':actual['net_pnl_usdt'],'cost_usdt':actual['cost_usdt'],'cost_parts_usdt':json.dumps(actual['cost_parts_usdt'],sort_keys=True),'max_drawdown_pct':actual['max_drawdown_pct'],'daily_mark_drawdown_pct':actual['daily_mark_drawdown_pct'],'round_trips':actual['round_trips'],'positive_1x_folds':actual['positive_1x_folds'],'rejected_orders':actual['rejected_orders'],'capacity_rejections':actual['capacity_rejections'],'terminal_flat':actual['terminal_flat']})
  for fold in actual['folds']:folds.append({'name':row['name'],'direction':row['leader']+'>'+row['follower'],'lookback_minutes':row['lookback_minutes'],'hold_minutes':row['hold_minutes'],'leader_threshold':row['leader_threshold'],'relative_gap_threshold':row['relative_gap_threshold'],'cost_multiplier':mult,**fold})
for row in batch:
 c=report['configs'][row['name']]['scenarios'];thresholds=plan['grid']['leader_return_threshold'];gaps=plan['grid']['leader_minus_follower_gap_threshold'];ti=thresholds.index(row['leader_threshold']);gi=gaps.index(row['relative_gap_threshold']);neighbors=[]
 for q in batch:
  if q['leader']==row['leader'] and abs(thresholds.index(q['leader_threshold'])-ti)<=1 and abs(gaps.index(q['relative_gap_threshold'])-gi)<=1:neighbors.append(q['name'])
 frac=sum(report['configs'][n]['scenarios']['3']['net_return_pct']>0 for n in neighbors)/len(neighbors)
 sensitivity.append({'name':row['name'],'direction':row['leader']+'>'+row['follower'],'lookback_minutes':row['lookback_minutes'],'hold_minutes':row['hold_minutes'],'leader_threshold':row['leader_threshold'],'relative_gap_threshold':row['relative_gap_threshold'],'neighbor_configs':';'.join(neighbors),'neighbor_count':len(neighbors),'neighbor_3x_positive_fraction':frac,'1x_net_return_pct':c['1']['net_return_pct'],'2x_net_return_pct':c['2']['net_return_pct'],'3x_net_return_pct':c['3']['net_return_pct'],'1x_sharpe':c['1']['sharpe_annualized_daily'],'1x_calmar':c['1']['calmar'],'3x_sample_drawdown_pct':c['3']['max_drawdown_pct']})
writecsv(ROUND/'fold_results.csv',folds);writecsv(ROUND/'cost_scenarios.csv',scenes);writecsv(ROUND/'sensitivity.csv',sensitivity)
curves=[]
for row in batch:
 for mult in (1,2,3):
  arc=readgz(run_dir/f"{row['name']}_cost{mult}.json.gz")
  for i,v in enumerate(arc['daily_nav_usdt']):curves.append({'name':row['name'],'direction':row['leader']+'>'+row['follower'],'cost_multiplier':mult,'day_index':i,'date':plan['data']['oos_start_utc'][:10] if i==0 else (plan['data']['oos_end_exclusive_utc'][:10] if i==360 else markets[row['leader']]['daily'][368+i]['date']),'nav_usdt':v})
writecsv(ROUND/'equity_curves_daily.csv',curves)
# Dependency-free two-direction threshold sensitivity surface (all nine cells retained).
tv=plan['grid']['leader_return_threshold'];gv=plan['grid']['leader_minus_follower_gap_threshold']
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="390" viewBox="0 0 900 390"><rect width="100%" height="100%" fill="white"/><text x="18" y="26" font-family="sans-serif" font-size="18" font-weight="bold">1× 成本：领先收益阈值 × 相对差阈值（固定回看30m/持有180m）</text>']
for panel,leader in enumerate(('BTC','ETH')):
 bx=28+panel*440;svg.append(f'<text x="{bx+200}" y="54" text-anchor="middle" font-family="sans-serif" font-size="15">{leader} 领先方向</text>')
 for j,g in enumerate(gv):svg.append(f'<text x="{bx+120+j*102}" y="76" text-anchor="middle" font-family="sans-serif" font-size="11">差阈值 {g*100:.2f}%</text>')
 for i,t in enumerate(tv):
  y=88+i*88;svg.append(f'<text x="{bx+94}" y="{y+42}" text-anchor="end" font-family="sans-serif" font-size="11">领先阈值 {t*100:.2f}%</text>')
  for j,g in enumerate(gv):
   v=next(x['1x_net_return_pct'] for x in sensitivity if x['direction'].startswith(leader+'>') and x['leader_threshold']==t and x['relative_gap_threshold']==g);x=bx+102+j*102;color='#b42318' if v<0 else '#16803c';svg.extend([f'<rect x="{x}" y="{y}" width="98" height="82" rx="4" fill="{color}"/>',f'<text x="{x+49}" y="{y+46}" text-anchor="middle" font-family="sans-serif" fill="white">{v:.2f}%</text>'])
svg.append('</svg>');(ROUND/'sensitivity_surface.svg').write_text('\n'.join(svg)+'\n')
report['integrity_audit']={'status':'passed','unique_reserved_fingerprints':18,'scenarios_audited':54,'exact_deterministic_replays':n_replays,'input_hashes_verified':True,'exchange_filter_snapshot_verified':True,'walk_forward_folds':12,'daily_curve_samples_per_scenario':361,'fill_cash_units_cost_lot_tick_and_delay_checks':'passed','historical_OOS_backtest_not_live':'confirmed'}
report['reproduction']={'evaluate':'.venv/bin/python research/experiments/'+ROUND.name+'/evaluate.py','audit':'.venv/bin/python research/experiments/'+ROUND.name+'/audit.py','reserve':'18 threshold variants reserved separately before the first return calculation.'}
report['artifacts']={'fold_results':'research/experiments/'+ROUND.name+'/fold_results.csv','cost_scenarios':'research/experiments/'+ROUND.name+'/cost_scenarios.csv','equity_curves_daily':'research/experiments/'+ROUND.name+'/equity_curves_daily.csv','sensitivity':'research/experiments/'+ROUND.name+'/sensitivity.csv','sensitivity_surface':'research/experiments/'+ROUND.name+'/sensitivity_surface.svg'}
report['code_hashes']={'freeze.py':sha(ROUND/'freeze.py'),'evaluate.py':sha(ROUND/'evaluate.py'),'audit.py':sha(ROUND/'audit.py')}
(ROUND/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
ranked=sorted([dict(v,name=k) for k,v in report['configs'].items()],key=lambda c:c['scenarios']['1']['net_return_pct'],reverse=True);best=ranked[0];base=report['baseline_references']
lines=['# BTC/ETH 小时级领先—跟随阈值敏感性回测','',f"- 冻结轮次 `{ROUND.name}`；18个方向/参数配置在计算前分别 reserve。计划 SHA256 `{sha(ROUND/'plan.json')}`。",'- 使用 Binance 现货历史 1 分钟 OHLCV；这不是实时行情模拟盘，也不代表真实订单成交。每日/分钟信号不读取未来K线，成交仅按历史可用后下一分钟开盘做成本模型估算。',f"- OOS {plan['data']['oos_start_utc']} 至 {plan['data']['oos_end_exclusive_utc']}，360日、12个连续30日折；重复开发历史而非未触碰最终留出集。",'- 固定回看30分钟、持有180分钟；方向分别BTC→ETH和ETH→BTC，单配置独立本金2000 USDT、只做多跟随币。敏感性轴为领先币30分钟收益阈值0.25%/0.5%/1%与领先—跟随收益差阈值0.10%/0.25%/0.50%，18格完整保留，不按OOS挑选。',"- 成本模型为每侧手续费10bp、估计半价差1bp、滑点2bp，加0.5×前20日收益样本标准差×sqrt(订单预算/前20日quote ADV)冲击，参与率≤0.1%；全部项按1x/2x/3x放大。价格/数量规则基于本轮公开GET exchangeInfo快照；历史盘口及历史过滤器不可得，成本及立即成交均为模型假设。",'', '## 结果','',f"- {len(ranked)}个配置全部 rejected；没有一个配置在1x、2x、3x全部成本下盈利。最佳为 `{best['name']}`（{best['leader']}→{best['follower']}，T={best['leader_threshold']*100:.2f}%，G={best['relative_gap_threshold']*100:.2f}%）：1x/2x/3x为{best['scenarios']['1']['net_return_pct']:.2f}%/{best['scenarios']['2']['net_return_pct']:.2f}%/{best['scenarios']['3']['net_return_pct']:.2f}%，1x正收益折{best['scenarios']['1']['positive_1x_folds']}/12，3x回撤{best['scenarios']['3']['max_drawdown_pct']:.2f}%。邻域3x正收益比例为{best['scenarios']['3']['neighborhood_positive_fraction_3x']:.0%}。",'- 同区间已登记BTC/ETH持有策略仅作为只读参照，未重新计算：见report.json中的baseline_references；其历史也不是未触碰留出。','', '|方向|领先收益阈值|相对差阈值|1x|2x|3x|1x正折|3x回撤|1x成交/往返|邻域3x正比例|状态|','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for c in ranked:
 s1,s2,s3=(c['scenarios'][m] for m in ('1','2','3'));lines.append(f"|{c['leader']}→{c['follower']}|{c['leader_threshold']*100:.2f}%|{c['relative_gap_threshold']*100:.2f}%|{s1['net_return_pct']:.2f}%|{s2['net_return_pct']:.2f}%|{s3['net_return_pct']:.2f}%|{s1['positive_1x_folds']}/12|{s3['max_drawdown_pct']:.2f}%|{s1['executions']}/{s1['round_trips']}|{s3['neighborhood_positive_fraction_3x']:.0%}|rejected|")
lines+=['','## 三项验证与限制','', '- Walk-forward：12×30日连续折，账户净值状态跨折延续；最佳配置未达预注册8/12正折门槛。历史已重复研究，存在严重多重试验选择偏差；不声称独立最终验证。分钟回撤按1分钟收盘NAV和成交参考点抽样，不含分钟内极值。', '- Sensitivity：双方向各一个完整3×3网格。整体收益随阈值变化不形成成本后正收益平台；3x相邻格通过比例列于 sensitivity.csv。', '- Costs：1x/2x/3x全成本逐笔应用；审计逐条复核费用、滑点、冲击、取整、参与率、LOT/tick、延迟和余额恒等式。无历史L2，因此成本及IOC成交为假设。', '- 逐折净收益、每日NAV、成本场景和按配置压缩的每笔信号/交易输出位于本轮文件夹与被忽略的 `data/runs/`；SHA与重现命令见 `data_manifest.json`/report.json。', '- 该参数批次被预注册用于检验小时领先—跟随阈值稳健性；18格全部完整完成后拒绝，不会声称稳定实盘盈利，也不替换paper10冻结账户。', '']
(ROUND/'result.md').write_text('\n'.join(lines))
manifest={'round':ROUND.name,'plan_sha256':sha(ROUND/'plan.json'),'exchange_info_raw_sha256':sha(ROUND/'exchange_info_raw.json'),'exchange_filters_sha256':sha(ROUND/'exchange_filters.json'),'source_files':report['data_manifest']['assets'],'output_hashes':{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in [ROUND/'report.json',ROUND/'result.md',ROUND/'fold_results.csv',ROUND/'cost_scenarios.csv',ROUND/'equity_curves_daily.csv',ROUND/'sensitivity.csv',ROUND/'sensitivity_surface.svg']},'code_hashes':{'freeze.py':sha(ROUND/'freeze.py'),'evaluate.py':sha(ROUND/'evaluate.py'),'audit.py':sha(ROUND/'audit.py'),'kernel.py':sha(ROOT/'research/experiments/20261001T133655Z/kernel.py'),'lagged_cost_engine.py':sha(ROOT/'research/experiments/20261001T013355Z/evaluate.py')},'reserve_events':sha(ROUND/'reserve.json')}
(ROUND/'data_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'audit':'passed','candidate_configs':len(ranked),'passed':sum(c['status']=='passed' for c in ranked),'rejected':sum(c['status']=='rejected' for c in ranked),'best':best['name'],'best_returns':[best['scenarios'][m]['net_return_pct'] for m in ('1','2','3')],'scenario_rows':len(scenes),'fold_rows':len(folds),'curve_rows':len(curves),'replays':n_replays,'report_sha256':sha(ROUND/'report.json')}))
