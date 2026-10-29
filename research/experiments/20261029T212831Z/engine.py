"""Short-horizon contrarian ROC with zero-cross exit; native accounting retained."""
import copy,hashlib,json,math,statistics
from datetime import datetime,timezone
from decimal import Decimal as D,ROUND_FLOOR,ROUND_CEILING
from fractions import Fraction as F
from pathlib import Path
import numpy as np,polars as pl
ROOT=Path(__file__).resolve().parents[3];MIN=60000000000;HOUR=60*MIN;DAY=24*HOUR
START,END,DAYS=33,403,370;CAPITAL=D(10000);NOTIONAL=D(2000)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
navhash=lambda v:hashlib.sha256(v.astype('<f8',copy=False).tobytes()).hexdigest()
stamp=lambda t:datetime.fromtimestamp(t/1e9,timezone.utc).isoformat().replace('+00:00','Z')

def target(values,i,look,hurdle,current_direction=0,exit_buffer_fraction=0,trend_lookback_days=7):
 assert look in [1,2,3,4,5,6,7] and trend_lookback_days in [7,14,21,22,25,26,27,28,29,30,31] and i-1-trend_lookback_days>=0 and exit_buffer_fraction==0 and current_direction in [-1,0,1]
 r=F(values[i-1])/F(values[i-1-look])-1;h=F(str(hurdle));slow=F(values[i-1])/F(values[i-1-trend_lookback_days])-1;assert 0<h<1
 desired=-1 if r>h else 1 if r < -h else (1 if current_direction==1 and r<0 else -1 if current_direction==-1 and r>0 else 0)
 # No hidden desired direction. Losing/flat slow regime flattens an actual position.
 allowed=1 if slow>0 else -1 if slow<0 else 0
 return desired if desired==allowed else 0,str(r),str(slow)

def majority_target(values,i,look,hurdle,current_direction=0,exit_buffer_fraction=0,trend_lookback_days=28,trend_gate_application='entries_and_retention'):
 assert look in [2,3,4,5] and trend_lookback_days in [27,28,29,30,31] and i-2-trend_lookback_days>=0 and abs(F(str(exit_buffer_fraction)))<F(str(hurdle)) and current_direction in [-1,0,1]
 j=i-1;r=F(values[j])/F(values[j-look])-1;h=F(str(hurdle));e=F(str(exit_buffer_fraction));assert 0<h<1 and (e==0 or trend_gate_application=='entries_only')
 slow=sorted(F(values[j])/F(values[j-n])-1 for n in [trend_lookback_days-1,trend_lookback_days,trend_lookback_days+1])[1]
 desired=-1 if r>h else 1 if r < -h else (1 if current_direction==1 and r<e else -1 if current_direction==-1 and r> -e else 0)
 allowed=1 if slow>0 else -1 if slow<0 else 0
 assert trend_gate_application in ['entries_only','entries_and_retention']
 if trend_gate_application=='entries_only' and current_direction and desired==current_direction:return desired,str(r),str(slow)
 return desired if desired==allowed else 0,str(r),str(slow)

def funding_amount(q,mark,rate,m):
 base=-q*mark*rate;return base,base*m if base<0 else base

