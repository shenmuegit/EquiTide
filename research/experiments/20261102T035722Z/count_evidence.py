"""Read saved ledgers only; distinguish expiry flags from changed policy intents and real fills."""
import gzip,json
from common import *
rep=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());out={}
for label,rows in [('new_native',[c for c in rep['configs'].values() if c['scope']=='native']),('old_readonly_native',[v for v in plan['read_only_references'].values() if v['scope']=='native'])]:
 count={'curves':0,'funding_records':0,'filled_trade_records':0,'rejected_trade_records':0,'native_NAV_points':0,'new_policy_decisions':0,'expiry_decisions':0,'expiry_desired_direction_changed':0,'maximum_verified_open_age_days':0}
 for c in rows:
  arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()))
  for s in arc['scenes'].values():
   count['curves']+=1;count['funding_records']+=len(s['funding_events']);count['filled_trade_records']+=sum(t['status']=='filled' for t in s['trades']);count['rejected_trade_records']+=sum(t['status']=='rejected' for t in s['trades']);count['native_NAV_points']+=s['summary']['NAV_points']
   if label=='new_native':
    for d in s['decisions']:
     a=d['policy_audit'];assert a['kind']=='ETH_gated_reversal_entry_vol_holding_limit' and a['max_holding_days']==c['D'];count['new_policy_decisions']+=1
     if a['held_age_days'] is not None:assert 0<=a['held_age_days']<=c['D'];count['maximum_verified_open_age_days']=max(count['maximum_verified_open_age_days'],a['held_age_days'])
     if a['holding_limit_applied']:count['expiry_decisions']+=1;count['expiry_desired_direction_changed']+=int(a['desired_before_holding_limit']!=d['desired_direction']);assert d['desired_direction']==0
 out[label]=count
v=json.loads((R/'verification.json').read_text());assert sum(x['funding_records'] for x in out.values())==v['counts']['funding'] and sum(x['filled_trade_records'] for x in out.values())==v['counts']['fills'] and out['new_native']['new_policy_decisions']==6660
out.update(scope='Age/expiry fields counted only on new archives; independent audit derives entryday from actual filled trades. Expiry may coincide with a normal exit, so flag count is separate from changed desired. No expiry is an exchange rejection. Parents reuse source operations.',new_aligned_native_and_parent_union_NAV_points=v['new_NAV_points'],report_sha256=sha(R/'report.json'));put(R/'research_evidence_counts.json',out);print(json.dumps(out),flush=True)
