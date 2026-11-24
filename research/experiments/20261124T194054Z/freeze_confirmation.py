"""Freeze four new passive graphs with complete actual source metadata before reserve."""
import copy,itertools,json
from decimal import Decimal
from common import *
rd=lambda p:json.loads(p.read_text());P=ROOT/'research/experiments/20261124T173957Z';old=rd(P/'plan.json');rs=reg.read_records(ROOT/'research/automation/registry.jsonl');WS=[9,10,11];KS=[2,3,4];BTC={9: '0bf89ad7e816dc8436650fa6be706c9b2ea1fb94554d3916ddb887a90002eb84', 10: '41de4309229b892489a07574af07a73ae93229a35c118558ed60362285e90c89', 11: 'dda512b902edcbc3c9534ab74e49f7cfc7f70c6048830c8f9f85cb4570750ecb'};ETH={2: '2d507bae7fcad21f0cee312f173fc1f75c24a0d7df574965a3c25d7fa60dc4cb', 3: 'a34c0bd6e523db4188b1b6f27d2e8efec9b679106ae19d9cd97438b6dbae3984', 4: '837c883b294d38362de4d77bbf8977e1656bffdad55f2e12c0917b6291c957ae'};refs={};grid=[];batch=[];lookup=[];(R/'specs').mkdir(exist_ok=True)
def actual(fp):
 z=rs[fp];assert z['result_available'] and sha(ROOT/z['report'])==z['report_sha256'];return copy.deepcopy(next(c for c in rd(ROOT/z['report'])['configs'].values() if c['fingerprint']==fp))
def reuse(fp,W=None,K=None,control=True):
 c=actual(fp);z=rs[fp];row={k:copy.deepcopy(c[k]) for k in ['scope','role','asset','capital_usdt','name','fingerprint','spec']};row.update(readonly=True,W=W,K=K,control_only=control)
 for k in ['N','NB','NE','source_fingerprints','raw_weights']:
  if k in c:row[k]=copy.deepcopy(c[k])
 refs[fp]={**row,'report':z['report'],'report_sha256':z['report_sha256'],'spec_sha256':sha(ROOT/c['spec']),'archive':c['archive'],'archive_sha256':sha(ROOT/c['archive']),'status':z['status']};return refs[fp]
# Complete canonical component index is built before looking up any grid cell.
def component_key(xs):
 totals={}
 for c in xs:totals[c['fingerprint']]=totals.get(c['fingerprint'],Decimal(0))+Decimal(str(c['weight']))
 return tuple(sorted(totals.items()))
index={}
for fp,z in rs.items():
 sp=z.get('spec',{});q=sp.get('parameters',{})
 if sp.get('kind')=='combination' and q.get('start_utc')=='2025-10-19T00:01:00Z' and q.get('end_utc')=='2026-11-14T00:01:00Z' and (z.get('result_available') or z['status']=='reserved'):index.setdefault(component_key(sp['components']),[]).append(fp)
def graph(l,r):return index.get(component_key([{'fingerprint':l,'weight':1},{'fingerprint':r,'weight':1}]),[])
btc={w:reuse(fp,w,None) for w,fp in BTC.items()};eth={k:reuse(fp,None,k) for k,fp in ETH.items()};bh=reuse('8c4a819586d938bef2d405290fa78edbd1a95b96dd1ac78ae4802edb7b22abd3');eh=reuse('2b5eb3d1a240680f04f3f8a531c4192e154c5aac118ccdfdb47bc164d21e968b');holdfps=graph(bh['fingerprint'],eh['fingerprint']);assert len(holdfps)==1;hold=reuse(holdfps[0]);parents={}
for w,k in itertools.product(WS,KS):
 fs=graph(BTC[w],ETH[k]);lookup.append({'BTC_entry_volatility_window_days':w,'ETH_trend_slope_lag_days':k,'matches':fs})
 if fs:assert len(fs)==1 and not (w in [9,11] and k in [2,4]);parents[w,k]=reuse(fs[0],w,k,False)
 else:assert w in [9,11] and k in [2,4]
