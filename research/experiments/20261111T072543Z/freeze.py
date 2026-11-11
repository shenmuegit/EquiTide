"""Freeze S/D finite-EWM grid at fixed fundingM4/VW8/R.00875;exactoldcenterreadonly."""
import copy,itertools,json
from decimal import Decimal
from common import *
P=ROOT/'research/experiments/20261111T052407Z';prior=json.loads((P/'plan.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');Ls=[4,5,6];Caps=[.055,.05625,.0575];B=prior['fixed_BTC_fingerprint'];HOLD=prior['benchmark_parent_fingerprint'];refs={};batch=[];grid=[];nativegrid=[];mapping={}
key=lambda sp:sorted((x['fingerprint'],Decimal(str(x['weight']))) for x in sp['components'])
FORMULA='min(hardcap,ratio*pastVW_sample_daily_logvol*latest_eligible_completed_actual_interval_hours/24)'
OLD_FORMULA='min(hardcap,ratio*past10_sample_daily_logvol*latest_eligible_completed_actual_interval_hours/24)'
def normalized(q):
 q=copy.deepcopy(q)
 if q.get('entry_funding_filter')=='volatility_relative_median_of_latest_N_eligible_realized_settlements_new_entry_only':
  vw=q.pop('entry_funding_budget_volatility_window_days',10)
  if vw!=10:q['entry_funding_budget_volatility_window_days']=vw
  if q.get('entry_funding_budget_formula') in [FORMULA,OLD_FORMULA]:q['entry_funding_budget_formula']=FORMULA
 return q
parents_by_graph={}
for fp,z in rs.items():
 if z.get('spec',{}).get('kind')=='combination':parents_by_graph.setdefault(tuple(key(z['spec'])),[]).append(fp)
def parent_for(nf):
 x=parents_by_graph.get(tuple(sorted([(B,Decimal(1)),(nf,Decimal(1))])),[]);assert len(x)==1;return x[0]
def reference(fp):
 if fp in refs:return
 z=rs[fp];assert z['result_available'] and sha(ROOT/z['report'])==z['report_sha256'];sp=z['spec'];c=next(c for c in json.loads((ROOT/z['report']).read_text())['configs'].values() if c['fingerprint']==fp);scope='native' if sp['kind']=='strategy' else 'parent';ref={k:c[k] for k in ['name','fingerprint','spec','archive','archive_sha256']};ref.update(scope=scope,asset=sp['universe'][0].split('/')[0] if scope=='native' else 'COMBO',capital_usdt=sp['parameters']['initial_capital_usdt'],report=z['report'],report_sha256=z['report_sha256'],spec_sha256=sha(ROOT/c['spec']),status=z['status']);assert sha(ROOT/ref['archive'])==ref['archive_sha256'];refs[fp]=ref
 if scope=='parent':
  ref.update(source_fingerprints=[x['fingerprint'] for x in sp['components']],raw_weights=[x['weight'] for x in sp['components']])
  for x in sp['components']:reference(x['fingerprint'])
C='1675ee38460d440cf728fb469d03ad259d5b5221c35107dc8d342cbd929ddc69';CP=parent_for(C);reference(CP);previous=prior['previous_price_center'];reference(previous['parent']);U='dd44fcda1ac5e61dcf9c2350625af79811695d323e58f7048c6e0b37d5b66569';UP=parent_for(U);reference(UP);reference(HOLD);assert len(refs)==10 and sum(z['scope']=='native' for z in refs.values())==6
impl={'path':rel(R/'engine.py'),'sha256':sha(R/'engine.py'),'accounting_unchanged_from':rel(P/'engine.py'),'signal_change':'Onlycapguardadds.05625afteractualsyntheticmissingdomainRED;existingL4/5/6domain and all accounting unchanged.'}
logic=copy.deepcopy(prior['rules']);logic.update(signal='ETH contrarianROC L[4,5,6] x PRICE entry capVC[.055,.05625,.0575];PRICE samplelogvolV6fixed,S16/D3/K.0075/H.02/E.0075fixed. Sameactualqretained,reverseclosesfirst,next00:01OPEN;fundingM4/BUDGET_VW8/R.00875/hardcap.0002 unchanged,latestmatureactualinterval,signedmedian,age1..36h andavailable<=signal.',validation='3x3 L/VCgrid,4exactoldcellsreadonly;5newETH+5wholebankparents/30scenes after10reserves;predeclaredL5VC.05625. Originalbanks/N/raw1,1/calendar/gatesunchanged;source33coversBTC30/ETHsignal19cost21. All4owncurrentwindowsmarksonly;reuseactualNov11_00/dailyonce,do notcapturefuture08. Reuseddevelopmenthistorynotfinal/future.',native_implementation=impl)
sources=prior['sources'];inventory=[]
for L,VC in itertools.product(Ls,Caps):
 V=6
 pars={**rs[C]['spec']['parameters'],'lookback_days':L,'entry_volatility_window_days':V,'entry_volatility_ceiling':VC};matches=[fp for fp,z in rs.items() if z.get('spec',{}).get('kind')=='strategy' and z['spec'].get('universe')==['ETH/USDT'] and normalized(z['spec']['parameters'])==normalized(pars)];readonly=(L,VC) in [(4,.055),(5,.055),(5,.0575),(6,.055)];attrs={'L':L,'V':V,'H':.02,'E':.0075,'R':.00875,'VW':8,'M':4,'S':16,'D':3,'K':.0075,'VC':VC,'hard_funding_cap':.0002}
 if readonly:
  assert len(matches)==1;efp=matches[0];pfp=parent_for(efp);assert rs[efp]['result_available'] and rs[pfp]['result_available'];reference(pfp)
 else:
  assert not matches;sp=copy.deepcopy(rs[C]['spec']);name=f'rocceil_370_ETH_L{L}_VC{int(Decimal(str(VC))*100000)}';sp.update(name=name,validation_plan=rel(R/'plan.json'),sources=sources,logic=copy.deepcopy(logic),parameters=pars);path=R/'specs'/(name+'.json');path.parent.mkdir(exist_ok=True);put(path,sp);efp=reg.fingerprint(sp);assert efp not in rs;batch.append({**attrs,'name':name,'fingerprint':efp,'scope':'native','role':'component','asset':'ETH','capital_usdt':15000,'N':4500,'spec':rel(path),'reference_fingerprint':C});mapping[efp]=C
  sp=copy.deepcopy(rs[CP]['spec']);name=f'rocceil_370_parent_BTC29H3_ETH_L{L}_VC{int(Decimal(str(VC))*100000)}';sp.update(name=name,logic=copy.deepcopy(logic),components=[{'fingerprint':B,'weight':1},{'fingerprint':efp,'weight':1}],validation_plan=rel(R/'plan.json'),sources=sources);sp['parameters'].update(ETH_lookback_days=L,ETH_entry_volatility_window_days=V,ETH_entry_volatility_ceiling=VC,source_component_spec_sha256=[refs[B]['spec_sha256'],sha(path)]);path=R/'specs'/(name+'.json');put(path,sp);pfp=reg.fingerprint(sp);assert pfp not in rs and tuple(key(sp)) not in parents_by_graph;batch.append({**attrs,'name':name,'fingerprint':pfp,'scope':'parent','role':'candidate','asset':'COMBO','capital_usdt':18750,'BTC_capital_usdt':3750,'ETH_capital_usdt':15000,'N':1000,'BTC_N':1000,'ETH_N':4500,'source_fingerprints':[B,efp],'reference_fingerprint':CP,'spec':rel(path)});mapping[pfp]=CP
 nativegrid.append({**attrs,'N':4500,'fingerprint':efp,'readonly':readonly,'role':'component'});grid.append({**attrs,'N':1000,'fingerprint':pfp,'readonly':readonly,'role':'candidate'});inventory.append({'L':L,'PRICE_V':V,'VC':VC,'D':3,'K':.0075,'BUDGET_VW':8,'native_fingerprint':efp,'parent_fingerprint':pfp,'readonly_existing_result':readonly,'semantic_matches':matches})
batch.sort(key=lambda z:(z['scope']!='native',z['L'],z['VC']));assert len(batch)==10 and len(refs)==16 and sum(z['scope']=='native' for z in refs.values())==9
counts={'new_configs':10,'new_native':5,'new_parents':5,'new_candidate_configs':5,'new_source_components':5,'new_benchmark_configs':0,'new_cost_scenes':30,'old_current_parent_cells':4,'old_current_native_cells':4,'old_external_contrarian_controls':2,'old_benchmark_parents':1,'read_only_unique_results':16}
p=copy.deepcopy(prior);p.update(round=R.name,frozen_at_utc=now(),hypothesis='固定PRICE_V6/S16/D3/K0.75%/H2%/E0.75%及资金费M4/VW8/R0.00875，预设快ROC L4/5/6×VC5.5/5.625/5.75%，4格旧结果只读，5新ETH+5全银行组合/30成本场景。事前代表L5/VC5.625%。仅扩cap guard.05625，原核算/银行/N/raw1,1/失败门槛不变。四原账户本窗均仅闭合估值，不重复00资金费/日决策，也不提前捕获未来08；SMAfull65日上下文仍是032206完整输入',entry_hurdles=[.02],exit_buffers=[.0075],slow_windows=[16],slope_lags=[3],fast_lookbacks=Ls,price_vol_windows=[6],slope_strengths=[.0075],volatility_ceilings=Caps,budget_vol_windows=[8],carry_ratios=[.00875],funding_counts=[4],grid=grid,native_grid=nativegrid,primary_control_fingerprint=CP,external_control_fingerprints=[CP,previous['parent'],UP],predeclared_reference_by_fingerprint=mapping,read_only_references=refs,rules=logic,expected_counts=counts,sensitivity={'candidate_axes':['ETH_ROC_L','ETH_volatility_ceiling_VC'],'native_component_axis':['ETH_ROC_L','ETH_volatility_ceiling_VC'],'index_radius':1,'includes_center':True,'local_positive3_min':.6,'local_recent_allcost6of8_min':.6,'scope':'5new+4actualoldreadonlypergrid;oldcanonicalstatusunchanged'},representative_preset={'K':.0075,'VC':.05625,'V':6,'VW':8,'R':.00875,'M':4,'L':5,'H':.02,'E':.0075,'S':16,'D':3,'N':1000,'scope':'parent','readonly':False},prior_report={'path':rel(P/'report.json'),'sha256':sha(P/'report.json')},new_native_policy_implementation=impl,new_engine_sha256=sha(R/'engine.py'),sources=sources,native_policy_sources={'unchanged_accounting':{'path':rel(CORE_PATH),'sha256':sha(CORE_PATH)},'parameterized_ETH_policy':impl},current_center={'native':C,'parent':CP},previous_budget_center=previous,previous_price_center=previous,unfiltered_control={'native':U,'parent':UP},fixed_ETH_D=3,fixed_ETH_K=.0075,fixed_ETH_VC=None)
limits=[];chars=''
for item in p['limits']:
 if isinstance(item,str) and len(item)==1:chars+=item
 else:
  if chars:limits.append(chars);chars=''
  limits.append(item)
if chars:limits.append(chars)
p['limits']=limits
p['trend_windows']=[16];p['time_boundaries']={**prior['time_boundaries'],'causality':logic['signal'],'calendar_frozen_before_current_evaluation_utc':now()}
for n,z in [('plan.json',p),('spec.json',p),('batch.json',batch),('source_inventory_before_freeze.json',{'records_read':len(rs),'new_native_count':5,'new_parent_count':5,'read_only_unique_results':16,'complete_parameters_and_numeric_parent_graph_checked':True,'rows':inventory}),('semantic_inventory.json',{'new_configs':batch,'read_only_unique_results':16,'new_native_evaluations':5,'old_center_native':C,'old_center_parent':CP,'fixed_BTC_fingerprint':B,'no_old_NAV_scaling':True})]:put(R/n,z)
print(json.dumps(counts),flush=True)
