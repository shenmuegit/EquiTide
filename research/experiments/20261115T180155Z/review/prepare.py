"""Prepare the preregistered ROC-memory neighborhood; preserve all money kernels."""
import ast,copy,importlib.util,json,re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261115T160124Z';sys.path.insert(0,str(R));from common import *
def edit(name,pairs):
 p=R/name;s=p.read_text()
 for a,b in pairs:
  assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);p.write_text(s)
for name in ['run.py','audit.py','exports.py']:
 edit(name,[('BTC_VOL_WINDOW','BTC_ROC_LOOKBACK')])
edit('definitions.py',[("q['lookback_days']==29","q['lookback_days'] in [28,30]"),("q['entry_volatility_window_days'] in [8,12]","q['entry_volatility_window_days']==10"),("'policy_and_accounting_source_equal_to_prior':False","'policy_and_accounting_source_equal_to_prior':True")])
edit('parent_units.py',[("for L in [29]:","for L in [28,29,30]:"),("g['W']==10","g['W']==29")])
p=R/'freeze.py';s=p.read_text();s=s.replace("bs={10:reuse(B,10,.01)};es={r:reuse(actual(fp),10,r)","bs={29:reuse(B,29,.01)};es={r:reuse(actual(fp),29,r)");s=re.sub(r'\bV\b','L',s)
for a,b in [('[8,12]','[28,30]'),('[8,10,12]','[28,29,30]'),('if L==10:','if L==29:'),("==(8,.01)","==(28,.01)"),("'representative_preset':{'W':8","'representative_preset':{'W':28"),("sp['parameters']['entry_volatility_window_days']=L","sp['parameters']['lookback_days']=L"),('BTC_L29_H3_E0p005_V{L}cap0p0275','BTC_L{L}_H3_E0p005_V10cap0p0275'),('parent_BTCV{L}cap0p0275_L29_H3_E0p005_ETHR','parent_BTCL{L}_V10cap0p0275_H3_E0p005_ETHR'),('BTC_VOL_WINDOW','BTC_ROC_LOOKBACK'),('btc-volatility-window-earlyexit-neighborhood','btc-roc-memory-fixed-risk-earlyexit-neighborhood'),('btc-volatility-window-eth-carry-bank-combination','btc-roc-memory-eth-carry-bank-combination'),('BTC_native_only_own_entry_volatility_window_axis','BTC_native_only_own_ROC_lookback_axis'),('ThreeBTCvolatilitywindows','ThreeBTCROCmemories')]:
 assert a in s,('freeze.py',a);s=s.replace(a,b)
