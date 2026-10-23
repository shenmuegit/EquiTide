"""Real-source identity and longest causal lookback guard;no historical rerun."""
import json
from run import ROOT,R,LOOKS,HURDLES,reg,sha,anchor_configs
import engine

def main():
 p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());refs=json.loads((R/'anchors.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');anchors=anchor_configs();assert len(batch)==6 and len(refs)==3 and LOOKS==[30,31,32] and engine.START-1-max(LOOKS)==0 and engine.START-1-33<0
 assert sha(R/'engine.py')==p['anchor_source']['engine_sha256'] and set(p['data']['assets'])=={'ETH'};assert not ({x['fingerprint'] for x in batch}&{x['fingerprint'] for x in refs.values()})
 for row in batch:
  s=json.loads((ROOT/row['spec']).read_text());assert reg.fingerprint(s)==row['fingerprint'] and s['parameters']['lookback_days'] in [31,32] and records[row['fingerprint']]['status']=='reserved';a=anchors[f"perp_zeroexit_ETH_L30_H{int(row['return_hurdle']*100):02d}"];old=json.loads((ROOT/a['spec']).read_text());q=dict(s['parameters']);q['lookback_days']=30;assert q==old['parameters'] and s['logic']==old['logic'] and s['family']==old['family']
 for ref in refs.values():
  rec=records[ref['fingerprint']];assert rec['status']==ref['original_status'] and rec['report_sha256']==ref['source_report_sha256'] and sha(ROOT/ref['source_archive'])==ref['source_archive_sha256']
 parent=p['read_only_parent_context'];doc=json.loads((ROOT/parent['report']).read_text());assert sha(ROOT/parent['report'])==parent['report_sha256'] and parent['qualified_names']==doc['summary']['passed'] and len(parent['qualified_names'])==7
 for name in parent['qualified_names']:assert records[doc['configs'][name]['fingerprint']]['status']=='passed'
 print('PASS:6newETH31/32specs,3oldETH30anchors,unchangedcosts/capital/period/rules,33daycontextpermits32butnot33,old7parentqualificationsreadonly')

if __name__=='__main__':main()
