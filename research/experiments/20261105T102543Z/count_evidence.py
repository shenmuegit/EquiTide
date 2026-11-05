"""Count actual saved native ledgers; distinguish old replay from newly simulated sources."""
import gzip,json
from common import *
rep=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text())
def count(archives):
 out={'curves':0,'funding_records':0,'filled_trade_records':0,'rejected_trade_records':0,'native_NAV_points':0,'new_policy_decisions':0}
 for path,isnew in archives:
  arc=json.loads(gzip.decompress((ROOT/path).read_bytes()))
  for s in arc['scenes'].values():
   out['curves']+=1;out['funding_records']+=len(s['funding_events']);out['filled_trade_records']+=sum(t['status']=='filled' for t in s['trades']);out['rejected_trade_records']+=sum(t['status']=='rejected' for t in s['trades']);out['native_NAV_points']+=s['summary']['NAV_points'];out['new_policy_decisions']+=len(s['decisions']) if isnew else 0
 return out
old=count([(x['archive'],False) for x in plan['read_only_references'].values() if x['scope']=='native']);new=count([(x['archive'],True) for x in rep['configs'].values() if x['scope']=='native']);v=json.loads((R/'verification.json').read_text());assert old['curves']==39 and new['curves']==0 and new['new_policy_decisions']==0==v['independent_new_policy_decisions']
for a,b in [('funding_records','funding'),('filled_trade_records','fills'),('rejected_trade_records','rejects')]:assert old[a]+new[a]==v['counts'][b]
parents=[x for x in rep['configs'].values() if x['scope']=='parent'];assert len(parents)==9
put(R/'research_evidence_counts.json',{'old_readonly_native':old,'new_native':new,'new_parent_cost_curves':27,'new_aligned_parent_NAV_points':sum(s['NAV_points'] for x in parents for s in x['scenes'].values()),'report_sha256':sha(R/'report.json'),'scope':'Old39costledgers replayedreadonly;zero native simulations,twentysevennewparentpaths valued. No parent orders or old-source policy rerun.'});print(json.dumps({'old':old,'new':new}),flush=True)
