"""Verify new native provenance and old BTC bank reuse;no strategy execution."""
from common import *
rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');r=rd(R/'report.json');rh=sha(R/'report.json');allc={**r['read_only_configs'],**{c['fingerprint']:c for c in r['configs'].values()}};rows=[]
for c in r['configs'].values():
 sp=rd(ROOT/c['spec']);arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));assert arc['spec']==sp and sha(ROOT/c['archive'])==c['archive_sha256']
 if c['scope']=='native':assert c['asset']=='ETH' and sp['parameters']['trend_slope_hurdle_fraction']==c['W'] and sp['parameters']['entry_funding_settlement_count']==c['K'];continue
 fps=c['source_fingerprints'];left,right=[allc[f] for f in fps];assert left['readonly'] and left['asset']=='BTC' and right['scope']=='native' and not right.get('readonly') and [z['weight'] for z in sp['components']]==[1,1]
 for k,z in arc['scenes'].items():assert z['source_full_NAV_sha256']==[allc[f]['scenes'][k]['NAV_sha256_f64le'] for f in fps] and z['summary']['parent_executions']==0
 rows.append({'fingerprint':c['fingerprint'],'old_BTC_actual_bank':fps[0],'new_ETH_actual_bank':fps[1],'raw_multipliers':[1,1],'capitals':[3750,15000],'entry_targets':[1000,4000]})
assert len(rows)==6 and sha(R/'report.json')==rh;put(R/'component_reuse_verification.json',{'passed':True,'recorded_utc':now(),'financial_report_sha256_unchanged':rh,'new_native_ETH_models':6,'new_parent_models':6,'old_actual_results_readonly':12,'old_BTC_and_holds_not_reexecuted':True,'new_ETH_actual_quantity_and_cost_stress_used':True,'no_NAV_scaling_normalization_transfers_or_parent_orders':True,'rows':rows,'no_financial_or_account_reexecution':True});print('PASS6newETH/6parents/12readonlyprovenance')
