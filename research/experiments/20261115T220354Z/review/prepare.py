"""Prepare exit-buffer geometry and verify scalar/descriptive consistency before reserve."""
import ast,json,sys
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261115T200222Z';sys.path.insert(0,str(R));from common import *
prior=json.loads((R/'native_exit_prior_lookup.json').read_text())['matching_fixed_definitions'];assert prior and not any(x['E'] in [.01,.015] and (x['result_available'] or x['status']=='reserved') for x in prior)
def edit(name,pairs):
 p=R/name;s=p.read_text()
 for a,b in pairs:assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);p.write_text(s)
for name in ['run.py','audit.py','exports.py']:edit(name,[('BTC_ROC_LOOKBACK','BTC_EXIT_BUFFER')])
edit('definitions.py',[("q['lookback_days'] in [28,30]","q['lookback_days']==29"),("q['exit_buffer_fraction']==.005","q['exit_buffer_fraction'] in [.01,.015]")])
p=R/'definitions.py';s=p.read_text();a="excluded={'commands.py'";b="descriptor=p['rules']['signal'];assert descriptor.startswith('BTC completedROC L29/strictentryH.03/exitE[.005,.01,.015]/priorV10samplelogvolCap.0275.')"+chr(10)+"assert all(json.loads((ROOT/z['spec']).read_text())['logic']['signal']==descriptor for z in batch)"+chr(10)+"assert all(json.loads((ROOT/z['spec']).read_text())['parameters']['exit_buffer_fraction']==z['W'] for z in batch if z['scope']=='native')"+chr(10)+"put(R/'signal_scalar_consistency_before_reservation.json',{'passed':True,'recorded_utc':now(),'explicit_signal':descriptor,'scalar_L':29,'scalar_H':.03,'native_E':[.01,.015],'old_E_readonly':.005,'native_V':10,'native_cap':.0275,'all_new_specs_match_descriptor_and_scalar_axis':True,'before_first_reservation':True,'no_market_or_account_calculations':True})"+chr(10)+a;assert a in s;s=s.replace(a,b);ast.parse(s);p.write_text(s)
edit('parent_units.py',[("E=F('.005');H=F('.03')\nfor L in [28,29,30]:","L=29;H=F('.03')\nfor E in [F('.005'),F('.01'),F('.015')]:"),("g['W']==29","g['W']==.01")])
edit('exports.py',[('BTC completed ROC lookback, days','BTC exit buffer E'),("['28 days','29 days','30 days']","['0.5%','1.0%','1.5%']"),('Preregistered BTC ROC memory / reused ETH funding budget','Preregistered BTC exit buffer / reused ETH funding budget')])
edit('review/diagnostics.py',[("center=btc[29]","center=btc[.005]"),('[28,30]','[.005,.015]'),('for V in [.005,.015]:','for V in [.01,.015]:'),("c['W']==29","c['W']==.005"),('BTC_ROC_lookback_days','BTC_exit_buffer_fraction'),('BTC_ROC_lookback_axis_boundary','BTC_exit_buffer_axis_boundary'),('matched_lookback29','matched_exit0p5percent'),('old_lookback29','old_exit0p5percent'),('ROC-lookback','exit-buffer'),('actual BTC entry-volatility-cap trade changes','actual BTC exit-buffer trade changes')])
edit('review/visual_review.py',[('BTC_ROC_lookback_days','BTC_exit_buffer_fraction'),('{28,29,30}','{.005,.01,.015}'),('[28,30]','[.01,.015]'),("y['BTC_exit_buffer_fraction']==29","y['BTC_exit_buffer_fraction']==.005"),('old_lookback29','old_exit0p5percent'),('BTC completedROC memory28/29/30days rows,V10/cap2.75percent fixed','BTC actual-position exitE0.5/1/1.5percent rows,L29/V10/cap2.75percent fixed'),('three BTC ROC lookbacks','three BTC exit buffers with old0.5percent reference at a boundary')])
assert sha(P/'engine.py')==sha(R/'engine.py') and sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py')
import engine
cases=[];L=29;H=F('.03')
for E in [F('.005'),F('.01'),F('.015')]:
 for actual in [-1,0,1]:
  for roc in [-H-F('1e-8'),-H,-E-F('1e-8'),-E,F(0),E,E+F('1e-8'),H,H+F('1e-8')]:
   c=[F(200)]*60;c[39-L]=F(100);c[39]=100*(1+roc);expected=1 if roc>H else -1 if roc<-H else 1 if actual==1 and roc>-E else -1 if actual==-1 and roc<E else 0;out=engine.btc.target(c,40,L,float(H),actual,float(E));assert out[0]==expected and F(out[1])==roc and out==engine.btc.target(c[:40]+[F(10**12),F(1)],40,L,float(H),actual,float(E));cases.append({'E':str(E),'actual':actual,'ROC':str(roc),'passed':True})
put(R/'exact_parameter_registry_screen.json',{'passed':True,'recorded_utc':now(),'new_exit_buffers':[.01,.015],'matching_fixed_definitions':prior,'fixed':{'L':29,'H':.03,'V':10,'cap':.0275,'capital':3750,'notional':1000,'days':391},'no_market_or_account_calculations':True})
put(R/'prebinding_parameter_guard_verification.json',{'passed':True,'recorded_utc':now(),'old_source':rel(P/'engine.py'),'old_sha256':sha(P/'engine.py'),'new_source':rel(R/'engine.py'),'new_sha256':sha(R/'engine.py'),'exact_only_source_changes':[],'policy_and_money_source_bytes_exactly_unchanged':True,'formulas_and_full_AST_unchanged_after_validation_list_normalization':True,'simulate_and_money_core_bytes_unchanged':True,'synthetic_checks':cases,'before_first_reservation_or_market_calculation':True,'current_evaluation_failures':0,'current_preparation_failures':0})
checked=[]
for f in R.rglob('*.py'):
 tree=ast.parse(f.read_text());assert not[n for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(f);checked.append(rel(f))
put(R/'path_join_guard.json',{'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True});print('PASS exitE1/1.5 planned,explicit descriptor guards,engine/core unchanged,81strict/future-suffix checks;0market/account calculations')
