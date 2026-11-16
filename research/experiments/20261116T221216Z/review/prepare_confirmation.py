"""Synthetic completed-window funding budgets and asset-axis checks before reserve."""
import ast,copy,json,math,statistics,sys
from pathlib import Path
from decimal import Decimal as D
from fractions import Fraction as F
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261116T201210Z';sys.path.insert(0,str(R));from common import *
import engine
prior=json.loads((R/'native_budget_prior_lookup.json').read_text())['matching_fixed_ETH_definitions'];assert not any(z['parameters'].get('entry_funding_volatility_ratio') in [.009375,.010625] and (z['result_available'] or z['status']=='reserved') for z in prior)
assert sha(P/'engine.py')==sha(R/'engine.py') and sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py');cases=[]
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');sp=rs['eaa75ec6bbd2cf0611b7e53931b6ada73b31f1d33f8186a9c885a3e544bf1270']['spec'];closes=[F(100)+F(j)+F((j*7)%11,10) for j in range(70)];i=50;sn=50*24*HOUR
funds=[{'settlement_ts':sn-age*HOUR,'available_ts':sn-(age-1)*HOUR,'realized_rate':D('.00000001'),'source_index':j+1,'entry_interval_hours':D(8)} for j,age in enumerate([32,24,16,8])];future={'settlement_ts':sn+HOUR,'available_ts':sn+2*HOUR,'realized_rate':D(999),'source_index':9,'entry_interval_hours':D(8)}
for ratio in [.009375,.01,.010625]:
 vw=8
 xs=[math.log(float(closes[j]/closes[j-1])) for j in range(i-vw,i)];mean=math.fsum(xs)/vw;independent=math.sqrt(math.fsum((x-mean)**2 for x in xs)/(vw-1));sigma=engine.budget_sigma(closes,i,vw);assert abs(sigma-independent)<1e-14 and sigma==engine.budget_sigma(closes[:i]+[F(10**12),F(1)],i,vw)
 event=engine.median_funding(funds,sn,4);assert event and event['count']==4
 for hours in [D(4),D(8),D(12)]:
  e=copy.deepcopy(event);e['events'][0]['entry_interval_hours']=hours;cap=engine.carry_cap(sigma,ratio,e);assert cap==min(D('.0002'),D(str(ratio))*D(str(sigma))*hours/D(24));cases.append({'R':ratio,'VW':vw,'actual_past_interval_hours':str(hours),'unbiased_sigma_and_budget_prefix':True})
  for wanted in [-1,0,1]:
   for actual in [-1,0,1]:
    for delta in [D('-1e-12'),D(0),D('1e-12')]:
     e['median_rate']=D(wanted)*(cap+delta) if wanted else D(0);out=engine.funding_filter(wanted,actual,e,sn,cap)[0];expected=0 if wanted and wanted!=actual and cap+delta>cap else wanted;assert out==expected;cases.append({'R':ratio,'VW':vw,'interval_hours':str(hours),'wanted':wanted,'actual':actual,'budget_delta':str(delta),'equality_passes_newentry_only':True})
 for actual in [-1,0,1]:
  spec=copy.deepcopy(sp);spec['parameters']['entry_funding_budget_volatility_window_days']=8;spec['parameters']['entry_funding_volatility_ratio']=ratio;m={'asset':'ETH','closes':closes,'frame':{'available_ts':[sn]*(i*1440)},'signal_funds':funds};a=engine.base_decide(spec,m,i,actual);b=engine.base_decide(spec,{**m,'closes':closes[:i]+[F(10**12),F(1)],'signal_funds':funds+[future]},i,actual);assert a==b and a[1]['funding_filter']['budget_volatility_window_days']==vw;cases.append({'R':ratio,'VW':vw,'actual':actual,'full_ETH_policy_unchanged_by_future_closes_or_funding':True})
put(R/'exact_parameter_registry_screen.json',{'passed':True,'recorded_utc':now(),'new_ETH_budget_ratios':[.009375,.010625],'old_exact_matching_ratios':[z['parameters']['entry_funding_volatility_ratio'] for z in prior],'exact_matching_actual_or_running_configs':0,'fixed_ETH_VW':8,'fixed_ETH_M':4,'readonly_BTC_H':[.03,.0325],'no_market_or_account_calculations':True})
put(R/'prebinding_parameter_guard_verification.json',{'passed':True,'recorded_utc':now(),'old_source':rel(P/'engine.py'),'old_sha256':sha(P/'engine.py'),'new_source':rel(R/'engine.py'),'new_sha256':sha(R/'engine.py'),'intentional_policy_changes':['Only predeclaredETHbudgetR.009375/.010625 atVW8;engine/money sourcebytesexactunchanged. FixedM4/risk/trend.','CompletedVW daily samplelogvol,past actualfundinterval;outflowbudgetequalitypasses,holdq unchanged;futureprice/funding excluded.'],'policy_and_money_source_bytes_exactly_unchanged':True,'full_engine_source_bytes_exactly_unchanged':True,'money_core_bytes_unchanged':True,'simulate_and_money_core_bytes_unchanged':True,'synthetic_checks':cases,'before_first_reservation_or_market_calculation':True,'current_evaluation_failures':0,'current_preparation_failures':0})
checked=[]
for f in R.rglob('*.py'):
 t=ast.parse(f.read_text());assert not[z for z in ast.walk(t) if isinstance(z,ast.Subscript) and isinstance(z.value,ast.Name) and z.value.id in ['ROOT','R','P']],str(f);checked.append(rel(f))
put(R/'path_join_guard.json',{'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True});print('PASS',len(cases),'syntheticETHbudgetcoefficient/equality/maturity/futuresuffixchecks;0market/accountvaluations')
