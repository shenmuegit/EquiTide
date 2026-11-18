"""Readonly verification of the append-only runtime-note correction; no backtest."""
import gzip,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=ROOT/'research/experiments/20261118T122939Z'
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
e=rd(Path(__file__).with_suffix('.json'));m=rd(R/'data_manifest.json');old=rd(R/'runtime_note.json');aw=rd(R/'account_window_verification.json');v=rd(R/'candidate_verification.json')
for p,h in e['source_sha256'].items():assert sha(ROOT/p)==h,p
for p,h in m['artifacts'].items():assert sha(ROOT/p)==h,p
d=json.loads(gzip.decompress((R/'candidate_observation/delta.json.gz').read_bytes()));tr=[z for z in d['journal'] if z['kind']=='trade' and z['status']=='filled']
assert old['current_original_new_fills']['candidate']==0 and e['original_value']==old['current_original_new_fills']
assert e['corrected_value']==aw['current_fills_by_account']=={'SMA':0,'candidate':3,'l4h02':0,'fewm':0}
assert tr==e['actual_filled_trades'] and len(tr)==v['new_fills']==3 and {z['cost_multiplier'] for z in tr}=={1,2,3}
assert all(z['asset']=='ETH' and z['opening'] and z['side']=='sell' and z['timestamp_ns']==1794960060000000000 for z in tr)
state=rd(R/'candidate_observation/state.json');assert all(state['books']['ETH'][k]['signed_units']=='-1.644000000000000000' for k in ['1','2','3'])
assert rd(R/'next_research_state.json')['UTC_midnight_handoff']['current_fills_by_account']==e['corrected_value']
assert e['financial_models_or_observation_windows_rerun']==0 and e['original_seal_kept_immutable']
print(json.dumps({'passed':True,'original_sealed_artifacts_unchanged':len(m['artifacts']),'actual_candidate_fills':3,'economic_actions':1,'cost_scenes':[1,2,3],'ETH_signed_units_per_scene':'-1.644000000000000000','new_financial_or_account_calculations':0}))
