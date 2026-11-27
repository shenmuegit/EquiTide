"""Definition-only full native parameter and component-graph lookup for the previously planned BTC grid."""
import copy,itertools,json
from decimal import Decimal
from common import *
rd=lambda p:json.loads(p.read_text());P=ROOT/'research/experiments/20261127T160858Z';future=rd(P/'next_direction_predeclaration.json');assert future['new_native_axis_grid']=={'lookback_days':[28,29,30],'return_hurdle':[.0275,.03,.0325]} and future['new_actual_strategy_account_or_cashflow_evaluations']==0
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');base=rs['41de4309229b892489a07574af07a73ae93229a35c118558ed60362285e90c89']['spec'];ignored={'persistence','prior_370day_source_fingerprint'}
def eq(a,b):return all(a.get(k)==b.get(k) for k in set(a)|set(b) if k not in ignored)
def graphkey(cs):
 totals={}
 for z in cs:totals[z['fingerprint']]=totals.get(z['fingerprint'],Decimal(0))+Decimal(str(z['weight']))
 return tuple(sorted(totals.items()))
graphs={}
for fp,z in rs.items():
 sp=z.get('spec',{});q=sp.get('parameters',{})
 if sp.get('kind')=='combination' and q.get('start_utc')==base['parameters']['start_utc'] and q.get('end_utc')==base['parameters']['end_utc'] and (z.get('result_available') or z['status']=='reserved'):graphs.setdefault(graphkey(sp['components']),[]).append(fp)
rows=[];ETH='a34c0bd6e523db4188b1b6f27d2e8efec9b679106ae19d9cd97438b6dbae3984'
for L,H in itertools.product([28,29,30],[.0275,.03,.0325]):
 sp=copy.deepcopy(base);sp['parameters'].update(lookback_days=L,return_hurdle=H);matches=[fp for fp,z in rs.items() if z.get('spec',{}).get('kind')==base['kind'] and z['spec'].get('market')==base['market'] and z['spec'].get('timeframe')==base['timeframe'] and z['spec'].get('universe')==base['universe'] and eq(z['spec']['parameters'],sp['parameters']) and (z.get('result_available') or z['status']=='reserved')];assert len(matches)<=1,(L,H,matches)
 if matches:fp=matches[0];assert rs[fp]['result_available'] and sha(ROOT/rs[fp]['report'])==rs[fp]['report_sha256'];sp=copy.deepcopy(rs[fp]['spec'])
 else:fp=reg.fingerprint(sp);assert fp not in rs or not rs[fp].get('result_available') and rs[fp]['status'] in ['blocked','abandoned']
 parents=graphs.get(graphkey([{'fingerprint':fp,'weight':1},{'fingerprint':ETH,'weight':1}]),[]) if matches else [];assert len(parents)<=1
 rows.append({'W':L,'K':H,'native_fingerprint':fp,'native_spec_template':sp,'native_actual_matches':matches,'parent_actual_matches':parents})
out={'passed':True,'recorded_utc':now(),'full_logical_registry_IDs_read':len(rs),'prior_predeclaration':{'path':rel(P/'next_direction_predeclaration.json'),'sha256':sha(P/'next_direction_predeclaration.json')},'axes':{'BTC_MAIN_LOOKBACK_DAYS':[28,29,30],'BTC_ENTRY_RETURN_HURDLE':[.0275,.03,.0325]},'representative_preset':{'W':28,'K':.0275},'default_control_preset':{'W':29,'K':.03},'ETH_fixed_fingerprint':ETH,'rows':rows,'new_native':sum(not z['native_actual_matches'] for z in rows),'new_parents':sum(not z['parent_actual_matches'] for z in rows),'native_semantic_lookup_ignored_only_explanatory_fields':sorted(ignored),'complete_component_graph_index_built_before_lookup':True,'new_financial_or_account_evaluations':0,'selection_uses_performance':False};put(R/'joint_parameter_metadata_availability.json',out);print(json.dumps({k:out[k] for k in ['passed','new_native','new_parents','representative_preset','default_control_preset','new_financial_or_account_evaluations']}),flush=True)
