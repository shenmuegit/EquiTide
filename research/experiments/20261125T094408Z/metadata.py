"""Select the first available new grid by definitions only; never inspect performance."""
import itertools,json,hashlib,sys
from decimal import Decimal
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');inv=rd(R/'source_inventory.json')
priorities=[('entry_volatility_window_days',[9,10,11]),('exit_buffer_fraction',[.00375,.005,.00625]),('return_hurdle',[.0275,.03,.0325]),('entry_volatility_ceiling',[.02625,.0275,.02875]),('entry_volatility_ceiling',[.026125,.0275,.028875])]
def key(xs):
 totals={}
 for z in xs:totals[z['fingerprint']]=totals.get(z['fingerprint'],Decimal(0))+Decimal(str(z['weight']))
 return tuple(sorted(totals.items()))
index={}
for fp,z in rs.items():
 sp=z.get('spec',{});p=sp.get('parameters',{})
 if sp.get('kind')=='combination' and p.get('start_utc')=='2025-10-19T00:01:00Z' and p.get('end_utc')=='2026-11-14T00:01:00Z' and (z.get('result_available') or z['status']=='reserved'):index.setdefault(key(sp['components']),[]).append(fp)
def native(asset,axis,values):
 result={};base=inv['assets'][asset]['baseline_parameters']
 for value in values:
  choices=[z for z in inv['assets'][asset]['rows'] if z['parameters'].get(axis)==value and all(z['parameters'].get(k)==base.get(k) for k in set(z['parameters'])|set(base) if k not in {axis,'persistence','prior_370day_source_fingerprint'})]
  if len(choices)!=1:return None
  z=choices[0];assert sha(ROOT/z['report'])==z['report_sha256'];result[value]=z['fingerprint']
 return result
ETH=native('ETH','entry_funding_budget_volatility_window_days',[7,9,12]);assert ETH
attempts=[];selected=None
for axis,values in priorities:
 BTC=native('BTC',axis,values)
 if BTC is None:attempts.append({'axis':axis,'values':values,'all_fixed_context_sources_available':False});continue
 rows=[]
 for w,k in itertools.product(values,[7,9,12]):
  fs=index.get(key([{'fingerprint':BTC[w],'weight':1},{'fingerprint':ETH[k],'weight':1}]),[]);rows.append({'W':w,'K':k,'BTC':BTC[w],'ETH':ETH[k],'matches':fs})
 a={'axis':axis,'values':values,'all_fixed_context_sources_available':True,'new_graphs':sum(not z['matches'] for z in rows),'rows':rows};attempts.append(a)
 a['cross_axis_controls_all_actual']=all(z['matches'] for z in rows if z['W']==inv['assets']['BTC']['baseline_parameters'][axis] or z['K']==9)
 if a['new_graphs'] and a['cross_axis_controls_all_actual']:
  selected={**a,'BTC':BTC,'ETH':ETH,'BTC_default':inv['assets']['BTC']['baseline_parameters'][axis],'ETH_axis':'entry_funding_budget_volatility_window_days','ETH_values':[7,9,12],'representative_preset':{'W':next(z['W'] for z in rows if not z['matches']),'K':next(z['K'] for z in rows if not z['matches'])}};break
assert selected,'No untested graph in the ordered available batches; do not calculate any duplicate.'
out={'recorded_utc':datetime.now(timezone.utc).isoformat(),'full_registry_IDs':len(rs),'complete_canonical_graph_index_built_before_lookup':True,'canonical_component_graph_keys':len(index),'ordered_priorities_before_lookup':priorities,'definition_only_attempts':attempts,'selected':selected,'new_financial_or_account_calculations':0,'no_performance_based_selection':True}
(R/'joint_parameter_metadata_availability.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':True,'axis':selected['axis'],'values':selected['values'],'BTC':selected['BTC'],'new_graphs':selected['new_graphs'],'representative':selected['representative_preset'],'attempts':[{'axis':z['axis'],'available':z['all_fixed_context_sources_available'],'new':z.get('new_graphs')} for z in attempts],'new_calculations':0}))
