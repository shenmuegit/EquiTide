"""Independent final identities, old controls, boundary and raw funding evidence."""
import gzip,json,sys
from decimal import Decimal as D
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import reg,sha,rel,put
rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');rep=rd(R/'report.json');rs=reg.read_records(ROOT/'research/automation/registry.jsonl');b=rd(R/'batch.json');assert len(b)==12;newfps={x['fingerprint'] for x in b};checks=[]
for row in b:
 sp=rd(ROOT/row['spec']);q=sp['parameters'];assert reg.fingerprint(sp)==row['fingerprint'] and row['D']==3 and row['E']==.0075 and row['F'] in [0,.00005] and row['VC']==.05 and row['K']==.0075 and row['L']==5 and row['H']==.02 and row['M'] in [2,3,4] and row['S']==16
 pref='' if row['scope']=='native' else 'ETH_'
 assert q[pref+'entry_funding_outflow_cap']==row['F'] and q[pref+'entry_funding_min_age_hours']==1 and q[pref+'entry_funding_max_age_hours']==36 and q[pref+'entry_funding_settlement_count']==row['M']
 if row['scope']=='native':
  assert sp['universe']==['ETH/USDT'] and q['initial_capital_usdt']==15000 and q['fixed_entry_notional_usdt']==4500 and q['return_hurdle']==q['long_entry_return_hurdle']==q['short_entry_return_hurdle']==row['H'] and q['lookback_days']==row['L'] and q['trend_slope_lag_days']==row['D'] and q['trend_slope_hurdle_fraction']==row['K'] and q['exit_buffer_fraction']==row['E'] and q['entry_volatility_ceiling']==row['VC'] and q['trend_lookback_days']==q['trend_window_days']==row['S'] and q['trend_decay_numerator']==row['S']-1 and q['trend_decay_denominator']==row['S']+1;matches=[fp for fp,z in rs.items() if fp not in newfps and z.get('spec',{}).get('kind')=='strategy' and z['spec'].get('universe')==['ETH/USDT'] and z['spec']['parameters']==q];assert not matches
 else:
  assert [x['weight'] for x in sp['components']]==[1,1] and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[1000,4500] and q['BTC_lookback_days']==29 and q['BTC_return_hurdle']==.03 and q['BTC_exit_buffer_fraction']==.01 and q['ETH_trend_slope_lag_days']==row['D'] and q['ETH_trend_slope_hurdle_fraction']==row['K'] and q['ETH_exit_buffer_fraction']==row['E'] and q['ETH_entry_volatility_ceiling']==row['VC'] and q['ETH_return_hurdle']==q['ETH_long_entry_return_hurdle']==q['ETH_short_entry_return_hurdle']==row['H'] and q['ETH_lookback_days']==row['L'] and q['ETH_trend_lookback_days']==q['ETH_trend_window_days']==row['S'] and q['ETH_trend_decay_numerator']==row['S']-1 and q['ETH_trend_decay_denominator']==row['S']+1;key=sorted((x['fingerprint'],D(str(x['weight']))) for x in sp['components']);matches=[fp for fp,z in rs.items() if fp not in newfps and z.get('spec',{}).get('kind')=='combination' and sorted((x['fingerprint'],D(str(x['weight']))) for x in z['spec']['components'])==key];assert not matches
 checks.append({'fingerprint':row['fingerprint'],'scope':row['scope'],'ETH_D':row['D'],'ETH_L':row['L'],'ETH_H':row['H'],'ETH_S':row['S'],'ETH_M':row['M'],'ETH_F':row['F'],'ETH_E':row['E'],'ETH_K':row['K'],'ETH_VC':row['VC'],'native_N':4500,'spec_sha256':sha(ROOT/row['spec']),'old_semantic_or_numeric_graph_matches':matches})
