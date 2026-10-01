"""Run only preregistered new signals/sizes; portfolios reuse exact component NAVs."""
import csv
import gzip
import hashlib
import importlib.util
import io
import json
import math
import statistics
import sys
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
import polars as pl

ROOT=Path(__file__).resolve().parents[3]; ROUND=Path(__file__).resolve().parent
OLD=ROOT/'research/experiments/20261001T013355Z'
def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
engine=module('daily_existing',OLD/'evaluate.py')
reg=module('registry_new',ROOT/'research/automation/registry.py')
sig=module('hysteresis_signal',ROUND/'signals.py')

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def canonical(v):return json.loads(json.dumps(v,ensure_ascii=False,sort_keys=True,default=str,allow_nan=False))
def archive(path,value,replay=False):
    value=canonical(value)
    if replay:
        assert json.loads(gzip.decompress(path.read_bytes()))==value,'reproduction mismatch '+str(path)
    else:
        path.parent.mkdir(exist_ok=True)
        buf=io.BytesIO()
        with gzip.GzipFile(fileobj=buf,mode='wb',mtime=0,filename='') as f:
            f.write(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode())
        path.write_bytes(buf.getvalue())
    return {'path':str(path.relative_to(ROOT)),'sha256':sha(path),'bytes':path.stat().st_size}

def extras(r,capital):
    gross=sum((1 if t['side']!='buy' else -1)*t['quantity']*t['reference'] for t in r['trades'])
    assert abs(gross-r['cost_usdt']-(r['equity_usdt'][-1]-capital))<1e-7
    r['gross_reference_PnL_usdt']=gross
    r['gross_reference_PnL_to_execution_cost']=gross/r['cost_usdt'] if r['cost_usdt'] else None
    r['fee_usdt']=sum(t['quantity']*t['execution']*t['fee_rate'] for t in r['trades'])
    r['spread_usdt']=sum(t['quantity']*t['reference']*t['half_spread_rate'] for t in r['trades'])
    r['slippage_usdt']=sum(t['quantity']*t['reference']*t['slippage_rate'] for t in r['trades'])
    r['impact_usdt']=sum(t['quantity']*t['reference']*t['impact_rate'] for t in r['trades'])
    assert abs(sum(r[x] for x in ('fee_usdt','spread_usdt','slippage_usdt','impact_usdt'))-r['cost_usdt'])<1e-7
    r['max_order_fraction_of_lagged_ADV']=max((t['estimated_daily_participation'] for t in r['trades']),default=0)
    r['cash_or_units_violations']=0
    return r

def attach_comparator(report,replay=False):
    """Preserve the disclosed first calculation, then reconstruct the registered comparison."""
    item=json.loads((ROUND/'comparator_batch.json').read_text())[0]
    spec=json.loads((ROOT/item['spec']).read_text())
    ledger=reg.read_records(ROOT/'research/automation/registry.jsonl')
    assert reg.fingerprint(spec)==item['fingerprint']
    assert ledger[item['fingerprint']]['status'] in (('rejected',) if replay else ('reserved',))
    previous=json.loads((OLD/'report.json').read_text())
    assert [c['fingerprint'] for c in spec['components']]==[previous['benchmarks'][a]['registry']['fingerprint'] for a in ('BTC','ETH')]
    assert [c['weight'] for c in spec['components']]==[0.5,0.5]
    scenes={}
    for k in ('1','2','3'):
        parts=[previous['benchmarks'][a][k] for a in ('BTC','ETH')]
        equity=[a+b for a,b in zip(*(p['equity_usdt'] for p in parts))]
        scenes[k]={**engine.metrics(equity,180,True),'equity_usdt':equity,'cost_usdt':sum(p['cost_usdt'] for p in parts),
                   'executions':sum(p['executions'] for p in parts),'round_trips':sum(p['round_trips'] for p in parts),'folds':engine.fold_metrics(equity,report['folds'],183)}
        original=report['benchmark_reuse']['equal_capital_portfolio']['scenes'][k]
        assert original=={x:y for x,y in scenes[k].items() if x not in ('equity_usdt','executions','round_trips','folds')}
    report['comparator_configs']={item['name']:{**item,'status':'rejected','interpretation':'Comparison-only, actual positive result; not a two-parameter-qualified candidate. First aggregate calculation preceded reservation and is explicitly preserved.',
      'result_archive':archive(ROUND/'results'/'benchmark_hold_equal2000.json.gz',{'components':spec['components'],'source_report_sha256':sha(OLD/'report.json'),'scenes':scenes},replay),
      'scenes':{k:{x:y for x,y in r.items() if x!='equity_usdt'} for k,r in scenes.items()}}}
    deviation=json.loads((ROUND/'protocol_deviation.json').read_text())
    report['protocol_deviation']={'path':str((ROUND/'protocol_deviation.json').relative_to(ROOT)),'sha256':sha(ROUND/'protocol_deviation.json'),**deviation}
    report['spec_sha256'][item['spec']]=sha(ROOT/item['spec'])
    report['summary'].update({'all_actual_registered_configs':40,'all_actual_cost_scenes':120,'comparison_configs':1,'comparison_scenes':3,'first_comparison_calculation_preregistered':False})

