from pathlib import Path
R=Path('research/experiments/20261111T192849Z');S=Path('research/experiments/20261111T152711Z');P=Path('research/experiments/20261111T172818Z')
s=(S/'run.py').read_text();a=s.index('def neighbors(');b=s.index('\ndef criteria',a)
s=s[:a]+'''def neighbors(c,p,full):
 if c['scope']=='parent':rows=[g for g in p['grid'] if abs(p['axes']['BTC_H'].index(g['H'])-p['axes']['BTC_H'].index(c['H']))<=1 and abs(p['axes']['ETH_R'].index(g['R'])-p['axes']['ETH_R'].index(c['R']))<=1]
 else:
  values=p['axes']['BTC_H' if c['asset']=='BTC' else 'ETH_R'];rows=[g for g in p['native_grid'] if g['asset']==c['asset'] and abs(values.index(g['value'])-values.index(c['value']))<=1]
 return [full[g['fingerprint']] for g in rows]
'''+s[b:]
s=s.replace('assert len(batch)==12',"assert len(batch)==p['expected_counts']['new_configs']")
s=s.replace("{'fingerprint':fp,'NB':c['NB'],'NE':c['NE']", "{'fingerprint':fp,'H':c['H'],'R':c['R'],'NB':c['NB'],'NE':c['NE']").replace('excess_to_fixed_exposure_hold_pp','excess_to_matched_hold_pp').replace("'matched_notional':(c['NB'],c['NE'])==(1000,4500)","'matched_notional':True")
s=s.replace("'new_native_models':4,'new_parent_models':8", "'new_native_models':2,'new_parent_models':8").replace("'varied_axes':['BTC_actual_entry_N','ETH_actual_entry_N']","'varied_axes':['BTC_entry_return_hurdle','ETH_funding_budget_ratio']").replace("'old_unique_results_readonly':10","'old_unique_results_readonly':8").replace("'native_sizing_sensitivity_own_N_only':True,'fixed_exposure_hold_not_a_matched_notional_control_for_other_cells':True","'native_component_own_controlled_rule_axis_only':True,'same_actual_N_matched_hold_for_all_cells':True")
(R/'run.py').write_text(s)
s=(S/'audit.py').read_text();a=s.index(" if c['scope']=='parent':ng=");b=s.index(" ns=[full",a)
s=s[:a]+''' if c['scope']=='parent':ng=[g for g in plan['grid'] if abs(plan['axes']['BTC_H'].index(g['H'])-plan['axes']['BTC_H'].index(c['H']))<=1 and abs(plan['axes']['ETH_R'].index(g['R'])-plan['axes']['ETH_R'].index(c['R']))<=1];dimensions=2
 else:
  ns=plan['axes']['BTC_H' if c['asset']=='BTC' else 'ETH_R'];ng=[g for g in plan['native_grid'] if g['asset']==c['asset'] and abs(ns.index(g['value'])-ns.index(c['value']))<=1];dimensions=1
'''+s[b:]
s=s.replace("assert (newnative,oldnative,parents,decisions)==(12,18,24,4440)", "assert (newnative,oldnative,parents,decisions)==(6,18,24,2220)")
s=s.replace("'native_BTC_N_values':[750,1250],'native_ETH_N_values':[4000,5000]", "'native_BTC_N_values':[],'native_ETH_N_values':[4000],'ETH_new_budget_ratios':[.00875,.01125],'new_BTC_policies':0,'all3_BTC_H_policies_readonly':True").replace("'parent_two_sizing_axes':True,'native_component_own_N_axis_only':True", "'parent_two_rule_axes':True,'native_component_own_controlled_rule_axis_only':True")
# Verify source rule parameters for every new parent, beyond bank amounts.
s=s.replace("assert c['scenes'][k]==z['summary']", "assert c['scenes'][k]==z['summary']\n if c['scope']=='parent':\n  source_specs=[json.loads((ROOT/(plan['read_only_references'][f]['spec'] if f in plan['read_only_references'] else next(x['spec'] for x in report['configs'].values() if x['fingerprint']==f))).read_text()) for f in c['source_fingerprints']];assert source_specs[0]['parameters']['return_hurdle']==c['H'] and source_specs[1]['parameters']['entry_funding_volatility_ratio']==c['R']")
s=s.replace("for fp,ref in plan['read_only_references'].items():\n z=reg", "for x in report['matched_hold_comparisons']:\n c=report['all_current_grid'][x['fingerprint']];h=old[plan['benchmark_parent_fingerprint']];k=str(x['cost_multiplier']);near(x['excess_to_matched_hold_pp'],c['scenes'][k]['net_return_pct']-h['scenes'][k]['net_return_pct']);assert x['matched_notional'] and x['H']==c['H'] and x['R']==c['R'] and [c['NB'],c['NE']]==[1000,4000]\nfor fp,ref in plan['read_only_references'].items():\n z=reg")
(R/'audit.py').write_text(s)
s=(S/'exports.py').read_text();s=s.replace("c.get('NE')]", "c.get('NE'),c.get('H'),c.get('R'),c.get('value')]").replace("'BTC_N','ETH_N'];cost", "'BTC_N','ETH_N','BTC_H','ETH_R','native_parameter_value'];cost")
s=s.replace("p['axes']['BTC_N'].index(c['NB'])","p['axes']['BTC_H'].index(c['H'])").replace("p['axes']['ETH_N'].index(c['NE'])","p['axes']['ETH_R'].index(c['R'])").replace("h['NB']==p['axes']['BTC_N'][i+1] and h['NE']==c['NE']", "h['H']==p['axes']['BTC_H'][i+1] and h['R']==c['R']").replace("h['NE']==p['axes']['ETH_N'][j+1] and h['NB']==c['NB']", "h['R']==p['axes']['ETH_R'][j+1] and h['H']==c['H']")
s=s.replace("vals=p['axes'][c['asset']+'_N'];i=vals.index(c['N']);adj=[h for h in cells if i<2 and h['N']==vals[i+1]]", "vals=p['axes']['BTC_H' if c['asset']=='BTC' else 'ETH_R'];i=vals.index(c['value']);adj=[h for h in cells if i<2 and h['value']==vals[i+1]]")
s=s.replace('fixed_exposure_hold_comparisons.csv','matched_hold_comparisons.csv').replace("p['axes']['ETH_N']", "p['axes']['ETH_R']").replace("p['axes']['BTC_N']", "p['axes']['BTC_H']").replace("ETH actual entry N (USDT)","ETH funding budget ratio R").replace("BTC actual entry N (USDT)","BTC entry return hurdle H")
s=s.replace("Actual notional grid |", "BTC hurdle x ETH funding ratio | fixed N1000/4000 |").replace("fixed BTC L29/H3%/E1%;ETH", "BTC L29/H2.75,3,3.25%/E1%;ETH").replace("/M4/R.01/VW8", "/M4/R.00875,.01,.01125/VW8").replace("O=old1000/4500; N=new", "O=oldH.03/R.01; N=new")
s=s.replace("key=lambda c:c['N']", "key=lambda c:c['value']").replace("[c['N'] for c in cells]", "[c['value'] for c in cells]").replace("set_xlabel('Actual entry N (USDT)')", "set_xlabel('BTC H (fraction)' if a=='BTC' else 'ETH funding R')").replace("Native sources: only own sizing N varied; all signal rules fixed. Actual quantities/impact/funding computed; oldcenter readonly.", "Native rule sensitivity: BTC H three exact old sources; ETH own funding ratio R varied, fixed N1000/4000. No new BTC calculation; oldcenter readonly.")
s=s.replace("'native_component_one_applicable_sizing_axis':True", "'native_component_one_controlled_rule_axis':True").replace("'fixed_exposure_hold_not_matched_for_other_N_cells':True", "'same_actual_C_N_matched_hold_for_every_H_R_cell':True")
(R/'exports.py').write_text(s)
# Before-first-reserve definitions and binding.
s=(P/'definitions.py').read_text().replace('20261111T172818Z','20261111T192849Z').replace('20261111T152711Z','20261111T172818Z')
a=s.index('assert len(b)==');b=s.index("assert (R/'engine.py')",a);s=s[:a]+"assert len(b)==10 and p['axes']=={'BTC_H':[.0275,.03,.0325],'ETH_R':[.00875,.01,.01125]} and sum(z['scope']=='native' for z in b)==2 and len(p['read_only_references'])==8\n"+s[b:]
s=s.replace("assert json.loads((R/'review/native_capture_nov11_16_public.py_receipt.json').read_text())['exit_code']==0", "assert json.loads((R/'funding16_source_verification.json').read_text())['passed'] and json.loads((R/'policy_primitive_verification.json').read_text())['passed']")
a=s.index("  old=rs[z['reference_fingerprint']]");b=s.index('\nfor fp,z in p[',a)
s=s[:a]+'''  old=rs[z['reference_fingerprint']]['spec']['parameters'];changed={'entry_funding_volatility_ratio'};assert z['asset']=='ETH' and {k:v for k,v in q.items() if k not in changed}=={k:v for k,v in old.items() if k not in changed} and q['entry_funding_volatility_ratio']==z['value'] and q['fixed_entry_notional_usdt']==4000 and q['initial_capital_usdt']==15000
 else:
  assert [x['weight'] for x in sp['components']]==[1,1] and q['component_capitals_usdt']==[3750,15000] and q['initial_capital_usdt']==18750 and q['component_initial_entry_notionals_usdt']==[1000,4000] and q['BTC_return_hurdle']==z['H'] and q['ETH_entry_funding_volatility_ratio']==z['R']
'''+s[b:]
s=s.replace("==[0,0,6,6]", "==[0,6,0,0]").replace("R/'funding16_nov11_preflight.json'", "R/'funding16_source_verification.json',ROOT/'research/experiments/20261111T172818Z/funding16_nov11_preflight.json'")
s=s.replace("'new_financial_configs':8,'new_native':2,'new_parents':6", "'new_financial_configs':10,'new_native':2,'new_parents':8").replace("'old_unique_results':22,'old_native_banks':10", "'old_unique_results':8,'old_native_banks':6").replace("'native_own_N_axis_only':True", "'native_own_controlled_rule_axis_only':True").replace('PASS8defs/2newnative/6parents','PASS10defs/2newnative/8parents')
(R/'definitions.py').write_text(s)
print('Prepared financial sources, all accounting engine bytes unchanged')
