"""Independent causal signals, Decimal inventory/cash, costs, NAV and registry audit."""
import gzip
import hashlib
import importlib.util
import json
import math
import statistics
import sys
from datetime import datetime
from decimal import Decimal as D
from pathlib import Path
import polars as pl

ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('registry_evidence',ROOT/'research/automation/registry.py');reg=importlib.util.module_from_spec(s);s.loader.exec_module(reg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def readgz(p):return json.loads(gzip.decompress(p.read_bytes()))
def near(a,b,tol=1e-7):assert abs(float(a)-float(b))<=tol,(a,b)
def metrics(equity,days,terminal):
    arr=list(map(float,equity));peak=arr[0];dd=0
    for x in arr:peak=max(peak,x);dd=max(dd,1-x/peak)
    curve=arr[:-2]+[arr[-1]] if terminal else arr
    returns=[y/x-1 for x,y in zip(curve,curve[1:])]
    sd=statistics.stdev(returns) if len(returns)>1 else 0
    cagr=(arr[-1]/arr[0])**(365/days)-1
    return {'net_return_pct':100*(arr[-1]/arr[0]-1),'max_drawdown_pct':100*dd,
      'sharpe_365':statistics.mean(returns)/sd*math.sqrt(365) if sd else None,'cagr_pct':100*cagr,'calmar':cagr/dd if dd else None}
def verify_metrics(r,equity,folds,start):
    for k,v in metrics(equity,180,True).items():
        if v is None:assert r[k] is None
        else:near(r[k],v,1e-6)
    product=1
    for j,f in enumerate(folds):
        a=f['test_start_index']-start;b=f['test_end_exclusive_index']-start
        if j==5:b=len(equity)-1
        for k,v in metrics(equity[a:b+1],30,b-a>30).items():
            if v is None:assert r['folds'][j][k] is None
            else:near(r['folds'][j][k],v,1e-6)
        product*=1+r['folds'][j]['net_return_pct']/100
    near(product,float(equity[-1])/float(equity[0]),1e-11)

report=json.loads((ROUND/'report.json').read_text());batch=json.loads((ROUND/'batch.json').read_text())
ledgerpath=ROOT/'research/automation/registry.jsonl';events=[json.loads(x) for x in ledgerpath.read_text().splitlines()];records=reg.read_records(ledgerpath)
finished='--finished' in sys.argv
assert len(batch)==len(report['configs'])==39 and len(report['folds'])==6
assert len(report['equity_timestamps_utc'])==182
for f in report['folds']:
    assert f['train_end_exclusive_index']-f['train_start_index']==180
    assert f['test_start_index']-f['train_end_exclusive_index']==3
    assert f['test_end_exclusive_index']-f['test_start_index']==30
for path,value in {**report['source_sha256'],**report['spec_sha256']}.items():assert sha(ROOT/path)==value,path
manifestrow=report['data_manifest'];assert sha(ROOT/manifestrow['path'])==manifestrow['sha256']
manifest=json.loads((ROOT/manifestrow['path']).read_text());assert len(manifest['archives'])==54 and not manifest['errors']
for row in manifest['archives']:assert sha(ROOT/row['path'])==row['sha256']==row['published_sha256']
assert sha(ROOT/report['inputs']['path'])==report['inputs']['sha256']
data=readgz(ROOT/report['inputs']['path'])
# Rebuild completed daily data directly from true normalized minute bars, not simulated output.
for asset,meta in manifest['normalized'].items():
    p=ROOT/meta['path'];assert sha(p)==meta['sha256']
    frame=pl.read_parquet(p);assert frame.height==525600 and frame['is_closed'].all()
    assert (frame['open_ts'].diff().drop_nulls()==60_000_000_000).all()
    daily=frame.group_by((pl.col('open_ts')//86_400_000_000_000).alias('day')).agg(pl.col('close').last(),pl.col('base_volume').sum().alias('volume'),pl.col('quote_volume').sum(),pl.col('available_ts').last().alias('close_available_ts')).sort('day')
    trade=frame.filter(pl.col('open_ts')%86_400_000_000_000==60_000_000_000)
    assert len(data[asset])==daily.height==trade.height==365
    for row,bar,minute in zip(data[asset],daily.to_dicts(),trade.to_dicts()):
        for key in ('close','volume','quote_volume'):assert D(row[key])==bar[key]
        assert row['day']==bar['day'] and row['close_available_ts']==bar['close_available_ts']
        assert D(row['trade_open'])==minute['open'] and row['trade_ts']==minute['open_ts']
        assert minute['available_ts']==minute['open_ts']+60_000_000_000

full={};navpoints=0;fills=0;decisionchecks=0
start=report['folds'][0]['test_start_index'];end=report['folds'][-1]['test_end_exclusive_index']
for item in batch:
    spec=json.loads((ROOT/item['spec']).read_text());assert reg.fingerprint(spec)==item['fingerprint']
    entry=records[item['fingerprint']];ev=[r for r in events if r['fingerprint']==item['fingerprint']]
    assert len(ev)==(2 if finished else 1)
    assert ev[0]['status']=='reserved' and ev[0]['recorded_at_utc']<report['evaluation_started_utc']
    row=report['configs'][item['name']];blob=row['result_archive'];assert sha(ROOT/blob['path'])==blob['sha256']
    saved=readgz(ROOT/blob['path']);full[item['name']]=saved
    if finished:
        assert entry['status']==row['status'] in ('passed','rejected') and entry['result_available']
        assert entry['report_sha256']==sha(ROUND/'report.json')
        assert ev[-1]['recorded_at_utc']>report['evaluation_started_utc']
    else:assert entry['status']=='reserved' and not entry['result_available']
    assert row['status']==('passed' if all(row['criteria'].values()) else 'rejected')
    assert row['failed_criteria']==[k for k,v in row['criteria'].items() if not v]
    if spec['kind']=='combination':continue
    p=spec['parameters'];asset=spec['universe'][0].split('/')[0];rows=data[asset];n=p['lookback_days'];band=D(str(p['symmetric_band_fraction']));long=False
    wanted={}
    for i,dec in zip(range(start,end),saved['decisions']):
        assert rows[i-1]['close_available_ts']<rows[i]['trade_ts']
        values=[D(r['close']) for r in rows[i-n:i]];sma=sum(values)/n;prior=values[-1]
        if not long and prior>sma*(1+band):long=True;action='enter'
        elif long and prior<sma*(1-band):long=False;action='exit'
        else:action='hold_long' if long else 'hold_cash'
        assert dec=={'decision_index':i,'prior_close':str(prior),'sma':str(sma),'long':long,'action':action}
        wanted[i]=long;decisionchecks+=1
    assert len(saved['decisions'])==180
    for k,r in saved['scenes'].items():
        cash=D(p['initial_capital_usdt']);units=D(0);equity=[cash];index=0;cost=D(0);gross=D(0);fee_sum=D(0)
        for i in range(start,end+1):
            buy=i<end and wanted[i] and not units
            sell=bool(units) and (i==end or not wanted[i])
            if buy or sell:
                t=r['trades'][index];index+=1;fills+=1
                assert t['date']==rows[i]['date'] and t['side']==('buy' if buy else ('terminal_sell' if i==end else 'sell'))
                ref=D(rows[i]['trade_open']);q=D(str(t['quantity']));exe=D(str(t['execution']));fee=D('0.001')*int(k)
                adv=statistics.mean(float(z['quote_volume']) for z in rows[i-20:i])
                closes=[float(z['close']) for z in rows[i-21:i]]
                sigma=statistics.stdev([math.log(b/a) for a,b in zip(closes,closes[1:])])
                budget=float(cash if buy else units*ref)
                participation=budget/adv;impact=0.5*sigma*math.sqrt(participation)*int(k)
                near(t['reference'],ref,1e-9);near(t['lagged_daily_quote_ADV'],adv,1e-5);near(t['lagged_daily_volatility'],sigma,1e-12)
                near(t['estimated_daily_participation'],participation,1e-13);assert participation<=0.001
                near(t['impact_rate'],impact,1e-12);near(t['fee_rate'],fee,1e-15)
                near(t['half_spread_rate'],0.0001*int(k),1e-15);near(t['slippage_rate'],0.0002*int(k),1e-15)
                adverse=0.0003*int(k)+impact
                near(exe,float(ref)*(1+adverse if buy else 1-adverse),1e-7)
                paid=q*exe*fee
                if buy:
                    near(q,cash/(exe*(1+fee)),1e-12)
                    out=q*exe+paid;execution_cost=out-q*ref;cash-=out;units=q;gross-=q*ref
                else:
                    assert q==units
                    incoming=q*exe-paid;execution_cost=q*ref-incoming;cash+=incoming;units=D(0);gross+=q*ref
                assert cash>=D('-0.00000001') and units>=0
                cost+=execution_cost;fee_sum+=paid;near(t['cost_usdt'],execution_cost,1e-8)
            equity.append(cash+units*D(rows[i]['close']) if i<end else cash)
        assert not units and index==r['executions']==len(r['trades'])
        assert r['round_trips']==sum(t['side']!='buy' for t in r['trades'])
        assert len(equity)==182
        for a,b in zip(equity,r['equity_usdt']):near(a,b,1e-7);navpoints+=1
        near(cost,r['cost_usdt']);near(fee_sum,r['fee_usdt']);near(gross,r['gross_reference_PnL_usdt'])
        near(gross-cost,equity[-1]-equity[0]);verify_metrics(r,equity,report['folds'],start)
        assert row['scenes'][k]=={x:y for x,y in r.items() if x not in ('equity_usdt','trades')}
for item in batch:
    spec=json.loads((ROOT/item['spec']).read_text())
    if spec['kind']!='combination':continue
    row=report['configs'][item['name']];saved=full[item['name']]
    assert saved['raw_weights']==[c['weight'] for c in spec['components']]==row['raw_weights']
    assert sum(saved['raw_weights'])==1
    for name,component in zip(row['components'],spec['components']):
        r=report['configs'][name];assert r['fingerprint']==component['fingerprint']
        assert r['parameters']['initial_capital_usdt']==2000*component['weight']
    for k,r in saved['scenes'].items():
        parts=[full[n]['scenes'][k] for n in row['components']]
        equity=[sum(D(str(v)) for v in values) for values in zip(*(p['equity_usdt'] for p in parts))]
        for a,b in zip(equity,r['equity_usdt']):near(a,b,1e-8);navpoints+=1
        verify_metrics(r,equity,report['folds'],start)
        for key in ('executions','round_trips','cost_usdt','gross_reference_PnL_usdt','fee_usdt','spread_usdt','slippage_usdt','impact_usdt'):near(r[key],sum(p[key] for p in parts))
        assert row['scenes'][k]=={x:y for x,y in r.items() if x!='equity_usdt'}
for group,surface in report['sensitivity'].items():
    selected=[r for r in report['configs'].values() if (group=='combination' and r['role']=='combination') or (r['role']=='core' and r['asset']==group)]
    assert len(selected)==surface['variants']==9
    for k,m in surface['metrics'].items():near(m['positive_return_fraction'],sum(r['scenes'][k]['net_return_pct']>0 for r in selected)/9,1e-14)
for row in report['configs'].values():
    c=row['scenes'];pf=sum(f['net_return_pct']>0 for f in c['1']['folds']);assert pf==row['positive_folds_1x']
    group='combination' if row['role']=='combination' else row['asset'];ratio=c['1']['gross_reference_PnL_to_execution_cost']
    assert row['criteria']=={'positive_all_costs':all(r['net_return_pct']>0 for r in c.values()),'minimum_four_positive_folds_1x':pf>=4,
      'max_drawdown_3x_lte25pct':c['3']['max_drawdown_pct']<=25,'neighborhood_3x_positive_gte60pct':report['sensitivity'][group]['metrics']['3']['positive_return_fraction']>=0.6,
      'minimum_two_round_trips_1x':c['1']['round_trips']>=2,'gross_PnL_to_cost_1x_gte2_5':ratio is not None and ratio>=2.5,'no_cash_units_violations':True}
for asset in ('BTC','ETH'):
    b=report['benchmark_reuse'][asset];path=ROOT/b['source_report'];assert sha(path)==b['source_sha256']
    old=json.loads(path.read_text());assert old['equity_timestamps_utc']==report['equity_timestamps_utc']
    for k in ('1','2','3'):assert b['scenes'][k]=={x:y for x,y in old['benchmarks'][asset][k].items() if x not in ('equity_usdt','trades')}
assert navpoints==21294
# Audit the new comparison and the preserved flow deviation, rather than pretending it was preregistered.
for item in json.loads((ROUND/'comparator_batch.json').read_text()):
    spec=json.loads((ROOT/item['spec']).read_text());assert reg.fingerprint(spec)==item['fingerprint']
    row=report['comparator_configs'][item['name']];entry=records[item['fingerprint']]
    ev=[r for r in events if r['fingerprint']==item['fingerprint']]
    assert len(ev)==(2 if finished else 1) and ev[0]['status']=='reserved'
    assert report['evaluation_started_utc']<ev[0]['recorded_at_utc']<report['comparison_reconstruction_at_utc']
    assert item['first_calculation_not_preregistered'] is True
    blob=row['result_archive'];assert sha(ROOT/blob['path'])==blob['sha256'];saved=readgz(ROOT/blob['path'])
    oldpath=ROOT/'research/experiments/20261001T013355Z/report.json';old=json.loads(oldpath.read_text());assert sha(oldpath)==saved['source_report_sha256']
    assert saved['components']==spec['components'] and [c['weight'] for c in spec['components']]==[0.5,0.5]
    for k,r in saved['scenes'].items():
        equity=[D(str(a))+D(str(b)) for a,b in zip(old['benchmarks']['BTC'][k]['equity_usdt'],old['benchmarks']['ETH'][k]['equity_usdt'])]
        for a,b in zip(equity,r['equity_usdt']):near(a,b,1e-8);navpoints+=1
        verify_metrics(r,equity,report['folds'],start)
        assert row['scenes'][k]=={x:y for x,y in r.items() if x!='equity_usdt'}
    if finished:assert entry['status']=='rejected' and entry['result_available'] and entry['report_sha256']==sha(ROUND/'report.json')
    else:assert entry['status']=='reserved'
dev=report['protocol_deviation'];assert sha(ROOT/dev['path'])==dev['sha256']
for key in ('first_report','first_sources'):assert sha(ROOT/dev[key]['path'])==dev[key]['sha256']
first=readgz(ROOT/dev['first_report']['path']);original_sources=readgz(ROOT/dev['first_sources']['path'])
assert first['configs']==report['configs'] and first['benchmark_reuse']==report['benchmark_reuse']
for path,content in original_sources.items():assert hashlib.sha256(content.encode()).hexdigest()==first['source_sha256'][path]
assert navpoints==21840 and len({reg.fingerprint(r['spec']) for r in records.values()})==188
assert sum(records[e['fingerprint']]['result_available'] for e in events[:16])==16
if finished:assert not any(r['status']=='reserved' for r in records.values())
print(f'PASS:39 preregistered research configs/117scenes +1 disclosed comparison/3scenes;{decisionchecks} causal decisions;{fills} real costed fills;{navpoints} independent daily NAV points;54 official archive hashes;exact capital-weight combinations,6folds,source/report hashes,first-output preservation;188canonical,initial16/16actualevidence;finished={finished}')