rules=copy.deepcopy(old['rules']);rules.update(signal='固定BTC L29/H.03/E.005、入场样本日logvol上限cap.0275及ROC5严格方向确认门槛.0025，只改变入场波动估计窗口V=9/10旧/11个完成日；风险过滤只管新开/反向，保留实际同向数量和原正常退出。联合ETH有限EWMS16 beta15/17趋势斜率滞后D=2/3旧/4日，K.0075、L5/H.02/E.0075、入场V6cap.05625、longonly、M4成熟资金费年龄1..36h/1h保守可得延迟、预算R.0075/VW9固定。检验BTC较短/较长波动估计与ETH趋势确认速度的联合作用。事前3×3网格有4个新角点V9/11×D2/4，5格真实旧结果只读；代表V9/D2在结果前固定。完整复用BTC C3750/N1000与ETH C15000/N4000银行，原始全银行乘数[1,1]，总资本18750、资本占比20%/80%、初始目标总敞口5000；不归一化、缩放数量、划拨、再平衡或交叉保证金。',execution='Actual original native bank cash,quantity,LOT,tick,fees,spread,slippage,volumeimpact,actualfunding,independentmargin and fullNAV reused;0newnative.',allocation='Rawwholebank[1,1],3750+15000=18750capital20/80,target1000+4000=5000. Aligned full-dollar bank NAV sum,no normalization,scaling,parentorders,transfers,rebalance,crossmargin.8native+6parent read-only sources;4newparents.')
for w,k in itertools.product(WS,KS):
 if (w,k) in parents:grid.append(parents[w,k]);continue
 l,r=btc[w],eth[k];sp=copy.deepcopy(rd(ROOT/parents[10,k]['spec']));q={a:v for a,v in sp['parameters'].items() if not a.startswith(('BTC_','ETH_')) and a not in ['prior_370day_source_fingerprint','fixed_total_initial_target_entry_notional_usdt']};name=f'parent_BTCEntryV{w}_N1000_ETHSlopeLag{k}_M4_N4000_raw1_1_C3750_15000_391d';sp.update(name=name,family='btc-entry-volwindow-eth-trend-slope-lag-passive-combination',logic=rules,validation_plan=rel(R/'plan.json'),components=[{'fingerprint':l['fingerprint'],'weight':1},{'fingerprint':r['fingerprint'],'weight':1}]);q.update(initial_capital_usdt=18750,component_capitals_usdt=[3750,15000],component_initial_entry_notionals_usdt=[1000,4000],raw_component_multipliers=[1,1],capital_allocation_fractions=[.2,.8],initial_target_total_notional_usdt=5000,initial_gross_notional_fraction_of_parent_capital=5000/18750,source_component_spec_sha256=[sha(ROOT/l['spec']),sha(ROOT/r['spec'])],actual_native_quantity_and_impact_reused=True,walk_forward_complete30day_folds=13)
 for asset,c in [('BTC',l),('ETH',r)]:
  ch=rd(ROOT/c['spec'])['parameters']
  for a,v in ch.items():
   if a not in ['input_hashes','costs','persistence','prior_370day_source_fingerprint','raw_entry_notional_fraction_of_initial_capital','initial_capital_usdt','fixed_entry_notional_usdt','start_utc','end_utc']:q[asset+'_'+a]=copy.deepcopy(v)
  q[asset+'_bank_capital_usdt']=ch['initial_capital_usdt'];q[asset+'_entry_notional_usdt']=ch['fixed_entry_notional_usdt'];q[asset+'_existing_actual_bank_reused']=True;q[asset+'_new_native_quantity_and_impact_computed']=False
 sp['parameters']=q;path=R/'specs'/(name+'.json');put(path,sp);fp=reg.fingerprint(sp);assert fp not in rs;row={'scope':'parent','role':'candidate','asset':'COMBO','capital_usdt':18750,'NB':1000,'NE':4000,'BTC_entry_volatility_window_days':w,'ETH_trend_slope_lag_days':k,'source_fingerprints':[l['fingerprint'],r['fingerprint']],'raw_weights':[1,1],'readonly':False,'name':name,'fingerprint':fp,'spec':rel(path),'W':w,'K':k};grid.append(row);batch.append(row)
assert len(refs)==14 and len(batch)==4 and len(grid)==9
p=copy.deepcopy(old)
for a in list(p):
 if a.startswith(('additional_predeclared_','baseline_by_')):p.pop(a)
p.update(round=R.name,frozen_at_utc=now(),hypothesis=rd(R/'research_design.json')['hypothesis'],rules=rules,axes={'BTC_ENTRY_VOLATILITY_WINDOW_DAYS':WS,'ETH_TREND_SLOPE_LAG_DAYS':KS},axis_semantics={'W':'BTC new/reversed entry sample daily logvol window in completed days;cap.0275,L29/H.03/E.005,ROC5confirmation.0025,N1000 fixed;retain actual same-direction quantity and normal exit.','K':'ETH finiteEWMS16 trend slope lag in completed days;K.0075,V6cap.05625,R.0075,VW9,M4,age36h,N4000 fixed.'},grid=grid,native_grid=[],native_axes={'BTC':{'axes':[]},'ETH':{'axes':[]}},benchmark_parent_fingerprint=hold['fingerprint'],benchmark_by_cell={f'{w}:{k}':hold['fingerprint'] for w,k in itertools.product(WS,KS)},baseline_by_ETH_slope_lag={str(k):parents[10,k]['fingerprint'] for k in KS},baseline_native_fingerprint=ETH[3],base_parent_fingerprint=next(g['fingerprint'] for g in grid if g['W']==9 and g['K']==2),representative_preset={'W':9,'K':2},read_only_references=refs,prior_report={'path':rel(P/'report.json'),'sha256':sha(P/'report.json')},sensitivity={'axes':['BTC_ENTRY_VOLATILITY_WINDOW_DAYS','ETH_TREND_SLOPE_LAG_DAYS'],'index_radius':1,'local_positive3_min':.6,'local_recent_allcost6of8_min':.6,'no_post_outcome_reselection_or_extension':True},primary_source_reads=rd(R/'primary_source_access.json'),limits=rd(R/'research_design.json')['limitations'].split(';'),expected_counts={'new_configs':4,'new_native':0,'new_parents':4,'new_candidate_configs':4,'new_benchmark_configs':0,'new_source_components':0,'new_cost_scenes':12,'read_only_unique_results':14,'read_only_native_models':8,'read_only_parent_models':6,'read_only_cost_scenes':42,'grid_points':9,'native_grid_points':0,'read_only_existing_grid_points':5})
p.pop('baseline_by_BTC_N',None);p.pop('baseline_by_ETH_K',None);controls={str(k):parents[10,k] for k in KS};p['additional_predeclared_BTCV10_report_controls']=controls;p['grid_index_semantics']=p['axis_semantics']
for n,z in [('plan.json',p),('spec.json',p),('batch.json',batch)]:put(R/n,z)
put(R/'combination_prior_lookup.json',{'passed':True,'complete_registry_IDs_read':len(rs),'rows':lookup,'new_graphs':4,'old_grid_controls':5,'complete_graph_index_checked_before_reserve':True,'no_market_or_account_calculations':True});print('PASS4newgraphs/8native+6parentactualoldrefs/0newnative/3x3fixednotionalgrid',flush=True)
