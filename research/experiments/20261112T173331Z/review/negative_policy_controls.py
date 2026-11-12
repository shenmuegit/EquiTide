"""Two deliberate OHLC timing/direction mutants must trigger specific semantic guards."""
import subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import now,put
for name,arg,guard in [('negative_policy_future_close','--future-close','Completed UTC daily range is not available at signal'),('negative_policy_ignore_direction','--ignore-direction','Known completed UTC daily CLV uses full intraday extrema and candidate sign')]:
 a=now();cmd=[sys.executable,'-B',str(R/'policy_units.py'),arg];z=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);(R/(name+'.log')).write_text(z.stdout+z.stderr);put(R/(name+'_receipt.json'),{'command':cmd,'cwd':str(ROOT),'started_utc':a,'finished_utc':now(),'exit_code':z.returncode,'expected_exit_code':1,'synthetic_only':True,'expected_semantic_guard':guard,'actual_market_or_account_evaluations':0});assert z.returncode==1 and guard in z.stderr
print('PASS current/future UTC daily extrema and omitted candidate direction mutants rejected by specific semantic guards')
