"""Check published-rate visibility and unsunk B1 gates against actual saved decisions."""
import bisect,json,math,statistics
from run import R,ROOT,c,datasets,readgz,sha,put

def main():
    report=json.loads((R/'report.json').read_text());data=datasets();checks=0;visibility_checks=0;early=0
    for cfg in report['configs'].values():
        d=data[cfg['asset']];rows={r['ts']:r for r in d['rows']};events=sorted(d['events'],key=lambda e:e['available']);available=[e['available'] for e in events]
        path=ROOT/cfg['full_result_path'];assert sha(path)==cfg['full_result_sha256'];saved=readgz(path);hours=cfg['holding_hours'];buffer=1
        for full in saved['costs'].values():
            scene=full['hourly_engine_output'];groups={}
            for trade in scene['trades']:groups.setdefault(trade['ts'],[]).append(trade)
            q=0.;expiry=None;seen=set()
            for decision in scene['decisions']:
                t=decision['ts'];row=rows[t];n=bisect.bisect_right(available,t);visible=events[n-21:n] if n>=21 else []
                rate=statistics.median(e['rate']/e['hours'] for e in visible) if visible else None
                assert decision['hourly_rate']==rate
                assert all(e['available']<=t for e in visible) and (n==len(events) or events[n]['available']>t)
                visibility_checks+=len(visible);held=q>0;qty=q if held else decision['target_quantity'];prices=[float(row['close']),float(row['close_perp'])]
                rates=[]
                for j,px in enumerate(prices):
                    adv,sigma=d['costs'][j][t//c.DAY];part=qty*px/adv;assert 0<=part<=.001
                    rates.append((.001 if j==0 else .0005)+.0001+.0002+.5*sigma*math.sqrt(part))
                cost=qty*(prices[0]*rates[0]+prices[1]*rates[1]);remaining=(expiry-t)/c.HOUR if held else hours
                if held:assert decision['remaining_hours']==max(0,remaining)
                else:
                    assert decision['known_spot']==prices[0] and decision['known_perp']==prices[1]
                    assert math.isclose(decision['estimated_roundtrip_cost_usdt'],2*cost,rel_tol=1e-12,abs_tol=1e-9)
                eligible=rate is not None and qty*prices[1]*rate*remaining-cost*(1 if held else 2)>buffer
                expected=('exit' if t>=expiry or (rate is not None and not eligible) else 'hold') if held else ('enter' if eligible else 'skip')
                if not held and qty*min(prices)<max(d['meta']['spot_min'],d['meta']['perp_min']):expected='below_min_notional'
                actual=decision['action'];assert actual==expected or (expected=='enter' and actual=='spot_cash_rejected'),(cfg['name'],t,actual,expected)
                trades=groups.get(t+c.MINUTE,[])
                if actual in ('enter','exit'):
                    assert len(trades)==2 and [x['leg'] for x in trades]==['spot','perp']
                    assert all(x['quantity']==qty for x in trades)
                    reason='entry' if actual=='enter' else 'fixed_expiry' if t>=expiry else 'remaining_funding_exit'
                    assert all(x['reason']==reason for x in trades);seen.add(t+c.MINUTE)
                    early+=reason=='remaining_funding_exit'
                    if actual=='enter':q=qty;expiry=t+hours*c.HOUR
                    else:q=0.;expiry=None
                else:assert not trades
                checks+=1
            for t,trades in groups.items():
                if t not in seen:
                    assert t==c.ns(report['time_boundaries']['oos_end_exclusive_utc']) and q>0
                    assert len(trades)==2 and all(x['reason']=='terminal_exit' and x['quantity']==q for x in trades);q=0.
            assert q==0
    out={'passed':True,'cost_scenes':54,'decisions_checked':checks,'published_funding_observations_checked':visibility_checks,'remaining_funding_early_exits_all_costs':early,'median_uses_available_not_settlement_and_actual_intervals':True,'base1x_entry_and_only_future_exit_cost_gates_checked':True,'actual_trade_reasons_and_fixed_expiry_verified':True,'report_sha256':sha(R/'report.json')}
    put(R/'b1_signal_verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
