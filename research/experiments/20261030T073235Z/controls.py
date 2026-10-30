import copy,json
from run import ROOT,R,sha

def all_reference_configs():
 p=json.loads((R/'plan.json').read_text());out={}
 for x in p['source_parent_references'].values():
  assert sha(ROOT/x['report'])==x['report_sha256'];c=copy.deepcopy(json.loads((ROOT/x['report']).read_text())['configs'][x['name']]);c.update(read_only_anchor=True,read_only_reference=True);out[c['name']]=c
 assert len(out)==30;return out

def old_ownership():return all_reference_configs()

def baselines(configs):
 old=all_reference_configs();out={}
 for c in configs.values():
  if c['role']!='candidate':continue
  a,L,H=[c[x] for x in ['fast_ETH_bank_units','lookback_days','return_hurdle']];hold=next(z for z in configs.values() if z['scope']=='parent' and z['mode']=='hold' and z['fast_ETH_bank_units']==a);prior=next(z for z in old.values() if z['role']=='candidate' and z['fast_ETH_bank_units']==a and z['lookback_days']==L and z['return_hurdle']==H);out[c['name']]={'same_raw_units_constantlong':hold,'matching_previous_ownership_index':prior}
 return out
