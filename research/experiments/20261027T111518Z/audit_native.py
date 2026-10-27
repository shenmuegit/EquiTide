"""Independent integer signals, Decimal fills, funding, risk and every NAV point for54newETHslowgatepaths."""
import copy,gzip,hashlib,json,math,statistics
from decimal import Decimal as D,ROUND_CEILING,ROUND_FLOOR
from fractions import Fraction as F
import numpy as np
import engine
from run import ROOT,R,sha,reg,grid_configs
from audit_helpers import near,metrics,independent_margin,verify_recent,qualification

def verify(report,plan,markets,events,records):
 batch=[x for x in json.loads((R/'batch.json').read_text()) if x['scope']=='native'];assert len(batch)==6
 scenes=fills=funding_checks=decision_checks=metric_checks=margin_checks=recent_checks=0;vectors={}
 for row in batch:
  cfg=report['configs'][row['name']];arc=json.loads(gzip.decompress((ROOT/cfg['archive']).read_bytes()));spec=json.loads((ROOT/row['spec']).read_text());assert sha(ROOT/cfg['archive'])==cfg['archive_sha256'] and arc['spec']==spec and arc['fingerprint']==row['fingerprint']==reg.fingerprint(spec);reserved=[e for e in events if e['fingerprint']==row['fingerprint'] and e['status']=='reserved'];assert len(reserved)==1 and reserved[0]['recorded_at_utc']<report['evaluation_started_utc'];m=markets[row['asset']];p=spec['parameters'];assert p['fixed_entry_notional_usdt']==row['fixed_entry_notional_usdt'] and p['fixed_entry_notional_usdt'] in [1000,2000,3000] and p['raw_entry_notional_fraction_of_initial_capital']==p['fixed_entry_notional_usdt']/10000 and row['asset']=='ETH';assert p['lookback_days']==row['lookback_days'] and p['lookback_days'] in [3,4,5] and p['return_hurdle']==row['return_hurdle'] and p['exit_buffer_fraction']==0 and p['trend_lookback_days']==row['trend_lookback_days'] and p['trend_lookback_days'] in [22,25];f=m['frame'];native=m['closes'];prices=[int(x*D(10)**18) for x in native];meta=m['meta'];lot=D(meta['lot_size']);tick=D(meta['tick_size'])
  if records[row['fingerprint']]['status']!='reserved':assert records[row['fingerprint']]['report_sha256']==sha(R/'report.json')
  for k,s in arc['scenes'].items():
   mult=int(k);state={x:D(v) for x,v in {'cash':'10000','signed_units':'0','entry_price':'0','entry_reference':'0'}.items()};v=np.empty(len(m['ts']));start=0;ti=fi=di=0;expected_segments=[];segstart=0;segstate=copy.deepcopy(state);wanted=0
   def fill(idx,i,change,opening,terminal=False):
    nonlocal state,ti,fills
    t=s['trades'][ti];assert t['status']=='filled' and t['axis_index']==idx and t['decision_index']==i and t['trade_ts_ns']==int(m['ts'][idx]) and t['terminal']==terminal and t['opening']==opening and t['asset']==row['asset'];assert {x:D(y) for x,y in t['state_before'].items()}==state
    cash,q,entry,er=[state[x] for x in ['cash','signed_units','entry_price','entry_reference']];ref=f['open'][i*1440+1];qty=abs(change);adv=D(t['lagged_ADV']);sig=D(t['lagged_sigma']);part=qty*ref/adv;near(adv,statistics.mean(float(x['quote_volume']) for x in m['rows'][i-20:i]),1e-13);rr=[math.log(float(native[j])/float(native[j-1])) for j in range(i-20,i)];near(sig,statistics.stdev(rr),1e-13)
    assert D(t['change_signed_units'])==change and D(t['quantity'])==qty and D(t['reference'])==ref and D(t['participation'])==part<=D('.001') and qty%lot==0
    fee,spread,slip=D('.0005')*mult,D('.0001')*mult,D('.0002')*mult;impact=D('.5')*sig*part.sqrt()*mult;theory=ref*(1+(spread+slip+impact)*(1 if change>0 else -1));px=(theory/tick).to_integral_value(rounding=ROUND_CEILING if change>0 else ROUND_FLOOR)*tick;assert D(t['execution'])==px and px%tick==0 and qty*px>=D(meta['min_notional']);parts={'fee':qty*px*fee,'half_spread':qty*ref*spread,'slippage':qty*ref*slip,'impact':qty*ref*impact,'tick_rounding':qty*abs(px-theory)};assert all(D(t['cost_parts'][a])==b for a,b in parts.items()) and D(t['cost_usdt'])==sum(parts.values())
    if opening:assert q==0;new={'cash':cash-parts['fee'],'signed_units':change,'entry_price':px,'entry_reference':ref};realized=refpnl=D(0);assert qty*px<=new['cash']
    else:assert change==-q;realized=q*(px-entry);refpnl=q*(ref-er);new={'cash':cash+realized-parts['fee'],'signed_units':D(0),'entry_price':D(0),'entry_reference':D(0)}
    assert D(t['realized_price_PnL_usdt'])==realized and D(t['reference_price_PnL_usdt'])==refpnl and {x:D(y) for x,y in t['state_after'].items()}==new;assert abs(cash+q*(ref-entry)-(new['cash']+new['signed_units']*(ref-new['entry_price']))-sum(parts.values()))<D('1e-18');state=new;ti+=1;fills+=1
   for idx0 in m['controls']:
    idx=int(idx0);before=copy.deepcopy(state);v[start:idx]=float(state['cash'])+float(state['signed_units'])*(m['axis_prices'][start:idx]-float(state['entry_price']));code=int(m['codes'][idx]);ref=int(m['refs'][idx])
    if code==4:
     e=m['funds'][ref];t=s['funding_events'][fi];q=state['signed_units'];raw=-q*e['mark_price_at_settlement']*e['realized_rate'];amount=raw*mult if raw<0 else raw;assert t['axis_index']==idx and t['settlement_ts_ns']==e['settlement_ts'] and t['available_ts_ns']==e['available_ts'] and t['source_index']==e['source_index'] and D(t['signed_units'])==q and D(t['realized_rate'])==e['realized_rate'] and D(t['mark_price'])==e['mark_price_at_settlement'];assert D(t['cash_before'])==state['cash'] and D(t['base_amount_usdt'])==raw and D(t['amount_usdt'])==amount
     if amount:state['cash']+=amount
     assert D(t['cash_after'])==state['cash'];fi+=1;funding_checks+=1
    elif code==6:
     j=ref-1;L=p['lookback_days'];assert L in [3,4,5] and j-L>=0 and p['exit_buffer_fraction']==0;n,d=prices[j]-prices[j-L],prices[j-L];hurdle=F(str(p['return_hurdle']));wanted=-1 if n*hurdle.denominator>hurdle.numerator*d else 1 if n*hurdle.denominator < -hurdle.numerator*d else 0
     if wanted==0:
      if state['signed_units']>0 and n<0:wanted=1
      elif state['signed_units']<0 and n>0:wanted=-1
     S=p['trend_lookback_days'];assert S in [22,25] and S==row['trend_lookback_days'] and j-S>=0;sn,sd=prices[j]-prices[j-S],prices[j-S];allowed=1 if sn>0 else -1 if sn<0 else 0;wanted=wanted if wanted==allowed else 0;roc=F(n,d);dec=s['decisions'][di];assert F(dec['trend_return_exact'])==F(sn,sd) and dec['trend_lookback_days']==S;assert dec['decision_index']==ref and dec['execution_ts_ns']==int(m['ts'][idx]) and dec['signal_available_ts_ns']+engine.MIN==dec['execution_ts_ns'] and dec['desired_direction']==wanted and dec['fixed_entry_notional_usdt']==p['fixed_entry_notional_usdt'] and {x:D(y) for x,y in dec['state_before'].items()}==state and F(dec['lookback_return_exact'])==roc
     q=state['signed_units']
     if q and (1 if q>0 else -1)!=wanted:fill(idx,ref,-q,False)
     decision_checks+=1
    elif code==7:
     if wanted and state['signed_units']==0:
      steps=F(str(p['fixed_entry_notional_usdt']))/(F(native[ref-1])*F(lot));qty=D(steps.numerator//steps.denominator)*lot;fill(idx,ref,D(wanted)*qty,True)
     assert {x:D(y) for x,y in s['decisions'][di]['state_after'].items()}==state;di+=1
    elif code==9:
     if state['signed_units']:fill(idx,engine.END,-state['signed_units'],False,True)
    if state!=before:
     if idx>segstart:expected_segments.append({'axis_start':segstart,'axis_end_exclusive':idx,**segstate})
     segstart=idx;segstate=copy.deepcopy(state)
    start=idx
   v[start:]=float(state['cash'])+float(state['signed_units'])*(m['axis_prices'][start:]-float(state['entry_price']));expected_segments.append({'axis_start':segstart,'axis_end_exclusive':len(v),**segstate});saved_segments=[{a:(D(b) if a not in ['axis_start','axis_end_exclusive'] else b) for a,b in x.items()} for x in s['state_segments']];assert expected_segments==saved_segments and di==370 and fi==1110 and ti==len(s['trades']) and state['signed_units']==0 and {x:D(y) for x,y in s['terminal_state'].items()}==state
   z=s['summary'];assert z==cfg['scenes'][k] and hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==z['NAV_sha256_f64le'] and z['NAV_points']==len(v)==545013 and (v>0).all();daily=v[m['daily_indices']].tolist();assert daily==z['daily_equity_usdt'];metrics(v,daily,370,z);metric_checks+=1
   for j,(a,b) in enumerate(zip(m['fold_indices'],m['fold_indices'][1:])):metrics(v[a:b+1],daily[j*30:min((j+1)*30,370)+1],min(30,370-j*30),z['folds'][j]);metric_checks+=1
   assert len(z['folds'])==13 and [f['duration_days'] for f in z['folds']]==[30]*12+[10] and abs(math.prod(1+x['net_return_pct']/100 for x in z['folds'])-v[-1]/10000)<1e-12
   gross=sum(D(t['reference_price_PnL_usdt']) for t in s['trades']);fund=sum(D(t['amount_usdt']) for t in s['funding_events']);basefund=sum(D(t['base_amount_usdt']) for t in s['funding_events']);cost=sum(sum(D(x) for x in t['cost_parts'].values()) for t in s['trades']);near(gross,z['gross_reference_price_PnL_usdt']);near(fund,z['funding_usdt']);near(basefund,z['base_funding_same_exposure_usdt']);near(fund-basefund,z['funding_stress_increment_usdt']);near(sum(D(t['amount_usdt']) for t in s['funding_events'] if D(t['amount_usdt'])>0),z['funding_income_usdt']);near(-sum(D(t['amount_usdt']) for t in s['funding_events'] if D(t['amount_usdt'])<0),z['funding_outflow_usdt']);near(cost,z['cost_usdt']);near(gross+fund-cost,D(str(v[-1]))-10000);assert z['executions']==len(s['trades']) and z['round_trips']==sum(not t['opening'] for t in s['trades']) and z['rejected_orders']==z['cash_or_units_violations']==0
   for mask,field in [(np.isin(m['codes'],[0,2,3,4,9]),'mark_observation_drawdown_pct'),(np.isin(m['codes'],[0,1,3,4,5,6,7,8,9]),'trade_proxy_drawdown_pct')]:
    vv=v[mask];near(100*np.max(1-vv/np.maximum.accumulate(vv)),z[field]);assert z[field]<=z['max_drawdown_pct']+1e-10
   minimum,count,viol=independent_margin(m,s['state_segments']);assert count==z['margin']['state_hour_extreme_bounding_checks'] and viol==z['margin']['violations']
   if count:near(minimum,z['margin']['minimum_equity_minus_maintenance_usdt'],1e-10)
   margin_checks+=count;scenes+=1;vectors[row['fingerprint'],k]=v;verify_recent(v,m,z);recent_checks+=9
  qualification(cfg,grid_configs(report['configs']))
 assert scenes==18 and funding_checks==19980 and decision_checks==6660 and metric_checks==252 and recent_checks==162
 return vectors,{'native_cost_scenes_audited':scenes,'actual_fills_independently_verified':fills,'actual_funding_settlements_verified_including_flat':funding_checks,'causal_daily_decisions_checked':decision_checks,'native_metric_checks':metric_checks,'native_recent_metric_checks':recent_checks,'independent_state_hour_margin_checks':margin_checks}
