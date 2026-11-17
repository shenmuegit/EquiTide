"""Synthetic strict fast-ROC boundaries, carry budgets and future-prefix checks before reserve."""
import ast,copy,json,math,statistics,sys
from pathlib import Path
from decimal import Decimal as D
from fractions import Fraction as F
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261117T061921Z';sys.path.insert(0,str(R));from common import *
import engine
screen=json.loads((R/'exit_buffer_semantic_screen.json').read_text());assert screen['passed'];assert not any(z['E'] in [.00625,.00875] and (z['result_available'] or z['status']=='reserved') for z in screen['matching_fixed_ETH_definitions']);assert sha(P/'engine.py')==sha(R/'engine.py') and sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py');cases=[]
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');sp=rs['cb3c8bf2ba5106ebd505174ea724e4d767a6c738743e2418f527c39ea06863c1']['spec'];i=50;sn=50*24*HOUR;eps=F('0.00000001');funds=[{'settlement_ts':sn-age*HOUR,'available_ts':sn-(age-1)*HOUR,'realized_rate':D('.000001'),'source_index':j+1,'entry_interval_hours':D(8)} for j,age in enumerate([32,24,16,8])];future={'settlement_ts':sn+HOUR,'available_ts':sn+2*HOUR,'realized_rate':D(999),'source_index':9,'entry_interval_hours':D(8)}
for E in [.00625,.0075,.00875]:
 L=5;H=.02;h=F(str(H));e=F(str(E))
 spec=copy.deepcopy(sp);spec['parameters'].update(lookback_days=5,exit_buffer_fraction=E,return_hurdle=H,long_entry_return_hurdle=H,short_entry_return_hurdle=H,entry_funding_settlement_count=4,entry_funding_volatility_ratio=.0075,entry_funding_budget_volatility_window_days=8)
 for actual in [-1,0,1]:
  for roc in sorted({-h-eps,-h,-e-eps,-e,-e+eps,F(0),e-eps,e,e+eps,h,h+eps}):
   closes=[F(100)+F(j,10)+F((j*7)%11,100) for j in range(70)];closes[i-1-L]=F(100);closes[i-1]=F(100)*(1+roc);m={'asset':'ETH','closes':closes,'frame':{'available_ts':[sn]*(i*1440)},'signal_funds':funds};a=engine.base_decide(spec,m,i,actual);b=engine.base_decide(spec,{**m,'closes':closes[:i]+[F(10**12),F(1)],'signal_funds':funds+[future]},i,actual);base=-1 if roc>h else 1 if roc<-h else actual if actual==1 and roc<e or actual==-1 and roc>-e else 0
   assert a==b and F(a[1]['return_exact'])==roc and a[1]['ungated_desired']==base and a[1]['fast_lookback_days']==L and a[1]['funding_filter']['settlement_count']==4 and a[1]['funding_filter']['budget_ratio']=='0.0075';cases.append({'E':E,'H':H,'L':L,'actual':actual,'exact_fast_ROC':str(roc),'strict_H_E_boundaries_and_raw_desired_independent':True,'all_features_and_desired_unchanged_by_future_suffix':True})
 closes=[F(100)+F(j)+F((j*7)%11,10) for j in range(70)];xs=[math.log(float(closes[j]/closes[j-1])) for j in range(i-8,i)];mean=math.fsum(xs)/8;ind=math.sqrt(math.fsum((x-mean)**2 for x in xs)/7);sigma=engine.budget_sigma(closes,i,8);assert abs(sigma-ind)<1e-14;event=engine.median_funding(funds,sn,4);assert event['median_rate']==D('.000001') and len(event['events'])==4
 for hours in [D(4),D(8),D(12)]:
  ev=copy.deepcopy(event);ev['events'][0]['entry_interval_hours']=hours;cap=engine.carry_cap(sigma,.0075,ev);assert cap==min(D('.0002'),D('.0075')*D(str(sigma))*hours/D(24));cases.append({'E':E,'H':H,'L':L,'M':4,'R':.0075,'VW':8,'synthetic_known_interval_hours':str(hours),'unbiased_sigma_and_budget_formula_checked':True})
  for wanted in [-1,0,1]:
   for actual in [-1,0,1]:
    for delta in [D('-1e-12'),D(0),D('1e-12')]:
     ev['median_rate']=D(wanted)*(cap+delta) if wanted else D(0);out=engine.funding_filter(wanted,actual,ev,sn,cap)[0];expect=0 if wanted and wanted!=actual and cap+delta>cap else wanted;assert out==expect;cases.append({'E':E,'H':H,'L':L,'wanted':wanted,'actual':actual,'cap_delta':str(delta),'equality_passes_only_new_entry_or_reverse_gated':True})
 for actual in [-1,0,1]:
  for wanted in [-1,0,1]:assert engine.funding_filter(wanted,actual,None,sn,None)[0]==(0 if wanted and wanted!=actual else wanted)
 cases.append({'E':E,'H':H,'L':L,'missing_mature_records_blocks_only_new_entry':True})
put(R/'exact_parameter_registry_screen.json',{'passed':True,'recorded_utc':now(),'new_ETH_exit_E':[.00625,.00875],'old_E00075_readonly':True,'fixed_H':.02,'fixed_L':5,'fixed_M':4,'fixed_R':.0075,'fixed_VW':8,'readonly_BTC_H':[.03,.0325],'no_market_or_account_calculations':True});put(R/'prebinding_parameter_guard_verification.json',{'passed':True,'recorded_utc':now(),'old_source':rel(P/'engine.py'),'old_sha256':sha(P/'engine.py'),'new_source':rel(R/'engine.py'),'new_sha256':sha(R/'engine.py'),'intentional_policy_changes':['OnlypredeclaredETHexitE.00625/.00875atL5H.02M4/R.0075/VW8;engine/money bytesexact.','Strict rawcontrarian H/E boundaries, exact completed fastROC, full-feature future-prefix exclusion, budgetequality/missingrecord handling checked synthetically.'],'policy_and_money_source_bytes_exactly_unchanged':True,'full_engine_source_bytes_exactly_unchanged':True,'money_core_bytes_unchanged':True,'simulate_and_money_core_bytes_unchanged':True,'synthetic_checks':cases,'before_first_reservation_or_market_calculation':True,'current_evaluation_failures':0,'current_preparation_failures':len(json.loads((R/'read_failures.json').read_text())['facts'])})
checked=[]
for f in R.rglob('*.py'):
 t=ast.parse(f.read_text());assert not[z for z in ast.walk(t) if isinstance(z,ast.Subscript) and isinstance(z.value,ast.Name) and z.value.id in ['ROOT','R','P']],str(f);checked.append(rel(f))
put(R/'path_join_guard.json',{'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True});print('PASS',len(cases),'syntheticexitE/strictH_E/futuresuffix/carrybudgetchecks;0market/accountvaluations')
