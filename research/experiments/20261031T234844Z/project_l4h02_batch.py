"""Index three completed actual first-window IDs; no new reservation or calculation."""
import json
from common import *
w=R/'l4h02_observation';rep=json.loads((w/'report.json').read_text());rec=reg.read_records(ROOT/'research/automation/registry.jsonl');batch=[]
for a in ['BTC','ETH','COMBO']:
 p=w/(a+'_spec.json');s=json.loads(p.read_text());fp=reg.fingerprint(s);name='forward_snapshot_l4h02_'+a;c=rep['configs'][name];z=rec[fp];assert z['result_available'] and z['status']==c['status'] and z['report_sha256']==sha(w/'report.json');batch.append({'name':name,'fingerprint':fp,'spec':rel(p),'asset':a,'capital_usdt':s['parameters']['initial_capital_usdt']})
put(R/'l4h02_batch.json',batch);print('PASS3 first-window L4H2 actual finished IDs indexed, zero new evaluation')
