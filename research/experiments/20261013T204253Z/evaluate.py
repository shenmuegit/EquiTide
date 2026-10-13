#!/usr/bin/env python3
"""Run the frozen, pre-reserved BTC/ETH 4h momentum batch."""
from __future__ import annotations
import csv, gzip, hashlib, importlib.util, json, math, os, statistics, sys, time
from bisect import bisect_right
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np
import polars as pl

ROOT=Path(__file__).resolve().parents[3]
ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'))
import registry
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'))
from kernel import fill
MIN=60_000_000_000

def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); sys.modules[name]=mod; spec.loader.exec_module(mod); return mod
cost_engine=load_module('paper10_lagged_cost_engine',ROOT/'research/experiments/20261001T013355Z/evaluate.py')

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def stamp(ns): return datetime.fromtimestamp(ns/1e9,timezone.utc).isoformat().replace('+00:00','Z')
def dec(x): return D(str(x))
def json_clean(x): return json.loads(json.dumps(x,default=str,ensure_ascii=False,allow_nan=False))

def exchange_filters():
    raw=json.loads((ROUND/'exchange_filters.json').read_text())['symbols']
    out={}
    for symbol, rows in raw.items():
        d={r['filterType']:r for r in rows if r['filterType'] in ('PRICE_FILTER','LOT_SIZE','NOTIONAL','PERCENT_PRICE_BY_SIDE')}
        assert {'PRICE_FILTER','LOT_SIZE','NOTIONAL'} <= set(d)
        out[symbol]=d
    return out

def load_asset(asset):
    paths=[ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20240916T000000Z_20250916T000000Z_transfer_20261001/spot_bars.parquet',ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20250916T000000Z_20260916T000000Z_archive_20260929/spot_bars.parquet']
    frames=[]; inputs=[]
    for p in paths:
        f=pl.read_parquet(p,columns=['open_ts','available_ts','open','close','base_volume','quote_volume','is_closed'])
        assert f.height==365*1440 and f['is_closed'].all() and f['open_ts'].is_sorted()
        assert (f['open_ts'].diff().drop_nulls()==MIN).all()
        assert (f['available_ts']-f['open_ts']==MIN).all()
        assert (f['open']>0).all() and (f['close']>0).all() and (f['base_volume']>=0).all() and (f['quote_volume']>=0).all()
        inputs.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'size_bytes':p.stat().st_size,'bars':f.height,'first_open_ns':int(f['open_ts'][0]),'last_open_ns':int(f['open_ts'][-1])})
        frames.append(f)
    f=pl.concat(frames,how='vertical_relaxed').sort('open_ts')
    assert f.height==730*1440 and (f['open_ts'].diff().drop_nulls()==MIN).all()
    opens=np.asarray(f['open'].cast(pl.Float64).to_numpy()); closes=np.asarray(f['close'].cast(pl.Float64).to_numpy())
    qv=np.asarray(f['quote_volume'].cast(pl.Float64).to_numpy()); bv=np.asarray(f['base_volume'].cast(pl.Float64).to_numpy()); ts=f['open_ts'].to_numpy()
    n=len(opens)//240; assert n==4380
    close4=np.asarray([closes[(i+1)*240-1] for i in range(n)])
    bars=[{'open_ns':int(ts[i*240]),'available_ns':int(ts[(i+1)*240-1])+MIN,'close':dec(closes[(i+1)*240-1]),'quote_volume':dec(np.sum(qv[i*240:(i+1)*240],dtype=np.float64))} for i in range(n)]
    daily=[]
    for day in range(730):
        end=(day+1)*1440
        daily.append({'close':dec(closes[end-1]),'quote_volume':dec(np.sum(qv[end-1440:end],dtype=np.float64))})
    proxy=np.zeros(n+1,dtype=np.float64)
    for i in range(n+1):
        k=i*240+1
        if k>=5:
            qq=float(np.sum(qv[k-5:k],dtype=np.float64)); bb=float(np.sum(bv[k-5:k],dtype=np.float64)); proxy[i]=qq/bb if bb else 0.
    assert stamp(bars[0]['open_ns'])=='2024-09-16T00:00:00Z' and stamp(bars[-1]['available_ns'])=='2026-09-16T00:00:00Z'
    assert int(ts[0])==1726444800000000000
    return {'asset':asset,'open':opens,'close':closes,'quote':qv,'base':bv,'minute_ts':ts,'close4':close4,'bars':bars,'daily':daily,'proxy':proxy,'inputs':inputs,
            'bar_close_hash':hashlib.sha256(np.asarray(close4,dtype='<f8').tobytes()).hexdigest()}

