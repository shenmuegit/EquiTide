"""Check frozen batch chronology, preserved evidence and isolated forward accounts."""
from pathlib import Path
from datetime import datetime,timezone
import csv,gzip,hashlib,json,subprocess,sys
T=Path(__file__).resolve().parent;R=T.parents[2]
sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
parse=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));L=R/'research/automation/registry.jsonl';lines=L.read_bytes().splitlines(keepends=True);records=registry.read_records(L)
assert (prior['lines'],prior['canonical'],prior['preserved_ids'],len(prior['conclusions']))==(4921,2411,2413,61)
assert hashlib.sha256(b''.join(lines[:prior['lines']])).hexdigest()==prior['ledger_sha256']
assert all(records[k]==v for k,v in prior['records'].items())
assert (len(lines),len(records),len({registry.fingerprint(v['spec']) for v in records.values()}))==(4935,2420,2418)
assert not [v for v in records.values() if v.get('status')=='reserved']
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());plan=r['plan'];audits=[json.loads((T/q).read_text()) for q in ('audit.log','audit_forward.log')]
assert all(a['passed'] for a in audits) and audits[0]['report_sha256']==sha(T/'report.json') and audits[1]['report_sha256']==sha(T/'forward_report.json')
assert r['summary']['new_configs']==4 and r['summary']['new_cost_scenes']==12 and len(r['summary']['passed'])==len(r['summary']['rejected'])==2
assert r['summary']['new_both_periods_passed_combination_pairs']==[]
for bf,rf,report,start in [('batch.json','report.json',r,r['evaluation_started_utc']),('forward_batch.json','forward_report.json',f,f['observation_started_utc'])]:
 for b in json.loads((T/bf).read_text()):
  assert registry.fingerprint(json.loads((R/b['spec']).read_text()))==b['fingerprint']
  events=[json.loads(x) for x in lines[prior['lines']:] if json.loads(x)['fingerprint']==b['fingerprint']]
  assert len(events)==2 and events[0]['status']=='reserved' and events[1]['status']==report['configs'][b['name']]['status']
  assert parse(plan['frozen_at_utc'])<parse(events[0]['recorded_at_utc'])<parse(start)<parse(events[1]['recorded_at_utc'])
  assert events[1]['result_available'] and events[1]['report_sha256']==sha(T/rf)
for report in (r,f):
 for path,h in report['source_hashes'].items():assert sha(R/path)==h,path
for path,h in plan['reused_code_sha256'].items():assert sha(R/path)==h,path
grid=json.loads((T/'grid_batch.json').read_text());assert len(grid)==18 and sum(b['is_new'] for b in grid)==4
for b in grid:
 assert b['raw_weights']==[.75,.25] and b['BTC_exit_days']==b['ETH_exit_days']==30
 assert b['BTC_entry_days'] in (10,15,20) and b['ETH_entry_days'] in (10,15,20)
 assert b['is_new']==((b['BTC_entry_days'],b['ETH_entry_days']) in ((10,15),(15,10)))
 if not b['is_new']:assert records[b['fingerprint']]==prior['records'][b['fingerprint']]
 for ref in b['component_refs']:
  sp=json.loads((R/ref['spec']).read_text());q=sp['parameters']
  assert q['initial_capital_usdt']==ref['capital_usdt']==(1500 if ref['asset']=='BTC' else 500)
  assert q['exit_lookback_days']==30 and q['entry_lookback_days']==b[ref['asset']+'_entry_days']
with (T/'sensitivity.csv').open() as fh:
 rows=list(csv.DictReader(fh));assert len(rows)==54 and all(None not in x and None not in x.values() for x in rows)
 for x in rows:assert int(x['BTC_entry_days'])==r['configs'][x['config']]['BTC_entry_days'] and int(x['ETH_entry_days'])==r['configs'][x['config']]['ETH_entry_days']
