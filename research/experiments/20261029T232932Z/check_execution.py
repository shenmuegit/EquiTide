"""Readonly actual-native versus oldbank-scaled quantities,NAVs and nonlinear costs."""
import gzip,json
from decimal import Decimal as D
import numpy as np
from run import ROOT,R,sha,put,engine,parent
from controls import matched
report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());assert json.loads((R/'verification.json').read_text())['passed'];_,markets,common,oldvectors,oldss=parent.parent.recover(plan);pool=plan['component_sources'];records=__import__('run').reg.read_records(ROOT/'research/automation/registry.jsonl');sourcecache={};rows=[];fractional=changed=impactdiff=0
for c in report['configs'].values():
 if c['scope']!='native':continue
 p=json.loads((ROOT/c['spec']).read_text())['parameters'];asset=c['asset'];m=markets[asset];scale=D(str(c['capital_usdt']))/10000
 if c['mode']=='momentum':ref=plan['fixed_BTC']
 elif c['mode']=='hold':ref=next(x for x in pool.values() if x['asset']==asset and x['role']=='benchmark')
 elif c['mode']=='ungated':ref=next(x for fp,x in pool.items() if x['asset']=='ETH' and x['role']=='candidate' and 'entry_funding_lookback_settlements' not in records[fp]['spec']['parameters'])
 else:ref=next(x for fp,x in pool.items() if x['asset']=='ETH' and records[fp]['spec']['parameters'].get('entry_funding_lookback_settlements')==6 and records[fp]['spec']['parameters'].get('entry_funding_cost_cap_per_settlement')==c['entry_funding_cost_cap_per_settlement'])
 if ref['fingerprint'] not in sourcecache:sourcecache[ref['fingerprint']]=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()))
 source=sourcecache[ref['fingerprint']];arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));lot=D(m['meta']['lot_size'])
 for k,s in arc['scenes'].items():
  old=source['scenes'][k];assert len(s['trades'])==len(old['trades']);fq=cq=iq=0
  for t,b in zip(s['trades'],old['trades']):
   assert all(t[x]==b[x] for x in ['decision_index','trade_ts_ns','opening','terminal','reference']);scaled=D(b['quantity'])*scale;fq+=int(scaled%lot!=0);cq+=int(D(t['quantity'])!=scaled);iq+=int(D(t['impact_rate'])!=D(b['impact_rate']));assert D(t['quantity'])%lot==0
  v=np.empty(len(m['ts']));coverage=0
  for z in s['state_segments']:
   a,b=z['axis_start'],z['axis_end_exclusive'];assert a==coverage;v[a:b]=float(z['cash'])+float(z['signed_units'])*(m['axis_prices'][a:b]-float(z['entry_price']));coverage=b
  assert coverage==len(v) and engine.navhash(v)==s['summary']['NAV_sha256_f64le'];projected=v[common['projections'][asset]];scaledold=float(scale)*oldvectors[ref['fingerprint'],k];delta=float(np.max(np.abs(projected-scaledold)));fractional+=fq;changed+=cq;impactdiff+=iq
  rows.append({'name':c['name'],'fingerprint':c['fingerprint'],'asset':asset,'cost_multiplier':int(k),'actual_capital_usdt':c['capital_usdt'],'actual_entry_N':p['fixed_entry_notional_usdt'],'old_source_fp':ref['fingerprint'],'old_bank_scale_for_comparison':str(scale),'trades_checked':len(s['trades']),'old_scaled_quantities_off_LOT':fq,'actual_quantity_differs_from_oldscaled':cq,'actual_impact_rate_differs_from_oldmodel':iq,'max_abs_full_NAV_difference_usdt':delta,'actual_NAV_sha256':s['summary']['NAV_sha256_f64le'],'old_scaled_NAV_sha256':engine.navhash(scaledold),'cost_actual_minus_linear_old_usdt':s['summary']['cost_usdt']-float(scale)*old['summary']['cost_usdt']})
configs=report['configs'];own,ungated,holds=matched(configs);pairs=[]
for c in configs.values():
 if c['role']!='candidate' or c['scope']!='parent':continue
 ref=own[c['BTC_capital_fraction'],c['entry_funding_cost_cap_per_settlement']]
 pairs.append({'actual_name':c['name'],'ownership_name':ref['name'],'BTC_capital_fraction':c['BTC_capital_fraction'],'funding_cap':c['entry_funding_cost_cap_per_settlement'],'actual_status':c['status'],'scenes':{k:{'actual_return_pct':z['net_return_pct'],'ownership_return_pct':ref['scenes'][k]['net_return_pct'],'return_delta_pp':z['net_return_pct']-ref['scenes'][k]['net_return_pct'],'actual_whole_DD_pct':z['max_drawdown_pct'],'ownership_whole_DD_pct':ref['scenes'][k]['max_drawdown_pct'],'actual_positive_recent_folds':sum(f['net_return_pct']>0 for f in z['recent40']['folds']),'ownership_positive_recent_folds':sum(f['net_return_pct']>0 for f in ref['scenes'][k]['recent40']['folds'])} for k,z in c['scenes'].items()}})
assert len(rows)==63 and len(pairs)==9 and fractional>0 and changed>0 and impactdiff>0
proof={'passed':True,'financial_evaluations':0,'native_cost_scenes_verified':63,'actual_banks_reconstructed_from_recorded_ledgers_only':True,'same_original_price_funding_directions_and_trade_times':True,'old_scaled_orders_that_would_violate_LOT':fractional,'native_quantities_different_from_linear_oldbank_scale':changed,'actual_impact_rates_recomputed_at_newsize':impactdiff,'native_rows':rows,'matched_parent_ownership_comparisons':pairs,'venue_capacity_L2_TCA_not_established':True,'financial_report_sha256':sha(R/'report.json')};put(R/'execution_verification.json',proof)
with (R/'result.md').open('a') as f:f.write('\n原生执行与旧银行缩放只读核验：63原生成本场景中，旧数量直接缩放有'+str(fractional)+'笔不符合lot，实际原生数量与线性缩放不同'+str(changed)+'笔，按新数量重算的冲击率有'+str(impactdiff)+'笔不同。全原生账本NAV已重新构造并核对SHA；9组父组合逐成本收益/整体回撤/近期正折与旧所有权精确比较见execution_verification.json，不以位级浮点差异宣称新增alpha，不称实际交易所容量验证。\n')
print(json.dumps({k:v for k,v in proof.items() if k not in ['native_rows','matched_parent_ownership_comparisons']},ensure_ascii=False),flush=True)
