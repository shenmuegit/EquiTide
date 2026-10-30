import copy,json
from run import ROOT,R,sha

def all_reference_configs():
 p=json.loads((R/'plan.json').read_text());out={}
 for x in p['source_parent_references'].values():
  assert sha(ROOT/x['report'])==x['report_sha256'];c=copy.deepcopy(json.loads((ROOT/x['report']).read_text())['configs'][x['name']]);c.update(read_only_anchor=True,read_only_reference=True);out[c['name']]=c
 assert len(out)==10;return out

def old_ownership():return all_reference_configs()

def baselines(configs):
 allc=all_reference_configs();p=json.loads((R/'plan.json').read_text());fast=allc[p['source_parent_references']['fast']['name']];out={}
 for c in configs.values():
  if c['role']!='candidate':continue
  a,L,H=[c[x] for x in ['fast_ETH_bank_units','lookback_days','return_hurdle']];hold=next(z for z in configs.values() if z['mode']=='hold' and z['fast_ETH_bank_units']==a);slow=allc[p['source_parent_references'][f'L{L}_H{H}']['name']];out[c['name']]={'same_raw_units_constantlong':hold,'pure_fast_ownership_endpoint':fast,'pure_slow_ownership_endpoint':slow}
 return out
