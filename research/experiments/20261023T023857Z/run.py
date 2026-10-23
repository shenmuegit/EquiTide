#!/usr/bin/env python3
"""Pre-register VWMA price bands and verify exact ratios, fills and continuous drawdown."""
import argparse, contextlib, copy, csv, gzip, hashlib, importlib.util, io, json, math, subprocess, sys, urllib.request
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
R = Path(__file__).resolve().parent
BASE = ROOT / 'research/experiments/20261014T125820Z'
REG = ROOT / 'research/automation/registry.jsonl'
LOOKS, HURDLES = [20, 40, 80], [0.5, 1, 2]

def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    spec.loader.exec_module(value)
    return value

ev = module(R / 'evaluate.py', 'daily_vwma_engine')
ev.R = R
put, sha = ev.put, ev.sha
rel = lambda p: str(p.relative_to(ROOT))
now = lambda: datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

def call(command, row, *args):
    p = subprocess.run([sys.executable, 'research/automation/registry.py', command, row['spec'], *args], cwd=ROOT, capture_output=True, text=True)
    result = {'configuration': row['name'], 'fingerprint': row['fingerprint'], 'command': command, 'exit_code': p.returncode, 'stdout': p.stdout.strip(), 'stderr': p.stderr.strip()}
    print(json.dumps(result), flush=True)
    assert p.returncode == 0 and p.stdout.strip() == row['fingerprint'], result
    return result

