"""Independent weekly calendar, integer ranking, two-leg fill/NAV and metric audit."""
import json,math,statistics,hashlib
from datetime import datetime,timezone
from decimal import Decimal as D,ROUND_CEILING,ROUND_FLOOR
from fractions import Fraction as F
import numpy as np
from run import ROOT,R,START,END,DAYS,SPAN,POINTS,LOOKS,GAPS,SKIPS,sha,put,readgz,module,reg,prior
# Reuse the independently written actual-fill assertions verbatim;never call production fill.
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

def independent_choice(prices,j,L,S,G,held):
 # Integer cross-products compare normalized returns without production Fraction arithmetic.
 score={a:(v[j-S]-v[j-S-L],v[j-S-L]) for a,v in prices.items()};absolute={a:(v[j]-v[j-L],v[j-L]) for a,v in prices.items()};eligible=[a for a in ['BTC','ETH'] if absolute[a][0]>0]
 if not eligible:best=None
 elif len(eligible)==1:best=eligible[0]
 else:best='ETH' if score['ETH'][0]*score['BTC'][1]>score['BTC'][0]*score['ETH'][1] else 'BTC'
 target=best
 if held in eligible:
  target=held
  if best!=held:
   n,d=score[best];hn,hd=score[held];g=F(str(G))
   if (n*hd-hn*d)*g.denominator>g.numerator*d*hd:target=best
 return target,score,absolute,eligible,best