def trade(state,change,ref,adv,sigma,meta,m,opening):
 """Notional is never debited from collateral;only fee and realized linear PnL."""
 cash,q,entry,entryref=[D(state[k]) for k in ['cash','signed_units','entry_price','entry_reference']];change=D(change);quantity=abs(change);buy=change>0;participation=quantity*ref/adv
 assert quantity>0 and ref>0 and adv>0 and sigma>=0 and ((q==0) if opening else change==-q)
 record={'change_signed_units':str(change),'quantity':str(quantity),'side':'buy' if buy else 'sell','opening':opening,'reference':str(ref),'lagged_ADV':str(adv),'lagged_sigma':str(sigma),'participation':str(participation),'cost_multiplier':m,'state_before':copy.deepcopy(state)}
 def reject(reason):return state,{**record,'status':'rejected','reason':reason,'state_after':copy.deepcopy(state)}
 if participation>D('.001'):return reject('participation')
 fee,spread,slip=D('.0005')*m,D('.0001')*m,D('.0002')*m;impact=D('.5')*sigma*participation.sqrt()*m;theoretical=ref*(1+(spread+slip+impact)*(1 if buy else -1));tick=D(meta['tick_size']);lot=D(meta['lot_size']);price=(theoretical/tick).to_integral_value(rounding=ROUND_CEILING if buy else ROUND_FLOOR)*tick
 if quantity%lot or quantity*price<D(meta['min_notional']):return reject('lot_or_min_notional')
 fee_usdt=quantity*price*fee;realized=D(0) if opening else q*(price-entry);cash2=cash+realized-fee_usdt;q2=change if opening else D(0);entry2=price if opening else D(0);ref2=ref if opening else D(0)
 if opening and quantity*price>cash2:return reject('fully_collateralized_1x_entry_cap')
 parts={'fee':fee_usdt,'half_spread':quantity*ref*spread,'slippage':quantity*ref*slip,'impact':quantity*ref*impact,'tick_rounding':quantity*abs(price-theoretical)};cost=sum(parts.values());new={'cash':str(cash2),'signed_units':str(q2),'entry_price':str(entry2),'entry_reference':str(ref2)}
 assert abs(cash+q*(ref-entry)-(cash2+q2*(ref-entry2))-cost)<D('1e-18')
 return new,{**record,'status':'filled','execution':str(price),'theoretical_execution':str(theoretical),'fee_rate':str(fee),'half_spread_rate':str(spread),'slippage_rate':str(slip),'impact_rate':str(impact),'realized_price_PnL_usdt':str(realized),'reference_price_PnL_usdt':str(D(0) if opening else q*(ref-entryref)),'cost_parts':{k:str(v) for k,v in parts.items()},'cost_usdt':str(cost),'state_after':copy.deepcopy(new)}

