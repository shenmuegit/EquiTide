#!/usr/bin/env python3
"""Pre-register HMA-slope rules and verify them with an exact rational convolution kernel."""
import argparse, contextlib, copy, csv, gzip, hashlib, importlib.util, io, json, math, subprocess, sys, urllib.request
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
R = Path(__file__).resolve().parent
BASE = ROOT / 'research/experiments/20261014T125820Z'
REG = ROOT / 'research/automation/registry.jsonl'
LOOKS, HURDLES = [40, 80, 160], [1, 3, 5]

def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    spec.loader.exec_module(value)
    return value

ev = module(R / 'evaluate.py', 'daily_hma_engine')
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
    accounts = [ROOT / 'research/paper10/plan.json', ROOT / 'research/paper10/state.json', ROOT / 'research/experiments/20261022T042721Z/forward_state.json', ROOT / 'research/experiments/20261022T042721Z/forward_report.json']
    prior = [{'path': rel(p), 'sha256': sha(p), 'opening': ' '.join(t.strip() for t in p.read_text().splitlines() if t.strip() and not t.startswith('#'))[:240]} for p in sorted((ROOT / 'research/experiments').glob('*/result.md'))]
    context = {'registry_events': len(events), 'registry_ids': len(records), 'canonical_research_definitions_excluding_observations': len(canonical), 'main_registry_sha256_before_reserve': sha(REG), 'initial_16_missing_actual_results': 0, 'prior_conclusions_read': prior, 'account_hashes_before': {rel(p): sha(p) for p in accounts}}
    put(R / 'context.json', context)
    plan = json.loads((BASE / 'plan.json').read_text())
    plan.update(round=R.name,frozen_at_utc=now(),trigger_utc='2026-10-22T06:29:21.852Z',direction='Daily Hull moving-average slope, unlevered spot long/cash.',hypothesis='Use a finite weighted-average lag correction and short outer smoothing, then follow its direction rather than price crossovers. Test whether smoother turning directions survive costs and regimes after adaptive KAMA failed; reduced indicator lag alone is not evidence of return predictability.')
    plan['grid'].update(hma_span_days=LOOKS,slope_lookback_days=HURDLES,half_span_rounding='floor',root_span_rounding='integer_floor_isqrt')
    for key in ('lookback_days','entry_hurdle_pct','exit_hurdle_pct'):plan['grid'].pop(key)
    plan['sources']=[{'url':'https://alanhull.com/the-hull-moving-average/','accessed_utc':'2026-10-22','version_observed':'Current author article, originally described as2005 work','scope':'Author primary source for WMA(sqrtN) of2WMA(N/2)-WMA(N), integer period convention and direction/turning-point use rather than crossover. Our exact floor indices and1/3/5day sign rule are explicitly fixed, without source-backed profitability claims.'},{'url':'https://developers.binance.com/en/docs/products/spot/filters','accessed_utc':'2026-10-22','scope':'Official spot filter definitions; historical filters unavailable.'}]
    plan['source_access_failures']=[]
    plan['costs']['filters_source'] = 'Unchanged 2026-10-14 frozen public exchangeInfo proxy, checked against the current public response in filter_check.json. Reuse the original hash so retrieval timestamps cannot manufacture novelty. Historical L2 and historical filters are unavailable.'
    plan['prior_results']={'source_report':'research/experiments/20261022T042721Z/report.json','source_sha256':sha(ROOT/'research/experiments/20261022T042721Z/report.json'),'initial_16_missing_actual_results':0,'canonical_prior_research_definitions':len(canonical),'last_batch':'All18 KAMA candidates lost in all three cost stresses; neither adaptive price anchor nor fixed band passed.','distinction':'Finite-window Hull average, integer half/root periods and sign of a lagged HMA difference; no adaptive ER smoothing or price-band crossover.'}
    plan['validation']['purging']='No fitted model or future-return labels; label purge inapplicable. Finite complete WMA windows only, no EMA seed, future padding, OOS/fold reset or parameter selection. First HMA indexN+floor(sqrtN)-2; a slope decision needs additionalM complete days.365day context and3day initial gap precede12 continuous folds.'
    plan['account_scope'] = 'Offline research only. Read existing paper10 and delayed SMA-shadow accounts without reset, replacement, new paper observations or real orders.'
    signal_rule='WMA_k[j]=sum(i=1..k,i*C[j-k+i])/sum(i=1..k,i), newest weightk. Set half=floor(N/2),root=floor(sqrtN)=isqrt(N). raw[j]=2*WMA_half[j]-WMA_N[j];HMA[j]=WMA_root(raw)[j],complete windows only,Decimal28. First HMA indexN+root-2. delta[j]=HMA[j]-HMA[j-M] uses only completed daily closes. No EMA seed or fold reset.'
    plan['rule'].update(signal=signal_rule,entry='When flat, enter iff completed HMA delta>0; strict sign, no previous-cross requirement, including first OOS decision.',exit='When long, exit iff HMA delta<0. Exact zero preserves actual cash/held state. No price crossover/band, short, hold cap or same-decision re-entry; costed terminal liquidation.')
    plan['validation']['parameter_sensitivity_axes']=['hma_span_days','slope_lookback_days']
    plan['validation']['continuous_drawdown'] = 'Initial capital plus all OOS minute-close and immediate post-fill marks; no fold reset or intraminute extrema.'
    put(R / 'plan.json', plan)
    template = json.loads((BASE / 'specs/daily_roc_momentum_BTC_L7_H0.json').read_text())
    template['family']='spot-daily-hull-ma-slope'
    template['logic']['entry']=signal_rule+' When flat, enter iff delta>0; no prior-cross requirement.'
    template['logic']['exit']='While long, exit iff delta<0. Exact zero preserves actual cash/held state. No future padding, price crossover/band, fold reset, short, hold cap or same-decision re-entry. Costed terminal liquidation.'
    for key in ('lookback_days','entry_hurdle_fraction','exit_hurdle_fraction'):template['parameters'].pop(key)
    template['parameters']['sensitivity_axes']=['hma_span_days','slope_lookback_days']
    batch = []
    for asset in ('BTC', 'ETH'):
        for look in LOOKS:
            for hurdle in HURDLES:
                name = f"daily_hma_slope_{asset}_N{look}_M{hurdle}"
                spec = copy.deepcopy(template)
                spec.update(name=name, universe=[asset + '/USDT'], sources=plan['sources'])
                spec['parameters'].update(asset=asset, hma_span_days=look, slope_lookback_days=hurdle, half_span_rounding="floor", root_span_rounding="integer_floor_isqrt", entry_delta=0, exit_delta=0, zero_delta_action="preserve_actual_held_state")
                assert spec['parameters']['exchange_filters_sha256'] == sha(R / 'exchange_filters.json')
                path = R / 'specs' / (name + '.json')
                put(path, spec)
                batch.append({'name': name, 'asset': asset, 'hma_span_days': look, 'slope_lookback_days': hurdle, 'spec': rel(path), 'fingerprint': ev.registry.fingerprint(spec)})
    assert len(batch) == len({r['fingerprint'] for r in batch}) == 18
    put(R / 'batch.json', batch)
    put(R / 'spec.json', json.loads((R / 'specs/daily_hma_slope_BTC_N80_M3.json').read_text()))
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
    audit = module(R / 'audit.py', 'macd_replay_audit')
    audit.R, audit.ev = R, ev
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        audit.main()
    plan = json.loads((R / 'plan.json').read_text())
    markets = {a: ev.load_asset(a, plan) for a in ('BTC', 'ETH')}
    decisions = list(csv.DictReader(gzip.open(R / 'decisions.csv.gz', 'rt')))
    trades=list(csv.DictReader(gzip.open(R/'trades.csv.gz','rt')))
    execution_trades={(t['configuration'],t['cost_multiplier'],t['execution_utc']):t for t in trades if t['terminal']=='False'}
    independent,held_state={},{}
    for d in decisions:
        market=markets[d['asset']]
        signal_ms=int(datetime.fromisoformat(d['signal_day_utc'].replace('Z','+00:00')).timestamp()*1000)
        execution=int(datetime.fromisoformat(d['simulated_decision_at_utc'].replace('Z','+00:00')).timestamp()*1000)
        i=int((signal_ms-market['day_ts'][0])//ev.DAY_MS);span=int(d['hma_span_days']);lag=int(d['slope_lookback_days']);key=(d['asset'],span)
        assert execution==signal_ms+ev.DAY_MS+ev.MIN_MS
        if key not in independent:
            from fractions import Fraction
            prices=[Fraction(str(v)) for v in market['daily_close']];half=span//2;root=math.isqrt(span)
            dh=half*(half+1)//2;dn=span*(span+1)//2;dr=root*(root+1)//2;den=dh*dn*dr
            base=[(2*(half-a)*dn if a<half else 0)-(span-a)*dh for a in range(span)]
            kernel=[sum(base[a]*(root-(age-a)) for a in range(span) if 0<=age-a<root) for age in range(span+root-1)]
            assert sum(kernel)==den
            values=[None]*len(prices)
            for j in range(len(kernel)-1,len(prices)):
                values[j]=sum((weight*prices[j-a] for a,weight in enumerate(kernel)),Fraction(0))/den
            independent[key]=values
        values=independent[key];anchor=values[i];previous_anchor=values[i-lag];delta=anchor-previous_anchor
        for actual,field in [(anchor,'hma'),(previous_anchor,'prior_hma'),(delta,'slope_delta')]:assert math.isclose(float(actual),float(d[field]),rel_tol=1e-9,abs_tol=1e-7),(d['configuration'],field)
        account=(d['configuration'],d['cost_multiplier']);held=held_state.get(account,False)
        expected=held if delta==0 else delta>0
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
    result = {'passed': True, 'report_sha256': sha(R / 'report.json'), 'exact_replay': output.getvalue(), 'independent_exact_rational_HMA_kernel_state_and_timestamp_checks': len(decisions), 'balance_conservation_checks': sum(t['status'] == 'filled' for t in trades), 'independent_capital_anchored_minute_drawdown_checks': 54, 'persistent_accounts_unchanged': True, 'maximum_observed_participation': max(float(t['participation']) for t in trades), 'minimum_event_notional_capacity_usdt_at_0_1pct_ADV': min(float(D(t['lagged_ADV']) * D('.001')) for t in trades)}
    print(json.dumps(result), flush=True)
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('freeze', 'evaluate', 'verify'))
    globals()[parser.parse_args().command]()
