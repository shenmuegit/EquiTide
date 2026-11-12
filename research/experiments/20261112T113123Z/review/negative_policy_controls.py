"""Two deliberately faulty downside estimators must fail a known analytic RMS assertion."""
import subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import now,put
for name,arg in [('negative_policy_future_close','--future-close'),('negative_policy_negative_count','--negative-count')]:
 a=now();cmd=[sys.executable,'-B',str(R/'policy_units.py'),arg];z=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);(R/(name+'.log')).write_text(z.stdout+z.stderr);put(R/(name+'_receipt.json'),{'command':cmd,'cwd':str(ROOT),'started_utc':a,'finished_utc':now(),'exit_code':z.returncode,'expected_exit_code':1,'synthetic_only':True,'actual_market_or_account_evaluations':0});assert z.returncode==1 and 'Known zero-target downside RMS uses all V observations' in z.stderr
print('PASS2actualfaultydownsideestimators rejected by analyticRMSguard')
