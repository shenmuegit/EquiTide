"""Pre-register and evaluate lower-turnover matched carry using the frozen prior engine."""
import argparse, copy, csv, gzip, hashlib, importlib.util, json, math, os, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import carry as c
from nav_audit import augment

ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
OLD=ROOT/'research/experiments/20261001T053425Z';PREV=ROOT/'research/experiments/20261022T223523Z'
reg=c.module('carry_registry',ROOT/'research/automation/registry.py')
old_eval=c.module('prior_carry_comparator',OLD/'evaluate.py')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def gzput(p,x):p.write_bytes(gzip.compress(json.dumps(x,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode(),compresslevel=9,mtime=0))
def readgz(p):return json.loads(gzip.decompress(p.read_bytes()))
def csvput(path,rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def call(command,row,*args):
    p=subprocess.run([sys.executable,'research/automation/registry.py',command,row['spec'],*args],cwd=ROOT,capture_output=True,text=True)
    x={'name':row['name'],'fingerprint':row['fingerprint'],'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    print(json.dumps(x),flush=True);assert p.returncode==0 and p.stdout.strip()==row['fingerprint'],x
    return x
def folds(plan):
    start=c.ns(plan['time_boundaries']['first_signal_utc'])
    return [{'fold':i+1,'test_start_signal_ns':start+i*28*c.DAY,'test_end_signal_ns':start+(i+1)*28*c.DAY,
             'test_start_utc':c.utc(start+i*28*c.DAY+c.MINUTE),'test_end_utc':c.utc(start+(i+1)*28*c.DAY+c.MINUTE)} for i in range(12)]
def freeze():
    assert not (R/'plan.json').exists()
    events=reg.read_events(ROOT/'research/automation/registry.jsonl');records=reg.read_records(ROOT/'research/automation/registry.jsonl')
    first=[json.loads(x)['fingerprint'] for x in (ROOT/'research/automation/registry.jsonl').read_text().splitlines()[:16]];initial={}
    for e in events:
        if e['fingerprint'] in first:initial.setdefault(e['fingerprint'],{}).update(e)
    assert len(initial)==16 and all(x.get('result_available') for x in initial.values())
    monitor=c.module('carry_monitor_context',ROOT/'research/monitor/snapshot.py')
    canonical={reg.fingerprint(x['spec']) for x in records.values() if not monitor.is_observation(x['spec'])}
    protected=[ROOT/'research/paper10/plan.json',ROOT/'research/paper10/state.json',PREV/'forward_state.json',PREV/'forward_report.json']
    put(R/'context.json',{'registry_events':len(events),'registry_ids':len(records),'canonical_research_definitions_excluding_observations':len(canonical),
        'main_registry_sha256_before_reserve':sha(ROOT/'research/automation/registry.jsonl'),'initial_16_missing_actual_results':0,
        'prior_conclusions_read':[{'path':rel(p),'sha256':sha(p),'opening':p.read_text()[:220]} for p in sorted((ROOT/'research/experiments').glob('*/result.md'))],
        'account_hashes_before':{rel(p):sha(p) for p in protected}})
    costs={'spot_fee_per_side':.001,'perp_fee_per_side':.0005,'half_spread_per_side':.0001,'slippage_per_side':.0002,
        'impact':'0.5*strictly previous20complete-day log-return sample sigma*sqrt(leg quote notional/leg prior20day quote ADV)',
        'maximum_participation':.001,'multipliers':[1,2,3],'funding_stress':'Paid negative receipts multiplied; positive income unchanged; actual settlement mark and millisecond jitter retained.',
        'metadata':'Frozen20261001spot snapshot plus normalized perp metadata; historical proxy,not refreshed historical tiers.',
        'maintenance_ratio_assumed':.01,'borrow':'No spot short or borrowing; USDT yield0; isolated5000/5000books,no transfers.'}
    plan={'round':R.name,'frozen_at_utc':now(),'trigger_utc':'2026-10-23T00:37:24.034Z','direction':'Longer-horizon B1 funding-filtered matched spot-long/perp-short carry',
        'hypothesis':'Test the existing causal prior21published funding median gate at longer holding horizons and lower raw per-leg exposures. Compare read-only B0 and spot references on the identical336day window; no new fitting or amplification of positive funding.',
        'grid':{'assets':['BTC','ETH'],'holding_hours':[672,1008,1344],'per_leg_fraction':[.15,.25,.35],'candidate_configs':18,'comparators_read_only':20,'cost_multipliers':[1,2,3]},
        'time_boundaries':{'data_start_utc':'2025-09-16T00:00:00Z','data_end_exclusive_utc':'2026-09-16T00:00:00Z','first_signal_utc':'2025-10-10T00:00:00Z',
            'last_signal_utc':'2026-09-11T00:00:00Z','oos_start_utc':'2025-10-10T00:01:00Z','oos_end_exclusive_utc':'2026-09-11T00:01:00Z','oos_days':336,
            'warmup_days':21,'initial_gap_days':3,'folds':12,'fold_days':28,'training':'No model/labels/fitting.21days cost warmup plus3day initial gap;fixed rules and grid throughout.'},
        'rule':{'entry':'At completed hourly T when flat and the full H-hour horizon fits, enter only if perp notional*median(last21published realized rates/actual interval hours)*H minus base1x estimated roundtrip execution cost exceeds1USDT. Quantity=floor(fraction*knownNAV/known spot close/commonlot)*commonlot fixed using information through T. Funding T..T+1minute settles old positions before execution but cannot influence sizing. Identical base1x eligibility model under1/2/3x actual cost stress; scenario NAV can affect size.',
            'exit':'At each held hourly T, exit when estimated remaining funding minus only future base1x exit costs is <=1USDT, or at fixed entry signal+H hours. Entry costs are sunk and excluded. Execute T+1minute open; next hourly decision may re-enter. Costed terminal exit; no fold resets.',
            'weights':'Fraction is raw notional/NAV PER LEG,not cash allocation or normalized portfolio weight; gross about2*f. Initial spotcash5000/perpcollateral5000,total10000. Exact matched base quantity; no transfers,rebalancing or borrow.',
            'funding':'Actual rate*actual settlement mark*old matched quantity; actual settlement and availability ns retained. B1 selects only21 observations with available_ts<=T; median of each realized rate divided by its actual settlement interval hours, never future announced or realized rates.',
            'margin':'Original1% hourly mark-high envelope plus independent pre/post-event whole-hour mark-high check and isolated cash checks. Conservative complete in-OOS hourly bounds can include pre-entry/post-exit extremes;terminal gap uses closed-minute traded-high proxy,never post-OOS mark high. Qualification only,never signals. No automatic liquidation model;any violation rejects.'},
        'costs':costs,'gates':{'all_cost_returns_positive':True,'positive_1x_folds_min':8,'max_3x_continuous_minute_traded_price_drawdown_pct':25,'local_3x_positive_fraction_min':.6,'round_trips_1x_min':4,'gross_reference_pnl_total_cost_ratio_1x_min':2.5,'cash_margin_violations':0,'spot_cash_order_rejections':0,'terminal_flat':True},
        'sources':[{'url':'https://github.com/binance/binance-public-data','accessed_utc':'2026-10-23','scope':'Original real minute spot/perp and hourly mark archive provenance; normalized ns hashes checked.'},
            {'url':'https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History','accessed_utc':'2026-10-23','scope':'Actual realized rates,settlement marks/timestamps. Official page redirects to current market-data catalog.'},
            {'path':rel(OLD/'carry.py'),'sha256':sha(OLD/'carry.py'),'scope':'Existing unchanged B1 causal funding gate and isolated-ledger accounting;longer horizons and raw per-leg fractions, unchanged kernel.'}],
        'history_note':'Reused2025-2026development history,not untouched finalholdout. Prior B0/B1 real results retained; no exact old configuration rerun. Many prior trials;no DSR/PBO claim.',
        'limits':['No historical L2/TCA or exchange liquidation tiers;frozen metadata and1%maintenance are declared proxies.','Original hourly equity retained;stronger full closed-minute traded-price plus post-fill NAV reconstructed independently;not minute mark-price NAV/intraminute extrema.','No real orders or changes to originalSMA orpaper10 accounts.']}
    assert c.ns(plan['time_boundaries']['last_signal_utc'])-c.ns(plan['time_boundaries']['first_signal_utc'])==336*c.DAY
    put(R/'plan.json',plan);(R/'specs').mkdir();batch=[]
    template=next(x['spec'] for x in records.values() if x['spec']['family']=='repeated-matched-carry' and x['spec']['parameters']['baseline']=='B1')
    shared={'initial_capital_usdt':10000,'books_usdt':[5000,5000],'oos_start_utc':plan['time_boundaries']['oos_start_utc'],'oos_end_exclusive_utc':plan['time_boundaries']['oos_end_exclusive_utc'],'warmup_days':21,'embargo_days':3,'walk_forward_folds':12,'walk_forward_test_days':28,'walk_forward_step_days':28,'costs':costs,'metadata_snapshot_sha256':sha(R/'spot_metadata_snapshot.json')}
    for asset in ('BTC','ETH'):
        for hours in plan['grid']['holding_hours']:
            for fraction in plan['grid']['per_leg_fraction']:
                name=f'carry_B1_{asset}_H{hours}_F{fraction}';s=copy.deepcopy(template);s.update(name=name,universe=[asset+'/USDT'],validation_plan=rel(R/'plan.json'),sources=plan['sources'])
                s['parameters'].update(shared,baseline='B1',holding_hours=hours,per_leg_fraction=fraction,buffer_usdt=1,funding_window=21)
                p=R/'specs'/(name+'.json');put(p,s);batch.append({'name':name,'asset':asset,'holding_hours':hours,'per_leg_fraction':fraction,'role':'candidate','spec':rel(p),'fingerprint':reg.fingerprint(s)})
    assert len(batch)==18 and len({x['fingerprint'] for x in batch})==18
    put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/carry_B1_BTC_H1008_F0.25.json').read_text()))
    out=[]
    for row in batch:out.append(call('reserve',row));put(R/'reserve.json',out)
    print('FROZEN_AND_RESERVED',len(out),sha(R/'plan.json'),flush=True)

def datasets():
    expected=json.loads((R/'carry_data_availability.json').read_text())
    for x in expected:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
    out={a:c.load(a) for a in ('BTC','ETH')}
    for d in out.values():
        for name in ('spot_bars','perp_bars'):
            f=d['frames'][name];assert (f['available_ts']-f['open_ts']==c.MINUTE).all() and (f['open_ts'].diff().drop_nulls()==c.MINUTE).all()
        assert (d['frames']['spot_bars']['open_ts']==d['frames']['perp_bars']['open_ts']).all()
        marks=d['frames']['mark_hour_bars'];assert marks['is_closed'].all() and (marks['available_ts']-marks['open_ts']==c.HOUR).all() and (marks['open_ts'].diff().drop_nulls()==c.HOUR).all()
        assert len(d['marks'])==8760 and all(e['available']>=e['ts'] and e['mark']>0 for e in d['events'])
        assert all(b['ts']>a['ts'] for a,b in zip(d['events'],d['events'][1:]))
    return out

def references():
    path=PREV/'report.json';assert sha(path)=='47ef2f9f0d06063b7f7d88a6000079cf641b4c90b57fccce43c9a17996ea2b1a'
    prior=json.loads(path.read_text());ledger=reg.read_records(ROOT/'research/automation/registry.jsonl')
    assert prior['time_boundaries']==json.loads((R/'plan.json').read_text())['time_boundaries']
    for cfg in prior['configs'].values():
        assert sha(ROOT/cfg['full_result_path'])==cfg['full_result_sha256']
        assert ledger[cfg['fingerprint']]['result_available'] and ledger[cfg['fingerprint']]['report_sha256']==sha(path)
    assert len(prior['configs'])==20
    return {'source_report':rel(path),'source_report_sha256':sha(path),'reuse':'Read-only original result bytes; no reservation, new evaluation or finish. Same window, capital, data and costs.', 'benchmark_read_only':{n:v for n,v in prior['configs'].items() if v['role']=='benchmark'},'B0_read_only_reference':{n:v for n,v in prior['configs'].items() if v['role']=='candidate'}}

def calculate(row,m,data,plan):
    fs=folds(plan);p=json.loads((ROOT/row['spec']).read_text())['parameters']
    assert row['role']=='candidate'
    base=c.simulate(data,p,m,fs)
    extra=augment(data,base,fs[0]['test_start_signal_ns']+c.MINUTE,fs[-1]['test_end_signal_ns']+c.MINUTE,m,row['role']=='benchmark')
    return {'cost_multiplier':m,'hourly_engine_output':base,'minute_and_accounting_audit':extra}

def summary(full):
    z=full['hourly_engine_output'];a=full['minute_and_accounting_audit'];s={k:v for k,v in z.items() if k not in ('equity','equity_signal_times','trades','funding_events','decisions')}
    s['hourly_sampled_max_drawdown_pct']=s.pop('max_drawdown_pct');s['max_drawdown_pct']=a['max_drawdown_1m_sampled_pct'];s.update(a)
    funds=z.get('funding_events',[]);paid=-sum(min(x['amount_usdt'],0) for x in funds);income=sum(max(x['amount_usdt'],0) for x in funds)
    s.update(cost_usdt=z['execution_cost_usdt']+paid,funding_paid_usdt=paid,funding_income_usdt=income,
             round_trips=z['round_trips'],positive_folds=z.get('positive_folds_1x',sum(x['net_return_pct']>0 for x in z['folds'])),
             rejected_orders=sum(x['action']=='spot_cash_rejected' for x in z.get('decisions',[])),
             calmar_1m_sampled=z['annualized_return_pct']/s['max_drawdown_pct'] if s['max_drawdown_pct'] else None)
    s['gross_reference_pnl_to_cost']=(z['final_NAV']-10000+s['cost_usdt'])/s['cost_usdt'] if s['cost_usdt'] else None
    m=full['cost_multiplier'];fees=sum(t['fee_usdt'] for t in z['trades'])
    spread=sum(abs(t['quantity'])*t['reference']*.0001*m for t in z['trades'])
    slip=sum(abs(t['quantity'])*t['reference']*.0002*m for t in z['trades'])
    impact=sum(abs(t['quantity'])*t['reference']*t['impact']*m for t in z['trades'])
    s['execution_cost_parts_usdt']={'fees':fees,'half_spread_model':spread,'slippage_model':slip,'impact_model':impact,'tick_and_float_residual':z['execution_cost_usdt']-fees-spread-slip-impact}
    return s

def evaluate():
    assert not (R/'report.json').exists(),'Use verify,never recompute finished configurations.'
    plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl')
    assert all(records[x['fingerprint']]['status']=='reserved' for x in batch)
    data=datasets();(R/'results').mkdir(exist_ok=True);(R/'checkpoints').mkdir(exist_ok=True);configs={}
    for row in batch:
        costs={}
        for m in (1,2,3):
            path=R/'checkpoints'/f"{row['name']}_{m}.json.gz"
            if path.exists():
                cached=readgz(path);assert cached['fingerprint']==row['fingerprint'] and cached['plan_sha256']==sha(R/'plan.json');full=cached['full']
            else:
                full=calculate(row,m,data[row['asset']],plan);gzput(path,{'fingerprint':row['fingerprint'],'plan_sha256':sha(R/'plan.json'),'full':full})
            costs[str(m)]=full;print(row['name'],m,summary(full)['net_return_pct'],flush=True)
        path=R/'results'/(row['name']+'.json.gz');gzput(path,{'fingerprint':row['fingerprint'],'plan_sha256':sha(R/'plan.json'),'costs':costs})
        configs[row['name']]={**row,'spec_path':row['spec'],'initial_capital_usdt':10000,'full_result_path':rel(path),'full_result_sha256':sha(path),'scenarios':{k:summary(v) for k,v in costs.items()}}
    candidates=[x for x in configs.values() if x['role']=='candidate'];hs=plan['grid']['holding_hours'];fr=plan['grid']['per_leg_fraction'];by={(x['asset'],x['holding_hours'],x['per_leg_fraction']):x for x in candidates}
    for x in candidates:
        i=hs.index(x['holding_hours']);j=fr.index(x['per_leg_fraction']);ns=[by[x['asset'],hs[a],fr[b]] for a in range(max(0,i-1),min(3,i+2)) for b in range(max(0,j-1),min(3,j+2))]
        fraction=sum(n['scenarios']['3']['net_return_pct']>0 for n in ns)/len(ns);x['sensitivity']={'local_3x_neighbor_positive_fraction':fraction,'neighbor_count':len(ns),'neighbor_names':[n['name'] for n in ns]}
        ss=x['scenarios'];one=ss['1'];three=ss['3'];x['gates']={'all_cost_scenarios_positive':all(s['net_return_pct']>0 for s in ss.values()),'positive_1x_folds_at_least_8':one['positive_folds']>=8,'drawdown3_lte25':three['max_drawdown_pct']<=25,'neighbor3_positive_fraction_gte60':fraction>=.6,'round_trips1_gte4':one['round_trips']>=4,'gross_cost_ratio1_gte2_5':one['gross_reference_pnl_to_cost'] is not None and one['gross_reference_pnl_to_cost']>=2.5,'no_cash_margin_violations':all(not s['cash_margin_violations'] and not s['independent_cash_margin_violations'] for s in ss.values()),'no_spot_cash_order_rejections':all(s['rejected_orders']==0 for s in ss.values()),'terminal_flat':all(s['terminal_flat'] for s in ss.values())}
        x['status']='passed' if all(x['gates'].values()) else 'rejected'
    for x in configs.values():
        if x['role']=='benchmark':x.update(status='rejected',gates={'reference_only_no_strategy_qualification':False},sensitivity={'explanation':'Fixed same-window comparator;no adjustable parameter batch or alpha qualification.'})
    report={'round':R.name,'frozen_at_utc':plan['frozen_at_utc'],'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':plan['time_boundaries'],'configs':configs,
        'summary':{'candidate_configs':18,'comparator_configs':0,'read_only_comparator_configs':20,'total_evaluated_configs':18,'cost_scenarios':54,'passed':sum(x['status']=='passed' for x in candidates),'rejected':sum(x['status']=='rejected' for x in candidates),'positive_configs_by_cost':{str(m):sum(x['scenarios'][str(m)]['net_return_pct']>0 for x in candidates) for m in (1,2,3)},'ranked_by_1x_net_return':sorted((x['name'] for x in candidates),key=lambda n:configs[n]['scenarios']['1']['net_return_pct'],reverse=True)},
        'input_data':json.loads((R/'carry_data_availability.json').read_text()),'sources':plan['sources'],'accounting_scope':plan['limits'],'benchmark_scope':'Same336day period;4500spot target/remaining cash is directional,not risk-matched carry. Benchmark rejected means reference-only,not necessarily negative return. Cash0yield comparator is analytic0.',
        'artifacts':{'full_results':'results/*.json.gz','sensitivity':'sensitivity.csv','folds':'fold_results.csv','verification':'verification.json'}}
    report.update(references());put(R/'report.json',report);print('SUMMARY',json.dumps(report['summary']),flush=True)

def verify():
    r=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());data=datasets();rows=json.loads((R/'batch.json').read_text());checks=0;hours=0;minutes=0
    assert all(r[k]==v for k,v in references().items())
    before={p:sha(ROOT/p) for p in json.loads((R/'context.json').read_text())['account_hashes_before']}
    for row in rows:
        cfg=r['configs'][row['name']];p=ROOT/cfg['full_result_path'];assert sha(p)==cfg['full_result_sha256'];saved=readgz(p)
        for m in (1,2,3):
            replay=calculate(row,m,data[row['asset']],plan);assert replay==saved['costs'][str(m)],(row['name'],m,'full replay')
            assert summary(replay)==cfg['scenarios'][str(m)]
            hours+=replay['minute_and_accounting_audit']['hourly_NAV_reconciled'];minutes+=replay['minute_and_accounting_audit']['minute_close_samples'];checks+=1
    assert all(sha(ROOT/p)==h for p,h in before.items())
    out={'passed':True,'report_sha256':sha(R/'report.json'),'actual_configurations':18,'read_only_prior_configurations_hash_checked':20,'cost_scenes_replayed':checks,'independently_reconciled_hourly_NAV_points':hours,'closed_minute_NAV_marks_reconstructed':minutes,'full_funding_trades_equity_decisions_and_minute_hash_exact':True,'protected_inputs_unchanged':True}
    put(R/'verification.json',out);print(json.dumps(out),flush=True)

def finish():
    r=json.loads((R/'report.json').read_text());out=[]
    for row in json.loads((R/'batch.json').read_text()):out.append(call('finish',row,r['configs'][row['name']]['status'],rel(R/'report.json')));put(R/'finish.json',out)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','verify','finish']);globals()[p.parse_args().command]()
