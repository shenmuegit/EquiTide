"""Exact unchanged-engine and independent entry-cap boundary/causal tests before reserve."""
import ast,copy,json,math,statistics,sys
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261116T120809Z';sys.path.insert(0,str(R));from common import *
import engine
prior=json.loads((R/'native_confirmation_prior_lookup.json').read_text())['matching_fixed_BTC_definitions'];assert not any(z['parameters'].get('entry_directional_confirmation_lookback_days')==5 and z['parameters'].get('entry_directional_confirmation_hurdle',0)==.0025 and z['parameters'].get('entry_volatility_ceiling') in [.02625,.02875] and (z['result_available'] or z['status']=='reserved') for z in prior)
assert sha(P/'engine.py')==sha(R/'engine.py') and sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py');cases=[]
for cap in [.02625,.0275,.02875]:
 for raw in [-1,0,1]:
  for actual in [-1,0,1]:
   for sigma in [cap-1e-12,cap,cap+1e-12]:
    expected=0 if raw and raw!=actual and sigma>cap else raw;assert engine.entry_filter(raw,actual,sigma,cap)==expected;cases.append({'cap':cap,'raw':raw,'actual':actual,'sigma':sigma,'vol_equality_passes_new_or_reversed_only':True})
for sign in [-1,1]:
 values=[F(200+sign*j) for j in range(70)];i=50;logs=[math.log(float(values[j]/values[j-1])) for j in range(i-10,i)];mean=math.fsum(logs)/10;expected_sigma=math.sqrt(math.fsum((x-mean)**2 for x in logs)/9);assert abs(expected_sigma-engine.btc_entry_sigma(values,i,10))<1e-14 and engine.btc_entry_sigma(values,i,10)==engine.btc_entry_sigma(values[:i]+[F(10**12),F(1)],i,10)
 for actual in [-1,0,1]:
  for cap in [.02625,.0275,.02875]:
   sp=copy.deepcopy(reg.read_records(ROOT/'research/automation/registry.jsonl')['41de4309229b892489a07574af07a73ae93229a35c118558ed60362285e90c89']['spec']);sp['parameters']['entry_volatility_ceiling']=cap;got=engine.base_decide(sp,{'asset':'BTC','closes':values},i,actual);assert got==engine.base_decide(sp,{'asset':'BTC','closes':values[:i]+[F(10**12),F(1)]},i,actual);r=values[i-1]/values[i-30]-1;raw=1 if r>F('.03') else -1 if r<-F('.03') else 1 if actual==1 and r>F('-.005') else -1 if actual==-1 and r<F('.005') else 0;wanted=0 if raw and raw!=actual and expected_sigma>cap else raw;recent=values[i-1]/values[i-6]-1;wanted=0 if wanted and wanted!=actual and wanted*recent<=F('.0025') else wanted;assert got[0]==wanted and F(got[1]['confirmation_hurdle_fraction'])==F('.0025');cases.append({'cap':cap,'trend':sign,'actual':actual,'independent_ROC_vol_minimum_and_causal_prefix_checked':True})
for d in [-1,1]:
 for actual in [-1,0,1]:
  for near in [F('.0025')-F('1e-12'),F('.0025'),F('.0025')+F('1e-12')]:
   got=engine.confirmation_filter(d,actual,d*near,F('.0025'));assert got==(0 if d!=actual and near<=F('.0025') else d);cases.append({'direction':d,'actual':actual,'direction_times_recent_ROC':str(near),'strict_minimum_equality_blocks_only_new_or_reversed':True})
put(R/'exact_parameter_registry_screen.json',{'passed':True,'recorded_utc':now(),'new_conditional_vol_caps':[.02625,.02875],'confirmation_days_fixed':5,'confirmation_min_return_fixed':.0025,'matching_fixed_BTC_definitions_read':len(prior),'exact_matching_actual_or_running_configs':0,'fixed':{'L':29,'H':.03,'E':.005,'V':10,'capital':3750,'notional':1000,'days':391},'no_market_or_account_calculations':True})
put(R/'prebinding_parameter_guard_verification.json',{'passed':True,'recorded_utc':now(),'old_source':rel(P/'engine.py'),'old_sha256':sha(P/'engine.py'),'new_source':rel(R/'engine.py'),'new_sha256':sha(R/'engine.py'),'intentional_policy_changes':['Only preregistered V10samplelogvol ceilings.02625/.02875 at fixed5day directionalROCminimum.0025;engine andmoney source bytesexactly unchanged','Vol equalitypasses;minimumROC equalityblocksnew/reversed;existing same-direction q andnormalexitsunchanged'],'policy_and_money_source_bytes_exactly_unchanged':True,'money_core_bytes_unchanged':True,'simulate_and_money_core_bytes_unchanged':True,'synthetic_checks':cases,'before_first_reservation_or_market_calculation':True,'current_evaluation_failures':0,'current_preparation_failures':0})
checked=[]
for p in R.rglob('*.py'):
 tree=ast.parse(p.read_text());assert not[n for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(p);checked.append(rel(p))
put(R/'path_join_guard.json',{'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True});print('PASS',len(cases),'synthetic strictvol/minimum/holding/futureprefix cases;enginebytesidentical;0market/accountvaluations')
