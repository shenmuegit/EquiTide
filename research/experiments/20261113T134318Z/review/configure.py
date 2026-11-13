"""Prepare fixed BTC ROC lookback/hurdle sensitivity before reservation."""
from pathlib import Path
import ast
R=Path(__file__).resolve().parents[1];P=R.parent/'20261113T114346Z'
def put(n,s):(R/n).write_text(s)
def alter(n,pairs):
 s=(R/n).read_text()
 for a,b in pairs:
  assert a in s,(n,a);s=s.replace(a,b)
 put(n,s)
alter('review/setup.py',[("put(R/'funding08_nov13_preflight.json',fresh)","(R/'funding08_nov13_preflight.json').write_bytes((P/'funding08_nov13_preflight.json').read_bytes())"),("('SMA','2026-11-13T06:30:00Z','2026-11-13T08:30:00Z'),('candidate','2026-11-13T06:30:00Z','2026-11-13T08:30:00Z'),('l4h02','2026-11-13T08:10:00Z','2026-11-13T10:10:00Z'),('fewm','2026-11-13T08:10:00Z','2026-11-13T10:10:00Z')","('SMA','2026-11-13T08:30:00Z','2026-11-13T10:30:00Z'),('candidate','2026-11-13T08:30:00Z','2026-11-13T10:30:00Z'),('l4h02','2026-11-13T10:10:00Z','2026-11-13T12:10:00Z'),('fewm','2026-11-13T10:10:00Z','2026-11-13T12:10:00Z')"),('==[0,6,0,0]','==[0,0,0,0]'),("assert prior['public_fields_by_asset']==fresh['public_fields_by_asset']","assert fresh['public_fields_by_asset']=={'BTC':[],'ETH':[]} and prior['public_fields_by_asset']==json.loads((R/'funding08_nov13_preflight.json').read_text())['public_fields_by_asset']"),('Single books actual08fund once using own prior cash/q;L4/FEWM already booked08 and do not repeat.','All3 perp accounts already booked actual00/08once;fresh current-window public captures show0settlements;do not repeat old funding.'),('split0/6/0/0','split0/0/0/0')])
alter('engine.py',[("assert p['lookback_days']==29 and p['return_hurdle']==.03 and p['exit_buffer_fraction']==.01 and i-1-p['lookback_days']>=0","assert p['lookback_days'] in [25,27,29] and p['return_hurdle'] in [.025,.03,.035] and p['exit_buffer_fraction']==.01 and i-1-p['lookback_days']>=0"),("btc.target(m['closes'],i,29,.03,actual,.01)","btc.target(m['closes'],i,int(p['lookback_days']),float(p['return_hurdle']),actual,.01)")])
alter('audit.py',[("r=F(m['closes'][i-1])/F(m['closes'][i-30])-1;assert p['lookback_days']==29 and p['return_hurdle']==.03 and p['exit_buffer_fraction']==.01;h=F('.03');e=F('.01')","L=int(p['lookback_days']);h=F(str(p['return_hurdle']));r=F(m['closes'][i-1])/F(m['closes'][i-1-L])-1;assert L in [25,27,29] and h in [F('.025'),F('.03'),F('.035')] and p['exit_buffer_fraction']==.01;e=F('.01')"),("['TREND_S']","['BTC_L']"),("['TREND_K']","['BTC_H']")])
alter('run.py',[("['TREND_S']","['BTC_L']"),("['TREND_K']","['BTC_H']"),("'read_only_BTC_bank_reused':True","'read_only_ETH_bank_reused':True")])
alter('exports.py',[("['TREND_S']","['BTC_L']"),("['TREND_K']","['BTC_H']"),("xlabel='Strict EWM slope threshold',ylabel='Finite EWM window days'","xlabel='Strict BTC ROC entry hurdle',ylabel='BTC completed-day ROC lookback'"),("['0.625%','0.750%','0.875%']","['2.5%','3.0%','3.5%']"),("['12','16','20']","['25','27','29']"),('Predeclared ETH long-only EWM neighborhood + fixed BTC bank','Predeclared BTC ROC neighborhood + fixed ETH long-only bank'),("n.startswith('longonly389_parent')","n.startswith('btcrocbank389_parent')")])
# Current funding preflight is empty; retain the previous real08 capture as its
# own explicit historical source for full-chain no-repeat assertions.
alter('checks.py',[("for xs in fresh['public_fields_by_asset'].values() for z in xs};oldfunds=","for xs in rd(R/'funding08_nov13_preflight.json')['public_fields_by_asset'].values() for z in xs};oldfunds="),("assert win['candidate']['expected_funding_by_asset']==fresh['public_fields_by_asset'] and win['l4h02']['expected_funding_by_asset']==win['fewm']['expected_funding_by_asset']=={'BTC':[],'ETH':[]} and [win[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']]==[0,6,0,0]","assert fresh['public_fields_by_asset']=={'BTC':[],'ETH':[]} and all(win[a]['expected_funding_by_asset']==fresh['public_fields_by_asset'] for a in ['candidate','l4h02','fewm']) and [win[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']]==[0,0,0,0]"),('currentSingleonly','currentFunding0forAll')])
put('freeze.py','''"""Predeclare BTC lookback/hurdle grid; retain exact old center as read-only."""
import copy,itertools,json
from common import *
P=ROOT/'research/experiments/20261113T114346Z';old=json.loads((P/'plan.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');refs={}
def ref(fp):
 if fp in refs:return
 z=rs[fp];assert z['result_available'] and sha(ROOT/z['report'])==z['report_sha256'];c=next(x for x in json.loads((ROOT/z['report']).read_text())['configs'].values() if x['fingerprint']==fp);sp=z['spec'];scope='native' if sp['kind']=='strategy' else 'parent';d={k:c[k] for k in ['name','fingerprint','spec','archive','archive_sha256']};d.update(scope=scope,asset=sp['universe'][0].split('/')[0] if scope=='native' else 'COMBO',capital_usdt=sp['parameters']['initial_capital_usdt'],report=z['report'],report_sha256=z['report_sha256'],spec_sha256=sha(ROOT/c['spec']),status=z['status']);assert sha(ROOT/d['archive'])==d['archive_sha256'];refs[fp]=d
 if scope=='parent':
  d.update(source_fingerprints=[x['fingerprint'] for x in sp['components']],raw_weights=[x['weight'] for x in sp['components']])
  for x in sp['components']:ref(x['fingerprint'])
B=old['fixed_BTC_fingerprint'];E=old['control_fingerprints']['ETH_long_only'];center=old['control_fingerprints']['parent_long_only'];hold=old['benchmark_parent_fingerprint'];base=old['base_parent_fingerprint']
for fp in [B,E,center,hold,base]:ref(fp)
assert len(refs)==8
axes={'BTC_L':[25,27,29],'BTC_H':[.025,.03,.035]};rules={'signal':'BTC strictROC r=close[i-1]/close[i-1-L]-1;L25/27/29 xH.025/.03/.035. Desired+1 ifr>H,-1ifr<-H;insidebands keep actual long while r>-.01 or short while r<.01;else0. Entrybands take priority,strict equality is insideband. New/reverse-only V10 completed samplelogvol<=.04;blocked reverse closesold,no replacement. Same-directionq retained. ETH exact existing longonly C15000/N4000,L5H.02E.0075,finiteEWMS16D3K.0075,V6cap.05625,M4laggedfundmedian/VW8ratio.01/actualinterval,not recomputed.','execution':rs[B]['spec']['logic']['execution'],'costs':rs[B]['spec']['logic']['costs'],'allocation':'Actual independent whole BTC C3750/N1000 and fixed ETH C15000/N4000,total18750;raw[1,1],20/80capitalfractions only;no normalization/NAVscaling/transfers/rebalance/parentorders/crossmargin.','validation':'Fixed389days,2025-10-19T00:01Z to2026-11-12T00:01Z;33dayscontext,12x30+29tail,recent40day349,8x5,extension19day370,5+5+5+4;inheritstate,nofoldreset,terminalcosted;alloldgatesunchanged. Repeated development history,not untouchedfinal/independentfuture.'}
batch=[];grid=[];nativegrid=[];lookup=[];(R/'specs').mkdir(exist_ok=True)
for W,K in itertools.product(axes['BTC_L'],axes['BTC_H']):
 if (W,K)==(29,.03):
  nativegrid.append({**refs[B],'role':'benchmark','readonly':True,'N':1000,'prior_fingerprint':B,'W':W,'K':K});grid.append({**refs[center],'role':'benchmark','readonly':True,'NB':1000,'NE':4000,'W':W,'K':K});continue
 sp=copy.deepcopy(rs[B]['spec']);name=f'btcrocbank389_BTC_L{W}_H{int(K*10000)}bp';sp.update(name=name,logic=rules,validation_plan=rel(R/'plan.json'));q=sp['parameters'];q.update(lookback_days=W,return_hurdle=K)
 matches=[fp for fp,z in rs.items() if z.get('spec',{}).get('kind')=='strategy' and z['spec'].get('universe')==sp['universe'] and z['spec'].get('parameters')==q and z.get('result_available')];assert not matches,(W,K,matches)
 path=R/'specs'/(name+'.json');put(path,sp);fp=reg.fingerprint(sp);assert fp not in rs;nr=dict(scope='native',role='component',asset='BTC',N=1000,capital_usdt=3750,prior_fingerprint=B,readonly=False,name=name,fingerprint=fp,spec=rel(path),W=W,K=K);batch.append(nr);nativegrid.append(nr)
 sp=copy.deepcopy(rs[center]['spec']);name=f'btcrocbank389_parent_L{W}_H{int(K*10000)}bp';sp.update(name=name,logic=rules,components=[{'fingerprint':fp,'weight':1},{'fingerprint':E,'weight':1}],validation_plan=rel(R/'plan.json'));sp['parameters'].update(source_component_spec_sha256=[sha(path),refs[E]['spec_sha256']],BTC_existing_actual_bank_reused=False,ETH_existing_actual_bank_reused=True,BTC_new_native_quantity_and_impact_computed=True,ETH_new_native_quantity_and_impact_computed=False)
 path=R/'specs'/(name+'.json');put(path,sp);pf=reg.fingerprint(sp);assert pf not in rs;pr=dict(scope='parent',role='candidate',asset='COMBO',capital_usdt=18750,NB=1000,NE=4000,source_fingerprints=[fp,E],readonly=False,name=name,fingerprint=pf,spec=rel(path),W=W,K=K);grid.append(pr);lookup.append({'L':W,'H':K,'full_parameter_exact_result_matches':matches,'new_BTC_fingerprint':fp,'new_parent_fingerprint':pf})
batch += [g for g in grid if not g['readonly']];assert len(batch)==16 and len(grid)==len(nativegrid)==9
p={k:copy.deepcopy(old[k]) for k in ['limits','sources','data','time_boundaries','qualification_gates']};p.update(round=R.name,frozen_at_utc=now(),hypothesis='Prior long-onlyETH was flat for extension19 and all parent-window PnL came from fixed BTC. Test the BTC ROC lookback/hurdle neighborhood at actual unchanged bank size to detect isolated historical selection or recent dependence. No new ETH execution or rule adoption.',rules=rules,axes=axes,axis_semantics={'W':'BTC completed-day ROC lookback L','K':'strict symmetric BTC entry ROC hurdle H as fraction'},grid=grid,native_grid=nativegrid,benchmark_parent_fingerprint=hold,base_parent_fingerprint=base,fixed_BTC_fingerprint=B,fixed_ETH_fingerprint=E,representative_preset={'W':27,'K':.03},control_fingerprints={'BTC_base':B,'ETH_long_only':E,'parent_long_only':center,'parent_base':center},bank_capitals_usdt=[3750,15000],fixed_entry_notionals_usdt=[1000,4000],raw_component_weights=[1,1],expected_counts=dict(new_configs=16,new_native=8,new_parents=8,new_candidate_configs=8,new_benchmark_configs=0,new_source_components=8,new_cost_scenes=48,read_only_unique_results=8,grid_points=9,read_only_center_points=1),sensitivity={'axes':['BTC_L','BTC_H'],'index_radius':1,'local_positive3_min':.6,'local_recent_allcost6of8_min':.6,'include_exact_read_only_center':True,'old_center_canonical_status_and_report_unchanged':True},prior_report={'path':rel(P/'report.json'),'sha256':sha(P/'report.json')},primary_source_reads=[{'url':'https://github.com/binance/binance-public-data/blob/master/README.md','access_utc_date':now()[:10],'primary_documentation_browsed':True},{'url':'https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data','access_utc_date':now()[:10],'primary_documentation_browsed':True}])
p['limits'].append('BTC grid25/27/29 by2.5/3/3.5pct is preset before results;maxL29 safely fits33daycontext. Existing29/3pct BTC and matched parent read-only;8newBTC banks recompute actualq/LOT/cost/volumeimpact/funding/margin;fixedETHarchiveexactlyreused. All389days repeatedly observed,not independentfuture.')
put(R/'long_only_prior_lookup.json',{'passed':True,'recorded_before_reservation_utc':now(),'direction':'BTC ROC lookback/hurdle at fixed bank size','exact_parameter_search':lookup,'existing_anchor_BTC':B,'existing_anchor_parent':center,'old_anchor_recalculated':False,'semantic_parameter_and_canonical_checks_both_passed':True})
for n,z in [('plan.json',p),('spec.json',p),('batch.json',batch)]:put(R/n,z)
print('PASS16predeclarednewconfigs:8BTCROC+8parents;fixedETHreadonly;anchor29/3pctreadonly;0calculations')
''')
put('definitions.py','''"""Bind unchanged native accounting and only explicitly parameterized BTC branch."""
import ast,json
from common import *
P=ROOT/'research/experiments/20261113T114346Z';p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');fun=lambda f:{n.name:n for n in ast.parse(f.read_text()).body if isinstance(n,ast.FunctionDef)};old,new=fun(P/'engine.py'),fun(R/'engine.py');dump=lambda n:ast.dump(n,include_attributes=False)
assert (R/'core389.py').read_bytes()==(P/'core389.py').read_bytes() and all(dump(old[k])==dump(new[k]) for k in old if k!='base_decide')
assert [dump(n) for n in old['base_decide'].body[:2]]==[dump(n) for n in new['base_decide'].body[:2]] and [dump(n) for n in old['base_decide'].body[3:]]==[dump(n) for n in new['base_decide'].body[3:]]
assert len(batch)==16 and len(p['grid'])==len(p['native_grid'])==9
for row in batch:
 sp=json.loads((ROOT/row['spec']).read_text());assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs
 if row['scope']=='parent':assert [x['weight'] for x in sp['components']]==[1,1] and sp['parameters']['initial_capital_usdt']==18750 and sp['components'][1]['fingerprint']==p['fixed_ETH_fingerprint']
 else:
  q=sp['parameters'];prior=rs[row['prior_fingerprint']]['spec']['parameters'];assert sp['universe']==['BTC/USDT'] and all(q[k]==v for k,v in prior.items() if k not in ['lookback_days','return_hurdle']);assert q['lookback_days'] in [25,27,29] and q['return_hurdle'] in [.025,.03,.035] and q['initial_capital_usdt']==3750 and q['fixed_entry_notional_usdt']==1000 and q['warmup_days']>=q['lookback_days']+1
for fs in p['data']['assets'].values():
 for x in fs:assert sha(ROOT/x['path'])==x['sha256']
for fp,z in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
 for key in ['spec','report','archive']:assert sha(ROOT/z[key])==z[key+'_sha256']
assert json.loads((R/'parent_primitive_verification.json').read_text())['passed'];ab=json.loads((R/'original_accounts_binding.json').read_text());assert all(sha(ROOT/x)==h for x,h in ab['sources_sha256'].items())
excluded={'commands.py','publish.py','exports.py','checks.py','collect.py','finalize.py','journal.py'};source={rel(f):sha(f) for f in R.glob('*.py') if f.name not in excluded};immutable={rel(f):sha(f) for f in [R/'account_windows.json',R/'l4h02_resume_plan.json',R/'plan.json',R/'spec.json',R/'batch.json',R/'original_accounts_binding.json',ROOT/'checks/monitor_snapshot.py',ROOT/'research/monitor/snapshot.py']}
for row in batch:immutable[row['spec']]=sha(ROOT/row['spec'])
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_research_calculation_yet':True,'original_accounts_have_separate_preexecution_binding':True,'new_native_models':8,'new_parent_models':8,'changed_policy_scope':'BTC branch reads L/H parameters instead of original constants only;ETH branch and all other functions AST unchanged','simulate_and_native_money_AST_unchanged':True,'readonly_formatters_excluded':sorted(excluded)})
put(R/'definition_check.json',{'passed':True,'new_financial_configs':16,'exact_previously_unavailable_fingerprints':16,'no_equal_existing_spec_fingerprint':True,'only_BTC_LH_policy_parameterized':True,'ETH_policy_and_all_money_functions_AST_unchanged':True,'two_BTC_axes_and_readonly_anchor':True});print('PASS16newdefinitions;onlyBTCbranchL/Hparameterized;cash/q/trade/funding/ETHASTunchanged;boundbeforefirstresearchreserve')
''')
put('parent_units.py','''"""Strict BTC entry/persistence boundaries, suffix causality and dollar-bank/DD checks."""
from common import *
import engine
from fractions import Fraction as F
import numpy as np
n=0
for L in [25,27,29]:
 for H in [F('.025'),F('.03'),F('.035')]:
  for actual in [-1,0,1]:
   for roc in [-H-F(1,10**8),-H,F('-.01'),F(0),F('.01'),H,H+F(1,10**8)]:
    closes=[F(100)]*50;closes[39]=100*(1+roc);expected=1 if roc>H else -1 if roc<-H else 1 if actual==1 and roc>F('-.01') else -1 if actual==-1 and roc<F('.01') else 0
    wanted,r=engine.btc.target(closes,40,L,float(H),actual,.01);assert wanted==expected and F(r)==roc
    mutated=closes[:40]+[F(1),F(10**12),F(2),F(10**10)];assert engine.btc.target(mutated,40,L,float(H),actual,.01)==(wanted,r);n+=1
a=np.array([3750.,4500.,3000.]);b=np.array([15000.,14000.,16000.]);assert (a+b).tolist()==[18750.,18500.,19000.] and not np.array_equal(a+b,(a+b)/2)
v=np.array([100.,120.,90.,110.]);assert max(1-v/np.maximum.accumulate(v))==.25
put(R/'parent_primitive_verification.json',{'passed':True,'synthetic_only':True,'BTC_strict_entry_persistence_future_suffix_cases':n,'tests':['bothentryequalities','entrybandpriority','strictlongshortexitbuffer','futureclosemutationirrelevant','33daywarmupsupportsL29','wholebanknotnormalized','continuouscrossfoldDD25pct'],'new_strategy_or_account_calculations':0});print('PASS',n,'syntheticBTCboundary/suffixcases+wholebank/DD;0backtests')
''')
for f in R.glob('*.py'):ast.parse(f.read_text())
print('PASS configured BTC25/27/29 x2.5/3/3.5pct;no calculations')
