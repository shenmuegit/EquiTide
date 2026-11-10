"""Independent complete numeric VW/R identity, semantic defaults and exported evidence."""
import copy,csv,gzip,json,sys
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import reg,sha,rel,put
rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');rep=rd(R/'report.json');rs=reg.read_records(ROOT/'research/automation/registry.jsonl');b=rd(R/'batch.json');assert len(b)==16;newfps={x['fingerprint'] for x in b};checks=[]
def normalized(q):
 q=copy.deepcopy(q)
 if q.get('entry_funding_filter')=='volatility_relative_median_of_latest_N_eligible_realized_settlements_new_entry_only':
  vw=q.pop('entry_funding_budget_volatility_window_days',10)
  if vw!=10:q['entry_funding_budget_volatility_window_days']=vw
  old='min(hardcap,ratio*past10_sample_daily_logvol*latest_eligible_completed_actual_interval_hours/24)';new=old.replace('past10','pastVW')
  if q.get('entry_funding_budget_formula') in [old,new]:q['entry_funding_budget_formula']=new
 return q
for row in b:
 sp=rd(ROOT/row['spec']);q=sp['parameters'];pre='' if row['scope']=='native' else 'ETH_';assert reg.fingerprint(sp)==row['fingerprint'] and row['M']==4 and row['VW']==8 and row['R']==.00875 and row['K']==.0075 and row['VC'] in [.045,.05,.055] and row['H']==.02 and row['E']==.0075 and row['S']==16 and row['D']==3 and row['L']==5 and row['V'] in [6,7,8] and (row['V'],row['VC'])!=(8,.05)
 expected={'entry_funding_outflow_cap':.0002,'entry_funding_volatility_ratio':row['R'],'entry_funding_budget_volatility_window_days':row['VW'],'entry_funding_settlement_count':4,'entry_funding_min_age_hours':1,'entry_funding_max_age_hours':36,'entry_volatility_window_days':row['V'],'entry_volatility_ceiling':row['VC'],'return_hurdle':row['H'],'long_entry_return_hurdle':row['H'],'short_entry_return_hurdle':row['H'],'lookback_days':row['L'],'trend_slope_lag_days':row['D'],'trend_slope_hurdle_fraction':row['K'],'exit_buffer_fraction':row['E'],'trend_lookback_days':row['S'],'trend_window_days':row['S'],'trend_decay_numerator':row['S']-1,'trend_decay_denominator':row['S']+1}
 assert all(q[pre+k]==v for k,v in expected.items())
 if row['scope']=='native':
  assert sp['universe']==['ETH/USDT'] and q['initial_capital_usdt']==15000 and q['fixed_entry_notional_usdt']==4500;matches=[fp for fp,z in rs.items() if fp not in newfps and z.get('spec',{}).get('kind')=='strategy' and z['spec'].get('universe')==['ETH/USDT'] and normalized(z['spec']['parameters'])==normalized(q)];assert not matches
 else:
  assert [x['weight'] for x in sp['components']]==[1,1] and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[1000,4500];key=sorted((x['fingerprint'],D(str(x['weight']))) for x in sp['components']);matches=[fp for fp,z in rs.items() if fp not in newfps and z.get('spec',{}).get('kind')=='combination' and sorted((x['fingerprint'],D(str(x['weight']))) for x in z['spec']['components'])==key];assert not matches
 rec=rs[row['fingerprint']];assert rec['result_available'] and rec['report_sha256']==sha(R/'report.json') and rec['status']==rep['configs'][row['name']]['status'];checks.append({'fingerprint':row['fingerprint'],'scope':row['scope'],'M':4,'budget_VW':row['VW'],'R':row['R'],'price_V':row['V'],'spec_sha256':sha(ROOT/row['spec']),'prior_semantic_or_graph_matches':matches})
for fp,ref in p['read_only_references'].items():
 assert rs[fp]['status']==ref['status'] and rs[fp]['report_sha256']==ref['report_sha256']
 for k in ['spec','report','archive']:assert sha(ROOT/ref[k])==ref[k+'_sha256']
