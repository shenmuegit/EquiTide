"""Prepare only this round's BTC lookback/exit interaction and original account windows."""
import ast,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2]
def alter(n,pairs):
 p=R/n;s=p.read_text()
 for a,b in pairs:
  assert a in s,(n,a);s=s.replace(a,b)
 p.write_text(s)
alter('review/preflight.py', [('2026-11-13T12:30:00Z','2026-11-13T14:30:00Z'),('2026-11-13T16:10:00Z','2026-11-13T18:10:00Z')])
alter('review/setup.py', [("put(R/'funding16_nov13_preflight.json',fresh)","(R/'funding16_nov13_preflight.json').write_bytes((P/'funding16_nov13_preflight.json').read_bytes())"),('2026-11-13T14:30:00Z','END_SINGLE'),('2026-11-13T12:30:00Z','2026-11-13T14:30:00Z'),('END_SINGLE','2026-11-13T16:30:00Z'),('2026-11-13T16:10:00Z','END_L4'),('2026-11-13T14:10:00Z','2026-11-13T16:10:00Z'),('END_L4','2026-11-13T18:10:00Z'),('==[0,0,6,6]','==[0,6,0,0]'),('All3 perp accounts already booked actual00/08once. L4/FEWM now cover actual16 settlement and book own cash/q once;single ends14:30 and must not book16early. Fresh actual timestamps determine records;no schedule assumption.','All3 perp accounts already booked actual00/08once. Single now covers actual16 and books own cash/q once;L4/FEWM alreadybooked16 and must not repeat. Fresh actual timestamps determine records;no schedule assumption.'),('split0/0/6/6','split0/6/0/0')])
for name in ['engine.py','audit.py']:alter(name,[('[29,31,32]','[27,29,31]')])
for name in ['audit.py','run.py','exports.py']:
 alter(name,[("['BTC_E']","['AXIS_L_TEMP']"),("['BTC_H']","['BTC_E']"),("['AXIS_L_TEMP']","['BTC_L']")])
