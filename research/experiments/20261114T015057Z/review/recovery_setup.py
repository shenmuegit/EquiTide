"""Preserve the interrupted implementation, then make only undefined one-day Sharpe safe."""
import ast,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
assert len(json.loads((R/'interrupted_finish_receipts.json').read_text()))==11
old=json.loads((R/'code_binding_before_evaluation.json').read_text());d=R/'implementation_attempt01';d.mkdir();archived={}
for path,h in old['source_sha256'].items():
 f=ROOT/path;assert sha(f)==h;dest=d/f.name;dest.write_bytes(f.read_bytes());archived[path]={'archive':rel(dest),'sha256':h}
for n in ['code_binding_before_evaluation.json','definition_check.json']:(R/n).rename(d/n)
s=(R/'core391.py').read_text();assert s.count('sd=statistics.stdev(rr);')==1;s=s.replace('sd=statistics.stdev(rr);','sd=statistics.stdev(rr) if len(rr)>1 else None;');(R/'core391_tail_safe.py').write_text(s)
f=R/'common.py';f.write_text(f.read_text().replace("CORE_PATH=R/'core391.py'","CORE_PATH=R/'core391_tail_safe.py'"))
f=R/'audit_helpers_complete.py';s=f.read_text();assert 'sd=np.std(rr,ddof=1)' in s;s=s.replace('sd=np.std(rr,ddof=1)','sd=np.std(rr,ddof=1) if len(rr)>1 else None');f.write_text(s)
f=R/'definitions.py';s=f.read_text().replace("funs(R/'core391.py')","funs(R/'core391_tail_safe.py')").replace("if k!='load_market'","if k not in ['load_market','stats']").replace("row['fingerprint'] not in rs and", "(row['fingerprint'] not in rs or rs[row['fingerprint']]['status']=='blocked' and not rs[row['fingerprint']]['result_available']) and").replace("'no_new_research_calculation_yet':True","'no_new_research_calculation_yet':False,'no_completed_research_curve_before_recovery':True").replace('No policy or moneyformula ASTchanges;only declared391daymarket/calendar geometry','No policy or native moneyformula ASTchanges;only one-day sample Sharpe undefined=None plus declared391daymarket/calendar geometry');f.write_text(s)
# The spec bytes, parameter grid and monetary rules remain exactly frozen.
for path,h in old['immutable_source_sha256'].items():assert sha(ROOT/path)==h,path
put(R/'implementation_recovery_binding.json',{'passed':True,'recorded_utc':now(),'initial_interrupted_source_snapshots':archived,'initial_binding':rel(d/'code_binding_before_evaluation.json'),'initial_binding_sha256':sha(d/'code_binding_before_evaluation.json'),'new_tail_safe_source':rel(R/'core391_tail_safe.py'),'new_tail_safe_sha256':sha(R/'core391_tail_safe.py'),'only_core_source_difference':"sd=statistics.stdev(rr) if len(rr)>1 else None",'one_day_Sharpe_undefined_not_zero':True,'all_multiday_statistics_bitwise_identical_test_required':True,'original_policies_native_trade_funding_and_margin_AST_unchanged':True,'all_frozen_specs_inputs_rules_weights_and_gates_byte_identical':True,'prior_noresult_finish_events':11,'prior_completed_curves':0,'completed_models_not_replayed':True})
for f in R.rglob('*.py'):ast.parse(f.read_text())
print('PASS interrupted sources/specs preserved,only undefined one-return samplevariance guarded')
