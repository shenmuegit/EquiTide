"""Project three already reserved/finished real observations into a publication index; no finance."""
import json
from run import ROOT,R,reg,sha,put,rel
W=R/'candidate_observation';report=json.loads((W/'report.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert not(R/'candidate_batch.json').exists();rows=[]
for asset in ['BTC','ETH','COMBO']:
 path=W/(asset+'_spec.json');sp=json.loads(path.read_text());fp=reg.fingerprint(sp);name='forward_snapshot_candidate_'+asset;assert fp==report['configs'][name]['fingerprint'] and records[fp]['status']=='rejected' and records[fp]['result_available'] is True and records[fp]['report_sha256']==sha(W/'report.json');rows.append({'name':name,'fingerprint':fp,'spec':rel(path),'report':rel(W/'report.json')})
put(R/'candidate_batch.json',rows);print('PASS:projected3 existingactual observationIDs;no reservation,calculation,account orreportwrite.')
