"""Independent past-only OLS, native money/events and paired policy replay; no model call."""
import copy,gzip,hashlib,json,math,statistics
from decimal import Decimal as D,ROUND_CEILING,ROUND_FLOOR
from fractions import Fraction as F
import numpy as np
from common import *
import market
from audit_helpers import near,metrics,independent_margin,verify_recent

def verify_features(ms,ff):
 xs=[math.log(float(x)) for x in ms['BTC']['hour_closes']];ys=[math.log(float(x)) for x in ms['ETH']['hour_closes']];out=[]
 for i,h in enumerate(range(792,9672)):
  f=ff[i];j=h-1;b=j-24;a=b-720;xx=xs[a:b];yy=ys[a:b];mx=math.fsum(xx)/720;my=math.fsum(yy)/720;den=math.fsum((v-mx)**2 for v in xx);assert f['hour']==h and f['tested_hour_index']==j and f['train_start']==a and f['train_stop_exclusive']==b and a>=0 and b<j
  if den<=1e-20:assert not f['eligible'];out.append({**f,'eligible':False});continue
  beta=math.fsum((x-mx)*(y-my) for x,y in zip(xx,yy))/den;alpha=my-beta*mx;res=[y-alpha-beta*x for x,y in zip(xx,yy)];mean=math.fsum(res)/720;std=math.sqrt(math.fsum((x-mean)**2 for x in res)/719);near(beta,f['beta'],1e-9);near(alpha,f['alpha'],1e-9);near(mean,f['residual_mean'],1e-8);near(std,f['residual_std'],1e-8)
  if std<=1e-12:assert not f['eligible'];out.append({**f,'eligible':False});continue
  z=(ys[j]-alpha-beta*xs[j]-mean)/std;near(z,f['z'],1e-7);eligible=bool(math.isfinite(z) and .5<=beta<=2);assert f['eligible']==eligible;out.append({**f,'z':z,'eligible':eligible})
 assert len(out)==8880;return out

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

