"""Deliberate future-close leak and forced existing-position exit must fail synthetic guards."""
import subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import now,put
for name,arg in [('negative_policy_future_close_retry1','--future-close'),('negative_policy_gate_existing_retry1','--gate-existing')]:
 a=now();cmd=[sys.executable,'-B',str(R/'policy_units.py'),arg];z=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);(R/(name+'.log')).write_text(z.stdout+z.stderr);put(R/(name+'_receipt.json'),{'command':cmd,'cwd':str(ROOT),'started_utc':a,'finished_utc':now(),'exit_code':z.returncode,'expected_exit_code':1,'synthetic_only':True,'actual_market_or_account_evaluations':0});assert z.returncode==1 and 'AssertionError' in z.stderr and (('Known unbiased closed-close volatility' in z.stderr or 'Future closes influenced entry volatility' in z.stderr) if arg=='--future-close' else 'Known entry/hold direction' in z.stderr)
print('PASS two deliberate policy errors detected')
