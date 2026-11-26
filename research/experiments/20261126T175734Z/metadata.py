"""Refresh the definition-only 3x3 batch already predeclared by the previous round."""
import hashlib,itertools,json,sys
from datetime import datetime,timezone
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;P=ROOT/'research/experiments/20261126T155738Z'
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
prior=rd(P/'next_parameter_availability.json');ref=rd(P/'next_research_state.json')['next_definition_only_parameter_availability'];assert sha(ROOT/ref['path'])==ref['sha256'] and not prior['selection_uses_performance'];preset=prior['first_definition_only_available_batch'];assert preset['BTC_axis']=='return_hurdle' and preset['BTC_values']==[.0275,.03,.0325] and preset['ETH_axis']=='entry_funding_settlement_count' and preset['ETH_values']==[3,4,5]
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
  choices=[z for z in inv['assets'][asset]['rows'] if z['parameters'].get(axis)==value and all(z['parameters'].get(k)==base.get(k) for k in set(z['parameters'])|set(base) if k not in {axis,'persistence','prior_370day_source_fingerprint'})];assert len(choices)==1
  z=choices[0];assert sha(ROOT/z['report'])==z['report_sha256'];out[value]=z['fingerprint']
 return out
axis='return_hurdle';values=[.0275,.03,.0325];ETHaxis='entry_funding_settlement_count';Ks=[3,4,5];BTC=native('BTC',axis,values);ETH=native('ETH',ETHaxis,Ks);rows=[]
for w,k in itertools.product(values,Ks):rows.append({'W':w,'K':k,'BTC':BTC[w],'ETH':ETH[k],'matches':index.get(key([{'fingerprint':BTC[w],'weight':1},{'fingerprint':ETH[k],'weight':1}]),[])})
selected={'axis':axis,'values':values,'BTC':BTC,'ETH':ETH,'BTC_default':.03,'ETH_axis':ETHaxis,'ETH_values':Ks,'new_graphs':sum(not x['matches'] for x in rows),'rows':rows,'representative_preset':{'W':.0275,'K':3},'cross_axis_controls_all_actual':all(x['matches'] for x in rows if x['W']==.03 or x['K']==4),'all_fixed_context_sources_available':True}
out={'recorded_utc':datetime.now(timezone.utc).isoformat(),'prior_predeclared_batch':{'path':str((P/'next_parameter_availability.json').relative_to(ROOT)),'sha256':sha(P/'next_parameter_availability.json')},'full_registry_IDs':len(rs),'complete_canonical_graph_index_built_before_lookup':True,'canonical_component_graph_keys':len(index),'ordered_priorities_before_lookup':[{'BTC_axis':axis,'values':values,'ETH_axis':ETHaxis,'values_ETH':Ks}],'definition_only_attempts':[selected],'selected':selected,'new_financial_or_account_calculations':0,'no_performance_based_selection':True};(R/'joint_parameter_metadata_availability.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');assert selected['new_graphs']==3 and selected['cross_axis_controls_all_actual'];print(json.dumps({'passed':True,'axis':axis,'values':values,'ETH_values':Ks,'new_graphs':selected['new_graphs'],'old_cells':len(rows)-selected['new_graphs'],'representative':selected['representative_preset'],'new_calculations':0}))
