"""Readonlyoldholdcontrols:normalizeonlyexistingrecent40fieldnames/foldtimestamps,nevernewfinance."""
import copy,json
from datetime import datetime,timedelta,timezone
from run import ROOT,R,sha

def all_reference_configs():
 p=json.loads((R/'plan.json').read_text());out={}
 for x in p['benchmark_references'].values():
  assert sha(ROOT/x['report'])==x['report_sha256'];c=copy.deepcopy(json.loads((ROOT/x['report']).read_text())['configs'][x['name']]);c.update(scope=x['scope'],asset=x['asset'],role='benchmark',mode='hold',read_only_anchor=True,read_only_reference=True,report=x['report'],entry_vote_threshold=0,retention_vote_threshold=0)
  if x['scope']=='parent':c.update(raw_component_multipliers=[1,1])
  for s in c['scenes'].values():
   t=copy.deepcopy(s.get('recent40',s.get('extension40')));assert t is not None;t.setdefault('initial_NAV_usdt',t.get('start_NAV_usdt'));t.setdefault('final_NAV_usdt',t.get('end_NAV_usdt'))
   for f in t['folds']:
    f.setdefault('start_utc',(datetime(2026,9,14,0,1,tzinfo=timezone.utc)+timedelta(days=5*(f['fold']-1))).isoformat().replace('+00:00','Z'));f.setdefault('end_exclusive_utc',(datetime(2026,9,14,0,1,tzinfo=timezone.utc)+timedelta(days=5*f['fold'])).isoformat().replace('+00:00','Z'))
   s['recent40']=t
  out[c['name']]=c
 assert len(out)==3;return out

def old_ownership():return all_reference_configs()

def baselines(configs):
 refs=all_reference_configs();return {c['name']:{'same_capital_notional_constantlong':next(x for x in refs.values() if x['scope']==c['scope'] and x['asset']==c['asset'])} for c in configs.values() if c['role']=='candidate'}
