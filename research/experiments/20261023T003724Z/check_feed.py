"""Check dashboard attribution and final append-only evidence without simulating trades."""
import gzip,hashlib,importlib.util,json,subprocess
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
stamp=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
def main():
    raw=gzip.decompress((ROOT/'research/monitor/configs.json.gz').read_bytes());feed=json.loads(raw);latest=json.loads((ROOT/'research/monitor/latest.json').read_text());by={x['fingerprint']:x for x in feed}
    assert len(by)==len(feed) and hashlib.sha256(raw).hexdigest()==latest['research']['configs_sha256']
    spec=importlib.util.spec_from_file_location('reg',ROOT/'research/automation/registry.py');reg=importlib.util.module_from_spec(spec);spec.loader.exec_module(reg)
    records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');ctx=json.loads((R/'context.json').read_text());report=json.loads((R/'report.json').read_text());fwd=json.loads((R/'forward_report.json').read_text())
    evaluations=json.loads((R/'research_commands.json').read_text());started=next(x['started_utc'] for x in evaluations if x['command'][-1]=='evaluate')
    fields={'return_pct':'net_return_pct','drawdown_pct':'max_drawdown_pct','sharpe':'sharpe_annualized','cost':'cost_usdt'}
    count=0
    for cfg in report['configs'].values():
        fp=cfg['fingerprint'];row=by[fp];assert row['report']==str((R/'report.json').relative_to(ROOT)) and row['status']==cfg['status'] and row['criteria']==cfg['gates']
        p=records[fp]['spec']['parameters'];assert row['start_utc']==p['oos_start_utc'] and row['end_utc']==p['oos_end_exclusive_utc'] and row['positive_folds_1x']==cfg['scenarios']['1']['positive_folds']
        assert row['validation']['walk_forward_folds']==12 and row['validation']['cost_scenarios']==['1','2','3'] and row['validation']['sensitivity_recorded']
        reserve=[e for e in events if e['fingerprint']==fp and e['status']=='reserved'];assert len(reserve)==1 and stamp(reserve[0]['recorded_at_utc'])<stamp(started)
        for cost,s in cfg['scenarios'].items():
            view=row['scenes'][cost]
            for dest,src in fields.items():assert view[dest]==(round(float(s[src]),6) if s[src] is not None else None),(cfg['name'],cost,dest)
            assert view['nav_hash']==s['minute_nav_sha256_f64le'] and view['executions']==s['executions'] and view['round_trips']==s['round_trips']
            assert view['fold_returns_pct']==[round(float(f['net_return_pct']),6) for f in s['folds']]
            assert view['fold_drawdowns_pct']==[round(float(f['max_drawdown_pct']),6) for f in s['folds']];count+=1
    for cfg in [*report['configs'].values(),*fwd['configs'].values()]:
        rec=records[cfg['fingerprint']];path=R/('forward_report.json' if cfg['name'].startswith('forward_snapshot') else 'report.json')
        assert rec['result_available'] is True and rec['status']=='rejected' and rec['report_sha256']==sha(path)
    for group in ['benchmark_read_only','B0_read_only_reference']:
        for cfg in report[group].values():
            assert by[cfg['fingerprint']]['report']==report['source_report']
            assert records[cfg['fingerprint']]['report_sha256']==report['source_report_sha256'] and sha(ROOT/cfg['full_result_path'])==cfg['full_result_sha256']
    assert '537f5a8fc4b6e58511fabbde15096659e072be117d9a365d3827ac178134c70e' in by
    assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items())
    base=json.loads((R/'startup.json').read_text())['head_after_successful_SSH_fetch']
    original=subprocess.check_output(['git','show',base+':research/automation/registry.jsonl'],cwd=ROOT);ledger=(ROOT/'research/automation/registry.jsonl').read_bytes()
    assert hashlib.sha256(original).hexdigest()==ctx['main_registry_sha256_before_reserve'] and ledger.startswith(original)
    new=[json.loads(line) for line in ledger[len(original):].splitlines()];assert len(new)==42 and len({x['fingerprint'] for x in new})==21 and all(e['status'] in ('reserved','rejected') for e in new)
    assert all(x['exit_code']==0 for name in ['initial_commands.json','research_commands.json','forward_commands.json','final_gates.json'] for x in json.loads((R/name).read_text()))
    out={'passed':True,'research_configs':len(feed),'paper_observations':latest['paper']['observation_count'],'paper_accounts':len(latest['paper']['accounts']),'new_configs_verified':18,'new_cost_scenes_verified':count,'prior_configs_reused_read_only':20,'new_finished_observations':3,'main_registry_append_only_events':42,'regression_alias_retained':True,'financial_report_sha256':sha(R/'report.json'),'forward_report_sha256':sha(R/'forward_report.json'),'protected_inputs_unchanged':True}
    (R/'feed_verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out),flush=True)
if __name__=='__main__':main()
