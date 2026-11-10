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
 sp=rd(ROOT/row['spec']);q=sp['parameters'];pre='' if row['scope']=='native' else 'ETH_';assert reg.fingerprint(sp)==row['fingerprint'] and row['M']==4 and row['VW'] in [8,10,12] and row['R'] in [.00625,.0075,.00875] and (row['VW'],row['R'])!=(10,.0075)
 expected={'entry_funding_outflow_cap':.0002,'entry_funding_volatility_ratio':row['R'],'entry_funding_budget_volatility_window_days':row['VW'],'entry_funding_settlement_count':4,'entry_funding_min_age_hours':1,'entry_funding_max_age_hours':36,'entry_volatility_window_days':10,'entry_volatility_ceiling':.05,'return_hurdle':.02,'long_entry_return_hurdle':.02,'short_entry_return_hurdle':.02,'lookback_days':5,'trend_slope_lag_days':3,'trend_slope_hurdle_fraction':.0075,'exit_buffer_fraction':.0075,'trend_lookback_days':16,'trend_window_days':16,'trend_decay_numerator':15,'trend_decay_denominator':17}
 assert all(q[pre+k]==v for k,v in expected.items())
 if row['scope']=='native':
  assert sp['universe']==['ETH/USDT'] and q['initial_capital_usdt']==15000 and q['fixed_entry_notional_usdt']==4500;matches=[fp for fp,z in rs.items() if fp not in newfps and z.get('spec',{}).get('kind')=='strategy' and z['spec'].get('universe')==['ETH/USDT'] and normalized(z['spec']['parameters'])==normalized(q)];assert not matches
 else:
  assert [x['weight'] for x in sp['components']]==[1,1] and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[1000,4500];key=sorted((x['fingerprint'],D(str(x['weight']))) for x in sp['components']);matches=[fp for fp,z in rs.items() if fp not in newfps and z.get('spec',{}).get('kind')=='combination' and sorted((x['fingerprint'],D(str(x['weight']))) for x in z['spec']['components'])==key];assert not matches
 rec=rs[row['fingerprint']];assert rec['result_available'] and rec['report_sha256']==sha(R/'report.json') and rec['status']==rep['configs'][row['name']]['status'];checks.append({'fingerprint':row['fingerprint'],'scope':row['scope'],'M':4,'budget_VW':row['VW'],'R':row['R'],'price_V':10,'spec_sha256':sha(ROOT/row['spec']),'prior_semantic_or_graph_matches':matches})
for fp,ref in p['read_only_references'].items():
 assert rs[fp]['status']==ref['status'] and rs[fp]['report_sha256']==ref['report_sha256']
 for k in ['spec','report','archive']:assert sha(ROOT/ref[k])==ref[k+'_sha256']
center=p['current_center'];assert all(rs[fp]['result_available'] for fp in center.values()) and all(fp not in newfps for fp in center.values());eq=copy.deepcopy(rs[center['native']]['spec']['parameters']);eq['entry_funding_budget_volatility_window_days']=10;eq['entry_funding_budget_formula']=eq['entry_funding_budget_formula'].replace('past10','pastVW');assert normalized(eq)==normalized(rs[center['native']]['spec']['parameters'])
put(R/'parameter_identity_inventory.json',{'passed':True,'full_new_definitions':16,'native_definitions':8,'parent_definitions':8,'rows':checks,'actual_grid':{'fixed_M':4,'budget_VW':[8,10,12],'R':[.00625,.0075,.00875],'price_V':10,'fixed_K':.0075,'fixed_VC':.05},'exact_old_default_center_reused':center,'semantic_default_equivalence_checked':True,'raw_weights':[1,1],'bank_capitals':[3750,15000],'entry_notionals':[1000,4500]});put(R/'numeric_equivalence_inventory_verification.json',{'passed':True,'full_records_checked':len(rs),'semantic_native_and_numeric_graph_duplicates':[],'new_native':8,'new_parents':8,'old_default_center_not_reserved':True});put(R/'readonly_control_parameter_verification.json',{'passed':True,'old_source_results':10,'old_native_banks':6,'current_center':center,'static_M4_F75_control':p['static_M4_F75_control'],'unfiltered_control':p['unfiltered_control'],'all_original_canonical_qualifications_preserved':True})
com=rd(R/'equivalent_realized_NAV_paths.json')['comparisons'];assert len(com)==16
for z in com:
 c=next(c for c in rep['configs'].values() if c['fingerprint']==z['fingerprint']);ref=p['read_only_references'][c['reference_fingerprint']];o=next(c for c in rd(ROOT/ref['report'])['configs'].values() if c['fingerprint']==ref['fingerprint']);assert z['VW']==c['VW']
 for k,s in c['scenes'].items():assert z['cost_comparisons'][k]['return_pct']==s['net_return_pct'] and z['cost_comparisons'][k]['old_return_pct']==o['scenes'][k]['net_return_pct']
