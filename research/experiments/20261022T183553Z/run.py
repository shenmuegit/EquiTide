#!/usr/bin/env python3
"""Pre-register Wilder RSI2 mean reversion and independently verify exact Fraction flows."""
import argparse, contextlib, copy, csv, gzip, hashlib, importlib.util, io, json, math, subprocess, sys, urllib.request
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
R = Path(__file__).resolve().parent
BASE = ROOT / 'research/experiments/20261014T125820Z'
REG = ROOT / 'research/automation/registry.jsonl'
LOOKS, HURDLES = [100, 150, 200], [10, 20, 30]

def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    spec.loader.exec_module(value)
    return value

ev = module(R / 'evaluate.py', 'daily_rsi2_engine')
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
    assert not (R / 'plan.json').exists(), 'Resume existing reservations; never overwrite a frozen batch.'
    (R / 'specs').mkdir()
    for name in ('exchange_filters.json', 'exchange_info_raw.json'):
        (R / name).write_bytes((BASE / name).read_bytes())
    snapshot = json.loads((R / 'exchange_filters.json').read_text())
    raw = subprocess.check_output(['curl', '--fail', '--silent', '--show-error', '--retry', '2', '--max-time', '20', snapshot['source_url']], timeout=65)
    public = json.loads(raw)
    filters = {s['baseAsset']: {f['filterType']: f for f in s['filters'] if f['filterType'] in snapshot['filters'][s['baseAsset']]} for s in public['symbols']}
    assert filters == snapshot['filters'], 'Changed filters require a new frozen specification.'
    put(R / 'filter_check.json', {'retrieved_utc': now(), 'source_url': snapshot['source_url'], 'raw_sha256': hashlib.sha256(raw).hexdigest(), 'server_time_ms': public.get('serverTime'), 'equals_frozen_filters': True, 'current_filters': filters})
    events = ev.registry.read_events(REG)
    records = ev.registry.read_records(REG)
    first = [json.loads(x)['fingerprint'] for x in REG.read_text().splitlines()[:16]]
    initial = {}
    for event in events:
        if event['fingerprint'] in first:
            initial.setdefault(event['fingerprint'], {}).update(event)
    assert len(initial) == 16 and all(x.get('result_available') is True for x in initial.values())
    monitor = module(ROOT / 'research/monitor/snapshot.py', 'long_roc_monitor_read')
    canonical = {ev.registry.fingerprint(x['spec']) for x in records.values() if isinstance(x.get('spec'), dict) and not monitor.is_observation(x['spec'])}
    accounts = [ROOT / 'research/paper10/plan.json', ROOT / 'research/paper10/state.json', ROOT / 'research/experiments/20261022T163422Z/forward_state.json', ROOT / 'research/experiments/20261022T163422Z/forward_report.json']
    prior = [{'path': rel(p), 'sha256': sha(p), 'opening': ' '.join(t.strip() for t in p.read_text().splitlines() if t.strip() and not t.startswith('#'))[:240]} for p in sorted((ROOT / 'research/experiments').glob('*/result.md'))]
    context = {'registry_events': len(events), 'registry_ids': len(records), 'canonical_research_definitions_excluding_observations': len(canonical), 'main_registry_sha256_before_reserve': sha(REG), 'initial_16_missing_actual_results': 0, 'prior_conclusions_read': prior, 'account_hashes_before': {rel(p): sha(p) for p in accounts}}
    put(R / 'context.json', context)
    plan = json.loads((BASE / 'plan.json').read_text())
    plan.update(round=R.name,frozen_at_utc=now(),trigger_utc='2026-10-22T18:35:53.033Z',direction='Daily Wilder RSI2 pullback above slow SMA,exit on fast-SMA rebound or trend loss;unlevered long/cash.',hypothesis='Test short pullback mean reversion only while above a slow trend,with a fast-price rebound exit. This changes activity and holding horizon from prior longer-RSI recovery exits;no presumption that equity recipes transfer to BTC/ETH.')
    plan['grid'].update(trend_sma_days=LOOKS,entry_rsi_threshold=HURDLES,rsi_period=2,exit_sma_days=5,zero_gain_and_loss_RSI=50,RSI_seed='Datasetday2:simplemean of first2close changes;then(gain_or_loss+new)/2;no OOS/fold reset',SMA_window='j-N+1..j including completed signal close',arithmetic='exact Fraction from daily Float64 decimal-string encoding;Decimal60 display only')
    for key in ('lookback_days','entry_hurdle_pct','exit_hurdle_pct'):plan['grid'].pop(key)
    plan['sources']=[{'url':'https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/rsi-2','accessed_utc':'2026-10-22','scope':'Primary publisher describes short RSI pullbacks above slow SMA and fastSMA5 rebound exit. Our100/150/200and10/20/30grid,strict trend-loss exit and next00:01execution are explicit adaptations;no claim of replicating original equity results or profitability.'},{'url':'https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/relative-strength-index-rsi','accessed_utc':'2026-10-22','scope':'Primary Wilder simple-mean initialization and recursive gain/loss smoothing;our two-period and neutral50zero-total convention are fixed.'},{'url':'https://raw.githubusercontent.com/TA-Lib/ta-lib/v0.6.4/src/ta_func/ta_RSI.c','accessed_utc':'2026-10-22','version_observed':'TA-Lib v0.6.4','scope':'Primary initialization/recursion reference. Exact Fraction and zero-total neutral50 differ from its float/zero convention;no bitwise-equivalence claim or copied source.'},{'url':'https://developers.binance.com/en/docs/products/spot/filters','accessed_utc':'2026-10-22','scope':'Official spot filter definitions;historical filters unavailable.'}]
    plan['source_access_failures']=[]
    plan['costs']['filters_source'] = 'Unchanged 2026-10-14 frozen public exchangeInfo proxy, checked against the current public response in filter_check.json. Reuse the original hash so retrieval timestamps cannot manufacture novelty. Historical L2 and historical filters are unavailable.'
    plan['prior_results']={'source_report':'research/experiments/20261022T163422Z/report.json','source_sha256':sha(ROOT/'research/experiments/20261022T163422Z/report.json'),'initial_16_missing_actual_results':0,'canonical_prior_research_definitions':len(canonical),'last_batch':'18 UO momentum candidates rejected;3/3/3positive bycost,all failed fold breadth and neighborhood.','prior_Wilder_pullback':'research/experiments/20261021T182350Z/report.json','distinction':'Prior Wilder uses7/14/28days andRSI>=50orclose<=SMA200exit;oldCutlerRSI2uses finite2change sums. New Wilder2has decaying recursive memory and fastSMA5rebound/strictslowtrendexit,with100/150/200slowSMA grid. New economic rules,not name/number-format novelty.'}
    plan['validation']['purging']='No fitted model/future-return labels;label purge inapplicable. Wilder2seedatdatasetday2,recursion never resets;365day context precedes OOS and covers slowSMA200. Slow and fast SMAs include only completed signal closes.3day initial gap,12continuous folds;no OOS parameter selection.'
    plan['account_scope']='Offline research only. Read existing paper10 and delayed SMA-shadow accounts without reset,replacement,new paper observations or real orders.'
    signal_rule='Use completed UTC daily closes. Seed avgGain/avgLoss atdatasetindex2 with simplemeans of first2changes. Eachlaterday avg=(previousavg+newgain_or_loss)/2. RSI2=100*avgGain/(avgGain+avgLoss);bothzero50. Exact Fraction from encodedFloat64decimalstrings;no rounding or OOS/fold reset. Slow SMA uses lastTcompleted closes includingj;fast exit SMA uses last5completed closes. Compare price*Twith slow sum andprice*5with fast sum,without rounded means. Decimal60display,canonical RSIratioSHA;accountingDecimal28 unchanged.'
    plan['rule'].update(signal=signal_rule,entry='When flat,enter iff RSI2<E AND completed close>SMA(T),bothstrict;entry equality remains cash,no priorcross requirement.',exit='When long,exit iff completed close>SMA5 OR close<SMA(T),bothstrict;equal fast/slow boundary alone preserves long. No RSI exit,short,hold cap or same-decision re-entry;costed terminal liquidation.')
    plan['validation']['parameter_sensitivity_axes']=['trend_sma_days','entry_rsi_threshold']
    plan['validation']['continuous_drawdown'] = 'Initial capital plus all OOS minute-close and immediate post-fill marks; no fold reset or intraminute extrema.'
    put(R / 'plan.json', plan)
    template = json.loads((BASE / 'specs/daily_roc_momentum_BTC_L7_H0.json').read_text())
    template['family']='spot-daily-wilder-rsi2-fast-sma-rebound'
    template['logic']['entry']=signal_rule+' While flat,enter iff RSI2<entry_rsi_threshold AND close>SMA(trend_sma_days),bothstrict,no prior-cross requirement.'
    template['logic']['exit']='While long,exit iff close>SMA5 OR close<SMA(trend_sma_days),bothstrict;equality alone preserves long. No RSI exit,future padding,fold reset,short,hold cap or same-decision re-entry. Costed terminal liquidation.'
    for key in ('lookback_days','entry_hurdle_fraction','exit_hurdle_fraction'):template['parameters'].pop(key)
    template['parameters']['sensitivity_axes']=['trend_sma_days','entry_rsi_threshold']
    batch = []
    for asset in ('BTC', 'ETH'):
        for look in LOOKS:
            for hurdle in HURDLES:
                name = f"daily_wilder_rsi2_{asset}_T{look}_E{hurdle}"
                spec = copy.deepcopy(template)
                spec.update(name=name, universe=[asset + '/USDT'], sources=plan['sources'])
                spec['parameters'].update(asset=asset,trend_sma_days=look,entry_rsi_threshold=hurdle,rsi_period=2,exit_sma_days=5,zero_gain_and_loss_RSI=50,RSI_seed='Simplemean first2datasetclosechanges atday2;then(previous+new)/2;no resets',arithmetic='exact Fraction from daily Float64 decimal-string encoding',display_precision=60,SMA_window='j-N+1..j:includes completed signal close',threshold_arithmetic='exact rational RSI comparison and price*N versus exact close sums;canonical RSIratioSHA in decisions')
                assert spec['parameters']['exchange_filters_sha256'] == sha(R / 'exchange_filters.json')
                path = R / 'specs' / (name + '.json')
                put(path, spec)
                batch.append({'name': name, 'asset': asset, 'trend_sma_days': look, 'entry_rsi_threshold': hurdle, 'spec': rel(path), 'fingerprint': ev.registry.fingerprint(spec)})
    assert len(batch) == len({r['fingerprint'] for r in batch}) == 18
    put(R / 'batch.json', batch)
    put(R / 'spec.json', json.loads((R / 'specs/daily_wilder_rsi2_BTC_T150_E20.json').read_text()))
    reserves = []
    for row in batch:
        reserves.append(call('reserve', row))
        put(R / 'reserve.json', reserves)
    print('FROZEN_AND_RESERVED', len(reserves), sha(R / 'plan.json'), flush=True)

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
    context = json.loads((R / 'context.json').read_text())
    account_before = {p: sha(ROOT / p) for p in context['account_hashes_before']}
    audit = module(R / 'audit.py', 'rsi2_replay_audit')
    audit.R, audit.ev = R, ev
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        audit.main()
    plan = json.loads((R / 'plan.json').read_text())
    markets = {a: ev.load_asset(a, plan) for a in ('BTC', 'ETH')}
    decisions = list(csv.DictReader(gzip.open(R / 'decisions.csv.gz', 'rt')))
    trades=list(csv.DictReader(gzip.open(R/'trades.csv.gz','rt')))
    execution_trades={(t['configuration'],t['cost_multiplier'],t['execution_utc']):t for t in trades if t['terminal']=='False'}
    import numpy as np
    extrema_checks=0;volume_checks=0;volume_max_abs_difference=0.
    for market in markets.values():
        hi=market['minute_high'].reshape(730,1440).max(axis=1);lo=market['minute_low'].reshape(730,1440).min(axis=1)
        assert np.array_equal(hi,market['daily_high']) and np.array_equal(lo,market['daily_low']);extrema_checks+=len(hi)+len(lo)
        base=market['minute_base'].reshape(730,1440).sum(axis=1)
        assert np.allclose(base,market['daily_base_volume'],rtol=1e-12,atol=1e-8)
        volume_checks+=len(base);volume_max_abs_difference=max(volume_max_abs_difference,float(np.max(np.abs(base-market['daily_base_volume']))))
    independent,held_state={},{}
    for d in decisions:
        market=markets[d['asset']]
        signal_ms=int(datetime.fromisoformat(d['signal_day_utc'].replace('Z','+00:00')).timestamp()*1000)
        execution=int(datetime.fromisoformat(d['simulated_decision_at_utc'].replace('Z','+00:00')).timestamp()*1000)
        i=int((signal_ms-market['day_ts'][0])//ev.DAY_MS);look=int(d['trend_sma_days']);threshold=D(d['entry_rsi_threshold']);key=(d['asset'],look)
        assert execution==signal_ms+ev.DAY_MS+ev.MIN_MS
        if key not in independent:
            # Independent closed-form powers of two,not recursive Fraction averages or prefix SMA sums.
            from fractions import Fraction as F
            encoded=[D(str(x)).as_integer_ratio() for x in market['daily_close']];scale=math.lcm(*(b for a,b in encoded));cs=[a*(scale//b) for a,b in encoded];deltas=[cs[j]-cs[j-1] for j in range(1,len(cs))]
            g=sum(max(x,0) for x in deltas[:2]);loss=sum(max(-x,0) for x in deltas[:2]);values=[None]*len(cs)
            for j in range(2,len(cs)):
                if j>2:g+=max(deltas[j-1],0)*(1<<(j-2));loss+=max(-deltas[j-1],0)*(1<<(j-2))
                score=F(100*g,g+loss) if g+loss else F(50)
                if j>=look-1:values[j]=(score,F(sum(cs[j-look+1:j+1]),scale),F(sum(cs[j-4:j+1]),scale))
            independent[key]=values
        score,trend_sum,fast_sum=independent[key][i];close=F(str(market['daily_close'][i]))
        assert hashlib.sha256(f'{score.numerator}/{score.denominator}'.encode()).hexdigest()==d['rsi2_exact_ratio_sha256']
        assert F(d['trend_close_sum'])==trend_sum and F(d['exit_close_sum5'])==fast_sum
        assert math.isclose(float(score),float(d['rsi2_value']),rel_tol=1e-12,abs_tol=1e-12),(d['configuration'],'RSI2')
        account=(d['configuration'],d['cost_multiplier']);held=held_state.get(account,False)
        expected=not(close*5>fast_sum or close*look<trend_sum) if held else score<F(threshold) and close*look>trend_sum
        action='entry' if expected and not held else 'exit' if held and not expected else 'hold'
        assert d['desired_long']==str(expected) and d['action']==action
        trade=execution_trades.get((*account,d['simulated_decision_at_utc']))
        if trade and trade['status']=='filled':held_state[account]=D(trade['units_after'])>0
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
    assert all(sha(ROOT / p) == h for p, h in account_before.items()), 'Persistent account changed during verification.'
    assert all(sha(ROOT / p) == h for p, h in context['account_hashes_before'].items() if p != 'research/paper10/state.json'), 'Frozen source changed.'
    assert len(decisions) == 18 * 3 * 360
    result = {'passed': True, 'report_sha256': sha(R / 'report.json'), 'exact_replay': output.getvalue(), 'independent_integer_power_RSI2_SMA_state_and_timestamp_checks': len(decisions), 'independent_daily_high_low_aggregation_checks': extrema_checks, 'independent_daily_base_volume_aggregation_checks':volume_checks,'volume_sum_max_abs_float_difference':volume_max_abs_difference,'balance_conservation_checks': sum(t['status'] == 'filled' for t in trades), 'independent_capital_anchored_minute_drawdown_checks': 54, 'persistent_accounts_unchanged': True, 'maximum_observed_participation': max(float(t['participation']) for t in trades), 'minimum_event_notional_capacity_usdt_at_0_1pct_ADV': min(float(D(t['lagged_ADV']) * D('.001')) for t in trades)}
    print(json.dumps(result), flush=True)
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('freeze', 'evaluate', 'verify'))
    globals()[parser.parse_args().command]()
