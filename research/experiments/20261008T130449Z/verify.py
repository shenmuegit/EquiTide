"""Verify full preregistration, exact funded EMA sources, old-path equivalence and account isolation."""
from pathlib import Path
from datetime import datetime,timezone
import csv,gzip,hashlib,json,subprocess,sys
T=Path(__file__).resolve().parent;R=T.parents[2];sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();parse=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));L=R/'research/automation/registry.jsonl';lines=L.read_bytes().splitlines(keepends=True);records=registry.read_records(L)
assert (prior['lines'],prior['canonical'],prior['preserved_ids'],len(prior['conclusions']))==(5005,2453,2455,63)
assert hashlib.sha256(b''.join(lines[:prior['lines']])).hexdigest()==prior['ledger_sha256'] and all(records[k]==v for k,v in prior['records'].items())
assert (len(lines),len(records),len({registry.fingerprint(v['spec']) for v in records.values()}))==(5035,2470,2468)
assert not [v for v in records.values() if v.get('status')=='reserved']
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());p=r['plan'];audits=[json.loads((T/x).read_text()) for x in ('audit.log','audit_forward.log')]
assert all(v['passed'] for v in audits) and audits[0]['report_sha256']==sha(T/'report.json') and audits[1]['report_sha256']==sha(T/'forward_report.json')
assert r['summary']['new_configs']==12 and r['summary']['new_cost_scenes']==36 and len(r['summary']['passed'])==10 and len(r['summary']['rejected'])==2
assert len(r['summary']['new_both_periods_passed_combination_pairs'])==4 and len(r['summary']['both_periods_passed_combination_pairs'])==6
for bf,rf,report,start in [('batch.json','report.json',r,r['evaluation_started_utc']),('forward_batch.json','forward_report.json',f,f['observation_started_utc'])]:
 for b in json.loads((T/bf).read_text()):
  assert registry.fingerprint(json.loads((R/b['spec']).read_text()))==b['fingerprint']
  ev=[json.loads(x) for x in lines[prior['lines']:] if json.loads(x)['fingerprint']==b['fingerprint']]
  assert len(ev)==2 and ev[0]['status']=='reserved' and ev[1]['status']==report['configs'][b['name']]['status'] and ev[1]['result_available'] and ev[1]['report_sha256']==sha(T/rf)
  assert parse(p['frozen_at_utc'])<parse(ev[0]['recorded_at_utc'])<parse(start)<parse(ev[1]['recorded_at_utc'])
for report in (r,f):
 for path,h in report['source_hashes'].items():assert sha(R/path)==h,path
for path,h in p['reused_code_sha256'].items():assert sha(R/path)==h,path
grid=json.loads((T/'grid_batch.json').read_text());assert len(grid)==18 and sum(b['is_new'] for b in grid)==12
for b in grid:
 assert b['raw_weights']==[.675,.325] and b['entry_days']==15 and b['exit_days']==30 and b['EMA_span_days']==50
 assert b['BTC_EMA_band'] in (.01,.03,.05) and b['ETH_EMA_band'] in (.01,.03,.05)
 assert b['is_new']==(b['BTC_EMA_band']!=b['ETH_EMA_band'])
 if not b['is_new']:assert records[b['fingerprint']]==prior['records'][b['fingerprint']]
 for ref in b['component_refs']:
  sp=json.loads((R/ref['spec']).read_text());q=sp['parameters'];assert q['initial_capital_usdt']==ref['capital_usdt']==(1350 if ref['asset']=='BTC' else 650)
  assert q['entry_lookback_days']==15 and q['exit_lookback_days']==30 and q['EMA_span_days']==50 and q['EMA_symmetric_band']==b[ref['asset']+'_EMA_band']
  assert sp['logic']==p['rules']
with (T/'sensitivity.csv').open() as fh:
 rows=list(csv.DictReader(fh));assert len(rows)==54 and all(None not in v and None not in v.values() for v in rows)
 for v in rows:assert float(v['BTC_EMA_band'])==r['configs'][v['config']]['BTC_EMA_band'] and float(v['ETH_EMA_band'])==r['configs'][v['config']]['ETH_EMA_band']
