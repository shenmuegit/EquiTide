"""Synthetic median-count, maturity, equality and future-prefix checks before reserve."""
import ast,copy,json,math,statistics,sys
from pathlib import Path
from decimal import Decimal as D
from fractions import Fraction as F
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261117T001412Z';sys.path.insert(0,str(R));from common import *
import engine
prior=json.loads((R/'tight_budget_median_prior_lookup.json').read_text());assert prior['passed'];rows=prior['matching_fixed_ETH_definitions'];assert not any(z['M'] in [2,3] and z['R']==.0075 and (z['result_available'] or z['status']=='reserved') for z in rows)
assert sha(P/'engine.py')==sha(R/'engine.py') and sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py');cases=[];rs=reg.read_records(ROOT/'research/automation/registry.jsonl');sp=rs['cb3c8bf2ba5106ebd505174ea724e4d767a6c738743e2418f527c39ea06863c1']['spec'];closes=[F(100)+F(j)+F((j*7)%11,10) for j in range(70)];i=50;sn=50*24*HOUR
funds=[{'settlement_ts':sn-age*HOUR,'available_ts':sn-(age-1)*HOUR,'realized_rate':rate,'source_index':j+1,'entry_interval_hours':D(8)} for j,(age,rate) in enumerate(zip([32,24,16,8],map(D,['.000011','-.000017','.000023','.000031'])))];future={'settlement_ts':sn+HOUR,'available_ts':sn+2*HOUR,'realized_rate':D(999),'source_index':9,'entry_interval_hours':D(8)}
for count in [2,3,4]:
 vw=8;ratio=.0075;xs=[math.log(float(closes[j]/closes[j-1])) for j in range(i-vw,i)];mean=math.fsum(xs)/vw;independent=math.sqrt(math.fsum((x-mean)**2 for x in xs)/(vw-1));sigma=engine.budget_sigma(closes,i,vw);assert abs(sigma-independent)<1e-14 and sigma==engine.budget_sigma(closes[:i]+[F(10**12),F(1)],i,vw)
 event=engine.median_funding(funds,sn,count);assert event and event['count']==count;selected=sorted(funds,key=lambda e:e['settlement_ts'],reverse=True)[:count];rates=sorted(F(e['realized_rate']) for e in selected);median=rates[count//2] if count%2 else (rates[count//2-1]+rates[count//2])/2;assert F(event['median_rate'])==median and event['events']==selected;cases.append({'M':count,'independent_odd_even_median_latestM_selection':True})
 boundary=[{**funds[j],'settlement_ts':sn-age*HOUR,'available_ts':sn-(age-1)*HOUR} for j,age in enumerate([36,16,8,1])];extras=[{**future,'settlement_ts':sn-HOUR//2,'available_ts':sn-HOUR//2},{**future,'settlement_ts':sn-36*HOUR-1,'available_ts':sn-35*HOUR},{**future,'settlement_ts':sn-2*HOUR,'available_ts':sn+1}];b=engine.median_funding(boundary,sn,count);assert b==engine.median_funding(boundary+extras+[future],sn,count);cases.append({'M':count,'inclusive_1h_36h_bounds_unavailable_future_and_outside_excluded':True})
 assert engine.median_funding(funds[:count-1],sn,count) is None
 for actual in [-1,0,1]:
  for wanted in [-1,0,1]:
   out,a=engine.funding_filter(wanted,actual,None,sn,None);assert out==(0 if wanted and wanted!=actual else wanted);cases.append({'M':count,'wanted':wanted,'actual':actual,'missing_required_records_blocks_only_new_or_reversed':True})
 for hours in [D(4),D(8),D(12)]:
  e=copy.deepcopy(event);e['events'][0]['entry_interval_hours']=hours;cap=engine.carry_cap(sigma,ratio,e);assert cap==min(D('.0002'),D(str(ratio))*D(str(sigma))*hours/D(24));cases.append({'M':count,'R':ratio,'VW':vw,'synthetic_past_interval_hours':str(hours),'unbiased_sigma_and_budget_prefix':True})
  for wanted in [-1,0,1]:
   for actual in [-1,0,1]:
    for delta in [D('-1e-12'),D(0),D('1e-12')]:
     e['median_rate']=D(wanted)*(cap+delta) if wanted else D(0);out=engine.funding_filter(wanted,actual,e,sn,cap)[0];expected=0 if wanted and wanted!=actual and cap+delta>cap else wanted;assert out==expected;cases.append({'M':count,'R':ratio,'VW':vw,'interval_hours':str(hours),'wanted':wanted,'actual':actual,'budget_delta':str(delta),'equality_passes_newentry_only':True})
 for actual in [-1,0,1]:
  spec=copy.deepcopy(sp);spec['parameters'].update(entry_funding_settlement_count=count,entry_funding_budget_volatility_window_days=8,entry_funding_volatility_ratio=.0075);m={'asset':'ETH','closes':closes,'frame':{'available_ts':[sn]*(i*1440)},'signal_funds':funds};a=engine.base_decide(spec,m,i,actual);b=engine.base_decide(spec,{**m,'closes':closes[:i]+[F(10**12),F(1)],'signal_funds':funds+[future]},i,actual);assert a==b and a[1]['funding_filter']['budget_volatility_window_days']==8 and a[1]['funding_filter']['settlement_count']==count and a[1]['funding_filter']['budget_ratio']=='0.0075';cases.append({'M':count,'actual':actual,'full_ETH_policy_unchanged_by_future_closes_or_funding':True})
put(R/'exact_parameter_registry_screen.json',{'passed':True,'recorded_utc':now(),'new_ETH_funding_M':[2,3],'fixed_R':.0075,'fixed_ETH_VW':8,'old_M4_tight_center':True,'already_tested_looser_M2_M3_not_recomputed':True,'readonly_BTC_H':[.03,.0325],'no_market_or_account_calculations':True})
put(R/'prebinding_parameter_guard_verification.json',{'passed':True,'recorded_utc':now(),'old_source':rel(P/'engine.py'),'old_sha256':sha(P/'engine.py'),'new_source':rel(R/'engine.py'),'new_sha256':sha(R/'engine.py'),'intentional_policy_changes':['Only predeclaredM2/M3atfixedR.0075/VW8;engine/money sourcebytesexact. Fixedrisk/trend/size.','Odd/even/latestMmedian,maturity1to36hinclusive,availability,missingrecords,budgetequality/heldq andfutureprefix verified synthetically.'],'policy_and_money_source_bytes_exactly_unchanged':True,'full_engine_source_bytes_exactly_unchanged':True,'money_core_bytes_unchanged':True,'simulate_and_money_core_bytes_unchanged':True,'synthetic_checks':cases,'before_first_reservation_or_market_calculation':True,'current_evaluation_failures':0,'current_preparation_failures':0})
checked=[]
for f in R.rglob('*.py'):
 t=ast.parse(f.read_text());assert not[z for z in ast.walk(t) if isinstance(z,ast.Subscript) and isinstance(z.value,ast.Name) and z.value.id in ['ROOT','R','P']],str(f);checked.append(rel(f))
put(R/'path_join_guard.json',{'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True});print('PASS',len(cases),'syntheticM/odd-evenmedian/maturity/equality/missing/futuresuffixchecks;0market/accountvaluations')
