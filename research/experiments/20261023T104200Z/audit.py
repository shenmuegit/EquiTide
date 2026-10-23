"""Independent shock integer boundaries,frozen entry state,actual fills and full NAV audit."""
import copy,json,math,statistics,hashlib
from decimal import Decimal as D,ROUND_CEILING,ROUND_FLOOR
from fractions import Fraction as F
import numpy as np
from run import ROOT,R,START,END,DAYS,SPAN,POINTS,DROPS,HOLDS,sha,put,readgz,module,reg,prior
# Independent fill assertions retained verbatim from prior audit;production fill is not called.
def close(a,b,tol=1e-10):
 assert abs(float(a)-float(b))<=tol*max(1,abs(float(a)),abs(float(b))),(a,b)

def fill(t,frame,rows,filters,m,cash,units):
 """No call to production fill: independent price/lot/cost and cash identity."""
 i=t['decision_index'];mi=i*1440+1;ref=frame['open'][mi];buy=t['side']=='buy';qty=D(t['quantity']);price=D(t['execution'])
 assert t['status']=='filled' and D(t['cash_before'])==cash and D(t['units_before'])==units
 assert t['trade_ts_ns']==rows[i]['trade_ts']==frame['open_ts'][mi] and D(t['reference'])==ref
 assert rows[i-1]['close_available_ts']+60000000000==t['trade_ts_ns']
 budget=cash if buy else units*ref;adv=D(t['lagged_ADV']);sigma=D(t['lagged_sigma']);participation=budget/adv
 close(adv,statistics.mean(float(x['quote_volume']) for x in rows[i-20:i]),1e-13)
 rr=[math.log(float(rows[j]['close'])/float(rows[j-1]['close'])) for j in range(i-20,i)]
 close(sigma,statistics.stdev(rr),1e-13);assert D(t['budget'])==budget and D(t['participation'])==participation<=D('.001')
 history=frame.slice(mi-5,5);assert int(history['available_ts'].max())<=rows[i]['trade_ts'];proxy=history['quote_volume'].sum()/history['base_volume'].sum();assert D(t['proxy_VWAP5'])==proxy
 fee=D('.001')*m;spread=D('.0001')*m;slip=D('.0002')*m;impact=D('.5')*sigma*participation.sqrt()*m
 theoretical=ref*(1+(spread+slip+impact)*(1 if buy else -1));tick=D(filters['PRICE_FILTER']['tickSize']);step=D(filters['LOT_SIZE']['stepSize'])
 assert price==(theoretical/tick).to_integral_value(rounding=ROUND_CEILING if buy else ROUND_FLOOR)*tick and price%tick==0 and qty%step==0
 expected_qty=((cash/(price*(1+fee)) if buy else units)/step).to_integral_value(rounding=ROUND_FLOOR)*step;assert qty==expected_qty
 pf,lf,nf=filters['PRICE_FILTER'],filters['LOT_SIZE'],filters['NOTIONAL'];assert D(pf['minPrice'])<=price<=D(pf['maxPrice']) and D(lf['minQty'])<=qty<=D(lf['maxQty']) and D(nf['minNotional'])<=qty*price<=D(nf['maxNotional'])
 if filters.get('PERCENT_PRICE_BY_SIDE'):
  percent=filters['PERCENT_PRICE_BY_SIDE'];prefix='bid' if buy else 'ask';assert proxy*D(percent[prefix+'MultiplierDown'])<=price<=proxy*D(percent[prefix+'MultiplierUp'])
 parts={'fee':qty*price*fee,'half_spread':qty*ref*spread,'slippage':qty*ref*slip,'impact':qty*ref*impact,'tick_rounding':qty*abs(price-theoretical)}
 assert all(D(t['cost_parts'][k])==v for k,v in parts.items()) and D(t['cost_usdt'])==sum(parts.values())
 cash2=cash+(-qty*price-parts['fee'] if buy else qty*price-parts['fee']);units2=units+(qty if buy else -qty)
 assert cash2==D(t['cash_after'])>=0 and units2==D(t['units_after'])>=0
 assert abs(cash+units*ref-cash2-units2*ref-sum(parts.values()))<D('1e-20')
 return cash2,units2