s=s.replace('BTC strictcompletedROC L29/entryH.03/exitE.005,priorV[28,29,30]sampledailylogvol<=cap.0275','BTC strictcompletedROC L[28,29,30]/entryH.03/exitE.005,priorV10sampledailylogvol<=cap.0275')
hyp='Does BTC completed ROC memory L28/L30 at fixed H.03/E.005/V10/cap.0275 improve chronological net performance around actual L29? L[28,29,30] x readonly ETH R[.00875,.01]. Preset L28/R.01 frozen before outcomes: shorter ROC can react earlier but trade more; longer ROC smooths noise but delays exits. No after-result extension or reselection. Old L29, ETH banks, center parents and holds readonly.'
s,n=re.subn(r"'hypothesis':'[^']*'",lambda _:"'hypothesis':"+repr(hyp),s);assert n==1
s,n=re.subn(r"'W':'[^']*'","'W':'BTC completed ROC lookback L in28/29/30 days;H.03/E.005/V10/cap.0275 fixed;strict entry priority and actual-position hysteresis unchanged'",s);assert n==1
s,n=re.subn(r"'novelty':'[^']*'","'novelty':'New exact BTC L28/L30 at fixed H.03/E.005/V10/cap.0275; old L29 center and ETH banks readonly. Native quantities, impact and all funding calculated at original capital.'",s);assert n==1
ast.parse(s);p.write_text(s)
edit('exports.py',[('BTC entry volatility window, days','BTC completed ROC lookback, days'),("['8 days','10 days','12 days']","['28 days','29 days','30 days']"),('Preregistered BTC volatility memory / reused ETH funding budget','Preregistered BTC ROC memory / reused ETH funding budget')])
edit('review/diagnostics.py',[("center=btc[10]","center=btc[29]"),('[8,12]','[28,30]'),("c['W']==10","c['W']==29"),('BTC_entry_volatility_window_days','BTC_ROC_lookback_days'),('BTC_volatility_window_axis_boundary','BTC_ROC_lookback_axis_boundary'),('matched_window10','matched_lookback29'),('old_window10','old_lookback29'),('entry-volatility-window','ROC-lookback')])
edit('review/visual_review.py',[('BTC_entry_vol_window_days','BTC_ROC_lookback_days'),('{8,10,12}','{28,29,30}'),('[8,12]','[28,30]'),("y['BTC_ROC_lookback_days']==10","y['BTC_ROC_lookback_days']==29"),('old_window10','old_lookback29'),('BTC_vol_window_days','BTC_ROC_lookback_days'),('BTC sampledailylogvol memory8/10/12days rows,cap2.75percent fixed','BTC completedROC memory28/29/30days rows,V10/cap2.75percent fixed'),('L29/H3/E0.5 fixed','H3/E0.5 fixed'),('three BTC memory windows','three BTC ROC lookbacks')])
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');hits=[]
for fp,z in rs.items():
 sp=z.get('spec',{});q=sp.get('parameters',{})
 if sp.get('kind')=='strategy' and sp.get('universe')==['BTC/USDT'] and q.get('return_hurdle')==.03 and q.get('exit_buffer_fraction')==.005 and q.get('entry_volatility_window_days')==10 and q.get('entry_volatility_ceiling')==.0275 and q.get('continuous_oos_days')==391 and q.get('initial_capital_usdt')==3750 and q.get('fixed_entry_notional_usdt')==1000 and q.get('start_utc')=='2025-10-19T00:01:00Z' and q.get('end_utc')=='2026-11-14T00:01:00Z':hits.append({'fingerprint':fp,'L':q['lookback_days'],'status':z['status'],'result_available':z['result_available']})
assert hits and not any(z['L'] in [28,30] and (z['result_available'] or z['status']=='reserved') for z in hits)
put(R/'exact_parameter_registry_screen.json',{'passed':True,'recorded_utc':now(),'new_ROC_lookbacks':[28,30],'matching_fixed_definitions':hits,'fixed':{'H':.03,'E':.005,'V':10,'cap':.0275,'capital':3750,'notional':1000,'days':391},'no_market_or_account_calculations':True})
assert sha(P/'engine.py')==sha(R/'engine.py') and sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py')
import engine
from fractions import Fraction as F
cases=[];H=F('.03');E=F('.005')
for L in [28,29,30]:
 for actual in [-1,0,1]:
  for roc in [-H-F('1e-8'),-H,-E-F('1e-8'),-E,F(0),E,E+F('1e-8'),H,H+F('1e-8')]:
   c=[F(200)]*60;c[39-L]=F(100);c[39]=100*(1+roc);expected=1 if roc>H else -1 if roc<-H else 1 if actual==1 and roc>-E else -1 if actual==-1 and roc<E else 0
   out=engine.btc.target(c,40,L,float(H),actual,float(E));assert out[0]==expected and F(out[1])==roc and out==engine.btc.target(c[:40]+[F(10**12),F(1)],40,L,float(H),actual,float(E));cases.append({'L':L,'actual':actual,'ROC':str(roc),'passed':True})
put(R/'prebinding_parameter_guard_verification.json',{'passed':True,'recorded_utc':now(),'old_source':rel(P/'engine.py'),'old_sha256':sha(P/'engine.py'),'new_source':rel(R/'engine.py'),'new_sha256':sha(R/'engine.py'),'exact_only_source_changes':[],'policy_and_money_source_bytes_exactly_unchanged':True,'formulas_and_full_AST_unchanged_after_validation_list_normalization':True,'simulate_and_money_core_bytes_unchanged':True,'synthetic_checks':cases,'before_first_reservation_or_market_calculation':True,'current_evaluation_failures':0,'current_preparation_failures':0})
checked=[]
for f in R.rglob('*.py'):
 tree=ast.parse(f.read_text());assert not[n for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(f);checked.append(rel(f))
put(R/'path_join_guard.json',{'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True})
print('PASS new BTC L28/L30 x readonly ETH R, engine/core bytes unchanged,81 synthetic strict-boundary/future-suffix cases;0market calculations')
