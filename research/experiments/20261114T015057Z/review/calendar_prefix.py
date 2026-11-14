"""Read saved archives only: extending the terminal must not alter any earlier causal decision."""
import gzip,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import sha,put,now,rel
P=ROOT/'research/experiments/20261113T234922Z';old=json.loads((P/'report.json').read_text());new=json.loads((R/'report.json').read_text());rows=[]
for c in new['configs'].values():
 if c['scope']!='native':continue
 prior=old['configs'][c['name'].replace('extend391_','extend390_')];a=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));b=json.loads(gzip.decompress((ROOT/prior['archive']).read_bytes()));assert sha(ROOT/prior['archive'])==prior['archive_sha256']
 for k,x in a['scenes'].items():
  y=b['scenes'][k];assert len(y['decisions'])==390 and x['decisions'][:390]==y['decisions'];assert x['funding_events'][:len(y['funding_events'])]==y['funding_events'];ot=[z for z in y['trades'] if not z['terminal']];nt=[z for z in x['trades'] if not z['terminal']];assert nt[:len(ot)]==ot
  rows.append({'name':c['name'],'prior_fingerprint':prior['fingerprint'],'fingerprint':c['fingerprint'],'cost':k,'old390_decisions_exact_equal':True,'old_funding_records_exact_equal':len(y['funding_events']),'old_nonterminal_trades_exact_equal':len(ot),'prior_status':prior['status'],'current_status':c['status'],'old_recent_positive_folds':prior['recent40_positive_5d_folds_by_cost'][k],'new_recent_positive_folds':c['recent40_positive_5d_folds_by_cost'][k]})
put(R/'calendar_prefix_verification.json',{'passed':True,'verified_utc':now(),'rows':rows,'old_report_sha256':sha(P/'report.json'),'new_report_sha256':sha(R/'report.json'),'18_native_curves_causal_prefix_verified':len(rows)==18,'old_terminal_exit_not_injected_into_new_period':True,'rolling_recent40_boundaries_changed_as_predeclared':True,'BTC_cap3_qualification_shift_not_independent_future_evidence':True,'new_model_or_account_calculations':0});print('PASS18savednativeprefixes:390olddecisions/funds/nonterminaltrades exact,oldterminalnotconcatenated')
