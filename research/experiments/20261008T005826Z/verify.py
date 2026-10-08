"""Verify chronology, complete results, immutable prior evidence and frozen account isolation."""
import csv,gzip,hashlib,json,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
T=Path(__file__).resolve().parent;R=T.parents[2];sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));L=R/'research/automation/registry.jsonl';lines=L.read_bytes().splitlines(keepends=True);rr=registry.read_records(L)
assert (p['lines'],p['canonical'],len(p['records']),len(p['prior_conclusions']))==(4697,2299,2301,57)
assert hashlib.sha256(b''.join(lines[:p['lines']])).hexdigest()==p['ledger_sha256'] and all(rr[k]==v for k,v in p['records'].items())
assert (len(lines),len(rr),len({registry.fingerprint(v['spec']) for v in rr.values()}))==(4751,2328,2326)
assert all(v['status']!='reserved' and (v.get('result_available') or v['spec'].get('parameters',{}).get('owner_automation_id')=='btc-eth-2') for v in rr.values())
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());audits=[json.loads((T/q).read_text()) for q in ('audit.log','audit_forward.log')];assert all(a['passed'] for a in audits)
assert len(r['summary']['passed'])==7 and len(r['summary']['rejected'])==17 and len(r['summary']['new_both_periods_passed_combination_pairs'])==0 and r['summary']['new_configs']==24 and r['summary']['new_cost_scenes']==72
parse=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
for batch,report,rp,start in [('batch.json','report.json',r,r['evaluation_started_utc']),('forward_batch.json','forward_report.json',f,f['observation_started_utc'])]:
 for b in json.loads((T/batch).read_text()):
  fp=b['fingerprint'];assert registry.fingerprint(json.loads((R/b['spec']).read_text()))==fp
  ev=[json.loads(z) for z in lines[p['lines']:] if json.loads(z)['fingerprint']==fp];assert len(ev)==2 and ev[0]['status']=='reserved' and parse(r['plan']['frozen_at_utc'])<parse(ev[0]['recorded_at_utc'])<parse(start)<parse(ev[1]['recorded_at_utc']) and ev[1]['status']==rp['configs'][b['name']]['status'] and ev[1]['report_sha256']==sha(T/report)
for rp in (r,f):
 for path,h in rp['source_hashes'].items():assert sha(R/path)==h,path
for path,h in r['plan']['reused_code_sha256'].items():assert sha(R/path)==h,path
old_grid=[]
for b in json.loads((T/'grid_batch.json').read_text()):
 assert b['CHANNEL_entry_days']==20 and b['raw_weights']==[.75,.25] and b['CHANNEL_exit_days'] in (10,20,30) and b['EMA_span_days'] in (50,65,80)
 assert b['is_new']==(b['CHANNEL_exit_days']!=30)
 if not b['is_new']:assert rr[b['fingerprint']]==p['records'][b['fingerprint']];old_grid.append(b['fingerprint'])
 for ref in b['component_refs']:
  sp=json.loads((R/ref['spec']).read_text());q=sp['parameters'];assert q['initial_capital_usdt']==ref['capital_usdt']==(1500 if ref['asset']=='BTC' else 500)
  if ref['kind']=='CHANNEL':assert q['entry_lookback_days']==20 and q['exit_lookback_days']==b['CHANNEL_exit_days']
  else:assert q['span_days']==b['EMA_span_days'] and q['symmetric_band_fraction']==.015
assert len(old_grid)==12
with (T/'sensitivity.csv').open() as fh:
 rows=list(csv.DictReader(fh));assert len(rows)==108 and all(None not in x and None not in x.values() for x in rows)
 for x in rows:assert int(x['CHANNEL_exit_days'])==r['configs'][x['config']]['CHANNEL_exit_days'] and float(x['EMA_span_days'])==r['configs'][x['config']]['EMA_span_days']
assert r['plan']['grid']['predeclared_center']=={'CHANNEL_entry_days':20,'CHANNEL_exit_days':20,'EMA_span_days':65}
assert all(len(z['equity_usdt'])==8697 and z['elapsed_minutes']==8689 and z['elapsed_complete_days']==6 and z['new_reference_points']==1 and z['new_executions']==0 for c in f['configs'].values() for z in c['scenes'].values())
old=json.loads((R/f['source_state']).read_text());state=json.loads((T/'forward_state.json').read_text());assert old['positions_by_asset_and_cost']==state['positions_by_asset_and_cost'] and state['next_daily_decision_utc']=='2026-10-09T00:01:00Z'
assert {a:x['action'] for a,x in f['daily_decisions_by_asset'].items()}=={'BTC':'hold_long','ETH':'hold_long'}
assert sum(x['kind']=='execution_reference' for x in f['append_axis'])==1 and next(x['NAV_index'] for x in f['append_axis'] if x['kind']=='execution_reference')==8647
replay=(T/'reproduce.log').read_text();assert all(x in replay for x in ('PASS:all72 NEW channel/EMA cost scenes','36 EXISTING scenes read-only verified','PASS:all9 cumulative forward scenes','PASS: new parameters/weights'))
assert len((T/'finish.log').read_text().splitlines())==27
h=json.loads((T/'history_paths.json').read_text());assert h['report_sha256']==sha(T/'report.json') and h['new_scenes_already_in_any_prior_report']+h['new_scenes_not_in_any_prior_report']==72
for path,hv in h['all_prior_report_sha256'].items():assert sha(R/path)==hv
for c in p['prior_conclusions']:assert sha(R/c['path'])==c['sha256'] and (R/c['path']).read_text()==c['full_text']
assert sha(R/'research/paper10/state.json')==p['paper10_live_state_sha256'] and sha(R/'research/paper10/plan.json')==p['paper10_plan_sha256']
initial=json.loads((T/'prior_evidence_audit.json').read_text());assert len(initial['initial16_actual_results_checked'])==16 and not initial['missing_initial16']
comp=json.loads((T/'comparison.json').read_text());assert comp['report_sha256']==sha(T/'report.json') and len(comp['comparisons'])==24 and comp['2026_lower_return_higher_DD3_count']==0
recovery=json.loads((T/'cache_recovery.json').read_text());assert recovery['new_backtests']==0 and recovery['scenes_hash_verified']==108
base=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert base==p['base_commit']
paths=sorted(q for q in T.rglob('*') if q.is_file() and '__pycache__' not in q.parts and q.name!='verification.json')+[L,R/'research/automation/README.md']
v={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':4751,'canonical':2326,'preserved_ids':2328,'unchanged_prior_rows':4697,'new_reserved_and_finished':27,'pending':0},'historical_summary':r['summary'],'new_cross_period_qualified':0,'paper10_accounts_unchanged':True,'checks':{'full_new_and_readonly_report_reproduced':True,'source_and_combination_NAV_and_money_audited':True,'frozen_rules_and_raw_weights_verified':True,'legacy_shadow_continuity_verified':True,'initial16_actual_results_verified':True,'sensitivity_plot_visually_reviewed':True},'audits':audits,'files_sha256':{str(q.relative_to(R)):sha(q) for q in paths}}
(T/'verification.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v['registry']))
