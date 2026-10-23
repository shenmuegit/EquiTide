"""Confirm old anchors are read-only, new exact definitions differ, and context covers L30."""
import json
from run import ROOT,R,LOOKS,HURDLES,reg,sha,anchor_configs
import engine

def main():
 plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());refs=json.loads((R/'anchors.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');anchors=anchor_configs();assert len(batch)==12 and len(refs)==6 and LOOKS==[20,25,30] and engine.START-1-max(LOOKS)==2
 assert sha(R/'engine.py')==plan['anchor_source']['engine_sha256'];assert not ({x['fingerprint'] for x in batch}&{x['fingerprint'] for x in refs.values()})
 for x in batch:
  s=json.loads((ROOT/x['spec']).read_text());assert reg.fingerprint(s)==x['fingerprint'] and s['parameters']['lookback_days'] in [25,30] and records[x['fingerprint']]['status']=='reserved'
  a=anchors[f"perp_zeroexit_{x['asset']}_L20_H{int(x['return_hurdle']*100):02d}"];old=json.loads((ROOT/a['spec']).read_text());newp=dict(s['parameters']);newp['lookback_days']=20;assert newp==old['parameters'] and s['logic']==old['logic'] and s['family']==old['family']
 for ref in refs.values():
  rec=records[ref['fingerprint']];assert rec['result_available'] and rec['status']==ref['original_status']=='rejected' and rec['report_sha256']==ref['source_report_sha256'];assert sha(ROOT/ref['source_archive'])==ref['source_archive_sha256'] and sha(ROOT/ref['source_spec'])==ref['source_spec_sha256']
 for L,H,expected in [(25,.02,9),(25,.01,6),(30,.02,6),(30,.04,4)]:
  cells=[(x,y) for x in LOOKS for y in HURDLES if abs(LOOKS.index(x)-LOOKS.index(L))<=1 and abs(HURDLES.index(y)-HURDLES.index(H))<=1];assert len(cells)==expected
 print('PASS:12newexactlookbackdefinitions,6oldanchorsnotreserved,reusedengine/costs/period/capital,nonnegative30daycontext,2Dneighborcounts;no oldNAV or qualification recalculated')

if __name__=='__main__':main()
