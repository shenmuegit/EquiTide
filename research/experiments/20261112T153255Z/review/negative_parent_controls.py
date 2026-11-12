"""Two deliberate synthetic errors must be detected; no actual market calculations."""
import os,subprocess,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import now,put
for name,arg in [('negative_parent_normalization','--mutant-normalize'),('negative_parent_fold_reset','--mutant-fold-reset')]:
 a=now();cmd=[sys.executable,'-B',str(R/'parent_units.py'),arg];z=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);(R/(name+'.log')).write_text(z.stdout+z.stderr);put(R/(name+'_receipt.json'),{'command':cmd,'cwd':str(ROOT),'started_utc':a,'finished_utc':now(),'exit_code':z.returncode,'expected_exit_code':1,'synthetic_only':True,'real_market_or_account_calculations':0});assert z.returncode==1 and 'AssertionError' in z.stderr
print('PASS two expected synthetic failures')
