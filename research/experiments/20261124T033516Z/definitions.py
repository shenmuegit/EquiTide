"""Bind each full new definition,actual native source and original account before reserve."""
import ast,json
from common import *
rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');batch=rd(R/'batch.json');rs=reg.read_records(ROOT/'research/automation/registry.jsonl');P=ROOT/'research/experiments/20261124T013414Z';assert len(batch)==4 and len(p['read_only_references'])==14 and len(p['grid'])==9 and not p['native_grid']
for n in ['engine.py','core391_tail_safe.py','market.py','portfolio.py','audit_native.py','observe_l4h02.py','observe_fewm.py','audit_incremental.py']:assert sha(R/n)==sha(P/n)
for row in batch:
 sp=rd(ROOT/row['spec']);q=sp['parameters'];assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[1000,4000] and q['initial_capital_usdt']==18750 and [x['weight'] for x in sp['components']]==[1,1] and q['continuous_oos_days']==391
 assert q['BTC_entry_volatility_ceiling']==row['W'] in [.026125,.028875] and q['ETH_entry_funding_volatility_ratio']==row['K'] in [.00625,.00875] and q['ETH_entry_funding_max_age_hours']==36 and q['ETH_entry_funding_settlement_count']==4 and q['ETH_entry_funding_volatility_ratio'] in [.00625,.00875] and q['BTC_entry_notional_usdt']==1000 and q['ETH_entry_notional_usdt']==4000
 for asset,fp in zip(['BTC','ETH'],row['source_fingerprints']):
  child=rs[fp]['spec']['parameters'];assert rs[fp]['result_available']
  for k,v in q.items():
   if k.startswith(asset+'_') and k[len(asset)+1:] in child:assert v==child[k[len(asset)+1:]],k
for fp,z in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['report_sha256']==z['report_sha256']
 for k in ['spec','report','archive']:assert sha(ROOT/z[k])==z[k+'_sha256']
a=rd(R/'original_accounts_binding.json');assert all(sha(ROOT/z)==h for z,h in a['sources_sha256'].items());assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='simulate' for n in ast.walk(ast.parse((R/'run.py').read_text())))
source={rel(f):sha(f) for f in R.glob('*.py')};names=['startup.json','context.json','plan.json','spec.json','batch.json','account_windows.json','original_accounts_binding.json','SMA_full75_prebinding.json','SMA_markonly_kernel_identity.json','l4h02_resume_plan.json','research_design.json','primary_source_access.json','window_funding_preflight.json','registry_archive_plan.json','budget_ratio_metadata_availability.json','actual08_nov23_prebinding_source.json'];imm={rel(R/n):sha(R/n) for n in names};imm.update({x['spec']:sha(ROOT/x['spec']) for x in batch});imm.update(a['sources_sha256']);put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':imm,'new_native_models':0,'new_parent_models':4,'no_new_financial_calculation_yet':True,'raw_weights_not_normalized':True,'actual08_firstsource_rebound_before_any_reserve':True});put(R/'definition_check.json',{'passed':True,'new_configs':4,'read_only_refs':14,'new_native_models':0,'source_metadata_checked':True,'full_graph_index_verified_before_reserve':True,'all_source_reports_archives_spec_and_account_hashes_bound':True});print('PASS4newgraphs/14actualrefs/0newnative/fullsourceandown08binding')