def policy(scene,spec,m,ff):
 side=0;entry=None;recovery=False;completed=0;units={'BTC':D(0),'ETH':D(0)};pointers={'BTC':0,'ETH':0};by={(int(t),int(c)):i for i,(t,c) in enumerate(zip(m['ts'],m['codes'])) if c in [6,7,9]};trs={a:scene['legs'][a]['trades'] for a in units};p=spec['parameters']
 def take(a,idx,opening,reason,expected_side=0,f=None,terminal=False):
  i=pointers[a];assert i<len(trs[a]);t=trs[a][i];assert t['axis_index']==idx and t['opening']==opening and t['decision_reason']==reason
  assert t['terminal']==terminal and D(t['state_before']['signed_units'])==units[a]
  if opening:
   h=f['hour'];amount=D(str(f['beta']))*D(2000) if a=='BTC' else D(2000);masset=markets[a];prior=masset['hour_closes'][h-1];lot=D(masset['meta']['lot_size']);steps=F(amount)/(F(prior)*F(lot));q=D(steps.numerator//steps.denominator)*lot;assert D(t['change_signed_units'])==q*(expected_side if a=='ETH' else -expected_side)
  else:assert D(t['change_signed_units'])==-units[a]
  units[a]=D(t['state_after']['signed_units']);pointers[a]+=1;return t['status']=='filled'
 assert len(scene['decisions'])==8880
 for d,f in zip(scene['decisions'],ff):
  h=f['hour'];t=m['first_ns']+h*HOUR+MIN;idx6=by[t,6];idx7=by[t,7];oldside,oldentry,oldrecovery=side,entry,recovery
  if recovery:close=True;fresh=0;reason='recovery'
  elif not f['eligible']:close=bool(side);fresh=0;reason='invalid_fit'
  elif side and t-entry>=48*HOUR:close=True;fresh=0;reason='timeout'
  else:
   z=f['z'];fresh=1 if z<=-p['entry_z'] else -1 if z>=p['entry_z'] else 0
   if not side:close=False;reason='entry' if fresh else 'flat'
   elif fresh and fresh!=side:close=True;reason='reverse'
   elif side==1 and z>=-p['exit_z'] or side==-1 and z<=p['exit_z']:close=True;fresh=0;reason='exit_crossing'
   else:close=False;fresh=0;reason='hold'
  assert d['hour']==h and d['feature_index']==h-792 and d['signal_available_ts_ns']==t-MIN and d['execution_ts_ns']==t and d['side_before']==oldside and d['entry_ns_before']==oldentry and d['recovery_before']==oldrecovery and d['close']==close and d['open_side']==fresh and d['reason']==reason
  if close:
   for a in units:
    if units[a]:take(a,idx6,False,reason)
   if all(v==0 for v in units.values()):completed+=int(side!=0);side=0;entry=None;recovery=False
   else:recovery=True
  if fresh and all(v==0 for v in units.values()):
   btc=take('BTC',idx7,True,'open_first',fresh,f)
   if btc:
    eth=take('ETH',idx7,True,'open_second',fresh,f)
    if eth:side=fresh;entry=t;recovery=False
    else:take('BTC',idx7,False,'second_leg_reject_unwind');recovery=any(units.values())
  assert d['side_after']==side and d['entry_ns_after']==entry and d['recovery_after']==bool(recovery) and d['completed_pairs_so_far']==completed
 t=m['end_ns'];idx=by[t,9]
 for a in units:
  if units[a]:take(a,idx,False,'terminal',terminal=True)
 if all(v==0 for v in units.values()):completed+=int(side!=0);side=0;entry=None;recovery=False
 else:recovery=True
 assert all(pointers[a]==len(trs[a]) for a in units) and scene['terminal_pair_state']=={'side':side,'entry_ns':entry,'recovery':bool(recovery)} and scene['summary']['round_trips']==completed
 return len(scene['decisions'])

def main():
 global markets
 plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');assert report['frozen_plan_sha256']==sha(R/'plan.json') and sha(CORE_PATH)==plan['source_core']['sha256'];markets,m=market.load(plan);assert len(m['ts'])==report['parent_axis']['union_points']==570543;ff=json.loads(gzip.decompress((R/'features.json.gz').read_bytes()))['features'];independent=verify_features(markets,ff);counters={'fills':0,'rejects':0,'funding':0,'margin_checks':0,'metric_checks':0};decision_checks=jointchecks=recentchecks=0
 for c in report['configs'].values():
  path=ROOT/c['archive'];arc=json.loads(gzip.decompress(path.read_bytes()));spec=json.loads((ROOT/c['spec']).read_text());assert sha(path)==c['archive_sha256'] and arc['spec']==spec and arc['fingerprint']==c['fingerprint']==reg.fingerprint(spec);rv=[e for e in events if e['fingerprint']==c['fingerprint'] and e['status']=='reserved'];assert len(rv)==1 and rv[0]['recorded_at_utc']<report['evaluation_started_utc']
  for k,z in arc['scenes'].items():
   vv={a:native(z['legs'][a],markets[a],m,int(k),ff,spec,counters) for a in ['BTC','ETH']};v=vv['BTC']+vv['ETH'];s=z['summary'];assert s==c['scenes'][k] and core.navhash(v)==s['NAV_sha256_f64le'] and s['NAV_points']==len(v) and s['initial_capital_usdt']==20000;daily=v[m['daily_indices']].tolist();assert daily==s['daily_equity_usdt'];metrics(v,daily,370,s);jointchecks+=1
   for j,(a,b) in enumerate(zip(m['fold_indices'],m['fold_indices'][1:])):metrics(v[a:b+1],daily[j*30:min(j*30+30,370)+1],min(30,370-j*30),s['folds'][j]);jointchecks+=1
   verify_recent(v,m,s);recentchecks+=9;decision_checks+=policy(z,spec,m,independent)
   parts=[z['legs'][a]['summary'] for a in ['BTC','ETH']]
   for key in ['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_income_usdt','funding_outflow_usdt','funding_stress_increment_usdt','gross_reference_price_PnL_usdt']:near(s[key],sum(x[key] for x in parts))
   for key in ['executions','rejected_orders','cash_or_units_violations','funding_settlements','nonzero_funding_settlements']:assert s[key]==sum(x[key] for x in parts)
   assert s['leg_round_trips']==sum(x['round_trips'] for x in parts) and s['margin']['independent_sleeve_violations']==sum(x['margin']['violations'] for x in parts) and s['margin']['no_cross_margin_netting']
   near(s['gross_reference_price_PnL_usdt']+s['funding_usdt']-s['cost_usdt'],v[-1]-20000)
  # Independently verify full-grid qualification without invoking the strategy.
  ns=[x for x in report['configs'].values() if abs(ENTRIES.index(x['entry_z'])-ENTRIES.index(c['entry_z']))<=1 and abs(EXITS.index(x['exit_z'])-EXITS.index(c['exit_z']))<=1];good=lambda x:all(sum(f['net_return_pct']>0 for f in x['scenes'][k]['recent40']['folds'])>=6 for k in ['1','2','3']);s=c['scenes'];ratio=s['1']['gross_reference_PnL_to_execution_cost'];tests={'positive_all_costs':all(x['net_return_pct']>0 for x in s.values()),'nine_of_twelve_positive_complete30d_1x_folds':sum(f['net_return_pct']>0 for f in s['1']['folds'][:12])>=9,'recent40_positive_all_costs':all(x['recent40']['net_return_pct']>0 for x in s.values()),'recent40_six_of_eight_positive5d_all_costs':good(c),'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'local_positive3_gte60pct':sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)>=.6,'local_recent6of8_allcost_gte60pct':sum(good(x) for x in ns)/len(ns)>=.6,'four_completed_pair_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_collateral':all(x['cash_or_units_violations']==0 for x in s.values()),'no_order_rejections':all(x['rejected_orders']==0 for x in s.values()),'no_margin_proxy_violations':all(x['margin']['independent_sleeve_violations']==0 for x in s.values()),'terminal_flat':all(x['terminal_flat'] for x in s.values()),'minimum180days':True};assert c['criteria']==tests and c['status']==('passed' if all(tests.values()) else 'rejected') and c['sensitivity']['local_recent6of8_allcost_fraction']==sum(good(x) for x in ns)/len(ns)
 assert counters['funding']==59940 and counters['metric_checks']==756 and decision_checks==239760 and jointchecks==378 and recentchecks==243
 ctx=json.loads((R/'context.json').read_text());assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items());put(R/'verification.json',{'passed':True,'actual_financial_configs':9,'new_cost_scenes':27,'internal_native_bank_cost_curves':54,'independent_rolling_OLS_fits':8880,'independent_pair_decisions':decision_checks,'native_overall_fold_metric_checks':counters['metric_checks'],'joint_overall_fold_metric_checks':jointchecks,'joint_recent_metric_checks':recentchecks,'actual_fills_verified':counters['fills'],'actual_rejected_orders_verified':counters['rejects'],'actual_funding_settlements_verified':counters['funding'],'native_state_hour_margin_checks':counters['margin_checks'],'full_NAV_points_per_curve':len(m['ts']),'curves_audited':81,'full_NAV_points_audited':len(m['ts'])*81,'source_core_unchanged':True,'protected_inputs_unchanged':True,'no_model_or_trade_function_called_by_audit':True,'report_sha256':sha(R/'report.json')});print(json.dumps(json.loads((R/'verification.json').read_text())),flush=True)
if __name__=='__main__':main()
