"""Read-only exact center and samecapital baseline references;no source simulations."""
import copy,json
from run import ROOT,R,sha

def all_reference_configs():
 out={}
 for x in json.loads((R/'plan.json').read_text())['all_read_only_references'].values():
  assert sha(ROOT/x['report'])==x['report_sha256'];c=copy.deepcopy(json.loads((ROOT/x['report']).read_text())['configs'][x['name']]);params=json.loads((ROOT/x['spec']).read_text())['parameters'];params=params['source_component_parameters'][1] if c['scope']=='parent' else params;c.update(read_only_anchor=True,read_only_reference=True,lookback_days=params.get('lookback_days'),return_hurdle=params.get('return_hurdle'),trend_lookback_days=params.get('trend_lookback_days'));out[c['name']]=c
 assert len(out)==8;return out

def old_ownership():
 # Compatibility for exported-value verifier;these are native-capital references,no ownership transformation.
 return all_reference_configs()

def baselines(configs):
 p=json.loads((R/'plan.json').read_text());allc=all_reference_configs();holds={c['scope']:c for c in configs.values() if c['mode']=='hold'};assert len(holds)==2
 return {scope:{'old_contrarian_N4500_different_exposure':allc[p['read_only_grid_references'][scope]['name']],'old_ungated_contrarian_N4500_different_exposure':allc[p['read_only_ungated_references'][scope]['name']],'matched_actual_notional_constantlong':holds[scope]} for scope in ['native','parent']}
