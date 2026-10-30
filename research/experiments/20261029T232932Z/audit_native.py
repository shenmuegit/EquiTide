"""Independent integer signals, Decimal fills, funding, risk and every NAV point for12newETHslowgatepaths."""
import copy,gzip,hashlib,json,math,statistics
from decimal import Decimal as D,ROUND_CEILING,ROUND_FLOOR
from fractions import Fraction as F
import numpy as np
import engine
from run import ROOT,R,sha,reg,grid_configs
from audit_helpers import near,metrics,independent_margin,verify_recent,qualification

def verify(report,plan,markets,events,records):
 batch=[x for x in json.loads((R/'batch.json').read_text()) if x['scope']=='native'];assert len(batch)==21
 feature_file=next(x for x in plan['data']['assets']['ETH'] if x['path'].endswith('/funding_settlement.parquet'));assert sha(ROOT/feature_file['path'])==feature_file['sha256'];full_feature_history=[{**x,'source_index':j} for j,x in enumerate(engine.pl.read_parquet(ROOT/feature_file['path']).to_dicts())];assert len(full_feature_history)==1212 and [x for x in full_feature_history if markets['ETH']['start_ns']<x['settlement_ts']<=markets['ETH']['end_ns']]==markets['ETH']['funds']
 scenes=fills=funding_checks=decision_checks=metric_checks=margin_checks=recent_checks=0;vectors={};feature_records=blocked_entries=retention_exempt=0
 for row in batch:
  cfg=report['configs'][row['name']];arc=json.loads(gzip.decompress((ROOT/cfg['archive']).read_bytes()));spec=json.loads((ROOT/row['spec']).read_text());assert sha(ROOT/cfg['archive'])==cfg['archive_sha256'] and arc['spec']==spec and arc['fingerprint']==row['fingerprint']==reg.fingerprint(spec);reserved=[e for e in events if e['fingerprint']==row['fingerprint'] and e['status']=='reserved'];assert len(reserved)==1 and max(x['recorded_at_utc'] for x in reserved)<report['evaluation_started_utc'];m=markets[row['asset']];p=spec['parameters'];capital=D(str(row['capital_usdt']));assert spec['universe']==[row['asset']+'/USDT'];assert p['initial_capital_usdt']==float(capital) and p['fixed_entry_notional_usdt']==row['fixed_entry_notional_usdt'] and p['raw_entry_notional_fraction_of_initial_capital']==p['fixed_entry_notional_usdt']/float(capital);f=m['frame'];native=m['closes'];prices=[int(x*D(10)**18) for x in native];meta=m['meta'];lot=D(meta['lot_size']);tick=D(meta['tick_size'])
  if records[row['fingerprint']]['status']!='reserved':assert records[row['fingerprint']]['report_sha256']==sha(R/'report.json')
  for k,s in arc['scenes'].items():
   mult=int(k);state={x:D(v) for x,v in {'cash':str(capital),'signed_units':'0','entry_price':'0','entry_reference':'0'}.items()};v=np.empty(len(m['ts']));start=0;ti=fi=di=0;expected_segments=[];segstart=0;segstate=copy.deepcopy(state);wanted=0
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
     j=ref-1;actual=1 if state['signed_units']>0 else -1 if state['signed_units']<0 else 0;constant=p.get('signal_mode')=='constant_long_reference';roc=None;slow=None;feature={'enabled':False}
     if constant:wanted=1
     else:
      L=p['lookback_days'];roc=F(prices[j]-prices[j-L],prices[j-L]);h=F(str(p['return_hurdle']));e=F(str(p['exit_buffer_fraction']))
      if row['asset']=='BTC':
       assert L==31 and h==F('.04') and e==F('.01');wanted=1 if roc>h else -1 if roc<-h else 1 if actual==1 and roc>-e else -1 if actual==-1 and roc<e else 0
      else:
       assert L==3 and h==F('.025') and e==F('-.01') and p['trend_lookback_days']==28 and p['trend_gate_application']=='entries_only';wanted=-1 if roc>h else 1 if roc<-h else 1 if actual==1 and roc<e else -1 if actual==-1 and roc>-e else 0;hs=[27,28,29];rs=[F(prices[j]-prices[j-h0],prices[j-h0]) for h0 in hs];signs=[1 if r>0 else -1 if r<0 else 0 for r in rs];slow=sorted(rs)[1];allowed=1 if signs.count(1)>=2 else -1 if signs.count(-1)>=2 else 0;wanted=wanted if actual and wanted==actual else wanted if wanted==allowed else 0
     base_wanted=wanted
     if 'entry_funding_lookback_settlements' in p:
      assert row['asset']=='ETH' and row['role']=='candidate' and p['entry_funding_lookback_settlements']==6;signal_time=int(f['available_ts'][ref*1440-1]);NF=6;cap=F(str(p['entry_funding_cost_cap_per_settlement']));candidates=[e for e in full_feature_history if e['settlement_ts']<=signal_time and e['available_ts']<=signal_time];candidates.sort(key=lambda e:(e['settlement_ts'],e['source_index']));chosen=candidates[-NF:];assert len(chosen)==NF and signal_time-max(e['available_ts'] for e in chosen)<=16*engine.HOUR;mean=sum(F(e['realized_rate']) for e in chosen)/NF;directional=base_wanted*mean if base_wanted else F(0);entry=bool(base_wanted and (actual==0 or base_wanted!=actual));permit=directional<=cap;wanted=base_wanted if not entry or permit else 0;feature_records+=NF;blocked_entries+=int(entry and not permit);retention_exempt+=int(not entry and actual!=0 and base_wanted==actual and not permit)
      feature={'enabled':True,'signal_available_ts_ns':signal_time,'lookback_settlements':NF,'cost_cap_exact':str(cap),'source_indices':[e['source_index'] for e in chosen],'settlement_ts_ns':[e['settlement_ts'] for e in chosen],'available_ts_ns':[e['available_ts'] for e in chosen],'realized_rates':[str(e['realized_rate']) for e in chosen],'mean_realized_rate_exact':str(mean),'directional_cost_exact':str(directional),'complete_history':True,'fresh_16h':True,'applied_to_new_or_reversal_entry':entry,'entry_cost_allowed':permit,'base_direction':base_wanted,'actual_direction':actual,'final_direction':wanted,'stress_does_not_change_signal':True}
     dec=s['decisions'][di];assert dec['decision_index']==ref and dec['execution_ts_ns']==int(m['ts'][idx]) and dec['signal_available_ts_ns']+engine.MIN==dec['execution_ts_ns'] and dec['desired_direction']==wanted and dec['fixed_entry_notional_usdt']==p['fixed_entry_notional_usdt'] and {x:D(y) for x,y in dec['state_before'].items()}==state and dec['lookback_return_exact']==(None if roc is None else str(roc))
     if row['asset']=='ETH':
      assert dec['base_desired_direction']==base_wanted and dec['entry_funding_gate']==feature and dec['trend_return_exact']==(None if slow is None else str(slow))
      if not constant:assert dec['trend_gate_lookbacks_days']==[27,28,29] and dec['trend_horizon_returns_exact']==[str(r) for r in rs] and dec['trend_horizon_signs']==signs and dec['trend_gate_application']=='entries_only'
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
   z=s['summary'];near(z['initial_capital_usdt'],capital);near(z['cost_pct_initial'],z['cost_usdt']/float(capital)*100);assert z==cfg['scenes'][k] and hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==z['NAV_sha256_f64le'] and z['NAV_points']==len(v)==545013 and (v>0).all();daily=v[m['daily_indices']].tolist();assert daily==z['daily_equity_usdt'];metrics(v,daily,370,z);metric_checks+=1
   for j,(a,b) in enumerate(zip(m['fold_indices'],m['fold_indices'][1:])):metrics(v[a:b+1],daily[j*30:min((j+1)*30,370)+1],min(30,370-j*30),z['folds'][j]);metric_checks+=1
   assert len(z['folds'])==13 and [f['duration_days'] for f in z['folds']]==[30]*12+[10] and abs(math.prod(1+x['net_return_pct']/100 for x in z['folds'])-v[-1]/float(capital))<1e-12
   gross=sum(D(t['reference_price_PnL_usdt']) for t in s['trades']);fund=sum(D(t['amount_usdt']) for t in s['funding_events']);basefund=sum(D(t['base_amount_usdt']) for t in s['funding_events']);cost=sum(sum(D(x) for x in t['cost_parts'].values()) for t in s['trades']);near(gross,z['gross_reference_price_PnL_usdt']);near(fund,z['funding_usdt']);near(basefund,z['base_funding_same_exposure_usdt']);near(fund-basefund,z['funding_stress_increment_usdt']);near(sum(D(t['amount_usdt']) for t in s['funding_events'] if D(t['amount_usdt'])>0),z['funding_income_usdt']);near(-sum(D(t['amount_usdt']) for t in s['funding_events'] if D(t['amount_usdt'])<0),z['funding_outflow_usdt']);near(cost,z['cost_usdt']);near(gross+fund-cost,D(str(v[-1]))-capital);assert z['executions']==len(s['trades']) and z['round_trips']==sum(not t['opening'] for t in s['trades']) and z['rejected_orders']==z['cash_or_units_violations']==0
   for mask,field in [(np.isin(m['codes'],[0,2,3,4,9]),'mark_observation_drawdown_pct'),(np.isin(m['codes'],[0,1,3,4,5,6,7,8,9]),'trade_proxy_drawdown_pct')]:
    vv=v[mask];near(100*np.max(1-vv/np.maximum.accumulate(vv)),z[field]);assert z[field]<=z['max_drawdown_pct']+1e-10
   minimum,count,viol=independent_margin(m,s['state_segments']);assert count==z['margin']['state_hour_extreme_bounding_checks'] and viol==z['margin']['violations']
   if count:near(minimum,z['margin']['minimum_equity_minus_maintenance_usdt'],1e-10)
   margin_checks+=count;scenes+=1;vectors[row['fingerprint'],k]=v;verify_recent(v,m,z);recent_checks+=9
  if cfg['role']=='candidate':qualification(cfg,grid_configs(report['configs']))
  else:assert cfg['status']=='rejected' and cfg['criteria']=={'reference_or_fixed_BTC_execution_component_only':False}
 assert scenes==63 and funding_checks==69930 and decision_checks==23310 and metric_checks==882 and recent_checks==567 and feature_records==59940
 return vectors,{'funding_feature_decisions_checked':9990,'available_funding_feature_records_independently_checked':feature_records,'new_entries_blocked_by_funding':blocked_entries,'actual_compatible_position_retention_exemptions':retention_exempt,'native_cost_scenes_audited':scenes,'actual_fills_independently_verified':fills,'actual_funding_settlements_verified_including_flat':funding_checks,'causal_daily_decisions_checked':decision_checks,'native_metric_checks':metric_checks,'native_recent_metric_checks':recent_checks,'independent_state_hour_margin_checks':margin_checks}