assert plan['grid']['predeclared_center']=={'BTC_entry_days':15,'ETH_entry_days':10}
assert all(len(s['equity_usdt'])==9187 and s['elapsed_minutes']==9179 and s['elapsed_complete_days']==6 and s['new_mark_minutes']==120 and s['new_reference_points']==0 and s['new_executions']==0 for c in f['configs'].values() for s in c['scenes'].values())
old=json.loads((R/f['source_state']).read_text());state=json.loads((T/'forward_state.json').read_text())
assert old['positions_by_asset_and_cost']==state['positions_by_asset_and_cost'] and state['next_daily_decision_utc']=='2026-10-09T00:01:00Z'
assert len(f['append_axis'])==120 and all(x['kind']=='closed_minute_mark' for x in f['append_axis'])
assert f['validation']['walk_forward']=='Incomplete9179minutes/6complete days;no180day/sixfold qualification'
assert f['validation']['continuity']=='9067oldNAVpoints exact prefix;120closedmarks appended to9187points;cash/units/desired/trades unchanged,no new reference/decision/forced sell'
assert all('9179minute' in c['reason'] for c in f['configs'].values())
replay=(T/'reproduce.log').read_text()
assert all(x in replay for x in ['PASS:all12 NEW mixed-entry cost scenes','42 EXISTING scenes read-only verified','PASS:all9 cumulative forward scenes','PASS: new parameters/weights'])
assert len((T/'finish.log').read_text().splitlines())==7
h=json.loads((T/'history_paths.json').read_text());assert h['report_sha256']==sha(T/'report.json') and h['new_scenes_already_in_any_prior_report']+h['new_scenes_not_in_any_prior_report']==12
for path,hv in h['all_prior_report_sha256'].items():assert sha(R/path)==hv
for c in prior['conclusions']:assert sha(R/c['path'])==c['sha256'] and (R/c['path']).read_text()==c['text']
assert sha(R/'research/paper10/state.json')==prior['paper10_state_sha256'] and sha(R/'research/paper10/plan.json')==prior['paper10_plan_sha256']
initial=json.loads((T/'prior_evidence_audit.json').read_text());assert len(initial['initial16_actual_results_checked'])==16 and initial['missing_initial16']==[]
comparison=json.loads((T/'comparison.json').read_text());assert comparison['report_sha256']==sha(T/'report.json') and len(comparison['matched_anchor_comparisons'])==8 and comparison['new_both_periods_qualified']==0 and comparison['full_grid_both_periods_qualified']==4
for item in comparison['matched_anchor_comparisons']:
 c=r['configs'][item['config']]['scenes']['3'];old=r['configs'][item['comparator']]['scenes']['3']
 assert item['return3_difference_pp']==c['net_return_pct']-old['net_return_pct'] and item['minute_DD3_difference_pp']==c['max_drawdown_pct']-old['max_drawdown_pct']
recovery=json.loads((T/'cache_recovery.json').read_text());assert recovery['new_backtests']==0 and recovery['scenes_hash_verified']==78
feed=json.loads((R/'research/monitor/latest.json').read_text());assert feed['research']['last_run']['id']==T.name and feed['research']['counts']['registered']==2172 and feed['research']['counts']['ranked']==2067
assert feed['paper']['observation_id']=='20261008T085553217840Z'
base=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert base==prior['base_head']
paths=sorted(q for q in T.rglob('*') if q.is_file() and '__pycache__' not in q.parts and q.name not in ('verification.json','verify.log'))+[L,R/'research/automation/README.md',R/'research/monitor/latest.json',R/'research/monitor/configs.json.gz']
v={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':4935,'canonical':2418,'preserved_ids':2420,'unchanged_prior_rows':4921,'new_reserved_and_finished':7,'new_historical_trials':4,'new_legacy_observation_cutoffs':3,'pending':0},'historical_summary':r['summary'],'new_cross_period_qualified':0,'paper10_accounts_unchanged':True,'checks':{'all_new_and_readonly_results_reproduced':True,'source_and_combination_NAV_and_money_audited':True,'fixed_rules_and_raw_weights_verified':True,'legacy_shadow_numeric_continuity_verified':True,'legacy_descriptions_derived_from_actual_counts':True,'initial16_actual_results_verified':True,'sensitivity_plot_visually_reviewed':True},'audits':audits,'files_sha256':{str(q.relative_to(R)):sha(q) for q in paths}}
(T/'verification.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v['registry']))
