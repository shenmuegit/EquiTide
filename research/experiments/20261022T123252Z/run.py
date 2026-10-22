#!/usr/bin/env python3
"""Pre-register base-volume MFI momentum and independently verify exact Fraction flows."""
import argparse, contextlib, copy, csv, gzip, hashlib, importlib.util, io, json, math, subprocess, sys, urllib.request
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
R = Path(__file__).resolve().parent
BASE = ROOT / 'research/experiments/20261014T125820Z'
REG = ROOT / 'research/automation/registry.jsonl'
LOOKS, HURDLES = [10, 20, 40], [50, 60, 70]

def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    spec.loader.exec_module(value)
    return value

ev = module(R / 'evaluate.py', 'daily_mfi_engine')
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
    accounts = [ROOT / 'research/paper10/plan.json', ROOT / 'research/paper10/state.json', ROOT / 'research/experiments/20261022T103152Z/forward_state.json', ROOT / 'research/experiments/20261022T103152Z/forward_report.json']
    prior = [{'path': rel(p), 'sha256': sha(p), 'opening': ' '.join(t.strip() for t in p.read_text().splitlines() if t.strip() and not t.startswith('#'))[:240]} for p in sorted((ROOT / 'research/experiments').glob('*/result.md'))]
    context = {'registry_events': len(events), 'registry_ids': len(records), 'canonical_research_definitions_excluding_observations': len(canonical), 'main_registry_sha256_before_reserve': sha(REG), 'initial_16_missing_actual_results': 0, 'prior_conclusions_read': prior, 'account_hashes_before': {rel(p): sha(p) for p in accounts}}
    put(R / 'context.json', context)
    plan = json.loads((BASE / 'plan.json').read_text())
    plan.update(round=R.name,frozen_at_utc=now(),trigger_utc='2026-10-22T12:32:52.305Z',direction='Daily base-volume Money Flow Index momentum with fixed45exit,unlevered spot long/cash.',hypothesis='Weight typical-price directional days by raw base-volume money flow. Test whether positive flow dominance with a lower exit boundary survives costs and varied regimes. This is our momentum hypothesis;source documentation cautions against assuming that MFI centerline bias is a reliable trend signal.')
    plan['grid'].update(mfi_lookback_days=LOOKS,entry_mfi_threshold=HURDLES,exit_mfi_threshold=45,flow_window='j-N+1..j:Ndirectional flows requiringN+1daily prices',zero_total_flow_MFI=50,flow_arithmetic_precision=60,volume_units='base asset units,sum of1440closed minutes')
    for key in ('lookback_days','entry_hurdle_pct','exit_hurdle_pct'):plan['grid'].pop(key)
    plan['sources']=[{'url':'https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/money-flow-index-mfi','accessed_utc':'2026-10-22','version_observed':'Current official StockCharts ChartSchool documentation','scope':'Primary definition TP*volume,positive/negative TP-direction flows and exclusion of unchangedTP. Our momentum rules and neutral50zero-flow convention are independent choices,not profitability endorsement.'},{'url':'https://raw.githubusercontent.com/TA-Lib/ta-lib/v0.6.4/src/ta_func/ta_MFI.c','accessed_utc':'2026-10-22','version_observed':'TA-Lib v0.6.4','scope':'Primary implementation confirms Nflows with an earlierTP and unchanged-price exclusion. We do not use its total-flow<1 zero guard:exact total-flow0 is independently fixed to50. No equivalence claim,library install or copied C source.'},{'url':'https://developers.binance.com/en/docs/products/spot/filters','accessed_utc':'2026-10-22','scope':'Official spot filter definitions;historical filters unavailable.'}]
    plan['source_access_failures']=[]
    plan['costs']['filters_source'] = 'Unchanged 2026-10-14 frozen public exchangeInfo proxy, checked against the current public response in filter_check.json. Reuse the original hash so retrieval timestamps cannot manufacture novelty. Historical L2 and historical filters are unavailable.'
    plan['prior_results']={'source_report':'research/experiments/20261022T103152Z/report.json','source_sha256':sha(ROOT/'research/experiments/20261022T103152Z/report.json'),'initial_16_missing_actual_results':0,'canonical_prior_research_definitions':len(canonical),'last_batch':'18 CCI candidates rejected;two all-cost positive cells did not meet fold breadth or full robustness.','distinction':'MFI weights typical-price direction by actual daily base volume,not a price-only mean-deviation score or extrema age.'}
    plan['validation']['purging']='No fitted model or future-return labels;label purge inapplicable. Ncomplete directional flows requireN+1completed daily prices;first valid indexN. No future padding,seed,OOS/fold reset or parameter selection.365day context and3day initial gap precede12continuous folds.'
    plan['account_scope'] = 'Offline research only. Read existing paper10 and delayed SMA-shadow accounts without reset, replacement, new paper observations or real orders.'
    signal_rule='Aggregate UTC daily high/low,last close and base volume over1440closed minutes. TP=(H+L+C)/3. Raw flow=TP*base_volume;assign to positive ifTP rises,negative ifTP falls,zero to both whenTP ties. Sum Nflows overj-N+1..j,using earlierTP atj-N. MFI=100*positive/(positive+negative);if total exactly0,set50. For exact thresholds use TP3=H+L+C,flow3=TP3*volume,which cancels the common3. Local Decimal60 flow arithmetic and cross-multiplied thresholds;accounting kernel remainsDecimal28. No seed/fold reset.'
    plan['rule'].update(signal=signal_rule,entry='When flat,enter iff MFI>E;strict boundary,no prior-cross requirement,including first OOS decision. Zero total flow yields neutral50.',exit='When long,exit iff MFI<45;equality45keeps long. Zero total flow50keeps long. No short,hold cap or same-decision re-entry;costed terminal liquidation.')
    plan['validation']['parameter_sensitivity_axes']=['mfi_lookback_days','entry_mfi_threshold']
    plan['validation']['continuous_drawdown'] = 'Initial capital plus all OOS minute-close and immediate post-fill marks; no fold reset or intraminute extrema.'
    put(R / 'plan.json', plan)
    template = json.loads((BASE / 'specs/daily_roc_momentum_BTC_L7_H0.json').read_text())
    template['family']='spot-daily-mfi-momentum'
    template['logic']['entry']=signal_rule+' When flat,enter iff MFI>entry_mfi_threshold;strict cross-multiplied comparison,no prior-cross requirement.'
    template['logic']['exit']='While long,exit iff MFI<45. Exact45and zero-flow-neutral50keep long;flat stays cash at or below entry threshold. No future padding,fold reset,short,hold cap or same-decision re-entry. Costed terminal liquidation.'
    for key in ('lookback_days','entry_hurdle_fraction','exit_hurdle_fraction'):template['parameters'].pop(key)
    template['parameters']['sensitivity_axes']=['mfi_lookback_days','entry_mfi_threshold']
    batch = []
    for asset in ('BTC', 'ETH'):
        for look in LOOKS:
            for hurdle in HURDLES:
                name = f"daily_mfi_{asset}_N{look}_E{hurdle}"
                spec = copy.deepcopy(template)
                spec.update(name=name, universe=[asset + '/USDT'], sources=plan['sources'])
                spec['parameters'].update(asset=asset, mfi_lookback_days=look, entry_mfi_threshold=hurdle, exit_mfi_threshold=45, zero_total_flow_MFI=50, flow_arithmetic_precision=60, window="Nflows:j-N+1..j,withTP atj-N", volume_units="base asset units,sum of1440closed minutes", threshold_arithmetic="unrounded factors with neutral50when total0")
                assert spec['parameters']['exchange_filters_sha256'] == sha(R / 'exchange_filters.json')
                path = R / 'specs' / (name + '.json')
                put(path, spec)
                batch.append({'name': name, 'asset': asset, 'mfi_lookback_days': look, 'entry_mfi_threshold': hurdle, 'spec': rel(path), 'fingerprint': ev.registry.fingerprint(spec)})
    assert len(batch) == len({r['fingerprint'] for r in batch}) == 18
    put(R / 'batch.json', batch)
    put(R / 'spec.json', json.loads((R / 'specs/daily_mfi_BTC_N20_E60.json').read_text()))
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
    audit = module(R / 'audit.py', 'mfi_replay_audit')
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
        i=int((signal_ms-market['day_ts'][0])//ev.DAY_MS);look=int(d['mfi_lookback_days']);threshold=int(d['entry_mfi_threshold']);key=(d['asset'],look)
        assert execution==signal_ms+ev.DAY_MS+ev.MIN_MS
        if key not in independent:
            from fractions import Fraction as F
            tp=[(F(str(h))+F(str(l))+F(str(c)))/3 for h,l,c in zip(market['daily_high'],market['daily_low'],market['daily_close'])];vol=[F(str(v)) for v in market['daily_base_volume']];values=[None]*len(tp)
            for j in range(look,len(tp)):
                positive=sum((tp[k]*vol[k] for k in range(j-look+1,j+1) if tp[k]>tp[k-1]),F(0));negative=sum((tp[k]*vol[k] for k in range(j-look+1,j+1) if tp[k]<tp[k-1]),F(0));total=positive+negative
                values[j]=100*positive/total if total else F(50)
            independent[key]=values
        score=independent[key][i];num,den=F(d['mfi_numerator']),F(d['mfi_denominator'])
        assert (num/den if den else F(50))==score
        assert math.isclose(float(score),float(d['mfi_value']),rel_tol=1e-12,abs_tol=1e-12),(d['configuration'],'MFI')
        account=(d['configuration'],d['cost_multiplier']);held=held_state.get(account,False);expected=score>=45 if held else score>threshold
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
    result = {'passed': True, 'report_sha256': sha(R / 'report.json'), 'exact_replay': output.getvalue(), 'independent_Fraction_MFI_state_and_timestamp_checks': len(decisions), 'independent_daily_high_low_aggregation_checks': extrema_checks, 'independent_daily_base_volume_aggregation_checks':volume_checks,'volume_sum_max_abs_float_difference':volume_max_abs_difference,'balance_conservation_checks': sum(t['status'] == 'filled' for t in trades), 'independent_capital_anchored_minute_drawdown_checks': 54, 'persistent_accounts_unchanged': True, 'maximum_observed_participation': max(float(t['participation']) for t in trades), 'minimum_event_notional_capacity_usdt_at_0_1pct_ADV': min(float(D(t['lagged_ADV']) * D('.001')) for t in trades)}
    print(json.dumps(result), flush=True)
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('freeze', 'evaluate', 'verify'))
    globals()[parser.parse_args().command]()
