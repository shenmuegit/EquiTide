"""Independent archive audit: no evaluation engine or fill kernel import."""
import gzip
import hashlib
import json
import math
import statistics
import sys
from datetime import datetime
from decimal import Decimal as D,ROUND_CEILING,ROUND_FLOOR
from pathlib import Path
import numpy as np
import polars as pl

ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def near(a,b,tol=1e-8):
    if a is None or b is None:assert a is None and b is None;return
    assert abs(float(a)-float(b))<=tol,(a,b)
def verify_metrics(v,daily,m,days):
    # Prefix peaks via independent vectorized scan and separately defined returns.
    pct=float((v[-1]/v[0]-1)*100);maximum=float(np.max((np.maximum.accumulate(v)-v)/np.maximum.accumulate(v))*100)
    ret=[b/a-1 for a,b in zip(daily,daily[1:])];sd=statistics.stdev(ret)
    sharpe=statistics.mean(ret)/sd*math.sqrt(365) if sd else None
    cagr=(v[-1]/v[0])**(365/days)*100-100
    near(pct,m['net_return_pct']);near(maximum,m['max_drawdown_pct']);near(cagr,m['cagr_pct']);near(sharpe,m['sharpe_365']);near(cagr/maximum if maximum else None,m['calmar'])
    dailydd=max(1-x/max(daily[:i+1]) for i,x in enumerate(daily))*100
    # Full reported daily DD also includes pre-terminal mark; final cost can be higher.
    assert m['daily_mark_drawdown_pct']+1e-8>=dailydd