def main():
 report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');market=prior.markets(plan);independent=module(ROOT/'research/experiments/20261001T213902Z/audit.py','shock_independent_metrics');independent.SPAN=SPAN
 assert len(batch)==18 and report['frozen_plan_sha256']==sha(R/'plan.json') and POINTS==519123;assert market['BTC']['frame']['open_ts'].equals(market['ETH']['frame']['open_ts']);fills=decisions=audited=metric_checks=target_exits=timeout_exits=terminal_exits=0
 for row in batch:
  c=report['configs'][row['name']];arc=readgz(ROOT/c['archive']);spec=json.loads((ROOT/row['spec']).read_text());assert sha(ROOT/c['archive'])==c['archive_sha256'] and arc['spec']==spec and arc['fingerprint']==row['fingerprint']==reg.fingerprint(spec);p=spec['parameters'];reserves=[x for x in events if x['fingerprint']==row['fingerprint'] and x['status']=='reserved'];assert len(reserves)==1 and reserves[0]['recorded_at_utc']<report['evaluation_started_utc']
  if records[row['fingerprint']]['status']!='reserved':assert records[row['fingerprint']]['report_sha256']==sha(R/'report.json')
  m=market[row['asset']];rows,f,closes=m['rows'],m['frame'],m['closes'];values=[x['close'] for x in rows];price=[int(x*D(10)**18) for x in values];assert all(D(x)*D(10)**18==y for x,y in zip(values,price));drop=F(str(p['entry_three_day_loss']));H=p['maximum_holding_days']
  for k,s in arc['scenes'].items():
   v=np.empty(POINTS);v[0]=2000;cash,units,position=D(2000),D(0),None;index=0;states=[];trades=s['trades'];assert len(s['decisions'])==DAYS
   def execute(i,buy,terminal=False):
    nonlocal cash,units,position,index,fills,terminal_exits
    t=trades[index];assert t['asset']==row['asset'] and t['decision_index']==i and t['side']==('buy' if buy else 'sell') and t['terminal']==terminal and t['day_offset']==i-START and t['position_before']==position
    assert (position is None and units==0) if buy else (position is not None and units>0)
    cash,units=fill(t,f,rows,p['execution']['filters'][row['asset']+'USDT'],int(k),cash,units);position={'entry_index':i,'entry_signal_close':str(values[i-1]),'shock_start_close':str(values[i-4])} if buy else None;assert t['position_after']==position;index+=1;fills+=1;terminal_exits+=int(terminal)
   for d,i in enumerate(range(START,END)):
    dec=s['decisions'][d];j=i-1;assert dec['decision_index']==i and D(dec['prior_close'])==values[j] and D(dec['shock_start_close'])==values[j-3] and dec['position_before']==position and rows[j]['close_available_ts']+60000000000==rows[i]['trade_ts'];v[d*SPAN+1]=float(cash+units*f['open'][i*1440+1]);numerator=price[j]-price[j-3];denominator=price[j-3];assert F(dec['three_day_return_exact'])==F(numerator,denominator)
    if position:
     e=position['entry_index'];A=price[e-4];B=price[e-1];age=i-e;recovery=2*price[j]>=A+B;timeout=age>=H;action='exit' if recovery or timeout else 'hold';assert D(position['shock_start_close'])==values[e-4] and D(position['entry_signal_close'])==values[e-1]
    else:age=recovery=timeout=None;action='entry' if numerator*drop.denominator < -drop.numerator*denominator else 'cash'
    assert dec['holding_age_days']==age and dec['half_recovery_hit']==recovery and dec['timeout_hit']==timeout and dec['action']==action
    if action in ['entry','exit']:
     execute(i,action=='entry');target_exits+=int(action=='exit' and recovery);timeout_exits+=int(action=='exit' and timeout)
    assert dec['position_after']==position;v[d*SPAN+2]=float(cash+units*f['open'][i*1440+1]);v[d*SPAN+3:(d+1)*SPAN+1]=float(cash)+float(units)*closes[i*1440+1:(i+1)*1440+1];states.append({'day_offset':d,'cash':str(cash),'units':str(units),'position':copy.deepcopy(position)});decisions+=1
   v[-2]=float(cash+units*f['open'][END*1440+1])
   if units:execute(END,False,True)
   v[-1]=float(cash);assert units==0 and position is None and index==len(trades) and s['terminal_position'] is None and D(s['terminal_cash'])==cash and D(s['terminal_units'])==0
   assert len({t['decision_index'] for t in trades})==len(trades),'No same-day exit/reentry is permitted'
   expanded=[{'day_offset':d,'cash':z['cash'],'units':z['units'],'position':z['position']} for z in s['position_segments'] for d in range(z['day_offset'],z['end_day_exclusive'])];assert expanded==states;z=s['summary'];assert z==c['scenes'][k] and len(v)==z['NAV_points']==POINTS and hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==z['NAV_sha256_f64le'] and np.isfinite(v).all() and (v>0).all();independent.check_metrics(v,z,DAYS,True);metric_checks+=1
   for j,fold in enumerate(z['folds']):independent.check_metrics(v[j*30*SPAN:(j+1)*30*SPAN+1+2*(j==11)],fold,30,j==11);metric_checks+=1
   assert len(z['folds'])==12 and abs(math.prod(1+x['net_return_pct']/100 for x in z['folds'])-v[-1]/2000)<1e-12
   parts={p0:float(sum(D(t['cost_parts'][p0]) for t in trades)) for p0 in ['fee','half_spread','slippage','impact','tick_rounding']};cost=sum(parts.values());gross=sum(float(D(t['quantity'])*D(t['reference']))*(1 if t['side']=='sell' else -1) for t in trades);assert parts==z['cost_parts_usdt'];close(cost,z['cost_usdt']);close(gross,z['gross_reference_PnL_usdt']);close(gross-cost,v[-1]-v[0]);assert z['executions']==len(trades) and z['round_trips']==sum(t['side']=='sell' for t in trades) and z['cash_or_units_violations']==z['rejected_orders']==0;audited+=1
  neighbors=[x for x in report['configs'].values() if x['asset']==c['asset'] and abs(DROPS.index(x['entry_three_day_loss'])-DROPS.index(c['entry_three_day_loss']))<=1 and abs(HOLDS.index(x['maximum_holding_days'])-HOLDS.index(c['maximum_holding_days']))<=1];frac=sum(x['scenes']['3']['net_return_pct']>0 for x in neighbors)/len(neighbors);assert c['sensitivity']=={'neighbor_names':[x['name'] for x in neighbors],'neighbor_count':len(neighbors),'local_3x_neighbor_positive_fraction':frac};ss=c['scenes'];ratio=ss['1']['gross_reference_PnL_to_execution_cost'];positive=sum(x['net_return_pct']>0 for x in ss['1']['folds']);assert positive==c['positive_folds_1x'];expected={'positive_all_costs':all(x['net_return_pct']>0 for x in ss.values()),'eight_positive_1x_folds':positive>=8,'minute_DD3_lte25pct':ss['3']['max_drawdown_pct']<=25,'neighbourhood_positive3_gte60pct':frac>=.6,'four_round_trips1':ss['1']['round_trips']>=4,'gross_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_balance_violations':all(x['cash_or_units_violations']==0 for x in ss.values()),'no_order_rejections':all(x['rejected_orders']==0 for x in ss.values()),'terminal_flat':all(D(x['terminal_units'])==0 for x in ss.values())};assert expected==c['criteria'] and (c['status']=='passed')==all(expected.values())
 assert audited==54 and metric_checks==702 and decisions==19440;assert all(sha(ROOT/p)==h for p,h in json.loads((R/'context.json').read_text())['account_hashes_before'].items());out={'passed':True,'financial_configs':18,'cost_scenes_audited':audited,'full_NAV_points_per_scene':POINTS,'full_NAV_points_audited':audited*POINTS,'independent_overall_and_fold_metric_checks':metric_checks,'integer_boundary_and_frozen_state_decisions_checked':decisions,'actual_fills_independently_verified':fills,'half_recovery_exit_events':target_exits,'timeout_exit_events':timeout_exits,'terminal_exit_events':terminal_exits,'exit_reason_overlap_disclosed':'Recovery andtimeout counts overlap when both true;terminal separate.','no_same_day_exit_reentry':True,'protected_source_accounts_unchanged':True,'report_sha256':sha(R/'report.json')};put(R/'verification.json',out);print(json.dumps(out),flush=True)

if __name__=='__main__':main()
