"""Define the directional adverse-risk experiment before any reservation or returns."""
import ast,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261116T020401Z';sys.path.insert(0,str(R));from common import *
assert not any((R/n).exists() for n in ['plan.json','batch.json','report.json','code_binding_before_evaluation.json'])
def edit(name,pairs):
 p=R/name;s=p.read_text()
 for a,b in pairs:assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);p.write_text(s)
old="raw,r=btc.target(m['closes'],i,int(p['lookback_days']),float(p['return_hurdle']),actual,float(p['exit_buffer_fraction']));sigma=btc_entry_sigma(m['closes'],i,V);wanted=entry_filter(raw,actual,sigma,cap)"
new="raw,r=btc.target(m['closes'],i,int(p['lookback_days']),float(p['return_hurdle']),actual,float(p['exit_buffer_fraction']));sigma=btc_entry_sigma(m['closes'],i,V);blend=float(p.get('entry_adverse_volatility_blend',0));effective,adverse=btc_directional_risk(m['closes'],i,V,raw,blend);wanted=entry_filter(raw,actual,effective,cap)\n  if blend:assert p['entry_volatility_estimator']=='directional_adverse_RMS_blend' and p['entry_adverse_volatility_target_logreturn']==0 and p['entry_adverse_volatility_denominator']=='population_n'"
edit('engine.py',[(old,new),("'entry_volatility_gate_scope':'new_or_reversed_position_only'}","'entry_volatility_gate_scope':'new_or_reversed_position_only','observed_entry_filter_vol':effective,'directional_adverse_RMS':adverse,'entry_adverse_volatility_blend':blend,'entry_volatility_estimator':'directional_adverse_RMS_blend' if blend else 'sample_logvol'}")])
p=R/'engine.py';s=p.read_text();at=s.index('\ndef latest_funding(');s=s[:at]+'''
def btc_directional_risk(closes,i,window,direction,blend):
 assert window==10 and direction in [-1,0,1] and blend in [0,.25,.5]
 sigma=btc_entry_sigma(closes,i,window)
 adverse=math.sqrt(math.fsum(min(direction*math.log(float(closes[j])/float(closes[j-1])),0.)**2 for j in range(i-window,i))/window)
 return (1-blend)*sigma+blend*adverse,adverse

'''+s[at:];ast.parse(s);p.write_text(s)
# Independent audit uses a separate signed-squared-sum calculation, retaining raw sigma.
old="wanted=0 if raw and raw!=actual and sigma>cap else raw\n   assert audit['kind']=='BTC_momentum_entry_vol'"
new="blend=float(p.get('entry_adverse_volatility_blend',0));bad_squared=[(raw*x)**2 for x in xs if raw*x<0];adverse=math.sqrt(sum(bad_squared)/V);effective=sigma*(1-blend)+adverse*blend;wanted=0 if raw and raw!=actual and effective>cap else raw\n   if blend:\n    assert p['entry_volatility_estimator']=='directional_adverse_RMS_blend' and p['entry_adverse_volatility_target_logreturn']==0 and p['entry_adverse_volatility_denominator']=='population_n' and audit['entry_adverse_volatility_blend']==blend and audit['entry_volatility_estimator']=='directional_adverse_RMS_blend';near(audit['directional_adverse_RMS'],adverse,1e-12);near(audit['observed_entry_filter_vol'],effective,1e-12)\n   assert audit['kind']=='BTC_momentum_entry_vol'"
edit('audit.py',[(old,new)])
for name in ['run.py','audit.py','exports.py']:edit(name,[('BTC_ENTRY_VOL_CAP','BTC_ADVERSE_BLEND')])
edit('exports.py',[('BTC entry sample-logvol ceiling','BTC adverse-risk blend gamma'),("['2.625%','2.750%','2.875%']","['0 (old)','0.25','0.50']"),('Preregistered BTC V10 entry-volatility ceiling','Preregistered BTC directional adverse-risk blend')])
edit('parent_units.py',[("g['W']==.0275","g['W']==.25"),("for cap in [.02625,.0275,.02875]:","for cap in [.0275]:")])
edit('commands.py',[("['freeze_caps.py']","['freeze_blend.py']")])
for name in ['review/diagnostics.py','review/visual_review.py']:
 edit(name,[('BTC_entry_volatility_ceiling','BTC_adverse_volatility_blend'),('cap2p75percent','gamma0')])
