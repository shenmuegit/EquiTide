from pathlib import Path
R=Path('research/experiments/20261111T212846Z');P=Path('research/experiments/20261111T192849Z')
s=(R/'run.py').read_text();a=s.index('def neighbors(');b=s.index('\ndef criteria',a)
s=s[:a]+'''def neighbors(c,p,full):
 rows=p['grid'] if c['scope']=='parent' else p['native_grid'];rows=[g for g in rows if abs(p['axes']['ETH_V'].index(g['V'])-p['axes']['ETH_V'].index(c['V']))<=1 and abs(p['axes']['ETH_VW'].index(g['VW'])-p['axes']['ETH_VW'].index(c['VW']))<=1]
 return [full[g['fingerprint']] for g in rows]
'''+s[b:]
s=s.replace("'dimension_count':2 if c['scope']=='parent' else 1", "'dimension_count':2").replace("{'fingerprint':fp,'H':c['H'],'R':c['R']", "{'fingerprint':fp,'V':c['V'],'VW':c['VW'],'H':c['H'],'R':c['R']").replace("'new_native_models':2", "'new_native_models':8").replace("'varied_axes':['BTC_entry_return_hurdle','ETH_funding_budget_ratio']", "'varied_axes':['ETH_entry_price_volatility_window','ETH_funding_budget_volatility_window']").replace("'old_unique_results_readonly':8", "'old_unique_results_readonly':6").replace("'native_component_own_controlled_rule_axis_only':True", "'ETH_native_and_parent_two_applicable_volatility_horizons':True,'new_BTC_calculations':0")
(R/'run.py').write_text(s)
s=(R/'audit.py').read_text();a=s.index(" if c['scope']=='parent':ng=");b=s.index(" ns=[full",a)
s=s[:a]+" rows=plan['grid'] if c['scope']=='parent' else plan['native_grid'];ng=[g for g in rows if abs(plan['axes']['ETH_V'].index(g['V'])-plan['axes']['ETH_V'].index(c['V']))<=1 and abs(plan['axes']['ETH_VW'].index(g['VW'])-plan['axes']['ETH_VW'].index(c['VW']))<=1];dimensions=2\n"+s[b:]
s=s.replace("(newnative,oldnative,parents,decisions)==(6,18,24,2220)", "(newnative,oldnative,parents,decisions)==(24,12,24,8880)").replace("'ETH_new_budget_ratios':[.00875,.01125]", "'ETH_new_price_V':[5,6,7],'ETH_new_budget_VW':[8,10,12],'ETH_fixed_budget_R':.00875").replace("'all3_BTC_H_policies_readonly':True", "'single_fixed_BTC_source_readonly':True").replace("'native_component_own_controlled_rule_axis_only':True", "'ETH_native_two_applicable_horizon_axes':True")
s=s.replace("source_specs[1]['parameters']['entry_funding_volatility_ratio']==c['R']", "source_specs[1]['parameters']['entry_funding_volatility_ratio']==c['R'] and source_specs[1]['parameters']['entry_volatility_window_days']==c['V'] and source_specs[1]['parameters']['entry_funding_budget_volatility_window_days']==c['VW']")
s=s.replace("x['H']==c['H'] and x['R']==c['R']", "x['H']==c['H'] and x['R']==c['R'] and x['V']==c['V'] and x['VW']==c['VW']")
(R/'audit.py').write_text(s)
s=(R/'definitions.py').read_text();a=s.index('assert len(b)==');b=s.index("assert (R/'engine.py')",a);s=s[:a]+"assert len(b)==16 and p['axes']=={'ETH_V':[5,6,7],'ETH_VW':[8,10,12]} and sum(z['scope']=='native' for z in b)==8 and len(p['read_only_references'])==6\n"+s[b:]
s=s.replace("changed={'entry_funding_volatility_ratio'}", "changed={'entry_volatility_window_days','entry_funding_budget_volatility_window_days'}").replace("q['entry_funding_volatility_ratio']==z['value']", "q['entry_volatility_window_days']==z['V'] and q['entry_funding_budget_volatility_window_days']==z['VW']")
s=s.replace("q['ETH_entry_funding_volatility_ratio']==z['R']", "q['ETH_entry_funding_volatility_ratio']==z['R'] and q['ETH_entry_volatility_window_days']==z['V'] and q['ETH_entry_funding_budget_volatility_window_days']==z['VW']")
s=s.replace("'negative_inclusive','negative_future_publication','negative_fixed_interval'", "'negative_price_future','negative_budget_future','negative_population'").replace("==[0,6,0,0]", "==[0,0,0,0]")
s=s.replace("'new_native_models_predeclared':2", "'new_native_models_predeclared':8").replace("'new_financial_configs':10,'new_native':2,'new_parents':8", "'new_financial_configs':16,'new_native':8,'new_parents':8").replace("'old_unique_results':8,'old_native_banks':6", "'old_unique_results':6,'old_native_banks':4").replace("'native_own_controlled_rule_axis_only':True", "'ETH_native_and_parent_two_applicable_horizon_axes':True").replace('PASS10defs/2newnative/8parents','PASS16defs/8newnative/8parents')
(R/'definitions.py').write_text(s)
print('Adapted real evaluator, independent auditor and before-reserve binding to V/VW two-axis study')
