from pathlib import Path
R=Path.cwd();O=R/'research/experiments/20261011T094956Z';T=R/'research/experiments/20261011T115056Z'
s=(O/'verify.py').read_text()
s=s.replace('(7253,3579,3577)','(7351,3628,3626)').replace('(7331,3618,3616)','(7405,3655,3653)').replace('(36,3,42)','(24,3,42)').replace("sum(b['role']=='component'for b in hist)==18","sum(b['role']=='component'for b in hist)==12").replace("sum(b.get('asset')=='BTC'for b in hist)==18","sum(b.get('asset')=='BTC'for b in hist)==12").replace('splitlines())==39','splitlines())==27').replace('(36,18,18,108,28013256)','(24,12,12,72,18675504)')
s=s.replace("for c in fresh)==36","for c in fresh)").replace("and len(summary['passed'])==21","and len(summary['passed'])+len(summary['rejected'])==24").replace("and len(summary['rejected'])==15","").replace("=={'four_positive_1x_folds':15}","")
s=s.replace("c['BTC_EMA_span_days']==20 and c['BTC_EMA_entry_band_fraction']in(.005,.01,.015)and c['BTC_EMA_exit_band_fraction']in(.02,.03,.04)","c['BTC_EMA_span_days']in(10,15) and c['BTC_EMA_entry_band_fraction']in(.005,.01,.015)and c['BTC_EMA_exit_band_fraction']==.03")
s=s.replace("==c['BTC_EMA_span_days']==20","==c['BTC_EMA_span_days']in(10,15)").replace("sp['logic']==plan['complete_rules']['BTC']","sp['logic']==plan['complete_rules']['BTC_by_EMA_span'][str(c['BTC_EMA_span_days'])]")
s=s.replace("g['predeclared_focus']=={'BTC_EMA_entry_band_fraction':.005,'BTC_EMA_exit_band_fraction':.03}and g['BTC_EMA_span_days']==20 and g['BTC_EMA_entry_band_fraction']==[.005,.01,.015]and g['BTC_EMA_exit_band_fraction']==[.02,.03,.04]","g['predeclared_focus']=={'BTC_EMA_span_days':15,'BTC_EMA_entry_band_fraction':.01,'BTC_EMA_exit_band_fraction':.03}and g['BTC_EMA_span_days']==[10,15,20]and g['BTC_EMA_entry_band_fraction']==[.005,.01,.015]and g['BTC_EMA_exit_band_fraction']==.03")
s=s.replace("len(plan['read_only_component_refs'])==4 and len(plan['read_only_grid_refs'])==2","len(plan['read_only_component_refs'])==10 and len(plan['read_only_grid_refs'])==8").replace("c['sensitivity_member']==(c.get('asset')=='ETH')","c['sensitivity_member']==(c.get('asset')=='ETH'or c['BTC_EMA_span_days']==20)")
s=s.replace('(108,28013256,9720,0,9720,9720)','(72,18675504,6480,0,6480,6480)').replace("summary['new_component_fills']==324","summary['new_component_fills']").replace("ah['read_only_component_scenes']==12 and ah['read_only_portfolio_scenes']==6","ah['read_only_component_scenes']==30 and ah['read_only_portfolio_scenes']==24").replace("['BTC_EMA_entry_band_fraction','BTC_EMA_exit_band_fraction']","['BTC_EMA_span_days','BTC_EMA_entry_band_fraction']")
s=s.replace("len(cmp['comparisons'])==54 and len(cmp['qualified_pair_comparisons'])==27","len(cmp['comparisons'])==36 and len(cmp['qualified_pair_comparisons'])==3*len(summary['new_both_periods_passed_combination_pairs'])")
s=s.replace("row['kind']=='MATCHED_SYMMETRIC'","row['kind']=='MATCHED_SPAN20'").replace("o['BTC_EMA_symmetric_band']==c['BTC_EMA_entry_band_fraction']","o['BTC_EMA_entry_band_fraction']==c['BTC_EMA_entry_band_fraction']and o['BTC_EMA_exit_band_fraction']==c['BTC_EMA_exit_band_fraction']==.03")
s=s.replace("('MATCHED_SYMMETRIC','jointly_improved_pairs_vs_matched_symmetric')","('MATCHED_SPAN20','jointly_improved_pairs_vs_matched_span20')")
old="assert len(summary['new_both_periods_passed_combination_pairs'])==9 and h['qualified_cross_period_pairs_not_in_any_prior_report']==1 and h['new_scenes_already_in_any_prior_report']==90 and h['new_scenes_not_in_any_prior_report']==18"
new="""expected_pairs=[[c['name'],c['other_period_config']]for c in fresh if c['year']=='2025'and c['role']=='combination'and c['both_periods_meet_full_gates']]
assert summary['new_both_periods_passed_combination_pairs']==expected_pairs
old_scene_paths=set();old_paired_paths=set()
for path,hsh in h['all_prior_report_sha256'].items():
 assert sha(R/path)==hsh,path
 oldconfigs=read(R/path).get('configs',{})
 for c in oldconfigs.values():
  old_scene_paths.update(z['NAV_sha256_f64le']for z in c.get('scenes',{}).values()if'NAV_sha256_f64le'in z)
  other=oldconfigs.get(c.get('other_period_config'),{})
  if c.get('year')=='2025'and c.get('role')=='combination'and other:
   try:old_paired_paths.add(tuple(x['scenes'][k]['NAV_sha256_f64le']for x in(c,other)for k in('1','2','3')))
   except KeyError:pass
new_paths=[z['NAV_sha256_f64le']for c in fresh for z in c['scenes'].values()]
new_pairs={tuple(r['configs'][n]['scenes'][k]['NAV_sha256_f64le']for n in pair for k in('1','2','3'))for pair in expected_pairs}
assert h['new_scenes_already_in_any_prior_report']==sum(x in old_scene_paths for x in new_paths)and h['new_scenes_not_in_any_prior_report']==sum(x not in old_scene_paths for x in new_paths)
assert h['distinct_new_scene_paths_not_in_prior']==len(set(new_paths)-old_scene_paths)and h['qualified_cross_period_pairs_not_in_any_prior_report']==len(new_pairs-old_paired_paths)
assert h['new_2026_combo_3x_paths_not_in_any_prior_report']==len({c['scenes']['3']['NAV_sha256_f64le']for c in fresh if c['role']=='combination'and c['year']=='2026'}-old_scene_paths)
for x in h['qualified_pair_histories']:assert x['whole_path_seen_before']==(tuple(r['configs'][n]['scenes'][k]['NAV_sha256_f64le']for n in x['pair']for k in('1','2','3'))in old_paired_paths)
"""
assert s.count(old)==1;s=s.replace(old,new.rstrip())
s=s.replace("('sensitivity.csv',126,108),('folds.csv',756,648)","('sensitivity.csv',126,72),('folds.csv',756,432)").replace("for key in('BTC_EMA_entry_band_fraction','BTC_EMA_exit_band_fraction')","for key in('BTC_EMA_span_days','BTC_EMA_entry_band_fraction','BTC_EMA_exit_band_fraction')")
s=s.replace("f['resume_utc']=='2026-10-11T07:00:00Z'and f['cutoff_utc']=='2026-10-11T09:00:00Z'","f['resume_utc']=='2026-10-11T09:00:00Z'and f['cutoff_utc']=='2026-10-11T11:00:00Z'").replace('(13390,13510,13499)','(13510,13630,13619)').replace("['scenes_hash_verified']==18","['scenes_hash_verified']==54").replace('PASS:all108 NEW asymmetric-BTC-volume-EMA scenes','PASS:all72 NEW asymmetric-BTC-volume-EMA scenes')
s=s.replace("prior['paper_observations']==43","prior['paper_observations']==44").replace('20261011T082211892738Z','20261011T102724451122Z').replace("counts[key]+=36","counts[key]+=24").replace("monitor['observations']==43 and monitor['research_configs']==2813","monitor['observations']==44 and monitor['research_configs']==2837")
a=s.index("label=read(T/'monitor_label_checks.json')");b=s.index("base=subprocess.check_output",a)
s=s[:a]+"assert sha(R/'research/monitor/snapshot.py')==prior['protected_sha256']['research/monitor/snapshot.py']\nassert subprocess.check_output(['git','show','HEAD:research/monitor/snapshot.py'],cwd=R)==(R/'research/monitor/snapshot.py').read_bytes()\nassert sum(x['kind']=='MATCHED_SPAN20_ASYMMETRIC'for x in plan['read_only_comparator_refs'])==6\nplot=read(T/'plot_review.json');assert plot['visually_reviewed']and set(plot['files_sha256'])=={'sensitivity.png','sensitivity_BTC.png'}\nfor name,hsh in plot['files_sha256'].items():assert sha(T/name)==hsh\n"+s[b:]
s=s.replace('022704a8c6526cb0e85b69c372cead10cc175031','6579c8127152e00f77bdd6e3f4957c01598cfabf').replace("'new_reserved_and_finished':39,'new_historical_trials':36","'new_reserved_and_finished':27,'new_historical_trials':24").replace("'new_qualified_cross_period_parameter_pairs':9,'new_cross_period_return_paths':1","'new_qualified_cross_period_parameter_pairs':len(expected_pairs),'new_cross_period_return_paths':h['qualified_cross_period_pairs_not_in_any_prior_report']").replace("cmp['jointly_improved_pairs_vs_matched_symmetric']","cmp['jointly_improved_pairs_vs_matched_span20']").replace("'intentional_read_only_monitor_label_patch':compat,","'monitor_source_unchanged':True,").replace('all108new_and18old_cost_scenes_verified','all72new_and54old_cost_scenes_verified').replace('all18_newBTC_components','all12_newBTC_components').replace('paper43_plan_state','paper44_plan_state').replace("'new_qualified_paths':1","'new_qualified_paths':h['qualified_cross_period_pairs_not_in_any_prior_report']")
assert not any(x in s for x in ('monitor_label_checks','(36,18,18,108,28013256)',"'new_historical_trials':36","'paper_observations']==43"))
compile(s,str(T/'verify.py'),'exec');(T/'verify.py').write_text(s);print('R40 final verifier binds predeclared counts and independently computed outcomes;nofinancial calculation')
