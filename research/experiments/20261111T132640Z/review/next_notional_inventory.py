"""Proposal-only full parameter/graph inventory; no reservations or policy/NAV calculation."""
import copy,json,sys
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import reg,sha,put,rel,now
p=json.loads((R/'plan.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');base={'BTC':p['fixed_BTC_fingerprint'],'ETH':p['current_center']['native']};out={}
for a,values in [('BTC',[750,1000,1250]),('ETH',[4000,4500,5000])]:
 src=rs[base[a]];q=src['spec']['parameters'];rows=[]
 for N in values:
  target={**q,'fixed_entry_notional_usdt':N};matches=[{'fingerprint':fp,'status':z['status'],'result_available':z['result_available'],'report':z.get('report'),'report_sha256':z.get('report_sha256')} for fp,z in rs.items() if z.get('spec',{}).get('kind')=='strategy' and z['spec'].get('universe')==[a+'/USDT'] and z['spec']['parameters']==target]
  rows.append({'N':N,'complete_parameter_matches':matches})
 out[a]={'source_fingerprint':base[a],'source_report':src['report'],'source_report_sha256':src['report_sha256'],'source_parameters':q,'proposed_values':rows}
put(R/'next_notional_inventory.json',{'passed':True,'recorded_utc':now(),'proposal_only':True,'full_registry_records_read':len(rs),'assets':out,'parent_grid':{'BTC_N':[750,1000,1250],'ETH_N':[4000,4500,5000],'bank_capitals_usdt':[3750,15000],'raw_bank_weights':[1,1],'predeclared_representative':{'BTC_N':1000,'ETH_N':4000},'capital_and_exposure_meaning':'FullbanksC3750/15000,total18750,20/80capital;N values are actual execution notional/exposure,not portfolio weights.Normalization0. ChangedNmustsimulateactualLOTq/fee/impact/funding/margin;noscaledoldNAV.','existing_source_reuse':'ExactalreadyactualNcomponentreadonly;changedNnewreservebeforenativesimulate;numericparentgraphduplicatecheckbeforeanycompute.'},'parent_maximum_grid_cells':9,'financial_reservations_or_evaluations':0,'scope':'Full equality preliminary inventory is not final semantic/default or numeric graph clearance;next round must reread complete registry and normalize defaults/parent graph before freeze/reserve.'})
print(json.dumps({'proposal_only':True,'exact_component_counts':{a:[{'N':x['N'],'matches':len(x['complete_parameter_matches'])} for x in out[a]['proposed_values']] for a in out},'financial_calculations':0}),flush=True)
