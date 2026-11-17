"""Compare saved all-cost paths with all already-tested total-risk cap banks and existing parents."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
rd=lambda p:json.loads(p.read_text());before=sha(R/'report.json');current=rd(R/'report.json');records=reg.read_records(ROOT/'research/automation/registry.jsonl');oldnative={fp for fp,z in records.items() if z.get('result_available') and z.get('spec',{}).get('kind')=='strategy' and z.get('spec',{}).get('universe')==['BTC/USDT'] and all(z['spec'].get('parameters',{}).get(k)==v for k,v in {'lookback_days':29,'return_hurdle':.03,'exit_buffer_fraction':.005,'entry_volatility_window_days':10,'continuous_oos_days':391,'initial_capital_usdt':3750,'fixed_entry_notional_usdt':1000}.items()) and not z['spec']['parameters'].get('entry_adverse_volatility_blend',0) and not z['spec']['parameters'].get('entry_path_efficiency_floor',0) and not z['spec']['parameters'].get('entry_directional_confirmation_lookback_days',0)};eth={'7bffd2a6fae9318e840664e45004554b74a95a3d874cd3994a398787b07e9729','eaa75ec6bbd2cf0611b7e53931b6ada73b31f1d33f8186a9c885a3e544bf1270'};wanted=set(oldnative)
for fp,z in records.items():
 sp=z.get('spec',{});q=sp.get('parameters',{});cc=sp.get('components',[])
 if sp.get('kind')=='combination' and z.get('result_available') and q.get('continuous_oos_days')==391 and q.get('initial_capital_usdt')==18750 and len(cc)==2 and all(x['weight']==1 for x in cc):
  fs={x['fingerprint'] for x in cc}
  if len(fs&oldnative)==1 and len(fs&eth)==1:wanted.add(fp)
docs={};old=[];sources={}
for fp in sorted(wanted):
 z=records[fp];assert z['result_available'];path=ROOT/z['report'];assert sha(path)==z['report_sha256']
 if path not in docs:docs[path]=rd(path)
 c=next(c for c in docs[path]['configs'].values() if c['fingerprint']==fp)
 assert sha(ROOT/c['archive'])==c['archive_sha256'];old.append(c);sources[str(path.relative_to(ROOT))]=z['report_sha256']
rows=[]
for c in current['configs'].values():
 signature=tuple(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3'])
 matches=[{'fingerprint':p['fingerprint'],'name':p['name'],'spec':p['spec'],'archive':p['archive'],'archive_sha256':p['archive_sha256'],'status':p['status']} for p in old if p['scope']==c['scope'] and tuple(p['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3'])==signature]
 rows.append({'new_fingerprint':c['fingerprint'],'scope':c['scope'],'ETH_funding_settlement_count':c['W'],'R':c['K'],'matches_saved_paths':matches})
assert sha(R/'report.json')==before
put(R/'known_totalrisk_path_alias_verification.json',{'passed':True,'recorded_utc':now(),'financial_report_sha256':before,'old_native_configurations_read':len(oldnative),'old_parent_configurations_read':len(wanted)-len(oldnative),'source_report_hashes':sources,'rows':rows,'matching_new_configurations':sum(bool(z['matches_saved_paths']) for z in rows),'comparison_scope':'All fixed L29/H.03/E.005/V10 total-risk cap banks found in complete registry before new directional mechanism,plus actually completed same-capital raw1/1 parents with the two frozen ETH banks;not a global independent-sample test.','existing_results_only_no_new_financial_configuration_or_curve_evaluation':True,'no_after_result_grid_or_preset_changes':True})
print('PASS saved cap-bank/parent path comparison',len(oldnative),len(wanted)-len(oldnative),'old;matching new configs',sum(bool(z['matches_saved_paths']) for z in rows))
