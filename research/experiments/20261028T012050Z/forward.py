"""Resume the original SMA65 floating-quantity shadow; never touch paper10."""
import argparse, copy, gzip, json, math, subprocess, sys, urllib.parse, urllib.request
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path
from run import ROOT, R, reg, put, sha, rel, now, call, module

PREV = ROOT / 'research/experiments/20261027T231921Z'
DAILY = ROOT / 'research/experiments/20261027T011211Z/forward_inputs.json.gz'
LEGACY = module(ROOT / 'research/experiments/20261011T014626Z/forward.py', 'original_shadow_daily')
MINUTE, DAY = 60000, 86400000
ms = lambda s: int(datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp() * 1000)
iso = lambda n: datetime.fromtimestamp(n / 1000, timezone.utc).isoformat().replace('+00:00', 'Z')
readgz = lambda p: json.loads(gzip.decompress(p.read_bytes()))

def reserve():
    assert not (R / 'forward_resume_plan.json').exists()
    old = json.loads((PREV / 'forward_report.json').read_text())
    state = json.loads((PREV / 'forward_state.json').read_text())
    assert state['source_report_sha256'] == sha(PREV / 'forward_report.json')
    assert state['last_completed_mark_utc'] == old['cutoff_utc']
    frozen = ROOT / old['frozen_plan_path']
    assert sha(frozen) == old['frozen_plan_sha256'] == state['frozen_plan_sha256']
    plan = {'frozen_at_utc': now(), 'source_state': rel(PREV / 'forward_state.json'), 'state_sha256': sha(PREV / 'forward_state.json'), 'source_report': rel(PREV / 'forward_report.json'), 'report_sha256': sha(PREV / 'forward_report.json'), 'resume_utc': old['cutoff_utc'], 'cutoff_utc': '2026-10-28T00:30:00Z', 'frozen_original_plan': rel(frozen), 'frozen_original_plan_sha256': sha(frozen), 'daily_overlap_source': rel(DAILY), 'daily_overlap_sha256': sha(DAILY), 'rule': json.loads(frozen.read_text())['rules'], 'terminal_utc': json.loads(frozen.read_text())['planned_terminal_utc'], 'mode': 'Delayed reconstruction from completed public historical bars, not contemporaneous paper10 execution.', 'failure_criteria': 'Stop on missing/revised overlap, incomplete timestamps, daily/minute disagreement, altered frozen source, negative balances, participation >0.1%, or replay mismatch. No reset, retuning, retrospective paper10 trade or forced terminal sale.', 'qualification': 'Partial original shadow observation; no 180-day/sixfold qualification; rejection does not cancel the frozen plan.'}
    assert ms(plan['resume_utc']) < ms(plan['cutoff_utc']) <= ms(plan['frozen_at_utc'])
    oldpoints=len(old['configs']['forward_snapshot_combo']['scenes']['1']['equity_usdt']);newminutes=(ms(plan['cutoff_utc'])-ms(plan['resume_utc']))//MINUTE;events=list(range(ms(state['next_daily_decision_utc']),ms(plan['cutoff_utc']),DAY));assert len(events)==1 and iso(events[0])=='2026-10-28T00:01:00Z'
    plan['forward_resume']={'source_report':plan['source_report'],'report_sha256':plan['report_sha256'],'source_state':plan['source_state'],'state_sha256':plan['state_sha256'],'resume_utc':plan['resume_utc'],'cutoff_utc':plan['cutoff_utc'],'new_minutes':newminutes,'prior_NAV_points':oldpoints,'total_NAV_points':oldpoints+newminutes+len(events),'cumulative_minutes':old['configs']['forward_snapshot_combo']['scenes']['1']['elapsed_minutes']+newminutes,'new_daily_references':len(events)}
    put(R / 'forward_resume_plan.json', plan)
    batch, fingerprints = [], {}
    previous_batch = json.loads((PREV / 'forward_batch.json').read_text())
    for oldrow in previous_batch:
        spec = json.loads((ROOT / oldrow['spec']).read_text())
        spec['parameters']['end_utc'] = plan['cutoff_utc']
        spec['validation_plan'] = rel(R / 'forward_resume_plan.json')
        if spec['kind'] == 'combination':
            spec['components'] = [{'fingerprint': fingerprints[a], 'weight': w} for a, w in [('BTC', .75), ('ETH', .25)]]
        path = R / 'specs' / (oldrow['name'] + '.json')
        put(path, spec)
        row = {**oldrow, 'spec': rel(path), 'fingerprint': reg.fingerprint(spec)}
        if 'asset' in row: fingerprints[row['asset']] = row['fingerprint']
        batch.append(row)
    put(R / 'forward_batch.json', batch)
    done = []
    for row in batch:
        done.append(call('reserve', row)); put(R / 'forward_reserve.json', done)

