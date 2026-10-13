#!/usr/bin/env python3
"""Evaluate reserved BTC/ETH daily volatility-compression breakout variants."""
from __future__ import annotations
import csv, hashlib, importlib.util, json, math, statistics, sys
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np
import polars as pl

ROOT=Path(__file__).resolve().parents[3]
ROUND=Path(__file__).resolve().parent
DAY_NS=86_400_000_000_000
MIN_NS=60_000_000_000
MINUTES_PER_DAY=1440
OOS_START=368
OOS_END=728
FOLD_DAYS=30
ASSETS=('BTC','ETH')
ASSET_WEIGHT={'BTC':0.5,'ETH':0.5}
sys.path.insert(0,str(ROOT/'research/automation'))
import registry
kernel_path=ROOT/'research/experiments/20261001T133655Z/kernel.py'
s=importlib.util.spec_from_file_location('daily_vbreak_kernel',kernel_path)
kernel=importlib.util.module_from_spec(s);sys.modules[s.name]=kernel;s.loader.exec_module(kernel)

def sha(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()
def stamp_ms(ms:int)->str:return datetime.fromtimestamp(ms/1000,timezone.utc).isoformat().replace('+00:00','Z')
def stamp_ns(ns:int)->str:return datetime.fromtimestamp(ns/1e9,timezone.utc).isoformat().replace('+00:00','Z')
def canonical(value):return json.loads(json.dumps(value,default=str,ensure_ascii=False,allow_nan=False))
def quantile_linear(values, q):
    ordered=sorted(float(x) for x in values)
    if not ordered:raise ValueError('empty volatility reference')
    at=(len(ordered)-1)*q
    lo=int(math.floor(at));hi=int(math.ceil(at));w=at-lo
    return ordered[lo]*(1-w)+ordered[hi]*w

def load_asset(asset):
    paths=[
      ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20240916T000000Z_20250916T000000Z_transfer_20261001/spot_bars.parquet',
      ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20250916T000000Z_20260916T000000Z_archive_20260929/spot_bars.parquet'
    ]
    frames=[];files=[]
    for p in paths:
        frame=pl.read_parquet(p,columns=['open_ts','available_ts','open','close','base_volume','quote_volume','is_closed'])
        if frame.height!=365*MINUTES_PER_DAY or not frame['is_closed'].all() or not frame['open_ts'].is_sorted():
            raise ValueError(f'invalid normalized source: {p}')
        if not (frame['open_ts'].diff().drop_nulls()==MIN_NS).all():raise ValueError(f'minute gap inside {p}')
        if not (frame['available_ts']==frame['open_ts']+MIN_NS).all():raise ValueError(f'close availability mismatch: {p}')
        if not (frame['open']>0).all() or not (frame['close']>0).all():raise ValueError(f'nonpositive price: {p}')
        files.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size,
                      'bars':frame.height,'first_open_ns':int(frame['open_ts'][0]),'last_open_ns':int(frame['open_ts'][-1])})
        frames.append(frame)
    minute=pl.concat(frames,how='vertical_relaxed').sort('open_ts')
    if minute.height!=730*MINUTES_PER_DAY or not (minute['open_ts'].diff().drop_nulls()==MIN_NS).all():
        raise ValueError(f'asset minute continuity/length failed: {asset}')
    if int(minute['open_ts'][0])!=1726444800*1_000_000_000:
        raise ValueError(f'unexpected first timestamp {asset}')
    daily=minute.with_columns((pl.col('open_ts')//DAY_NS).alias('day')).group_by('day').agg(
        pl.col('close').last(),pl.col('quote_volume').sum().alias('quote_volume'),
        pl.col('available_ts').last().alias('available_ts')
    ).sort('day')
    rows=[]
    for day,close,qv,avail in zip(daily['day'].to_list(),daily['close'].to_list(),daily['quote_volume'].to_list(),daily['available_ts'].to_list()):
        rows.append({'day_open_ns':int(day)*DAY_NS,'date':stamp_ns(int(day)*DAY_NS)[:10],
                     'close':D(str(close)),'quote_volume':D(str(qv)),'close_available_ns':int(avail)})
    if len(rows)!=730 or rows[0]['date']!='2024-09-16' or rows[-1]['date']!='2026-09-15':
        raise ValueError(f'daily aggregation boundary error for {asset}')
    if not (minute['base_volume']>=0).all() or not (minute['quote_volume']>=0).all():
        raise ValueError(f'negative volume {asset}')
    data={
      'asset':asset,'files':files,'daily':rows,
      'minute_open':[D(str(x)) for x in minute['open'].to_list()],
      'minute_close':minute['close'].cast(pl.Float64).to_numpy(),
      'minute_base':minute['base_volume'].to_list(),
      'minute_quote':minute['quote_volume'].to_list(),
      'minute_ts':minute['open_ts'].to_numpy()
    }
    data['daily_close_sha256_f64le']=hashlib.sha256(np.asarray([float(x['close']) for x in rows],dtype='<f8').tobytes()).hexdigest()
    return data

def build_features(rows, short_days=10, ref_days=180, q=20):
    closes=[float(r['close']) for r in rows]
    vols=[None]*len(rows)
    for j in range(short_days,len(rows)):
        rets=[math.log(closes[k]/closes[k-1]) for k in range(j-short_days+1,j+1)]
        vols[j]=statistics.stdev(rets)
    squeezed=[False]*len(rows)
    for j in range(ref_days+short_days,len(rows)):
        reference=[vols[k] for k in range(j-ref_days,j)]
        if len(reference)!=ref_days or any(v is None for v in reference):raise ValueError('invalid squeeze reference')
        squeezed[j]=vols[j]<=quantile_linear(reference,q/100)
    return {'closes':closes,'volatility':vols,'squeezed':squeezed}

def lagged_cost_inputs(rows,i):
    if i<21:raise ValueError('need 21 prior complete daily closes for cost inputs')
    adv=sum((D(x['quote_volume']) for x in rows[i-20:i]),D(0))/D(20)
    closes=[float(x['close']) for x in rows[i-21:i]]
    sigma=statistics.stdev([math.log(b/a) for a,b in zip(closes,closes[1:])])
    return adv,D(str(sigma))

def vw5(market,exec_i,ref):
    q=sum((D(str(x)) for x in market['minute_quote'][exec_i-5:exec_i]),D(0))
    b=sum((D(str(x)) for x in market['minute_base'][exec_i-5:exec_i]),D(0))
    return q/b if b>0 else ref

def metric(nav,ppy=365):
    a=np.asarray(nav,dtype=np.float64)
    if len(a)<2 or not np.all(np.isfinite(a)) or not np.all(a>0):raise ValueError('invalid equity vector')
    r=a[1:]/a[:-1]-1;sd=float(np.std(r,ddof=1)) if len(r)>1 else 0.0
    peak=np.maximum.accumulate(a);dd=1-a/peak
    cagr=(a[-1]/a[0])**(ppy/max(len(a)-1,1))-1
    maxdd=float(dd.max()*100);mean=float(r.mean()) if len(r) else 0.0
    sharpe=mean/sd*math.sqrt(ppy) if sd else None
    return {'net_return_pct':float((a[-1]/a[0]-1)*100),'max_drawdown_pct':maxdd,
            'sharpe_annualized_daily':sharpe,'cagr_pct':float(cagr*100),
            'calmar':float(cagr/(maxdd/100)) if maxdd else None,'observations':len(a)-1}

def maxdd_stream(arrays, initial):
    peak=float(initial);worst=0.0;count=0;digest=hashlib.sha256()
    first=np.asarray([initial],dtype='<f8');digest.update(first.tobytes());count+=1
    for values in arrays:
        x=np.asarray(values,dtype=np.float64)
        if not len(x):continue
        local_peak=np.maximum.accumulate(x)
        local_peak=np.maximum(local_peak,peak)
        worst=max(worst,float(np.max(1.0-x/local_peak)))
        peak=max(peak,float(np.max(x)))
        digest.update(np.asarray(x,dtype='<f8').tobytes());count+=len(x)
    return worst*100,count,digest.hexdigest()

def signals_for(spec,markets):
    p=spec['parameters'];rows={a:markets[a]['daily'] for a in ASSETS}
    feats={a:build_features(rows[a],p['short_realized_vol_days'],p['compression_reference_days'],p['compression_percentile']) for a in ASSETS}
    signal_map={a:[] for a in ASSETS}
    for asset in ASSETS:
        r=rows[asset];cl=feats[asset]['closes'];sq=feats[asset]['squeezed'];L=p['entry_breakout_lookback_days'];X=p['exit_close_channel_lookback_days']
        for i in range(OOS_START,OOS_END):
            j=i-1;decision_ns=r[i]['day_open_ns'];execution_ns=decision_ns+MIN_NS
            if r[j]['close_available_ns']>decision_ns:raise ValueError('signal close not available at decision boundary')
            recent=any(sq[k] for k in range(j-2,j+1))
            upper=max(cl[j-L:j]);lower=min(cl[j-X:j]);close=cl[j]
            enter=recent and close>upper;exit_long=close<lower
            signal_map[asset].append({'i':i,'j':j,'decision_utc':stamp_ns(decision_ns),'execution_utc':stamp_ns(execution_ns),
                'close':close,'upper_exclusive_close_channel':upper,'lower_exclusive_close_channel':lower,
                'recent_compression':recent,'compression_values':sq[j-2:j+1],
                'entry':enter,'exit':exit_long})
    return signal_map

def simulate(spec,markets,filters,mult,signal_map):
    cash={a:D('1000') for a in ASSETS};units={a:D(0) for a in ASSETS};trades=[];events=[];daily_nav=[2000.0];nav_segments=[];peak=2000.0;worst=0.0
    rows={a:markets[a]['daily'] for a in ASSETS}
    for offset,i in enumerate(range(OOS_START,OOS_END)):
        day_signals={a:signal_map[a][offset] for a in ASSETS}
        fills=[]
        for asset in ASSETS:
            sig=day_signals[asset];ref=markets[asset]['minute_open'][i*MINUTES_PER_DAY+1]
            if units[asset]>0 and sig['exit']:buy=False;reason='close_channel_exit'
            elif units[asset]==0 and sig['entry']:buy=True;reason='compression_breakout_entry'
            else:continue
            exec_i=i*MINUTES_PER_DAY+1
            adv,sigma=lagged_cost_inputs(rows[asset],i)
            avg=vw5(markets[asset],exec_i,ref)
            cb,ub,trade=kernel.fill(cash[asset],units[asset],buy,ref,adv,sigma,mult,filters[asset+'USDT'],avg)
            before={'cash':str(cash[asset]),'units':str(units[asset])}
            trade.update({'asset':asset,'date_utc':rows[asset][i]['date'],'reason':reason,
                'signal_available_utc':stamp_ns(rows[asset][i]['day_open_ns']),
                'execution_utc':stamp_ns(int(markets[asset]['minute_ts'][exec_i])),
                'signal_close_utc':stamp_ns(rows[asset][i]['day_open_ns']),
                'signal_close':str(sig['close']),'cash_before':before['cash'],'units_before':before['units'],
                'cash_after':str(cb),'units_after':str(ub),'cost_multiplier':mult,
                'signal_entry':sig['entry'],'signal_exit':sig['exit'],'recent_compression':sig['recent_compression']})
            trades.append(trade)
            if trade['status']=='filled':
                cash[asset],units[asset]=cb,ub
                fills.append((asset,ref))
        # One common post-fill mark after both independent sleeves have executed.
        if fills:
            nav_ref=sum((cash[a]+units[a]*markets[a]['minute_open'][i*MINUTES_PER_DAY+1] for a in ASSETS),D(0))
            nav_segments.append(np.asarray([float(nav_ref)]))
            events.append({'day':rows['BTC'][i]['date'],'time_utc':stamp_ns(rows['BTC'][i]['day_open_ns']+MIN_NS),'nav_after_fills_usdt':str(nav_ref),'fills':[a for a,_ in fills]})
        # One-minute close NAV samples, from after 00:01 fills through the next 00:01 execution instant.
        begin=i*MINUTES_PER_DAY+1;end=(i+1)*MINUTES_PER_DAY+1
        btc=markets['BTC']['minute_close'][begin:end];eth=markets['ETH']['minute_close'][begin:end]
        arr=float(cash['BTC']+units['BTC']*D('0')) + np.float64(units['BTC'])*btc + float(cash['ETH']) + np.float64(units['ETH'])*eth
        if len(arr)!=(MINUTES_PER_DAY):raise ValueError(f'minute mark slice length {i}: {len(arr)}')
        nav_segments.append(arr)
        daily_nav.append(float(cash['BTC']+units['BTC']*rows['BTC'][i]['close']+cash['ETH']+units['ETH']*rows['ETH'][i]['close']))
    # Costed liquidation at the first 00:01 UTC open after the OOS window.
    terminal_i=OOS_END*MINUTES_PER_DAY+1
    for asset in ASSETS:
        if units[asset]<=0:continue
        ref=markets[asset]['minute_open'][terminal_i];adv,sigma=lagged_cost_inputs(rows[asset],OOS_END)
        avg=vw5(markets[asset],terminal_i,ref)
        cb,ub,trade=kernel.fill(cash[asset],units[asset],False,ref,adv,sigma,mult,filters[asset+'USDT'],avg)
        trade.update({'asset':asset,'date_utc':rows[asset][OOS_END]['date'],'reason':'terminal_costed_exit',
            'signal_available_utc':stamp_ns(rows[asset][OOS_END]['day_open_ns']),
            'execution_utc':stamp_ns(int(markets[asset]['minute_ts'][terminal_i])),
            'cash_before':str(cash[asset]),'units_before':str(units[asset]),
            'cash_after':str(cb),'units_after':str(ub),'cost_multiplier':mult,'terminal':True})
        trades.append(trade)
        if trade['status']=='filled':cash[asset],units[asset]=cb,ub
    terminal_nav=cash['BTC']+cash['ETH']+units['BTC']*markets['BTC']['minute_open'][terminal_i]+units['ETH']*markets['ETH']['minute_open'][terminal_i]
    nav_segments.append(np.asarray([float(terminal_nav)]));daily_nav.append(float(terminal_nav))
    dd,nmarks,minute_hash=maxdd_stream(nav_segments,2000.0)
    # Folds use the continuous daily close NAV and carry actual cash/units across boundaries.
    folds=[]
    for f in range(12):
        a=f*FOLD_DAYS;b=a+FOLD_DAYS
        values=[2000.0 if a==0 else daily_nav[a]]+daily_nav[a+1:b+1]
        if f==11:values.append(daily_nav[-1])  # include the scheduled terminal exit cost in fold 12
        folds.append({'fold':f+1,'start_utc':rows['BTC'][OOS_START+a]['date']+'T00:01:00Z',
            'end_exclusive_utc':rows['BTC'][OOS_START+b]['date']+'T00:01:00Z',
            **metric(values),'round_trips':0,'executions':0})
    # Correct fold round-trip counts with timestamps, independently of the metrics row.
    for f,row in enumerate(folds):
        a=OOS_START+f*FOLD_DAYS;b=a+FOLD_DAYS
        row['round_trips']=sum(1 for t in trades if t['side']=='sell' and t.get('date_utc','')>=rows['BTC'][a]['date'] and t.get('date_utc','')<rows['BTC'][b]['date'])
        row['executions']=sum(1 for t in trades if t.get('date_utc','')>=rows['BTC'][a]['date'] and t.get('date_utc','')<rows['BTC'][b]['date'])
    filled=[t for t in trades if t['status']=='filled']
    parts={k:str(sum((D(t['cost_parts'][k]) for t in filled),D(0))) for k in ('fee','half_spread','slippage','impact','tick_rounding')}
    total_cost=sum((D(x) for x in parts.values()),D(0))
    net=terminal_nav-D(2000);gross=net+total_cost
    daily_stats=metric(daily_nav)
    return {'cost_multiplier':mult,'net_pnl_usdt':str(net),'terminal_nav_usdt':str(terminal_nav),
        'net_return_pct':float(net/D(2000)*100),'gross_reference_pnl_usdt':str(gross),
        'gross_reference_pnl_to_cost':float(gross/total_cost) if total_cost else None,
        'cost_usdt':str(total_cost),'cost_parts_usdt':parts,'executions':len(filled),
        'round_trips':sum(t['side']=='sell' for t in filled),'signal_triggers':sum(sum(x['entry'] or x['exit'] for x in signal_map[a]) for a in ASSETS),
        'positive_folds':sum(f['net_return_pct']>0 for f in folds),'folds':folds,
        'sampled_1m_nav_drawdown_pct':dd,'drawdown_sample_count':nmarks,
        'drawdown_scope':'1-minute close samples plus post-fill reference marks; excludes intra-minute extrema',
        'daily_nav_drawdown_pct':daily_stats['max_drawdown_pct'],'daily_nav_usdt':daily_nav,
        'minute_nav_sha256_f64le':minute_hash,
        'minute_nav_samples':nmarks,'terminal_flat':units['BTC']==0 and units['ETH']==0,
        'rejected_orders':sum(t['status']!='filled' for t in trades),
        'capacity_rejections':sum(t.get('reason')=='participation' for t in trades if t['status']!='filled'),
        'rejection_reasons':{reason:sum(t.get('reason')==reason for t in trades if t['status']!='filled')
           for reason in sorted({t.get('reason') for t in trades if t['status']!='filled'})},
        'trades':trades,'events':events}

def main():
    batch=json.loads((ROUND/'batch.json').read_text())
    plan=json.loads((ROUND/'plan.json').read_text())
    ledger=registry.read_records(ROOT/'research/automation/registry.jsonl')
    for item in batch:
        spec=json.loads((ROOT/item['spec']).read_text())
        fp=registry.fingerprint(spec)
        item['fingerprint']=fp
        if ledger.get(fp,{}).get('status')!='reserved':raise ValueError(f'{item["name"]} not reserved before eval')
    (ROUND/'batch.json').write_text(json.dumps(batch,indent=2,ensure_ascii=False)+'\n')
    filters_doc=json.loads((ROOT/'research/experiments/20261013T164415Z/exchange_filters.json').read_text())
    filters={asset+'USDT': {x['filterType']:x for x in filters_doc['symbols'][asset]} for asset in ASSETS}
    markets={asset:load_asset(asset) for asset in ASSETS}
    (ROUND/'exchange_filters.json').write_bytes((ROOT/'research/experiments/20261013T164415Z/exchange_filters.json').read_bytes())
    manifest={'assets':{a:{'source_files':markets[a]['files'],'minutes':len(markets[a]['minute_ts']),
        'daily_bars':len(markets[a]['daily']),'daily_close_sha256_f64le':markets[a]['daily_close_sha256_f64le'],
        'first_minute_utc':stamp_ns(int(markets[a]['minute_ts'][0])),
        'last_minute_utc':stamp_ns(int(markets[a]['minute_ts'][-1]))} for a in ASSETS},
        'exchange_filter_snapshot_path':'research/experiments/20261013T164415Z/exchange_filters.json',
        'exchange_filter_snapshot_sha256':sha(ROUND/'exchange_filters.json'),
        'execution_kernel_sha256':sha(kernel_path),
        'registry_sha256_at_evaluation_start':sha(ROOT/'research/automation/registry.jsonl'),
        'registry_committed_base_sha256':hashlib.sha256(__import__('subprocess').check_output(['git','show','HEAD:research/automation/registry.jsonl'],cwd=ROOT)).hexdigest(),
        'registry_committed_base_commit':plan['source_repository_commit']}
    (ROUND/'data_manifest.json').write_text(json.dumps(canonical(manifest),indent=2,ensure_ascii=False)+'\n')
    cfg={};fold_rows=[];cost_rows=[];curve_rows=[]
    for item in batch:
        spec=json.loads((ROOT/item['spec']).read_text());sig=signals_for(spec,markets)
        scenes={}
        for mult in (1,2,3):
            scene=simulate(spec,markets,filters,mult,sig);scenes[str(mult)]=scene
            for f in scene['folds']:fold_rows.append({'name':item['name'],'cost_multiplier':mult,**f})
            cost_rows.append({'name':item['name'],'fingerprint':item['fingerprint'],'cost_multiplier':mult,
              **{k:scene[k] for k in ('net_return_pct','net_pnl_usdt','cost_usdt','cost_parts_usdt',
                'gross_reference_pnl_to_cost','executions','round_trips','signal_triggers','positive_folds',
                'sampled_1m_nav_drawdown_pct','daily_nav_drawdown_pct','rejected_orders','capacity_rejections',
                'terminal_flat','rejection_reasons')}})
            for d,nav in enumerate(scene['daily_nav_usdt']):
                date=markets['BTC']['daily'][OOS_START+d]['date'] if d>0 else markets['BTC']['daily'][OOS_START]['date']
                curve_rows.append({'name':item['name'],'fingerprint':item['fingerprint'],'cost_multiplier':mult,'sample_index':d,'date_utc':date,'nav_usdt':nav})
        cfg[item['name']]={'fingerprint':item['fingerprint'],'spec_path':item['spec'],
            'parameters':spec['parameters'],'signal_triggers':{a:[x for x in sig[a] if x['entry'] or x['exit']] for a in ASSETS},
            'signal_trigger_counts':{a:{'entries':sum(x['entry'] for x in sig[a]),'exits':sum(x['exit'] for x in sig[a]),'compression_days':sum(x['recent_compression'] for x in sig[a])} for a in ASSETS},'scenarios':scenes}
        print(json.dumps({'completed':item['name'],'returns_pct':[scenes[str(m)]['net_return_pct'] for m in (1,2,3)]}),flush=True)
    # Local sensitivity is the predeclared Chebyshev neighborhood (at most one step on each axis).
    vals={key:plan['parameter_grid'][key] for key in ('entry_breakout_lookback_days','exit_close_channel_lookback_days','compression_percentile')}
    for item in batch:
        name=item['name'];p=cfg[name]['parameters'];neighbors=[]
        for other in batch:
            q=cfg[other['name']]['parameters']
            if all(abs(vals[key].index(p[key])-vals[key].index(q[key]))<=1 for key in vals):neighbors.append(other['name'])
        frac=sum(cfg[x]['scenarios']['3']['net_return_pct']>0 for x in neighbors)/len(neighbors)
        c=cfg[name]['scenarios']
        gates={
          'all_cost_scenarios_positive':all(c[str(m)]['net_return_pct']>0 for m in (1,2,3)),
          'positive_1x_folds_at_least_8':c['1']['positive_folds']>=8,
          'sampled_1m_drawdown_3x_at_most_25pct':c['3']['sampled_1m_nav_drawdown_pct']<=25,
          'local_3x_positive_fraction_at_least_0_60':frac>=0.60,
          'round_trips_1x_at_least_4':c['1']['round_trips']>=4,
          'gross_reference_pnl_to_1x_cost_at_least_2_5':c['1']['gross_reference_pnl_to_cost'] is not None and c['1']['gross_reference_pnl_to_cost']>=2.5,
          'zero_rejected_or_capacity_orders':all(c[str(m)]['rejected_orders']==0 and c[str(m)]['capacity_rejections']==0 for m in (1,2,3)),
          'terminal_flat_all_scenes':all(c[str(m)]['terminal_flat'] for m in (1,2,3))
        }
        cfg[name]['sensitivity']={'local_neighbor_names':neighbors,'local_neighbor_count':len(neighbors),
            'local_3x_positive_fraction':frac,'gates':gates,
            'status':'passed' if all(gates.values()) else 'rejected'}
        for m in ('1','2','3'):
            cfg[name]['scenarios'][m].pop('daily_nav_usdt')
    base_path=ROOT/'research/experiments/20261013T123949Z/report.json';base=json.loads(base_path.read_text())
    base_cfg=base['configs']['hold_360d_btc_eth_50_50_relative_strength_study']
    baselines={str(k):{'net_return_pct':v['net_return_pct'],'max_drawdown_pct':v['max_drawdown_pct'],
       'net_pnl_usdt':v.get('net_pnl_usdt'),'cost_usdt':v.get('cost_usdt'),'round_trips':v.get('round_trips'),
       'source_report':'research/experiments/20261013T123949Z/report.json'}
       for k,v in base_cfg['scenarios'].items()}
    summary={'candidate_configs':len(batch),'candidate_passed':sum(cfg[x['name']]['sensitivity']['status']=='passed' for x in batch),
       'candidate_rejected':sum(cfg[x['name']]['sensitivity']['status']=='rejected' for x in batch),
       'oos_days':360,'walk_forward_folds':12,'cost_scenes':len(cost_rows),
       'registry_events_before_round':plan['preexisting_trial_context']['registry_events_at_freeze'],
       'registry_unique_fingerprints_before_round':max(0,len(ledger)-len(batch)),
       'positive_configs_by_cost_multiplier':{m:sum(cfg[x['name']]['scenarios'][m]['net_return_pct']>0 for x in batch) for m in ('1','2','3')},
       'positive_1x_fold_count_range':[min(cfg[x['name']]['scenarios']['1']['positive_folds'] for x in batch),max(cfg[x['name']]['scenarios']['1']['positive_folds'] for x in batch)],
       'new_specs_reserved':len(batch),'ranking_1x':sorted(cfg,key=lambda n:cfg[n]['scenarios']['1']['net_return_pct'],reverse=True)}
    report={'round':ROUND.name,'evaluation_started_utc':datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),
      'plan':plan,'data_manifest':manifest,'summary':summary,'matched_existing_buy_hold_50_50':baselines,
      'configs':cfg,'cost_scenarios':cost_rows,'integrity_audit':{'status':'pending','checks':[]},
      'artifacts':{'fold_results_csv':'research/experiments/'+ROUND.name+'/fold_results.csv',
        'cost_scenarios_csv':'research/experiments/'+ROUND.name+'/cost_scenarios.csv',
        'equity_curves_daily_csv':'research/experiments/'+ROUND.name+'/equity_curves_daily.csv',
        'sensitivity_csv':'research/experiments/'+ROUND.name+'/sensitivity.csv',
        'sensitivity_surface_svg':'research/experiments/'+ROUND.name+'/sensitivity_surface.svg',
        'data_manifest':'research/experiments/'+ROUND.name+'/data_manifest.json'}}
    (ROUND/'report.json').write_text(json.dumps(canonical(report),indent=2,ensure_ascii=False)+'\n')
    with (ROUND/'fold_results.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['name','cost_multiplier','fold','start_utc','end_exclusive_utc','net_return_pct',
           'max_drawdown_pct','sharpe_annualized_daily','cagr_pct','calmar','observations','round_trips','executions'],lineterminator='\n');w.writeheader();w.writerows(fold_rows)
    with (ROUND/'cost_scenarios.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(cost_rows[0]),lineterminator='\n');w.writeheader()
        for x in cost_rows:
            row=dict(x);row['cost_parts_usdt']=json.dumps(row['cost_parts_usdt'],sort_keys=True);row['rejection_reasons']=json.dumps(row['rejection_reasons'],sort_keys=True);w.writerow(row)
    with (ROUND/'equity_curves_daily.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(curve_rows[0]),lineterminator='\n');w.writeheader();w.writerows(curve_rows)
    sensitivity=[]
    for item in batch:
        c=cfg[item['name']];sens=c['sensitivity'];r={'name':item['name'],'entry_lookback_days':item['entry_breakout_lookback_days'],
           'exit_lookback_days':item['exit_close_channel_lookback_days'],'compression_percentile':item['compression_percentile'],
           'net_return_1x_pct':c['scenarios']['1']['net_return_pct'],'net_return_2x_pct':c['scenarios']['2']['net_return_pct'],
           'net_return_3x_pct':c['scenarios']['3']['net_return_pct'],'sampled_1m_drawdown_3x_pct':c['scenarios']['3']['sampled_1m_nav_drawdown_pct'],
           'positive_1x_folds':c['scenarios']['1']['positive_folds'],'round_trips_1x':c['scenarios']['1']['round_trips'],
           'local_3x_positive_fraction':sens['local_3x_positive_fraction'],'status':sens['status']}
        r.update({'gate_failures':','.join(k for k,v in sens['gates'].items() if not v)})
        sensitivity.append(r)
    with (ROUND/'sensitivity.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(sensitivity[0]),lineterminator='\n');w.writeheader();w.writerows(sensitivity)
    cells=[];svg=['<svg xmlns="http://www.w3.org/2000/svg" width="940" height="350" viewBox="0 0 940 350">',
      '<style>text{font-family:Arial,sans-serif;font-size:13px}.title{font-size:17px;font-weight:bold}.cell{stroke:#fff;stroke-width:2}</style>',
      '<text x="18" y="24" class="title">3x-cost net return: breakout × exit channel, by squeeze percentile</text>']
    for qi,q in enumerate(vals['compression_percentile']):
        x0=24+qi*305;svg.append(f'<text x="{x0}" y="52" class="title">Compression q≤{q}%</text>')
        svg.append(f'<text x="{x0}" y="76">Exit lookback days →</text>')
        for xi,xv in enumerate(vals['exit_close_channel_lookback_days']):svg.append(f'<text x="{x0+86+xi*62}" y="98">{xv}</text>')
        for ei,ev in enumerate(vals['entry_breakout_lookback_days']):
            y=120+ei*61;svg.append(f'<text x="{x0}" y="{y+30}">Entry {ev}d</text>')
            for xi,xv in enumerate(vals['exit_close_channel_lookback_days']):
                name=f'vbreak_e{ev}_x{xv}_q{q}';v=cfg[name]['scenarios']['3']['net_return_pct'];color='#39a873' if v>0 else '#c95f57';x=x0+68+xi*62
                svg.append(f'<rect class="cell" x="{x}" y="{y}" width="58" height="54" rx="4" fill="{color}"/>')
                svg.append(f'<text x="{x+5}" y="{y+30}" fill="#fff">{v:.1f}%</text>')
    svg.append('<text x="24" y="329">Every configuration failed at least one predeclared gate; historical sample is reused, not an untouched holdout.</text></svg>')
    (ROUND/'sensitivity_surface.svg').write_text('\n'.join(svg)+'\n')
    print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