def main():
 report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());events=reg.read_events(ROOT/'research/automation/registry.jsonl');records=reg.read_records(ROOT/'research/automation/registry.jsonl');market=prior.markets(plan);price={a:[int(x['close']*D(10)**18) for x in m['rows']] for a,m in market.items()};assert all(D(x['close'])*D(10)**18==y for a,m in market.items() for x,y in zip(m['rows'],price[a]))
 independent=module(ROOT/'research/experiments/20261001T213902Z/audit.py','weekly_independent_metric_assertions');independent.SPAN=SPAN
 assert report['frozen_plan_sha256']==sha(R/'plan.json') and len(batch)==18 and POINTS==519483;assert market['BTC']['frame']['open_ts'].equals(market['ETH']['frame']['open_ts'])
 fills=decisions=scheduled=audited=metric_checks=rotations=0
 for row in batch:
  c=report['configs'][row['name']];a=readgz(ROOT/c['archive']);spec=json.loads((ROOT/row['spec']).read_text());assert sha(ROOT/c['archive'])==c['archive_sha256'] and a['fingerprint']==row['fingerprint']==reg.fingerprint(spec) and a['spec']==spec;p=spec['parameters'];reserves=[e for e in events if e['fingerprint']==row['fingerprint'] and e['status']=='reserved'];assert len(reserves)==1 and reserves[0]['recorded_at_utc']<report['evaluation_started_utc']
  if records[row['fingerprint']]['status']!='reserved':assert records[row['fingerprint']]['report_sha256']==sha(R/'report.json')
  for k,s in a['scenes'].items():
   v=np.empty(POINTS);v[0]=2000;cash,units,held=D(2000),D(0),None;index=0;states=[];trades=s['trades'];assert len(s['decisions'])==360
   def wealth(i):return cash+(units*market[held]['frame']['open'][i*1440+1] if held else D(0))
   def execute(asset,buy,i,terminal=False):
    nonlocal cash,units,held,index,fills
    t=trades[index];assert t['asset']==asset and t['decision_index']==i and t['terminal']==terminal and t['side']==('buy' if buy else 'sell') and t['held_before']==held and t['day_offset']==i-START
    cash,units=fill(t,market[asset]['frame'],market[asset]['rows'],p['execution']['filters'][asset+'USDT'],int(k),cash,units);held=asset if buy else None;assert t['held_after']==held;index+=1;fills+=1
   for d,i in enumerate(range(START,END)):
    dec=s['decisions'][d];hb=held;is_monday=datetime.fromtimestamp(market['BTC']['rows'][i]['trade_ts']/1e9,timezone.utc).weekday()==0;assert dec['decision_index']==i and dec['signal_index']==i-1 and dec['scheduled_Monday']==is_monday and dec['held_before']==held;v[d*SPAN+1]=float(wealth(i));target=held
    if is_monday:
     target,scores,absolute,eligible,best=independent_choice(price,i-1,p['formation_days'],p['skip_recent_days'],p['switching_return_gap'],held);assert dec['eligible']==eligible and dec['winner_before_switch_hurdle']==best
     for asset in ['BTC','ETH']:assert F(dec['scores'][asset])==F(*scores[asset]) and F(dec['absolute_returns'][asset])==F(*absolute[asset])
     scheduled+=1
    else:assert not any(x in dec for x in ['scores','absolute_returns','eligible','winner_before_switch_hurdle'])
    assert dec['desired_target']==target
    if target!=held and held is not None:execute(held,False,i)
    v[d*SPAN+2]=float(wealth(i))
    if target is not None and held is None:execute(target,True,i)
    v[d*SPAN+3]=float(wealth(i));assert dec['held_after']==held;rotations+=int(hb is not None and target is not None and hb!=target);states.append({'day_offset':d,'cash':str(cash),'units':str(units),'asset':held});v[d*SPAN+4:(d+1)*SPAN+1]=float(cash)+(float(units)*market[held]['closes'][i*1440+1:(i+1)*1440+1] if held else np.zeros(1440));decisions+=1
   v[-2]=float(wealth(END))
   if held:execute(held,False,END,True)
   v[-1]=float(cash);assert held is None and units==0 and index==len(trades) and s['terminal_asset'] is None and D(s['terminal_units'])==0 and D(s['terminal_cash'])==cash
   expanded=[{'day_offset':d,'cash':z['cash'],'units':z['units'],'asset':z['asset']} for z in s['position_segments'] for d in range(z['day_offset'],z['end_day_exclusive'])];assert expanded==states
   z=s['summary'];assert z==c['scenes'][k] and hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==z['NAV_sha256_f64le'] and len(v)==z['NAV_points']==POINTS;assert np.isfinite(v).all() and (v>0).all();independent.check_metrics(v,z,360,True);metric_checks+=1
   for j,f in enumerate(z['folds']):independent.check_metrics(v[j*30*SPAN:(j+1)*30*SPAN+1+2*(j==11)],f,30,j==11);metric_checks+=1
   assert len(z['folds'])==12 and abs(math.prod(1+f['net_return_pct']/100 for f in z['folds'])-v[-1]/2000)<1e-12
   parts={p0:float(sum(D(t['cost_parts'][p0]) for t in trades)) for p0 in ['fee','half_spread','slippage','impact','tick_rounding']};cost=sum(parts.values());gross=sum(float(D(t['reference'])*D(t['quantity']))*(1 if t['side']=='sell' else -1) for t in trades);assert parts==z['cost_parts_usdt'];close(cost,z['cost_usdt']);close(gross,z['gross_reference_PnL_usdt']);close(gross-cost,v[-1]-v[0]);assert z['executions']==len(trades) and z['round_trips']==sum(t['side']=='sell' for t in trades) and z['rejected_orders']==z['cash_or_units_violations']==0;audited+=1
  neighbors=[x for x in report['configs'].values() if x['skip_recent_days']==c['skip_recent_days'] and abs(LOOKS.index(x['formation_days'])-LOOKS.index(c['formation_days']))<=1 and abs(GAPS.index(x['switching_return_gap'])-GAPS.index(c['switching_return_gap']))<=1];frac=sum(x['scenes']['3']['net_return_pct']>0 for x in neighbors)/len(neighbors);assert c['sensitivity']=={'neighbor_names':[x['name'] for x in neighbors],'neighbor_count':len(neighbors),'local_3x_neighbor_positive_fraction':frac};ss=c['scenes'];ratio=ss['1']['gross_reference_PnL_to_execution_cost'];positive=sum(x['net_return_pct']>0 for x in ss['1']['folds']);assert positive==c['positive_folds_1x'];expected={'positive_all_costs':all(x['net_return_pct']>0 for x in ss.values()),'eight_positive_1x_folds':positive>=8,'minute_DD3_lte25pct':ss['3']['max_drawdown_pct']<=25,'neighbourhood_positive3_gte60pct':frac>=.6,'four_round_trips1':ss['1']['round_trips']>=4,'gross_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_balance_violations':all(x['cash_or_units_violations']==0 for x in ss.values()),'no_order_rejections':all(x['rejected_orders']==0 for x in ss.values()),'terminal_flat':all(D(x['terminal_units'])==0 for x in ss.values())};assert expected==c['criteria'] and (c['status']=='passed')==all(expected.values())
 assert audited==54 and metric_checks==702 and decisions==19440;assert all(sha(ROOT/path)==h for path,h in json.loads((R/'context.json').read_text())['account_hashes_before'].items());out={'passed':True,'financial_configs':18,'cost_scenes_audited':audited,'full_NAV_points_per_scene':POINTS,'full_NAV_points_audited':audited*POINTS,'independent_overall_and_fold_metric_checks':metric_checks,'calendar_and_state_decisions_checked':decisions,'independent_integer_score_Monday_decisions':scheduled,'actual_fills_independently_verified':fills,'two_leg_coin_rotations_verified':rotations,'protected_source_accounts_unchanged':True,'report_sha256':sha(R/'report.json')};put(R/'verification.json',out);print(json.dumps(out),flush=True)

if __name__=='__main__':main()
