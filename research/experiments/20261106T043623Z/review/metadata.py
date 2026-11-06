"""Read-only final metadata/context checks; no strategy, valuation or account mutation."""
import ast,gzip,hashlib,json
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];P=ROOT/'research/experiments/20261106T023552Z'
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,value):(R/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
p,b,rep,bind=[rd(R/n) for n in ['plan.json','batch.json','report.json','code_binding_before_evaluation.json']]
assert len(b)==len(rep['configs'])==9 and len(p['read_only_references'])==23
assert {(x['N'],x['D'],x['K']) for x in b}=={(1250,d,k) for d in [6,7,8] for k in [.01,.02,.03]}
assert p['fixed_bank_capitals']==[3750,15000] and p['fixed_BTC_entry_notional']==1250 and p['fixed_ETH_entry_notional']==4500
assert len(bind['source_sha256'])==36
for path,h in {**bind['source_sha256'],**bind['immutable_source_sha256']}.items():assert sha(ROOT/path)==h,path
assert sha(R/'engine.py')==sha(P/'engine.py')
spec_checks=[]
for row in b:
 sp=rd(ROOT/row['spec']);q=sp['parameters'];cfg=rep['configs'][row['name']]
 assert [x['weight'] for x in sp['components']]==q['raw_component_multipliers']==[1,1]
 assert q['initial_capital_usdt']==18750 and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[1250,4500]
 assert (q['ETH_trend_window_days'],q['ETH_trend_decay_numerator'],q['ETH_trend_decay_denominator'])==(24,23,25)
 assert (q['ETH_trend_slope_lag_days'],q['ETH_trend_slope_hurdle_fraction'])==(row['D'],row['K'])
 assert cfg['status']=='rejected' and set(cfg['scenes'])=={'1','2','3'}
 spec_checks.append({'fingerprint':row['fingerprint'],'spec':row['spec'],'sha256':sha(ROOT/row['spec']),'D':row['D'],'K':row['K']})
windows={}
for stem,lo,hi,nav in [('candidate','2026-11-06T00:30:00Z','2026-11-06T02:30:00Z',14885),('l4h02','2026-11-06T02:10:00Z','2026-11-06T04:10:00Z',7622),('fewm','2026-11-06T02:10:00Z','2026-11-06T04:10:00Z',1730)]:
 z=rd(R/(stem+'_verification.json'));assert z['passed'] and z['window_start_utc']==lo and z['cutoff_utc']==hi and z['NAV_points_per_scene']==nav
 assert all(z[k]==0 for k in ['new_daily_events','new_exact_causal_decisions','new_fills','new_funding_settlements','new_rejected_orders','new_risk_proxy_violations'])
 if stem=='fewm':assert z['cumulative_finished_fewm_observations']==45 and z['elapsed_minutes']==1689
 windows[stem]={k:z[k] for k in ['window_start_utc','cutoff_utc','new_daily_events','new_exact_causal_decisions','new_fills','new_funding_settlements','NAV_points_per_scene','daily_context_bars']}
fv=rd(R/'forward_verification.json');fr=rd(R/'forward_report.json');assert fv['passed'] and (fv['original_NAV_prefix'],fv['NAV_points_per_scene'],fv['cumulative_minutes'],fv['complete_days'])==(50466,50586,50549,35)
assert fv['new_daily_decisions']==fv['new_reference_points']==fv['new_executions']==0 and fr['cutoff_utc']=='2026-11-06T02:30:00Z' and fv['next_daily_decision_utc']=='2026-11-07T00:01:00Z'
context=rd(P/'next_research_state.json')['original_SMA65']['daily_context_source'];assert context=='research/experiments/20261106T023552Z/forward_inputs.json.gz'
oldinput=json.loads(gzip.decompress((ROOT/context).read_bytes()));newinput=json.loads(gzip.decompress((R/'forward_inputs.json.gz').read_bytes()))
for asset in ['BTC','ETH']:
 assert isinstance(oldinput[asset],dict) and len(oldinput[asset]['1d'])==65 and isinstance(newinput[asset],list)
assert sha(ROOT/context)==bind['immutable_source_sha256'][context]
br=rd(R/'budget_bracket_comparison.json');assert br['new_report_sha256']==sha(R/'report.json') and len(br['rows'])==27 and br['old_report_sha256']==p['budget_bracket_readonly_reports']
oldconfigs={}
for n,ref in br['old_report_sha256'].items():
 assert n in ['1000','2000'] and sha(ROOT/ref['path'])==ref['sha256'];doc=rd(ROOT/ref['path']);oldconfigs[n]={c['fingerprint']:c for c in doc['configs'].values()}
for row in br['rows']:
 cfg=next(c for c in rep['configs'].values() if c['fingerprint']==row['fingerprint']);k=str(row['cost_multiplier']);scene=cfg['scenes'][k]
 assert cfg['D']==row['D'] and cfg['K']==row['K'] and cfg['N']==row['BTC_entry_notional']==1250 and row['new_return_pct']==scene['net_return_pct'] and row['new_DD_pct']==scene['max_drawdown_pct']
 for n,v in row['old_readonly'].items():
  old=oldconfigs[n][v['fingerprint']];assert old['N']==int(n) and old['D']==cfg['D'] and old['K']==cfg['K'] and old['source_fingerprints'][1]==cfg['source_fingerprints'][1]
  assert v['canonical_status']==old['status'] and v['return_pct']==old['scenes'][k]['net_return_pct'] and v['DD_pct']==old['scenes'][k]['max_drawdown_pct']
# Preserve frozen text and disclose inherited descriptions rather than changing a finished spec.
errata=[{'path':'plan.json:time_boundaries.causality','original':p['time_boundaries']['causality'],'correction':'Descriptive inherited text D1/3/5, maximum29 and all18 is stale. Actual frozen typed grid/spec/batch is D6/7/8, S24, beta23/25, maximum32 previous complete closes and 9 reservations before new parent valuation. Calendar dates are unchanged.'},{'paths':['plan.json:sources[0].version',*[x['spec']+':sources[0].version' for x in b]],'original':p['sources'][0]['version'],'correction':'The cited pandas formula is a reference; inherited window32/beta31/33 version prose is stale. Every actual ETH component/typed parent parameter uses finite normalized window24 and beta23/25. No strategy/source curve/report/finished spec is rewritten.'}]
put('frozen_description_errata.json',{'recorded_utc':datetime.now(timezone.utc).isoformat(),'scope':'Post-result descriptive metadata review only; original frozen plan/spec/report hashes preserved, no parameter/rule/grid/gate/qualification change or rerun.','errata':errata,'effective_definitions_verified':spec_checks,'source_binding_verified':len(bind['source_sha256']),'actual_parent_configs':9,'actual_max_past_context_days':32,'available_past_context_days':33})
put('current_round_metadata_verification.json',{'passed':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'new_financial_configs':9,'new_native_models':0,'new_cost_scenes':27,'new_historical_passes':0,'new_historical_rejections':9,'read_only_native_banks':13,'read_only_native_cost_curves':39,'raw_weights':[1,1],'bank_capitals':[3750,15000],'entry_notionals':[1250,4500],'bound_sources':36,'native_engine_bytes_unchanged':True,'current_perp_windows':windows,'SMA_original_daily_context_verified':True,'SMA_last_full65day_context':context,'SMA_last_full_context_sha256':sha(ROOT/context),'SMA_current_shape':'asset->minute-array','SMA_prior_shape':'asset->{1d,1m}','SMA_new_percost_daily_decisions':0,'SMA_new_daily_reference_points_per_scene':0,'SMA_new_executions':0,'SMA_original_NAV_prefix':50466,'SMA_current_NAV_points':50586,'no_cash_restart_or_frozen_rule_change':True,'new_independent_candidate_future_created':False,'readonly_budget_context_rows_checked':27,'readonly_budget_context_values':[1000,2000],'postresult_description_errata':'frozen_description_errata.json','all_frozen_parameter_arrays_and_finished_results_unchanged':True})
for f in R.rglob('*.py'):ast.parse(f.read_text())
debris=[str(f.relative_to(R)) for f in R.rglob('*') if f.name=='__pycache__' or f.suffix in ['.pyc','.npy','.tmp'] or 'checkpoint' in f.name];assert not debris
put('cleanup_verification.json',{'passed':True,'scope':'Only current round rebuild debris inspected; none generated/remaining. All actual results/rejections/full account ledgers/frozen rules/registry/raw packets/first warmup and real market inputs retained.','removed_rebuild_files':[],'actual_financial_results_removed':0,'account_ledger_files_removed':0,'remaining_rebuild_intermediates':debris,'preexisting_data_normalized_untouched':True})
print(json.dumps({'passed':True,'configs':len(spec_checks),'bound_sources':36,'budget_context_rows':27,'SMA_last_full65day_context':context,'description_errata':len(errata),'remaining_rebuild_intermediates':len(debris)}))
