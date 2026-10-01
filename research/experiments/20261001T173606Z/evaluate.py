"""Pre-registered historical refinement; complete minute NAV represented compactly."""
import csv
import gzip
import hashlib
import json
import math
import statistics
import sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np
import polars as pl
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'research/experiments/20261001T133655Z'))
from kernel import fill

ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
import importlib.util
def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
engine=module('daily_engine',ROOT/'research/experiments/20261001T013355Z/evaluate.py')
signals=module('frozen_signals',ROOT/'research/experiments/20261001T113625Z/signals.py')
DAY=86400000000000;MIN=60000000000;SPAN=1441;POINTS=180*SPAN+2
CACHE=ROOT/'data/runs'/ROUND.name
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return json.loads(json.dumps(x,default=str,allow_nan=False))
def gzwrite(path,x):
    path.parent.mkdir(exist_ok=True)
    with path.open('wb') as f:
        with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:z.write(json.dumps(canonical(x),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def dd(v):
    return float(np.max(1-v/np.maximum.accumulate(v))*100)
def navhash(v):return hashlib.sha256(v.astype('<f8',copy=False).tobytes()).hexdigest()
def metric(v,days,terminal=False):
    daily=[float(v[d*SPAN]) for d in range(days+1)]
    if terminal:daily.append(float(v[-1]))
    m=engine.metrics(daily,days,terminal);m['daily_mark_drawdown_pct']=m['max_drawdown_pct'];m['max_drawdown_pct']=dd(v);m['calmar']=m['cagr_pct']/m['max_drawdown_pct'] if m['max_drawdown_pct'] else None
    return m,daily
def summarize(v,trades,capital,folds,terminal_units):
    m,daily=metric(v,180,True);m['folds']=[]
    for j,f in enumerate(folds):
        a=j*30*SPAN;b=(j+1)*30*SPAN+1+(j==5)
        fm,_=metric(v[a:b],30,j==5);m['folds'].append({'fold':j+1,**fm})
    assert abs(math.prod(1+f['net_return_pct']/100 for f in m['folds'])-v[-1]/v[0])<1e-12
    filled=[t for t in trades if t['status']=='filled']
    parts={k:float(sum(D(t['cost_parts'][k]) for t in filled)) for k in ('fee','half_spread','slippage','impact','tick_rounding')}
    cost=sum(parts.values());gross=sum(float(D(t['quantity'])*D(t['reference']))*(1 if t['side']!='buy' else -1) for t in filled)
    assert abs(gross-cost-(v[-1]-v[0]))<1e-8 if terminal_units==0 else True
    peak=np.maximum.accumulate(v);ratios=1-v/peak;trough=int(np.argmax(ratios));peakidx=int(np.argmax(v[:trough+1]))
    m.update({'initial_capital_usdt':capital,'final_NAV_usdt':float(v[-1]),'cost_usdt':cost,'cost_pct_initial':cost/capital*100,'cost_parts_usdt':parts,'gross_reference_PnL_usdt':gross,'gross_reference_PnL_to_execution_cost':gross/cost if cost else None,'executions':len(filled),'round_trips':sum(t['side']!='buy' for t in filled),'rejected_orders':len(trades)-len(filled),'cash_or_units_violations':sum(D(t['cash_after'])<0 or D(t['units_after'])<0 for t in trades),'terminal_units':str(terminal_units),'daily_equity_usdt':daily,'NAV_points':len(v),'NAV_sha256_f64le':navhash(v),'drawdown_peak_index':peakidx,'drawdown_trough_index':trough,'drawdown_peak_NAV':float(v[peakidx]),'drawdown_trough_NAV':float(v[trough])})
    return m
from input_data import prepare_data
def component(spec,rows,prices,mult,start,end,folds):
    p=spec['parameters'];capital=p['initial_capital_usdt'];asset=spec['universe'][0].split('/')[0]
    decisions=signals.hysteresis([r['close'] for r in rows],p['lookback_days'],.01,start,end) if p['lookback_days'] else [{'decision_index':i,'long':True,'action':'hold'} for i in range(start,end)]
    cash=D(capital);units=D(0);trades=[];states=[];v=np.empty(POINTS,dtype=np.float64);v[0]=capital
    filters=p['execution']['filters'][asset+'USDT']
    for d,i in enumerate(range(start,end)):
        r=rows[i];assert rows[i-1]['close_available_ts']<r['trade_ts']
        assert decisions[d]['decision_index']==i
        want=decisions[d]['long'];buy=want and not units;sell=not want and units>0
        if buy or sell:
            adv,sigma=engine.lagged_cost_inputs(rows,i)
            cash,units,t=fill(cash,units,bool(buy),D(str(r['trade_open'])),D(str(adv)),D(str(sigma)),mult,filters,D(r['proxy_vwap5']))
            t.update({'decision_index':i,'day_offset':d,'trade_ts_ns':r['trade_ts'],'terminal':False});trades.append(t)
        states.append({'day_offset':d,'cash':str(cash),'units':str(units)})
        base=d*SPAN;v[base+1]=float(cash+units*D(str(r['trade_open'])))
        source=i*1440+1
        v[base+2:base+SPAN+1]=float(cash)+float(units)*prices['close'][source:source+1440]
    if units:
        r=rows[end];adv,sigma=engine.lagged_cost_inputs(rows,end)
        cash,units,t=fill(cash,units,False,D(str(r['trade_open'])),D(str(adv)),D(str(sigma)),mult,filters,D(r['proxy_vwap5']))
        t.update({'decision_index':end,'day_offset':180,'trade_ts_ns':r['trade_ts'],'terminal':True});trades.append(t)
    v[-1]=float(cash+units*D(str(rows[end]['trade_open'])))
    assert np.all(v>0) and len(v)==259382
    m=summarize(v,trades,capital,folds,units)
    segments=[]
    for st in states:
        if not segments or (st['cash'],st['units'])!=(segments[-1]['cash'],segments[-1]['units']):segments.append({**st,'end_day_exclusive':st['day_offset']+1})
        else:segments[-1]['end_day_exclusive']+=1
    archive={'decisions':decisions,'trades':trades,'position_segments':segments,'terminal_cash':str(cash),'terminal_units':str(units),'summary':m}
    return v,archive
def main():
    replay='--reproduce' in sys.argv;plan=json.loads((ROUND/'spec.json').read_text());batch=json.loads((ROUND/'batch.json').read_text());ledger=registry.read_records(ROOT/'research/automation/registry.jsonl')
    for b in batch:
        assert ledger[b['fingerprint']]['status'] in (('passed','rejected') if replay else ('reserved',)),b['name']
        sp=json.loads((ROOT/b['spec']).read_text());assert registry.fingerprint(sp)==b['fingerprint']
    started=datetime.now(timezone.utc).isoformat()
    data,frames,manifest=prepare_data();wf=module('splitter',ROOT/'.agents/skills/walk-forward-validation/scripts/walk_forward.py')
    split=wf.WalkForwardValidator(wf.WalkForwardConfig(train_size=180,test_size=30,step_size=30,window_type='rolling',purge_size=0,embargo_size=3))
    folds=[{'fold':f.fold_idx+1,'train_start_index':int(f.train_indices[0]),'train_end_exclusive_index':int(f.train_indices[-1])+1,'test_start_index':int(f.test_indices[0]),'test_end_exclusive_index':int(f.test_indices[-1])+1} for f in split.split(365)]
    start,end=folds[0]['test_start_index'],folds[-1]['test_end_exclusive_index'];assert (start,end)==(183,363)
    assert data['BTC'][start]['date']=='2025-03-18' and data['BTC'][end]['date']=='2025-09-14'
    assert [r['trade_ts'] for r in data['BTC']]==[r['trade_ts'] for r in data['ETH']]
    CACHE.mkdir(parents=True,exist_ok=True)
    report={'evaluation_started_utc':started,'plan':plan,'data':manifest,'folds':folds,'environment':{'python':sys.version,'numpy':np.__version__,'polars':pl.__version__},'configs':{},'sensitivity':{},
      'curve_formula':{'points':POINTS,'span_per_day':SPAN,'day_offsets':'d=0..179; initial vector[0]=capital; post-decision reference NAV at[d*1441+1]; closed minute marks[d*1441+2:(d+1)*1441+1] use close source[(183+d)*1440+1:(184+d)*1440+1]; terminal vector[-1]=terminal_cash+terminal_units*terminal_open. Component Decimal cash/qty converted to float64 for minute multiplication; post/terminal Decimal before float conversion.',
       'timestamps':'vector[0]=start pre-trade; [d*1441+1] same decision timestamp post-trade; next1440 entries available_ts of real minute closes strictly after decision through next day00:01. Terminal final duplicate boundary after liquidation. Combination = elementwise sum of exact already-sized component vectors; no reweighting.'},
      'interpretation':json.loads((ROUND/'interpretation.json').read_text()),'previous_period_reference':plan['previous_period_reference'],'prior_candidate':{'path':'research/experiments/20261001T113625Z/report.json','sha256':sha(ROOT/'research/experiments/20261001T113625Z/report.json'),'forward_plan_sha256':sha(ROOT/'research/experiments/20261001T113625Z/forward_plan.json'),'no_forward_results':True}}
    byfp={b['fingerprint']:b['name'] for b in batch};archives={}
    for b in batch:
        spec=json.loads((ROOT/b['spec']).read_text());scenes={};vectors={};ar={'spec':spec,'fingerprint':b['fingerprint'],'scenes':{}}
        if spec['kind']=='strategy':
            asset=spec['universe'][0].split('/')[0]
            for k in (1,2,3):
                v,a=component(spec,data[asset],frames[asset],k,start,end,folds);vectors[str(k)]=v;ar['scenes'][str(k)]=a;scenes[str(k)]=a['summary']
            row={'role':b['role'],'asset':asset,'parameters':spec['parameters']}
        else:
            names=[byfp[c['fingerprint']] for c in spec['components']]
            for k in ('1','2','3'):
                parts=[archives[n]['scenes'][k] for n in names]
                v=sum(np.load(CACHE/f'{n}_{k}.npy',allow_pickle=False) for n in names)
                trades=[t for p in parts for t in p['trades']]
                m=summarize(v,trades,2000,folds,sum(D(p['terminal_units']) for p in parts))
                a={'component_names':names,'trades':trades,'terminal_units':str(sum(D(p['terminal_units']) for p in parts)),'summary':m}
                ar['scenes'][k]=a;scenes[k]=m;vectors[k]=v
            n=json.loads((ROOT/next(x['spec'] for x in batch if x['name']==names[0])).read_text())['parameters']['lookback_days']
            row={'role':b['role'],'raw_weights':[c['weight'] for c in spec['components']],'lookback_days':n,'component_names':names}
        path=ROUND/'results'/f'{b["name"]}.json.gz'
        if replay:
            old=json.loads(gzip.decompress(path.read_bytes()));assert canonical(ar)==old,'archive mismatch '+b['name']
            for k,v in vectors.items():assert navhash(v)==navhash(np.load(CACHE/f'{b["name"]}_{k}.npy',allow_pickle=False))
        else:
            gzwrite(path,ar)
            for k,v in vectors.items():np.save(CACHE/f'{b["name"]}_{k}.npy',v,allow_pickle=False)
        row.update({'fingerprint':b['fingerprint'],'spec_path':b['spec'],'archive':str(path.relative_to(ROOT)),'archive_sha256':sha(path),'scenes':scenes});report['configs'][b['name']]=row;archives[b['name']]=ar
        print(json.dumps({'completed':b['name'],'return1':scenes['1']['net_return_pct'],'return3':scenes['3']['net_return_pct'],'minute_DD3':scenes['3']['max_drawdown_pct']}),flush=True)
    for group in ('BTC','ETH','combination'):
        rows=[(n,r) for n,r in report['configs'].items() if (r['role']=='component' and r['asset']==group) or (group=='combination' and r['role']=='combination')];assert len(rows)==9
        stats={k:{'positive_return_fraction':sum(r['scenes'][k]['net_return_pct']>0 for _,r in rows)/9,'positive_sharpe_fraction':sum((r['scenes'][k]['sharpe_365'] or 0)>0 for _,r in rows)/9,'return_range_pct':[min(r['scenes'][k]['net_return_pct'] for _,r in rows),max(r['scenes'][k]['net_return_pct'] for _,r in rows)]} for k in ('1','2','3')}
        coords={n:(r['lookback_days'],r['raw_weights'][0]) if group=='combination' else (r['parameters']['lookback_days'],r['parameters']['initial_capital_usdt']) for n,r in rows}
        xs=sorted({v[0] for v in coords.values()});ys=sorted({v[1] for v in coords.values()});edges=[]
        for a,ra in rows:
            for b,rb in rows:
                if a>=b:continue
                ca,cb=coords[a],coords[b]
                if abs(xs.index(ca[0])-xs.index(cb[0]))+abs(ys.index(ca[1])-ys.index(cb[1]))==1:
                    edges.append({'a':a,'b':b,'return_difference_3x_pct':abs(ra['scenes']['3']['net_return_pct']-rb['scenes']['3']['net_return_pct']),'sharpe_difference_3x':abs(ra['scenes']['3']['sharpe_365']-rb['scenes']['3']['sharpe_365'])})
        cutoff=2*statistics.stdev(e['sharpe_difference_3x'] for e in edges)
        for e in edges:e['cliff_flag_2sd']=e['sharpe_difference_3x']>cutoff
        report['sensitivity'][group]={'axes':['lookback_days','BTC_initial_weight' if group=='combination' else 'actual_initial_capital_usdt'],'cells':9,'metrics':stats,'adjacent_edges':edges,'cliff_cutoff':cutoff,'cliff_note':'Descriptive2sd threshold; not a significance test. Capital axis changes impact/lot residuals but is not independent signal evidence.'}
    for n,r in report['configs'].items():
        s=r['scenes'];pf=sum(f['net_return_pct']>0 for f in s['1']['folds']);r['positive_folds_1x']=pf
        if r['role'].startswith('comparator'):r['criteria']={'research_candidate_scope':False}
        else:
            group='combination' if r['role']=='combination' else r['asset'];ratio=s['1']['gross_reference_PnL_to_execution_cost']
            r['criteria']={'positive_all_costs':all(v['net_return_pct']>0 for v in s.values()),'four_positive_1x_folds':pf>=4,'minute_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'neighbourhood_positive3_gte60pct':report['sensitivity'][group]['metrics']['3']['positive_return_fraction']>=.6,'two_round_trips1':s['1']['round_trips']>=2,'gross_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_balance_violations':all(v['cash_or_units_violations']==0 for v in s.values()),'terminal_flat':all(D(v['terminal_units'])==0 for v in s.values())}
        r['status']='passed' if all(r['criteria'].values()) else 'rejected';r['failed_criteria']=[k for k,v in r['criteria'].items() if not v]
    previous=json.loads((ROOT/plan['previous_period_reference']['report']).read_text())
    for item in batch:
        row=report['configs'][item['name']];oldrow=previous['configs'][item['previous_name']]
        row['previous_period_status']=oldrow['status'];row['previous_period_returns']={k:x['net_return_pct'] for k,x in oldrow['scenes'].items()}
        row['both_periods_meet_full_gates']=row['status']=='passed' and oldrow['status']=='passed'
    research={n:r for n,r in report['configs'].items() if not r['role'].startswith('comparator')}
    report['summary']={'configs':30,'research_configs':27,'actual_cost_scenes':90,'minute_NAV_points':30*3*POINTS,'passed':[n for n,r in research.items() if r['status']=='passed'],'rejected':[n for n,r in research.items() if r['status']=='rejected'],'positive_1x':sum(r['scenes']['1']['net_return_pct']>0 for r in research.values()),'positive_3x':sum(r['scenes']['3']['net_return_pct']>0 for r in research.values()),'fills':sum(r['scenes'][k]['executions'] for r in report['configs'].values() if r['role'] in ('component','comparator') for k in ('1','2','3'))}
    report['source_hashes']={str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'research/experiments/20261001T133655Z/kernel.py',ROUND/'evaluate.py',ROUND/'prepare.py',ROUND/'input_data.py',ROUND/'download_data.py',ROOT/'research/experiments/20261001T133655Z/check_kernel.py',ROOT/'research/experiments/20261001T113625Z/signals.py',ROOT/'research/experiments/20261001T013355Z/evaluate.py',ROOT/'checks/obv_trend_oos.py',ROOT/'.agents/skills/walk-forward-validation/scripts/walk_forward.py']}
    if replay:
        old=json.loads((ROUND/'report.json').read_text());report['evaluation_started_utc']=old['evaluation_started_utc'];assert canonical(report)==old,'full report mismatch'
        print('PASS:all90 actual scene archives, complete NAV vectors and frozen report exactly reproduced; no new ledger mutations');return
    gzwrite(ROUND/'daily_inputs.json.gz',data)
    (ROUND/'data_manifest.json').write_text(json.dumps({'normalized':manifest,'upstream_manifest':str((ROUND/'download_manifest.json').relative_to(ROOT)),'upstream_manifest_sha256':sha(ROUND/'download_manifest.json'),'metadata_sha256':plan['execution']['metadata_sha256']},indent=2)+'\n')
    (ROUND/'report.json').write_text(json.dumps(canonical(report),ensure_ascii=False,separators=(',',':'))+'\n')
    with (ROUND/'sensitivity.csv').open('w',newline='') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['config','role','lookback','capital_or_weights','cost_multiplier','net_return_pct','minute_DD_pct','daily_DD_pct','sharpe365','calmar','positive_folds1','round_trips','cost_pct','status'])
        for n,r in report['configs'].items():
            for k,c in r['scenes'].items():w.writerow([n,r['role'],r.get('lookback_days',r.get('parameters',{}).get('lookback_days')),r.get('raw_weights',r.get('parameters',{}).get('initial_capital_usdt')),k,*[c[x] for x in ('net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar')],r['positive_folds_1x'],c['round_trips'],c['cost_pct_initial'],r['status']])
    print(json.dumps(report['summary']),flush=True)

if __name__=='__main__':main()
