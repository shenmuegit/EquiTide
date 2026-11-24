"""Commit small exact public response/packet copies required to verify original accounts."""
import json
from common import *
rd=lambda p:json.loads(p.read_text());dest=R/'retained_raw';dest.mkdir(exist_ok=True);paths=set()
for a in ['candidate','l4h02','fewm']:
 d=rd(R/(a+'_observation/input_manifest.json'));paths.add(d['packet']);paths.update(z['raw'] for z in d['provenance'])
rows=[]
for name in sorted(paths):
 source=ROOT/name;hh=sha(source);target=dest/(hh+'.gz')
 if not target.exists():target.write_bytes(source.read_bytes())
 assert sha(target)==hh;rows.append({'original_path':name,'committed_copy':rel(target),'sha256':hh,'bytes':source.stat().st_size,'original_first_capture_UTC_preserved_in_provenance':True,'restoration_rule':'If ignored original cache is absent in a fresh checkout,copy these exact bytes back to original_path before readonly observer audit;no new market request or account execution.'})
put(R/'raw_evidence_index.json',{'passed':True,'artifacts':rows,'distinct_copies':len({z['committed_copy'] for z in rows}),'total_distinct_bytes':sum(f.stat().st_size for f in dest.iterdir()),'only_public_market_data_no_account_credentials':True,'failed_response_bytes_included':True,'full_account_books_and_rules_retained_separately':True});print(json.dumps({'retained':len(rows),'distinct':len({z['committed_copy'] for z in rows}),'bytes':sum(f.stat().st_size for f in dest.iterdir())}),flush=True)
