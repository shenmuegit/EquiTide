import copy,json
from run import ROOT,R,sha,grid_configs

def all_reference_configs():
 p=json.loads((R/'plan.json').read_text());out={}
 for x in p['source_parent_references'].values():
  assert sha(ROOT/x['report'])==x['report_sha256'];c=copy.deepcopy(json.loads((ROOT/x['report']).read_text())['configs'][x['name']]);c.update(read_only_anchor=True,read_only_reference=True);out[c['name']]=c
 assert len(out)==2;return out

def old_ownership():return all_reference_configs()

def baselines(configs):
 p=json.loads((R/'plan.json').read_text());allc=all_reference_configs();center=allc[p['source_parent_references']['center']['name']];hold=allc[p['source_parent_references']['hold']['name']];return {c['name']:{'same_raw_units_constantlong':hold,'read_only_prespecified_center':center} for c in grid_configs(configs).values()}
