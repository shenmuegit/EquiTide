import copy,math,statistics
from decimal import Decimal as D,ROUND_CEILING,ROUND_FLOOR
import numpy as np
from common import *
from audit_helpers_complete import near,metrics,independent_margin,verify_recent

def native(leg,mm,m,k,ff,spec,counters):
 state={q:D(v) for q,v in {'cash':'10000','signed_units':'0','entry_price':'0','entry_reference':'0'}.items()};start=0;segstart=0;segstate=copy.deepcopy(state);segments=[];v=np.empty(len(m['ts']));trades=leg['trades'];funds=leg['funding_events'];source=mm['funds'];assert len(funds)==len(source)==1110
 for t,e in zip(funds,source):assert t['settlement_ts_ns']==e['settlement_ts'] and t['source_index']==e['source_index'] and t['available_ts_ns']==e['available_ts']
 events=sorted([(x['axis_index'],0,i,'fund',x) for i,x in enumerate(funds)]+[(x['axis_index'],1,i,'trade',x) for i,x in enumerate(trades)])
 for idx,_,_,kind,t in events:
  before=copy.deepcopy(state);v[start:idx]=float(state['cash'])+float(state['signed_units'])*(mm['axis_prices'][start:idx]-float(state['entry_price']));now_ns=int(m['ts'][idx]);code=int(m['codes'][idx])
  if kind=='fund':
   e=mm['fund_lookup'][now_ns];q=state['signed_units'];base=-q*e['mark_price_at_settlement']*e['realized_rate'];amount=base*k if base<0 else base;assert code==4 and D(t['realized_rate'])==e['realized_rate'] and D(t['mark_price'])==e['mark_price_at_settlement'] and D(t['signed_units'])==q and D(t['base_amount_usdt'])==base and D(t['amount_usdt'])==amount and D(t['cash_before'])==state['cash']
   if amount:state['cash']+=amount
   assert D(t['cash_after'])==state['cash'];counters['funding']+=1
  else:
   assert code in [6,7,9] and t['trade_ts_ns']==now_ns and {q:D(z) for q,z in t['state_before'].items()}==state
   h=(now_ns-m['first_ns']-MIN)//HOUR;day=h//24;ref=mm['frame']['open'][h*60+1];change=D(t['change_signed_units']);qty=abs(change);opening=t['opening'];cash,q,entry,er=[state[a] for a in ['cash','signed_units','entry_price','entry_reference']];adv=D(str(statistics.mean(float(x['quote_volume']) for x in mm['rows'][day-20:day])));rr=[math.log(float(mm['closes'][j])/float(mm['closes'][j-1])) for j in range(day-20,day)];sig=D(str(statistics.stdev(rr)));part=qty*ref/adv;lot=D(mm['meta']['lot_size']);tick=D(mm['meta']['tick_size']);fee=D('.0005')*k;spread=D('.0001')*k;slip=D('.0002')*k;impact=D('.5')*sig*part.sqrt()*k;theory=ref*(1+(spread+slip+impact)*(1 if change>0 else -1));px=(theory/tick).to_integral_value(rounding=ROUND_CEILING if change>0 else ROUND_FLOOR)*tick;parts={'fee':qty*px*fee,'half_spread':qty*ref*spread,'slippage':qty*ref*slip,'impact':qty*ref*impact,'tick_rounding':qty*abs(px-theory)}
   assert t['cost_multiplier']==k and qty>0 and D(t['reference'])==ref and D(t['lagged_ADV'])==adv and D(t['lagged_sigma'])==sig and D(t['participation'])==part and D(t['quantity'])==qty
   reason='participation' if part>D('.001') else 'lot_or_min_notional' if qty%lot or qty*px<D(mm['meta']['min_notional']) else 'fully_collateralized_1x_entry_cap' if opening and qty*px>cash-parts['fee'] else None
   if reason:assert t['status']=='rejected' and t['reason']==reason and {a:D(z) for a,z in t['state_after'].items()}==state;counters['rejects']+=1
   else:
    assert t['status']=='filled' and D(t['execution'])==px and D(t['theoretical_execution'])==theory and all(D(t['cost_parts'][a])==x for a,x in parts.items()) and D(t['cost_usdt'])==sum(parts.values())
    if opening:assert q==0;state={'cash':cash-parts['fee'],'signed_units':change,'entry_price':px,'entry_reference':ref};realized=rpnl=D(0)
    else:assert change==-q;realized=q*(px-entry);rpnl=q*(ref-er);state={'cash':cash+realized-parts['fee'],'signed_units':D(0),'entry_price':D(0),'entry_reference':D(0)}
    assert D(t['realized_price_PnL_usdt'])==realized and D(t['reference_price_PnL_usdt'])==rpnl and {a:D(z) for a,z in t['state_after'].items()}==state
    assert abs(cash+q*(ref-entry)-(state['cash']+state['signed_units']*(ref-state['entry_price']))-sum(parts.values()))<D('1e-18');counters['fills']+=1
  if before!=state:
   if idx>segstart:segments.append({'axis_start':segstart,'axis_end_exclusive':idx,**segstate})
   segstart=idx;segstate=copy.deepcopy(state)
  start=idx
 v[start:]=float(state['cash'])+float(state['signed_units'])*(mm['axis_prices'][start:]-float(state['entry_price']));segments.append({'axis_start':segstart,'axis_end_exclusive':len(v),**segstate});saved=[{a:(z if a in ['axis_start','axis_end_exclusive'] else D(z)) for a,z in s.items()} for s in leg['state_segments']];assert saved==segments and {a:D(z) for a,z in leg['terminal_state'].items()}==state
 z=leg['summary'];assert z['NAV_sha256_f64le']==core.navhash(v) and z['NAV_points']==len(v) and z['daily_equity_usdt']==v[m['daily_indices']].tolist();daily=z['daily_equity_usdt'];metrics(v,daily,370,z);counters['metric_checks']+=1
 for j,(a,b) in enumerate(zip(m['fold_indices'],m['fold_indices'][1:])):metrics(v[a:b+1],daily[30*j:min(30*j+30,370)+1],min(30,370-30*j),z['folds'][j]);counters['metric_checks']+=1
 filled=[t for t in trades if t['status']=='filled'];gross=sum(D(t['reference_price_PnL_usdt']) for t in filled)+state['signed_units']*(mm['terminal_reference_decimal']-state['entry_reference']);fund=sum(D(t['amount_usdt']) for t in funds);cost=sum(D(t['cost_usdt']) for t in filled);near(gross,z['gross_reference_price_PnL_usdt']);near(fund,z['funding_usdt']);near(cost,z['cost_usdt']);near(gross+fund-cost,v[-1]-10000);assert z['executions']==len(filled) and z['round_trips']==sum(not t['opening'] for t in filled)
 minimum,count,viol=independent_margin(mm,leg['state_segments']);assert z['margin']['state_hour_extreme_bounding_checks']==count and z['margin']['violations']==viol
 if count:near(minimum,z['margin']['minimum_equity_minus_maintenance_usdt'],1e-9)
 counters['margin_checks']+=count;return v