def freeze():
    assert not (R/'plan.json').exists(),'Never overwrite a frozen batch.'
    (R/'specs').mkdir()
    for name in ('exchange_filters.json','exchange_info_raw.json'):(R/name).write_bytes((BASE/name).read_bytes())
    snapshot=json.loads((R/'exchange_filters.json').read_text())
    response=subprocess.run(['curl','--fail','--silent','--show-error','--retry','2','--retry-all-errors','--max-time','20','--write-out','\n%{http_code}',snapshot['source_url']],capture_output=True,timeout=65)
    if response.stderr:sys.stderr.buffer.write(response.stderr);sys.stderr.flush()
    response.check_returncode();raw,status=response.stdout.rsplit(b'\n',1);assert int(status)==200;public=json.loads(raw)
    (R/'exchange_info_current.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    filters={s['baseAsset']:{f['filterType']:f for f in s['filters'] if f['filterType'] in snapshot['filters'][s['baseAsset']]} for s in public['symbols']}
    assert filters==snapshot['filters'],'Changed filters require a new frozen spec.'
    put(R/'filter_check.json',{'retrieved_utc':now(),'source_url':snapshot['source_url'],'HTTP_status':int(status),'raw_sha256':hashlib.sha256(raw).hexdigest(),'raw_gzip_path':rel(R/'exchange_info_current.json.gz'),'raw_gzip_sha256':sha(R/'exchange_info_current.json.gz'),'equals_frozen_filters':True,'current_filters':filters})
    events=ev.registry.read_events(REG);records=ev.registry.read_records(REG);first=[json.loads(x)['fingerprint'] for x in REG.read_text().splitlines()[:16]];initial={}
    for event in events:
        if event['fingerprint'] in first:initial.setdefault(event['fingerprint'],{}).update(event)
    assert len(initial)==16 and all(x.get('result_available') is True for x in initial.values())
    monitor=module(ROOT/'research/monitor/snapshot.py','vwma_monitor_context')
    canonical={ev.registry.fingerprint(x['spec']) for x in records.values() if not monitor.is_observation(x['spec'])}
    previous=ROOT/'research/experiments/20261023T003724Z';accounts=[ROOT/'research/paper10/plan.json',ROOT/'research/paper10/state.json',previous/'forward_state.json',previous/'forward_report.json']
    prior=[{'path':rel(p),'sha256':sha(p),'opening':p.read_text()[:220]} for p in sorted((ROOT/'research/experiments').glob('*/result.md'))]
    put(R/'context.json',{'registry_events':len(events),'registry_ids':len(records),'canonical_research_definitions_excluding_observations':len(canonical),'main_registry_sha256_before_reserve':sha(REG),'initial_16_missing_actual_results':0,'prior_conclusions_read':prior,'account_hashes_before':{rel(p):sha(p) for p in accounts}})
    plan=json.loads((BASE/'plan.json').read_text());plan.update(round=R.name,frozen_at_utc=now(),trigger_utc='2026-10-23T02:38:57.945Z',direction='Daily base-volume-weighted moving close with symmetric price hysteresis',hypothesis='Use greater weight on high-base-volume daily closes to test whether the causal trend anchor survives whipsaw and execution costs. Daily close times day volume is an indicator proxy,not traded VWAP,aggressor flow or profitability evidence.')
    plan['grid'].update(lookback_days=LOOKS,entry_hurdle_pct=HURDLES,exit_hurdle_pct='negative entry band',volume='UTC daily base-asset volume',arithmetic='Exact Fraction of daily Float64 decimal-string encoded close and base volume;Decimal60 display only;accounting Decimal28 unchanged')
    plan['sources']=[{'url':'https://raw.githubusercontent.com/QuantConnect/Lean/master/Indicators/VolumeWeightedMovingAverage.cs','accessed_utc':'2026-10-23','version_observed':'LEAN master as accessed2026-10-23','scope':'Primary formula sums close*volume over rolling sum volume;source only,our rational implementation and trading grid independently frozen,no library or code copy.'},{'url':'https://www.quantconnect.com/docs/v2/writing-algorithms/indicators/supported-indicators/volume-weighted-moving-average','accessed_utc':'2026-10-23','scope':'Official indicator formula only,not a profitable strategy endorsement or bitwise equivalence claim.'},{'url':'https://developers.binance.com/en/docs/products/spot/filters','accessed_utc':'2026-10-23','scope':'Official spot filter definitions;actual historical filters remain unavailable.'}]
    plan['costs']['filters_source']='Unchanged2026-10-14 frozen public exchangeInfo proxy,compared to current response in filter_check.json. Frozen SHA is reused;current retrieval time cannot manufacture novelty. Historical L2/filter rules unavailable.'
    plan['prior_results']={'source_report':rel(previous/'report.json'),'source_sha256':sha(previous/'report.json'),'last_batch':'18 long-horizon B1 carry candidates rejected;all1/2/3x negative. Do not retest these exact configurations.','distinction':'Spot directional volume-weighted close anchor differs from carry,median,SMA/EMA and volume-ratio filters. Full registry entry/exit scan found no VWMA signal definition.','initial_16_missing_actual_results':0,'canonical_prior_research_definitions':len(canonical)}
    signal='On each completed UTC signal dayj, VWMA_L=sum(C_i*V_i)/sum(V_i),i=j-L+1..j,includingj;C is last closed minute close,V is sum of1440closed-minute base-asset volumes. Exact Fraction from daily Float64decimal strings,canonical ratioSHA,Decimal60display only. NeedLclosed days,no padding. If window volume iszero,preserve actual position without a trade.'
    plan['rule'].update(signal=signal,entry='When actually flat,enter iff C_j>VWMA_L*(1+b),strict.',exit='When actually long,exit iff C_j<VWMA_L*(1-b),strict;equality/deadband preserves position. No short,leverage,add-on,transfer,cash interest or same-decision reentry;costed terminal liquidation.')
    plan['validation']['parameter_sensitivity_axes']=['lookback_days','entry_hurdle_fraction'];plan['validation']['purging']='No fitting or future-return labels;label purge inapplicable.365day context and3day initial gap;fixed rules and two-axis grid,12chronological30day folds,continuous account,no OOS reset or selection.'
    plan['validation']['continuous_drawdown']='Initial capital,all closed OOS minute-close NAVs and immediate post-fill reference marks;no fold reset or intraminute extrema.'
    plan['account_scope']='Independent2000USDT single-asset research account,raw_asset_weight1 per configuration,not a combined4000USDT evaluation;volume division belongs only to the indicator formula,not portfolio-weight normalization. Existing SMA/paper10 accounts remain independent and unchanged.'
    put(R/'plan.json',plan)
    template=json.loads((BASE/'specs/daily_roc_momentum_BTC_L7_H0.json').read_text());template['family']='spot-daily-base-volume-weighted-close-hysteresis';template['logic']['entry']=signal+' When flat,enter iff close>VWMA*(1+entry_hurdle_fraction),strict.';template['logic']['exit']=plan['rule']['exit'];template['parameters']['arithmetic']='Exact Fraction from daily Float64decimal strings;Decimal60display,accounting Decimal28';template['parameters']['volume_weight']='base-asset daily volume';template['parameters']['zero_window_volume']='preserve actual position,no trade'
    batch=[]
    for asset in ('BTC','ETH'):
        for look in LOOKS:
            for hurdle in HURDLES:
                name=f"daily_vwma_{asset}_L{look}_H{str(hurdle).replace('.','p')}";spec=copy.deepcopy(template);spec.update(name=name,universe=[asset+'/USDT'],sources=plan['sources'],validation_plan=rel(R/'plan.json'));spec['parameters'].update(asset=asset,lookback_days=look,entry_hurdle_fraction=hurdle/100,exit_hurdle_fraction=-hurdle/100);assert spec['parameters']['exchange_filters_sha256']==sha(R/'exchange_filters.json');path=R/'specs'/(name+'.json');put(path,spec);batch.append({'name':name,'asset':asset,'lookback_days':look,'entry_hurdle_pct':hurdle,'spec':rel(path),'fingerprint':ev.registry.fingerprint(spec)})
    assert len(batch)==len({x['fingerprint'] for x in batch})==18;put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/daily_vwma_BTC_L40_H1.json').read_text()));done=[]
    for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
    print('FROZEN_AND_RESERVED',len(done),sha(R/'plan.json'),flush=True)

def evaluate():
    assert not (R / 'report.json').exists(), 'Use verify for existing results.'
    records = ev.registry.read_records(REG)
    assert all(records[r['fingerprint']]['status'] == 'reserved' for r in json.loads((R / 'batch.json').read_text()))
    checkpoint = R / 'checkpoints'
    checkpoint.mkdir(exist_ok=True)
    original = ev.evaluate_one
    def saved(row, mult, market, filters, plan):
        path = checkpoint / f"{row['name']}_{mult}.json.gz"
        if path.exists():
            cached = json.loads(gzip.decompress(path.read_bytes()))
            assert cached['fingerprint'] == row['fingerprint'] and cached['plan_sha256'] == sha(R / 'plan.json')
            return cached['result']
        result = original(row, mult, market, filters, plan)
        path.write_bytes(gzip.compress(json.dumps({'fingerprint': row['fingerprint'], 'plan_sha256': sha(R / 'plan.json'), 'result': result}, allow_nan=False).encode(), mtime=0))
        return result
    ev.evaluate_one = saved
    try:
        ev.main()
    finally:
        ev.evaluate_one = original

def verify():
    audit = module(BASE / 'audit.py', 'long_roc_replay_audit')
    audit.R, audit.ev = R, ev
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        audit.main()
    plan = json.loads((R / 'plan.json').read_text())
    markets = {a: ev.load_asset(a, plan) for a in ('BTC', 'ETH')}
    decisions = list(csv.DictReader(gzip.open(R / 'decisions.csv.gz', 'rt')))
    trades=list(csv.DictReader(gzip.open(R/'trades.csv.gz','rt')));execution_trades={(t['configuration'],t['cost_multiplier'],t['execution_utc']):t for t in trades if t['terminal']=='False'}
    import numpy as np
    from fractions import Fraction as F
    independent,held_state={},{};volume_checks=0;volume_max_difference=0.
    for market in markets.values():
        assert np.array_equal(market['minute_close'].reshape(730,1440)[:,-1],market['daily_close'])
        summed=market['minute_base'].reshape(730,1440).sum(axis=1);actual=market['daily_base_volume'];assert np.allclose(summed,actual,rtol=1e-12,atol=1e-8);volume_checks+=len(summed);volume_max_difference=max(volume_max_difference,float(np.max(np.abs(summed-actual))))
    for d in decisions:
        m=markets[d['asset']];signal=int(datetime.fromisoformat(d['signal_day_utc'].replace('Z','+00:00')).timestamp()*1000);execution=int(datetime.fromisoformat(d['simulated_decision_at_utc'].replace('Z','+00:00')).timestamp()*1000);i=int((signal-m['day_ts'][0])//ev.DAY_MS);look=int(d['lookback_days']);key=(d['asset'],look)
        assert execution==signal+ev.DAY_MS+ev.MIN_MS
        if key not in independent:
            encoded=[[D(str(x)).as_integer_ratio() for x in m[k]] for k in ('daily_close','daily_base_volume')];scales=[math.lcm(*(b for a,b in seq)) for seq in encoded];cl,vol=[[a*(scale//b) for a,b in seq] for seq,scale in zip(encoded,scales)];pv=[0];vv=[0]
            for c,v in zip(cl,vol):pv.append(pv[-1]+c*v);vv.append(vv[-1]+v)
            independent[key]=[F(pv[j+1]-pv[j-look+1],(vv[j+1]-vv[j-look+1])*scales[0]) if j+1>=look and vv[j+1]>vv[j-look+1] else None for j in range(len(cl))]
        reference=independent[key][i];close=F(D(str(m['daily_close'][i])));band=F(D(d['entry_hurdle_fraction']));account=(d['configuration'],d['cost_multiplier']);held=held_state.get(account,False)
        expected=held if reference is None else not(close<reference*(1-band)) if held else close>reference*(1+band)
        action='entry' if expected and not held else 'exit' if held and not expected else 'hold'
        assert d['action']==action and d['desired_long']==str(expected)
        if reference is not None:
            assert hashlib.sha256(f'{reference.numerator}/{reference.denominator}'.encode()).hexdigest()==d['vwma_exact_ratio_sha256']
            assert math.isclose(float(close/reference-1),float(d['signed_distance_from_vwma']),rel_tol=1e-12,abs_tol=1e-12)
            with __import__('decimal').localcontext() as dc:dc.prec=60;assert D(d['vwma_reference'])==D(reference.numerator)/D(reference.denominator)
        else:assert d['vwma_exact_ratio_sha256']=='undefined'
        trade=execution_trades.get((*account,d['simulated_decision_at_utc']))
        if trade and trade['status']=='filled':held_state[account]=D(trade['units_after'])>0
    trades = list(csv.DictReader(gzip.open(R / 'trades.csv.gz', 'rt')))
    for t in trades:
        if t['status'] != 'filled':
            assert t['cash_before'] == t['cash_after'] and t['units_before'] == t['units_after']
            continue
        ref, c0, c1, u0, u1 = map(D, [t['reference'], t['cash_before'], t['cash_after'], t['units_before'], t['units_after']])
        assert abs(c0 + u0 * ref - c1 - u1 * ref - D(t['cost_usdt'])) < D('1e-20')
        assert c1 >= 0 and u1 >= 0 and D(t['participation']) <= D('.001')
    report = json.loads((R / 'report.json').read_text())
    import numpy as np
    for c in report['configs'].values():
        m = markets[c['asset']]
        start = int(datetime.fromisoformat(plan['time_boundaries']['oos_start_utc'].replace('Z', '+00:00')).timestamp() * 1000)
        begin = int((start - m['minute_ts'][0]) // ev.MIN_MS)
        end = begin + 360 * 1440
        for mult in (1, 2, 3):
            peak, loss, cash, units, cursor = 2000., 0., 2000., 0., begin
            filled = [t for t in trades if t['configuration'] == c['name'] and int(t['cost_multiplier']) == mult and t['status'] == 'filled']
            for t in filled + [None]:
                stop = int(t['minute_index']) if t else end
                values = cash + units * m['minute_close'][cursor:stop]
                if len(values):
                    peaks = np.maximum.accumulate(np.r_[peak, values])
                    loss = max(loss, float(np.max(1 - values / peaks[1:])))
                    peak = float(peaks[-1])
                if t:
                    cash, units = float(t['cash_after']), float(t['units_after'])
                    post = cash + units * float(t['reference'])
                    peak = max(peak, post); loss = max(loss, 1 - post / peak)
                cursor = stop
            assert math.isclose(loss * 100, c['scenarios'][str(mult)]['max_drawdown_1m_sampled_pct'], rel_tol=1e-10, abs_tol=1e-10), (c['name'], mult, 'initial-capital-anchored drawdown', loss * 100)
    context = json.loads((R / 'context.json').read_text())
    assert all(sha(ROOT / p) == h for p, h in context['account_hashes_before'].items()), 'Persistent account changed.'
    assert len(decisions) == 18 * 3 * 360
    result = {'passed': True, 'report_sha256': sha(R / 'report.json'), 'exact_replay': output.getvalue(), 'independent_integer_VWMA_ratio_state_and_timestamp_checks':len(decisions),'independent_daily_base_volume_checks':volume_checks,'volume_sum_max_abs_float_difference':volume_max_difference, 'balance_conservation_checks': sum(t['status'] == 'filled' for t in trades), 'independent_capital_anchored_minute_drawdown_checks': 54, 'persistent_accounts_unchanged': True, 'maximum_observed_participation': max(float(t['participation']) for t in trades), 'minimum_event_notional_capacity_usdt_at_0_1pct_ADV': min(float(D(t['lagged_ADV']) * D('.001')) for t in trades)}
    print(json.dumps(result), flush=True)
    return result

def finish():
    report=json.loads((R/'report.json').read_text());done=[]
    for row in json.loads((R/'batch.json').read_text()):done.append(call('finish',row,report['configs'][row['name']]['status'],rel(R/'report.json')));put(R/'finish.json',done)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('freeze', 'evaluate', 'verify','finish'))
    globals()[parser.parse_args().command]()