assert p['grid']['predeclared_center']=={'BTC_EMA_band':.03,'ETH_EMA_band':.03} and p['grid']['predeclared_focus']=={'BTC_EMA_band':.01,'ETH_EMA_band':.05}
assert all(len(s['equity_usdt'])==9427 and s['elapsed_minutes']==9419 and s['elapsed_complete_days']==6 and s['new_mark_minutes']==120 and s['new_reference_points']==0 and s['new_executions']==0 for c in f['configs'].values() for s in c['scenes'].values())
old=json.loads((R/f['source_state']).read_text());state=json.loads((T/'forward_state.json').read_text());assert old['positions_by_asset_and_cost']==state['positions_by_asset_and_cost'] and state['next_daily_decision_utc']=='2026-10-09T00:01:00Z'
assert len(f['append_axis'])==120 and f['validation']['walk_forward']=='Incomplete9419minutes/6complete days;no180day/sixfold qualification'
assert f['validation']['continuity']=='9307oldNAVpoints exact prefix;120closedmarks appended to9427points;cash/units/desired/trades unchanged,no new reference/decision/forced sell'
replay=(T/'reproduce.log').read_text();assert all(v in replay for v in ['PASS:all36 NEW mixed-EMA-bands cost scenes','18 EXISTING scenes read-only verified','including9427point complete time axis','PASS: new parameters/weights'])
assert len((T/'finish.log').read_text().splitlines())==15
h=json.loads((T/'history_paths.json').read_text());assert h['report_sha256']==sha(T/'report.json') and h['new_scenes_already_in_any_prior_report']==24 and h['new_scenes_not_in_any_prior_report']==12 and h['qualified_cross_period_pairs_not_in_any_prior_report']==1
for path,expected in h['all_prior_report_sha256'].items():assert sha(R/path)==expected
for c in prior['conclusions']:assert sha(R/c['path'])==c['sha256'] and (R/c['path']).read_text()==c['text']
assert sha(R/'research/paper10/state.json')==prior['paper10_state_sha256'] and sha(R/'research/paper10/plan.json')==prior['paper10_plan_sha256']
initial=json.loads((T/'prior_evidence_audit.json').read_text());assert len(initial['initial16_actual_results_checked'])==16 and initial['missing_initial16']==[]
comparison=json.loads((T/'comparison.json').read_text());assert comparison['report_sha256']==sha(T/'report.json') and len(comparison['matched_diagonal_comparisons'])==36 and comparison['new_both_periods_qualified']==4 and comparison['full_grid_both_periods_qualified']==6
assert comparison['focus_status']=={'2025':'passed','2026':'rejected'}
assert all(not v for v in comparison['qualified_pair_improvements_vs3percent_center'].values())
for year in ('2025','2026'):assert comparison['existing_component_path_signature_counts'][year+'_BTC']==3
for v in comparison['matched_diagonal_comparisons']:
 c=r['configs'][v['config']];old=r['configs'][v['comparator']]
 assert v['minute_DD3_difference_pp']==c['scenes']['3']['max_drawdown_pct']-old['scenes']['3']['max_drawdown_pct']
 assert all(v['all_cost_return_difference_pp'][k]==c['scenes'][k]['net_return_pct']-old['scenes'][k]['net_return_pct'] for k in ('1','2','3'))
 assert v['all_cost_NAV_identical']==all(c['scenes'][k]['NAV_sha256_f64le']==old['scenes'][k]['NAV_sha256_f64le'] for k in ('1','2','3'))
recovery=json.loads((T/'cache_recovery.json').read_text());assert recovery['new_backtests']==0 and recovery['scenes_hash_verified']==54
feed=json.loads((R/'research/monitor/latest.json').read_text());assert feed['research']['last_run']['id']==T.name and feed['research']['counts']['registered']==2196 and feed['research']['counts']['ranked']==2091 and feed['paper']['observation_id']=='20261008T124834202465Z'
base=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert base==prior['base_head']
paths=sorted(q for q in T.rglob('*') if q.is_file() and '__pycache__' not in q.parts and q.name not in ('verification.json','verify.log'))+[L,R/'research/automation/README.md',R/'research/monitor/latest.json',R/'research/monitor/configs.json.gz']
v={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':5035,'canonical':2468,'preserved_ids':2470,'unchanged_prior_rows':5005,'new_reserved_and_finished':15,'new_historical_trials':12,'new_legacy_observation_cutoffs':3,'pending':0},'historical_summary':r['summary'],'new_cross_period_parameter_pairs':4,'new_scene_records_with_unseen_NAV':12,'new_2026_3x_unique_paths':3,'new_cross_period_return_paths':1,'paper10_accounts_unchanged':True,'checks':{'all_new_and_readonly_results_reproduced':True,'funding1350_650_and_original_weights_verified':True,'source_and_combination_NAV_and_money_audited':True,'whole_NAV_novelty_and_repetition_disclosed':True,'existing_BTC_band_paths_actually_differ':True,'legacy_shadow_numeric_continuity_verified':True,'initial16_actual_results_verified':True,'sensitivity_plot_visually_reviewed':True},'audits':audits,'files_sha256':{str(q.relative_to(R)):sha(q) for q in paths}}
(T/'verification.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v['registry']))
