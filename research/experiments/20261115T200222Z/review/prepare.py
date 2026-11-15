"""Prepare a fixed BTC entry-hurdle neighborhood with unchanged native money code."""
import ast,copy,json,re,sys
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261115T180155Z';sys.path.insert(0,str(R));from common import *
prior=json.loads((R/'native_hurdle_prior_lookup.json').read_text())['matching_fixed_definitions'];assert prior and not any(x['H'] in [.025,.035] and (x['result_available'] or x['status']=='reserved') for x in prior)
def edit(name,pairs):
 p=R/name;s=p.read_text()
 for a,b in pairs:assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);p.write_text(s)
for name in ['run.py','audit.py','exports.py']:edit(name,[('BTC_ROC_LOOKBACK','BTC_ENTRY_HURDLE')])
edit('definitions.py',[("q['lookback_days'] in [28,30]","q['lookback_days']==29"),("q['return_hurdle']==.03","q['return_hurdle'] in [.025,.035]")])
edit('parent_units.py',[("E=F('.005');H=F('.03')\nfor L in [28,29,30]:","E=F('.005');L=29\nfor H in [F('.025'),F('.03'),F('.035')]:"),("g['W']==29","g['W']==.03")])
p=R/'freeze.py';s=p.read_text().replace("bs={29:reuse(B,29,.01)};es={r:reuse(actual(fp),29,r)","bs={.03:reuse(B,.03,.01)};es={r:reuse(actual(fp),.03,r)");s=re.sub(r'\bL\b','H',s)
for a,b in [('[28,30]','[.025,.035]'),('[28,29,30]','[.025,.03,.035]'),('if H==29:','if H==.03:'),("==(28,.01)","==(.025,.01)"),("'representative_preset':{'W':28","'representative_preset':{'W':.025"),("sp['parameters']['lookback_days']=H","sp['parameters']['return_hurdle']=H"),("name=f'BTC_L{H}_H3_E0p005_V10cap0p0275_391d'","name=f'BTC_L29_Hfrac{str(H).replace(chr(46),chr(112))}_E0p005_V10cap0p0275_391d'"),("name=f'parent_BTCL{H}_V10cap0p0275_H3_E0p005_ETHR","name=f'parent_BTCHfrac{str(H).replace(chr(46),chr(112))}_L29_V10cap0p0275_E0p005_ETHR"),('BTC_ROC_LOOKBACK','BTC_ENTRY_HURDLE'),('btc-roc-memory-fixed-risk-earlyexit-neighborhood','btc-roc-entry-hurdle-fixed-risk-earlyexit-neighborhood'),('btc-roc-memory-eth-carry-bank-combination','btc-roc-entry-hurdle-eth-carry-bank-combination'),('BTC_native_only_own_ROC_lookback_axis','BTC_native_only_own_entry_hurdle_axis'),('ThreeBTCROCmemories','ThreeBTCentryhurdles'),('predeclared3BTCvolcapsx2ETHR','predeclared3BTCentryhurdlesx2ETHR')]:
 assert a in s,('freeze',a);s=s.replace(a,b)
