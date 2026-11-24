"""Freeze six new passive graphs with complete actual source metadata before reserve."""
import copy,itertools,json
from decimal import Decimal
from common import *
rd=lambda p:json.loads(p.read_text());P=ROOT/'research/experiments/20261124T073649Z';old=rd(P/'plan.json');rs=reg.read_records(ROOT/'research/automation/registry.jsonl');WS=[0, 0.0025, 0.005];KS=[0.00625, 0.0075, 0.00875];BTC={0.0: '4820334331e1c14d0a37fcea1453968338ab94aaa9e4a77db68a8289d310a928', 0.0025: '41de4309229b892489a07574af07a73ae93229a35c118558ed60362285e90c89', 0.005: '4776466845bbab4b6ad910db952e913f21fdd850e053b1d2dd43dbbb8df4717d'};ETH={0.00625: 'abfce249bc303d17fa3a010900d6bbb74d7516bf90afeb219bd6ab3e99f74462', 0.0075: 'a34c0bd6e523db4188b1b6f27d2e8efec9b679106ae19d9cd97438b6dbae3984', 0.00875: '03946df62d906368f08cd9e8ac86d0622c769d0517c51d20c49e9cda414d3cc2'};refs={};grid=[];batch=[];lookup=[];(R/'specs').mkdir(exist_ok=True)
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
 fs=graph(BTC[w],ETH[k]);lookup.append({'BTC_confirmation_hurdle':w,'ETH_trend_strength':k,'matches':fs})
 if fs:assert len(fs)==1 and w==.0025;parents[w,k]=reuse(fs[0],w,k,False)
 else:assert w in [0,.005]
rules=copy.deepcopy(old['rules']);rules.update(signal='固定BTC L29/H.03/E.005、V10cap.0275，只改变新建或反向入场的五日方向确认门槛Q=0/.0025旧/.005；Q0仍要求方向乘已完成ROC5严格大于0，并非关闭确认。联合ETH有限EWMS16 beta15/17、D3趋势斜率门槛K=.00625/.0075旧/.00875，L5H.02E.0075、longonly、入场V6cap.05625、M4成熟资金费年龄1..36h/1h保守可得延迟、预算R.0075/VW9固定。检验BTC短期动量确认强度与ETH趋势强度的风险和成本交换。6个新父图、BTC Q.0025三旧格；事前代表Q0/K.0075，不按结果重选。原生银行C3750/N1000与C15000/N4000完整复用，原始权重[1,1]，总资金18750（20/80）、初始目标敞口5000；不归一化、缩放数量、划拨、再平衡或交叉保证金。',execution='BTC C3750/N1000 and ETH C15000/N4000 exact original quantity,LOT,tick,fee,impact,funding,margin and complete NAV;no scaling.',allocation='Rawwholebank[1,1],3750+15000=18750 capital20/80;fixed grosstarget1000+4000=5000. Passive full dollarNAV sum on common union axis;no parentorders,normalization,transfers,rebalance or crossmargin.8native+4parent old reports readonly,6newparents.')
for w,k in itertools.product(WS,KS):
 if (w,k) in parents:grid.append(parents[w,k]);continue
 l,r=btc[w],eth[k];sp=copy.deepcopy(rd(ROOT/parents[.0025,k]['spec']));q={a:v for a,v in sp['parameters'].items() if not a.startswith(('BTC_','ETH_')) and a not in ['prior_370day_source_fingerprint','fixed_total_initial_target_entry_notional_usdt']};name=f'parent_BTCConfirmQ{w}_N1000_ETHTrendK{k}_M4_N4000_raw1_1_C3750_15000_391d';sp.update(name=name,family='btc-directional-confirmation-eth-trend-strength-passive-combination',logic=rules,validation_plan=rel(R/'plan.json'),components=[{'fingerprint':l['fingerprint'],'weight':1},{'fingerprint':r['fingerprint'],'weight':1}]);q.update(initial_capital_usdt=18750,component_capitals_usdt=[3750,15000],component_initial_entry_notionals_usdt=[1000,4000],raw_component_multipliers=[1,1],capital_allocation_fractions=[.2,.8],initial_target_total_notional_usdt=5000,initial_gross_notional_fraction_of_parent_capital=5000/18750,source_component_spec_sha256=[sha(ROOT/l['spec']),sha(ROOT/r['spec'])],actual_native_quantity_and_impact_reused=True,walk_forward_complete30day_folds=13)
 for asset,c in [('BTC',l),('ETH',r)]:
  ch=rd(ROOT/c['spec'])['parameters']
  for a,v in ch.items():
   if a not in ['input_hashes','costs','persistence','prior_370day_source_fingerprint','raw_entry_notional_fraction_of_initial_capital','initial_capital_usdt','fixed_entry_notional_usdt','start_utc','end_utc']:q[asset+'_'+a]=copy.deepcopy(v)
  q[asset+'_bank_capital_usdt']=ch['initial_capital_usdt'];q[asset+'_entry_notional_usdt']=ch['fixed_entry_notional_usdt'];q[asset+'_existing_actual_bank_reused']=True;q[asset+'_new_native_quantity_and_impact_computed']=False
 q['BTC_entry_directional_confirmation_hurdle']=w;sp['parameters']=q;path=R/'specs'/(name+'.json');put(path,sp);fp=reg.fingerprint(sp);assert fp not in rs;row={'scope':'parent','role':'candidate','asset':'COMBO','capital_usdt':18750,'NB':1000,'NE':4000,'BTC_confirmation_hurdle':w,'ETH_trend_strength':k,'source_fingerprints':[l['fingerprint'],r['fingerprint']],'raw_weights':[1,1],'readonly':False,'name':name,'fingerprint':fp,'spec':rel(path),'W':w,'K':k};grid.append(row);batch.append(row)
