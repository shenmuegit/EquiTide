"""Read saved ledgers; only new policy archives expose varied volatility-cap evidence."""
import gzip,json
from common import *
rep=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());out={}
for label,rows in [('new_native',[c for c in rep['configs'].values() if c['scope']=='native']),('old_readonly_native',[v for v in plan['read_only_references'].values() if v['scope']=='native'])]:
 count={'curves':0,'funding_records':0,'filled_trade_records':0,'rejected_trade_records':0,'native_NAV_points':0,'new_policy_decisions':0,'desired_long_decisions':0,'desired_short_decisions':0,'desired_flat_decisions':0}
 for c in rows:
  arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()))
  for s in arc['scenes'].values():
   count['curves']+=1;count['funding_records']+=len(s['funding_events']);count['filled_trade_records']+=sum(t['status']=='filled' for t in s['trades']);count['rejected_trade_records']+=sum(t['status']=='rejected' for t in s['trades']);count['native_NAV_points']+=s['summary']['NAV_points']
   if label=='new_native':
    for d in s['decisions']:
     a=d['policy_audit'];assert a['kind']=='ETH_gated_reversal_entry_vol_asymmetric_long_hurdle' and a['long_entry_return_hurdle']==.015 and a['short_entry_return_hurdle']==.025 and a['entry_volatility_ceiling']==.045 and a['volatility_window_days']==10 and a['exit_buffer_fraction']==.005 and a['slow_lookback_days']==c['S'];count['new_policy_decisions']+=1;count[{-1:'desired_short_decisions',0:'desired_flat_decisions',1:'desired_long_decisions'}[d['desired_direction']]]+=1
 out[label]=count
v=json.loads((R/'verification.json').read_text());assert sum(x['funding_records'] for x in out.values())==v['counts']['funding'] and sum(x['filled_trade_records'] for x in out.values())==v['counts']['fills'] and out['new_native']['new_policy_decisions']==6660
out.update(scope='Thresholds/direction decisions verified only on new archives. Desired direction counts are not fill/order counts. Old fields left unchanged, actual funding/cost records counted separately; parents reuse source operations.',new_aligned_native_and_parent_union_NAV_points=v['new_NAV_points'],report_sha256=sha(R/'report.json'));put(R/'research_evidence_counts.json',out);print(json.dumps(out),flush=True)
