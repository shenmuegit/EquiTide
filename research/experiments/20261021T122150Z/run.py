#!/usr/bin/env python3
"""Pre-register and verify a signed-efficiency-ratio batch using the archived ROC engine."""
import argparse, contextlib, copy, csv, gzip, hashlib, importlib.util, io, json, math, subprocess, sys, urllib.request
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
R = Path(__file__).resolve().parent
BASE = ROOT / 'research/experiments/20261014T125820Z'
REG = ROOT / 'research/automation/registry.jsonl'
LOOKS, HURDLES = [21, 42, 63], [10, 20, 30]

def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    spec.loader.exec_module(value)
    return value

ev = module(R / 'evaluate.py', 'signed_efficiency_engine')
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
    accounts = [ROOT / 'research/paper10/plan.json', ROOT / 'research/paper10/state.json', ROOT / 'research/experiments/20261021T102104Z/forward_state.json', ROOT / 'research/experiments/20261021T102104Z/forward_report.json']
    prior = [{'path': rel(p), 'sha256': sha(p), 'opening': ' '.join(t.strip() for t in p.read_text().splitlines() if t.strip() and not t.startswith('#'))[:240]} for p in sorted((ROOT / 'research/experiments').glob('*/result.md'))]
    context = {'registry_events': len(events), 'registry_ids': len(records), 'canonical_research_definitions_excluding_observations': len(canonical), 'main_registry_sha256_before_reserve': sha(REG), 'initial_16_missing_actual_results': 0, 'prior_conclusions_read': prior, 'account_hashes_before': {rel(p): sha(p) for p in accounts}}
    put(R / 'context.json', context)
    plan = json.loads((BASE / 'plan.json').read_text())
    plan.update(round=R.name, frozen_at_utc=now(), trigger_utc='2026-10-21T12:21:50.243Z', direction='Daily signed efficiency ratio trend filter.', hypothesis='Normalize net price movement by total absolute movement to reject choppy paths before entering a long-only trend position. This differs from a raw-return hurdle and is a new economic hypothesis on reused development data, not independent validation.')
    plan['grid'].update(lookback_days=LOOKS, entry_hurdle_pct=HURDLES)
    plan['sources'] = [{'citation': 'TA-Lib KAMA source: net movement / accumulated absolute one-bar movement efficiency construction.', 'url': 'https://github.com/TA-Lib/ta-lib/blob/59489444d4f5a659fc35cfd918a0a6ce5bc875c2/src/ta_func/ta_KAMA.c', 'version_commit': '59489444d4f5a659fc35cfd918a0a6ce5bc875c2', 'accessed_utc': '2026-10-21', 'scope': 'Motivation and denominator definition only. This signed flat=0 trading filter is an explicit adaptation, not KAMA smoothing or a profitability replication.'}, {'url': 'https://developers.binance.com/en/docs/products/spot/filters', 'accessed_utc': '2026-10-21', 'scope': 'Official execution filter definitions; current filters are historical proxies.'}]
    plan['costs']['filters_source'] = 'Unchanged 2026-10-14 frozen public exchangeInfo proxy, checked against the current public response in filter_check.json. Reuse the original hash so retrieval timestamps cannot manufacture novelty. Historical L2 and historical filters are unavailable.'
    plan['prior_results'] = {'source_report': 'research/experiments/20261021T102104Z/report.json', 'source_sha256': sha(ROOT / 'research/experiments/20261021T102104Z/report.json'), 'initial_16_missing_actual_results': 0, 'canonical_prior_research_definitions': len(canonical), 'last_batch': '18 long-horizon raw-return configurations rejected; read-only reference.', 'distinction': 'Signed path-efficiency filtering replaces raw-return hurdle; full rules and parameter values determine novelty.'}
    plan['validation']['purging'] = 'No fitted model, labels or OOS parameter selection; label purge is inapplicable. Fixed signals use prior closed bars; account state is continuous across 12 chronological windows.'
    plan['account_scope'] = 'Offline research only. Read existing paper10 and delayed SMA-shadow accounts without reset, replacement, new paper observations or real orders.'
    plan['rule'].update(signal='SER_L=(close[j]-close[j-L])/sum(abs(close[k]-close[k-1]), k=j-L+1..j); use L+1 completed daily closes. Flat path returns0; bound score to[-1,1].', entry='When flat, enter only if SER_L is strictly greater than the frozen0.1/0.2/0.3 threshold.', exit='When long, exit if SER_L<=0; between thresholds preserve the long position.')
    plan['validation']['continuous_drawdown'] = 'Initial capital plus all OOS minute-close and immediate post-fill marks; no fold reset or intraminute extrema.'
    put(R / 'plan.json', plan)
    template = json.loads((BASE / 'specs/daily_roc_momentum_BTC_L7_H0.json').read_text())
    template['family'] = 'spot-daily-directional-efficiency-hysteresis'
    template['logic']['entry'] = 'On a newly closed UTC daily bar j, signed efficiency=(close[j]-close[j-L])/sum(abs(close[k]-close[k-1]), k=j-L+1..j); flat denominator yields0. If flat, enter only when signed efficiency > entry_hurdle_fraction; strict inequality.'
    template['logic']['exit'] = 'When long, exit when signed efficiency<=0; otherwise preserve prior target. Entry and exit depend only on L+1 completed daily closes.'
    batch = []
    for asset in ('BTC', 'ETH'):
        for look in LOOKS:
            for hurdle in HURDLES:
                name = f"daily_efficiency_{asset}_L{look}_H{str(hurdle).replace('.', 'p')}"
                spec = copy.deepcopy(template)
                spec.update(name=name, universe=[asset + '/USDT'], sources=plan['sources'])
                spec['parameters'].update(asset=asset, lookback_days=look, entry_hurdle_fraction=hurdle / 100)
                assert spec['parameters']['exchange_filters_sha256'] == sha(R / 'exchange_filters.json')
                path = R / 'specs' / (name + '.json')
                put(path, spec)
                batch.append({'name': name, 'asset': asset, 'lookback_days': look, 'entry_hurdle_pct': hurdle, 'spec': rel(path), 'fingerprint': ev.registry.fingerprint(spec)})
    assert len(batch) == len({r['fingerprint'] for r in batch}) == 18
    put(R / 'batch.json', batch)
    put(R / 'spec.json', json.loads((R / 'specs/daily_efficiency_BTC_L42_H20.json').read_text()))
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
    audit = module(BASE / 'audit.py', 'long_roc_replay_audit')
    audit.R, audit.ev = R, ev
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        audit.main()
    plan = json.loads((R / 'plan.json').read_text())
    markets = {a: ev.load_asset(a, plan) for a in ('BTC', 'ETH')}
    decisions = list(csv.DictReader(gzip.open(R / 'decisions.csv.gz', 'rt')))
    for d in decisions:
        m = markets[d['asset']]
        signal = int(datetime.fromisoformat(d['signal_day_utc'].replace('Z', '+00:00')).timestamp() * 1000)
        execution = int(datetime.fromisoformat(d['simulated_decision_at_utc'].replace('Z', '+00:00')).timestamp() * 1000)
        i = int((signal - m['day_ts'][0]) // ev.DAY_MS)
        assert execution == signal + ev.DAY_MS + ev.MIN_MS
        window = [D(str(x)) for x in m['daily_close'][i-int(d['lookback_days']):i+1]]
        movement = sum(abs(b-a) for a,b in zip(window,window[1:]))
        score = float((window[-1]-window[0])/movement) if movement else 0.
        assert math.isclose(score, float(d['signed_efficiency_ratio']), rel_tol=1e-12, abs_tol=1e-12)
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
    result = {'passed': True, 'report_sha256': sha(R / 'report.json'), 'exact_replay': output.getvalue(), 'independent_efficiency_and_timestamp_checks': len(decisions), 'balance_conservation_checks': sum(t['status'] == 'filled' for t in trades), 'independent_capital_anchored_minute_drawdown_checks': 54, 'persistent_accounts_unchanged': True, 'maximum_observed_participation': max(float(t['participation']) for t in trades), 'minimum_event_notional_capacity_usdt_at_0_1pct_ADV': min(float(D(t['lagged_ADV']) * D('.001')) for t in trades)}
    print(json.dumps(result), flush=True)
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('freeze', 'evaluate', 'verify'))
    globals()[parser.parse_args().command]()