def load_market(asset,files):
 frames={}
 for x in files:
  p=ROOT/x['path'];assert sha(p)==x['sha256'] and p.stat().st_size==x['bytes'];frames[p.stem]=pl.read_parquet(p)
 f,h,fu=frames['perp_bars'],frames['mark_hour_bars'],frames['funding_settlement'];meta=frames['perp_instrument_meta'].to_dicts()[0];assert meta['contract_multiplier']==1
 assert f.height==581760 and f['is_closed'].all() and (f['open_ts'].diff().drop_nulls()==MIN).all() and (f['available_ts']-f['open_ts']==MIN).all();assert h.height==9696 and h['is_closed'].all() and (h['available_ts']-h['open_ts']==HOUR).all() and (h['open_ts'].diff().drop_nulls()==HOUR).all()
 assert (f['open']>0).all() and (f['close']>0).all() and (f['quote_volume']>=0).all() and (h['low']>0).all() and (h['high']>=h['low']).all();daily=f.with_columns((pl.col('open_ts')//DAY).alias('day')).group_by('day',maintain_order=True).agg(pl.col('close').last().alias('close'),pl.col('quote_volume').sum().alias('quote_volume'),pl.len().alias('bars')).sort('day');assert daily.height==404 and (daily['bars']==1440).all();rows=daily.to_dicts();prices=[x['close'] for x in rows];first=int(f['open_ts'][0]);S=first+START*DAY+MIN;E=first+END*DAY+MIN;assert stamp(S)=='2025-10-19T00:01:00Z' and stamp(E)=='2026-10-24T00:01:00Z'
 funds=fu.to_dicts();assert len(funds)==1212 and all(x['available_ts']>=x['settlement_ts'] and x['mark_price_at_settlement']>0 and x['actual_interval_hours']>0 for x in funds);funds=[{**x,'source_index':j} for j,x in enumerate(funds) if S<x['settlement_ts']<=E];assert len(funds)==1110
 parts=[]
 def add(ts,code,px,refs):
  ts=np.atleast_1d(np.asarray(ts,dtype=np.int64));n=len(ts);parts.append((ts,np.full(n,code,dtype=np.int8),np.atleast_1d(np.asarray(px,dtype=np.float64)),np.atleast_1d(np.asarray(refs,dtype=np.int32))));assert all(len(x)==n for x in parts[-1])
 lo,hi=START*1440+1,END*1440+1;add(S,0,float(f['open'][lo]),-1);add(np.asarray(f['available_ts'][lo:hi]),1,[float(x) for x in f['close'][lo:hi]],np.arange(lo,hi));hs=[j for j,x in enumerate(h['available_ts']) if S<int(x)<=E];add([int(h['available_ts'][j]) for j in hs],2,[float(h['close'][j]) for j in hs],hs)
 for code in [3,4]:add([x['settlement_ts'] for x in funds],code,[float(x['mark_price_at_settlement']) for x in funds],np.arange(len(funds)))
 for code in [5,6,7]:add([first+i*DAY+MIN for i in range(START,END)],code,[float(f['open'][i*1440+1]) for i in range(START,END)],np.arange(START,END))
 for code in [8,9]:add(E,code,float(f['open'][hi]),END)
 ts,codes,px,refs=[np.concatenate([x[j] for x in parts]) for j in range(4)];order=np.lexsort((codes,ts));ts,codes,px,refs=[x[order] for x in [ts,codes,px,refs]];pre=np.flatnonzero(codes==5);assert len(pre)==DAYS and len(ts)==545013 and np.all(np.diff(ts)>=0);axis_sha=hashlib.sha256(ts.astype('<i8').tobytes()+codes.tobytes()+refs.astype('<i4').tobytes()).hexdigest();controls=np.flatnonzero(np.isin(codes,[4,6,7,9]));daily_idx=np.asarray([0,*pre[1:],len(ts)-1],dtype=int);bounds=np.asarray([0,*pre[np.arange(30,DAYS,30)],len(ts)-1],dtype=int)
 cost_inputs={}
 for i in range(START,END+1):
  adv=statistics.mean(float(x['quote_volume']) for x in rows[i-20:i]);rr=[math.log(float(prices[j])/float(prices[j-1])) for j in range(i-20,i)];cost_inputs[i]=(D(str(adv)),D(str(statistics.stdev(rr))))
 return {'asset':asset,'frame':f,'hour':h,'funds':funds,'meta':meta,'rows':rows,'closes':prices,'ts':ts,'codes':codes,'axis_prices':px,'refs':refs,'controls':controls,'daily_indices':daily_idx,'fold_indices':bounds,'cost_inputs':cost_inputs,'start_ns':S,'end_ns':E,'axis_sha256':axis_sha,'axis_price_sha256_f64le':navhash(px)}

def margin_audit(m,segments):
 h=m['hour'];opens=np.asarray(h['open_ts']);ends=np.asarray(h['available_ts']);low=np.asarray([float(x) for x in h['low']]);high=np.asarray([float(x) for x in h['high']]);minimum=float('inf');count=violations=0;eligible=(opens>=m['start_ns'])&(ends<=m['end_ns'])
 for s in segments:
  q=float(s['signed_units'])
  if not q:continue
  a=int(m['ts'][s['axis_start']]);b=int(m['ts'][s['axis_end_exclusive']-1]);ix=np.flatnonzero(eligible&(opens<=b)&(ends>a))
  if not len(ix):continue
  adverse=low[ix] if q>0 else high[ix];cushion=float(s['cash'])+q*(adverse-float(s['entry_price']))-.01*abs(q)*adverse;minimum=min(minimum,float(cushion.min()));count+=len(ix);violations+=int((cushion<=0).sum())
 return {'maintenance_margin_rate_proxy':.01,'state_hour_extreme_bounding_checks':count,'minimum_equity_minus_maintenance_usdt':minimum if count else None,'violations':violations,'scope':'Conservative full-hour adverse high/low applied to every state overlapping each fully in-OOS closed mark hour;states may overlap same hour. Partial first/last hours lack full mark extrema;no true tick-liquidation guarantee.'}

def stats(v,daily,days):
 ret=100*(v[-1]/v[0]-1);dd=100*float(np.max(1-v/np.maximum.accumulate(v)));rr=[b/a-1 for a,b in zip(daily,daily[1:])];sd=statistics.stdev(rr);cagr=100*((v[-1]/v[0])**(365/days)-1)
 return {'net_return_pct':float(ret),'max_drawdown_pct':dd,'daily_mark_drawdown_pct':100*float(np.max(1-np.asarray(daily)/np.maximum.accumulate(daily))),'sharpe_365':statistics.mean(rr)/sd*math.sqrt(365) if sd else None,'cagr_pct':float(cagr),'calmar':float(cagr/dd) if dd else None}

def summary(m,v,trades,funding,segments):
 daily=v[m['daily_indices']].tolist();s=stats(v,daily,DAYS);s['folds']=[]
 for j,(a,b) in enumerate(zip(m['fold_indices'],m['fold_indices'][1:])):s['folds'].append({'fold':j+1,'start_utc':stamp(m['start_ns']+j*30*DAY),'end_exclusive_utc':stamp(m['start_ns']+min((j+1)*30,DAYS)*DAY),'duration_days':min(30,DAYS-j*30),**stats(v[a:b+1],daily[j*30:min((j+1)*30,DAYS)+1],min(30,DAYS-j*30))})
 filled=[x for x in trades if x['status']=='filled'];parts={k:float(sum(D(t['cost_parts'][k]) for t in filled)) for k in ['fee','half_spread','slippage','impact','tick_rounding']};cost=sum(parts.values());fund=sum(D(x['amount_usdt']) for x in funding);basefund=sum(D(x['base_amount_usdt']) for x in funding);gross=sum(D(t['reference_price_PnL_usdt']) for t in filled);assert abs(float(gross+fund)-cost-(v[-1]-10000))<1e-8;assert abs(math.prod(1+f['net_return_pct']/100 for f in s['folds'])-v[-1]/v[0])<1e-12
 mark=np.isin(m['codes'],[0,2,3,4,9]);mv=v[mark];minute=np.isin(m['codes'],[0,1,3,4,5,6,7,8,9]);pv=v[minute];margin=margin_audit(m,segments)
 s.update(initial_capital_usdt=10000,final_NAV_usdt=float(v[-1]),cost_usdt=cost,cost_pct_initial=cost/100,cost_parts_usdt=parts,funding_usdt=float(fund),base_funding_same_exposure_usdt=float(basefund),funding_stress_increment_usdt=float(fund-basefund),funding_income_usdt=float(sum(D(x['amount_usdt']) for x in funding if D(x['amount_usdt'])>0)),funding_outflow_usdt=float(-sum(D(x['amount_usdt']) for x in funding if D(x['amount_usdt'])<0)),gross_reference_price_PnL_usdt=float(gross),gross_reference_PnL_to_execution_cost=float((gross+fund)/D(str(cost))) if cost else None,executions=len(filled),round_trips=sum(not t['opening'] for t in filled),rejected_orders=len(trades)-len(filled),cash_or_units_violations=sum(D(x['cash'])<0 for x in segments),terminal_units=segments[-1]['signed_units'],daily_equity_usdt=daily,NAV_points=len(v),NAV_sha256_f64le=navhash(v),axis_sha256=m['axis_sha256'],axis_prices_sha256_f64le=m['axis_price_sha256_f64le'],mark_observation_drawdown_pct=100*float(np.max(1-mv/np.maximum.accumulate(mv))),trade_proxy_drawdown_pct=100*float(np.max(1-pv/np.maximum.accumulate(pv))),margin=margin,funding_settlements=len(funding),nonzero_funding_settlements=sum(D(x['signed_units'])!=0 for x in funding));return s

def funding_entry_gate(parameters,m,decision_index,base_direction,signed_units):
 if 'entry_funding_lookback_settlements' not in parameters:return base_direction,{'enabled':False}
 n=parameters['entry_funding_lookback_settlements'];cap=F(str(parameters['entry_funding_cost_cap_per_settlement']));assert n in [3,6,9] and cap in [F(0),F('0.00005'),F('0.0001')] and parameters['entry_funding_application']=='new_and_reversal_entries_only' and parameters['entry_funding_max_age_hours']==16
 signal_ts=int(m['frame']['available_ts'][decision_index*1440-1]);known=sorted((x for x in m['funding_feature_history'] if x['available_ts']<=signal_ts and x['settlement_ts']<=signal_ts),key=lambda x:(x['settlement_ts'],x['source_index']));chosen=known[-n:];enough=len(chosen)==n;mean=sum((F(x['realized_rate']) for x in chosen),F(0))/n if enough else None;fresh=enough and signal_ts-max(x['available_ts'] for x in chosen)<=16*HOUR;actual=1 if signed_units>0 else -1 if signed_units<0 else 0;entry=bool(base_direction and (not actual or base_direction!=actual));cost=base_direction*mean if mean is not None and base_direction else F(0);allowed=bool(enough and fresh and cost<=cap);final=base_direction if not entry or allowed else 0
 audit={'enabled':True,'signal_available_ts_ns':signal_ts,'lookback_settlements':n,'cost_cap_exact':str(cap),'source_indices':[x['source_index'] for x in chosen],'settlement_ts_ns':[x['settlement_ts'] for x in chosen],'available_ts_ns':[x['available_ts'] for x in chosen],'realized_rates':[str(x['realized_rate']) for x in chosen],'mean_realized_rate_exact':str(mean) if mean is not None else None,'directional_cost_exact':str(cost),'complete_history':enough,'fresh_16h':fresh,'applied_to_new_or_reversal_entry':entry,'entry_cost_allowed':allowed,'base_direction':base_direction,'actual_direction':actual,'final_direction':final,'stress_does_not_change_signal':True}
 return final,audit

def simulate(spec,m,mult):
 p=spec['parameters'];assert p.get('trend_gate_mode') in [None,'adjacent_horizon_majority'];notional=D(str(p['fixed_entry_notional_usdt']));assert 0<notional<=CAPITAL;state={'cash':'10000','signed_units':'0','entry_price':'0','entry_reference':'0'};v=np.empty(len(m['ts']));segments=[];trades=[];funds=[];decisions=[];start=0;segment_start=0;segment_state=copy.deepcopy(state);wanted=0
 def execute(i,change,opening,axis_index,terminal=False):
  nonlocal state
  adv,sigma=m['cost_inputs'][i];state,t=trade(state,change,m['frame']['open'][i*1440+1],adv,sigma,m['meta'],mult,opening);t.update(decision_index=i,trade_ts_ns=int(m['ts'][axis_index]),axis_index=int(axis_index),terminal=terminal,asset=m['asset']);trades.append(t)
 for idx in m['controls']:
  idx=int(idx);cash,q,entry=[float(state[k]) for k in ['cash','signed_units','entry_price']];v[start:idx]=cash+q*(m['axis_prices'][start:idx]-entry);code=int(m['codes'][idx]);ref=int(m['refs'][idx]);before=copy.deepcopy(state)
  if code==4:
   e=m['funds'][ref];base,amount=funding_amount(D(state['signed_units']),e['mark_price_at_settlement'],e['realized_rate'],mult);cb=D(state['cash'])
   if amount:state['cash']=str(cb+amount)
   funds.append({'source_index':e['source_index'],'settlement_ts_ns':e['settlement_ts'],'available_ts_ns':e['available_ts'],'realized_rate':str(e['realized_rate']),'mark_price':str(e['mark_price_at_settlement']),'actual_interval_hours':str(e['actual_interval_hours']),'signed_units':state['signed_units'],'base_amount_usdt':str(base),'amount_usdt':str(amount),'cash_before':str(cb),'cash_after':state['cash'],'axis_index':idx})
  elif code==6:
   target_fn=majority_target if p.get('trend_gate_mode')=='adjacent_horizon_majority' else target
   wanted,r,slow_r=(1,None,None) if p.get('signal_mode')=='constant_long_reference' else target_fn(m['closes'],ref,p['lookback_days'],p['return_hurdle'],1 if D(state['signed_units'])>0 else -1 if D(state['signed_units'])<0 else 0,p['exit_buffer_fraction'],p['trend_lookback_days'],**({'trend_gate_application':p.get('trend_gate_application','entries_and_retention')} if p.get('trend_gate_mode')=='adjacent_horizon_majority' else {}));q=D(state['signed_units']);base_wanted=wanted;wanted,funding_gate_audit=funding_entry_gate(p,m,ref,base_wanted,q);decisions.append({'decision_index':ref,'signal_available_ts_ns':int(m['frame']['available_ts'][ref*1440-1]),'execution_ts_ns':int(m['ts'][idx]),'lookback_return_exact':r,'trend_return_exact':slow_r,'trend_lookback_days':p['trend_lookback_days'],'desired_direction':wanted,'fixed_entry_notional_usdt':float(notional),'state_before':copy.deepcopy(state)})
   decisions[-1].update(entry_funding_gate=funding_gate_audit,base_desired_direction=base_wanted)
   if p.get('trend_gate_mode')=='adjacent_horizon_majority':
    horizons=[p['trend_lookback_days']-1,p['trend_lookback_days'],p['trend_lookback_days']+1];assert p['trend_gate_lookbacks_days']==horizons
    returns=[F(m['closes'][ref-1])/F(m['closes'][ref-1-n])-1 for n in horizons];decisions[-1].update(trend_gate_mode=p['trend_gate_mode'],trend_gate_lookbacks_days=horizons,trend_horizon_returns_exact=[str(x) for x in returns],trend_horizon_signs=[1 if x>0 else -1 if x<0 else 0 for x in returns],trend_gate_application=p.get('trend_gate_application','entries_and_retention'))
   if q and (1 if q>0 else -1)!=wanted:execute(ref,-q,False,idx)
  elif code==7:
   if wanted and D(state['signed_units'])==0:
    lot=D(m['meta']['lot_size']);quantity=(notional/m['closes'][ref-1]/lot).to_integral_value(rounding=ROUND_FLOOR)*lot;execute(ref,D(wanted)*quantity,True,idx)
   decisions[-1]['state_after']=copy.deepcopy(state)
  elif code==9:
   if D(state['signed_units']):execute(END,-D(state['signed_units']),False,idx,True)
  if state!=before:
   if idx>segment_start:segments.append({'axis_start':segment_start,'axis_end_exclusive':idx,**segment_state})
   segment_start=idx;segment_state=copy.deepcopy(state)
  start=idx
 cash,q,entry=[float(state[k]) for k in ['cash','signed_units','entry_price']];v[start:]=cash+q*(m['axis_prices'][start:]-entry);segments.append({'axis_start':segment_start,'axis_end_exclusive':len(v),**segment_state});assert D(state['signed_units'])==0 and len(decisions)==DAYS and (v>0).all() and np.isfinite(v).all()
 return v,{'decisions':decisions,'trades':trades,'funding_events':funds,'state_segments':segments,'terminal_state':state,'summary':summary(m,v,trades,funds,segments)}
