#!/usr/bin/env python3
"""Pre-register and verify close-channel breakouts with an explicit filled-position age limit."""
import argparse, contextlib, copy, csv, gzip, hashlib, importlib.util, io, json, math, subprocess, sys, urllib.request
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
R = Path(__file__).resolve().parent
BASE = ROOT / 'research/experiments/20261014T125820Z'
REG = ROOT / 'research/automation/registry.jsonl'
LOOKS, HURDLES = [10, 20, 40], [5, 10, 20]

def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    spec.loader.exec_module(value)
    return value

ev = module(R / 'evaluate.py', 'daily_channel_timeout_engine')
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
    accounts = [ROOT / 'research/paper10/plan.json', ROOT / 'research/paper10/state.json', ROOT / 'research/experiments/20261021T182350Z/forward_state.json', ROOT / 'research/experiments/20261021T182350Z/forward_report.json']
    prior = [{'path': rel(p), 'sha256': sha(p), 'opening': ' '.join(t.strip() for t in p.read_text().splitlines() if t.strip() and not t.startswith('#'))[:240]} for p in sorted((ROOT / 'research/experiments').glob('*/result.md'))]
    context = {'registry_events': len(events), 'registry_ids': len(records), 'canonical_research_definitions_excluding_observations': len(canonical), 'main_registry_sha256_before_reserve': sha(REG), 'initial_16_missing_actual_results': 0, 'prior_conclusions_read': prior, 'account_hashes_before': {rel(p): sha(p) for p in accounts}}
    put(R / 'context.json', context)
    plan = json.loads((BASE / 'plan.json').read_text())
    plan.update(round=R.name, frozen_at_utc=now(), trigger_utc='2026-10-21T20:23:50.803Z', direction='Prior-close channel breakout with a maximum filled-position holding time.', hypothesis='A fixed holding-time cap may limit adverse drift or concentration after a breakout, at the cost of extra turnover and potentially truncating sustained trends. Test both lookback and holding cap before observing this grid; no profitability claim.')
    plan['grid'].update(entry_lookback_days=LOOKS,max_holding_days=HURDLES,exit_lookback_days=10)
    for key in ('lookback_days','entry_hurdle_pct','exit_hurdle_pct'):plan['grid'].pop(key)
    plan['sources'] = [
        {'url':'https://www.tradingview.com/support/solutions/43000502253-donchian-channels-dc/','accessed_utc':'2026-10-21','scope':'Primary channel reference uses high/low extrema. Our generated close-only lagged channel is explicitly a different rule, not a literal replication or a profitability endorsement.'},
        {'url':'https://www.tradingview.com/pine-script-docs/faq/strategies/','accessed_utc':'2026-10-21','version':'Pine Script6 official FAQ','scope':'Time-based exit example tracks the executed entry timestamp. Our daily next-minute model retains a60second signal delay and does not use their same-close immediate order example.'},
        {'url':'https://developers.binance.com/en/docs/products/spot/filters','accessed_utc':'2026-10-21','scope':'Official filter definitions; historical filters remain unavailable.'}]
    plan['source_access_failures'] = []
    plan['costs']['filters_source'] = 'Unchanged 2026-10-14 frozen public exchangeInfo proxy, checked against the current public response in filter_check.json. Reuse the original hash so retrieval timestamps cannot manufacture novelty. Historical L2 and historical filters are unavailable.'
    plan['prior_results']={'source_report':'research/experiments/20261021T182350Z/report.json','source_sha256':sha(ROOT/'research/experiments/20261021T182350Z/report.json'),'initial_16_missing_actual_results':0,'canonical_prior_research_definitions':len(canonical),'last_batch':'18 Wilder-RSI configurations rejected; highest return came from one round trip/one profitable fold.','distinction':'Close-based breakout with a filled-entry age cap and fixed10-day channel exit; new lookback/time-cap grid. Existing channel and ATR families are not excluded wholesale, but exact completed definitions remain blocked by reserve.'}
    plan['validation']['purging']='Fixed causal channel and elapsed-position age, no fitted model or future-return labels; label purge is inapplicable. Initial365day context plus3day gap; channel state and actual position age remain continuous across all12folds. No OOS parameter selection.'
    plan['account_scope'] = 'Offline research only. Read existing paper10 and delayed SMA-shadow accounts without reset, replacement, new paper observations or real orders.'
    signal_rule='At completed signal barj, upper=max(close[j-L:j]) and lower=min(close[j-10:j]), both exclude current signal bar. Compare Decimal close[j] with these strictly lagged levels. Track only successful entry fills at their next-day00:01UTC execution time; age is (current decision execution time minus that entry time)/86400000. Failed entries do not start the clock; failed exits preserve the existing clock.'
    plan['rule'].update(signal=signal_rule,entry='When flat, enter iff close[j]>upper. Equality remains cash.',exit='When long, first exit if age_days>=max_holding_days; otherwise exit iff close[j]<lower. Equality at lower holds unless the age cap applies. Exit precedence; no same-decision re-entry.')
    plan['validation']['parameter_sensitivity_axes']=['entry_lookback_days','max_holding_days']
    plan['validation']['continuous_drawdown'] = 'Initial capital plus all OOS minute-close and immediate post-fill marks; no fold reset or intraminute extrema.'
    put(R / 'plan.json', plan)
    template = json.loads((BASE / 'specs/daily_roc_momentum_BTC_L7_H0.json').read_text())
    template['family']='spot-daily-close-channel-breakout-timeout'
    template['logic']['entry']=signal_rule+' While flat, enter iff close[j]>upper; equality remains cash.'
    template['logic']['exit']='While long, exit first when filled-position age>=max_holding_days, otherwise when close[j]<min(previous exit_lookback_days closes excludingj). Lower-bound equality holds before timeout. No same-decision re-entry; terminal liquidation remains costed.'
    for key in ('lookback_days','entry_hurdle_fraction','exit_hurdle_fraction'):template['parameters'].pop(key)
    template['parameters']['sensitivity_axes']=['entry_lookback_days','max_holding_days']
    batch = []
    for asset in ('BTC', 'ETH'):
        for look in LOOKS:
            for hurdle in HURDLES:
                name = f"daily_channel_timeout_{asset}_E{look}_T{hurdle}"
                spec = copy.deepcopy(template)
                spec.update(name=name, universe=[asset + '/USDT'], sources=plan['sources'])
                spec['parameters'].update(asset=asset, entry_lookback_days=look, max_holding_days=hurdle, exit_lookback_days=10)
                assert spec['parameters']['exchange_filters_sha256'] == sha(R / 'exchange_filters.json')
                path = R / 'specs' / (name + '.json')
                put(path, spec)
                batch.append({'name': name, 'asset': asset, 'entry_lookback_days': look, 'max_holding_days': hurdle, 'spec': rel(path), 'fingerprint': ev.registry.fingerprint(spec)})
    assert len(batch) == len({r['fingerprint'] for r in batch}) == 18
    put(R / 'batch.json', batch)
    put(R / 'spec.json', json.loads((R / 'specs/daily_channel_timeout_BTC_E20_T10.json').read_text()))
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
    audit = module(R / 'audit.py', 'channel_timeout_replay_audit')
    audit.R, audit.ev = R, ev
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        audit.main()
    plan = json.loads((R / 'plan.json').read_text())
    markets = {a: ev.load_asset(a, plan) for a in ('BTC', 'ETH')}
    decisions = list(csv.DictReader(gzip.open(R / 'decisions.csv.gz', 'rt')))
    trades = list(csv.DictReader(gzip.open(R / 'trades.csv.gz', 'rt')))
    execution_trades={(t['configuration'],t['cost_multiplier'],t['execution_utc']):t for t in trades if t['terminal']=='False'}
    entered = {}
    for d in decisions:
        m=markets[d['asset']]
        signal=int(datetime.fromisoformat(d['signal_day_utc'].replace('Z','+00:00')).timestamp()*1000)
        execution=int(datetime.fromisoformat(d['simulated_decision_at_utc'].replace('Z','+00:00')).timestamp()*1000)
        i=int((signal-m['day_ts'][0])//ev.DAY_MS);n=int(d['entry_lookback_days']);limit=int(d['max_holding_days'])
        assert execution==signal+ev.DAY_MS+ev.MIN_MS
        prices=[D(str(v)) for v in m['daily_close']];close=prices[i]
        assert all(D(d['entry_channel_high'])>=v for v in prices[i-n:i]) and D(d['entry_channel_high']) in prices[i-n:i]
        assert all(D(d['exit_channel_low'])<=v for v in prices[i-10:i]) and D(d['exit_channel_low']) in prices[i-10:i]
        account=(d['configuration'],d['cost_multiplier']);entry=entered.get(account);held=entry is not None
        age=(execution-entry)//ev.DAY_MS if held else 0
        assert age==int(d['elapsed_holding_days']) and d['position_entry_utc']==(ev.stamp(entry) if held else '')
        expected=(age<limit and any(close>=v for v in prices[i-10:i])) if held else all(close>v for v in prices[i-n:i])
        action='entry' if expected and not held else 'exit' if held and not expected else 'hold'
        assert d['desired_long']==str(expected) and d['action']==action
        if held and age>=limit:assert d['decision_reason']=='exit_maximum_holding_time' and action=='exit'
        trade=execution_trades.get((*account,d['simulated_decision_at_utc']))
        if trade and trade['status']=='filled':entered[account]=execution if D(trade['units_after'])>0 else None
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
    result = {'passed': True, 'report_sha256': sha(R / 'report.json'), 'exact_replay': output.getvalue(), 'independent_channel_extrema_filled_age_state_and_timestamp_checks': len(decisions), 'balance_conservation_checks': sum(t['status'] == 'filled' for t in trades), 'independent_capital_anchored_minute_drawdown_checks': 54, 'persistent_accounts_unchanged': True, 'maximum_observed_participation': max(float(t['participation']) for t in trades), 'minimum_event_notional_capacity_usdt_at_0_1pct_ADV': min(float(D(t['lagged_ADV']) * D('.001')) for t in trades)}
    print(json.dumps(result), flush=True)
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('freeze', 'evaluate', 'verify'))
    globals()[parser.parse_args().command]()
