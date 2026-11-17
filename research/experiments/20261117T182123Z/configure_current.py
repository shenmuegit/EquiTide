"""Prepare genuinely new carry-budget windows; keep financial and original account kernels exact."""
import ast,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;P=ROOT/'research/experiments/20261117T162156Z'
def edit(s,a,b):
 assert a in s,a
 return s.replace(a,b)
def write(n,s):ast.parse(s);(R/n).write_text(s)
names=['common.py','engine.py','core391_tail_safe.py','market.py','recent.py','portfolio.py','run.py','audit.py','audit_native.py','audit_helpers_complete.py','audit_incremental.py','audit_l4h02.py','audit_candidate.py','audit_fewm.py','project_l4h02_batch.py','project_candidate_batch.py','project_fewm_batch.py','parent_units.py','exports.py','observe_l4h02.py','observe_fewm.py','observe_candidate.py','journal.py','forward.py','forward_registry.py','audit_forward.py','commands.py','checks.py','collect.py','finalize.py','publish.py','definitions.py','freeze_confirmation.py','units_funding_ratio.py']
for n in names:
 s=(P/n).read_text()
 if n not in ['engine.py','core391_tail_safe.py','common.py','market.py','recent.py','portfolio.py','audit_native.py','audit_helpers_complete.py','audit_incremental.py','audit_l4h02.py','audit_candidate.py','audit_fewm.py','project_l4h02_batch.py','project_candidate_batch.py','project_fewm_batch.py','audit_forward.py']:s=s.replace('20261117T142055Z',P.name)
 s=s.replace('ETH_FUNDING_VOLATILITY_RATIO','ETH_FUNDING_BUDGET_WINDOW')
 if n in ['observe_fewm.py','observe_candidate.py']:s=s.replace('2897816','2931227')
 if n=='freeze_confirmation.py':
  s=s.replace('funding-budget ratios','funding-budget windows').replace('funding_ratio_prior_lookup.json','funding_budget_window_prior_lookup.json')
  s=edit(s,"z['funding_ratio'] in [.005,.00625]","z['budget_window'] in [7,9]")
  s=edit(s,'VS=[.005,.00625,.0075];NEW=[.005,.00625]','VS=[7,8,9];NEW=[7,9]')
  s=edit(s,'es={.0075:reuse(E,.0075,.03)}','es={8:reuse(E,8,.03)}')
  s=edit(s,'entry_funding_volatility_ratio=window','entry_funding_budget_volatility_window_days=window')
  s=edit(s,'BudgetVW8R{str(window).replace(chr(46),chr(112))}','BudgetVW{window}R0p0075')
  s=edit(s,'M4actualmaturefundmedianR{window}/VW8','M4actualmaturefundmedianR.0075/VW{window}')
  s=edit(s,'if window==.0075:','if window==8:');s=edit(s,'==(.00625,.03)','==(7,.03)');s=edit(s,"'W':.00625,'K':.03","'W':7,'K':.03")
  a=s.index("rules=copy.deepcopy(old['rules']);");b=s.index('for window in NEW:',a)
  s=s[:a]+'''rules=copy.deepcopy(old['rules']);rules['signal']='ETH longonly L5/H.02/E.0075;fast r=lastcompletedclose/close5completeddaysearlier-1. Contrarian base=-1 if r>.02,+1 if r<-.02,else actual if(actual==1 and r<.0075)or(actual==-1 and r>-.0075),else0. Finite normalized EWM S16 beta15/17, slope=level/completedlevel3daysearlier-1,strictK.0075;direction=+1 if slope>.0075,-1 if slope<-.0075,else0. Base accepted if base==actual or base==direction,else0. Fixed entryrisk sample-log-volV6/cap.05625:onlynew/reversed blocked if sigma>cap,equalitypasses. LatestM4mature1to36hinclusive/available<=signal signedactualfundmedian outgoingcost<=min(.0002,.0075*pastVW[7,8readonly,9]completedunbiasedsamplelogvol*latesteligiblepastactualintervalhours/24). Fundingbudget equalitypasses,missingblocksnewentryonly,heldq/normalexitunchanged;finallymax(desired,0). OldVW8nativeandparentsreadonly. BTCreadonlyL29 strictmainH[.03,.0325]/exitE.005/V10cap.0275/recent5directionalROCstrictly>.0025,newentrygatesonly,retainactualq. No fit/labels/futurevalues. EntryriskV6,carrybudgetVW7/8/9 andexecutionimpactV20 are separate.'
rules['legacy_metadata_resolution']='Only ETH entry_funding_budget_volatility_window_days7/9 changes. FastL5/return_hurdle/long_entry_return_hurdle/short_entry_return_hurdle.02,E.0075,finiteEWM16beta15/17lag3/K.0075,entryriskV6cap.05625,fundingM4/R.0075 andallmoney fixed. Oldspec/report/statusbytespreserved.'
''' +s[b:]
  s=s.replace('eth-funding-volatility-ratio','eth-funding-budget-volatility-window')
  old='Tighter ETH mature-funding outgoing-budget ratiosR.005/.00625 versus readonlyR.0075 may avoid expensive carry entries while preserving fixedfastROC/trend/riskV6cap.05625/VW8 andnative money. OldBTCbanks readonly. RepresentativeETHR.00625/BTCH.03 fixedbeforeoutcomes;noafterresultgridextension/reselection.'
  new='Faster/slower carry-budget sample-log-vol windowsVW7/VW9 versus readonlyVW8 may adapt to changing risk andcarry costs while preserving fixedfastROC/trend/riskV6cap.05625/M4R.0075 andnative money. OldBTCbanks readonly. RepresentativeETHVW7/BTCH.03 fixedbeforeoutcomes;noafterresultgridextension/reselection.'
  s=edit(s,old,new)
  s=edit(s,'ETH mature-funding budget ratioR.005/.00625/.0075readonly; budget=min(.0002,R*past8samplelogvol*latesteligibleactualintervalhours/24). L5/H.02/E.0075,EWM16D3K.0075,V6cap.05625,M4/VW8 fixed. R is a budget coefficient, not a capital or portfolio weight.','ETH carry-budget volatility windowVW7/8readonly/9; budget=min(.0002,.0075*pastVWsamplelogvol*latesteligibleactualintervalhours/24). L5/H.02/E.0075,EWM16D3K.0075,V6cap.05625,M4/R.0075 fixed. This window is distinct from entryriskV6 and executionimpactV20.')
  s=s.replace('ETH_native_only_own_funding_ratio_axis','ETH_native_only_own_budget_window_axis').replace('ThreeETHfundingratios','ThreeETHfundingbudgetwindows').replace('onlyactualentry_funding_volatility_ratio.005/.00625changesarenew','onlyactualentry_funding_budget_volatility_window_days7/9changesarenew').replace('Two genuinely new entry_funding_volatility_ratio.005/.00625atfixedL5/H.02/E.0075/EWM16D3K.0075/V6cap.05625/M4/VW8','Two genuinely new entry_funding_budget_volatility_window_days7/9atfixedL5/H.02/E.0075/EWM16D3K.0075/V6cap.05625/M4/R.0075').replace('ETHfundingR.005/.00625','ETHbudgetVW7/9').replace('presetR.00625','presetVW7')
 if n=='definitions.py':
  s=edit(s,"q['entry_funding_budget_volatility_window_days']==8 and q['entry_funding_volatility_ratio']==z['W'] and z['W'] in [.005,.00625]","q['entry_funding_budget_volatility_window_days']==z['W'] and z['W'] in [7,9] and q['entry_funding_volatility_ratio']==.0075")
  s=s.replace('funding_ratio_verification.json','budget_window_verification.json').replace("'new_ETH_funding_ratio':[.005,.00625],'old_ETH_funding_ratio':.0075","'new_ETH_budget_window':[7,9],'old_ETH_budget_window':8,'fixed_ETH_funding_ratio':.0075").replace('only_ETH_funding_ratio_parameter_changed','only_ETH_budget_window_parameter_changed').replace('newfundingRatiospecs','newbudgetWindowspecs')
 if n=='units_funding_ratio.py':
  s=s.replace('Synthetic funding-budget ratios','Synthetic carry-budget windows')
  s=edit(s,"p['entry_funding_volatility_ratio'] in [.005,.00625]","p['entry_funding_volatility_ratio']==.0075 and p['entry_funding_budget_volatility_window_days'] in [7,9]")
  s=edit(s,'for j in range(i-8,i)]);expected=','for j in range(i-int(p[\'entry_funding_budget_volatility_window_days\']),i)]);expected=')
  s=s.replace('funding_ratio_verification.json','budget_window_verification.json').replace('new_funding_ratio_cap_formula_and_closed_prefix_checked','new_budget_VW7_VW9_sample_vol_formula_and_closed_prefix_checked');n='units_budget_window.py'
 if n=='commands.py':s=s.replace('units_funding_ratio','units_budget_window')
 if n=='exports.py':
  s=edit(s,"['0.0050','0.00625','0.0075 (old)']","['7','8 (old)','9']")
  s=s.replace('ETH funding-budget ratio R','ETH carry-budget window VW (days)').replace('ETH funding-budget R 0.005/0.00625/0.0075','ETH carry-budget VW 7/8/9').replace('M4/VW8, fixed entry','M4/R0.0075, fixed entry')
 if n=='checks.py':
  s=edit(s,"{'SMA':0,'candidate':6,'l4h02':0,'fewm':0} and len(cashflows)==6","{'SMA':0,'candidate':0,'l4h02':0,'fewm':0} and len(cashflows)==0")
  s=s.replace('currentActualFundingSplit0/6/0/0','currentActualFundingSplit0/0/0/0')
 if n=='finalize.py':
  s=s.replace('funding_ratio_verification.json','budget_window_verification.json').replace('funding_ratio_effect_decomposition.json','budget_window_effect_decomposition.json').replace("{'SMA':0,'candidate':6,'l4h02':0,'fewm':0}","{'SMA':0,'candidate':0,'l4h02':0,'fewm':0}")
  s=s.replace("['2026-11-17T08:30:00Z','2026-11-17T10:30:00Z']","['2026-11-17T10:30:00Z','2026-11-17T12:30:00Z']").replace("['2026-11-17T10:10:00Z','2026-11-17T12:10:00Z']","['2026-11-17T12:10:00Z','2026-11-17T14:10:00Z']").replace('only_ETH_funding_ratio_changed','only_ETH_budget_window_changed')
 if n=='publish.py':s=s.replace('test tighter ETH funding budgets','test ETH carry budget windows')
 write(n,s)
