"""Reserve a new mark-only cutoff or finish the three actual partial observations."""
import argparse,copy,json
from run import R,ROOT,reg,put,sha,rel,now,call
from datetime import datetime
PREV=ROOT/'research/experiments/20261029T012253Z'
ms=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*1000)
def reserve():
 assert not (R/'forward_resume_plan.json').exists()
 old=json.loads((PREV/'forward_report.json').read_text());state=json.loads((PREV/'forward_state.json').read_text());cut='2026-10-29T02:30:00Z'
 assert old['cutoff_utc']=='2026-10-29T00:30:00Z' and cut=='2026-10-29T02:30:00Z'
 assert state['source_report_sha256']==sha(PREV/'forward_report.json') and state['last_completed_mark_utc']==old['cutoff_utc'] and ms(old['cutoff_utc'])<ms(cut)<ms(state['next_daily_decision_utc']) and ms(cut)<ms(now())
 frozen=ROOT/old['frozen_plan_path'];assert sha(frozen)==old['frozen_plan_sha256']==state['frozen_plan_sha256']=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
 points=len(old['configs']['forward_snapshot_combo']['scenes']['1']['equity_usdt']);delta=(ms(cut)-ms(old['cutoff_utc']))//60000
 plan={'frozen_at_utc':now(),'forward_resume':{'source_report':rel(PREV/'forward_report.json'),'report_sha256':sha(PREV/'forward_report.json'),'source_state':rel(PREV/'forward_state.json'),'state_sha256':sha(PREV/'forward_state.json'),'resume_utc':old['cutoff_utc'],'cutoff_utc':cut,'new_minutes':delta,'prior_NAV_points':points,'total_NAV_points':points+delta,'cumulative_minutes':old['configs']['forward_snapshot_combo']['scenes']['1']['elapsed_minutes']+delta},'frozen_original_plan':rel(frozen),'frozen_original_plan_sha256':sha(frozen),'rule':'Original SMA65/symmetric1%,rawBTC1500/ETH500 and per-cost Float accounting;closed marks only,no daily decision or new fill,transfer,rebalancing,reset or forced exit. Next daily event2026-10-30UTC00:01;terminal2027-03-31 unchanged.','failure_criteria':'Stop on source hash,overlap,timestamp,closed-bar,cash/units/desired/cost/trades or exact NAV-prefix mismatch. Delayed real historical shadow,not live execution or paper10.','qualification':'Actual partial observation only;not mature180day/sixfold. Rejected partial does not cancel frozen plan.'}
 put(R/'forward_resume_plan.json',plan);batch=[];fps={}
 for row in json.loads((PREV/'forward_batch.json').read_text()):
  spec=copy.deepcopy(json.loads((ROOT/row['spec']).read_text()));spec['parameters']['end_utc']=cut;spec['validation_plan']=rel(R/'forward_resume_plan.json')
  if spec['kind']=='combination':spec['components']=[{'fingerprint':fps[a],'weight':w} for a,w in [('BTC',.75),('ETH',.25)]]
  path=R/'specs'/(row['name']+'.json');put(path,spec);current={**row,'spec':rel(path),'fingerprint':reg.fingerprint(spec)}
  if 'asset' in row:fps[row['asset']]=current['fingerprint']
  batch.append(current)
 put(R/'forward_batch.json',batch);done=[]
 for row in batch:done.append(call('reserve',row));put(R/'forward_reserve.json',done)
def finish():
 report=json.loads((R/'forward_report.json').read_text());assert report['cutoff_utc']=='2026-10-29T02:30:00Z';done=[]
 for row in json.loads((R/'forward_batch.json').read_text()):done.append(call('finish',row,'rejected',rel(R/'forward_report.json')));put(R/'forward_finish.json',done)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['reserve','finish']);globals()[p.parse_args().command]()
