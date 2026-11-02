"""Count already saved actual ledgers; new strength policy fields apply only to new archives."""
import gzip,json
from common import *
rep=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());out={}
for label,rows in [('new_native',[c for c in rep['configs'].values() if c['scope']=='native']),('old_readonly_native',[v for v in plan['read_only_references'].values() if v['scope']=='native'])]:
 count={'curves':0,'funding_records':0,'filled_trade_records':0,'rejected_trade_records':0,'native_NAV_points':0,'new_policy_decisions':0,'strength_entry_intents_screened':0,'entry_intents_suppressed':0}
 for c in rows:
  arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()))
  for s in arc['scenes'].values():
   count['curves']+=1;count['funding_records']+=len(s['funding_events']);count['filled_trade_records']+=sum(t['status']=='filled' for t in s['trades']);count['rejected_trade_records']+=sum(t['status']=='rejected' for t in s['trades']);count['native_NAV_points']+=s['summary']['NAV_points']
   if label=='new_native':
    for d in s['decisions']:
     a=d['policy_audit'];assert a['kind']=='ETH_gated_reversal_entry_vol_minimum_trend_strength' and a['minimum_absolute_slow_return_for_fresh_entry']==c['T'];count['new_policy_decisions']+=1
     if a['strength_filter_applied']:count['strength_entry_intents_screened']+=1;count['entry_intents_suppressed']+=int(a['desired_after_volatility_filter']!=0 and d['desired_direction']==0)
 out[label]=count
v=json.loads((R/'verification.json').read_text());assert sum(x['funding_records'] for x in out.values())==v['counts']['funding'] and sum(x['filled_trade_records'] for x in out.values())==v['counts']['fills'] and out['new_native']['new_policy_decisions']==6660
out.update(scope='New trend strength intent fields counted only on new archives. Actual funding cash records counted on both old/new; no funding signal used. Suppressed entry intents are not rejected exchange orders. Parent paths reuse source operations.',new_aligned_native_and_parent_union_NAV_points=v['new_NAV_points'],report_sha256=sha(R/'report.json'));put(R/'research_evidence_counts.json',out);print(json.dumps(out),flush=True)
