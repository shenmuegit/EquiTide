"""Independent signed ledger, funding, causal sizing, sampled curves and risk verification."""
import bisect,copy,gzip,hashlib,json,math,statistics
from decimal import Decimal as D,ROUND_CEILING,ROUND_FLOOR
from fractions import Fraction as F
import numpy as np
import engine
from run import ROOT,R,LOOKS,HURDLES,EXITS,sha,put,reg,grid_configs,neighbors,axes

def near(a,b,tol=1e-9):assert abs(float(a)-float(b))<=tol*max(1,abs(float(a)),abs(float(b))),(a,b)

def metrics(curve,daily,days,saved):
 values=np.asarray(curve);d=np.asarray(daily);rr=d[1:]/d[:-1]-1;sd=np.std(rr,ddof=1);cagr=100*((values[-1]/values[0])**(365/days)-1);dd=float(max(100*(1-values/np.maximum.accumulate(values))));near(saved['net_return_pct'],100*(values[-1]/values[0]-1),1e-12);near(saved['max_drawdown_pct'],dd,1e-12);near(saved['cagr_pct'],cagr,1e-12);near(saved['daily_mark_drawdown_pct'],max(100*(1-d/np.maximum.accumulate(d))),1e-12)
 if sd:near(saved['sharpe_365'],np.mean(rr)/sd*math.sqrt(365),1e-10)
 else:assert saved['sharpe_365'] is None
 if dd:near(saved['calmar'],cagr/dd,1e-10)
 else:assert saved['calmar'] is None

def verify_axis(m):
 f,h=m['frame'],m['hour'];codes=m['codes'];ts=m['ts'];S,E=m['start_ns'],m['end_ns'];assert len(ts)==545013 and np.all(np.diff(ts)>=0) and np.array_equal(np.lexsort((codes,ts)),np.arange(len(ts)))
 for code in range(10):assert np.all(m['axis_prices'][codes==code]>0)
 ix=np.flatnonzero(codes==1);assert len(ix)==532800 and ts[ix].tolist()==f['available_ts'][engine.START*1440+1:engine.END*1440+1].to_list();assert np.array_equal(m['axis_prices'][ix],np.asarray([float(x) for x in f['close'][engine.START*1440+1:engine.END*1440+1]]))
 for code in [5,6,7]:
  ix=np.flatnonzero(codes==code);assert len(ix)==370 and ts[ix].tolist()==[S+i*engine.DAY for i in range(370)]
  assert m['axis_prices'][ix].tolist()==[float(f['open'][i*1440+1]) for i in range(engine.START,engine.END)]
 for code in [3,4]:
  ix=np.flatnonzero(codes==code);assert len(ix)==1110 and ts[ix].tolist()==[e['settlement_ts'] for e in m['funds']]
  assert m['axis_prices'][ix].tolist()==[float(e['mark_price_at_settlement']) for e in m['funds']]
 ix=np.flatnonzero(codes==2);expected=[j for j,z in enumerate(h['available_ts']) if S<int(z)<=E];assert len(ix)==8880 and ts[ix].tolist()==[int(h['available_ts'][j]) for j in expected];assert len(m['controls'])==1851 and len(m['daily_indices'])==371 and len(m['fold_indices'])==14
 assert ts[0]==S and ts[-1]==E and codes[0]==0 and codes[-1]==9

def independent_margin(m,segments):
 ta=[int(m['ts'][s['axis_start']]) for s in segments];tb=[int(m['ts'][s['axis_end_exclusive']-1]) for s in segments];minimum=None;count=viol=0
 for hour in m['hour'].to_dicts():
  if hour['open_ts']<m['start_ns'] or hour['available_ts']>m['end_ns']:continue
  lo=bisect.bisect_left(tb,hour['open_ts']);hi=bisect.bisect_left(ta,hour['available_ts'])
  for s in segments[lo:hi]:
   q=D(s['signed_units'])
   if not q:continue
   adverse=hour['low'] if q>0 else hour['high'];cushion=D(s['cash'])+q*(adverse-D(s['entry_price']))-D('.01')*abs(q)*adverse;minimum=cushion if minimum is None else min(minimum,cushion);count+=1;viol+=int(cushion<=0)
 return minimum,count,viol

