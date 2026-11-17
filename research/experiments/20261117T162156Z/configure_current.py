"""Freeze a new funding-budget ratio batch; reuse original money and account kernels."""
import ast,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;P=ROOT/'research/experiments/20261117T142055Z'
def edit(s,a,b):
 assert a in s,a
 return s.replace(a,b)
def write(n,s):ast.parse(s);(R/n).write_text(s)
names=['common.py','engine.py','core391_tail_safe.py','market.py','recent.py','portfolio.py','run.py','audit.py','audit_native.py','audit_helpers_complete.py','audit_incremental.py','audit_l4h02.py','audit_candidate.py','audit_fewm.py','project_l4h02_batch.py','project_candidate_batch.py','project_fewm_batch.py','parent_units.py','exports.py','observe_l4h02.py','observe_fewm.py','observe_candidate.py','journal.py','forward.py','forward_registry.py','audit_forward.py','commands.py','checks.py','collect.py','finalize.py','publish.py','definitions.py','freeze_confirmation.py','units_entry_cap.py']
for n in names:
 s=(P/n).read_text()
 if n not in ['engine.py','core391_tail_safe.py','common.py','market.py','recent.py','portfolio.py','audit_native.py','audit_helpers_complete.py','audit_incremental.py','audit_l4h02.py','audit_candidate.py','audit_fewm.py','project_l4h02_batch.py','project_candidate_batch.py','project_fewm_batch.py','audit_forward.py']:s=s.replace('20261117T122025Z',P.name)
 s=s.replace('ETH_ENTRY_VOLATILITY_CEILING','ETH_FUNDING_VOLATILITY_RATIO')
 if n in ['observe_fewm.py','observe_candidate.py']:s=s.replace('2866212','2897816')
 if n=='freeze_confirmation.py':
  s=s.replace('Freeze genuinely new ETH entry-volatility windows','Freeze genuinely new ETH funding-budget ratios')
  s=edit(s,'entry_cap_prior_lookup.json','funding_ratio_prior_lookup.json')
  s=edit(s,"assert {z['entry_cap'] for z in screen['all_fixed_context_ETH_matches']}=={.05625}","assert not any(z['funding_ratio'] in [.005,.00625] for z in screen['all_fixed_context_ETH_matches'])")
  s=edit(s,'VS=[.0525,.05625,.06];NEW=[.0525,.06]','VS=[.005,.00625,.0075];NEW=[.005,.00625]')
  s=edit(s,'es={.05625:reuse(E,.05625,.03)}','es={.0075:reuse(E,.0075,.03)}')
  s=edit(s,'entry_volatility_ceiling=window','entry_funding_volatility_ratio=window')
  s=edit(s,'EntryRiskV6Cap{str(window).replace(chr(46),chr(112))}_M4_BudgetVW8R0p0075','EntryRiskV6Cap0p05625_M4_BudgetVW8R{str(window).replace(chr(46),chr(112))}')
  s=edit(s,'parent_ETHEntryRiskV6Cap{str(window).replace(chr(46),chr(112))}BudgetVW8R0p0075','parent_ETHEntryRiskV6Cap0p05625BudgetVW8R{str(window).replace(chr(46),chr(112))}')
  s=s.replace('entryriskV6cap{window},M4actualmaturefundmedianfixedR.0075/VW8','entryriskV6cap.05625,M4actualmaturefundmedianR{window}/VW8')
  s=edit(s,'if window==.05625:','if window==.0075:')
  s=edit(s,'==(.0525,.03)','==(.00625,.03)');s=edit(s,"'W':.0525,'K':.03","'W':.00625,'K':.03")
  a=s.index("rules=copy.deepcopy(old['rules']);");b=s.index('for window in NEW:',a)
  s=s[:a]+'''rules=copy.deepcopy(old['rules']);rules['signal']='ETH longonly L5/H.02/E.0075;fast r=lastcompletedclose/close5completeddaysearlier-1. Contrarian base=-1 if r>.02,+1 if r<-.02,else actual if(actual==1 and r<.0075)or(actual==-1 and r>-.0075),else0. Finite normalized EWM S16 beta15/17, slope=level/completedlevel3daysearlier-1,strictK.0075;direction=+1 if slope>.0075,-1 if slope<-.0075,else0. Base accepted if base==actual or base==direction,else0. Fixed entryrisk sample-log-volV6/cap.05625:onlynew/reversed blocked if sigma>cap,equalitypasses. LatestM4mature1to36hinclusive/available<=signal signedactualfundmedian outgoingcost<=min(.0002,R[.005,.00625,.0075readonly]*past8completedunbiasedsamplelogvol*latesteligiblepastactualintervalhours/24). Fundingbudget equalitypasses,missingblocksnewentryonly,heldq/normalexitunchanged;finallymax(desired,0). OldR.0075nativeandparentsreadonly. BTCreadonlyL29 strictmainH[.03,.0325]/exitE.005/V10cap.0275/recent5directionalROCstrictly>.0025,newentrygatesonly,retainactualq. No fit/labels/futurevalues. EntryriskV6,carrybudgetVW8 andexecutionimpactV20 are separate.'
rules['legacy_metadata_resolution']='Only ETH entry_funding_volatility_ratio.005/.00625 changes. FastL5/return_hurdle/long_entry_return_hurdle/short_entry_return_hurdle.02,E.0075,finiteEWM16beta15/17lag3/K.0075,entryriskV6cap.05625,fundingM4/VW8 andallmoney fixed. Oldspec/report/statusbytespreserved.'
''' +s[b:]
  s=s.replace('eth-entry-volatility-ceiling','eth-funding-volatility-ratio')
  old='Tighter/looser ETH new-entry risk ceilings.0525/.06 atfixedV6 may alter adverse entry avoidance and trade costs,without changing fastROC,trend orcarrybudgetVW8 ormoney. Oldcap.05625 andBTCbanks readonly. RepresentativeETHcap.0525/BTCH.03 fixedbeforeoutcomes;noafterresultgridextension/reselection.'
  new='Tighter ETH mature-funding outgoing-budget ratiosR.005/.00625 versus readonlyR.0075 may avoid expensive carry entries while preserving fixedfastROC/trend/riskV6cap.05625/VW8 andnative money. OldBTCbanks readonly. RepresentativeETHR.00625/BTCH.03 fixedbeforeoutcomes;noafterresultgridextension/reselection.'
  s=edit(s,old,new)
  s=edit(s,'ETH new-entry unbiasedsamplelogvolceiling.0525/.05625/.06 atfixedV6;oldcap.05625readonly. L5/H.02/E.0075,EWM16beta15/17D3K.0075,M4/R.0075/VW8 fixed. EntryriskV is distinct fromcarrybudgetVW8 andexecutioncostV20.','ETH mature-funding budget ratioR.005/.00625/.0075readonly; budget=min(.0002,R*past8samplelogvol*latesteligibleactualintervalhours/24). L5/H.02/E.0075,EWM16D3K.0075,V6cap.05625,M4/VW8 fixed. R is a budget coefficient, not a capital or portfolio weight.')
  s=s.replace('ETH_native_only_own_entry_cap_axis','ETH_native_only_own_funding_ratio_axis').replace('ThreeETHriskceilings','ThreeETHfundingratios').replace('onlyactualentry_volatility_ceiling.0525/.06changesarenew','onlyactualentry_funding_volatility_ratio.005/.00625changesarenew').replace('Two genuinely new entry_volatility_ceiling.0525/.06atfixedV6andL5/H.02/E.0075/EWM16D3K.0075/M4/R.0075/VW8','Two genuinely new entry_funding_volatility_ratio.005/.00625atfixedL5/H.02/E.0075/EWM16D3K.0075/V6cap.05625/M4/VW8').replace('ETHriskCap.0525/.06','ETHfundingR.005/.00625').replace('presetCap.0525','presetR.00625')
 if n=='definitions.py':
  s=edit(s,"q['entry_funding_volatility_ratio']==.0075","q['entry_funding_volatility_ratio']==z['W'] and z['W'] in [.005,.00625]")
  s=edit(s,"q['entry_volatility_ceiling']==z['W'] and z['W'] in [.0525,.06]","q['entry_volatility_ceiling']==.05625")
  s=s.replace('entry_cap_verification.json','funding_ratio_verification.json').replace("'new_ETH_entry_cap':[.0525,.06],'old_ETH_entry_cap':.05625","'new_ETH_funding_ratio':[.005,.00625],'old_ETH_funding_ratio':.0075,'fixed_ETH_entry_cap':.05625").replace('only_ETH_entry_risk_cap_parameter_changed','only_ETH_funding_ratio_parameter_changed').replace('newentryCapspecs','newfundingRatiospecs')
 if n=='units_entry_cap.py':
  s=s.replace('Synthetic entry-volatility windows','Synthetic funding-budget ratios')
  s=edit(s,"p['entry_volatility_ceiling'] in [.0525,.06]","p['entry_volatility_ceiling']==.05625 and p['entry_funding_volatility_ratio'] in [.005,.00625]")
  s=edit(s,"cap=F(a['funding_filter']['cap_fraction_per_settlement']);median=", "budget_sigma=statistics.stdev([math.log(float(closes[j])/float(closes[j-1])) for j in range(i-8,i)]);expected=min(core.D('.0002'),core.D(str(p['entry_funding_volatility_ratio']))*core.D(str(budget_sigma))*core.D(8)/core.D(24));assert core.D(a['funding_filter']['cap_fraction_per_settlement'])==expected;cap=F(str(expected));median=")
  s=s.replace('entry_cap_verification.json','funding_ratio_verification.json').replace('new_entry_cap_sample_denominator_and_closed_prefix_checked','new_funding_ratio_cap_formula_and_closed_prefix_checked')
  s+='''
for ratio in [.005,.00625,.0075]:
 event={'events':[{'entry_interval_hours':core.D(8),'settlement_ts':sn-HOUR,'available_ts':sn,'realized_rate':core.D(0),'source_index':1}], 'median_rate':core.D(0),'count':1}
 for sigma in [0,.001,.05,1]:
  cap=engine.carry_cap(sigma,ratio,event);assert cap==min(core.D('.0002'),core.D(str(ratio))*core.D(str(sigma))*core.D(8)/core.D(24))
  event['median_rate']=cap;assert engine.funding_filter(1,0,event,sn,cap)[0]==1
  event['median_rate']=cap+core.D('1e-12');assert engine.funding_filter(1,0,event,sn,cap)[0]==0 and engine.funding_filter(1,1,event,sn,cap)[0]==1
 for invalid in [0,37]:assert engine.carry_cap(.05,ratio,{'events':[{'entry_interval_hours':core.D(invalid)}]}) is None
'''
  n='units_funding_ratio.py'
 if n=='commands.py':s=s.replace('units_entry_cap','units_funding_ratio')
 if n=='exports.py':
  s=edit(s,"['0.0525','0.05625 (old)','0.0600']","['0.0050','0.00625','0.0075 (old)']")
  s=edit(s,'ETH entry-risk ceiling (fraction)','ETH funding-budget ratio R')
  s=edit(s,'ETH entry-risk cap 0.0525/0.05625/0.06','ETH funding-budget R 0.005/0.00625/0.0075')
  s=edit(s,'M4/R0.0075/VW8 | raw whole banks','M4/VW8, fixed entry V6/cap0.05625 | raw whole banks')
 if n=='checks.py':
  s=s.replace("{'SMA':0,'candidate':0,'l4h02':6,'fewm':6} and len(cashflows)==12","{'SMA':0,'candidate':6,'l4h02':0,'fewm':0} and len(cashflows)==6")
  s=edit(s,"z['account'] in ['l4h02','fewm'] for z in cashflows","z['account']=='candidate' for z in cashflows")
  s=edit(s,"chains[a]['funding'][str(t)]==(0 if a=='candidate' else 6)","chains[a]['funding'][str(t)]==6")
  s=s.replace('currentActualFundingSplit0/0/6/6','currentActualFundingSplit0/6/0/0')
 if n=='finalize.py':
  s=s.replace('entry_cap_verification.json','funding_ratio_verification.json').replace('entry_cap_effect_decomposition.json','funding_ratio_effect_decomposition.json')
  s=edit(s,"{'SMA':0,'candidate':0,'l4h02':6,'fewm':6}","{'SMA':0,'candidate':6,'l4h02':0,'fewm':0}")
  s=s.replace("['2026-11-17T06:30:00Z','2026-11-17T08:30:00Z']","['2026-11-17T08:30:00Z','2026-11-17T10:30:00Z']").replace("['2026-11-17T08:10:00Z','2026-11-17T10:10:00Z']","['2026-11-17T10:10:00Z','2026-11-17T12:10:00Z']")
  s=s.replace('exports_retry1','exports').replace(",'plot_reformat_verification.json'",'').replace('only_ETH_entry_risk_cap_changed','only_ETH_funding_ratio_changed')
  s=s.replace("'new_independent_alpha_evidence':False","'new_independent_alpha_evidence':False")
 if n=='publish.py':s=s.replace('test ETH entry volatility ceilings','test tighter ETH funding budgets')
 write(n,s)
