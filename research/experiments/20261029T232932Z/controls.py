"""Read immutable center ownership controls only;newactualscale references live in report."""
import copy,json
from run import ROOT,R,sha

def old_ownership():
 out={}
 for key,x in json.loads((R/'anchors.json').read_text()).items():
  assert sha(ROOT/x['report'])==x['report_sha256'];c=copy.deepcopy(json.loads((ROOT/x['report']).read_text())['configs'][x['name']]);c.update(scope='parent',asset='COMBO',role='benchmark',mode='ownership',capital_usdt=20000,BTC_capital_fraction=.25,read_only_anchor=True);out[.25,float(key)]=c
 assert len(out)==3;return out

def matched(configs):
 own=old_ownership();own.update({(c['BTC_capital_fraction'],c['entry_funding_cost_cap_per_settlement']):c for c in configs.values() if c['mode']=='ownership'});ungated={(c['scope'],c['BTC_capital_fraction']):c for c in configs.values() if c['mode']=='ungated'};hold={(c['scope'],c['asset'],c['BTC_capital_fraction']):c for c in configs.values() if c['mode']=='hold'};assert len(own)==9 and len(ungated)==6 and len(hold)==9;return own,ungated,hold
