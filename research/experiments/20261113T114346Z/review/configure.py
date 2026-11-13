"""Prepare the explicit long-only neighborhood before financial reservation."""
import json, pathlib
R=pathlib.Path(__file__).resolve().parents[1];P=R.parent/'20261113T094314Z'
def put(name,s): (R/name).write_text(s)
def alter(name,pairs):
 s=(R/name).read_text()
 for a,b in pairs:
  assert a in s,(name,a);s=s.replace(a,b)
 put(name,s)
# Preserve the exact audited account kernels. The only adapter changes are this
# round's paths, broker PID and predeclared next windows.
put('review/setup.py','''"""Freeze actual next windows and source bindings before account calculation."""
import json,sys,subprocess
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
P=ROOT/'research/experiments/20261113T094314Z'
assert not (R/'code_binding_before_evaluation.json').exists()
(R/'bootstrap_receipt.json').write_bytes((R/'review/native_bootstrap.py_receipt.json').read_bytes())
receipts=[]
for cmd in [['git','rev-parse','HEAD'],['git','rev-parse','origin/main']]:
 a=now();z=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);receipts.append({'command':cmd,'cwd':str(ROOT),'started_utc':a,'finished_utc':now(),'exit_code':z.returncode,'stdout':z.stdout,'stderr':z.stderr});assert z.returncode==0
assert receipts[0]['stdout']==receipts[1]['stdout'];put(R/'remote_sync_receipts.json',receipts)
fresh=json.loads((R/'window_funding_preflight.json').read_text());assert fresh['passed'];put(R/'funding08_nov13_preflight.json',fresh)
for name in ['funding00_nov13_preflight.json','funding00_public_reuse.json']:(R/name).write_bytes((P/name).read_bytes())
ms=lambda t:int(datetime.fromisoformat(t.replace('Z','+00:00')).timestamp()*1000);w={}
for a,begin,end in [('SMA','2026-11-13T06:30:00Z','2026-11-13T08:30:00Z'),('candidate','2026-11-13T06:30:00Z','2026-11-13T08:30:00Z'),('l4h02','2026-11-13T08:10:00Z','2026-11-13T10:10:00Z'),('fewm','2026-11-13T08:10:00Z','2026-11-13T10:10:00Z')]:
 fields={asset:[] if a=='SMA' else [z for z in fresh['public_fields_by_asset'][asset] if ms(begin)<z['fundingTime']<=ms(end)] for asset in ['BTC','ETH']};times=sorted({z['fundingTime'] for xs in fields.values() for z in xs});w[a]={'start_utc':begin,'cutoff_utc':end,'expected_daily_events_utc':[],'expected_funding_utc':[datetime.fromtimestamp(t/1000,timezone.utc).isoformat().replace('+00:00','Z') for t in times],'expected_funding_by_asset':fields,'expected_funding_records':3*sum(map(len,fields.values())),'next_daily_decision_utc':'2026-11-14T00:01:00Z'}
assert [w[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']]==[0,6,0,0]
prior=json.loads((P/'funding08_nov13_preflight.json').read_text());assert prior['public_fields_by_asset']==fresh['public_fields_by_asset']
w.update(recorded_utc=now(),rules='Single books actual08fund once using own prior cash/q;L4/FEWM already booked08 and do not repeat. No daily decisions/fills/reset/forcedexit/research adoption;SMA full65 authority033939 unchanged.');put(R/'account_windows.json',w)
l=json.loads((P/'l4h02_resume_plan.json').read_text());point=ROOT/'research/automation/l4h02_forward_latest.json';l.update(frozen_at_utc=now(),recorded_utc=now(),round=R.name,previous_pointer=json.loads(point.read_text()),previous_pointer_sha256=sha(point),cutoff_utc=w['l4h02']['cutoff_utc'],cutoff_ns=ms(w['l4h02']['cutoff_utc'])*1000000,branch_lock_broker_pid=1308836,rules=w['rules']);put(R/'l4h02_resume_plan.json',l)
paths=[R/name for name in ['observe_l4h02.py','observe_fewm.py','observe_candidate.py','forward.py','forward_registry.py','audit_incremental.py','audit_l4h02.py','audit_fewm.py','audit_candidate.py','audit_forward.py']]
paths += [ROOT/x for x in l['source_sha256']]
put(R/'original_accounts_binding.json',{'recorded_utc':now(),'sources_sha256':{rel(x):sha(x) for x in paths},'frozen_before_current_account_calculation':True,'original_kernels_unchanged':True,'SMA_full65_authority':'research/experiments/20261113T033939Z/forward_inputs.json.gz'})
print('PASS frozen actual funding split0/6/0/0,no daily;sourcebinding before0calculations')
''')
# No premium data are consulted by this neighborhood; native accounting and the
# exact long-only base policy are reused byte-for-byte from the previous round.
put('engine.py',(P/'engine.py').read_text());put('core389.py',(P/'core389.py').read_text())
s=(R/'market.py').read_text();a=s.index(" source=json.loads((R/'premium_data_manifest.json')");b=s.index(' return ms,aligner.align(ms)',a);put('market.py',s[:a]+s[b:])
put('freeze.py','''"""Fixed price-only long-only EWM sensitivity, with the exact old center read-only."""
import copy,itertools,json
from common import *
P=ROOT/'research/experiments/20261113T094314Z';old=json.loads((P/'plan.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');refs={}
def ref(fp):
 if fp in refs:return
 z=rs[fp];assert z['result_available'] and sha(ROOT/z['report'])==z['report_sha256'];c=next(x for x in json.loads((ROOT/z['report']).read_text())['configs'].values() if x['fingerprint']==fp);sp=z['spec'];scope='native' if sp['kind']=='strategy' else 'parent';d={k:c[k] for k in ['name','fingerprint','spec','archive','archive_sha256']};d.update(scope=scope,asset=sp['universe'][0].split('/')[0] if scope=='native' else 'COMBO',capital_usdt=sp['parameters']['initial_capital_usdt'],report=z['report'],report_sha256=z['report_sha256'],spec_sha256=sha(ROOT/c['spec']),status=z['status']);assert sha(ROOT/d['archive'])==d['archive_sha256'];refs[fp]=d
 if scope=='parent':
  d.update(source_fingerprints=[x['fingerprint'] for x in sp['components']],raw_weights=[x['weight'] for x in sp['components']])
  for x in sp['components']:ref(x['fingerprint'])
B=old['fixed_BTC_fingerprint'];E=old['control_fingerprints']['ETH_long_only'];center=old['control_fingerprints']['parent_long_only'];hold=old['benchmark_parent_fingerprint'];base=old['base_parent_fingerprint']
for fp in [B,E,center,hold,base]:ref(fp)
assert len(refs)==8
rules=copy.deepcopy(rs[E]['spec']['logic']);axes={'TREND_S':[12,16,20],'TREND_K':[.00625,.0075,.00875]};batch=[];grid=[];nativegrid=[];lookup=[];(R/'specs').mkdir(exist_ok=True)
for W,K in itertools.product(axes['TREND_S'],axes['TREND_K']):
 if (W,K)==(16,.0075):
  nr={**refs[E],'role':'benchmark','readonly':True,'N':4000,'prior_fingerprint':E,'W':W,'K':K};pr={**refs[center],'role':'benchmark','readonly':True,'NB':1000,'NE':4000,'W':W,'K':K};nativegrid.append(nr);grid.append(pr);continue
 sp=copy.deepcopy(rs[E]['spec']);name=f'longonly389_ETH_S{W}_K{int(K*1000000)}ppm';sp.update(name=name,validation_plan=rel(R/'plan.json'));q=sp['parameters'];q.update(trend_lookback_days=W,trend_window_days=W,trend_decay_numerator=W-1,trend_decay_denominator=W+1,trend_slope_hurdle_fraction=K)
 matches=[fp for fp,z in rs.items() if z.get('spec',{}).get('kind')=='strategy' and z['spec'].get('universe')==sp['universe'] and z['spec'].get('parameters')==q and z.get('result_available')];assert not matches,(W,K,matches)
 path=R/'specs'/(name+'.json');put(path,sp);fp=reg.fingerprint(sp);assert fp not in rs;nr=dict(scope='native',role='component',asset='ETH',N=4000,capital_usdt=15000,prior_fingerprint=E,readonly=False,name=name,fingerprint=fp,spec=rel(path),W=W,K=K);batch.append(nr);nativegrid.append(nr)
 parent=copy.deepcopy(rs[center]['spec']);name=f'longonly389_parent_S{W}_K{int(K*1000000)}ppm';parent.update(name=name,components=[{'fingerprint':B,'weight':1},{'fingerprint':fp,'weight':1}],validation_plan=rel(R/'plan.json'));parent['parameters'].update(source_component_spec_sha256=[refs[B]['spec_sha256'],sha(path)],BTC_existing_actual_bank_reused=True,ETH_existing_actual_bank_reused=False,BTC_new_native_quantity_and_impact_computed=False,ETH_new_native_quantity_and_impact_computed=True)
 path=R/'specs'/(name+'.json');put(path,parent);pf=reg.fingerprint(parent);assert pf not in rs;pr=dict(scope='parent',role='candidate',asset='COMBO',capital_usdt=18750,NB=1000,NE=4000,source_fingerprints=[B,fp],readonly=False,name=name,fingerprint=pf,spec=rel(path),W=W,K=K);grid.append(pr);lookup.append({'W':W,'K':K,'parameter_exact_result_matches':matches,'new_ETH_fingerprint':fp,'new_parent_fingerprint':pf})
batch += [g for g in grid if not g['readonly']];assert len(batch)==16 and len(grid)==len(nativegrid)==9
p={k:copy.deepcopy(old[k]) for k in ['limits','sources','data','time_boundaries','qualification_gates']};p.update(round=R.name,frozen_at_utc=now(),hypothesis='Prior narrow premium positive path exactly equaled price-only long-only control. Test whether the long-only finite-EWM slope neighborhood is a broad historical plateau or an isolated reused-history optimum. No premium signal, extra source, OOS fitting or future-profit claim.',rules=rules,axes=axes,axis_semantics={'W':'ETH finite normalized EWM window in completed UTC days','K':'strict positive/negative EWM slope threshold as fraction; final negative desired is suppressed'},grid=grid,native_grid=nativegrid,benchmark_parent_fingerprint=hold,base_parent_fingerprint=base,fixed_BTC_fingerprint=B,read_only_references=refs,representative_preset={'W':16,'K':.00625},control_fingerprints={'ETH_long_only':E,'parent_long_only':center},bank_capitals_usdt=[3750,15000],fixed_entry_notionals_usdt=[1000,4000],raw_component_weights=[1,1],expected_counts=dict(new_configs=16,new_native=8,new_parents=8,new_candidate_configs=8,new_benchmark_configs=0,new_source_components=8,new_cost_scenes=48,read_only_unique_results=8,grid_points=9,read_only_center_points=1),sensitivity={'axes':['TREND_S','TREND_K'],'index_radius':1,'local_positive3_min':.6,'local_recent_allcost6of8_min':.6,'include_exact_read_only_center':True,'old_center_canonical_status_and_report_unchanged':True},prior_report={'path':rel(P/'report.json'),'sha256':sha(P/'report.json')},primary_source_reads=[{'url':'https://github.com/binance/binance-public-data/blob/master/README.md','access_utc_date':now()[:10],'primary_documentation_browsed':True},{'url':'https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data','access_utc_date':now()[:10],'primary_documentation_browsed':True}])
p['limits'].append('Eight new parameter settings plus a read-only old center on reused389day development history; no independent future data or funding/premium alpha attribution. Original accounts and frozen candidate plans unchanged.')
put(R/'long_only_prior_lookup.json',{'passed':True,'recorded_before_reservation_utc':now(),'exact_parameter_search':lookup,'existing_center_ETH':E,'existing_center_parent':center,'old_center_recalculated':False,'semantic_exact_parameter_and_canonical_checks_both_passed':True})
for n,v in [('plan.json',p),('spec.json',p),('batch.json',batch)]:put(R/n,v)
print('PASS16newconfigs,8ETH+8parents;9pointjointgridwithcenterread-only;0calculations')
''')
put('definitions.py','''"""Bind unchanged engine and exact new parameters before research reserve."""
import ast,json
from common import *
P=ROOT/'research/experiments/20261113T094314Z';p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl')
assert (R/'core389.py').read_bytes()==(P/'core389.py').read_bytes() and (R/'engine.py').read_bytes()==(P/'engine.py').read_bytes()
assert len(batch)==16 and len(p['grid'])==len(p['native_grid'])==9
for z in batch:
 sp=json.loads((ROOT/z['spec']).read_text());assert reg.fingerprint(sp)==z['fingerprint'] and z['fingerprint'] not in rs
 if z['scope']=='parent':assert [x['weight'] for x in sp['components']]==[1,1] and sp['parameters']['initial_capital_usdt']==18750
 else:
  q=sp['parameters'];prior=rs[z['prior_fingerprint']]['spec']['parameters'];changed={'trend_lookback_days','trend_window_days','trend_decay_numerator','trend_decay_denominator','trend_slope_hurdle_fraction'};assert all(q[k]==v for k,v in prior.items() if k not in changed);assert q['entry_direction_mode']=='long_only' and q['initial_capital_usdt']==15000 and q['fixed_entry_notional_usdt']==4000 and not any(k.startswith('entry_premium') for k in q)
for fs in p['data']['assets'].values():
 for x in fs:assert sha(ROOT/x['path'])==x['sha256']
for fp,z in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
 for key in ['spec','report','archive']:assert sha(ROOT/z[key])==z[key+'_sha256']
assert json.loads((R/'parent_primitive_verification.json').read_text())['passed']
ab=json.loads((R/'original_accounts_binding.json').read_text());assert all(sha(ROOT/x)==h for x,h in ab['sources_sha256'].items())
excluded={'commands.py','publish.py','exports.py','checks.py','collect.py','finalize.py','journal.py'};source={rel(f):sha(f) for f in R.glob('*.py') if f.name not in excluded};immutable={rel(f):sha(f) for f in [R/'account_windows.json',R/'l4h02_resume_plan.json',R/'plan.json',R/'spec.json',R/'batch.json',R/'original_accounts_binding.json',ROOT/'checks/monitor_snapshot.py',ROOT/'research/monitor/snapshot.py']}
for row in batch:immutable[row['spec']]=sha(ROOT/row['spec'])
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_research_calculation_yet':True,'original_accounts_have_separate_preexecution_binding':True,'new_native_models':8,'new_parent_models':8,'original_base_and_long_only_policy_unchanged':True,'simulate_and_native_money_AST_unchanged':True,'readonly_formatters_excluded':sorted(excluded)})
put(R/'definition_check.json',{'passed':True,'new_financial_configs':16,'exact_previously_unavailable_fingerprints':16,'no_equal_existing_spec_fingerprint':True,'engine_and_accounting_bytes_unchanged':True,'two_EWM_axes_and_readonly_center':True});print('PASS16newdefinitions;exactengineunchanged;boundbeforefirstresearchreserve')
''')
# Joint-neighborhood implementation includes the old center without another
# reserve, policy run, trade, or finish call.
alter('run.py',[("['PREM_W']","['TREND_S']"),("['PREM_CAP']","['TREND_K']"),('len(batch)==20','len(batch)==16'),("full={c['fingerprint']:c for c in configs.values()}","full={c['fingerprint']:c for c in configs.values()}\n for rows in [p['grid'],p['native_grid']]:\n  for g in rows:\n   if g['readonly']:\n    d=p['read_only_references'][g['fingerprint']];c=copy.deepcopy(next(c for c in json.loads((ROOT/d['report']).read_text())['configs'].values() if c['fingerprint']==g['fingerprint']));c.update(W=g['W'],K=g['K'],readonly=True);full[g['fingerprint']]=c"),("'new_native_models':10,'new_parent_models':10","'new_native_models':8,'new_parent_models':8")])
# A separate primitive regression checks the exact side wrapper using the actual
# unchanged base function; synthetic data are explicitly not market results.
put('parent_units.py','''"""Strict slope, side suppression and full-bank/DD primitive regressions."""
from common import *
import engine
from fractions import Fraction as F
import numpy as np
for k in [F('.00625'),F('.0075'),F('.00875')]:
 assert engine.slope_gate(k,k)==engine.slope_gate(-k,k)==0
 assert engine.slope_gate(k+F(1,10**9),k)==1 and engine.slope_gate(-k-F(1,10**9),k)==-1
old=engine.base_decide
try:
 for desired,actual in [(-1,0),(-1,1),(0,1),(1,0),(1,1)]:
  engine.base_decide=lambda sp,m,i,a,d=desired:(d,{'kind':'synthetic_base'})
  result,audit=engine.decide({'parameters':{'entry_direction_mode':'long_only'}},{},0,actual);assert result==max(desired,0) and audit['raw_desired_before_side_filter']==desired
finally:engine.base_decide=old
a=np.array([3750.,4500.,3000.]);b=np.array([15000.,14000.,16000.]);assert (a+b).tolist()==[18750.,18500.,19000.] and not np.array_equal(a+b,(a+b)/2)
v=np.array([100.,120.,90.,110.]);assert max(1-v/np.maximum.accumulate(v))==.25
put(R/'parent_primitive_verification.json',{'passed':True,'synthetic_only':True,'strict_threshold_cases':12,'side_wrapper_cases':5,'tests':['strictpositiveandnegativeequalities','longonlysuppressesnegative','normalexit','sameqtarget','wholebanknotnormalized','continuouscrossfoldDD25pct'],'new_strategy_or_account_calculations':0});print('PASS slope/side/fullbank/DDprimitive regressions;0backtests')
''')
# Independent saved-result auditor preserves all original arithmetic checks.
alter('audit.py',[("['PREM_W']","['TREND_S']"),("['PREM_CAP']","['TREND_K']"),("full={c['fingerprint']:c for c in report['configs'].values()};recent_ok=","full={c['fingerprint']:c for c in report['configs'].values()}\nfor rows in [plan['grid'],plan['native_grid']]:\n for g in rows:\n  if g['readonly']:\n   d=plan['read_only_references'][g['fingerprint']];c=copy.deepcopy(next(c for c in json.loads((ROOT/d['report']).read_text())['configs'].values() if c['fingerprint']==g['fingerprint']));c.update(W=g['W'],K=g['K'],readonly=True);full[g['fingerprint']]=c\nrecent_ok="),('for c in full.values():','for c in report[\'configs\'].values():'),('(30,30,11670,15)','(24,24,9336,15)')])
put('audit.py','\n'.join(x.rstrip() for x in (R/'audit.py').read_text().splitlines())+'\n')
# Account-specific current-window expected counts and complete-chain checks.
alter('checks.py', [('==20','==16'),('(30,30,11670)','(24,24,9336)'),("'financial_IDs':20,'new_native_models':10,'passive_parents':10,'cost_curves':60","'financial_IDs':16,'new_native_models':8,'passive_parents':8,'cost_curves':48"),('==32','==28'),("+64","+56"),("+32","+28"),("'financial_IDs':20,'observation_IDs':12,'finished_IDs':32,'append_only_events':64","'financial_IDs':16,'observation_IDs':12,'finished_IDs':28,'append_only_events':56"),('len(old)+20','len(old)+16'),("'new_actual_financial_configs':20,'new_displayed_financial_configs':20 if success else 0,'pending_current_financial_configurations':0 if success else 20","'new_actual_financial_configs':16,'new_displayed_financial_configs':16 if success else 0,'pending_current_financial_configurations':0 if success else 16"),("(0 if stem=='candidate' else 6)",'6'),("(max(fund00) if stem=='candidate' else max(fund08))",'max(fund08)'),("assert win['candidate']['expected_funding_by_asset']=={'BTC':[],'ETH':[]} and win['l4h02']['expected_funding_by_asset']==win['fewm']['expected_funding_by_asset']==fresh['public_fields_by_asset'] and [win[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']]==[0,0,6,6]","assert win['candidate']['expected_funding_by_asset']==fresh['public_fields_by_asset'] and win['l4h02']['expected_funding_by_asset']==win['fewm']['expected_funding_by_asset']=={'BTC':[],'ETH':[]} and [win[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']]==[0,6,0,0]")])
alter('journal.py',[('==32','==28'),('==64','==56'),('+32','+28'),('+64','+56'),("'current_round_events':64,'current_round_finished_IDs':32","'current_round_events':56,'current_round_finished_IDs':28"),("'events':64,'IDs':32","'events':56,'IDs':28")])
alter('forward_registry.py',[('Next daily event2026-11-13UTC00:01','Next daily event2026-11-14UTC00:01')])
alter('forward.py',[('already completed Nov12 daily decision','already completed Nov13 daily decision')])
# Exports include all nine grid points, marking the center as read-only; only
# the sixteen new actual financial results enter the registry and monitor.
alter('exports.py',[("['PREM_W']","['TREND_S']"),("['PREM_CAP']","['TREND_K']"),("'new_configs':20","'new_configs':16"),("cs=[c for c in r['configs'].values() if c['scope']==scope and c['role']!='benchmark']","cs=list((r['all_current_grid'] if scope=='parent' else r['all_current_native_grid']).values())"),("cs=[c for c in r['configs'].values() if c['scope']=='parent' and c['role']=='candidate']","cs=list(r['all_current_grid'].values())"),("xlabel='Maximum directional premium',ylabel='Completed UTC day window'","xlabel='Strict EWM slope threshold',ylabel='Finite EWM window days'"),("['4 bp','8 bp','12 bp']","['0.625%','0.750%','0.875%']"),("['1','3','5']","['12','16','20']"),('Predeclared ETH premium filter + fixed BTC bank','Predeclared ETH long-only EWM neighborhood + fixed BTC bank'),("n.startswith('premium389_parent')","n.startswith('longonly389_parent')")])
# Heatmap center sensitivity is an explicitly read-only grid diagnostic. Its
# previously registered benchmark status and report are not changed.
s=(R/'exports.py').read_text();needle="fig,axs=plt.subplots";i=s.index(needle);s=s[:i]+"for g,c in r['all_current_grid'].items():\n if c.get('readonly'):\n  ns=[z for z in r['all_current_grid'].values() if abs(p['axes']['TREND_S'].index(z['W'])-p['axes']['TREND_S'].index(c['W']))<=1 and abs(p['axes']['TREND_K'].index(z['K'])-p['axes']['TREND_K'].index(c['K']))<=1];c['sensitivity']=dict(c['sensitivity'],local_recent_allcost_qualifying_fraction=sum(all(z['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in z['recent40']['folds'])>=6 for z in a['scenes'].values()) for a in ns)/len(ns))\n"+s[i:];put('exports.py',s)
print('PASS configured explicit16-definition long-only neighborhood and original account windows; no calculations')
