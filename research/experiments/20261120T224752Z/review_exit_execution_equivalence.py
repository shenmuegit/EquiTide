"""Read saved decisions/trades only; explain threshold plateaus without executing any model."""
import gzip,hashlib,json
from fractions import Fraction as F
from common import ROOT,R,sha,put,rel,now
rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));report=rd(R/'report.json');plan=rd(R/'plan.json');before=sha(R/'report.json');refs=report['read_only_configs'];rows=[]
for c in report['configs'].values():
 if c['scope']!='native':continue
 baseline=refs[next(z['fingerprint'] for z in plan['native_grid'] if z['W']==.0075 and z['K']==c['K'])];new=gz(ROOT/c['archive']);old=gz(ROOT/baseline['archive']);costs={}
 for k,scene in new['scenes'].items():
  previous=old['scenes'][k];held=[d for d in scene['decisions'] if F(d['state_before']['signed_units'])>0];inside=[d for d in held if F('.00625')<=F(d['policy_audit']['return_exact'])<F('.00875')]
  action=lambda x:[(d['signal_available_ts_ns'],d['desired_direction'],F(d['state_before']['signed_units'])) for d in x['decisions']]
  same_actions=action(scene)==action(previous);same_nav=c['scenes'][k]['NAV_sha256_f64le']==baseline['scenes'][k]['NAV_sha256_f64le'];costs[k]={'saved_decisions':len(scene['decisions']),'executed_long_held_at_decision':len(held),'held_decisions_inside_differentiating_E_interval':len(inside),'differentiating_interval_closed_open':['.00625','.00875'],'actual_desired_and_held_q_sequence_equals_old_E0p0075':same_actions,'complete_NAV_equals_old_E0p0075':same_nav,'actual_filled_closes':sum(not t['opening'] and t['status']=='filled' for t in scene['trades'])}
  assert len(scene['decisions'])==391 and same_actions and same_nav and not inside
 rows.append({'fingerprint':c['fingerprint'],'E':c['W'],'M':c['K'],'matched_actual_center_fingerprint':baseline['fingerprint'],'actual_center_report':plan['read_only_references'][baseline['fingerprint']]['report'],'by_cost':costs})
assert sha(R/'report.json')==before
put(R/'exit_execution_equivalence_review.json',{'passed':True,'recorded_utc':now(),'source':'Saved actual decisions/trades and registered old matched E.0075 cost-scene archives only','rows':rows,'new_native_models_reviewed':len(rows),'all7038_saved_new_decisions_compared':sum(v['saved_decisions'] for r in rows for v in r['by_cost'].values()),'held_decisions_inside_differentiating_E_interval':sum(v['held_decisions_inside_differentiating_E_interval'] for r in rows for v in r['by_cost'].values()),'finding':'No actual held-long decision has5dayROC in[.00625,.00875);therefore these preregistered thresholds produce identical realized actions/NAV for eachM. Structural threshold unit tests did distinguish them on synthetic boundary cases. This is not independent alpha evidence.','financial_report_sha256_unchanged':before,'no_new_reserve_or_strategy_account_market_execution':True});print(json.dumps({'passed':True,'actual_saved_new_decisions_compared':sum(v['saved_decisions'] for r in rows for v in r['by_cost'].values()),'actual_differentiating_held_cases':sum(v['held_decisions_inside_differentiating_E_interval'] for r in rows for v in r['by_cost'].values()),'report_unchanged':True}))