s=(P/'prepare.py').read_text().replace('20261117T122025Z',P.name).replace('2866212','2897816')
a=s.index('sources={rel(P/n):');b=s.index("assert sha(R/'engine.py')",a);s=s[:a]+"sources={rel(P/n):sha(P/n) for n in "+repr(names)+"}\n"+s[b:]
s=s.replace('1794889800000','1794897000000').replace('1794903060000','1794910260000').replace("['2026-11-17T04:30:00Z','2026-11-17T08:11:00Z']","['2026-11-17T06:30:00Z','2026-11-17T10:11:00Z']")
s=edit(s,"put(R/'window_funding_preflight.json',fresh);put(R/'funding08_nov17_preflight.json',fresh)","put(R/'window_funding_preflight.json',fresh);assert sha(R/'funding08_nov17_preflight.json')==sha(P/'funding08_nov17_preflight.json');assert responses==rd(P/'funding08_nov17_preflight.json')['public_fields_by_asset']")
a=s.index('windows.update(recorded_utc=');b=s.index("put(R/'account_windows.json'",a)
s=s[:a]+"windows.update(recorded_utc=now(),rules='SMA/single06:30to08:30,onlysingleincludesactual08funding;L4/FEWM08:10to10:10alreadybooked08andmustnotrepeat. Freshcompleteactualfundinglookup andeachownheldq/cash/mark/rate,negativeoutflowstress1/2/3,incomeunboosted. Zero newdailydecisions/fills,allnextdailyNov18_00:01;originalrules/capital/positions/terminals/fullNAVprefix retained,SMAfull69authority unchanged;no researchR adoption.')\n"+s[b:]
s=s.replace("'facts':[rd(R/'initial_read_failure.json')]+[", "'facts':[")
a=s.index("put(R/'implementation_plan.json'");b=s.index('print(json.dumps',a)
s=s[:a]+'''put(R/'implementation_plan.json',{'frozen_utc':now(),'hypothesis':'Tighter actualmaturefunding outflow-budget coefficientsR.005/.00625 versus readonlyR.0075 may avoid carry-expensive newentries. AllfastROC/finiteEWMtrend/entryriskV6cap.05625/M4/VW8 andnativecapital fixed. RepresentativeR.00625/BTCH.03 fixedbeforeoutcomes. No result-driven gridextension.','axes':{'ETH_FUNDING_VOLATILITY_RATIO':[.005,.00625,.0075],'BTC_MAIN_ENTRY_H':[.03,.0325]},'new_ETH_funding_ratios':[.005,.00625],'readonly_ETH_funding_ratio':.0075,'representative':{'ETH_funding_ratio':.00625,'BTC_H':.03},'new_configs':6,'stages':['full fixedspecs beforeoutcomes','synthetic causality/budget/equality tests','bind code anddata','reserve each6','actual391d evaluateonce','independent fullNAV/nativepolicy/money/cost/folds','allvariant exports','finish six','continue4originalaccounts afterownreserves','independent complete accountchain/funding checks','appendonly journal','registry andreadonlymonitorchecks','collect/seal/commit/pushmain','fullremoteevidenceverify','unlock/postreleaseverify'],'no_subagents':True,'no_real_orders':True,'no_new_paper10_trades':True})
''' +s[b:]
write('prepare.py',s)
print('PASS sources ready: R.005/.00625 x readonly BTCH.03/.0325, oldR.0075, zero financial/account calculations')
