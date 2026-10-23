"""Independent annual signal, actual fill ledger, full NAV and gate verification."""
import json,math,statistics
from decimal import Decimal as D,localcontext,ROUND_CEILING,ROUND_FLOOR
import numpy as np
from run import ROOT,R,START,END,DAYS,SPAN,POINTS,CAPS,EMAS,sha,put,readgz,module,reg,markets

metrics=module(ROOT/'research/experiments/20261001T213902Z/audit.py','independent_annual_metrics').check_metrics

def close(a,b,tol=1e-10):
 assert abs(float(a)-float(b))<=tol*max(1,abs(float(a)),abs(float(b))),(a,b)

def signals(spec,rows,saved):
 """Use high precision alternate formulas; verify every recorded causal decision."""
 capital=spec['parameters']['initial_capital_usdt'];asset=spec['universe'][0].split('/')[0]
 assert len(saved)==DAYS
 if spec['family']=='spot-hold-comparator':
  assert all(d=={'decision_index':i,'long':True,'action':'constant_long'} for i,d in zip(range(START,END),saved));return
 values=[x['close'] for x in rows];before=False
 with localcontext() as ctx:
  ctx.prec=50
  if asset=='ETH':
   alpha=D(2)/(D(spec['parameters']['EMA_span_days'])+1);level=values[0];levels=[level]
   for x in values[1:]:level+=alpha*(x-level);levels.append(level)
  for i,d in zip(range(START,END),saved):
   assert d['decision_index']==i and D(d['prior_close'])==values[i-1]
   assert rows[i-1]['close_available_ts']<rows[i]['trade_ts']
   if asset=='BTC':
    avg=sum(values[i-65:i])/D(65);rr=[(values[j]/values[j-1]).ln() for j in range(i-20,i)]
    variance=(sum(x*x for x in rr)-sum(rr)**2/D(20))/D(19);vol=(variance*365).sqrt();eligible=vol<=D(str(spec['parameters']['annual_volatility_ceiling']))
    close(avg,D(d['SMA_prior']),1e-13);close(vol,D(d['annual_volatility_prior']),1e-13);assert eligible==d['volatility_eligible']
    if not eligible:want=False
    elif values[i-1]>avg*D('1.0125'):want=True
    elif values[i-1]<avg*D('.995'):want=False
    else:want=before
   else:
    upper=max(values[i-16:i-1]);lower=min(values[i-31:i-1]);level=levels[i-1]
    close(level,d['EMA_prior'],1e-13);assert upper==D(d['entry_channel_prior']) and lower==D(d['exit_channel_prior'])
    cu=values[i-1]>upper;cd=values[i-1]<lower;eu=values[i-1]>level*D('1.0125');ed=values[i-1]<level*D('.9875')
    assert [cu,cd,eu,ed]==[d['channel_entry'],d['channel_exit'],d['EMA_entry'],d['EMA_exit']]
    want=False if cd or ed else True if cu and eu else before
   assert want==d['long'] and d['action']==('entry' if want and not before else 'exit' if before and not want else 'hold')
   before=want

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
 report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl')
 assert report['frozen_plan_sha256']==sha(R/'plan.json') and len(batch)==18 and len({x['fingerprint'] for x in batch})==18
 market=markets(plan);arcs={};vectors={};fills=0;decisions=0;scenes=0;metric_checks=0
 assert market['BTC']['frame']['open_ts'].equals(market['ETH']['frame']['open_ts'])
 for row in batch:
  c=report['configs'][row['name']];a=readgz(ROOT/c['archive']);spec=json.loads((ROOT/row['spec']).read_text());fp=row['fingerprint']
  assert sha(ROOT/c['archive'])==c['archive_sha256'] and a['spec']==spec and a['fingerprint']==fp==reg.fingerprint(spec)
  reserved=[x for x in events if x['fingerprint']==fp and x['status']=='reserved'];assert len(reserved)==1 and reserved[0]['recorded_at_utc']<report['evaluation_started_utc']
  rec=records[fp];assert rec['status']=='reserved' or rec['report_sha256']==sha(R/'report.json')
  arcs[fp]=a
  for k,scene in a['scenes'].items():
   trades=scene['trades'];v=np.empty(POINTS);v[0]=row['capital_usdt']
   if spec['kind']=='strategy':
    m=market[row['asset']];f,rows,closes=m['frame'],m['rows'],m['closes'];signals(spec,rows,scene['decisions']);decisions+=DAYS
    cash,units=D(row['capital_usdt']),D(0);index=0;states=[]
    for offset,i in enumerate(range(START,END)):
     want=scene['decisions'][offset]['long'];expected=(want and units==0) or (not want and units!=0)
     if expected:
      t=trades[index];assert t['decision_index']==i and t['terminal'] is False and t['side']==('buy' if want else 'sell') and t['day_offset']==offset
      cash,units=fill(t,f,rows,spec['parameters']['execution']['filters'][row['asset']+'USDT'],int(k),cash,units);index+=1;fills+=1
     states.append({'day_offset':offset,'cash':str(cash),'units':str(units)})
     v[offset*SPAN+1]=float(cash+units*f['open'][i*1440+1]);v[offset*SPAN+2:(offset+1)*SPAN+1]=float(cash)+float(units)*closes[i*1440+1:(i+1)*1440+1]
    if units:
     t=trades[index];assert t['decision_index']==END and t['terminal'] is True and t['side']=='sell' and t['day_offset']==DAYS
     cash,units=fill(t,f,rows,spec['parameters']['execution']['filters'][row['asset']+'USDT'],int(k),cash,units);index+=1;fills+=1
    assert index==len(trades) and units==0 and D(scene['terminal_cash'])==cash and D(scene['terminal_units'])==units
    expanded=[{'day_offset':d,'cash':s['cash'],'units':s['units']} for s in scene['position_segments'] for d in range(s['day_offset'],s['end_day_exclusive'])];assert expanded==states
    v[-1]=float(cash);vectors[fp,k]=v
   else:
    fps=[x['fingerprint'] for x in spec['components']];assert [arcs[x]['spec']['parameters']['initial_capital_usdt'] for x in fps]==[1500,500] and [x['weight'] for x in spec['components']]==[.75,.25]
    v=vectors[fps[0],k]+vectors[fps[1],k];assert trades==[t for fp0 in fps for t in arcs[fp0]['scenes'][k]['trades']]
   s=scene['summary'];assert s==c['scenes'][k] and np.isfinite(v).all() and (v>0).all() and len(v)==s['NAV_points']==POINTS
   assert sha_bytes(v)==s['NAV_sha256_f64le'];metrics(v,s,DAYS,True);metric_checks+=1
   for j,fold in enumerate(s['folds']):metrics(v[j*30*SPAN:(j+1)*30*SPAN+1+(j==11)],fold,30,j==11);metric_checks+=1
   assert len(s['folds'])==12 and abs(math.prod(1+x['net_return_pct']/100 for x in s['folds'])-v[-1]/v[0])<1e-12
   parts={p:float(sum(D(t['cost_parts'][p]) for t in trades)) for p in ['fee','half_spread','slippage','impact','tick_rounding']};cost=sum(parts.values());gross=sum(float(D(t['reference'])*D(t['quantity']))*(1 if t['side']=='sell' else -1) for t in trades)
   assert parts==s['cost_parts_usdt'];close(cost,s['cost_usdt']);close(gross,s['gross_reference_PnL_usdt']);close(gross-cost,v[-1]-v[0]);assert s['executions']==len(trades) and s['round_trips']==sum(t['side']=='sell' for t in trades) and s['rejected_orders']==s['cash_or_units_violations']==0 and D(s['terminal_units'])==0
   scenes+=1
  ss=c['scenes'];assert c['positive_folds_1x']==sum(x['net_return_pct']>0 for x in ss['1']['folds'])
  if c['role'].startswith('benchmark'):assert c['status']=='rejected' and c['criteria']=={'reference_only_no_strategy_qualification':False};continue
  if c['role']=='component':
   axes=CAPS if c['asset']=='BTC' else EMAS;neighbors=[x for x in report['configs'].values() if x['role']=='component' and x['asset']==c['asset'] and abs(axes.index(x['axis'])-axes.index(c['axis']))<=1]
  else:neighbors=[x for x in report['configs'].values() if x['role']=='combination' and abs(CAPS.index(x['BTC_annual_volatility_ceiling'])-CAPS.index(c['BTC_annual_volatility_ceiling']))<=1 and abs(EMAS.index(x['ETH_EMA_span_days'])-EMAS.index(c['ETH_EMA_span_days']))<=1]
  frac=sum(x['scenes']['3']['net_return_pct']>0 for x in neighbors)/len(neighbors);assert c['sensitivity']=={'neighbor_names':[x['name'] for x in neighbors],'neighbor_count':len(neighbors),'local_3x_neighbor_positive_fraction':frac}
  ratio=ss['1']['gross_reference_PnL_to_execution_cost'];expected={'positive_all_costs':all(x['net_return_pct']>0 for x in ss.values()),'eight_positive_1x_folds':c['positive_folds_1x']>=8,'minute_DD3_lte25pct':ss['3']['max_drawdown_pct']<=25,'neighbourhood_positive3_gte60pct':frac>=.6,'four_round_trips1':ss['1']['round_trips']>=4,'gross_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_balance_violations':all(x['cash_or_units_violations']==0 for x in ss.values()),'no_order_rejections':all(x['rejected_orders']==0 for x in ss.values()),'terminal_flat':all(D(x['terminal_units'])==0 for x in ss.values())}
  assert expected==c['criteria'] and (c['status']=='passed')==all(expected.values())
 assert scenes==54 and metric_checks==702 and decisions==8640
 assert all(sha(ROOT/p)==h for p,h in json.loads((R/'context.json').read_text())['account_hashes_before'].items())
 out={'passed':True,'financial_configs':18,'candidates':15,'benchmarks':3,'leaf_cost_scenes_rebuilt_from_actual_trades':24,'parent_cost_scenes_summed_once':30,'full_NAV_points_per_scene':POINTS,'full_NAV_points_audited':scenes*POINTS,'independent_overall_and_fold_metric_checks':metric_checks,'independent_causal_decisions_checked':decisions,'actual_leaf_fills_independently_verified':fills,'negative_returns_retained':54,'protected_source_accounts_unchanged':True,'report_sha256':sha(R/'report.json')};put(R/'verification.json',out);print(json.dumps(out),flush=True)

def sha_bytes(v):
 import hashlib
 return hashlib.sha256(v.astype('<f8',copy=False).tobytes()).hexdigest()

if __name__=='__main__':main()