s=(P/'prepare.py').read_text().replace('20261117T142055Z',P.name).replace('2897816','2931227')
a=s.index('sources={rel(P/n):');b=s.index("assert sha(R/'engine.py')",a);s=s[:a]+"sources={rel(P/n):sha(P/n) for n in "+repr(names)+"}\n"+s[b:]
s=s.replace('1794897000000','1794904200000').replace('1794910260000','1794917460000').replace("['2026-11-17T06:30:00Z','2026-11-17T10:11:00Z']","['2026-11-17T08:30:00Z','2026-11-17T12:11:00Z']")
s=edit(s,"assert all(len(xs)==1 for xs in responses.values()),responses","assert responses=={'BTC':[],'ETH':[]},responses")
s=edit(s,";assert responses==rd(P/'funding08_nov17_preflight.json')['public_fields_by_asset']",'')
a=s.index('windows.update(recorded_utc=');b=s.index("put(R/'account_windows.json'",a)
s=s[:a]+"windows.update(recorded_utc=now(),rules='SMA/single08:30to10:30;L4/FEWM10:10to12:10. Freshcompleteactualfundinglookup hasnoevents;all3perpsalreadybooked08once,neverrepeat. Zero newdailydecisions/fills;preserve each owncash/q/desired/costs andfullNAVprefix,allnextdailyNov18_00:01,SMAfull69authorityunchanged,no newresearchVW adoption.')\n"+s[b:]
a=s.index("put(R/'implementation_plan.json'");b=s.index('print(json.dumps',a)
s=s[:a]+'''put(R/'implementation_plan.json',{'frozen_utc':now(),'hypothesis':'VW7/VW9 faster/slower completed sample logvol may adapt the carry budget to changing risk; oldVW8readonly. FixedR.0075/M4/entryriskV6cap.05625/fastROC/finiteEWM/native money. RepresentativeVW7/BTCH.03 setbeforeoutcomes.','axes':{'ETH_FUNDING_BUDGET_WINDOW':[7,8,9],'BTC_MAIN_ENTRY_H':[.03,.0325]},'new_ETH_budget_windows':[7,9],'readonly_ETH_budget_window':8,'new_configs':6,'representative':{'ETH_budget_window':7,'BTC_H':.03},'stages':['freeze specs and gates','synthetic budget/cause/equality checks','bind sources/data','reserve6','actual391d evaluateonce','independent fullpolicy/money/cost/fund/risk/NAV/fold audits','full exports','finish6','continue4originalaccounts afterindividualreserve','fullaccountchainaudit','appendonlyjournal','registry/readonlymonitorchecks','collect/seal/commit/pushmain','fullremoteevidenceverify','nativeunlock/postreleaseverify'],'no_subagents':True,'no_real_orders':True,'no_new_paper10_trades':True})
''' +s[b:]
write('prepare.py',s)
print('PASS budgetVW7/9 x readonlyBTCH.03/.0325, oldVW8, representativeVW7/H.03; no financial/account calculations')