def verify_recent(v,m,z):
 ix=m['daily_indices'];daily=v[ix].tolist();a=ix[330];tail=v[a:];t=z['recent40'];assert t['NAV_points']==len(tail) and t['NAV_sha256_f64le']==hashlib.sha256(tail.astype('<f8').tobytes()).hexdigest() and t['daily_equity_usdt']==daily[330:] and t['initial_NAV_usdt']==v[a] and t['final_NAV_usdt']==v[-1];metrics(tail,daily[330:],40,t)
 for j,f in enumerate(t['folds']):
  l,h=330+5*j,335+5*j;aa,bb=ix[[l,h]];assert f['duration_days']==5 and f['start_utc']==engine.stamp(int(m['ts'][aa])) and f['end_exclusive_utc']==engine.stamp(int(m['ts'][bb]));metrics(v[aa:bb+1],daily[l:h+1],5,f)
 assert len(t['folds'])==8 and abs(math.prod(1+f['net_return_pct']/100 for f in t['folds'])-tail[-1]/tail[0])<1e-12

def verify_qualification(c,configs):
 dimensions=axes(c);ns=[x for x in configs.values() if x['asset']==c['asset'] and x['scope']==c['scope'] and all(abs(vals.index(x[p])-vals.index(c[p]))<=1 for p,vals in dimensions.items())];frac=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);assert c['sensitivity']=={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'dimension_count':len(dimensions),'local_3x_neighbor_positive_fraction':frac};ss=c['scenes'];fullpos=sum(f['net_return_pct']>0 for f in ss['1']['folds'][:12]);recentpos=sum(f['net_return_pct']>0 for f in ss['1']['recent40']['folds']);assert c['positive_complete_30d_folds_1x']==fullpos and c['recent40_positive_5d_folds_1x']==recentpos and c['positive_folds_1x']==sum(f['net_return_pct']>0 for f in ss['1']['folds']);ratio=ss['1']['gross_reference_PnL_to_execution_cost'];margins=[z['margin']['violations'] if c['scope']=='native' else z['margin']['independent_sleeve_violations'] for z in ss.values()];expected={'positive_all_costs':all(z['net_return_pct']>0 for z in ss.values()),'nine_of_twelve_positive_complete30d_1x_folds':fullpos>=9,'recent40_positive_all_costs':all(z['recent40']['net_return_pct']>0 for z in ss.values()),'recent40_six_of_eight_positive5d_1x_folds':recentpos>=6,'composite_DD3_lte25pct':ss['3']['max_drawdown_pct']<=25,'local_positive3_gte60pct':frac>=.6,'four_round_trips1':ss['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_collateral':all(z['cash_or_units_violations']==0 for z in ss.values()),'no_order_rejections':all(z['rejected_orders']==0 for z in ss.values()),'no_margin_proxy_violations':all(v==0 for v in margins),'terminal_flat':all(D(z['terminal_units'])==0 for z in ss.values()),'minimum180days':(datetime_ns(ss['1']['folds'][-1]['end_exclusive_utc'])-datetime_ns(ss['1']['folds'][0]['start_utc']))>=180*engine.DAY};assert c['criteria']==expected and c['failed_criteria']==[k for k,v in expected.items() if not v] and (c['status']=='passed')==all(expected.values())
def datetime_ns(s):return int(__import__('datetime').datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*1e9)

def recover_from_recorded_events(m,scene,counters,multiplier):
 state={'cash':D(10000),'signed_units':D(0),'entry_price':D(0),'entry_reference':D(0)};v=np.empty(len(m['ts']));events=sorted([(int(t['axis_index']),'trade',t) for t in scene['trades']]+[(int(f['axis_index']),'fund',f) for f in scene['funding_events']]);assert len({i for i,_,_ in events})==len(events);start=0
 for idx,kind,e in events:
  v[start:idx]=float(state['cash'])+float(state['signed_units'])*(m['axis_prices'][start:idx]-float(state['entry_price']))
  if kind=='trade':
   assert e['status']=='filled' and {k:D(x) for k,x in e['state_before'].items()}==state and e['trade_ts_ns']==int(m['ts'][idx]);q=state['signed_units'];cash=state['cash'];change=D(e['change_signed_units']);ref=D(e['reference']);px=D(e['execution']);fee=D(e['cost_parts']['fee']);cost=sum(D(x) for x in e['cost_parts'].values());assert abs(change)==D(e['quantity'])
   if e['opening']:
    assert q==0;new={'cash':cash-fee,'signed_units':change,'entry_price':px,'entry_reference':ref};assert abs(change)*px<=new['cash']
   else:
    assert change==-q;near(D(e['reference_price_PnL_usdt']),q*(ref-state['entry_reference']),1e-13);new={'cash':cash+q*(px-state['entry_price'])-fee,'signed_units':D(0),'entry_price':D(0),'entry_reference':D(0)}
   assert abs(cash+q*(ref-state['entry_price'])-(new['cash']+new['signed_units']*(ref-new['entry_price']))-cost)<D('1e-18');assert {k:D(x) for k,x in e['state_after'].items()}==new;state=new;counters['source_recorded_trades_checked']+=1
  else:
   assert int(m['codes'][idx])==4 and e['settlement_ts_ns']==int(m['ts'][idx]) and D(e['signed_units'])==state['signed_units'] and D(e['cash_before'])==state['cash'];base=-state['signed_units']*D(e['mark_price'])*D(e['realized_rate']);assert base==D(e['base_amount_usdt']);amount=D(e['amount_usdt']);assert amount==(base if base>=0 else base*multiplier)
   if amount:state['cash']+=amount
   assert state['cash']==D(e['cash_after']);counters['source_recorded_funding_checked']+=1
  start=idx
 v[start:]=float(state['cash'])+float(state['signed_units'])*(m['axis_prices'][start:]-float(state['entry_price']));assert state['signed_units']==0 and {k:D(x) for k,x in scene['terminal_state'].items()}==state
 # The actual event ledger and independent saved-state encoding must produce every same point.
 n=0
 for s in scene['state_segments']:
  a,b=s['axis_start'],s['axis_end_exclusive'];assert a==n;other=float(s['cash'])+float(s['signed_units'])*(m['axis_prices'][a:b]-float(s['entry_price']));assert np.array_equal(v[a:b],other);n=b
 assert n==len(v) and hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==scene['summary']['NAV_sha256_f64le'];return v


def main():
 report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());batch=[x for x in json.loads((R/'batch.json').read_text()) if x['scope']=='native'];records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');markets={a:engine.load_market(a,x) for a,x in plan['data']['assets'].items()};assert len(batch)==27 and report['frozen_plan_sha256']==sha(R/'plan.json') and report['summary']['cost_scenarios']==324
 for m in markets.values():verify_axis(m)
 scenes=fills=funding_checks=decision_checks=metric_checks=margin_checks=recent_checks=0;vectors={}
 counters={'source_recorded_trades_checked':0,'source_recorded_funding_checked':0};source_configs={}
 for fp,ref in plan['component_sources'].items():
  assert ref['asset']=='BTC' and sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'] and records[fp]['report_sha256']==ref['report_sha256'] and records[fp]['status']==ref['original_status'];arc=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()));assert reg.fingerprint(arc['spec'])==fp;source_configs[fp]=json.loads((ROOT/ref['report']).read_text())['configs'][ref['name']]
  for k,scene in arc['scenes'].items():
   v=recover_from_recorded_events(markets['BTC'],scene,counters,int(k));assert hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==ref['NAV_sha256_by_cost'][k];vectors[fp,k]=v
 assert len(vectors)==9 and counters['source_recorded_funding_checked']==9990
 for row in batch:
  cfg=report['configs'][row['name']];arc=json.loads(gzip.decompress((ROOT/cfg['archive']).read_bytes()));spec=json.loads((ROOT/row['spec']).read_text());assert sha(ROOT/cfg['archive'])==cfg['archive_sha256'] and arc['spec']==spec and arc['fingerprint']==row['fingerprint']==reg.fingerprint(spec);reserved=[e for e in events if e['fingerprint']==row['fingerprint'] and e['status']=='reserved'];assert len(reserved)==1 and reserved[0]['recorded_at_utc']<report['evaluation_started_utc'];m=markets[row['asset']];p=spec['parameters'];assert p['fixed_entry_notional_usdt']==2000 and row['asset']=='ETH';f=m['frame'];native=m['closes'];prices=[int(x*D(10)**18) for x in native];meta=m['meta'];lot=D(meta['lot_size']);tick=D(meta['tick_size'])
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
     j=ref-1;L=p['lookback_days'];assert L in [1,2,3] and j-L>=0 and p['exit_buffer_fraction']==0;n,d=prices[j]-prices[j-L],prices[j-L];hurdle=F(str(p['return_hurdle']));wanted=-1 if n*hurdle.denominator>hurdle.numerator*d else 1 if n*hurdle.denominator < -hurdle.numerator*d else 0
     if wanted==0:
      if state['signed_units']>0 and n<0:wanted=1
      elif state['signed_units']<0 and n>0:wanted=-1
     S=p['trend_lookback_days'];assert S in [7,14,28] and S==row['trend_lookback_days'] and j-S>=0;sn,sd=prices[j]-prices[j-S],prices[j-S];allowed=1 if sn>0 else -1 if sn<0 else 0;wanted=wanted if wanted==allowed else 0;roc=F(n,d);dec=s['decisions'][di];assert F(dec['trend_return_exact'])==F(sn,sd) and dec['trend_lookback_days']==S;assert dec['decision_index']==ref and dec['execution_ts_ns']==int(m['ts'][idx]) and dec['signal_available_ts_ns']+engine.MIN==dec['execution_ts_ns'] and dec['desired_direction']==wanted and dec['fixed_entry_notional_usdt']==p['fixed_entry_notional_usdt'] and {x:D(y) for x,y in dec['state_before'].items()}==state and F(dec['lookback_return_exact'])==roc
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
  verify_qualification(cfg,grid_configs(report['configs']))
 assert scenes==81 and funding_checks==89910 and decision_checks==29970 and metric_checks==1134 and recent_checks==729
 dtype=np.dtype([('t','<i8'),('k','<i8')]);structured={}
 for a,m in markets.items():
  keys=np.empty(len(m['ts']),dtype=dtype);keys['t']=m['ts'];keys['k']=m['codes'];structured[a]=keys
 union=np.union1d(structured['BTC'],structured['ETH']);packed=(union['t']-markets['BTC']['start_ns'])*16+union['k'];assert hashlib.sha256(packed.astype('<i8').tobytes()).hexdigest()==report['parent_axis']['union_axis_sha256'];projections={}
 for a,old in structured.items():
  ix=np.searchsorted(old,union,side='right')-1;assert (ix>=0).all() and ((old[ix]['t']<union['t'])|((old[ix]['t']==union['t'])&(old[ix]['k']<=union['k']))).all() and np.array_equal(ix[np.searchsorted(union,old)],np.arange(len(old)));projections[a]=ix
 pre=np.flatnonzero(union['k']==5);assert len(pre)==370;daily_idx=np.asarray([0,*pre[1:],len(union)-1]);fold_idx=np.asarray([0,*pre[np.arange(30,370,30)],len(union)-1]);common={'daily_indices':daily_idx,'ts':union['t']};parent_scenes=0;byfp={**source_configs,**{c['fingerprint']:c for c in report['configs'].values()}}
 for row in json.loads((R/'batch.json').read_text()):
  if row['scope']!='parent':continue
  cfg=report['configs'][row['name']];arc=json.loads(gzip.decompress((ROOT/cfg['archive']).read_bytes()));spec=json.loads((ROOT/row['spec']).read_text());assert sha(ROOT/cfg['archive'])==cfg['archive_sha256'] and arc['spec']==spec and arc['fingerprint']==row['fingerprint']==reg.fingerprint(spec);p=spec['parameters'];assert p['initial_capital_usdt']==20000 and p['component_capitals_usdt']==[10000,10000] and p['raw_component_multipliers']==[1,1] and p['component_initial_entry_notionals_usdt']==[row['BTC_fixed_entry_notional_usdt'],row['ETH_fixed_entry_notional_usdt']] and sum(p['component_initial_entry_notionals_usdt'])==4000 and [x['weight'] for x in spec['components']]==[1,1]
  reserved=[e for e in events if e['fingerprint']==row['fingerprint'] and e['status']=='reserved'];assert len(reserved)==1 and reserved[0]['recorded_at_utc']<report['evaluation_started_utc'];fps=row['source_fingerprints'];assert [byfp[fp]['asset'] for fp in fps]==['BTC','ETH'] and [x['fingerprint'] for x in spec['components']]==fps and fps[0] in source_configs and byfp[fps[0]]['lookback_days']==31 and byfp[fps[0]]['return_hurdle']==.04 and byfp[fps[0]]['exit_buffer_fraction']==row['trend_exit_buffer_fraction'] and byfp[fps[1]]['scope']=='native' and byfp[fps[1]]['lookback_days']==row['reversal_lookback_days'] and byfp[fps[1]]['return_hurdle']==row['reversal_return_hurdle'] and byfp[fps[1]]['trend_lookback_days']==row['trend_filter_lookback_days']==p['ETH_trend_lookback_days'] and [byfp[fp]['fixed_entry_notional_usdt'] for fp in fps]==p['component_initial_entry_notionals_usdt']
  if records[row['fingerprint']]['status']!='reserved':assert records[row['fingerprint']]['report_sha256']==sha(R/'report.json')
  for k,s in arc['scenes'].items():
   v=vectors[fps[0],k][projections['BTC']]+vectors[fps[1],k][projections['ETH']];z=s['summary'];parts=[byfp[fp]['scenes'][k] for fp in fps];assert z==cfg['scenes'][k] and v[0]==20000 and z['initial_capital_usdt']==20000 and len(v)==z['NAV_points']==len(union) and hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==z['NAV_sha256_f64le'];assert s['source_fingerprints']==fps and s['source_full_NAV_sha256']==[x['NAV_sha256_f64le'] for x in parts];daily=v[daily_idx].tolist();assert z['daily_equity_usdt']==daily;metrics(v,daily,370,z);metric_checks+=1
   for j,(a,b) in enumerate(zip(fold_idx,fold_idx[1:])):
    l,h=j*30,min((j+1)*30,370);f=z['folds'][j];assert f['duration_days']==h-l and f['start_utc']==engine.stamp(int(union['t'][a])) and f['end_exclusive_utc']==engine.stamp(int(union['t'][b]));metrics(v[a:b+1],daily[l:h+1],h-l,f);metric_checks+=1
   assert len(z['folds'])==13 and abs(math.prod(1+f['net_return_pct']/100 for f in z['folds'])-v[-1]/20000)<1e-12;verify_recent(v,common,z);recent_checks+=9
   for field in ['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','gross_reference_price_PnL_usdt','executions','round_trips','rejected_orders','cash_or_units_violations','funding_settlements','nonzero_funding_settlements']:near(z[field],sum(x[field] for x in parts))
   assert z['funding_settlements']==2220 and all(D(x['terminal_units'])==0 for x in parts) and D(z['terminal_units'])==0;near(z['gross_reference_price_PnL_usdt']+z['funding_usdt']-z['cost_usdt'],v[-1]-20000)
   for name,val in z['cost_parts_usdt'].items():near(val,sum(x['cost_parts_usdt'][name] for x in parts))
   assert z['margin']=={'independent_sleeve_violations':sum(x['margin']['violations'] for x in parts),'minimum_individual_sleeve_cushion_usdt':min((x['margin']['minimum_equity_minus_maintenance_usdt'] for x in parts if x['margin']['minimum_equity_minus_maintenance_usdt'] is not None),default=None),'no_cross_margin_netting':True};parent_scenes+=1
  verify_qualification(cfg,grid_configs(report['configs']))
 assert parent_scenes==243 and metric_checks==4536 and recent_checks==2916 and len(report['configs'])==108
 assert all(sha(ROOT/p)==h for p,h in json.loads((R/'context.json').read_text())['account_hashes_before'].items());out={'passed':True,'actual_financial_configs':108,'new_native_components':27,'new_passive_parents':81,'native_cost_scenes_audited':scenes,'parent_cost_scenes_audited':parent_scenes,'cost_scenes_audited':324,'full_NAV_points_per_scene':545013,'full_NAV_points_audited':545013*324,'independent_overall_and_fold_metric_checks':metric_checks,'independent_recent40_and_fold_metric_checks':recent_checks,'causal_daily_decisions_checked':decision_checks,'actual_fills_independently_verified':fills,'actual_funding_settlements_verified_including_flat':funding_checks,'independent_state_hour_margin_checks':margin_checks,'contrarian_and_slow_ROC_integer_cross_products_independently_verified':True,'slow_regime_compatibility_cash_exit_and_no_hidden_position_verified':True,'zero_sign_exit_opposite_extreme_priority_and_native_sizing_verified':True,'funding_rates_not_used_for_signal_or_quantity':True,'parent_structured_ns_keys_and_raw1_1_20000_sum_verified':True,'source_native_BTC_configs_reused':3,'source_native_cost_NAVs_recovered':9,**counters,'old_source_results_not_recalculated_or_rerated':True,'protected_inputs_unchanged':True,'report_sha256':sha(R/'report.json')};put(R/'verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