def complete_comparator():
    # Resume saved evidence; never compute any of the39 already evaluated research paths.
    report=json.loads((ROUND/'report.json').read_text())
    assert 'comparator_configs' not in report
    report['comparison_reconstruction_at_utc']=datetime.now(timezone.utc).isoformat()
    report['source_sha256']={str(p.relative_to(ROOT)):sha(p) for p in [OLD/'evaluate.py',ROOT/'checks/obv_trend_oos.py',ROOT/'.agents/skills/walk-forward-validation/scripts/walk_forward.py',ROOT/'research/automation/registry.py',*(sorted(ROUND.glob('*.py')))]}
    attach_comparator(report)
    (ROUND/'report.json').write_text(json.dumps(canonical(report),ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n')
    print('Completed registered comparison from saved real component NAVs;39 research outcomes unchanged; first calculation before reservation explicitly preserved',flush=True)

def main():
    replay='--reproduce' in sys.argv
    started=datetime.now(timezone.utc).isoformat()
    plan=json.loads((ROUND/'spec.json').read_text());batch=json.loads((ROUND/'batch.json').read_text())
    ledger=reg.read_records(ROOT/'research/automation/registry.jsonl')
    for item in batch:
        sp=json.loads((ROOT/item['spec']).read_text())
        assert reg.fingerprint(sp)==item['fingerprint']
        assert ledger[item['fingerprint']]['status'] in (('passed','rejected') if replay else ('reserved',)),item
    assert len(batch)==39
    manifest=json.loads((OLD/'data_manifest.json').read_text())
    for a,r in manifest['normalized'].items(): assert sha(ROOT/r['path'])==r['sha256'],a
    for a in manifest['archives']: assert sha(ROOT/a['path'])==a['sha256']==a['published_sha256']
    data,_=engine.load_data()
    assert [r['date'] for r in data['BTC']]==[r['date'] for r in data['ETH']]
    wf=module('wf_hyst',ROOT/'.agents/skills/walk-forward-validation/scripts/walk_forward.py')
    splitter=wf.WalkForwardValidator(wf.WalkForwardConfig(train_size=180,test_size=30,step_size=30,window_type='rolling',purge_size=0,embargo_size=3))
    folds=[];dates=[r['date'] for r in data['BTC']]
    for f in splitter.split(len(dates)):
        a,b=int(f.test_indices[0]),int(f.test_indices[-1])+1
        folds.append({'fold':f.fold_idx+1,'train_start_index':int(f.train_indices[0]),'train_end_exclusive_index':int(f.train_indices[-1])+1,'test_start_index':a,'test_end_exclusive_index':b,'test_start_utc':dates[a]+'T00:01:00Z','test_end_mark_utc':dates[b]+'T00:00:00Z'})
    start,end=folds[0]['test_start_index'],folds[-1]['test_end_exclusive_index']
    assert len(folds)==6 and end-start==180
    assert all(a['test_end_exclusive_index']==b['test_start_index'] for a,b in zip(folds,folds[1:]))
    timestamps=[dates[start]+'T00:01:00Z']+[dates[i+1]+'T00:00:00Z' for i in range(start,end)]+[dates[end]+'T00:01:00Z']
    assert timestamps[0]==plan['oos_start_utc'] and timestamps[-1]==plan['terminal_exit_utc']
    inputs=archive(ROUND/'inputs_daily.json.gz',data,replay)
    report={'evaluation_started_utc':started,'plan':plan,'folds':folds,'equity_timestamps_utc':timestamps,'inputs':inputs,
      'data_manifest':{'path':str((OLD/'data_manifest.json').relative_to(ROOT)),'sha256':sha(OLD/'data_manifest.json'),'archives_count':len(manifest['archives']),'normalized':manifest['normalized']},
      'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in [OLD/'evaluate.py',ROOT/'checks/obv_trend_oos.py',ROOT/'.agents/skills/walk-forward-validation/scripts/walk_forward.py',ROOT/'research/automation/registry.py',*(sorted(ROUND.glob('*.py')))]},
      'spec_sha256':{i['spec']:sha(ROOT/i['spec']) for i in batch},'configs':{},'sensitivity':{},'benchmark_reuse':{},
      'environment':{'python':sys.version,'polars':pl.__version__,'numpy':np.__version__},'selection_note':'Full grid, no OOS tuning or final untouched test, 148 prior +39 new canonical configs; earlier all-trial total unknown; no selection-adjusted significance claim.'}
    full={};byfp={};signal_cache={}
    for item in batch:
        sp=json.loads((ROOT/item['spec']).read_text());p=sp['parameters']
        if sp['kind']!='strategy':continue
        asset=sp['universe'][0].split('/')[0];capital=p['initial_capital_usdt']
        key=(asset,p['lookback_days'],p['symmetric_band_fraction'])
        if key not in signal_cache:
            signal_cache[key]=sig.hysteresis([r['close'] for r in data[asset]],p['lookback_days'],p['symmetric_band_fraction'],start,end)
        decisions=signal_cache[key];signals=[False]*len(dates)
        for r in decisions:signals[r['decision_index']]=r['long']
        scenes={}
        for k in (1,2,3):
            r=extras(engine.backtest(data[asset],signals,start,end,capital,1,k),capital)
            r['folds']=engine.fold_metrics(r['equity_usdt'],folds,start)
            scenes[str(k)]=r
        blob=archive(ROUND/'results'/f"{item['name']}.json.gz",{'decisions':decisions,'scenes':scenes},replay)
        full[item['name']]=scenes;byfp[item['fingerprint']]=item['name']
        report['configs'][item['name']]={**item,'asset':asset,'parameters':p,'result_archive':blob,'scenes':{k:{x:y for x,y in r.items() if x not in ('equity_usdt','trades')} for k,r in scenes.items()}}
        print(json.dumps({'computed':item['name'],'return_1x':scenes['1']['net_return_pct'],'return_3x':scenes['3']['net_return_pct'],'trips':scenes['1']['round_trips']}),flush=True)
    for item in batch:
        sp=json.loads((ROOT/item['spec']).read_text())
        if sp['kind']!='combination':continue
        names=[byfp[c['fingerprint']] for c in sp['components']]
        weights=[c['weight'] for c in sp['components']]
        capital=sp['parameters']['initial_capital_usdt']
        assert sum(weights)==1
        assert all(report['configs'][n]['parameters']['initial_capital_usdt']==capital*w for n,w in zip(names,weights))
        assert [report['configs'][n]['asset'] for n in names]==['BTC','ETH']
        scenes={}
        for k in ('1','2','3'):
            parts=[full[n][k] for n in names]
            equity=[sum(v) for v in zip(*(r['equity_usdt'] for r in parts))]
            cost=sum(r['cost_usdt'] for r in parts);gross=sum(r['gross_reference_PnL_usdt'] for r in parts)
            scenes[k]={**engine.metrics(equity,end-start,True),'equity_usdt':equity,'executions':sum(r['executions'] for r in parts),'round_trips':sum(r['round_trips'] for r in parts),
             'cost_usdt':cost,'cost_pct_initial':100*cost/capital,'gross_reference_PnL_usdt':gross,'gross_reference_PnL_to_execution_cost':gross/cost if cost else None,
             **{x:sum(r[x] for r in parts) for x in ('fee_usdt','spread_usdt','slippage_usdt','impact_usdt')},
             'max_order_fraction_of_lagged_ADV':max(r['max_order_fraction_of_lagged_ADV'] for r in parts),'cash_or_units_violations':0,
             'folds':engine.fold_metrics(equity,folds,start)}
        full[item['name']]=scenes
        report['configs'][item['name']]={**item,'parameters':sp['parameters'],'raw_weights':weights,'components':names,'lookback_days':report['configs'][names[0]]['parameters']['lookback_days'],
          'reuse':'Exact absolute component cash+inventory NAV, independently registered at500/1000/1500; no backtest or scaling in portfolio loop; no transfer/rebalance so additional rebalance cost=0.',
          'result_archive':archive(ROUND/'results'/f"{item['name']}.json.gz",{'components':names,'raw_weights':weights,'scenes':scenes},replay),
          'scenes':{k:{x:y for x,y in r.items() if x!='equity_usdt'} for k,r in scenes.items()}}
        print(json.dumps({'combined':item['name'],'return_1x':scenes['1']['net_return_pct'],'return_3x':scenes['3']['net_return_pct']}),flush=True)
    for group in ('BTC','ETH','combination'):
        rows=[(n,r) for n,r in report['configs'].items() if (r['role']=='core' and r['asset']==group) or (group=='combination' and r['role']=='combination')]
        assert len(rows)==9
        metrics={k:{'positive_return_fraction':sum(r['scenes'][k]['net_return_pct']>0 for _,r in rows)/9,'positive_sharpe_fraction':sum((r['scenes'][k]['sharpe_365'] or 0)>0 for _,r in rows)/9,
                   'return_range_pct':[min(r['scenes'][k]['net_return_pct'] for _,r in rows),max(r['scenes'][k]['net_return_pct'] for _,r in rows)]} for k in ('1','2','3')}
        edges=[]
        for i,(an,a) in enumerate(rows):
            pa=(a['lookback_days'],a['raw_weights'][0]) if group=='combination' else (a['parameters']['lookback_days'],a['parameters']['symmetric_band_fraction'])
            grid2=plan['grid']['raw_BTC_capital_weights'] if group=='combination' else plan['grid']['symmetric_band_fraction']
            for bn,b in rows[i+1:]:
                pb=(b['lookback_days'],b['raw_weights'][0]) if group=='combination' else (b['parameters']['lookback_days'],b['parameters']['symmetric_band_fraction'])
                ia=[plan['grid']['lookback_days'].index(pa[0]),grid2.index(pa[1])];ib=[plan['grid']['lookback_days'].index(pb[0]),grid2.index(pb[1])]
                if sum(abs(x-y) for x,y in zip(ia,ib))!=1:continue
                sr1=a['scenes']['3']['sharpe_365'];sr2=b['scenes']['3']['sharpe_365']
                edges.append({'a':an,'b':bn,'return_difference_pct_3x':abs(a['scenes']['3']['net_return_pct']-b['scenes']['3']['net_return_pct']),'sharpe_difference_3x':abs(sr1-sr2) if sr1 is not None and sr2 is not None else None})
        differences=[e['sharpe_difference_3x'] for e in edges if e['sharpe_difference_3x'] is not None]
        cutoff=2*statistics.stdev(differences) if len(differences)>1 else None
        for e in edges:e['cliff_flag_2std']=e['sharpe_difference_3x'] is not None and cutoff is not None and e['sharpe_difference_3x']>cutoff
        report['sensitivity'][group]={'variants':9,'axes':['lookback_days','BTC_initial_capital_weight' if group=='combination' else 'symmetric_band_fraction'],'metrics':metrics,'adjacent_edges':edges,'cliff_cutoff_sharpe':cutoff,
          'all_cells_retained':True,'threshold_note':'2sd of adjacent absolute Sharpe differences is descriptive, not statistical significance; inspect all cells.'}
    for name,row in report['configs'].items():
        scenes=row['scenes']; group='combination' if row['role']=='combination' else row['asset']
        pf=sum(r['net_return_pct']>0 for r in scenes['1']['folds'])
        ratio=scenes['1']['gross_reference_PnL_to_execution_cost']
        row['criteria']={'positive_all_costs':all(r['net_return_pct']>0 for r in scenes.values()),'minimum_four_positive_folds_1x':pf>=4,
          'max_drawdown_3x_lte25pct':scenes['3']['max_drawdown_pct']<=25,'neighborhood_3x_positive_gte60pct':report['sensitivity'][group]['metrics']['3']['positive_return_fraction']>=0.6,
          'minimum_two_round_trips_1x':scenes['1']['round_trips']>=2,'gross_PnL_to_cost_1x_gte2_5':ratio is not None and ratio>=2.5,'no_cash_units_violations':all(r['cash_or_units_violations']==0 for r in scenes.values())}
        row['positive_folds_1x']=pf;row['status']='passed' if all(row['criteria'].values()) else 'rejected'
        row['failed_criteria']=[k for k,v in row['criteria'].items() if not v]
    previous=json.loads((OLD/'report.json').read_text())
    assert previous['equity_timestamps_utc']==timestamps
    for asset in ('BTC','ETH'):
        report['benchmark_reuse'][asset]={'registry':previous['benchmarks'][asset]['registry'],'source_report':str((OLD/'report.json').relative_to(ROOT)), 'source_sha256':sha(OLD/'report.json'),
          'scenes':{k:{x:y for x,y in previous['benchmarks'][asset][k].items() if x not in ('equity_usdt','trades')} for k in ('1','2','3')}}
    report['benchmark_reuse']['cash']={'return_pct':0,'yield':0}
    report['benchmark_reuse']['equal_capital_portfolio']={'capital':2000,'source':'Sum the two original1000 held-spot curves on matching timestamps; no recomputation or weighted-size cost approximation.',
      'scenes':{k:{**engine.metrics([a+b for a,b in zip(previous['benchmarks']['BTC'][k]['equity_usdt'],previous['benchmarks']['ETH'][k]['equity_usdt'])],180,True),
                  'cost_usdt':sum(previous['benchmarks'][a][k]['cost_usdt'] for a in ('BTC','ETH'))} for k in ('1','2','3')}}
    report['summary']={'configs':39,'actual_scenes':117,'passed':[n for n,r in report['configs'].items() if r['status']=='passed'],'rejected':[n for n,r in report['configs'].items() if r['status']=='rejected'],
      'positive_1x':sum(r['scenes']['1']['net_return_pct']>0 for r in report['configs'].values()),'positive_3x':sum(r['scenes']['3']['net_return_pct']>0 for r in report['configs'].values()),'core_positive_3x':sum(r['scenes']['3']['net_return_pct']>0 for r in report['configs'].values() if r['role']=='core')}
    if (ROUND/'comparator_batch.json').exists():
        frozen=json.loads((ROUND/'report.json').read_text()) if replay else {}
        report['comparison_reconstruction_at_utc']=frozen.get('comparison_reconstruction_at_utc',datetime.now(timezone.utc).isoformat())
        attach_comparator(report,replay)
    if replay:
        frozen=json.loads((ROUND/'report.json').read_text());report['evaluation_started_utc']=frozen['evaluation_started_utc']
        assert canonical(report)==frozen,'Entire report reproduction mismatch'
        print('PASS:39 preregistered research configurations/117scenes and1 disclosed comparison/3scenes; all120 archives and full report exactly reproduced; old components reused',flush=True)
        return
    with (ROUND/'sensitivity.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['config','role','asset','parameters_or_weights','cost_multiplier','net_return_pct','max_drawdown_pct','sharpe_365','calmar','round_trips','cost_pct_initial','gross_to_cost','positive_1x_folds','status'])
        for n,r in report['configs'].items():
            for k,c in r['scenes'].items():w.writerow([n,r['role'],r.get('asset','portfolio'),json.dumps(r.get('raw_weights',{x:r['parameters'].get(x) for x in ('lookback_days','symmetric_band_fraction','initial_capital_usdt')})),k,*[c[x] for x in ('net_return_pct','max_drawdown_pct','sharpe_365','calmar','round_trips','cost_pct_initial','gross_reference_PnL_to_execution_cost')],r['positive_folds_1x'],r['status']])
    (ROUND/'report.json').write_text(json.dumps(canonical(report),ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n')
    print(json.dumps(report['summary']),flush=True)

if __name__=='__main__':
    if '--complete-comparator' in sys.argv:complete_comparator()
    else:main()
