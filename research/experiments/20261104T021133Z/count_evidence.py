import gzip,json
from common import *
p=json.loads((R/'plan.json').read_text());rep=json.loads((R/'report.json').read_text());v=json.loads((R/'verification.json').read_text());old={'curves':0,'funding_records':0,'filled_trade_records':0,'rejected_trade_records':0,'native_NAV_points':0,'new_policy_decisions':0}
for ref in p['read_only_references'].values():
 if ref['scope']!='native':continue
 arc=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()))
 for z in arc['scenes'].values():
  old['curves']+=1;old['funding_records']+=len(z['funding_events']);old['filled_trade_records']+=sum(x['status']=='filled' for x in z['trades']);old['rejected_trade_records']+=sum(x['status']=='rejected' for x in z['trades']);old['native_NAV_points']+=z['summary']['NAV_points']
assert old['curves']==39 and v['new_native_curves']==0 and v['new_parent_curves']==27 and v['independent_new_policy_decisions']==0
new={k:0 for k in old};parents={'curves':27,'new_NAV_points':sum(z['NAV_points'] for c in rep['configs'].values() for z in c['scenes'].values()),'new_parent_orders':0,'new_native_policy_or_order_evaluations':0}
put(R/'research_evidence_counts.json',{'old_readonly_native':old,'new_native':new,'new_parent':parents,'scope':'Existingnativeledger records are reusedauditcounts,not newtrades/funding.Only newportfolioNAV/metricsvaluedafterreserve.'});print(json.dumps({'old':old,'new':new,'parents':parents}),flush=True)
