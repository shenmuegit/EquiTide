"""Inspect predeclared future definitions only; never execute a financial/account model."""
import copy,itertools,json
from decimal import Decimal
from common import *
rd=lambda p:json.loads(p.read_text());b=rd(R/'next_parameter_availability_binding.json');assert b['bound_before_readonly_execution'] and sha(Path(__file__))==b['source_sha256'] and b['new_financial_account_or_cashflow_evaluations']==0
for path,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/path)==h
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');p=rd(R/'plan.json');decl=rd(R/'next_direction_predeclaration.json');assert decl['before_any_current_reserve_or_outcomes'] and not decl['selection_uses_performance'];ignored={'persistence','prior_370day_source_fingerprint'};index={}
def key(cs):
 sums={}
 for c in cs:sums[c['fingerprint']]=sums.get(c['fingerprint'],Decimal(0))+Decimal(str(c['weight']))
 return tuple(sorted(sums.items()))
for fp,z in rs.items():
 sp=z.get('spec',{});q=sp.get('parameters',{})
 if sp.get('kind')=='combination' and q.get('start_utc')=='2025-10-19T00:01:00Z' and q.get('end_utc')=='2026-11-14T00:01:00Z' and (z.get('result_available') or z['status']=='reserved'):index.setdefault(key(sp['components']),[]).append(fp)
def source(basefp,axis,value):
 base=rs[basefp]['spec'];q0=copy.deepcopy(base['parameters']);q0[axis]=value;choices=[(fp,z) for fp,z in rs.items() if z.get('result_available') and z.get('spec',{}).get('kind')==base['kind'] and z['spec'].get('market')==base['market'] and z['spec'].get('timeframe')==base['timeframe'] and z['spec'].get('universe')==base['universe'] and all(z['spec']['parameters'].get(k)==q0.get(k) for k in set(z['spec']['parameters'])|set(q0) if k not in ignored)]
 if len(choices)!=1:return None
 fp,z=choices[0];assert sha(ROOT/z['report'])==z['report_sha256'];return fp
batches=[]
for definition in decl['ordered_definition_only_priorities']:
 BTC={x:source('41de4309229b892489a07574af07a73ae93229a35c118558ed60362285e90c89',definition['BTC_axis'],x) for x in definition['BTC_values']};ETH={x:source(p['baseline_native_fingerprint'],definition['ETH_axis'],x) for x in definition['ETH_values']};available=all(BTC.values()) and all(ETH.values())
 if not available:batches.append({**definition,'all_fixed_context_native_sources_available':False,'new_financial_evaluations':0});continue
 cells=[{'BTC_value':w,'ETH_value':k,'BTC':BTC[w],'ETH':ETH[k],'existing_exact_graphs':index.get(key([{'fingerprint':BTC[w],'weight':1},{'fingerprint':ETH[k],'weight':1}]),[])} for w,k in itertools.product(BTC,ETH)]
 batches.append({**definition,'BTC_sources':BTC,'ETH_sources':ETH,'cells':cells,'all_fixed_context_native_sources_available':True,'new_graphs':sum(not z['existing_exact_graphs'] for z in cells),'old_graphs':sum(bool(z['existing_exact_graphs']) for z in cells),'representative_preset':{'W':definition['BTC_values'][0],'K':definition['ETH_values'][0]},'default_control_preset':{'W':definition['BTC_default'],'K':definition['ETH_default']}})
selected=next((z for z in batches if z.get('new_graphs')),None)
out={'passed':True,'recorded_utc':now(),'source_sha256':b['source_sha256'],'registry_IDs_read':len(rs),'source_metadata_sha256':sha(R/'source_inventory.json'),'complete_component_graph_index_built_before_lookup':True,'ordered_priorities_frozen_in_source_before_lookup':decl['ordered_definition_only_priorities'],'priorities_declaration_sha256':sha(R/'next_direction_predeclaration.json'),'batches':batches,'first_definition_only_available_batch':selected,'selection_uses_performance':False,'current_grid_or_representative_changed':False,'new_strategy_account_or_cashflow_evaluations':0,'all_future_actual_configs_require_fresh_full_registry_lookup_complete_spec_and_successful_reserve_before_calculation':True,'raw_bank_weights':[1,1],'capital_usdt':[3750,15000],'entry_targets_usdt':[1000,4000],'no_normalization_scaling_transfers_rebalance_or_parent_orders':True};put(R/'next_parameter_availability.json',out)
path=R/'next_research_state.json';before=rd(path);after=copy.deepcopy(before);after['next_definition_only_parameter_availability']={'path':rel(R/'next_parameter_availability.json'),'sha256':sha(R/'next_parameter_availability.json'),'first_batch_axes':{k:selected[k] for k in ['BTC_axis','BTC_values','ETH_axis','ETH_values','new_graphs','old_graphs']} if selected else None,'fresh_lookup_and_full_prebinding_required_before_next_reserve':True,'next_metadata_selector_must_be_adapted_before_execution':True,'reason':'First available batch in immutable pre-current definition priority order; no current financial outcomes used.','new_financial_evaluations':0};oldhash=sha(path);put(path,after);check=copy.deepcopy(after);check.pop('next_definition_only_parameter_availability');assert check==before
for path,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/path)==h
put(R/'next_parameter_availability_verification.json',{'passed':True,'source_sha256':b['source_sha256'],'current_grid_unchanged':True,'all_old_next_state_JSON_fields_unchanged':True,'next_state_before_sha256':oldhash,'next_state_after_sha256':sha(R/'next_research_state.json'),'new_strategy_account_or_cashflow_evaluations':0});print(json.dumps({'passed':True,'metadata_only':True,'selected_axes':{k:selected[k] for k in ['BTC_axis','BTC_values','ETH_axis','ETH_values','new_graphs','old_graphs']} if selected else None,'new_evaluations':0}))
