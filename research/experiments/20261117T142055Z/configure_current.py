"""Prepare a fixed cap sensitivity batch; original money and observer kernels remain unchanged."""
import ast,json
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[2];P=ROOT/'research/experiments/20261117T122025Z'
def edit(s,a,b):
 assert a in s,a
 return s.replace(a,b)
def write(n,s):
 ast.parse(s);(R/n).write_text(s)
names=['common.py','engine.py','core391_tail_safe.py','market.py','recent.py','portfolio.py','run.py','audit.py','audit_native.py','audit_helpers_complete.py','audit_incremental.py','audit_l4h02.py','audit_candidate.py','audit_fewm.py','project_l4h02_batch.py','project_candidate_batch.py','project_fewm_batch.py','parent_units.py','exports.py','observe_l4h02.py','observe_fewm.py','observe_candidate.py','journal.py','forward.py','forward_registry.py','audit_forward.py','commands.py','checks.py','collect.py','finalize.py','publish.py','definitions.py','freeze_confirmation.py','units_entry_volatility.py']
for n in names:
 s=(P/n).read_text()
 if n not in ['common.py','engine.py','core391_tail_safe.py','market.py','recent.py','portfolio.py','audit_native.py','audit_helpers_complete.py','audit_incremental.py','audit_l4h02.py','audit_candidate.py','audit_fewm.py','project_l4h02_batch.py','project_candidate_batch.py','project_fewm_batch.py','audit_forward.py']:
  s=s.replace('20261117T102048Z',P.name)
 s=s.replace('ETH_ENTRY_VOLATILITY_WINDOW','ETH_ENTRY_VOLATILITY_CEILING')
 if n in ['observe_fewm.py','observe_candidate.py']:s=s.replace('2834464','2866212')
 if n=='freeze_confirmation.py':
  s=edit(s,'entry_volatility_window_prior_lookup.json','entry_cap_prior_lookup.json')
  s=edit(s,"{z['entry_V'] for z in screen['all_fixed_context_ETH_matches']}=={6}","{z['entry_cap'] for z in screen['all_fixed_context_ETH_matches']}=={.05625}")
  s=edit(s,'VS=[5,6,7];NEW=[5,7]','VS=[.0525,.05625,.06];NEW=[.0525,.06]')
  s=edit(s,'es={6:reuse(E,6,.03)}','es={.05625:reuse(E,.05625,.03)}')
  s=edit(s,'entry_volatility_window_days=window','entry_volatility_ceiling=window')
  s=edit(s,'EntryRiskV{window}Cap0p05625','EntryRiskV6Cap{str(window).replace(chr(46),chr(112))}')
  s=edit(s,'entryriskV{window}cap.05625','entryriskV6cap{window}')
  s=edit(s,'if window==6:','if window==.05625:')
  s=edit(s,"==(5,.03)","==(.0525,.03)")
  s=edit(s,"'W':5,'K':.03","'W':.0525,'K':.03")
  a=s.index("rules=copy.deepcopy(old['rules']);");b=s.index('for window in NEW:',a)
  s=s[:a]+'''rules=copy.deepcopy(old['rules']);rules['signal']='ETH longonly L5/H.02/E.0075;fast r=lastcompletedclose/close5completeddaysearlier-1. Contrarian base=-1 if r>.02,+1 if r<-.02,else actual if(actual==1 and r<.0075)or(actual==-1 and r>-.0075),else0. Finite normalized EWM S16 beta15/17, slope=level/completedlevel3daysearlier-1,strictK.0075;direction=+1 if slope>.0075,-1 if slope<-.0075,else0. Base accepted if base==actual or base==direction,else0. Entry risk fixedV6 completed daily logreturns,unbiased sample standard deviation,cap[.0525,.05625readonly,.06]:onlynew/reversed blocked if sigma>cap,equalitypasses. LatestM4mature1to36hinclusive/available<=signal signedactualfundmedian outgoingcost<=min(.0002,.0075*past8completedunbiasedsamplelogvol*latesteligiblepastactualintervalhours/24). Budget equalitypasses,missingblocksnewentryonly,heldq/normalexitunchanged;finallymax(desired,0). Oldcap.05625nativeandparentsreadonly. BTCreadonlyL29 strictmainH[.03,.0325]/exitE.005/V10cap.0275/recent5directionalROCstrictly>.0025,newentrygatesonly,retainactualq. No fit/labels/futurevalues. EntryRiskV6,carrybudgetVW8 andexecutionimpactV20 are separate.'
rules['legacy_metadata_resolution']='Only ETH entry_volatility_ceiling.0525/.06 changes. FastL5/return_hurdle/long_entry_return_hurdle/short_entry_return_hurdle.02,E.0075,finiteEWM16beta15/17lag3/K.0075,entryriskV6,fundingM4/R.0075/VW8 andallmoney fixed. Oldspec/report/statusbytespreserved.'
''' +s[b:]
  s=s.replace('eth-entry-volatility-window','eth-entry-volatility-ceiling')
  s=s.replace('Shorter/longer ETH new-entry volatility measurement V5/V7 atfixedcap.05625 may alter adverse entry avoidance and trade costs,without changing fastROC,trend orcarrybudgetVW8 ormoney. OldV6 andBTCbanks readonly. RepresentativeETHV5/BTCH.03 fixedbeforeoutcomes;noafterresultgridextension/reselection.','Tighter/looser ETH new-entry risk ceilings.0525/.06 atfixedV6 may alter adverse entry avoidance and trade costs,without changing fastROC,trend orcarrybudgetVW8 ormoney. Oldcap.05625 andBTCbanks readonly. RepresentativeETHcap.0525/BTCH.03 fixedbeforeoutcomes;noafterresultgridextension/reselection.')
  s=s.replace('ETH new-entry unbiasedsamplelogvolwindow V5/6/7 atfixedcap.05625;oldV6readonly.','ETH new-entry unbiasedsamplelogvolceiling.0525/.05625/.06 atfixedV6;oldcap.05625readonly.')
  s=s.replace('ETH_native_only_own_entry_V_axis','ETH_native_only_own_entry_cap_axis').replace('ThreeETHriskwindows','ThreeETHriskceilings').replace('onlyactualentry_volatility_window_days5/7changesarenew','onlyactualentry_volatility_ceiling.0525/.06changesarenew')
  s=s.replace('Two genuinely new entry_volatility_window_days5/7atfixedcap.05625','Two genuinely new entry_volatility_ceiling.0525/.06atfixedV6').replace('ETHriskV5/7','ETHriskCap.0525/.06').replace('presetV5','presetCap.0525')
 if n=='definitions.py':
  s=edit(s,"q['entry_volatility_window_days']==z['W'] and z['W'] in [5,7] and q['entry_volatility_ceiling']==.05625","q['entry_volatility_window_days']==6 and q['entry_volatility_ceiling']==z['W'] and z['W'] in [.0525,.06]")
  s=s.replace('entry_volatility_window_verification.json','entry_cap_verification.json').replace("'new_ETH_entry_V':[5,7],'old_ETH_entry_V':6","'new_ETH_entry_cap':[.0525,.06],'old_ETH_entry_cap':.05625,'fixed_ETH_entry_V':6").replace('only_ETH_entry_risk_V_parameter_changed','only_ETH_entry_risk_cap_parameter_changed').replace('newentryVspecs','newentryCapspecs')
 if n=='units_entry_volatility.py':
  s=edit(s,'assert V in [5,7]','assert V==6 and p[\'entry_volatility_ceiling\'] in [.0525,.06]')
  s=edit(s,'sigma>.05625','sigma>float(p[\'entry_volatility_ceiling\'])')
  s=s.replace('entry_volatility_window_verification.json','entry_cap_verification.json').replace('new_entry_risk_V5_V7_sample_denominator_and_closed_prefix_checked','new_entry_cap_sample_denominator_and_closed_prefix_checked')
  n='units_entry_cap.py'
 if n=='commands.py':s=s.replace('units_entry_volatility','units_entry_cap')
 if n=='exports.py':
  s=s.replace('ETH new-entry volatility window V (days)','ETH new-entry sample volatility ceiling').replace('Preregistered ETH entry-risk V','Preregistered ETH entry-risk ceiling').replace("['5','6 (old)','7']","['0.0525','0.05625 (old)','0.0600']")
 if n=='checks.py':
  s=edit(s,"'first_actual_Nov17_00_public_capture_UTC':rd(R/'funding00_nov17_preflight.json')['recorded_utc']","'first_actual_Nov17_08_public_capture_UTC':rd(R/'funding08_nov17_preflight.json')['recorded_utc']")
  s=edit(s,"{'SMA':0,'candidate':0,'l4h02':0,'fewm':0} and len(cashflows)==0","{'SMA':0,'candidate':0,'l4h02':6,'fewm':6} and len(cashflows)==12")
  s=edit(s,"assert all(z['actual_settlement_ns']==1794873600000000000 and z['account'] in ['l4h02','fewm'] for z in cashflows)","assert all(z['actual_settlement_ns'] in fresh_times and z['account'] in ['l4h02','fewm'] for z in cashflows);assert all(chains[a]['funding'][str(t)]==(0 if a=='candidate' else 6) for t in fresh_times for a in ['candidate','l4h02','fewm'])")
  s=s.replace('currentActualFundingSplit0/0/0/0','currentActualFundingSplit0/0/6/6')
 if n=='finalize.py':
  s=s.replace('entry_volatility_window_verification.json','entry_cap_verification.json').replace(",'plot_reformat_verification.json'",'').replace('exports_retry1','exports').replace('final_checks_retry1','final_checks')
  s=edit(s,"all(z==0 for z in h['current_funding_records_by_account'].values())","h['current_funding_records_by_account']=={'SMA':0,'candidate':0,'l4h02':6,'fewm':6}")
  s=edit(s,"['2026-11-17T04:30:00Z','2026-11-17T06:30:00Z']","['2026-11-17T06:30:00Z','2026-11-17T08:30:00Z']")
  s=edit(s,"['2026-11-17T06:10:00Z','2026-11-17T08:10:00Z']","['2026-11-17T08:10:00Z','2026-11-17T10:10:00Z']")
  s=edit(s,"v['new_funding_settlements']==v['new_daily_events']==v['new_fills']==0","v['new_funding_settlements']==aw['current_funding_records_by_account'][stem] and v['new_daily_events']==v['new_fills']==0")
  s=s.replace('only_ETH_entry_risk_V_changed','only_ETH_entry_risk_cap_changed').replace('original_rules_terminal_dates_cash_and_units_unchanged','original_rules_terminal_dates_and_own_continuous_accounts_preserved')
 if n=='publish.py':s=s.replace('test ETH entry volatility windows','test ETH entry volatility ceilings')
 write(n,s)

