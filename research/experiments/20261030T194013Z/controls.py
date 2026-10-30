import copy,json
from datetime import datetime,timedelta,timezone
from common import ROOT,R,sha

def reference():
 p=json.loads((R/'plan.json').read_text());x=next(x for x in p['read_only_references'].values() if x['scope']=='parent');assert sha(ROOT/x['report'])==x['report_sha256'];c=copy.deepcopy(json.loads((ROOT/x['report']).read_text())['configs'][x['name']]);c.update(scope='reference',role='benchmark',entry_z=None,exit_z=None,read_only_reference=True,report=x['report'])
 for s in c['scenes'].values():
  t=copy.deepcopy(s.get('recent40',s.get('extension40')));t.setdefault('initial_NAV_usdt',t.get('start_NAV_usdt'));t.setdefault('final_NAV_usdt',t.get('end_NAV_usdt'))
  for f in t['folds']:
   f.setdefault('start_utc',(datetime(2026,9,14,0,1,tzinfo=timezone.utc)+timedelta(days=5*(f['fold']-1))).isoformat().replace('+00:00','Z'));f.setdefault('end_exclusive_utc',(datetime(2026,9,14,0,1,tzinfo=timezone.utc)+timedelta(days=5*f['fold'])).isoformat().replace('+00:00','Z'))
  s['recent40']=t
 return c
