"""Count only saved readonly actual source ledgers, no new native valuation."""
import gzip,json
from common import *
rep=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());count={'curves':0,'funding_records':0,'filled_trade_records':0,'rejected_trade_records':0,'native_NAV_points':0,'new_policy_decisions':0}
for ref in plan['read_only_references'].values():
 if ref['scope']!='native':continue
 arc=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()))
 for s in arc['scenes'].values():
  count['curves']+=1;count['funding_records']+=len(s['funding_events']);count['filled_trade_records']+=sum(t['status']=='filled' for t in s['trades']);count['rejected_trade_records']+=sum(t['status']=='rejected' for t in s['trades']);count['native_NAV_points']+=s['summary']['NAV_points']
v=json.loads((R/'verification.json').read_text());assert count['curves']==36 and count['funding_records']==v['counts']['funding'] and count['filled_trade_records']==v['counts']['fills'] and v['new_native_curves']==v['independent_new_policy_decisions']==0
put(R/'research_evidence_counts.json',{'old_readonly_native':count,'new_native':{'curves':0,'funding_records':0,'filled_trade_records':0,'new_policy_decisions':0},'new_parent_cost_curves':18,'new_aligned_parent_NAV_points':v['new_NAV_points'],'report_sha256':sha(R/'report.json'),'scope':'Source operations are old actual ledgers,not fresh executions. New work only evaluates 6new fullbank combinations/18cost paths.'});print(json.dumps(count),flush=True)