screen=json.loads((R/'entry_cap_ratio_prior_lookup.json').read_text());screen['all_fixed_context_ETH_matches']=[z for z in screen['all_fixed_context_ETH_matches'] if z['funding_ratio']==.0075];(R/'entry_cap_prior_lookup.json').write_text(json.dumps(screen,ensure_ascii=False,indent=2)+'\n')
s=(P/'prepare.py').read_text().replace('20261117T102048Z',P.name).replace('2834464','2866212')
a=s.index('names=[');b=s.index("assert sha(R/'engine.py')",a)
s=s[:a]+"sources={rel(P/n):sha(P/n) for n in "+repr(names)+"}\n"+s[b:]
s=edit(s,'1794882600000','1794889800000');s=edit(s,'1794895860000','1794903060000')
s=edit(s,"assert responses=={'BTC':[],'ETH':[]},responses","assert all(len(xs)==1 for xs in responses.values()),responses\nassert all(1794889800000<int(z['fundingTime'])<=1794903060000 and 'fundingRate' in z and 'markPrice' in z for xs in responses.values() for z in xs),responses")
s=edit(s,"['2026-11-17T02:30:00Z','2026-11-17T06:11:00Z']","['2026-11-17T04:30:00Z','2026-11-17T08:11:00Z']")
s=edit(s,"put(R/'window_funding_preflight.json',fresh)","put(R/'window_funding_preflight.json',fresh);put(R/'funding08_nov17_preflight.json',fresh)")
old="windows[a]={'start_utc':start,'cutoff_utc':cut,'expected_daily_events_utc':[],'expected_funding_utc':[],'expected_funding_by_asset':{'BTC':[],'ETH':[]},'expected_funding_records':0,'next_daily_decision_utc':daily}"
new="startms=int(datetime.fromisoformat(start.replace('Z','+00:00')).timestamp()*1000);cutms=int(datetime.fromisoformat(cut.replace('Z','+00:00')).timestamp()*1000);fr={s:[z for z in responses[s] if startms<int(z['fundingTime'])<=cutms] for s in ['BTC','ETH']} if a!='SMA' else {'BTC':[],'ETH':[]};times=sorted({int(z['fundingTime']) for xs in fr.values() for z in xs});windows[a]={'start_utc':start,'cutoff_utc':cut,'expected_daily_events_utc':[],'expected_funding_utc':[datetime.fromtimestamp(t/1000,timezone.utc).isoformat().replace('+00:00','Z') for t in times],'expected_funding_by_asset':fr,'expected_funding_records':3*sum(map(len,fr.values())),'next_daily_decision_utc':daily}"
s=edit(s,old,new)
a=s.index('windows.update(recorded_utc=');b=s.index("put(R/'account_windows.json'",a)
s=s[:a]+"windows.update(recorded_utc=now(),rules='SMA/single04:30to06:30 no newfunding;L4/FEWM06:10to08:10 include the fresh actual settlement fields. Each own signedq and own fundingcashflow,negativecoststress1/2/3,incomeunboosted. No newdailydecisions/fills;allnextdailyNov18_00:01. Preserve all old prefixes/rules/capital/positions and originalterminals;SMAfull69authorityunchanged,no researchcapadoption.')\n"+s[b:]
s=s.replace("'facts':[{**z", "'facts':[rd(R/'initial_read_failure.json')]+[{**z")
a=s.index("put(R/'implementation_plan.json'");b=s.index("print(json.dumps",a)
s=s[:a]+'''put(R/'implementation_plan.json',{'frozen_utc':now(),'hypothesis':'Only change ETH entry sample-log-vol ceiling.0525/.06 versus readonly.05625 atfixedV6; tighter/looser entryrisk may alter adverseentryavoidance. AllfastROC/finiteEWMtrend/fundingM4R.0075VW8/money fixed. Presetbatch nooutcomeextension.','axes':{'ETH_ENTRY_VOLATILITY_CEILING':[.0525,.05625,.06],'BTC_MAIN_ENTRY_H':[.03,.0325]},'new_ETH_entry_caps':[.0525,.06],'readonly_ETH_entry_cap':.05625,'representative':{'ETH_entry_cap':.0525,'BTC_H':.03},'new_configs':6,'stages':['freeze complete specs andfailuregates','synthetic causal boundary tests','bind code anddata','reserve six independently','evaluate391d exactlyonce','independent fullNAV/policy/money/cost/foldaudit','allvariant exports','finish six','continue4originalaccounts withownreserves and actualfunding','independent fullaccountchainaudit','appendonly registry shard','registry+readonlymonitorchecks','collectandseal','commit/pushmain','remote complete treeandblobverification','nativeunlock+postreleaseaudit'],'no_subagents':True,'no_real_orders':True,'no_new_paper10_trades':True})
''' +s[b:]
write('prepare.py',s)
print('PASS sources prepared, cap.0525/.06 fixed, no financial/account calculation')