def main():
    finished='--finished' in sys.argv
    report=json.loads((ROUND/'report.json').read_text());plan=json.loads((ROUND/'spec.json').read_text());batch=json.loads((ROUND/'batch.json').read_text())
    assert report['plan']==plan and len(batch)==30
    records=registry.read_records(ROOT/'research/automation/registry.jsonl')
    lines=[json.loads(x) for x in (ROOT/'research/automation/registry.jsonl').read_text().splitlines()]
    evalstart=datetime.fromisoformat(report['evaluation_started_utc']);frozen=datetime.fromisoformat(plan['frozen_at_utc'])
    for b in batch:
        sp=json.loads((ROOT/b['spec']).read_text());fp=registry.fingerprint(sp);assert fp==b['fingerprint']
        reserves=[r for r in lines if r['fingerprint']==fp and r['status']=='reserved'];assert len(reserves)==1
        assert frozen<=datetime.fromisoformat(reserves[0]['recorded_at_utc'])<evalstart
        assert records[fp]['status']==(report['configs'][b['name']]['status'] if finished else 'reserved')
        if finished:assert records[fp]['report_sha256']==sha(ROUND/'report.json') and records[fp]['result_available']
    for p,h in report['source_hashes'].items():assert sha(ROOT/p)==h,p
    assert sha(ROOT/plan['execution']['metadata_path'])==plan['execution']['metadata_sha256']
    assert sha(ROOT/'research/experiments/20261001T113625Z/forward_plan.json')==report['prior_candidate']['forward_plan_sha256']
    old=json.loads((ROUND/'download_manifest.json').read_text())
    assert len(old['archives'])==26
    for a in old['archives']:assert sha(ROOT/a['path'])==a['sha256']==a['published_sha256']
    frames={};daily=json.loads(gzip.decompress((ROUND/'daily_inputs.json.gz').read_bytes()));closes={};opens={}
    for asset,provenance in report['data'].items():
        assert sha(ROOT/provenance['path'])==provenance['sha256'];frame=pl.read_parquet(ROOT/provenance['path']);frames[asset]=frame
        assert frame.height==525600 and frame['is_closed'].all()
        assert (frame['available_ts']-frame['open_ts']==60000000000).all()
        assert (frame['open_ts'].diff().drop_nulls()==60000000000).all()
        closes[asset]=np.asarray(frame['close'].cast(pl.Float64));opens[asset]=np.asarray(frame['open'].cast(pl.Float64))
        for i,r in enumerate(daily[asset]):
            near(frame['close'][(i+1)*1440-1],r['close'],1e-10)
            assert int(r['trade_ts'])==frame['open_ts'][i*1440+1]
            near(frame['open'][i*1440+1],r['trade_open'],1e-10)
            near(float(frame['quote_volume'].slice(i*1440,1440).sum()),r['quote_volume'],.0001)
    curves={};counts={'decisions':0,'fills':0,'minute_NAV_points':0,'actual_scenes':0,'archives':0,'rejected_orders':0}
    for b in batch:
        row=report['configs'][b['name']];path=ROOT/row['archive'];assert sha(path)==row['archive_sha256'];a=json.loads(gzip.decompress(path.read_bytes()));sp=a['spec'];assert registry.fingerprint(sp)==b['fingerprint']
        counts['archives']+=1
        for k,scene in a['scenes'].items():
            m=scene['summary'];assert m==row['scenes'][k];mult=int(k)
            if sp['kind']=='strategy':
                asset=sp['universe'][0].split('/')[0];p=sp['parameters'];fs=p['execution']['filters'][asset+'USDT'];cash=D(p['initial_capital_usdt']);units=D(0);desired=False
                if p['lookback_days']:
                    n=p['lookback_days']
                    for d,decision in enumerate(scene['decisions']):
                        i=183+d;values=[D(daily[asset][j]['close']) for j in range(i-n,i)];avg=sum(values)/n
                        if not desired and values[-1]>avg*D('1.01'):desired=True
                        elif desired and values[-1]<avg*D('.99'):desired=False
                        assert decision['decision_index']==i and decision['long']==desired and D(decision['sma'])==avg and D(decision['prior_close'])==values[-1]
                        assert int(daily[asset][i-1]['close_available_ts'])<int(daily[asset][i]['trade_ts'])
                        counts['decisions']+=1
                for t in scene['trades']:
                    i=t['decision_index'];r=daily[asset][i];ref=D(r['trade_open']);assert D(t['reference'])==ref
                    assert t['trade_ts_ns']==int(r['trade_ts'])
                    adv=statistics.mean(float(daily[asset][j]['quote_volume']) for j in range(i-20,i))
                    prev=[float(daily[asset][j]['close']) for j in range(i-21,i)]
                    sig=statistics.stdev(math.log(prev[z+1]/prev[z]) for z in range(20));near(adv,t['lagged_ADV'],1e-6);near(sig,t['lagged_sigma'],1e-15)
                    last5=frames[asset].slice(i*1440-4,5);assert last5['available_ts'].max()<=int(r['trade_ts'])
                    near(last5['quote_volume'].sum()/last5['base_volume'].sum(),t['proxy_VWAP5'],1e-10)
                    buy=t['side']=='buy';budget=cash if buy else units*ref;assert D(t['budget'])==budget
                    impact=D('.5')*D(str(sig))*(budget/D(str(adv))).sqrt()*mult
                    expected=ref*(1+(D('.0003')*mult+impact)*(1 if buy else -1));tick=D(fs['PRICE_FILTER']['tickSize'])
                    px=(expected/tick).to_integral_value(rounding=ROUND_CEILING if buy else ROUND_FLOOR)*tick
                    step=D(fs['LOT_SIZE']['stepSize']);fee=D('.001')*mult
                    q=((cash/(px*(1+fee)) if buy else units)/step).to_integral_value(rounding=ROUND_FLOOR)*step
                    if t['status']!='filled':
                        assert D(t['cash_after'])==cash and D(t['units_after'])==units;counts['rejected_orders']+=1;continue
                    assert D(t['quantity'])==q and D(t['execution'])==px and q%step==0 and px%tick==0
                    assert D(fs['LOT_SIZE']['minQty'])<=q<=D(fs['LOT_SIZE']['maxQty'])
                    assert D(fs['NOTIONAL']['minNotional'])<=q*px<=D(fs['NOTIONAL']['maxNotional'])
                    pc=fs['PERCENT_PRICE_BY_SIDE'];prefix='bid' if buy else 'ask';vwap=D(t['proxy_VWAP5'])
                    assert vwap*D(pc[prefix+'MultiplierDown'])<=px<=vwap*D(pc[prefix+'MultiplierUp'])
                    costs={'fee':q*px*fee,'half_spread':q*ref*D('.0001')*mult,'slippage':q*ref*D('.0002')*mult,'impact':q*ref*impact,'tick_rounding':q*abs(px-expected)}
                    for part,x in costs.items():assert abs(x-D(t['cost_parts'][part]))<D('1e-20')
                    cash=cash-q*px*(1+fee) if buy else cash+q*px*(1-fee);units=units+q if buy else units-q
                    assert cash==D(t['cash_after']) and units==D(t['units_after']) and cash>=0 and units>=0
                    counts['fills']+=1
                assert D(scene['terminal_cash'])==cash and D(scene['terminal_units'])==units
                v=np.empty(259382);v[0]=p['initial_capital_usdt'];daycount=0
                for st in scene['position_segments']:
                    for d in range(st['day_offset'],st['end_day_exclusive']):
                        c=D(st['cash']);u=D(st['units']);daycount+=1;i=183+d
                        v[d*1441+1]=float(c+u*D(daily[asset][i]['trade_open']))
                        v[d*1441+2:(d+1)*1441+1]=float(c)+closes[asset][i*1440+1:(i+1)*1440+1]*float(u)
                assert daycount==180
                v[-1]=float(cash+units*D(daily[asset][363]['trade_open']))
                # Check segments also track the archived actual fill state, not a hypothetical desired position.
                c=D(p['initial_capital_usdt']);u=D(0)
                for d in range(180):
                    for t in scene['trades']:
                        if t['day_offset']==d:c=D(t['cash_after']);u=D(t['units_after'])
                    st=next(s for s in scene['position_segments'] if s['day_offset']<=d<s['end_day_exclusive'])
                    assert c==D(st['cash']) and u==D(st['units'])
            else:
                names=scene['component_names'];assert names==row['component_names'];parts=[curves[(n,k)] for n in names]
                assert len(parts)==2;v=parts[0]+parts[1]
                for key in ('cost_usdt','executions','round_trips'):
                    near(sum(report['configs'][n]['scenes'][k][key] for n in names),m[key])
                caps=[report['configs'][n]['parameters']['initial_capital_usdt'] for n in names]
                assert caps==[int(2000*D(str(c['weight']))) for c in sp['components']] and sum(caps)==2000
            assert len(v)==259382 and (v>0).all()
            assert hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==m['NAV_sha256_f64le']
            disk=np.load(ROOT/'data/runs'/ROUND.name/f'{b["name"]}_{k}.npy',allow_pickle=False);assert np.array_equal(disk,v)
            days=[float(v[d*1441]) for d in range(181)];assert days+[float(v[-1])]==m['daily_equity_usdt']
            verify_metrics(v,days[:-1]+[float(v[-1])],m,180)
            for j,fm in enumerate(m['folds']):
                seg=v[j*30*1441:(j+1)*30*1441+1+(j==5)];ds=[float(seg[d*1441]) for d in range(31)]
                if j==5:ds[-1]=float(seg[-1])
                verify_metrics(seg,ds,fm,30)
            curves[(b['name'],k)]=v;counts['minute_NAV_points']+=len(v);counts['actual_scenes']+=1
        if not row['role'].startswith('comparator'):
            scenes=row['scenes'];group='combination' if row['role']=='combination' else row['asset'];positive=sum(f['net_return_pct']>0 for f in scenes['1']['folds'])
            criteria={'positive_all_costs':all(s['net_return_pct']>0 for s in scenes.values()),'four_positive_1x_folds':positive>=4,'minute_DD3_lte25pct':scenes['3']['max_drawdown_pct']<=25,'neighbourhood_positive3_gte60pct':report['sensitivity'][group]['metrics']['3']['positive_return_fraction']>=.6,'two_round_trips1':scenes['1']['round_trips']>=2,'gross_to_cost1_gte2_5':scenes['1']['gross_reference_PnL_to_execution_cost']>=2.5,'no_balance_violations':all(s['cash_or_units_violations']==0 for s in scenes.values()),'terminal_flat':all(D(s['terminal_units'])==0 for s in scenes.values())}
            assert row['criteria']==criteria and (row['status']=='passed')==all(criteria.values()) and positive==row['positive_folds_1x']
    assert counts['decisions']==9720 and counts['minute_NAV_points']==23344380 and counts['actual_scenes']==90 and counts['archives']==30,counts
    assert counts['fills']==report['summary']['fills']
    previous=json.loads((ROOT/plan['previous_period_reference']['report']).read_text())
    for item in batch:
        row=report['configs'][item['name']];prior=previous['configs'][item['previous_name']]
        assert row['previous_period_status']==prior['status']
        assert row['previous_period_returns']=={k:x['net_return_pct'] for k,x in prior['scenes'].items()}
        assert row['both_periods_meet_full_gates']==(row['status']=='passed' and prior['status']=='passed')
    if finished:assert not any(r['status']=='reserved' for r in records.values())
    print('PASS:'+json.dumps(counts)+'; independent real-data/Decimal trade/continuous minute NAV/fold/gate/pre-reservation'+('/finish SHA' if finished else '')+' audit',flush=True)

if __name__=='__main__':main()