alter('audit.py',[('(18,18,7002,21)','(12,12,4668,27)')])
alter('definitions.py',[('len(batch)==12','len(batch)==8'),("if k not in ['return_hurdle','exit_buffer_fraction']","if k not in ['lookback_days','exit_buffer_fraction']"),("q['lookback_days']==29","q['lookback_days'] in [27,31]"),("q['return_hurdle'] in [.025,.03,.035]","q['return_hurdle']==.03"),("'new_native_models':6,'new_parent_models':6","'new_native_models':4,'new_parent_models':4"),("'new_financial_configs':12","'new_financial_configs':8"),("'exact_previously_unavailable_fingerprints':12","'exact_previously_unavailable_fingerprints':8"),('OnlyBTC exitbuffer E is read from declared parameter;L29 fixed,H/E jointgrid;ETH and all accounting formulas retained;threeE1percentcellsreused','OnlyBTC declaredL27/29/31 and E0.5/1/1.5percent;H3percent fixed;ETH and money functions unchanged;5oldgridcells reused')])
alter('exports.py',[("xlabel='Strict BTC ROC entry hurdle',ylabel='BTC persistence exit buffer'","xlabel='BTC persistence exit buffer',ylabel='BTC completed-day ROC lookback'"),("['0.5%','1.0%','1.5%']","['27','29','31']"),('Predeclared BTC exit-buffer neighborhood','Predeclared BTC lookback/exit interaction'),("n.startswith('btcexit389_parent')","n.startswith('btclexit389_parent')")])
alter('checks.py',[('len(batch)==len(r[\'configs\'])==12',"len(batch)==len(r['configs'])==8"),('(18,18,7002)','(12,12,4668)'),('len(res)==len(fin)==12','len(res)==len(fin)==8'),("'financial_IDs':12","'financial_IDs':8"),("'new_native_models':6,'passive_parents':6,'cost_curves':36","'new_native_models':4,'passive_parents':4,'cost_curves':24"),("'all36scenes_and_folds_audited'","'all24scenes_and_folds_audited'"),("'read_only_native_curves_audited':21","'read_only_native_curves_audited':27"),('PASS12actualconfigs/36scenes','PASS8actualconfigs/24scenes'),("assert all(len(fundcounts[t])==(0 if stem=='candidate' else 6) for t in fund16);assert last==(max(fund08) if stem=='candidate' else max(fund16))","assert all(len(fundcounts[t])==6 for t in fund16);assert last==max(fund16)"),("assert win['candidate']['expected_funding_by_asset']=={'BTC':[],'ETH':[]} and win['l4h02']['expected_funding_by_asset']==win['fewm']['expected_funding_by_asset']==fresh['public_fields_by_asset']","assert win['candidate']['expected_funding_by_asset']==fresh['public_fields_by_asset'] and win['l4h02']['expected_funding_by_asset']==win['fewm']['expected_funding_by_asset']=={'BTC':[],'ETH':[]}"),('==[0,0,6,6]','==[0,6,0,0]'),('currentL4FEWM16onceSingleBefore16','currentSingle16onceL4FEWMnotRepeated'),('len(bs)==24','len(bs)==20'),("ctx['registry_events']+48","ctx['registry_events']+40"),("ctx['registry_ids']+24","ctx['registry_ids']+20"),("'finished_IDs':24,'append_only_events':48","'finished_IDs':20,'append_only_events':40"),('PASS24finishedIDs/48','PASS20finishedIDs/40'),('len(data)==len(old)+12','len(data)==len(old)+8'),("'new_actual_financial_configs':12,'new_displayed_financial_configs':12","'new_actual_financial_configs':8,'new_displayed_financial_configs':8"),('0 if success else 12','0 if success else 8'),('current12financialconfigs','current8financialconfigs')])
# Boundary and suffix causality checks use synthetic prices only, not a new financial evaluation.
(R/'parent_units.py').write_text('''from common import *
import engine
from fractions import Fraction as F
import numpy as np
n=0
for L in [27,29,31]:
 for E in [F('.005'),F('.01'),F('.015')]:
  H=F('.03')
  for actual in [-1,0,1]:
   for roc in [-H-F(1,10**8),-H,-E,F(0),E,H,H+F(1,10**8)]:
    closes=[F(100)]*50;closes[39]=100*(1+roc);wanted=1 if roc>H else -1 if roc<-H else 1 if actual==1 and roc>-E else -1 if actual==-1 and roc<E else 0;out,r=engine.btc.target(closes,40,L,float(H),actual,float(E));assert out==wanted and F(r)==roc
    future=closes[:40]+[F(1),F(10**12),F(2)];assert engine.btc.target(future,40,L,float(H),actual,float(E))==(out,r);n+=1
a=np.array([3750.,4500.,3000.]);b=np.array([15000.,14000.,16000.]);assert (a+b).tolist()==[18750.,18500.,19000.] and not np.array_equal(a+b,(a+b)/2)
v=np.array([100.,120.,90.,110.]);assert max(1-v/np.maximum.accumulate(v))==.25
put(R/'parent_primitive_verification.json',{'passed':True,'synthetic_only':True,'BTC_hysteresis_boundary_future_suffix_cases':n,'tests':['bothentryequalities','entrybandpriority','strictlongshortexitbufferE','futureclosemutationirrelevant','wholebanknotnormalized','continuouscrossfoldDD25pct'],'new_strategy_or_account_calculations':0});print('PASS',n,'syntheticBTClookbackexitboundary/futurecases;0backtests')
''')
startup={'round':R.name,'trigger_utc':'2026-11-13T19:47:21.382Z','base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'branch_lock_broker_pid':1451527,'branch_lock_session':77619,'branch_lock_native_start_chunk':'e992d8','root_native_verification_chunk':'19aa90','initial_fetch_native_start_chunk':'de8a1f','initial_fetch_native_session':80068,'initial_fetch_native_completion_chunk':'4b1df8','initial_sync_no_merge_required':True,'only_preexisting_untracked':'data/normalized','primary_docs_browsed':['https://github.com/binance/binance-public-data/blob/master/README.md'],'official_funding_old_URL_read_error':'web open Internal Error; catalog URL to be read before freeze'}
(R/'startup.json').write_text(json.dumps(startup,indent=2)+'\n')
for f in R.rglob('*.py'):ast.parse(f.read_text())
print('PASS configured4newBTCand4parents;5oldgridcells;originalsingle16settlementowncashflow;no calculations')