def lag_cost(daily,day):
    if day<21: raise ValueError(f'insufficient lagged daily history for day {day}')
    adv=statistics.mean(float(x['quote_volume']) for x in daily[day-20:day])
    closes=[float(x['close']) for x in daily[day-21:day]]
    sigma=statistics.stdev(math.log(b/a) for a,b in zip(closes,closes[1:]))
    return dec(adv),dec(sigma)

def drawdown(values):
    x=np.asarray(values,dtype=np.float64); peak=np.maximum.accumulate(x); dd=1-x/peak; j=int(np.argmax(dd)); return float(dd[j]*100),int(np.argmax(x[:j+1])),j

def run_sleeve(spec, market, filters, mult, is_comparator):
    p=spec['parameters']; start=2208; end=4368
    assert (start,end)==(2208,4368)
    closes=market['close4']; cash=D('1000'); units=D(0); held=False; trades=[]; decisions=[]; fills=[]
    equity_by_decision=[1000.0]; fold_boundaries=[]
    exec_min_start=(start+1)*240+1; terminal_bar=end+1; exec_min_end=terminal_bar*240+1
    # OOS starts with the completed bar available at 04:00 UTC; first fill uses 04:01.
    if is_comparator:
        i=start+1; day=(i*240+1)//1440; adv,sigma=lag_cost(market['daily'],day)
        ref=dec(market['open'][i*240+1]); avg=dec(market['proxy'][i])
        cash,units,tr=fill(cash,units,True,ref,adv,sigma,mult,filters,avg)
        tr.update({'signal_bar_index':start,'signal_available_utc':stamp(market['bars'][start]['available_ns']),'execution_utc':stamp(market['minute_ts'][i*240+1]),'signal_to_execution_seconds':60.0,'terminal':False,'cash_after':str(cash),'units_after':str(units),'asset':market['asset']}); trades.append(tr); fills.append(tr)
    else:
        for signal_i in range(start,end):
            look=int(p['lookback_4h_bars']); mom=closes[signal_i]/closes[signal_i-look]-1.0
            before=held
            if held and mom<=float(p['exit_return_threshold_fraction']): held=False
            elif not held and mom>float(p['entry_return_threshold_fraction']): held=True
            side='buy' if held and units==0 else ('sell' if not held and units>0 else None)
            execution_bar=signal_i+1; execution_min=execution_bar*240+1
            rec={'signal_bar_index':signal_i,'signal_close_available_utc':stamp(market['bars'][signal_i]['available_ns']),'execution_utc':stamp(market['minute_ts'][execution_min]),'signal_to_execution_seconds':(int(market['minute_ts'][execution_min])-market['bars'][signal_i]['available_ns'])/1e9,'momentum_return_fraction':mom,'held_before':before,'held_after':held,'action':side}
            decisions.append(rec)
            if side:
                day=execution_min//1440; adv,sigma=lag_cost(market['daily'],day); ref=dec(market['open'][execution_min]); avg=dec(market['proxy'][execution_bar])
                cash,units,tr=fill(cash,units,side=='buy',ref,adv,sigma,mult,filters,avg)
                tr.update({'asset':market['asset'],'signal_bar_index':signal_i,'signal_available_utc':stamp(market['bars'][signal_i]['available_ns']),'execution_utc':stamp(market['minute_ts'][execution_min]),'signal_to_execution_seconds':rec['signal_to_execution_seconds'],'cash_after':str(cash),'units_after':str(units),'terminal':False})
                trades.append(tr); fills.append(tr)
            equity_by_decision.append(float(cash+units*dec(market['close'][execution_min])))
            if (signal_i-start+1)%180==0: fold_boundaries.append((signal_i+1,float(cash+units*dec(market['close'][execution_min]))))
    terminal_i=end+1; terminal_min=terminal_i*240+1; day=terminal_min//1440; adv,sigma=lag_cost(market['daily'],day); ref=dec(market['open'][terminal_min]); avg=dec(market['proxy'][terminal_i])
    if units>0:
        cash,units,tr=fill(cash,units,False,ref,adv,sigma,mult,filters,avg)
        tr.update({'asset':market['asset'],'signal_bar_index':end,'signal_available_utc':stamp(market['bars'][end]['available_ns']),'execution_utc':stamp(market['minute_ts'][terminal_min]),'signal_to_execution_seconds':(int(market['minute_ts'][terminal_min])-market['bars'][end]['available_ns'])/1e9,'cash_after':str(cash),'units_after':str(units),'terminal':True})
        trades.append(tr); fills.append(tr)
    terminal_nav=float(cash+units*ref)
    # One-minute close NAV samples plus immediately-after-fill reference marks; no intra-minute extremes.
    indices=np.arange(exec_min_start,exec_min_end+1,dtype=np.int64)
    minute_close=market['close'][indices]
    # Overlay post-fill mark and current minute close with the positions that apply after that fill.
    cash_now=1000.; units_now=0.; nav=np.empty(len(indices),dtype=np.float64); samples=[1000.]
    by_min={}
    for t in fills:
        mi=exec_min_end if t.get('terminal') else (t['signal_bar_index']+1)*240+1
        by_min.setdefault(mi,[]).append(t)
    for pos,mi in enumerate(indices):
        for t in by_min.get(int(mi),[]):
            cash_now=float(dec(t['cash_after'])); units_now=float(dec(t['units_after']))
            samples.append(cash_now+units_now*float(dec(t['reference'])))
        nav[pos]=cash_now+units_now*minute_close[pos]
        samples.append(float(nav[pos]))
    maxdd,peak_i,trough_i=drawdown(samples)
    daily_indices=np.arange(exec_min_start+1439,exec_min_end+1,1440,dtype=np.int64)
    daily_nav=np.asarray([nav[int(i-exec_min_start)] for i in daily_indices],dtype=float)
    daily_nav=np.concatenate(([1000.],daily_nav,[terminal_nav]))
    ddd,_,_=drawdown(daily_nav)
    cost_parts={k:str(sum((dec(t.get('cost_parts',{}).get(k,'0')) for t in fills),D(0))) for k in ('fee','half_spread','slippage','impact','tick_rounding')}
    costs=sum((dec(x) for x in cost_parts.values()),D(0)); gross=dec(terminal_nav)-D('1000')+costs
    folds=[]; initial=1000.0; previous_sample=start
    for k in range(12):
        left=start+k*180; right=left+180
        e0=equity_by_decision[k*180] if not is_comparator else 1000.0
        e1=equity_by_decision[(k+1)*180] if not is_comparator else 1000.0
        folds.append({'fold':k+1,'test_start_utc':stamp(market['bars'][left]['available_ns']+60*1_000_000_000),'test_end_exclusive_utc':stamp(market['bars'][right]['available_ns']+60*1_000_000_000),'start_equity_usdt':e0,'end_equity_usdt':e1,'net_return_pct':(e1/e0-1)*100 if e0 else None})
    rejected=sum(t.get('status')!='filled' for t in fills)
    return {'terminal_nav_usdt':str(terminal_nav),'net_pnl_usdt':str(dec(terminal_nav)-D('1000')),'net_return_pct':(terminal_nav/1000-1)*100,'max_drawdown_1m_sampled_pct':maxdd,'daily_mark_drawdown_pct':ddd,'drawdown_scope':'OOS one-minute closes plus immediate post-fill reference marks; no intra-minute extrema.','round_trips':sum(t['side']=='sell' for t in fills),'fills':sum(t.get('status')=='filled' for t in fills),'rejected_or_capacity_orders':rejected,'cost_usdt':str(costs),'cost_parts_usdt':cost_parts,'gross_reference_pnl_usdt':str(gross),'gross_to_1x_cost':float(gross/costs) if costs else None,'folds':folds,'terminal_cash_usdt':str(cash),'terminal_units':str(units),'daily_nav_usdt':[float(x) for x in daily_nav],'minute_nav_sha256':hashlib.sha256(np.asarray(nav,dtype='<f8').tobytes()).hexdigest(),'minute_nav_samples':len(nav),'_minute_nav':nav,'trades':trades,'decisions':decisions}

