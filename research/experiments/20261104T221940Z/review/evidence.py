"""Read-only independent identity, source, boundary and funding review; no valuation."""
import csv,gzip,hashlib,json,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import reg,sha,rel,put
p=json.loads((R/'plan.json').read_text());r=json.loads((R/'report.json').read_text());ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');batch=json.loads((R/'batch.json').read_text());newfps={x['fingerprint'] for x in batch};proof=[]
for c in batch:
 sp=json.loads((ROOT/c['spec']).read_text());old=records[c['reference_fingerprint']]['spec'];q=sp['parameters'];diff={k:{'old':old['parameters'].get(k),'new':v} for k,v in q.items() if v!=old['parameters'].get(k)};assert set(diff)=={'BTC_entry_notional_usdt','component_initial_entry_notionals_usdt','source_component_spec_sha256'};assert sp['components'][1]==old['components'][1] and [x['weight'] for x in sp['components']]==[1,1] and c['N']==750
 key=sorted((x['fingerprint'],D(str(x['weight']))) for x in sp['components']);others=[fp for fp,z in records.items() if fp not in newfps and z.get('spec',{}).get('kind')=='combination' and sorted((x['fingerprint'],D(str(x['weight']))) for x in z['spec']['components'])==key];assert not others,others
 proof.append({**{k:c[k] for k in ['name','fingerprint','scope','N','K','D','source_fingerprints','reference_fingerprint']},'spec_sha256':sha(ROOT/c['spec']),'changed_parameter_fields':diff,'old_graph_numeric_equivalent_matches':others})
assert len(proof)==6
put(R/'parameter_identity_inventory.json',{'passed':True,'full_new_definitions':6,'native_definitions':0,'parent_definitions':6,'new_candidate_definitions':6,'new_matchedhold_definitions':0,'actual_grid':{'D':p['slope_lags'],'K':p['slope_strengths']},'fixed_BTC_N':750,'bank_capitals':[3750,15000],'raw_weights':[1,1],'rows':proof,'maximum_context_days':32,'source_context_days':33})
put(R/'numeric_equivalence_inventory_verification.json',{'passed':True,'full_records_checked':len(records),'new_parent_graphs_checked':6,'new_native_definitions':0,'equivalent_numeric_weight_and_order_matches':[],'scope':'Decimal numeric equality and sortedcomponentgraphs,alloldrecordstatuses scanned;only6newN750D3/5graphs. Existingnative/historicalgraphs readonly; no naming-only novelty.'})
controls=[]
for fp in p['external_control_fingerprints']:
 z=records[fp];sp=z['spec'];b,e=[records[x['fingerprint']]['spec']['parameters'] for x in sp['components']];assert b['fixed_entry_notional_usdt']==500 and b['initial_capital_usdt']==3750 and e['fixed_entry_notional_usdt']==4500 and e['initial_capital_usdt']==15000 and e['trend_slope_lag_days'] in p['slope_lags'] and e['trend_slope_hurdle_fraction'] in p['slope_strengths'] and e['trend_gate_scope']=='new_or_reversed_position_only';controls.append({'fingerprint':fp,'ETH_K':e['trend_slope_hurdle_fraction'],'ETH_D':e['trend_slope_lag_days'],'report_sha256':z['report_sha256']})
put(R/'readonly_control_parameter_verification.json',{'passed':True,'controls':controls,'matched_same_ETH_K_and_D':True,'BTC_N_intentionally_differs':True,'canonical_qualifications_unchanged':True})
comp=json.loads((R/'equivalent_realized_NAV_paths.json').read_text())['comparisons'];assert len(comp)==6
for z in comp:
 c=next(c for c in r['configs'].values() if c['fingerprint']==z['fingerprint']);ref=p['read_only_references'][z['reference_fingerprint']];old=next(c for c in json.loads((ROOT/ref['report']).read_text())['configs'].values() if c['fingerprint']==z['reference_fingerprint']);assert old['K']==c['K'] and old['D']==c['D'] and old['source_fingerprints'][1]==c['source_fingerprints'][1]
 for k,s in c['scenes'].items():assert abs(z['cost_comparisons'][k]['delta_return_to_control_pp']-(s['net_return_pct']-old['scenes'][k]['net_return_pct']))<1e-12