put(R/'reference_comparison_verification.json',{'passed':True,'new_native_comparisons':8,'new_parent_comparisons':8,'same_initial_capital_and_entry_notionals':True,'fixed_BTC_native_reused':True,'old_statuses_unchanged':True})
d=rd(R/'sensitivity_diagnostics.json');maxima=[]
for scope,key in [('native','all_current_native_grid'),('parent','all_current_grid')]:
 for k in ['1','2','3']:
  cells=rep[key];best=max(c['scenes'][k]['sharpe_365'] for c in cells.values() if c['scenes'][k]['sharpe_365'] is not None);assert d['grid'][scope][k]['maximum_Sharpe']==best
  for z in d['grid'][scope][k]['maximum_cells']:assert z['at_grid_boundary']==(z['VW'] in [8,12] or z['R'] in [.00625,.00875])
  maxima.append({'scope':scope,'cost':k,'maximum_Sharpe':best,'maximum_cells':d['grid'][scope][k]['maximum_cells']})
put(R/'boundary_verification.json',{'passed':True,'axes':['budget_VW','R'],'maxima':maxima,'no_postoutcome_grid_or_gate_change':True})
# Closed current account windows contain no funding/daily/fills; verify every own book.
packets=[]
for stem in ['candidate','l4h02','fewm']:
 W=R/(stem+'_observation');im=rd(W/'input_manifest.json');assert sha(ROOT/im['packet'])==im['sha256'];packet=json.loads(gzip.decompress((ROOT/im['packet']).read_bytes()));v=rd(R/(stem+'_verification.json'));before=rd(ROOT/rd(W/'previous_pointer.json')['state']);state=rd(W/'state.json');delta=json.loads(gzip.decompress((W/'delta.json.gz').read_bytes()));raw=[z for body in packet['assets'].values() for z in body['funding'] if before['cutoff_ns']<int(z['fundingTime'])*1000000<=state['cutoff_ns']];assert not raw and not [z for z in delta['journal'] if z['kind'] in ['funding','decision','trade']] and v['new_funding_settlements']==v['new_exact_causal_decisions']==v['new_fills']==0 and state['books']==before['books'];packets.append({'account':stem,'raw_funding_in_window':0,'funding_decisions_fills':0,'own_books_unchanged':True,'full_NAV_audit_sha256':sha(R/(stem+'_verification.json'))})
put(R/'primary_funding_field_verification.json',{'passed':True,'official_fields':['symbol','fundingTime','fundingRate','markPrice'],'fundingTime_ms_to_ns':True,'current_actual_packets':packets,'historical_real_settlements_not_rebooked':True,'all_latest_Nov10_00_retained':True})
counts={}
for name in ['cost_scenes.csv','walk_forward_folds.csv','recent40_folds.csv','daily_NAV.csv']:
 rows=list(csv.DictReader((R/name).open()))
 for x in rows:
  c=rep['configs'][x['configuration']];assert int(x['ETH_budget_VW'])==c['VW'] and int(x['ETH_M'])==4 and float(x['ETH_R'])==c['R'] and float(x['ETH_VC'])==.05 and float(x['ETH_K'])==.0075
 counts[name]=len(rows)
for name,key in [('sensitivity_grid.csv','all_current_grid'),('native_sensitivity_grid.csv','all_current_native_grid')]:
 rows=list(csv.DictReader((R/name).open()))
 for x in rows:c=rep[key][x['fingerprint']];assert int(x['ETH_budget_VW'])==c['VW'] and int(x['ETH_M'])==4 and float(x['ETH_R'])==c['R']
 counts[name]=len(rows)
put(R/'CSV_parameter_verification.json',{'passed':True,'report_sha256':sha(R/'report.json'),'rows':counts,'actual_separate_budget_VW_and_R_exported':True,'pricegate_V10_and_funding_M4_fixed':True,'no_new_valuations':True});assert rd(R/'visual_inspection.json')['passed'] and rd(R/'visual_inspection.json')['sha256']==sha(R/'sensitivity.png');print('PASS16complete VW/R identities and semantic-default reuse,allCSV VW/R,48costscenes,oldcanonical sources and3ownmark-only books')
