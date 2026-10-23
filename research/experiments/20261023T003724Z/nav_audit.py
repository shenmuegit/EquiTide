"""Independent cash-flow reconstruction and continuous traded-price minute NAV."""
import hashlib, math
from collections import defaultdict
import numpy as np

MINUTE = 60 * 10**9

def augment(data, scene, start, end, multiplier, benchmark=False):
    frames = data['frames']
    ts = frames['spot_bars']['open_ts'].to_numpy()
    spot = frames['spot_bars']['close'].cast(__import__('polars').Float64).to_numpy()
    perp = frames['perp_bars']['close'].cast(__import__('polars').Float64).to_numpy()
    a = int((start-ts[0])//MINUTE); b = int((end-ts[0])//MINUTE)
    assert ts[a] == start and ts[b] == end and np.isfinite(spot).all() and np.isfinite(perp).all()
    groups = defaultdict(list)
    for x in scene.get('funding_events', []): groups[x['ts']].append(('funding', x))
    for x in scene['trades']: groups[x['ts']].append(('trade', x))
    cash, qs, qp, spot_cash, perp_cash, entry = 10000., 0., 0., 5000., 5000., 0.
    cursor, peak, loss, samples = a, 10000., 0., 0
    digest = hashlib.sha256(); hourly_checks = 0; violations = []
    hourly = {t+MINUTE: i+1 for i,t in enumerate(scene['equity_signal_times'])}
    row_by = {r['ts']: r for r in data['rows']}
    source_funding = {x['ts']: x for x in data['events']}

    def marks(values):
        nonlocal peak, loss, samples
        values = np.asarray(values, dtype='<f8')
        if not len(values): return
        assert np.isfinite(values).all() and np.all(values>0)
        peaks = np.maximum.accumulate(np.r_[peak, values])[1:]
        loss = max(loss, float(np.max(1-values/peaks)))
        peak = float(peaks[-1]); samples += len(values); digest.update(values.tobytes())

    def risk(t, stage):
        if benchmark: return
        hour = (t//(60*MINUTE))*(60*MINUTE)
        if qp and hour in data['marks']:
            if hour+60*MINUTE <= end:
                high = float(data['marks'][hour]['high']); envelope='hour_mark'
            else:
                # Terminal gap has no complete in-window hourly mark; never use post-OOS highs.
                k=min(int((t-ts[0])//MINUTE),b-1)
                high=float(frames['perp_bars']['high'][k]);envelope='closed_minute_traded_price_proxy'
            margin = perp_cash+(-qp)*(entry-high)
            if margin <= .01*(-qp)*high:
                violations.append({'ts':t,'stage':stage,'kind':'conservative_margin_envelope','envelope':envelope,'equity':margin,'maintenance':.01*(-qp)*high})
        if spot_cash < -1e-6 or perp_cash < -1e-6:
            violations.append({'ts':t,'stage':stage,'kind':'isolated_negative_cash','spot_cash':spot_cash,'perp_cash':perp_cash})

    marks([10000.])
    for t in sorted(groups):
        assert start <= t <= end
        i = int((t-ts[0])//MINUTE)
        assert cursor <= i <= b
        marks(cash+qs*spot[cursor:i]+qp*perp[cursor:i]); cursor = i
        risk(t, 'old_position_before_events')
        for kind,x in sorted(groups[t], key=lambda z: 0 if z[0]=='funding' else 1):
            if kind == 'funding':
                source = source_funding[t]
                assert all(source[k]==x[k] for k in ('ts','available','rate','mark','hours'))
                assert math.isclose(-qp,x['quantity'],abs_tol=1e-8)
                raw = -qp*x['mark']*x['rate']; amount = raw if raw>=0 else raw*multiplier
                assert abs(raw-x['base_amount_usdt'])<1e-7 and abs(amount-x['amount_usdt'])<1e-7
                cash += amount; perp_cash += amount
            else:
                leg = x.get('leg','spot')
                change = (x['quantity'] if benchmark else x['quantity']*(1 if x['side']=='buy' else -1))
                cash -= change*x['execution']+x.get('fee_usdt',x.get('fee',0))
                fee = x.get('fee_usdt',x.get('fee',0))
                assert x['participation']<=.001
                if leg == 'spot':
                    qs += change; spot_cash -= change*x['execution']+fee
                else:
                    if change<0: assert abs(qp)<1e-8; entry=x['execution']
                    else: perp_cash += (-qp)*(entry-x['execution'])
                    qp += change; perp_cash -= fee
        if not benchmark: assert abs(qs+qp)<1e-8
        risk(t, 'after_events')
        if any(kind=='trade' for kind,_ in groups[t]):
            oi = int((t-ts[0])//MINUTE)
            sr=float(frames['spot_bars']['open'][oi]); pr=float(frames['perp_bars']['open'][oi])
            marks([cash+qs*sr+qp*pr])
    marks(cash+qs*spot[cursor:b]+qp*perp[cursor:b])
    assert abs(qs)<1e-8 and abs(qp)<1e-8 and abs(cash-scene['final_NAV'])<1e-6
    # A second event walk reconciles every original hourly reference NAV.
    cash, qs, qp = 10000., 0., 0.; ordered = sorted(groups); j=0
    for t in scene['equity_signal_times']:
        while j<len(ordered) and ordered[j]<=t+MINUTE:
            for kind,x in sorted(groups[ordered[j]], key=lambda z: 0 if z[0]=='funding' else 1):
                if kind=='funding': cash+=x['amount_usdt']
                else:
                    change=x['quantity'] if benchmark else x['quantity']*(1 if x['side']=='buy' else -1)
                    cash-=change*x['execution']+x.get('fee_usdt',x.get('fee',0))
                    if x.get('leg','spot')=='spot':qs+=change
                    else:qp+=change
            j+=1
        row=row_by[t];value=cash+qs*float(row['fill'])+qp*float(row['fill_perp'])
        assert abs(value-scene['equity'][hourly[t+MINUTE]])<1e-6
        hourly_checks+=1
    return {'max_drawdown_1m_sampled_pct':loss*100,'minute_nav_sha256_f64le':digest.hexdigest(),
            'minute_nav_samples':samples,'minute_close_samples':b-a,'hourly_NAV_reconciled':hourly_checks,
            'independent_cash_margin_violations':violations,'terminal_spot_cash_usdt':spot_cash,
            'terminal_perp_collateral_usdt':perp_cash,'terminal_flat':abs(qs)<1e-8 and abs(qp)<1e-8,
            'scope':'Initial capital, all closed-minute spot/perp traded-price NAVs and atomic post-fill reference NAVs; no minute mark-price series or intraminute extrema. Cash-credit short reconstruction is for reconciliation only, not spendable collateral.'}