s=s.replace('BTC strictcompletedROC L[.025,.03,.035]/entryH.03/exitE.005','BTC strictcompletedROC L29/entryH[.025,.03,.035]/exitE.005')
hyp='Does BTC strict completed29day ROC entry hurdle H2.5/H3.5percent at fixed E.005/V10/cap.0275 improve chronological net performance around actual H3percent? H[.025,.03,.035] x readonly ETH R[.00875,.01]. Preset H.025/R.01 frozen before outcomes: lower entry hurdle captures moves earlier but may add turnover; higher hurdle filters weak moves but delays entry. No after-result grid extension or reselection. Old H.03 BTC and center parents, ETH banks and holds readonly.'
s,n=re.subn(r"'hypothesis':'[^']*'",lambda _:"'hypothesis':"+repr(hyp),s);assert n==1
s,n=re.subn(r"'W':'[^']*'","'W':'BTC strict absolute29day ROC entry hurdle fraction H=.025/.03/.035 (2.5/3/3.5percent);E.005/V10/cap.0275 fixed;strict entry priority and actual-position hysteresis unchanged'",s);assert n==1
s,n=re.subn(r"'novelty':'[^']*'","'novelty':'New exact BTC H.025/H.035 at fixed L29/E.005/V10/cap.0275; old H.03 center and ETH banks readonly. Native quantities, impact and funding calculated at original capital.'",s);assert n==1
s=s.replace('Predeclare BTC entry volatility ceiling with fixed ROC memory,entry and early exit','Predeclare BTC ROC entry hurdle with fixed lookback,risk window and early exit');ast.parse(s);p.write_text(s)
edit('exports.py',[('BTC completed ROC lookback, days','BTC strict ROC entry hurdle'),("['28 days','29 days','30 days']","['2.5%','3.0%','3.5%']"),('Preregistered BTC ROC memory / reused ETH funding budget','Preregistered BTC entry hurdle / reused ETH funding budget')])
edit('review/diagnostics.py',[("center=btc[29]","center=btc[.03]"),('[28,30]','[.025,.035]'),("c['W']==29","c['W']==.03"),('BTC_ROC_lookback_days','BTC_entry_hurdle_fraction'),('BTC_ROC_lookback_axis_boundary','BTC_entry_hurdle_axis_boundary'),('matched_lookback29','matched_hurdle3percent'),('old_lookback29','old_hurdle3percent'),('ROC-lookback','entry-hurdle')])
edit('review/visual_review.py',[('BTC_ROC_lookback_days','BTC_entry_hurdle_fraction'),('{28,29,30}','{.025,.03,.035}'),('[28,30]','[.025,.035]'),("y['BTC_entry_hurdle_fraction']==29","y['BTC_entry_hurdle_fraction']==.03"),('old_lookback29','old_hurdle3percent'),('BTC completedROC memory28/29/30days rows,V10/cap2.75percent fixed','BTC strict29dayROC entry2.5/3/3.5percent rows,V10/cap2.75percent fixed'),('three BTC ROC lookbacks','three BTC entry hurdles')])
assert sha(P/'engine.py')==sha(R/'engine.py') and sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py')
import engine
cases=[];E=F('.005');L=29
for H in [F('.025'),F('.03'),F('.035')]:
 for actual in [-1,0,1]:
  for roc in [-H-F('1e-8'),-H,-E-F('1e-8'),-E,F(0),E,E+F('1e-8'),H,H+F('1e-8')]:
   c=[F(200)]*60;c[39-L]=F(100);c[39]=100*(1+roc);expected=1 if roc>H else -1 if roc<-H else 1 if actual==1 and roc>-E else -1 if actual==-1 and roc<E else 0;out=engine.btc.target(c,40,L,float(H),actual,float(E));assert out[0]==expected and F(out[1])==roc and out==engine.btc.target(c[:40]+[F(10**12),F(1)],40,L,float(H),actual,float(E));cases.append({'H':str(H),'actual':actual,'ROC':str(roc),'passed':True})
put(R/'exact_parameter_registry_screen.json',{'passed':True,'recorded_utc':now(),'new_entry_hurdles':[.025,.035],'matching_fixed_definitions':prior,'fixed':{'L':29,'E':.005,'V':10,'cap':.0275,'capital':3750,'notional':1000,'days':391},'no_market_or_account_calculations':True})
put(R/'prebinding_parameter_guard_verification.json',{'passed':True,'recorded_utc':now(),'old_source':rel(P/'engine.py'),'old_sha256':sha(P/'engine.py'),'new_source':rel(R/'engine.py'),'new_sha256':sha(R/'engine.py'),'exact_only_source_changes':[],'policy_and_money_source_bytes_exactly_unchanged':True,'formulas_and_full_AST_unchanged_after_validation_list_normalization':True,'simulate_and_money_core_bytes_unchanged':True,'synthetic_checks':cases,'before_first_reservation_or_market_calculation':True,'current_evaluation_failures':0,'current_preparation_failures':0})
checked=[]
for f in R.rglob('*.py'):
 tree=ast.parse(f.read_text());assert not[n for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(f);checked.append(rel(f))
put(R/'path_join_guard.json',{'passed':True,'checked':checked,'Path_names_not_subscripted':True,'before_binding_and_evaluation':True,'no_model_or_account_calculations':True});print('PASS6 planned new hurdle definitions,engine/core bytes unchanged,81strict boundary/future-suffix cases;0market/account calculations')