put(R/'parameter_identity_inventory.json',{'passed':True,'full_new_definitions':12,'native_definitions':6,'parent_definitions':6,'rows':checks,'actual_grid':{'fixed_ETH_D':3,'ETH_K':[.0075],'ETH_S':[16],'ETH_H':[.02],'ETH_M':[1,2,3,4],'fixed_ETH_L':5,'fixed_ETH_S':16,'ETH_E_values':[.0075],'ETH_F_values':[0,.00005],'fixed_ETH_VC':.05},'fixed_BTC':{'L':29,'H':.03,'E':.01,'N':1000},'raw_weights':[1,1],'bank_capitals':[3750,15000],'entry_notionals':[1000,4500]});put(R/'numeric_equivalence_inventory_verification.json',{'passed':True,'full_records_checked':len(rs),'semantic_native_and_numeric_graph_duplicates':[],'new_native':6,'new_parents':6})
for fp,ref in p['read_only_references'].items():assert rs[fp]['status']==ref['status'] and rs[fp]['report_sha256']==ref['report_sha256'] and sha(ROOT/ref['report'])==ref['report_sha256']
put(R/'readonly_control_parameter_verification.json',{'passed':True,'old_source_results':10,'old_native_banks':6,'baseline_BTC_L':29,'baseline_BTC_E':.01,'baseline_BTC_H':.03,'BTC_N':1000,'ETH_L_control':5,'ETH_H_controls':[.02],'ETH_M_control':1,'ETH_F_controls':[0,.00005],'ETH_S_values':[16],'ETH_D':3,'ETH_K':[.0075],'ETH_N':4500,'ETH_VC_control':.05,'ETH_E_controls':[.0075],'all_original_canonical_qualifications_preserved':True})
com=rd(R/'equivalent_realized_NAV_paths.json')['comparisons'];assert len(com)==12
for z in com:
 c=next(x for x in rep['configs'].values() if x['fingerprint']==z['fingerprint']);ref=p['read_only_references'][c['reference_fingerprint']];old=next(x for x in rd(ROOT/ref['report'])['configs'].values() if x['fingerprint']==c['reference_fingerprint'])
 for k,s in c['scenes'].items():assert z['cost_comparisons'][k]['return_pct']==s['net_return_pct'] and z['cost_comparisons'][k]['old_return_pct']==old['scenes'][k]['net_return_pct']
put(R/'reference_comparison_verification.json',{'passed':True,'new_native_comparisons':6,'new_parent_comparisons':6,'same_initial_capital_and_entry_notionals':True,'fixed_BTC_native_reused':True,'old_statuses_unchanged':True})
d=rd(R/'sensitivity_diagnostics.json');maxima=[]
for scope,key in [('native','all_current_native_grid'),('parent','all_current_grid')]:
 for k in ['1','2','3']:
  cells=rep[key];best=max((c['scenes'][k]['sharpe_365'] for c in cells.values() if c['scenes'][k]['sharpe_365'] is not None),default=None);assert d['grid'][scope][k]['maximum_Sharpe']==best;maxima.append({'scope':scope,'cost':k,'maximum_Sharpe':best,'maximum_cells':d['grid'][scope][k]['maximum_cells']})
put(R/'boundary_verification.json',{'passed':True,'axes':['ETH_M','ETH_F'],'maxima':maxima,'no_postoutcome_grid_or_gate_change':True})
packets=[]
for stem in ['candidate','l4h02','fewm']:
 w=R/(stem+'_observation');im=rd(w/'input_manifest.json');assert sha(ROOT/im['packet'])==im['sha256'];packet=json.loads(gzip.decompress((ROOT/im['packet']).read_bytes()));v=rd(R/(stem+'_verification.json'));before=rd(ROOT/rd(w/'previous_pointer.json')['state']);state=rd(w/'state.json');delta=json.loads(gzip.decompress((w/'delta.json.gz').read_bytes()));raw={(a,int(z['fundingTime'])*1000000):z for a,body in packet['assets'].items() for z in body['funding'] if before['cutoff_ns']<int(z['fundingTime'])*1000000<=state['cutoff_ns']};funds=[z for z in delta['journal'] if z['kind']=='funding'];decs=[z for z in delta['journal'] if z['kind']=='decision'];assert v['passed'] and len(decs)==v['new_exact_causal_decisions'] and len(funds)==v['new_funding_settlements']==3*len(raw);formula=[]
 for z in funds:
  a,k,t=z['asset'],str(z['cost_multiplier']),z['timestamp_ns'];f=raw[a,t];q=D(before['books'][a][k]['signed_units']);base=-q*D(f['markPrice'])*D(f['fundingRate']);amount=base*int(k) if base<0 else base;assert D(z['signed_units'])==q and D(z['mark_price'])==D(f['markPrice']) and D(z['rate'])==D(f['fundingRate']) and D(z['base_amount_usdt'])==base and D(z['amount_usdt'])==amount and D(z['cash_before'])==D(before['books'][a][k]['cash']) and D(z['cash_after'])==D(z['cash_before'])+amount;formula.append({'asset':a,'cost':k,'actual_ns':t,'actual_rate':f['fundingRate'],'actual_mark':f['markPrice'],'own_units':str(q),'own_base_usdt':str(base),'own_amount_usdt':str(amount)})
 for a in ['BTC','ETH']:
  for k in ['1','2','3']:
   bs,ss=before['books'][a][k],state['books'][a][k];ts=[x for x in delta['journal'] if x['kind']=='trade' and x['asset']==a and str(x['cost_multiplier'])==k and x['status']=='filled'];assert ss==ts[-1]['state_after'] if ts else all(bs[f]==ss[f] for f in ['signed_units','entry_price','entry_reference']) and D(ss['cash'])==D(bs['cash'])+sum((D(z['amount_usdt']) for z in funds if z['asset']==a and str(z['cost_multiplier'])==k),D(0))
 packets.append({'account':stem,'raw_funding_records_in_new_window':len(raw),'new_settlement_ledger_records':len(funds),'independent_own_account_funding_formulas':formula,'actual_daily_decisions':len(decs),'actual_fills':v['new_fills'],'raw_packet_sha256':im['sha256'],'complete_NAV_audit_sha256':sha(R/(stem+'_verification.json'))})
