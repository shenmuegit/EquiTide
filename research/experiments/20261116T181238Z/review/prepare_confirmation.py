"""Synthetic exit/entry/confirmation boundaries; no market or account evaluations."""
import ast,copy,json,math,sys
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261116T161211Z';sys.path.insert(0,str(R));from common import *
import engine
prior=json.loads((R/'native_confirmation_prior_lookup.json').read_text())['matching_fixed_BTC_definitions'];assert not any(z['parameters'].get('entry_directional_confirmation_lookback_days')==5 and z['parameters'].get('entry_directional_confirmation_hurdle',0)==.0025 and z['parameters'].get('entry_volatility_ceiling')==.0275 and z['parameters'].get('return_hurdle')==.03 and z['parameters'].get('exit_buffer_fraction') in [.00375,.00625] and (z['result_available'] or z['status']=='reserved') for z in prior)
before=(P/'engine.py').read_text();after=(R/'engine.py').read_text();old="p['exit_buffer_fraction'] in [0.,.0025,.005,.01,.015]";new="p['exit_buffer_fraction'] in [0.,.0025,.00375,.005,.00625,.01,.015]";assert after==before.replace(old,new) and ast.dump(ast.parse(after.replace(new,old)))==ast.dump(ast.parse(before)) and sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py');cases=[]
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');base=rs['41de4309229b892489a07574af07a73ae93229a35c118558ed60362285e90c89']['spec'];h=F('.03')
for e in [F('.00375'),F('.005'),F('.00625')]:
 for actual in [-1,0,1]:
  for roc in [h-F('1e-12'),h,h+F('1e-12'),-h-F('1e-12'),-h,-h+F('1e-12'),-e-F('1e-12'),-e,-e+F('1e-12'),e-F('1e-12'),e,e+F('1e-12'),F(0)]:
   c=[F(100)]*60;i=50;c[i-30]=F(100);c[i-1]=100*(1+roc);expected=1 if roc>h else -1 if roc<-h else 1 if actual==1 and roc>-e else -1 if actual==-1 and roc<e else 0;got=engine.btc.target(c,i,29,.03,actual,float(e));assert got==(expected,str(roc)) and got==engine.btc.target(c[:i]+[F(10**12),F(1)],i,29,.03,actual,float(e));cases.append({'E':str(e),'fixed_H':'.03','actual':actual,'ROC':str(roc),'strict_exit_entry_priority_future_suffix':True})
 for sign in [-1,1]:
  values=[F(200+sign*j) for j in range(70)];i=50;logs=[math.log(float(values[j]/values[j-1])) for j in range(i-10,i)];mean=math.fsum(logs)/10;sigma=math.sqrt(math.fsum((x-mean)**2 for x in logs)/9);assert abs(sigma-engine.btc_entry_sigma(values,i,10))<1e-14
  for actual in [-1,0,1]:
   sp=copy.deepcopy(base);sp['parameters']['exit_buffer_fraction']=float(e);got=engine.base_decide(sp,{'asset':'BTC','closes':values},i,actual);assert got==engine.base_decide(sp,{'asset':'BTC','closes':values[:i]+[F(10**12),F(1)]},i,actual);roc=values[i-1]/values[i-30]-1;raw=1 if roc>h else -1 if roc<-h else 1 if actual==1 and roc>-e else -1 if actual==-1 and roc<e else 0;want=0 if raw and raw!=actual and sigma>.0275 else raw;recent=values[i-1]/values[i-6]-1;want=0 if want and want!=actual and want*recent<=F('.0025') else want;assert got[0]==want;cases.append({'E':str(e),'actual':actual,'trend':sign,'independent_full_policy_prefix':True})
for raw in [-1,0,1]:
 for actual in [-1,0,1]:
  for sigma in [.0275-1e-12,.0275,.0275+1e-12]:
   assert engine.entry_filter(raw,actual,sigma,.0275)==(0 if raw and raw!=actual and sigma>.0275 else raw);cases.append({'raw':raw,'actual':actual,'sigma':sigma,'vol_cap_boundary':True})
for d in [-1,1]:
 for actual in [-1,0,1]:
  for near in [F('.0025')-F('1e-12'),F('.0025'),F('.0025')+F('1e-12')]:
   assert engine.confirmation_filter(d,actual,d*near,F('.0025'))==(0 if d!=actual and near<=F('.0025') else d);cases.append({'direction':d,'actual':actual,'directional_ROC':str(near),'minimum_equality_blocks_new_or_reversed':True})
put(R/'exact_parameter_registry_screen.json',{'passed':True,'recorded_utc':now(),'new_exit_buffers':[.00375,.00625],'confirmation_days_fixed':5,'confirmation_min_return_fixed':.0025,'matching_fixed_BTC_definitions_read':len(prior),'exact_matching_actual_or_running_configs':0,'fixed':{'L':29,'H':.03,'volatility_cap':.0275,'V':10,'capital':3750,'notional':1000,'days':391},'no_market_or_account_calculations':True})
put(R/'prebinding_parameter_guard_verification.json',{'passed':True,'recorded_utc':now(),'old_source':rel(P/'engine.py'),'old_sha256':sha(P/'engine.py'),'new_source':rel(R/'engine.py'),'new_sha256':sha(R/'engine.py'),'intentional_policy_changes':['Only predeclaredexitE.00375/.00625;engineacceptanceallowlistextended,noformula/moneychange. FixedH.03,V10cap.0275 and5dayminimum.0025.','StrictEexits,Hentrypriority,vol equalitypasses,confirmation equalityblocksnew/reversed;existingqretainedinsideEbands.'],'policy_and_money_source_bytes_exactly_unchanged':False,'normalized_engine_AST_equal_except_exit_E_validation_allowlist':True,'money_core_bytes_unchanged':True,'simulate_and_money_core_bytes_unchanged':True,'synthetic_checks':cases,'before_first_reservation_or_market_calculation':True,'current_evaluation_failures':0,'current_preparation_failures':0})
checked=[]
for p in R.rglob('*.py'):
 tree=ast.parse(p.read_text());assert not[n for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(p);checked.append(rel(p))
put(R/'path_join_guard.json',{'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True});print('PASS',len(cases),'syntheticexit/entry/vol/minimum/futureprefixcases;onlyEallowlistextended;0market/accountvaluations')
