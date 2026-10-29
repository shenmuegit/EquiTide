"""Read only original ungated/constant-long controls;copy metadata,never alter source files."""
import copy,json
from datetime import datetime,timedelta,timezone
from run import ROOT,R,sha

def load_controls():
 refs={**{'nogate_'+k:x for k,x in json.loads((R/'anchors.json').read_text()).items()},**{'hold_'+k:x for k,x in json.loads((R/'holds.json').read_text()).items()}};out={}
 for key,x in refs.items():
  assert sha(ROOT/x['report'])==x['report_sha256'];c=copy.deepcopy(json.loads((ROOT/x['report']).read_text())['configs'][x['name']]);assert c['fingerprint']==x['fingerprint'] and c['status']==x['original_status'];c.update(scope=x['scope'],role=x['role'],capital_usdt=x['capital_usdt'],read_only_anchor=True)
  for z in c['scenes'].values():
   if 'recent40' not in z:z['recent40']=copy.deepcopy(z['extension40'])
   for f in z['recent40']['folds']:
    f.setdefault('start_utc',(datetime(2026,9,14,0,1,tzinfo=timezone.utc)+timedelta(days=5*(f['fold']-1))).isoformat().replace('+00:00','Z'));f.setdefault('end_exclusive_utc',(datetime(2026,9,14,0,1,tzinfo=timezone.utc)+timedelta(days=5*f['fold'])).isoformat().replace('+00:00','Z'))
  out[key]=c
 assert len(out)==4;return out