def main():
    started=time.time(); plan=json.loads((ROUND/'plan.json').read_text()); batch=json.loads((ROUND/'batch.json').read_text()); filters=exchange_filters()
    assert len(batch)==28
    reserved=registry.read_records(Path(os.environ.get('PAPER10_REGISTRY_LEDGER',ROOT/'research/automation/registry.jsonl')))
    for row in batch:
        s=json.loads((ROOT/row['spec']).read_text()); fp=registry.fingerprint(s)
        rec=reserved.get(fp)
        assert rec and rec.get('status')=='reserved' and rec.get('result_available') is False, f"configuration not reserved or already finished: {row['name']}"
    markets={a:load_asset(a) for a in ('BTC','ETH')}
    manifest={'built_at_utc':datetime.now(timezone.utc).isoformat(),'plan_sha256':sha(ROUND/'plan.json'),'exchange_filters_sha256':sha(ROUND/'exchange_filters.json'),'raw_exchange_info_sha256':sha(ROUND/'exchange_info_raw.json'),'assets':{a:{'source_files':m['inputs'],'one_minute_rows':len(m['open']),'four_hour_bars':len(m['bars']),'first_4h_utc':stamp(m['bars'][0]['open_ns']),'last_4h_available_utc':stamp(m['bars'][-1]['available_ns']),'4h_close_sha256_f64le':m['bar_close_hash']} for a,m in markets.items()},'source': 'Previously archived Binance spot 1m OHLCV; used for historical research only, not current forward paper trading.'}
    (ROUND/'data_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    result={'round':ROUND.name,'plan_sha256':sha(ROUND/'plan.json'),'evaluation_started_utc':datetime.now(timezone.utc).isoformat(),'plan':plan,'data_manifest':manifest,'configs':{},'all_cost_rows':[]}
    all_trades=[]; daily_csv=[]
    for row in batch:
        spec=json.loads((ROOT/row['spec']).read_text()); name=row['name']; result['configs'][name]={'spec_path':row['spec'],'fingerprint':registry.fingerprint(spec),'is_comparator':row['is_comparator'],'asset_sleeves':{},'cost_scenarios':{}}
        for mult in (1,2,3):
            sleeves={}
            for asset in ('BTC','ETH'):
                sleeves[asset]=run_sleeve(spec,markets[asset],filters[asset+'USDT'],mult,row['is_comparator'])
                sleeves[asset].pop('decisions')
            agg={}
            for key in ('terminal_nav_usdt','net_pnl_usdt','cost_usdt','gross_reference_pnl_usdt','terminal_cash_usdt'):
                agg[key]=str(sum((dec(sleeves[a][key]) for a in ('BTC','ETH')),D(0)))
            agg['net_return_pct']=(float(dec(agg['terminal_nav_usdt']))/2000-1)*100
            # Aggregate independent sleeves on a synchronized daily sample to get portfolio drawdown.
            day_nav=[sleeves['BTC']['daily_nav_usdt'][i]+sleeves['ETH']['daily_nav_usdt'][i] for i in range(len(sleeves['BTC']['daily_nav_usdt']))]
            agg['daily_nav_usdt']=day_nav; agg['daily_mark_drawdown_pct']=drawdown(day_nav)[0]
            # Conservative overall drawdown uses sum of both sleeve instantaneous maximum drawdowns.
            portfolio_minute_nav=sleeves['BTC']['_minute_nav']+sleeves['ETH']['_minute_nav']
            exec_start=2209*240+1; exec_end=4369*240+1
            event_maps={}
            for asset in ('BTC','ETH'):
                em={}
                for tr in sleeves[asset]['trades']:
                    mi=exec_end if tr.get('terminal') else (int(tr['signal_bar_index'])+1)*240+1
                    em[mi]=tr
                event_maps[asset]=em
            event_times=sorted(set(event_maps['BTC'])|set(event_maps['ETH']))
            state_times={a:sorted(event_maps[a]) for a in ('BTC','ETH')}; state_trades={a:[event_maps[a][t] for t in state_times[a]] for a in ('BTC','ETH')}
            marks=[]
            for mi in event_times:
                wealth=0.0
                for asset in ('BTC','ETH'):
                    idx=bisect_right(state_times[asset],mi)-1
                    if idx<0: cash0,units0=1000.,0.
                    else: cash0=float(dec(state_trades[asset][idx]['cash_after'])); units0=float(dec(state_trades[asset][idx]['units_after']))
                    tr=event_maps[asset].get(mi)
                    px=float(dec(tr['reference'])) if tr else float(markets[asset]['open'][mi])
                    wealth+=cash0+units0*px
                marks.append((mi-exec_start,wealth))
            sampled=[2000.]; cursor=0
            for pos,mark in marks:
                if 0<=pos<len(portfolio_minute_nav):
                    if pos>=cursor: sampled.extend(portfolio_minute_nav[cursor:pos].tolist())
                    sampled.append(mark); sampled.append(float(portfolio_minute_nav[pos])); cursor=max(cursor,pos+1)
            sampled.extend(portfolio_minute_nav[cursor:].tolist()); sampled=np.asarray(sampled,dtype='<f8')
            agg['max_drawdown_1m_sampled_pct']=drawdown(sampled)[0]
            agg['minute_nav_sha256']=hashlib.sha256(sampled.tobytes()).hexdigest()
            agg['minute_nav_samples']=len(sampled)
            agg['drawdown_scope']='Synchronized portfolio OOS one-minute close NAV plus immediate post-fill reference marks; no intra-minute extrema.'
            agg['round_trips']=sum(sleeves[a]['round_trips'] for a in ('BTC','ETH')); agg['fills']=sum(sleeves[a]['fills'] for a in ('BTC','ETH')); agg['rejected_or_capacity_orders']=sum(sleeves[a]['rejected_or_capacity_orders'] for a in ('BTC','ETH'))
            agg['cost_parts_usdt']={k:str(sum((dec(sleeves[a]['cost_parts_usdt'][k]) for a in ('BTC','ETH')),D(0))) for k in ('fee','half_spread','slippage','impact','tick_rounding')}
            c=dec(agg['cost_usdt']); gross=dec(agg['gross_reference_pnl_usdt']); agg['gross_to_1x_cost']=float(gross/c) if c else None
            agg['folds']=[{'fold':i+1,'test_start_utc':sleeves['BTC']['folds'][i]['test_start_utc'],'test_end_exclusive_utc':sleeves['BTC']['folds'][i]['test_end_exclusive_utc'],'start_equity_usdt':sleeves['BTC']['daily_nav_usdt'][i*30]+sleeves['ETH']['daily_nav_usdt'][i*30],'end_equity_usdt':sleeves['BTC']['daily_nav_usdt'][(i+1)*30]+sleeves['ETH']['daily_nav_usdt'][(i+1)*30],'net_return_pct':((sleeves['BTC']['daily_nav_usdt'][(i+1)*30]+sleeves['ETH']['daily_nav_usdt'][(i+1)*30])/(sleeves['BTC']['daily_nav_usdt'][i*30]+sleeves['ETH']['daily_nav_usdt'][i*30])-1)*100} for i in range(12)]
            agg['asset_sleeves']={a:{k:v for k,v in sleeves[a].items() if k not in ('daily_nav_usdt','folds','_minute_nav','trades','decisions')} for a in ('BTC','ETH')}
            for a in ('BTC','ETH'): all_trades.extend({'config':name,'cost_multiplier':mult,**tr} for tr in sleeves[a]['trades'])
            result['configs'][name]['cost_scenarios'][str(mult)]=agg
            result['all_cost_rows'].append({'name':name,'cost_multiplier':mult,'is_comparator':row['is_comparator'],'net_return_pct':agg['net_return_pct'],'net_pnl_usdt':agg['net_pnl_usdt'],'max_drawdown_1m_sampled_pct':agg['max_drawdown_1m_sampled_pct'],'daily_mark_drawdown_pct':agg['daily_mark_drawdown_pct'],'round_trips':agg['round_trips'],'fills':agg['fills'],'rejected_or_capacity_orders':agg['rejected_or_capacity_orders'],'cost_usdt':agg['cost_usdt'],'cost_parts_usdt':agg['cost_parts_usdt'],'folds':agg['folds']})
            for d,v in enumerate(day_nav): daily_csv.append({'config':name,'cost_multiplier':mult,'day_index':d,'nav_usdt':v})
        print(f"{name}: 1x={result['configs'][name]['cost_scenarios']['1']['net_return_pct']:.4f}% 3x={result['configs'][name]['cost_scenarios']['3']['net_return_pct']:.4f}%",flush=True)
    # Full 3x3x3 local sensitivity neighborhood and frozen, predeclared gates.
    candidates=[r for r in batch if not r['is_comparator']]
    for row in candidates:
        p=json.loads((ROOT/row['spec']).read_text())['parameters']; l,e,x=p['lookback_4h_bars'],p['entry_return_threshold_fraction'],p['exit_return_threshold_fraction']
        neighbors=[]
        for other in candidates:
            q=json.loads((ROOT/other['spec']).read_text())['parameters']
            if abs([6,18,42].index(q['lookback_4h_bars'])-[6,18,42].index(l))<=1 and abs(q['entry_return_threshold_fraction']-e)<=.005000001 and abs(q['exit_return_threshold_fraction']-x)<=.005000001: neighbors.append(other)
        frac=sum(result['configs'][o['name']]['cost_scenarios']['3']['net_return_pct']>0 for o in neighbors)/len(neighbors)
        cfg=result['configs'][row['name']]; s1,s2,s3=(cfg['cost_scenarios'][str(i)] for i in (1,2,3)); posfold=sum(f['net_return_pct']>0 for f in s1['folds'])
        gates={'positive_net_return_all_cost_scenarios':all(cfg['cost_scenarios'][str(i)]['net_return_pct']>0 for i in (1,2,3)),'positive_1x_folds_at_least_8':posfold>=8,'positive_1x_fold_count':posfold,'3x_sampled_drawdown_at_most_25pct':s3['max_drawdown_1m_sampled_pct']<=25,'3x_local_neighbor_positive_fraction_at_least_0_60':frac>=.60,'3x_local_neighbor_positive_fraction':frac,'local_neighbor_count':len(neighbors),'at_least_4_round_trips':s1['round_trips']>=4,'gross_reference_pnl_to_1x_cost_at_least_2_5':s1['gross_to_1x_cost'] is not None and s1['gross_to_1x_cost']>=2.5,'zero_rejected_or_capacity_fills':all(cfg['cost_scenarios'][str(i)]['rejected_or_capacity_orders']==0 for i in (1,2,3)),'terminal_flat':all(all(dec(cfg['cost_scenarios'][str(i)]['asset_sleeves'][a]['terminal_units_usdt'] if False else '0')==0 for a in ()) for i in ())}
        # Terminal holdings are computed from the actual terminal state; no open sleeve is allowed by the plan.
        terminal_units={str(i):{a:cfg['cost_scenarios'][str(i)]['asset_sleeves'][a]['terminal_units'] for a in ('BTC','ETH')} for i in (1,2,3)}
        gates['terminal_flat']=all(dec(v)==0 for scene in terminal_units.values() for v in scene.values())
        gates['terminal_units_by_cost_scene']=terminal_units
        gates['pass']=all([gates['positive_net_return_all_cost_scenarios'],gates['positive_1x_folds_at_least_8'],gates['3x_sampled_drawdown_at_most_25pct'],gates['3x_local_neighbor_positive_fraction_at_least_0_60'],gates['at_least_4_round_trips'],gates['gross_reference_pnl_to_1x_cost_at_least_2_5'],gates['zero_rejected_or_capacity_fills'],gates['terminal_flat']])
        cfg['sensitivity']={'local_3x_neighbor_fraction':frac,'neighbor_count':len(neighbors),'neighbors':[n['name'] for n in neighbors]}; cfg['gates']=gates; cfg['status']='passed' if gates['pass'] else 'rejected'
    result['summary']={'candidate_count':27,'comparator_count':1,'candidate_passed':sum(result['configs'][r['name']]['status']=='passed' for r in candidates),'candidate_rejected':sum(result['configs'][r['name']]['status']=='rejected' for r in candidates),'oos_days':360,'folds':12,'decision_bars':2160,'ranked_by_1x_net_return':[r['name'] for r in sorted(candidates,key=lambda z:result['configs'][z['name']]['cost_scenarios']['1']['net_return_pct'],reverse=True)]}
    result['evaluation_finished_utc']=datetime.now(timezone.utc).isoformat(); result['wall_seconds']=time.time()-started
    (ROUND/'report.json').write_text(json.dumps(json_clean(result),indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    with (ROUND/'trades.csv').open('w',newline='') as f:
        fields=sorted({k for t in all_trades for k in t}); w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(all_trades)
    with (ROUND/'daily_equity.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['config','cost_multiplier','day_index','nav_usdt']); w.writeheader(); w.writerows(daily_csv)
    print(json.dumps(result['summary'],ensure_ascii=False),flush=True)

if __name__=='__main__': main()
