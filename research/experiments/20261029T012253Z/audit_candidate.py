"""Read-only independent cross-day signals, Decimal executions, funding, risk and complete NAV audit."""
import copy,gzip,hashlib,json,math,statistics,sys,urllib.parse
from collections import defaultdict
from decimal import Decimal as D,ROUND_CEILING,ROUND_FLOOR
from fractions import Fraction as F
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;W=R/'candidate_observation';SRC=ROOT/'research/experiments/20261026T110637Z';sys.path.insert(0,str(SRC));import prospective_core as c
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
read=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def near(a,b):assert abs(float(a)-float(b))<=1e-11*max(1,abs(float(a)),abs(float(b))),(a,b)
def main():
 point=read(ROOT/'research/automation/candidate_forward_latest.json');previous=read(W/'previous_pointer.json');before=read(ROOT/previous['state']);state=read(W/'state.json');rep=read(W/'report.json');delta=gz(W/'delta.json.gz');im=read(W/'input_manifest.json');complete=read(W/'complete.json');binding=c.bindings();guard={str(p):sha(p) for p in [W/'state.json',W/'report.json',W/'delta.json.gz',W/'complete.json',W/'previous_pointer.json',ROOT/'research/automation/candidate_forward_latest.json']}
 assert point['previous_pointer']=={'path':str((W/'previous_pointer.json').relative_to(ROOT)),'sha256':sha(W/'previous_pointer.json')} and complete['previous_pointer_sha256']==hashlib.sha256(c.canonical(previous)).hexdigest()
 for key,file in [('state','state.json'),('report','report.json'),('delta','delta.json.gz'),('complete','complete.json')]:assert point[key]==str((W/file).relative_to(ROOT)) and point[key+'_sha256']==sha(W/file)
 for key in ['state','report','delta','complete']:assert sha(ROOT/previous[key])==previous[key+'_sha256']
 assert sha(ROOT/im['packet'])==im['sha256'];packet=gz(ROOT/im['packet']);lo,cut,actions,contexts=c.normalize(packet,before,binding);assert lo==c.ns('2026-10-28T22:30:00Z') and cut==c.ns('2026-10-29T00:30:00Z')==state['cutoff_ns'] and state['context']==contexts
 rawby=defaultdict(list)
 for item in im['provenance']:
  assert item['http_status']==200 and item['curl_exit_code']==0 and sha(ROOT/item['raw'])==item['sha256'];raw=gzip.decompress((ROOT/item['raw']).read_bytes());assert len(raw)==item['bytes'];data=json.loads(raw);u=urllib.parse.urlparse(item['url']);q=urllib.parse.parse_qs(u.query)
  if u.path in ['/fapi/v1/klines','/fapi/v1/markPriceKlines','/fapi/v1/fundingRate']:rawby[q['symbol'][0][:-4],u.path].extend(data)
 for a in ['BTC','ETH']:
  pa=packet['assets'][a];assert rawby[a,'/fapi/v1/klines']==pa['minutes'] and rawby[a,'/fapi/v1/markPriceKlines']==pa['hours'] and rawby[a,'/fapi/v1/fundingRate']==pa['funding'] and len(pa['minutes'])==122
  # Independent minute-to-day accumulation, retaining exact previous partial-day volume.
  cx=copy.deepcopy(before['context'][a]);assert pa['minutes'][0]==cx['last_bar'] and pa['minutes'][1]==cx['reference_bar']
  for bar in pa['minutes'][1:-1]:
   t=int(bar[0])*c.MS;end=(int(bar[6])+1)*c.MS;assert lo<=t<cut and end-t==c.MIN and end<=cut
   part=cx['partial']
   if part is None:assert t%c.DAY==0;part={'day':t//c.DAY,'count':0,'quote_volume':'0'}
   assert part['day']==t//c.DAY;part['count']+=1;part['quote_volume']=str(D(part['quote_volume'])+D(bar[7]));part['close']=str(D(bar[4]))
   if end%c.DAY==0:assert part['count']==1440;cx['daily'].append(copy.deepcopy(part));cx['daily']=cx['daily'][-64:];cx['partial']=None
   else:cx['partial']=part
  cx.update(last_bar=pa['minutes'][-2],reference_bar=pa['minutes'][-1],last_hour=pa['hours'][-1],last_funding=next(x for x in reversed(pa['funding']) if int(x['fundingTime'])*c.MS<=cut));assert cx==contexts[a] and len(cx['daily'])==35 and cx['partial']['count']==30
 daytimes={t for t,code in actions if code==6};assert daytimes=={c.ns('2026-10-29T00:01:00Z')} and {k for _,k in actions}=={1,2,3,4,5,6,7};assert len(actions)==125+2*len({t for t,code in actions if code==4}) and len(actions)==len(delta['NAV'])
 assert delta['previous_nav_chain_sha256']==before['nav_chain_sha256'];expected_funding=sum(3*len(p) for (t,k),p in actions.items() if k==4);prices=copy.deepcopy(before['last_prices']);books=copy.deepcopy(before['books']);counts=copy.deepcopy(before['counters']);risk=copy.deepcopy(before['risk']);daily=copy.deepcopy(before['daily']);chain=before['nav_chain_sha256'];journal=delta['journal'];ji=0;wanted={};funding=[];decisions=[];trades=[];cushions=[];checks=breaches=0
 def take(kind,a,k,t,code):
  nonlocal ji
  x=journal[ji];ji+=1;assert x['kind']==kind and x['asset']==a and str(x['cost_multiplier'])==k and x['timestamp_ns']==t and x['event_code']==code;return x
 def fill(a,k,p,change,opening,t,code):
  x=take('trade',a,k,t,code);b=books[a][k];cash,q,entry,entryref=[D(b[z]) for z in ['cash','signed_units','entry_price','entry_reference']];change=D(change);qty=abs(change);ref,adv,sigma=[D(p[z]) for z in ['price','ADV','sigma']];m=int(k);lot,tick=[D(binding['metadata'][a][z]) for z in ['lot_size','tick_size']];part=qty*ref/adv;assert qty>0 and ref>0 and adv>0 and sigma>=0 and (q==0 if opening else change==-q)
  assert {z:D(v) for z,v in x['state_before'].items()}=={z:D(v) for z,v in b.items()} and D(x['change_signed_units'])==change and D(x['quantity'])==qty and x['side']==('buy' if change>0 else 'sell') and x['opening']==opening and not x['terminal'] and D(x['reference'])==ref and D(x['lagged_ADV'])==adv and D(x['lagged_sigma'])==sigma and D(x['participation'])==part
  fee,spread,slip=D('.0005')*m,D('.0001')*m,D('.0002')*m;impact=D('.5')*sigma*part.sqrt()*m;theory=ref*(1+(spread+slip+impact)*(1 if change>0 else -1));px=(theory/tick).to_integral_value(rounding=ROUND_CEILING if change>0 else ROUND_FLOOR)*tick;fee_usdt=qty*px*fee;realized=D(0) if opening else q*(px-entry);cash2=cash+realized-fee_usdt
  reject='participation' if part>D('.001') else 'lot_or_min_notional' if qty%lot or qty*px<D(binding['metadata'][a]['min_notional']) else 'fully_collateralized_1x_entry_cap' if opening and qty*px>cash2 else None
  if reject:assert x['status']=='rejected' and x['reason']==reject and x['state_after']==b;counts[a][k]['rejected_orders']+=1;trades.append(x);return
  assert x['status']=='filled';parts={'fee':fee_usdt,'half_spread':qty*ref*spread,'slippage':qty*ref*slip,'impact':qty*ref*impact,'tick_rounding':qty*abs(px-theory)};cost=sum(parts.values());refpnl=D(0) if opening else q*(ref-entryref);new={'cash':str(cash2),'signed_units':str(change if opening else D(0)),'entry_price':str(px if opening else D(0)),'entry_reference':str(ref if opening else D(0))}
  assert all(D(x[z])==v for z,v in {'execution':px,'theoretical_execution':theory,'fee_rate':fee,'half_spread_rate':spread,'slippage_rate':slip,'impact_rate':impact,'realized_price_PnL_usdt':realized,'reference_price_PnL_usdt':refpnl,'cost_usdt':cost}.items()) and all(D(x['cost_parts'][z])==v for z,v in parts.items()) and x['state_after']==new
  assert abs(cash+q*(ref-entry)-(D(new['cash'])+D(new['signed_units'])*(ref-D(new['entry_price'])))-cost)<D('1e-18');books[a][k]=new;z=counts[a][k];z['executions']+=1;z['round_trips']+=int(not opening);z['cost_usdt']=str(D(z['cost_usdt'])+cost);z['gross_reference_price_PnL_usdt']=str(D(z['gross_reference_price_PnL_usdt'])+refpnl);trades.append(x)
 for row,key in zip(delta['NAV'],sorted(actions)):
  t,code=key;assert [row['timestamp_ns'],row['event_code']]==list(key) and tuple(before['last_key'])<key
  for a,p in sorted(actions[key].items()):
   prices[a]=float(p['price'])
   for k in ['1','2','3']:
    oldbook=copy.deepcopy(books[a][k]);b=books[a][k];z=counts[a][k];q=D(b['signed_units']);direction=1 if q>0 else -1 if q<0 else 0
    if code==2:
     stack=risk[a][k];op=p['hour_open_ns']
     if op>=c.START:
      for i,item in enumerate(stack):
       end=stack[i+1]['t'] if i+1<len(stack) else t;sb=item['state'];units=D(sb['signed_units'])
       if units and item['t']<t and end>op and end>item['t']:
        adverse=D(p['low'] if units>0 else p['high']);cushion=D(sb['cash'])+units*(adverse-D(sb['entry_price']))-D('.01')*abs(units)*adverse;checks+=1;breaches+=int(cushion<=0);cushions.append(float(cushion));z['margin_checks']+=1;z['margin_proxy_violations']+=int(cushion<=0)
     risk[a][k]=[{'t':t,'state':copy.deepcopy(b)}]
    elif code==4:
     x=take('funding',a,k,t,code);base=-q*D(p['price'])*D(p['rate']);amount=base*int(k) if base<0 else base;cash=D(b['cash']);assert D(x['signed_units'])==q and D(x['mark_price'])==D(p['price']) and D(x['rate'])==D(p['rate']) and D(x['base_amount_usdt'])==base and D(x['amount_usdt'])==amount and D(x['cash_before'])==cash and D(x['cash_after'])==cash+amount
     if amount:b['cash']=str(cash+amount)
     z['funding_settlements']+=1;z['funding_usdt']=str(D(z['funding_usdt'])+amount);funding.append(x)
    elif code in [6,7]:
     closes=[D(v) for v in p['closes']];ds=contexts[a]['daily'];assert closes==[D(x['close']) for x in ds] and ds[-1]['day']==t//c.DAY-1 and t%c.DAY==c.MIN;adv=D(str(statistics.mean(float(x['quote_volume']) for x in ds[-20:])));sigma=D(str(statistics.stdev(math.log(float(closes[j])/float(closes[j-1])) for j in range(len(closes)-20,len(closes)))));assert D(p['ADV'])==adv and D(p['sigma'])==sigma
     if code==6:
      L=31 if a=='BTC' else 3;r=F(closes[-1])/F(closes[-1-L])-1;H=F(4,100) if a=='BTC' else F(2,100)
      if a=='BTC':w=1 if r>H else -1 if r< -H else 1 if direction==1 and r> -F(1,100) else -1 if direction==-1 and r<F(1,100) else 0;returns=[r]
      else:
       slow=F(closes[-1])/F(closes[-29])-1;w=-1 if r>H else 1 if r< -H else 1 if direction==1 and r<0 else -1 if direction==-1 and r>0 else 0;allowed=1 if slow>0 else -1 if slow<0 else 0;w=w if w==allowed else 0;returns=[r,slow]
      x=take('decision',a,k,t,code);assert x['wanted']==w and [F(v) for v in x['returns_exact']]==returns and D(x['prior_complete_close'])==closes[-1] and D(x['ADV'])==adv and D(x['sigma'])==sigma;wanted[a,k]=w;decisions.append(x)
      if q and direction!=w:fill(a,k,p,-q,False,t,code)
     elif wanted[a,k] and D(books[a][k]['signed_units'])==0:
      lot=D(binding['metadata'][a]['lot_size']);steps=F(binding['rules'][a]['N'])/(F(closes[-1])*F(lot));qty=D(steps.numerator//steps.denominator)*lot;assert qty>0;fill(a,k,p,D(wanted[a,k])*qty,True,t,code)
    if oldbook!=books[a][k]:risk[a][k].append({'t':t,'state':copy.deepcopy(books[a][k])})
    z['cash_violations']+=int(D(books[a][k]['cash'])<0)
  values={a:{k:float(b['cash'])+float(b['signed_units'])*(prices[a]-float(b['entry_price'])) for k,b in bb.items()} for a,bb in books.items()};values['COMBO']={k:values['BTC'][k]+values['ETH'][k] for k in ['1','2','3']};assert values==row['NAV'];chain=hashlib.sha256(bytes.fromhex(chain)+c.canonical(row)).hexdigest()
  if code==5:
   for a in values:
    for k,v in values[a].items():daily[a][k].append({'timestamp_ns':t,'equity_usdt':v})
 assert ji==len(journal) and len(funding)==expected_funding and len(decisions)==6 and state['books']==books and state['counters']==counts and state['last_prices']==prices and state['risk']==risk and state['daily']==daily and chain==state['nav_chain_sha256']==delta['nav_chain_sha256']==rep['NAV_chain_sha256'] and state['nav_points']==before['nav_points']+len(actions) and tuple(state['last_key'])==sorted(actions)[-1]
 pointers=[];p=previous
 while p:
  assert sha(ROOT/p['delta'])==p['delta_sha256'];pointers.append(gz(ROOT/p['delta']));ref=p.get('previous_pointer');assert ref is None or sha(ROOT/ref['path'])==ref['sha256'];p=read(ROOT/ref['path']) if ref else None
 prefix=[row for d in reversed(pointers) for row in d['NAV']];assert len(prefix)==before['nav_points']==2852 and 3*(len(pointers)+1)==75 and (cut-c.START)//c.MIN==2909;full=prefix+delta['NAV'];assert len(full)==state['nav_points'] and all((a['timestamp_ns'],a['event_code'])<(b['timestamp_ns'],b['event_code']) for a,b in zip(full,full[1:]));records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl')
 for a in ['BTC','ETH','COMBO']:
  sp=read(W/(a+'_spec.json'));fp=reg.fingerprint(sp);cfg=rep['configs']['forward_snapshot_candidate_'+a];rv=[x for x in events if x['fingerprint']==fp and x['status']=='reserved'];assert cfg['fingerprint']==fp and records[fp]['status']=='rejected' and records[fp]['result_available'] is True and records[fp]['report_sha256']==sha(W/'report.json') and sp['parameters']['previous_state_sha256']==previous['state_sha256'] and len(rv)==1 and int(__import__('datetime').datetime.fromisoformat(rv[0]['recorded_at_utc'].replace('Z','+00:00')).timestamp()*1e9)<(W/'complete.json').stat().st_mtime_ns
  assert cfg['partial_observation'] and cfg['does_not_cancel_or_reset_frozen_plan'] and not cfg['criteria']['full180days'] and not cfg['criteria']['six_complete_folds']
  for k,z in cfg['scenes'].items():
   v=np.asarray([x['NAV'][a][k] for x in full]);capital=20000 if a=='COMBO' else 10000;near(z['net_return_pct'],100*(v[-1]/capital-1));near(z['max_drawdown_pct'],100*max(1-v/np.maximum.accumulate(v)));assert z['NAV_sha256_f64le']==hashlib.sha256(v.astype('<f8').tobytes()).hexdigest() and z['NAV_points']==len(full) and z['daily_equity_usdt']==daily[a][k] and len(daily[a][k])==3 and len(z['folds'])==0 and z['recent40'] is None
   rr=[b['equity_usdt']/a0['equity_usdt']-1 for a0,b in zip(daily[a][k],daily[a][k][1:])];sd=statistics.stdev(rr) if len(rr)>1 else None
   if sd:near(z['sharpe_365'],statistics.mean(rr)/sd*math.sqrt(365))
   else:assert z['sharpe_365'] is None
   cg=100*((v[-1]/capital)**(365/((cut-c.START)/c.DAY))-1);near(z['cagr_pct'],cg)
   if z['max_drawdown_pct']:near(z['calmar'],cg/z['max_drawdown_pct'])
   else:assert z['calmar'] is None
   group=[counts[aa][k] for aa in ['BTC','ETH']] if a=='COMBO' else [counts[a][k]]
   for f in group[0]:near(z[f],sum(float(x[f]) for x in group))
 assert all(sha(Path(p))==h for p,h in guard.items()) and all(sha(ROOT/p)==h for p,h in read(R/'context.json')['account_hashes_before'].items())
 proof={'passed':True,'actual_observation_configs':3,'cumulative_finished_candidate_observations':75,'window_start_utc':'2026-10-28T22:30:00Z','cutoff_utc':'2026-10-29T00:30:00Z','new_elapsed_minutes':120,'elapsed_minutes':2909,'cost_scenes':9,'complete30day_folds':0,'NAV_points_per_scene':len(full),'prior_NAV_prefix':2852,'new_NAV_points_per_scene':len(actions),'full_NAV_points_checked':len(full)*9,'new_exact_causal_decisions':len(decisions),'new_daily_decisions_per_asset_and_cost':1,'daily_boundaries_per_scene':3,'new_fills':sum(x['status']=='filled' for x in trades),'new_rejected_orders':sum(x['status']=='rejected' for x in trades),'new_funding_settlements':len(funding),'expected_from_actual_settlement_actions':expected_funding,'funding_events_not_assumed_zero':True,'independent_funding_cashflows':funding,'independent_decisions':decisions,'independent_trades':trades,'new_closed_hour_risk_checks':checks,'new_risk_proxy_violations':breaches,'minimum_checked_cushion_usdt':min(cushions) if cushions else None,'actual_HTTP200_response_pages_verified':len(im['provenance']),'raw_minutes_per_asset':122,'exact_crossday_context_independently_rebuilt':True,'daily_decisions_and_funding_and_fills_verified_independently':True,'no_core_transition_target_trade_funding_calls_in_auditor':True,'partial_annualized_metrics_not_interpreted':True,'new_strategy_trials':0,'original_candidate_and_paper10_unchanged':True,'no_financial_model_rerun':True,'report_sha256':sha(W/'report.json'),'state_sha256':sha(W/'state.json'),'pointer_sha256':sha(ROOT/'research/automation/candidate_forward_latest.json'),'parent_returns_pct':{k:s['net_return_pct'] for k,s in rep['configs']['forward_snapshot_candidate_COMBO']['scenes'].items()},'parent_drawdowns_pct':{k:s['max_drawdown_pct'] for k,s in rep['configs']['forward_snapshot_candidate_COMBO']['scenes'].items()}};put(R/'candidate_verification.json',proof);print(json.dumps(proof),flush=True)
if __name__=='__main__':main()