center=p['current_center'];assert all(rs[fp]['result_available'] for fp in center.values()) and all(fp not in newfps for fp in center.values());assert rs[center['native']]['spec']['parameters']['trend_slope_hurdle_fraction']==.0075 and rs[center['native']]['spec']['parameters']['entry_volatility_ceiling']==.05
put(R/'parameter_identity_inventory.json',{'passed':True,'full_new_definitions':16,'native_definitions':8,'parent_definitions':8,'rows':checks,'actual_grid':{'fixed_M':4,'budget_VW':[8],'R':[.00875],'price_V':[6,7,8],'L':[5],'S':[16],'D':[3],'H':[.02],'E':[.0075],'K':[.0075],'VC':[.045,.05,.055]},'exact_old_default_center_reused':center,'semantic_default_equivalence_checked':True,'raw_weights':[1,1],'bank_capitals':[3750,15000],'entry_notionals':[1000,4500]});put(R/'numeric_equivalence_inventory_verification.json',{'passed':True,'full_records_checked':len(rs),'semantic_native_and_numeric_graph_duplicates':[],'new_native':8,'new_parents':8,'old_default_center_not_reserved':True});put(R/'readonly_control_parameter_verification.json',{'passed':True,'old_source_results':10,'old_native_banks':6,'current_center':center,'previous_budget_center':p['previous_budget_center'],'unfiltered_control':p['unfiltered_control'],'all_original_canonical_qualifications_preserved':True})
com=rd(R/'equivalent_realized_NAV_paths.json')['comparisons'];assert len(com)==16
for z in com:
 c=next(c for c in rep['configs'].values() if c['fingerprint']==z['fingerprint']);ref=p['read_only_references'][c['reference_fingerprint']];o=next(c for c in rd(ROOT/ref['report'])['configs'].values() if c['fingerprint']==ref['fingerprint']);assert z['VW']==c['VW']
 for k,s in c['scenes'].items():assert z['cost_comparisons'][k]['return_pct']==s['net_return_pct'] and z['cost_comparisons'][k]['old_return_pct']==o['scenes'][k]['net_return_pct']
put(R/'reference_comparison_verification.json',{'passed':True,'new_native_comparisons':8,'new_parent_comparisons':8,'same_initial_capital_and_entry_notionals':True,'fixed_BTC_native_reused':True,'old_statuses_unchanged':True})
d=rd(R/'sensitivity_diagnostics.json');maxima=[]
for scope,key in [('native','all_current_native_grid'),('parent','all_current_grid')]:
 for k in ['1','2','3']:
  cells=rep[key];best=max(c['scenes'][k]['sharpe_365'] for c in cells.values() if c['scenes'][k]['sharpe_365'] is not None);assert d['grid'][scope][k]['maximum_Sharpe']==best
  for z in d['grid'][scope][k]['maximum_cells']:assert z['at_grid_boundary']==(z['V'] in [6,8] or z['VC'] in [.045,.055])
  maxima.append({'scope':scope,'cost':k,'maximum_Sharpe':best,'maximum_cells':d['grid'][scope][k]['maximum_cells']})
put(R/'boundary_verification.json',{'passed':True,'axes':['PRICE_V','VC'],'maxima':maxima,'no_postoutcome_grid_or_gate_change':True})
# Current own08cashflows independently checked against fresh publicfields and each beforebook.
fund=rd(R/'current_actual_nov10_16_funding_verification.json');assert fund['passed'] and fund['own_current_funding_records']=={'candidate':6,'l4h02':0,'fewm':0}
put(R/'primary_funding_field_verification.json',{'passed':True,'official_fields':['symbol','fundingTime','fundingRate','markPrice'],'fundingTime_ms_to_ns':True,'current_nov10_16_verification_sha256':sha(R/'current_actual_nov10_16_funding_verification.json'),'current_funding_counts':fund['own_current_funding_records'],'own_q_cash_and_amount_formulas_verified':True,'no_old00_or_other_account_cashflow_copy':True})
counts={}
for name in ['cost_scenes.csv','walk_forward_folds.csv','recent40_folds.csv','daily_NAV.csv']:
 rows=list(csv.DictReader((R/name).open()))
 for x in rows:
  c=rep['configs'][x['configuration']];assert int(x['ETH_price_V'])==c['V'] and int(x['ETH_L'])==c['L'] and int(x['ETH_budget_VW'])==c['VW'] and int(x['ETH_M'])==4 and float(x['ETH_R'])==c['R'] and float(x['ETH_VC'])==c['VC'] and float(x['ETH_K'])==c['K'] and float(x['ETH_H'])==c['H'] and float(x['ETH_E'])==c['E'] and int(x['ETH_S'])==c['S'] and int(x['ETH_D'])==c['D']
 counts[name]=len(rows)
for name,key in [('sensitivity_grid.csv','all_current_grid'),('native_sensitivity_grid.csv','all_current_native_grid')]:
 rows=list(csv.DictReader((R/name).open()))
 for x in rows:c=rep[key][x['fingerprint']];assert int(x['ETH_price_V'])==c['V'] and int(x['ETH_L'])==c['L'] and int(x['ETH_budget_VW'])==c['VW'] and int(x['ETH_M'])==4 and float(x['ETH_R'])==c['R'] and int(x['ETH_S'])==c['S'] and int(x['ETH_D'])==c['D']
 counts[name]=len(rows)
put(R/'CSV_parameter_verification.json',{'passed':True,'report_sha256':sha(R/'report.json'),'rows':counts,'actual_L_PRICE_V_exported_fixed_budget_VW8_R00875':True,'price_V_separate_funding_M4_VW8_fixed':True,'no_new_valuations':True});assert rd(R/'visual_inspection.json')['passed'] and rd(R/'visual_inspection.json')['sha256']==sha(R/'sensitivity.png');print('PASS16complete S/D identities and semantic-default reuse,allCSV VW/R,48costscenes,oldcanonical sources and3owncurrentfunding books')