assert len(refs)==12 and len(batch)==6 and len(grid)==9
p=copy.deepcopy(old)
for a in list(p):
 if a.startswith('additional_predeclared_'):p.pop(a)
p.update(round=R.name,frozen_at_utc=now(),hypothesis=rd(R/'research_design.json')['hypothesis'],rules=rules,axes={'BTC_CONFIRMATION_HURDLE':WS,'ETH_TREND_STRENGTH':KS},axis_semantics={'W':'BTC direction-times-completed-ROC5 strict confirmation hurdle fraction,only new/reversed entry;0 still strictpositive;L29H.03E.005,V10cap.0275,N1000 fixed.','K':'ETH finiteEWMS16 D3 trend slope hurdle fraction;V6cap.05625,R.0075,VW9,M4,age36h,N4000 fixed.'},grid=grid,native_grid=[],native_axes={'BTC':{'axes':[]},'ETH':{'axes':[]}},benchmark_parent_fingerprint=hold['fingerprint'],benchmark_by_cell={f'{w}:{k}':hold['fingerprint'] for w,k in itertools.product(WS,KS)},baseline_by_ETH_trend_strength={str(k):parents[.0025,k]['fingerprint'] for k in KS},baseline_native_fingerprint=ETH[.0075],base_parent_fingerprint=next(g['fingerprint'] for g in grid if g['W']==0 and g['K']==.0075),representative_preset={'W':0,'K':.0075},read_only_references=refs,prior_report={'path':rel(P/'report.json'),'sha256':sha(P/'report.json')},sensitivity={'axes':['BTC_CONFIRMATION_HURDLE','ETH_TREND_STRENGTH'],'index_radius':1,'local_positive3_min':.6,'local_recent_allcost6of8_min':.6,'no_post_outcome_reselection_or_extension':True},primary_source_reads=rd(R/'primary_source_access.json'),limits=rd(R/'research_design.json')['limitations'].split(';'),expected_counts={'new_configs':6,'new_native':0,'new_parents':6,'new_candidate_configs':6,'new_benchmark_configs':0,'new_source_components':0,'new_cost_scenes':18,'read_only_unique_results':12,'read_only_native_models':8,'read_only_parent_models':4,'read_only_cost_scenes':36,'grid_points':9,'native_grid_points':0,'read_only_existing_grid_points':3})
p.pop('baseline_by_BTC_N',None);p.pop('baseline_by_ETH_K',None);controls={str(k):parents[.0025,k] for k in KS};p['additional_predeclared_Q0025_report_controls']=controls;p['grid_index_semantics']=p['axis_semantics']
for n,z in [('plan.json',p),('spec.json',p),('batch.json',batch)]:put(R/n,z)
put(R/'combination_prior_lookup.json',{'passed':True,'complete_registry_IDs_read':len(rs),'rows':lookup,'new_graphs':6,'old_grid_controls':3,'complete_graph_index_checked_before_reserve':True,'no_market_or_account_calculations':True});print('PASS6newgraphs/8native+4parentactualoldrefs/0newnative/3x3fixednotionalgrid',flush=True)
