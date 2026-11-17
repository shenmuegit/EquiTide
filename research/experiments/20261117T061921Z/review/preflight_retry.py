"""First actual funding query after restoring the unchanged local accounting dependency."""
import runpy,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R))
from common import *
P=ROOT/'research/experiments/20261117T041819Z';assert sha(R/'core391_tail_safe.py')==sha(P/'core391_tail_safe.py') and not (R/'window_funding_preflight_attempts.json').exists()
runpy.run_path(str(R/'review/preflight.py'),run_name='__main__')
f=R/'read_failures.json';x=json.loads(f.read_text());assert len(x['facts'])==1 and not x['facts'][0]['resolved'];x['facts'][0].update(resolved=True,resolution='Copied original core391_tail_safe.py byte-identically before first HTTP query; original failed source/log/exit1 retained.',restored_core_sha256=sha(R/'core391_tail_safe.py'),retry_helper='review/preflight_retry.py');put(f,x)
put(R/'preflight_dependency_verification.json',{'passed':True,'recorded_utc':now(),'original_failure_before_HTTP_reserve_or_calculation':True,'prior_core_sha256':sha(P/'core391_tail_safe.py'),'restored_core_sha256':sha(R/'core391_tail_safe.py'),'same_preflight_source_reexecuted_after_dependency_copy':True,'first_actual_public_query_completed':True,'current_engineering_preparation_failures':1,'no_financial_model_or_account_evaluations':True})
