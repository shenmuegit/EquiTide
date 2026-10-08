"""Read-only publication verification for this actual quote observation; no HTTP or fills."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal as D
import hashlib, json, math, subprocess, sys
T=Path(__file__).resolve().parent;R=T.parents[3]
sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
dt=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
pre=json.loads((T/'preflight.json').read_text());report=json.loads((T/'report.json').read_text())
before=json.loads((T/'state_before.json').read_text());after=json.loads((T/'state_after.json').read_text())
market=json.loads((T/'market.json').read_text());plan=json.loads((R/'research/paper10/plan.json').read_text())
complete=json.loads((T/'complete.json').read_text());checks=json.loads((T/'supplemental_checks.json').read_text())
assert len(checks)==5 and all(c['exit_code']==0 for c in checks)
assert json.loads(checks[0]['stdout'])['synthetic_fixture_checks']=='PASS'
assert json.loads(checks[1]['stdout'])['passed'] and json.loads(checks[4]['stdout'])['ok']
assert complete['report_sha256']==sha(T/'report.json')==json.loads(checks[1]['stdout'])['report_sha256']
assert complete['state_after_sha256']==sha(T/'state_after.json')==sha(R/'research/paper10/state.json')
assert sha(T/'state_before.json')==pre['old_state_sha256']==report['state_before_sha256']
assert before['last_observation_id']==pre['old_observation_id'] and before['observations']==pre['old_observations']==12
assert after['observations']==13 and after['last_observation_id']==T.name and after['last_observed_at_utc']==report['observed_at_utc']
assert before['cohort_started_at_utc']==after['cohort_started_at_utc']==report['cohort_started_at_utc']=='2026-10-07T18:32:17.645611Z'
assert before['cohort_end_utc']==after['cohort_end_utc']==report['cohort_end_utc']=='2027-04-05T18:32:17.645611Z'
assert sha(R/'research/paper10/plan.json')==pre['plan_sha256']==report['plan_sha256']
assert len(report['configs'])==10 and set(report['configs'])=={p['id'] for p in plan['portfolios']}
assert not report['trades'] and not report['decisions'] and report['new_filled_virtual_orders']==0 and report['real_orders']==0 and report['new_gap'] is None
assert json.loads((T/'trade_ledger.json').read_text())==[]
assert before['coverage_gaps']==after['coverage_gaps']==report['coverage_gaps'] and len(after['coverage_gaps'])==1
oldmarket=json.loads((R/'research/paper10/observations'/before['last_observation_id']/'market.json').read_text())
totals={};sleeves_checked=0
for k in ('1','2','3'):
    total_nav=D(0);total_cost=D(0);parts={a:D(0) for a in ('fee','half_spread','slippage','impact','tick_rounding')}
    for name,c in report['configs'].items():
        prev=before['portfolios'][name]['scenarios'][k];curr=after['portfolios'][name]['scenarios'][k];s=c['scenes'][k]
        assert c['status']=='rejected' and not c['criteria']['minimum180days'] and not c['criteria']['six_observed_folds']
        assert c['capital_usdt']==2000 and c['label']==next(p['label'] for p in plan['portfolios'] if p['id']==name)
        assert c['raw_weights']==next([x['weight'] for x in p['components']] for p in plan['portfolios'] if p['id']==name)
        assert prev['sleeves']==curr['sleeves']==s['sleeves'] and prev['fold_milestones']==curr['fold_milestones']==s['fold_milestones']==[]
        nav=D(0);mark_change=D(0)
        for a,st in curr['sleeves'].items():
            cash,units=D(st['cash_usdt']),D(st['units']);assert cash>=0 and units>=0
            q=market['quotes'][a];oq=oldmarket['quotes'][a]
            mid=(D(q['bid'])+D(q['ask']))/2;oldmid=(D(oq['bid'])+D(oq['ask']))/2
            nav+=cash+units*mid;mark_change+=units*(mid-oldmid);sleeves_checked+=1
            assert st['last_signal_open_ms']==market['daily'][a][-2]['open_ms']
        assert nav==D(s['NAV_usdt'])==D(curr['NAV_usdt'])
        assert abs(nav-D(prev['NAV_usdt'])-mark_change)<D('1e-18')
        peak=max(D(prev['peak_NAV_usdt']),nav);dd=max(prev['max_drawdown_pct'],float(100*(1-nav/peak)))
        assert D(curr['peak_NAV_usdt'])==peak and abs(dd-s['observed_sample_max_drawdown_pct'])<1e-12
        assert D(s['net_PnL_usdt'])==nav-D(2000) and abs(s['net_return_pct']-float(100*(nav/D(2000)-1)))<1e-12
        assert sum(D(st['cost_usdt']) for st in curr['sleeves'].values())==D(s['cost_usdt'])
        total_nav+=nav;total_cost+=D(s['cost_usdt'])
        for a in parts:parts[a]+=D(s['cost_parts'][a])
    totals[k]={'NAV_usdt':str(total_nav),'net_PnL_usdt':str(total_nav-D(20000)),'net_return_pct':str(100*(total_nav/D(20000)-1)),'cost_usdt':str(total_cost),'cost_parts_usdt':{a:str(v) for a,v in parts.items()}}
assert sleeves_checked==60 and all(D(totals[k]['cost_usdt'])>0 for k in totals)
assert len(market['provenance'])==9 and all(p['method']=='GET' and p['status']==200 for p in market['provenance'])
for a,q in market['quotes'].items():
    assert 0<D(q['bid'])<=D(q['ask']) and 0<=(dt(report['observed_at_utc'])-dt(q['observed_at_utc'])).total_seconds()<=30
    assert all(b['available_ms']<=market['server_time_before_ms'] for b in market['daily'][a][:-1])
    assert market['daily'][a][-1]['available_ms']>market['server_time_after_ms']
L=R/'research/automation/registry.jsonl';lines=L.read_bytes().splitlines(keepends=True);records=registry.read_records(L)
assert hashlib.sha256(b''.join(lines[:pre['ledger_rows']])).hexdigest()==pre['ledger_sha256']
assert len(lines)==pre['ledger_rows']+20==5155 and len(records)==pre['preserved_ids']+10==2530
assert len({registry.fingerprint(v['spec']) for v in records.values()})==pre['canonical']+10==2528
assert not [v for v in records.values() if v.get('status')=='reserved']
for b in json.loads((T/'batch.json').read_text()):
    fp=b['fingerprint'];sp=json.loads((R/b['spec']).read_text());events=[json.loads(x) for x in lines[pre['ledger_rows']:] if json.loads(x)['fingerprint']==fp]
    assert registry.fingerprint(sp)==fp and len(events)==2 and events[0]['status']=='reserved' and events[1]['status']=='rejected'
    assert events[1]['result_available'] and events[1]['report_sha256']==sha(T/'report.json')
    assert dt(events[0]['recorded_at_utc'])<min(dt(p['requested_at_utc']) for p in market['provenance'])
    assert dt(sp['parameters']['capture_not_before_utc'])<=dt(report['observed_at_utc'])<=dt(sp['parameters']['capture_deadline_utc'])
    assert sp['parameters']['state_before_sha256']==pre['old_state_sha256'] and sp['parameters']['owner_automation_id']=='btc-eth-2'
for path,expected in pre['protected_sha256'].items():assert sha(R/path)==expected,path
for path,expected in report['source_hashes'].items():assert sha(R/path)==expected,path
for name,expected in pre['skills'].items():assert sha(R/'.agents/skills'/name/'SKILL.md')==expected
feed=json.loads((R/'research/monitor/latest.json').read_text())
assert feed['paper']['observation_id']==T.name and feed['research']['last_run']['id']=='20261008T170619Z'
assert feed['research']['counts']['registered']==2220 and feed['research']['counts']['ranked']==2115
assert json.loads(checks[-1]['stdout'])['observations']==13
elapsed=(dt(report['observed_at_utc'])-dt(report['cohort_started_at_utc'])).total_seconds()
interval=(dt(report['observed_at_utc'])-dt(before['last_observed_at_utc'])).total_seconds()
coverage=min(c['observation_coverage_fraction'] for c in report['configs'].values())
assert elapsed<180*86400 and interval<plan['maximum_observation_gap_seconds'] and coverage>=.95
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert base==pre['base_head']
out={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'base_head':base,'checks':{c['kind']:c['exit_code']==0 for c in checks},
     'plan_sha256_unchanged':pre['plan_sha256'],'continuous_sleeves_checked':60,'cash_units_desired_processed_day_and_costs_unchanged':True,
     'previous_ledger_prefix_unchanged':True,'observations_before':12,'observations_after':13,'all10_reserved_before_HTTP_and_finished_with_actual_results':True,
     'pending_reservations':0,'new_signal_decisions':0,'new_virtual_trades':0,'real_orders':0,'elapsed_seconds':elapsed,'last_interval_seconds':interval,
     'new_sampling_gap':None,'coverage_gap_count':1,'coverage_fraction':coverage,'coverage_above95pct':True,'historic_gap_still_retained':True,
     'no_backfilled_orders':True,'snapshot_totals':totals,'report_sha256':sha(T/'report.json'),'state_sha256':sha(R/'research/paper10/state.json'),
     'protected_code_research_and_shadow_sha256':pre['protected_sha256'],'interpretation':'13actual quote observations,immature fixed accounts;sampled drawdown only,not minute-risk or stable live-profit proof.'}
(T/'verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':True,'observations':13,'actual_sleeves_checked':60,'coverage':coverage,'new_trades':0,'new_gap':False,'totals':totals},ensure_ascii=False))