edit('review/diagnostics.py',[("center=btc[.0275]","center=btc[0]"),('for V in [.02625,.02875]:','for V in [.25,.5]:'),("c['W']==.0275","c['W']==0"),("best['W'] in [.02625,.02875]","best['W'] in [0,.5]"),('actual BTC entry-volatility-ceiling trade changes','actual BTC directional adverse-risk trade changes')])
edit('review/visual_review.py',[('{.02625,.0275,.02875}','{0,.25,.5}'),('[.02625,.02875]','[.25,.5]'),("y['BTC_adverse_volatility_blend']==.0275","y['BTC_adverse_volatility_blend']==0"),('three BTC entry-volatility ceilings with old2.75percent reference at the middle','three BTC gamma values with old gamma0 reference at the lower boundary')])
edit('review/setup_blend.py',[('SMA/single16:30to18:30 andL4/FEWM18:10to20:10','SMA/single18:30to20:30 andL4/FEWM20:10to22:10'),('Next18:30to20:30 and20:10to22:10','Next20:30to22:30 and22:10to00:10;L4/FEWM next window crosses Nov16_00:01 daily decision'),('adoption of research caps','adoption of research blends')])
# Bind all pre-existing monetary helpers exactly; BTC policy deliberately changes.
p=R/'definitions.py';s=p.read_text();a=s.index(';funs=lambda');b=s.index('\nassert len(batch)',a)
s=s[:a]+'''
funs=lambda f:{x.name:ast.dump(x,include_attributes=False) for x in ast.parse(f.read_text()).body if isinstance(x,ast.FunctionDef)}
before,after=funs(P/'engine.py'),funs(R/'engine.py');assert set(after)-set(before)=={'btc_directional_risk'} and all(before[k]==after[k] for k in before if k!='base_decide') and before['base_decide']!=after['base_decide']
oldnode=ast.parse((P/'engine.py').read_text()).body;newnode=ast.parse((R/'engine.py').read_text()).body
oldbase=next(x for x in oldnode if isinstance(x,ast.FunctionDef) and x.name=='base_decide');newbase=next(x for x in newnode if isinstance(x,ast.FunctionDef) and x.name=='base_decide')
assert all(ast.dump(x,include_attributes=False)==ast.dump(y,include_attributes=False) for x,y in zip(oldbase.body[3:],newbase.body[3:])) and len(oldbase.body)==len(newbase.body)
assert sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py')
'''+s[b:]
s=s.replace("q['entry_volatility_ceiling'] in [.02625,.02875]","q['entry_volatility_ceiling']==.0275 and q['entry_adverse_volatility_blend'] in [.25,.5]")
s=s.replace("descriptor.startswith('BTC completedROC L29/strictentryH.03/fixedexitE.005/priorV10samplelogvolCap[.02625,.0275,.02875].')","descriptor.startswith('BTC completedROC L29/strictentryH.03/fixedexitE.005/V10directionalAdverseBlend[0,.25,.5]/cap.0275.')")
s=s.replace("['parameters']['entry_volatility_ceiling']==z['W']","['parameters']['entry_adverse_volatility_blend']==z['W']")
s=s.replace("'native_caps':[.02625,.02875],'old_cap_readonly':.0275","'native_blends':[.25,.5],'old_blend_readonly':0,'fixed_cap':.0275")
s=s.replace("'policy_and_accounting_AST_equal_after_allowlist_normalization':True,'policy_and_money_formulas_unchanged_except_predeclared_parameter_allowlist':True","'BTC_entry_risk_policy_intentionally_changed':True,'ETH_AST_and_all_existing_nonpolicy_helpers_unchanged':True")
s=s.replace("'all_policy_and_native_money_AST_unchanged_after_allowlist_normalization':True","'only_BTC_entry_risk_policy_changed_all_money_and_ETH_unchanged':True")
s=s.replace('only declared entry-cap assertion allowlist widened;full money core bytes/normalized policy AST unchanged','BTC directional adverse-risk formula bound; money core bytes, simulate AST and ETH unchanged');ast.parse(s);p.write_text(s)
p=R/'finalize.py';s=p.read_text().replace('configure_caps.py','configure_blend_retry1.py').replace('prepare_caps.py','prepare_blend.py').replace('setup_caps.py','setup_blend.py').replace(", 'cap_history_aliases.py'",'')
s='\n'.join(l for l in s.splitlines() if not l.startswith("ca=rd(R/'known_cap_path_alias_verification.json')"))+'\n'
s=s.replace("'only_predeclared_validation_allowlist_changed':True","'only_predeclared_validation_allowlist_changed':False,'BTC_directional_entry_risk_policy_intentionally_changed':True").replace("'engine_AST_equal_after_allowlist_normalization':True","'ETH_and_simulate_AST_unchanged':True").replace("m['new_actual_results']['policy_and_money_formulas_unchanged_except_parameter_guard']=True","m['new_actual_results']['only_BTC_directional_entry_risk_formula_changed_money_unchanged']=True")
s=s.replace('predeclared BTC entry ceiling assertion allowlist,not policy formula or money core','predeclared BTC directional adverse-risk blend; ETH and money core unchanged');ast.parse(s);p.write_text(s)
edit('publish.py',[('research: validate BTC entry-volatility ceilings and continue frozen accounts','research: test BTC directional adverse-risk blends and continue frozen accounts')])
put(R/'stdout_label_notes.json',{'round':R.name,'notes':[],'current_scalar_and_window_labels_checked_before_binding':True,'old_round_raw_logs_and_errata_preserved':True,'financial_or_account_reruns':0})
put(R/'primary_source_reads_current.json',{'round':R.name,'observed_reads_recorded_utc':now(),'reads':[{'url':u,'web_reference':w,'access_UTC_date':'2026-11-16','read_success':True} for u,w in [('https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data','turn291view0'),('https://github.com/binance/binance-public-data/blob/master/README.md','turn291view1')]],'tool_timeouts':0,'HTTP_capture_timestamp_not_claimed':True})
(R/'research_work_plan.md').write_text('固定BTC L29/H3%/E0.5%、V10与风险门槛2.75%。gamma0旧实际结果只读；新gamma.25/.5把无偏总样本波动率与逆期望持仓方向logreturn的RMS（目标0、分母n）线性混合，sigma_eff=(1-gamma)*sigma+gamma*sqrt(sum(min(direction*r,0)^2)/10)。仅新或反手过滤，持仓q/退出/成交成本核算保持。ETH R.00875/.01只读，raw整银行[1,1]不归一化；代表gamma.25/R.01。6新定义逐一reserve后完整391日和三成本，严格两轴及全NAV核验再finish，正负全保留。\n\n原SMA/single18:30→20:30、L4/FEWM20:10→22:10，各自延续旧现金/持仓/desired/规则，原67日权威保持；不采用新策略。下轮20:30→22:30与22:10→Nov16_00:10，后者跨00:01原日决策，必须使用完成日线原adapter与真实资金费。\n\n锁内检查、只读snapshot、main提交推送、完整远端核验并释锁；不下真实订单、不委派、不建分支或定时任务。\n')
print('PASS directional adverse-risk formula, separate independent audit and gamma axes configured before first reserve')
