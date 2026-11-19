"""Capture actual closed SPOT context, before any reservation or account calculation."""
import gzip, hashlib, json, subprocess, urllib.parse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
R = Path(__file__).resolve().parent
P = ROOT / 'research/experiments/20261119T123454Z'
rd = lambda p: json.loads(p.read_text())
gz = lambda p: json.loads(gzip.decompress(p.read_bytes()))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
now = lambda: datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
ms = lambda s: int(datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp() * 1000)
put = lambda p, x: p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n')
assert not (R / 'sma65_prebinding_manifest.json').exists()
assert not (R / 'forward_resume_plan.json').exists()
state = rd(P / 'forward_state.json')
old = rd(P / 'forward_report.json')
assert state['source_report_sha256'] == sha(P / 'forward_report.json')
h = rd(P / 'next_research_state.json')['UTC_midnight_handoff']
authority = ROOT / h['SMA_full71_authority']
assert sha(authority) == h['SMA_full71_sha256']
earlier = gz(authority)
previous = gz(ROOT / old['source_inputs_path'])
begin, cut = map(ms, [state['last_completed_mark_utc'], h['next_SMA_single_window_utc'][1]])
assert cut - begin == 120 * 60000 and begin < ms(state['next_daily_decision_utc']) < cut
assert ms(now()) > cut
rawdir = R / 'sma65_prebinding_raw'
rawdir.mkdir(exist_ok=False)
receipts, provenance, inputs = [], [], {}
for asset in ['BTC', 'ETH']:
    assert len(earlier[asset]['1d']) == 70
    inputs[asset] = {}
    for interval in ['1d', '1m']:
        lo = earlier[asset]['1d'][0][0] if interval == '1d' else begin - 60000
        end = cut // 86400000 * 86400000 - 1 if interval == '1d' else cut - 1
        params = {'symbol': asset + 'USDT', 'interval': interval, 'startTime': lo, 'endTime': end, 'limit': 1000}
        url = 'https://api.binance.com/api/v3/klines?' + urllib.parse.urlencode(params)
        for attempt in range(1, 4):
            started = now()
            cmd = ['curl', '--ipv4', '--compressed', '--http1.1', '--tlsv1.2', '--silent', '--show-error', '--connect-timeout', '10', '--max-time', '30', '--write-out', '\n%{http_code}', url]
            z = subprocess.run(cmd, cwd=ROOT, capture_output=True, timeout=55)
            body, code = z.stdout.rsplit(b'\n', 1) if b'\n' in z.stdout else (z.stdout, b'000')
            path = rawdir / f'{asset}_{interval}_{attempt}.json.gz'
            path.write_bytes(gzip.compress(body, mtime=0))
            item = {'asset': asset, 'interval': interval, 'url': url, 'started_utc': started, 'retrieved_utc': now(), 'timestamp_unit': 'milliseconds', 'status': int(code), 'curl_exit_code': z.returncode, 'raw_gzip_path': str(path.relative_to(ROOT)), 'raw_gzip_sha256': sha(path), 'raw_response_sha256': hashlib.sha256(body).hexdigest(), 'bytes': len(body), 'stderr': z.stderr.decode(errors='replace')}
            receipts.append(item)
            put(R / 'sma65_prebinding_http_attempts.json', receipts)
            if z.returncode == 0 and int(code) == 200:
                bars = json.loads(body)
                assert isinstance(bars, list) and len(bars) < 1000
                inputs[asset][interval] = bars
                provenance.append(item)
                break
        else:
            raise RuntimeError('Three actual SPOT GET attempts failed; no account/model evaluated')
    daily, minute = inputs[asset]['1d'], inputs[asset]['1m']
    assert len(daily) == 71 and daily[:70] == earlier[asset]['1d']
    assert [b[0] for b in daily] == list(range(daily[0][0], cut // 86400000 * 86400000, 86400000))
    assert all(b[6] + 1 == b[0] + 86400000 <= cut // 86400000 * 86400000 for b in daily)
    assert len(minute) == 121 and [b[0] for b in minute] == list(range(begin - 60000, cut, 60000))
    prior = previous[asset]['1m'] if isinstance(previous[asset], dict) else previous[asset]
    assert minute[0] == prior[-1]
    assert all(b[6] + 1 == b[0] + 60000 <= cut for b in minute)
    assert daily[-1][4] == next(b[4] for b in minute if b[0] == daily[-1][6] + 1 - 60000)
dest = R / 'sma65_prebinding_inputs.json.gz'
dest.write_bytes(gzip.compress(json.dumps(inputs, sort_keys=True, separators=(',', ':'), allow_nan=False).encode(), mtime=0))
put(R / 'sma65_prebinding_manifest.json', {'passed': True, 'recorded_utc': now(), 'input_path': str(dest.relative_to(ROOT)), 'input_sha256': sha(dest), 'prior_state': str((P / 'forward_state.json').relative_to(ROOT)), 'prior_state_sha256': sha(P / 'forward_state.json'), 'prior_report': str((P / 'forward_report.json').relative_to(ROOT)), 'prior_report_sha256': sha(P / 'forward_report.json'), 'prior_daily_authority': str(authority.relative_to(ROOT)), 'prior_daily_authority_sha256': sha(authority), 'daily_context_days': 71, 'exact_previous_70_day_prefix': True, 'minute_bars_per_asset': 121, 'daily_decision_utc': state['next_daily_decision_utc'], 'provenance': provenance, 'native_HTTP_attempts': len(receipts), 'financial_or_account_calculations': 0, 'captured_before_forward_reservation': True, 'no_future_daily_context': True})
print(json.dumps({'captured': True, 'SPOT_days_per_asset': 71, 'exact_70_prefix': True, 'minute_bars_per_asset': 121, 'HTTP_attempts': len(receipts), 'financial_or_account_calculations': 0}), flush=True)
