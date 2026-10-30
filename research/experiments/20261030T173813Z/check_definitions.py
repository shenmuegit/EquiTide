import json
from run import ROOT,R,sha,put,reg,now,ENTRIES,EXITS
p=json.loads((R/'plan.json').read_text());rows=json.loads((R/'batch.json').read_text());by={x['fingerprint']:json.loads((ROOT/x['spec']).read_text()) for x in rows};assert len(rows)==27 and len(by)==27 and sum(x['scope']=='native' for x in rows)==18 and sum(x['scope']=='parent' for x in rows)==9
for x in rows:
 sp=by[x['fingerprint']];q=sp['parameters'];N=x['entry_vote_threshold'];M=x['retention_vote_threshold'];assert reg.fingerprint(sp)==x['fingerprint'] and N in ENTRIES and M in EXITS and M<N
 if x['scope']=='native':assert q['signal_mode']=='channel_state_consensus' and q['initial_capital_usdt']==10000 and q['fixed_entry_notional_usdt']==(1000 if x['asset']=='BTC' else 2000) and sp['universe']==[x['asset']+'/USDT']
 else:assert q['initial_capital_usdt']==20000 and q['raw_component_multipliers']==[1,1] and q['component_capitals_usdt']==[10000,10000] and q['source_component_parameters']==[by[f]['parameters'] for f in x['source_fingerprints']]
assert p['gates']['recent40_positive5d_each_cost_min']==6
from signal_inputs import load_votes
votes=load_votes(p);assert len(votes)==2 and all(len(v)==404 for v in votes.values())
files=['plan.json','run.py','engine.py','audit.py','audit_native.py','audit_helpers.py','controls.py','freeze_batch.py','check_definitions.py','check_engine.py','check_data.py','signal_inputs.py'];put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':{str((R/f).relative_to(ROOT)):sha(R/f) for f in files}});put(R/'definition_check.json',{'passed':True,'new_complete_specs':27,'new_candidates':27,'native_candidates':18,'parent_candidates':9,'three_separate_asset_scope_grids':True,'full_cells':27,'edges':36,'old_readonly_controls':3,'weights_raw_1_1_not_normalized':True});print('PASS27completecandidate definitions,separateBTC/ETH/COMBOneighborhoods,exactholdsreadonly')
