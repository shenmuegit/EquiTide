"""Resume untouched frozen definitions after a nonfinancial checker typo stopped all reserves."""
import json,subprocess,sys
from run import ROOT,R,reg,sha,put,call
binding=json.loads((R/'frozen_recovery_binding.json').read_text());assert sha(R/'plan.json')==binding['plan_sha256'] and sha(R/'batch.json')==binding['batch_sha256'] and all(sha(ROOT/p)==h for p,h in binding['specs_sha256'].items()) and not(R/'report.json').exists() and not(R/'reserve.json').exists();inv=json.loads((R/'inventory.json').read_text());assert sha(ROOT/'research/automation/registry.jsonl')==inv['registry_sha256_before_reserve']
cmd=[sys.executable,str(R/'check_definitions.py')];z=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);(R/'definition_recovery_preflight.log').write_text(z.stdout+z.stderr);put(R/'definition_recovery_preflight_command.json',{'command':cmd,'cwd':str(ROOT),'exit_code':z.returncode,'stdout':z.stdout,'stderr':z.stderr});assert z.returncode==0,z.stderr
batch=json.loads((R/'batch.json').read_text());done=[]
for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
assert len(done)==12 and sha(R/'plan.json')==binding['plan_sha256'] and sha(R/'batch.json')==binding['batch_sha256'] and all(sha(ROOT/p)==h for p,h in binding['specs_sha256'].items());print('PASS:all12untouchedfrozenconfigsreservedaftercompletecorrecteddefinitionpreflight;priorfailurespreserved.',flush=True)
