"""Readonly operation counts; funding-feature schema belongs only to new native models."""
import gzip,json
from common import *
rep=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());out={}
for label,rows in [('new_native',[c for c in rep['configs'].values() if c['scope']=='native']),('old_readonly_native',[v for v in plan['read_only_references'].values() if v['scope']=='native'])]:
 count={'curves':0,'funding_records':0,'filled_trade_records':0,'rejected_trade_records':0,'native_NAV_points':0,'funding_feature_citations':0,'funding_entry_intents_screened':0,'entry_intents_suppressed':0}
 for c in rows:
  arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()))
  for s in arc['scenes'].values():
   count['curves']+=1;count['funding_records']+=len(s['funding_events']);count['filled_trade_records']+=sum(t['status']=='filled' for t in s['trades']);count['rejected_trade_records']+=sum(t['status']=='rejected' for t in s['trades']);count['native_NAV_points']+=s['summary']['NAV_points']
   if label=='new_native':
    for d in s['decisions']:
     a=d['policy_audit'];assert a['funding_signal'] is not None and a['funding_signal']['available_ts']+3600000000000<=d['signal_available_ts_ns'];count['funding_feature_citations']+=1
     if a['funding_entry_filter_applied']:count['funding_entry_intents_screened']+=1;count['entry_intents_suppressed']+=int(a['desired_after_volatility_filter']!=0 and d['desired_direction']==0)
 out[label]=count
v=json.loads((R/'verification.json').read_text());assert sum(x['funding_records'] for x in out.values())==v['counts']['funding'] and sum(x['filled_trade_records'] for x in out.values())==v['counts']['fills'];assert out['new_native']['funding_feature_citations']==6660
out.update(scope='New funding feature citations counted only on new archives; old archive decisions use earlier schemas. Suppressed rule intents are not exchange order rejections; parent operations reuse native records.',new_aligned_native_and_parent_union_NAV_points=v['new_NAV_points'],report_sha256=sha(R/'report.json'));put(R/'research_evidence_counts.json',out);print(json.dumps(out),flush=True)