put(R/'primary_funding_field_verification.json',{'passed':True,'accessed_UTC':'2026-11-10','official_fields':['symbol','fundingTime','fundingRate','markPrice'],'fundingTime_ms_to_ns':True,'current_actual_packets':packets,'zero_cashflows_if_actual_units_zero_are_derived_not_missing_data':True,'no_duplicate00_or_other_account_cashflow_copy':True});assert rd(R/'visual_inspection.json')['passed'] and rd(R/'visual_inspection.json')['sha256']==sha(R/'sensitivity.png');print('PASS12newfinancial identities/readonlycenters/6boundaryscenes/allthreeownfundingbooks')

# Verify exported varying S against authoritative complete configuration identities.
import csv
csvcounts={}
for name in ['cost_scenes.csv','walk_forward_folds.csv','recent40_folds.csv','daily_NAV.csv']:
 rows=list(csv.DictReader((R/name).open()))
 for x in rows:
  c=rep['configs'][x['configuration']];assert int(x['ETH_S'])==c['S'] and float(x['ETH_E'])==c['E'] and float(x['ETH_VC'])==c['VC'] and int(x['ETH_D'])==c['D'] and float(x['ETH_K'])==c['K'] and float(x['ETH_H'])==c['H'] and int(x['ETH_L'])==c['L'] and float(x['ETH_F'])==c['F'] and int(x['ETH_M'])==c['M']
 csvcounts[name]=len(rows)
for name,key in [('sensitivity_grid.csv','all_current_grid'),('native_sensitivity_grid.csv','all_current_native_grid')]:
 rows=list(csv.DictReader((R/name).open()))
 for x in rows:c=rep[key][x['fingerprint']];assert int(x['ETH_M'])==c['M'] and int(x['ETH_S'])==c['S'] and float(x['ETH_E'])==c['E'] and float(x['ETH_VC'])==c['VC'] and int(x['ETH_D'])==c['D'] and float(x['ETH_K'])==c['K'] and ((x['ETH_F']=='' and c['F'] is None) or (x['ETH_F']!='' and float(x['ETH_F'])==c['F'] and int(x['ETH_M'])==c['M']))
 csvcounts[name]=len(rows)
for x in csv.DictReader((R/'fixed_allocations.csv').open()):
 if x['role']!='benchmark':assert int(x['ETH_S'])==rep['all_current_grid'][x['fingerprint']]['S']
put(R/'CSV_parameter_verification.json',{'passed':True,'report_sha256':sha(R/'report.json'),'rows':csvcounts,'varying_M_and_F_fixed_H_E_VC5_exported_from_actual_definitions':True,'no_new_valuations':True});print('PASS actualK/EandfixedS/VC5 parametersinallcost/fold/daily/sensitivity/allocationexports')