def validate(plan, inputs):
    assert sha(ROOT / plan['source_report']) == plan['report_sha256'] and sha(ROOT / plan['source_state']) == plan['state_sha256']
    assert sha(ROOT / plan['frozen_original_plan']) == plan['frozen_original_plan_sha256']
    old = json.loads((ROOT / plan['source_report']).read_text())
    previous = readgz(ROOT / old['source_inputs_path'])
    assert sha(ROOT / plan['daily_overlap_source']) == plan['daily_overlap_sha256']
    earlier_daily = readgz(ROOT / plan['daily_overlap_source'])
    begin, cut = ms(plan['resume_utc']), ms(plan['cutoff_utc'])
    for asset in ('BTC', 'ETH'):
        minutes, daily = inputs[asset]['1m'], inputs[asset]['1d']
        prior = previous[asset]; prior = prior['1m'] if isinstance(prior, dict) else prior
        assert minutes[0] == prior[-1]
        assert [b[0] for b in minutes] == list(range(begin - MINUTE, cut, MINUTE))
        assert all(b[6] + 1 == b[0] + MINUTE and b[6] + 1 <= cut and 0 < D(b[3]) <= D(b[4]) <= D(b[2]) and D(b[3]) <= D(b[1]) <= D(b[2]) and D(b[7]) >= 0 for b in minutes)
        assert all(b[6] + 1 == b[0] + DAY and b[6] + 1 <= cut // DAY * DAY for b in daily)
        assert [b[0] for b in daily] == list(range(daily[0][0], cut // DAY * DAY, DAY))
        indexed = {b[0]: b for b in daily}
        overlap = [b for b in earlier_daily[asset]['1d'] if b[0] in indexed]
        assert len(overlap) >= 64 and all(indexed[b[0]] == b for b in overlap)
        minute_map = {b[0]: b for b in minutes}
        for d in daily:
            if d[0] + DAY - MINUTE in minute_map:
                assert D(d[4]) == D(minute_map[d[0] + DAY - MINUTE][4])
            if d[0] >= begin and d[0] + DAY <= cut:
                part = [minute_map[t] for t in range(d[0], d[0] + DAY, MINUTE)]
                assert abs(sum(D(b[7]) for b in part) - D(d[7])) <= D('.001')

def capture():
    plan = json.loads((R / 'forward_resume_plan.json').read_text())
    state = json.loads((ROOT / plan['source_state']).read_text())
    ledger = reg.read_records(ROOT / 'research/automation/registry.jsonl')
    assert all(ledger[b['fingerprint']]['status'] == 'reserved' for b in json.loads((R / 'forward_batch.json').read_text()))
    begin, cut = ms(plan['resume_utc']), ms(plan['cutoff_utc'])
    first_day = ms(state['next_daily_decision_utc']) - MINUTE
    inputs, provenance = {}, []
    cache = json.loads((R / 'forward_provenance.json').read_text()) if (R / 'forward_provenance.json').exists() else []
    for asset in ('BTC', 'ETH'):
        inputs[asset] = {}
        for interval, start, end, step in [('1m', begin - MINUTE, cut, MINUTE), ('1d', first_day - 65 * DAY, cut // DAY * DAY, DAY)]:
            cursor, page, bars = start, 0, []
            while cursor < end:
                stop = min(end, cursor + 900 * step)
                url = 'https://data-api.binance.vision/api/v3/klines?' + urllib.parse.urlencode({'symbol': asset + 'USDT', 'interval': interval, 'startTime': cursor, 'endTime': stop - 1, 'limit': 1000})
                path = R / f'forward_response_{asset}_{interval}_{page}.json.gz'
                prior = next((p for p in cache if p['url'] == url), None)
                if prior:
                    raw = gzip.decompress(path.read_bytes()); status = prior['status']
                    assert sha(path) == prior['raw_gzip_sha256'] and __import__('hashlib').sha256(raw).hexdigest() == prior['raw_response_sha256']
                    provenance.append(prior)
                else:
                    response = subprocess.run(['curl','--fail','--silent','--show-error','--retry','2','--retry-all-errors','--max-time','20','--write-out','\n%{http_code}',url],capture_output=True,timeout=65)
                    if response.stderr: sys.stderr.buffer.write(response.stderr); sys.stderr.flush()
                    response.check_returncode()
                    raw, status_bytes = response.stdout.rsplit(b'\n',1); status = int(status_bytes)
                    path.write_bytes(gzip.compress(raw, mtime=0))
                    provenance.append({'asset': asset, 'interval': interval, 'page': page, 'url': url, 'status': status, 'retrieved_utc': now(), 'raw_response_sha256': __import__('hashlib').sha256(raw).hexdigest(), 'raw_gzip_path': rel(path), 'raw_gzip_sha256': sha(path), 'bars': len(json.loads(raw)), 'timestamp_unit': 'milliseconds', 'delayed_shadow_reconstruction': True})
                    put(R / 'forward_provenance.json', provenance)
                rows = json.loads(raw)
                assert status == 200 and rows and rows[0][0] == cursor and rows[-1][6] + 1 == stop
                bars.extend(rows); cursor = stop; page += 1
            inputs[asset][interval] = bars
            print('CAPTURED', asset, interval, len(bars), flush=True)
    (R / 'forward_inputs.json.gz').write_bytes(gzip.compress(json.dumps(inputs, separators=(',', ':'), allow_nan=False).encode(), mtime=0))
    validate(plan, inputs)
    print('VALIDATED_REAL_OVERLAPS_AND_CLOSED_DATA', flush=True)

def simulate():
    plan = json.loads((R / 'forward_resume_plan.json').read_text())
    inputs = readgz(R / 'forward_inputs.json.gz'); validate(plan, inputs)
    old = json.loads((ROOT / plan['source_report']).read_text())
    state = json.loads((ROOT / plan['source_state']).read_text())
    begin, cut = ms(plan['resume_utc']), ms(plan['cutoff_utc'])
    events = list(range(ms(state['next_daily_decision_utc']), cut, DAY))
    newminutes = (cut - begin) // MINUTE
    oldpoints = len(old['configs']['forward_snapshot_combo']['scenes']['1']['equity_usdt'])
    elapsed = old['configs']['forward_snapshot_combo']['scenes']['1']['elapsed_minutes'] + newminutes
    totalpoints = oldpoints + newminutes + len(events)
    batch = json.loads((R / 'forward_batch.json').read_text())
    configs, decisions, positions = {}, {}, {}
    for b in batch[:2]:
        asset = b['asset']; minutes, daily = inputs[asset]['1m'], inputs[asset]['1d']
        minute_map = {z[0]: z for z in minutes}
        desired = state['positions_by_asset_and_cost'][asset]['1']['desired_long']
        assert all(p['desired_long'] == desired for p in state['positions_by_asset_and_cost'][asset].values())
        schedule = {}
        for event in events:
            history = [d for d in daily if d[6] + 1 <= event - MINUTE][-65:]
            assert len(history) == 65 and history[-1][6] + 1 == event - MINUTE
            closes = [D(d[4]) for d in history]; sma = sum(closes) / 65
            before = desired; desired, action = LEGACY.sig.step(desired, closes[-1], sma, D('.01'))
            rows = [{'close': d[4], 'quote_volume': d[7], 'close_available_ts': (d[6] + 1) * 1000000} for d in history]
            adv, sigma = LEGACY.engine.lagged_cost_inputs(rows, 65)
            schedule[event] = {'executed_at_utc': iso(event), 'prior_close': str(closes[-1]), 'SMA65': str(sma), 'before_desired_long': before, 'desired_long': desired, 'action': action, 'last_daily_close_available_utc': iso(history[-1][6] + 1), 'daily_bars': 65, 'lagged_daily_quote_ADV': adv, 'lagged_daily_volatility': sigma, 'reference_minute_open': float(minute_map[event][1])}
        decisions[asset] = list(schedule.values()); cfg = copy.deepcopy(old['configs'][b['name']]); cfg.update(b)
        cfg['latest_daily_decision'] = decisions[asset][-1]; positions[asset] = {}
        for k, s in cfg['scenes'].items():
            pos = state['positions_by_asset_and_cost'][asset][k]
            cash, units, want = pos['cash_usdt'], pos['units'], pos['desired_long']
            assert s['cash_usdt'] == cash and s['units'] == units and s['desired_long'] == want
            assert s['equity_usdt'][-1] == cash + units * float(minutes[0][4])
            previous = s['equity_usdt'][-1]; newtrades = []
            for z in minutes[1:]:
                if z[0] in schedule:
                    d = schedule[z[0]]; want = d['desired_long']; ref = float(z[1])
                    buy, sell = want and units == 0, not want and units > 0
                    if buy or sell:
                        budget = cash if buy else units * ref; adv, sigma = d['lagged_daily_quote_ADV'], d['lagged_daily_volatility']; mult = int(k)
                        assert 0 <= budget / adv <= .001
                        fee, spread, slip = .001 * mult, .0001 * mult, .0002 * mult
                        impact = .5 * sigma * math.sqrt(budget / adv) * mult
                        execution = ref * (1 + (spread + slip + impact) * (1 if buy else -1))
                        quantity = cash / (execution * (1 + fee)) if buy else units
                        before_wealth = cash + units * ref
                        if buy: cost = cash - quantity * ref; cash, units = 0., quantity
                        else: cash = quantity * execution * (1 - fee); cost = quantity * ref - cash; units = 0.
                        assert math.isclose(before_wealth - cash - units * ref, cost, abs_tol=1e-9)
                        newtrades.append({'side': 'buy' if buy else 'sell', 'reference': ref, 'execution': execution, 'quantity': quantity, 'fee_rate': fee, 'half_spread_rate': spread, 'slippage_rate': slip, 'impact_rate': impact, 'lagged_daily_quote_ADV': adv, 'lagged_daily_volatility': sigma, 'participation': budget / adv, 'cost_usdt': cost, 'executed_at_utc': iso(z[0]), 'cash_after': cash, 'units_after': units})
                    s['equity_usdt'].append(cash + units * ref)
                s['equity_usdt'].append(cash + units * float(z[4])); assert cash >= 0 and units >= 0
            s['trades'] += newtrades; s['cost_usdt'] += sum(t['cost_usdt'] for t in newtrades)
            s.update(cash_usdt=cash, units=units, desired_long=want, executions=s['executions'] + len(newtrades), round_trips=s['round_trips'] + sum(t['side'] == 'sell' for t in newtrades), cost_pct_initial=s['cost_usdt'] / b['capital_usdt'] * 100, net_return_pct=100 * (s['equity_usdt'][-1] / b['capital_usdt'] - 1), max_drawdown_pct=LEGACY.dd(s['equity_usdt']), elapsed_minutes=elapsed, elapsed_complete_days=elapsed // 1440, new_mark_minutes=newminutes, new_reference_points=len(events), new_executions=len(newtrades), since_previous_mark_return_pct=100 * (s['equity_usdt'][-1] / previous - 1))
            assert len(s['equity_usdt']) == totalpoints and s['equity_usdt'][:oldpoints] == old['configs'][b['name']]['scenes'][k]['equity_usdt']
            positions[asset][k] = {'cash_usdt': cash, 'units': units, 'desired_long': want}
        cfg.update(status='rejected', reason=f'Partial delayed shadow: {elapsed // 1440} complete days; 180-day/sixfold qualification not mature; original frozen plan continues.')
        configs[b['name']] = cfg
    b = batch[-1]; cfg = copy.deepcopy(old['configs'][b['name']]); cfg.update(b)
    for k, s in cfg['scenes'].items():
        a, e = configs['forward_snapshot_BTC']['scenes'][k], configs['forward_snapshot_ETH']['scenes'][k]
        values = [x + y for x, y in zip(a['equity_usdt'], e['equity_usdt'])]
        assert values[:oldpoints] == s['equity_usdt']
        previous = s['equity_usdt'][-1]
        s.update(equity_usdt=values, net_return_pct=100 * (values[-1] / 2000 - 1), max_drawdown_pct=LEGACY.dd(values), cost_usdt=a['cost_usdt'] + e['cost_usdt'], cost_pct_initial=(a['cost_usdt'] + e['cost_usdt']) / 20, executions=a['executions'] + e['executions'], round_trips=a['round_trips'] + e['round_trips'], component_states={a: {'cash': positions[a][k]['cash_usdt'], 'units': positions[a][k]['units']} for a in ('BTC', 'ETH')}, elapsed_minutes=elapsed, elapsed_complete_days=elapsed // 1440, new_mark_minutes=newminutes, new_reference_points=len(events), new_executions=a['new_executions'] + e['new_executions'], since_previous_mark_return_pct=100 * (values[-1] / previous - 1))
    cfg.update(status='rejected', reason=f'Actual {elapsed // 1440}-day partial delayed shadow; not a failed or cancelled long-term frozen plan.')
    configs[b['name']] = cfg
    refs = [{'open_ts_ms': event, 'NAV_index': oldpoints + (event - begin) // MINUTE + i} for i, event in enumerate(events)]
    report = {'observation_started_utc': json.loads((R / 'forward_provenance.json').read_text())[0]['retrieved_utc'], 'frozen_plan_path': old['frozen_plan_path'], 'frozen_plan_sha256': old['frozen_plan_sha256'], 'start_utc': old['start_utc'], 'resume_utc': plan['resume_utc'], 'cutoff_utc': plan['cutoff_utc'], 'source_report': plan['source_report'], 'source_report_sha256': plan['report_sha256'], 'source_state': plan['source_state'], 'source_state_sha256': plan['state_sha256'], 'input_sha256': sha(R / 'forward_inputs.json.gz'), 'source_inputs_path': rel(R / 'forward_inputs.json.gz'), 'provenance': json.loads((R / 'forward_provenance.json').read_text()), 'append_axis': {'encoding': 'Closed-minute open timestamps in range(start, stop, step), each marked at open+60000; insert each daily post-trade reference immediately before that minute-close mark.', 'closed_minute_open_ms_range': [begin, cut, MINUTE], 'daily_execution_references': refs, 'old_NAV_points_preserved': oldpoints, 'new_NAV_points_per_scene': newminutes + len(events)}, 'daily_decisions_by_asset': decisions, 'configs': configs, 'validation': {'walk_forward': f'{elapsed // 1440} complete days only; no mature 180-day/sixfold result.', 'sensitivity': 'Frozen SMA65, symmetric1%, raw75/25 unchanged; no new parameter search.', 'costs': 'Original floating-quantity 1/2/3x fee/spread/slippage/lagged20-day quote-ADV impact preserved, no retrofit tick/lot rounding or forced exit.', 'continuity': f'{oldpoints} NAV points remain an exact prefix; append {newminutes} closed minutes and {len(events)} daily references per scene, without cash restart.', 'interpretation': 'Delayed historical shadow reconstruction, not live execution or paper10 real-quote performance.'}, 'source_hashes': {rel(p): sha(p) for p in [Path(__file__), ROOT / 'research/experiments/20261011T014626Z/forward.py', ROOT / 'research/experiments/20261001T113625Z/signals.py', ROOT / 'research/experiments/20261001T013355Z/evaluate.py']}}
    nextstate = copy.deepcopy(state)
    nextstate.update(source_report=rel(R / 'forward_report.json'), last_completed_mark_utc=plan['cutoff_utc'], next_daily_decision_utc=iso(events[-1] + DAY), positions_by_asset_and_cost=positions, previous_state=plan['source_state'], previous_state_sha256=plan['state_sha256'], next_round='Continue the exact floating-quantity SMA65/1%75:25 account; reserve any new cutoff first; preserve all costs, trades and NAV prefix. Delayed shadow remains separate from paper10. No terminal close before the frozen2027-03-31 plan.')
    return report, nextstate

def evaluate():
    assert not (R / 'forward_report.json').exists(), 'Use verify for existing actual results.'
    ledger = reg.read_records(ROOT / 'research/automation/registry.jsonl')
    assert all(ledger[b['fingerprint']]['status'] == 'reserved' for b in json.loads((R / 'forward_batch.json').read_text()))
    report, state = simulate()
    (R / 'forward_report.json').write_text(json.dumps(report, ensure_ascii=False, separators=(',', ':'), allow_nan=False) + '\n')
    state['source_report_sha256'] = sha(R / 'forward_report.json'); put(R / 'forward_state.json', state)
    print(json.dumps({'cutoff_utc': report['cutoff_utc'], 'daily_decisions_per_asset': len(report['daily_decisions_by_asset']['BTC']), 'combo_return_pct': {k: s['net_return_pct'] for k, s in report['configs']['forward_snapshot_combo']['scenes'].items()}}), flush=True)

def verify():
    report, state = simulate()
    assert report == json.loads((R / 'forward_report.json').read_text())
    state['source_report_sha256'] = sha(R / 'forward_report.json')
    assert state == json.loads((R / 'forward_state.json').read_text())
    inputs = readgz(R / 'forward_inputs.json.gz'); all_raw = {}
    for p in report['provenance']:
        path = ROOT / p['raw_gzip_path']; raw = gzip.decompress(path.read_bytes())
        assert sha(path) == p['raw_gzip_sha256'] and __import__('hashlib').sha256(raw).hexdigest() == p['raw_response_sha256']
        assert ms(p['retrieved_utc']) > ms(report['cutoff_utc'])
        all_raw.setdefault((p['asset'], p['interval']), []).extend(json.loads(raw))
    for (asset, interval), bars in all_raw.items(): assert bars == inputs[asset][interval]
    for a, decisions in report['daily_decisions_by_asset'].items():
        for d in decisions:
            close, sma = D(d['prior_close']), D(d['SMA65']); prior = d['before_desired_long']
            wanted = False if prior and close < sma * D('.99') else True if not prior and close > sma * D('1.01') else prior
            assert wanted == d['desired_long'] and ms(d['executed_at_utc']) - ms(d['last_daily_close_available_utc']) == MINUTE
    result = {'passed': True, 'report_sha256': sha(R / 'forward_report.json'), 'scenes': 9, 'closed_minutes_added_per_asset': report['append_axis']['closed_minute_open_ms_range'], 'daily_decisions_per_asset': len(report['daily_decisions_by_asset']['BTC']), 'raw_response_pages_verified': len(report['provenance']), 'original_NAV_prefix_and_cash_quantity_cost_trade_continuity_verified': True, 'frozen_plan_unchanged': True, 'paper10_unchanged': True, 'new_virtual_component_orders_all_costs': sum(s['new_executions'] for c in report['configs'].values() if c.get('asset') in ('BTC', 'ETH') for s in c['scenes'].values())}
    baseline = json.loads((R / 'context.json').read_text())['account_hashes_before']
    assert all(sha(ROOT / p) == h for p, h in baseline.items())
    print(json.dumps(result), flush=True); return result

def finish():
    verify()
    assert json.loads((R/'forward_verification.json').read_text())['passed'] is True
    done = []
    for row in json.loads((R / 'forward_batch.json').read_text()):
        done.append(call('finish', row, 'rejected', rel(R / 'forward_report.json'))); put(R / 'forward_finish.json', done)

if __name__ == '__main__':
    if '--reproduce' in sys.argv:verify()
    elif len(sys.argv)==1:capture();evaluate()
    else:
        parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=('reserve','capture','evaluate','verify','finish'));globals()[parser.parse_args().command]()