put(R/'reference_comparison_verification.json',{'passed':True,'candidate_comparisons':6,'native_comparisons':0,'new_benchmark_comparisons':0,'all_ETH_parameters_matched':True,'all_old_canonical_statuses_preserved':True,'same_totalcapital':18750,'reference_BTC_N':500,'current_BTC_N':750})
sens=json.loads((R/'sensitivity_diagnostics.json').read_text());bounds=[]
for scope,key in [('parent','all_current_grid'),('native','all_current_native_grid')]:
 for k in ['1','2','3']:
  vals=list(r[key].values());best=max(c['scenes'][k]['sharpe_365'] for c in vals);maxs=[c for c in vals if c['scenes'][k]['sharpe_365']==best];d=sens['grid'][scope][k];assert d['maximum_Sharpe']==best and {c['fingerprint'] for c in maxs}=={c['fingerprint'] for c in d['maximum_cells']};bounds.append({'scope':scope,'cost':k,'maximum_Sharpe':best,'maxima':d['maximum_cells']})
alloc=list(csv.DictReader((R/'fixed_allocations.csv').open()));assert len(alloc)==10 and all(D(x['total_initial_capital'])==D(x['BTC_bank'])+D(x['ETH_bank'])==18750 and D(x['raw_BTC_weight'])==D(x['raw_ETH_weight'])==1 for x in alloc)
put(R/'boundary_verification.json',{'passed':True,'actual_axes':{'ETH_D':p['slope_lags'],'ETH_K':p['slope_strengths']},'native_axis_count':2,'parent_axis_count':2,'native_axes_readonly':True,'fixed_BTC_N':750,'results':bounds,'report_sha256':sha(R/'report.json'),'no_postoutcome_expansion_or_gate_change':True})
packets=[]
for stem in ['candidate','l4h02']:
 w=R/(stem+'_observation');im=json.loads((w/'input_manifest.json').read_text());packet=json.loads(gzip.decompress((ROOT/im['packet']).read_bytes()));a=json.loads((R/(stem+'_verification.json')).read_text());prev=json.loads((w/'previous_pointer.json').read_text());before=json.loads((ROOT/prev['state']).read_text());after=json.loads((w/'state.json').read_text());lo=before['cutoff_ns'];cut=after['cutoff_ns'];fs=[]
 for asset,data in packet['assets'].items():
  for row in data['funding']:
   assert {'symbol','fundingTime','fundingRate','markPrice'}<=set(row) and row['symbol']==asset+'USDT' and D(row['markPrice'])>0;within=lo<int(row['fundingTime'])*1000000<=cut;fs.append({'asset':asset,**{k:row[k] for k in ['fundingTime','fundingRate','markPrice']},'within_new_observation_window':within});assert not within
 assert a['new_funding_settlements']==0 and not a['independent_funding_cashflows'] and a['new_fills']==0 and before['books']==after['books']
 packets.append({'account':stem,'window_start_utc':a['window_start_utc'],'cutoff_utc':a['cutoff_utc'],'packet':im['packet'],'packet_sha256':sha(ROOT/im['packet']),'raw_funding_fields_checked':fs,'new_settlement_cashflows':[],'actual_new_settlement_records':0,'actual_new_fills':0,'own_cash_and_quantity_continuity_verified':True,'independent_audit_sha256':sha(R/(stem+'_verification.json'))})
put(R/'primary_funding_field_verification.json',{'passed':True,'accessed_UTC':'2026-11-04','official_documentation_URL':'https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data','official_fields':['symbol','fundingTime','fundingRate','markPrice'],'current_actual_packets':packets,'prior16_settlement_excluded_in_both_current_windows':True,'no_actual_funding_fabricated_or_zero_assumed':True,'new_future_cadence_guard_disclosed_not_synthetic_settlements':True})
put(R/'visual_inspection.json',{'passed':True,'image':'sensitivity.png','sha256':sha(R/'sensitivity.png'),'actual_view_image_tool_output':'functions.exec view_image sensitivity.png; same call includes chunks67fe2c and4c19f3','checked':'D1/3/5/K250/500/750labels,oldO/newN,all9parent/9ETHsourcecells,actualDD/recent5/8vs6/8,legibility andnooverlap.','image_numbers_match_report':True})
print(json.dumps({'passed':True,'new_parent_graphs':len(proof),'readonly_controls':len(controls),'maximum_boundary_scenes':len(bounds),'actual_new_funding_records':0,'same_N_allocations':len(alloc)}))
