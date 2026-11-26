"""Inspect future parameter combinations by definitions only; no strategy or account execution."""
import copy,hashlib,itertools,json,sys
from datetime import datetime,timezone
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
b=rd(R/'next_parameter_availability_binding.json');assert b['bound_before_readonly_execution'] and sha(Path(__file__))==b['source_sha256'] and b['new_financial_account_or_cashflow_evaluations']==0
for p,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/p)==h
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');inv=rd(R/'source_inventory.json')
def key(xs):
 totals={}
 for z in xs:totals[z['fingerprint']]=totals.get(z['fingerprint'],Decimal(0))+Decimal(str(z['weight']))
 return tuple(sorted(totals.items()))
index={}
for fp,z in rs.items():
 sp=z.get('spec',{});q=sp.get('parameters',{})
 if sp.get('kind')=='combination' and q.get('start_utc')=='2025-10-19T00:01:00Z' and q.get('end_utc')=='2026-11-14T00:01:00Z' and (z.get('result_available') or z['status']=='reserved'):index.setdefault(key(sp['components']),[]).append(fp)
def native(asset,axis,values):
 out={};base=inv['assets'][asset]['baseline_parameters']
 for value in values:
  choices=[z for z in inv['assets'][asset]['rows'] if z['parameters'].get(axis)==value and all(z['parameters'].get(k)==base.get(k) for k in set(z['parameters'])|set(base) if k not in {axis,'persistence','prior_370day_source_fingerprint'})]
  if len(choices)!=1:return None
  z=choices[0];assert rs[z['fingerprint']]['result_available'] and sha(ROOT/z['report'])==z['report_sha256'];out[value]=z['fingerprint']
 return out
priorities=[('entry_directional_confirmation_hurdle',[.0025,.005],'entry_funding_budget_volatility_window_days',[8,9,10]),('entry_volatility_window_days',[9,10,11],'entry_funding_budget_volatility_window_days',[8,9,10]),('entry_volatility_ceiling',[.026125,.0275,.028875],'entry_funding_budget_volatility_window_days',[8,9,10]),('entry_volatility_window_days',[9,10,11],'entry_funding_volatility_ratio',[.00625,.0075,.00875]),('entry_volatility_ceiling',[.026125,.0275,.028875],'entry_funding_volatility_ratio',[.00625,.0075,.00875]),('return_hurdle',[.0275,.03,.0325],'trend_slope_lag_days',[2,3,4]),('entry_volatility_window_days',[9,10,11],'entry_volatility_window_days',[5,6,7]),('exit_buffer_fraction',[.00375,.005,.00625],'exit_buffer_fraction',[.00625,.0075,.00875]),('return_hurdle',[.0275,.03,.0325],'exit_buffer_fraction',[.00625,.0075,.00875]),('exit_buffer_fraction',[.00375,.005,.00625],'trend_slope_lag_days',[2,3,4]),('entry_volatility_window_days',[9,10,11],'trend_slope_lag_days',[2,3,4]),('entry_volatility_ceiling',[.026125,.0275,.028875],'exit_buffer_fraction',[.00625,.0075,.00875]),('return_hurdle',[.0275,.03,.0325],'entry_funding_budget_volatility_window_days',[8,9,10]),('exit_buffer_fraction',[.00375,.005,.00625],'entry_funding_budget_volatility_window_days',[8,9,10]),('return_hurdle',[.0275,.03,.0325],'entry_volatility_window_days',[5,6,7]),('entry_directional_confirmation_hurdle',[.0025,.005],'exit_buffer_fraction',[.00625,.0075,.00875])]
rows=[]
for ax,vs,ay,ks in priorities:
 A=native('BTC',ax,vs);B=native('ETH',ay,ks);z={'BTC_axis':ax,'BTC_values':vs,'ETH_axis':ay,'ETH_values':ks,'all_fixed_context_native_sources_available':A is not None and B is not None}
 if z['all_fixed_context_native_sources_available']:
  cells=[{'BTC_value':w,'ETH_value':k,'BTC':A[w],'ETH':B[k],'existing_exact_graphs':index.get(key([{'fingerprint':A[w],'weight':1},{'fingerprint':B[k],'weight':1}]),[])} for w,k in itertools.product(vs,ks)];z.update(BTC_sources=A,ETH_sources=B,cells=cells,new_graphs=sum(not x['existing_exact_graphs'] for x in cells),old_graphs=sum(bool(x['existing_exact_graphs']) for x in cells))
 rows.append(z)
chosen=next((x for x in rows if x.get('new_graphs',0)>0),None)
out={'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':b['source_sha256'],'registry_IDs_read':len(rs),'source_metadata_sha256':sha(R/'source_inventory.json'),'complete_component_graph_index_built_before_lookup':True,'ordered_priorities_frozen_in_source_before_lookup':priorities,'batches':rows,'first_definition_only_available_batch':chosen,'selection_uses_performance':False,'current_grid_or_representative_changed':False,'new_strategy_account_or_cashflow_evaluations':0,'all_future_actual_configs_require_fresh_full_registry_lookup_complete_spec_and_successful_reserve_before_calculation':True,'raw_bank_weights':[1,1],'capital_usdt':[3750,15000],'entry_targets_usdt':[1000,4000],'no_normalization_scaling_transfers_rebalance_or_parent_orders':True};put(R/'next_parameter_availability.json',out)
path=R/'next_research_state.json';before=rd(path);after=copy.deepcopy(before);after['next_definition_only_parameter_availability']={'path':str((R/'next_parameter_availability.json').relative_to(ROOT)),'sha256':sha(R/'next_parameter_availability.json'),'first_batch_axes':{k:chosen[k] for k in ['BTC_axis','BTC_values','ETH_axis','ETH_values','new_graphs','old_graphs']} if chosen else None,'fresh_lookup_and_full_prebinding_required_before_next_reserve':True,'next_metadata_selector_must_be_adapted_before_execution':True,'reason':'Refresh the ordered definition-only batches, including newly predeclared parameter crosses. Read this metadata inventory before running the next metadata.py; adapt the selector for the new axes, then refresh the complete registry before any reservation. Do not rerun old completed configurations.','new_financial_evaluations':0};oldhash=sha(path);put(path,after);check=copy.deepcopy(after);check.pop('next_definition_only_parameter_availability');assert check==before
for p,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/p)==h
put(R/'next_parameter_availability_verification.json',{'passed':True,'source_sha256':b['source_sha256'],'current_grid_unchanged':True,'all_old_next_state_JSON_fields_unchanged':True,'next_state_before_sha256':oldhash,'next_state_after_sha256':sha(path),'new_strategy_account_or_cashflow_evaluations':0});print(json.dumps({'passed':True,'metadata_only':True,'new_graphs_by_future_batch':[z.get('new_graphs') for z in rows],'first_available_axes':{k:chosen[k] for k in ['BTC_axis','BTC_values','ETH_axis','ETH_values','new_graphs','old_graphs']} if chosen else None,'new_evaluations':0}))
