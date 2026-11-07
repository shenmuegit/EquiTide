"""Predeclare fourteen genuinely new full-bank parents on BTC lookback/D/VC axes."""
import copy,itertools,json
from decimal import Decimal
from common import *
P=ROOT/'research/experiments/20261107T024625Z';prior=json.loads((P/'plan.json').read_text());oldrep=json.loads((ROOT/'research/experiments/20261106T224426Z/report.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl')
Ls=[27,29,31];Ds=[6,7,8];VCs=[.04,.045,.05];HOLD='554d265dc8906ec3e55fbca9fe593c3112540d94ada7e88d77594cbd3e3d0886'
inventory=json.loads((R/'parent_graph_inventory_preproposal.json').read_text());assert inventory['new']==14 and inventory['old']==13 and inventory['actual_parent_evaluations']==0
base={(c['D'],c['VC']):c for c in oldrep['all_current_grid'].values() if c['BTC_H']==.04};cat=json.loads((R/'readonly_native_identity_catalog.json').read_text())['rows'];BTC={x['L']:x['fp'] for x in cat if x['asset']=='BTC' and x['H']==.04 and x['L'] in Ls};ETH={(d,v):base[d,v]['source_fingerprints'][1] for d,v in itertools.product(Ds,VCs)}
refs={};batch=[];grid=[];native_grid=[];mapping={}
def reference(fp):
 if fp in refs:return
 z=rs[fp];assert z['result_available'] and z['status'] in ['passed','rejected'] and sha(ROOT/z['report'])==z['report_sha256']
 sp=z['spec'];cfg=next(x for x in json.loads((ROOT/z['report']).read_text())['configs'].values() if x['fingerprint']==fp);scope='native' if sp['kind']=='strategy' else 'parent'
 ref={k:cfg[k] for k in ['name','fingerprint','spec','archive','archive_sha256']};ref.update(scope=scope,asset=sp['universe'][0].split('/')[0] if scope=='native' else 'COMBO',capital_usdt=sp['parameters']['initial_capital_usdt'],report=z['report'],report_sha256=z['report_sha256'],spec_sha256=sha(ROOT/cfg['spec']),status=z['status'])
 assert sha(ROOT/ref['archive'])==ref['archive_sha256'];refs[fp]=ref
 if scope=='parent':
  ref.update(source_fingerprints=[x['fingerprint'] for x in sp['components']],raw_weights=[x['weight'] for x in sp['components']])
  for x in sp['components']:reference(x['fingerprint'])
reference(HOLD)
for row in inventory['rows']:
 for fp in row['component_fingerprints']:reference(fp)
 for fp in row['existing_numeric_graphs']:reference(fp)
assert len(refs)==28 and sum(x['scope']=='native' for x in refs.values())==14 and (P/'engine.py').read_bytes()==(R/'engine.py').read_bytes()
impl={'path':rel(R/'engine.py'),'sha256':sha(R/'engine.py'),'previous_engine':rel(P/'engine.py'),'previous_sha256':sha(P/'engine.py'),'only_code_change':'None;whole nativeengine unchanged. All14oldnativebanks/42costledgers readonly,zero nativepolicy/order calls.','native_simulate_AST_unchanged':True,'entry_filter_AST_unchanged':True}
logic=copy.deepcopy(prior['rules']);logic.update(signal='Existing BTC ROC27/29/31,H4%,E1%,C3750/N1000 and existing ETH contrarianROC5,H2%,E0.5%,finiteEWM24 beta23/25,K2%,D6/7/8,entry-onlypastV10cap4/4.5/5%,C15000/N4500. No newnativepolicy or executions.',validation='Predeclared BTC_lookback x ETH_D x ETH_VC radius1 includingcenter,27cells14new13old,all9ETHnativecells readonly. All old canonical statuses/criteria unchanged. Continuous370d12x30+10tail,recentday330inherited40d8x5,noreset. All frozen gates unchanged;local3xpositive andstrictrecent>=.6. Nofit/labels,purge0/embargo0,source33pastcontext/max32closes;reuseddevelopmenthistory,notuntouchedfinal/future.',benchmark='SameC18750/N1000BTC+N4500ETHholdparent/cash0readonly. Eachnewparent comparedwith old BTC29/H4 sameD/K/VC andsamewholebankcapital/notionals;only BTClookback differs.',native_implementation=impl)
sources=copy.deepcopy(prior['sources'])
graphs={}
for fp,z in rs.items():
 sp=z.get('spec',{})
 if sp.get('kind')=='combination':graphs.setdefault(tuple(sorted((x['fingerprint'],Decimal(str(x['weight']))) for x in sp['components'])),[]).append(fp)
rows=[]
for l,d,v in itertools.product(Ls,Ds,VCs):
 fps=[BTC[l],ETH[d,v]];matches=graphs.get(tuple(sorted((x,Decimal(1)) for x in fps)),[]);assert len(matches)<=1
 ro=bool(matches)
 if ro:fp=matches[0];assert fp in refs
 else:
  reference_fp=base[d,v]['fingerprint'];sp=copy.deepcopy(rs[reference_fp]['spec']);name=f'btcLvolK2_370_parent_BL{l}_D{d}_VC{round(v*1e6)}ppm'
  sp.update(name=name,logic=copy.deepcopy(logic),components=[{'fingerprint':x,'weight':1} for x in fps],validation_plan=rel(R/'plan.json'),sources=sources)
  q=sp['parameters'];q.update(BTC_lookback_days=l,BTC_return_hurdle=.04,ETH_entry_volatility_ceiling=v,ETH_trend_slope_hurdle_fraction=.02,BTC_existing_actual_bank_reused=True,BTC_new_native_quantity_and_impact_computed=False,actual_native_quantity_and_impact_reused=True,ETH_new_native_quantity_and_impact_computed=False,source_component_spec_sha256=[refs[x]['spec_sha256'] for x in fps])
  path=R/'specs'/(name+'.json');path.parent.mkdir(exist_ok=True);put(path,sp);fp=reg.fingerprint(sp);assert fp not in rs
  row={'name':name,'fingerprint':fp,'scope':'parent','role':'candidate','asset':'COMBO','capital_usdt':18750,'BTC_capital_usdt':3750,'ETH_capital_usdt':15000,'BTC_L':l,'BTC_H':.04,'BTC_N':1000,'ETH_N':4500,'L':5,'H':.02,'E':.005,'S':24,'D':d,'K':.02,'VC':v,'N':1000,'source_fingerprints':fps,'reference_fingerprint':reference_fp,'spec':rel(path)};batch.append(row);mapping[fp]=reference_fp
 grid.append({'L':5,'H':.02,'E':.005,'S':24,'D':d,'K':.02,'VC':v,'N':1000,'BTC_L':l,'BTC_H':.04,'fingerprint':fp,'readonly':ro,'role':'candidate'});rows.append({'BTC_L':l,'BTC_H':.04,'D':d,'K':.02,'VC':v,'native_fingerprints':fps,'parent':fp,'readonly':ro,'numeric_graph_matches':matches})
for d,v in itertools.product(Ds,VCs):native_grid.append({'L':5,'H':.02,'E':.005,'S':24,'D':d,'K':.02,'VC':v,'N':4500,'fingerprint':ETH[d,v],'readonly':True,'role':'component'})
assert len(batch)==14 and sum(g['readonly'] for g in grid)==13
counts={'new_configs':14,'new_native':0,'new_parents':14,'new_candidate_configs':14,'new_source_components':0,'new_benchmark_configs':0,'new_cost_scenes':42,'old_current_parent_cells':13,'old_current_native_cells':9,'old_external_contrarian_controls':9,'old_benchmark_parents':1,'read_only_unique_results':28}
p={k:copy.deepcopy(prior[k]) for k in ['data','time_boundaries','sources','limits']}
p['limits']=p['limits'].replace(' Official Binance documentation read successfully this round; actual current API data still required and audited.',' Existing official data/source provenance retained; actual new public account data separately captured and audited.')
p.update(round=R.name,frozen_at_utc=now(),hypothesis='上轮K3网格15新组合虽全期三档成本净正，但11个近期/邻域淘汰，4个历史通过仍被旧L29匹配对照支配。本轮固定较低ETH K2%，预声明BTC回看27/29/31日、H4%及ETH D6/7/8、VC4/4.5/5%全27格，检验较不稀疏ETH门槛是否支持BTC时钟变化。完整图查重13旧格（L29九格、L31中间VC三格、L27一格），只补14个新组合；复用14原生银行42成本路径和28旧结果，0新原生policy/订单。Raw[1,1]完整银行不归一化、门槛不改，不将重复历史称未触碰最终/独立未来。四原冻结账户本轮仅续自己的闭合mark/风险，不重复午夜或采纳研究规则。',slope_lags=Ds,volatility_ceilings=VCs,fixed_ETH_K=.02,BTC_lookbacks=Ls,BTC_hurdles=[.04],entry_notionals=[1000],fixed_BTC_entry_notional=1000,fixed_BTC_L=None,fixed_BTC_H=.04,fixed_bank_capitals=[3750,15000],fixed_ETH_entry_notional=4500,grid=grid,native_grid=native_grid,benchmarks=[{'L':0,'H':0,'E':0,'S':None,'D':None,'K':None,'VC':None,'N':1000,'fingerprint':HOLD,'readonly':True,'role':'benchmark'}],benchmark_parent_fingerprint=HOLD,current_center_fingerprint=base[7,.045]['fingerprint'],external_control_fingerprints=[base[d,v]['fingerprint'] for d,v in itertools.product(Ds,VCs)],primary_control_fingerprint=base[7,.045]['fingerprint'],predeclared_reference_by_fingerprint=mapping,read_only_references=refs,rules=logic,costs=rs[BTC[29]]['spec']['parameters']['costs'],expected_counts=counts,sensitivity={'candidate_axes':['BTC_lookback_days','ETH_slope_lag_D','ETH_entry_volatility_ceiling_VC'],'native_component_axis':['ETH_slope_lag_D','ETH_entry_volatility_ceiling_VC'],'index_radius':1,'includes_center':True,'local_positive3_min':.6,'local_recent_allcost6of8_min':.6,'scope':'27parentcells14new13old;9ETHcellsreadonly,canonicaloldstatusesunchanged'},representative_preset={'BTC_L':29,'BTC_H':.04,'D':7,'K':.02,'VC':.045,'N':1000,'scope':'parent','readonly':True,'original_status':rs[base[7,.045]['fingerprint']]['status']},prior_report={'path':rel(P/'report.json'),'sha256':sha(P/'report.json')},new_native_policy_implementation=impl,new_engine_sha256=sha(R/'engine.py'),native_policy_sources={'readonly_native_engine':impl,'accounting':{'path':rel(CORE_PATH),'sha256':sha(CORE_PATH)}},budget_bracket_readonly_reports={})
p['time_boundaries'].update(causality='ExistingBTC27/29/31H4 and ETHK2/D6/7/8/VC4/4.5/5 ledgers readonly;source33/max32pastcloses,nofits/labels,purge0/embargo0. All14parents reserved before valuation;alignedfull370dayNAV,notuntouchedhistory.',calendar_frozen_before_current_evaluation_utc=now())
for name,obj in [('plan.json',p),('spec.json',p),('batch.json',batch),('engine_policy_domain_change.json',impl),('source_inventory_before_freeze.json',{'records_read':len(rs),'new_native':0,'new_parents':14,'old_unique_results':28,'old_native_banks':14,'rows':rows,'native_accounting_AST_unchanged':True}),('semantic_inventory.json',{'new_configs':batch,'read_only_unique_results':28,'new_native_evaluations':0,'old_baseline_cells':13,'no_old_NAV_scaling':True}),('novelty_precheck.json',{'records_read':len(rs),'rows':rows,'numeric_and_reordered_graphs_checked':True,'new_native':0,'new_parents_expected':14,'same_graph_prior_results_or_reservations':13})]:put(R/name,obj)
print(json.dumps(counts),flush=True)
