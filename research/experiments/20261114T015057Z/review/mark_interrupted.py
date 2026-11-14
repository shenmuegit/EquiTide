"""Finish every interrupted reservation as blocked without actual results, preserving retry eligibility."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
batch=json.loads((R/'batch.json').read_text());assert not(R/'report.json').exists() and not list((R/'results').glob('*'));(R/'results').rmdir()
put(R/'implementation_blocked_report.json',{'status':'blocked','result_available':False,'recorded_utc':now(),'failure_receipt':rel(R/'evaluate_commands.json'),'failure_log':rel(R/'evaluate.log'),'first_config':batch[0]['fingerprint'],'scope':'First native cost scene interrupted in summary before any curve/archive/report completed;dependent native and parent configs not yet evaluated. No return result exists.','reason':'One-day tail has one daily return; old sample stdev requires2. Sharpe must be None. Rules/parameters/gates will remain unchanged.','completed_native_cost_curves':0,'completed_parent_cost_curves':0,'financial_evaluation_attempts':1,'recovery_allowed':True})
done=[]
for row in batch:
 a=now();z=call('finish',row,'blocked',rel(R/'implementation_blocked_report.json'));z.update(started_utc=a,finished_utc=now());done.append(z);put(R/'interrupted_finish_receipts.json',done)
print('PASS11blocked/noresult finish records,all recoverable')
