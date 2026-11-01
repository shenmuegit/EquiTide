"""Frozen event assembly; independent signals, native ledgers, funding/risk and full NAV.

Only the frozen normalize function is reused for closed-data/event validation.
No call to target/trade/transition/advance, and no account or registry writes.
"""
import copy,gzip,hashlib,importlib.util,json,math,statistics,sys,urllib.parse
from collections import defaultdict
from datetime import datetime,timezone
from decimal import Decimal as D,ROUND_CEILING,ROUND_FLOOR
from fractions import Fraction as F
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
read=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();canonical=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode();numeric=lambda b:{k:D(v) for k,v in b.items()};put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+chr(10))
def near(a,b):assert abs(float(a)-float(b))<=1e-11*max(1,abs(float(a)),abs(float(b))),(a,b)
def main(mode):
 isnew=mode=='l4h02';assert mode in ['candidate','l4h02'];folder='l4h02_observation' if isnew else 'candidate_observation';stem='forward_snapshot_l4h02_' if isnew else 'forward_snapshot_candidate_';pointerpath=ROOT/'research/automation'/('l4h02_forward_latest.json' if isnew else 'candidate_forward_latest.json');source=ROOT/('research/experiments/20261031T174613Z/prospective_l4/core.py' if isnew else 'research/experiments/20261026T110637Z/prospective_core.py');spec=importlib.util.spec_from_file_location('frozen_incremental_kernel',source);c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c);binding=c.bindings();caps={x['asset']:x['parameters']['initial_capital_usdt'] for x in read(c.PLAN)['components']};assert caps==({'BTC':5000,'ETH':15000} if isnew else {'BTC':10000,'ETH':10000});assert 'capitals' not in binding or binding['capitals']==caps;W=R/folder
 point=read(pointerpath);previous=read(W/'previous_pointer.json');before=read(ROOT/previous['state']);state=read(W/'state.json');rep=read(W/'report.json');delta=gz(W/'delta.json.gz');im=read(W/'input_manifest.json');complete=read(W/'complete.json');guard={str(p):sha(p) for p in [W/'state.json',W/'report.json',W/'delta.json.gz',W/'complete.json',W/'previous_pointer.json',pointerpath,ROOT/'research/automation/registry.jsonl']}
 assert point['previous_pointer']=={'path':str((W/'previous_pointer.json').relative_to(ROOT)),'sha256':sha(W/'previous_pointer.json')} and complete['previous_pointer_sha256']==hashlib.sha256(canonical(previous)).hexdigest()
 for key,file in [('state','state.json'),('report','report.json'),('delta','delta.json.gz'),('complete','complete.json')]:assert point[key]==str((W/file).relative_to(ROOT)) and point[key+'_sha256']==sha(W/file)
 for key in ['state','report','delta','complete']:assert sha(ROOT/previous[key])==previous[key+'_sha256']
 assert sha(ROOT/im['packet'])==im['sha256'];packet=gz(ROOT/im['packet']);lo,cut,actions,contexts=c.normalize(packet,before,binding);expected_lo=c.ns('2026-11-01T12:10:00Z' if isnew else '2026-11-01T10:30:00Z');expected_cut=c.ns('2026-11-01T14:10:00Z' if isnew else '2026-11-01T12:30:00Z');assert lo==expected_lo and cut==expected_cut==state['cutoff_ns'] and cut-lo==120*c.MIN and state['context']==contexts and state['binding_sha256']==hashlib.sha256(canonical(binding)).hexdigest()
 rawby=defaultdict(list);bad=[];pages=0
 for item in im['provenance']:
  assert sha(ROOT/item['raw'])==item['sha256'];raw=gzip.decompress((ROOT/item['raw']).read_bytes());assert len(raw)==item['bytes'];u=urllib.parse.urlparse(item['url']);q=urllib.parse.parse_qs(u.query);assert u.scheme=='https' and u.netloc=='fapi.binance.com'
  if item['http_status']!=200 or item.get('curl_exit_code',0):bad.append(item);continue
  data=json.loads(raw);pages+=1
  if u.path in ['/fapi/v1/klines','/fapi/v1/markPriceKlines','/fapi/v1/fundingRate']:rawby[q['symbol'][0][:-4],u.path].extend(data)
 for a in ['BTC','ETH']:
  ar=packet['assets'][a];assert rawby[a,'/fapi/v1/klines']==ar['minutes'] and rawby[a,'/fapi/v1/markPriceKlines']==ar['hours'] and rawby[a,'/fapi/v1/fundingRate']==ar['funding'] and len(ar['minutes'])==122 and numeric(ar['metadata'])==numeric(binding['metadata'][a]);assert ar['minutes'][0]==before['context'][a]['last_bar']
  # Independently verify any completed day uses the carried partial volume/count plus only new closed minutes.
  oldpartial=before['context'][a]['partial'];dayend=(oldpartial['day']+1)*c.DAY
  if lo<dayend<=cut:
   bars=[b for b in ar['minutes'] if lo<=int(b[0])*c.MS<dayend];d=next(x for x in contexts[a]['daily'] if x['day']==oldpartial['day']);assert oldpartial['count']+len(bars)==1440 and D(d['quote_volume'])==D(oldpartial['quote_volume'])+sum((D(b[7]) for b in bars),D(0)) and D(d['close'])==D(bars[-1][4])
 daily_events=sorted(t for t,code in actions if code==5);assert len(daily_events)==0 and all(t%c.DAY==c.MIN for t in daily_events);assert {k for _,k in actions}<=set(range(1,8)) and sum(code==1 for _,code in actions)==120 and sum(code==2 for _,code in actions)==2
 journal=defaultdict(list)
 for x in delta['journal']:journal[x['timestamp_ns'],x['event_code'],x['asset'],str(x['cost_multiplier'])].append(x)
 expected_funds=3*sum(len(payload) for (t,code),payload in actions.items() if code==4);assert len(actions)==len(delta['NAV'])==122+3*len(daily_events)+2*len({t for t,code in actions if code==4}) and delta['previous_nav_chain_sha256']==before['nav_chain_sha256']
 prices=copy.deepcopy(before['last_prices']);books=copy.deepcopy(before['books']);counts=copy.deepcopy(before['counters']);risk=copy.deepcopy(before['risk']);daily=copy.deepcopy(before['daily']);chain=before['nav_chain_sha256'];wanted={};funding=[];decisions=[];fills=rejects=used=0;cushions=[];marginchecks=0;violations=0
 def trade(a,k,p,change,opening,tr,t,code):
  nonlocal fills,rejects
  b=books[a][k];z=counts[a][k];cash,q,entry,er=[D(b[n]) for n in ['cash','signed_units','entry_price','entry_reference']];change=D(change);qty=abs(change);ref=D(p['price']);adv=D(p['ADV']);sig=D(p['sigma']);meta=binding['metadata'][a];part=qty*ref/adv;lot=D(meta['lot_size']);tick=D(meta['tick_size']);m=int(k);fee=D('.0005')*m;spread=D('.0001')*m;slip=D('.0002')*m;impact=D('.5')*sig*part.sqrt()*m;theory=ref*(1+(spread+slip+impact)*(1 if change>0 else -1));px=(theory/tick).to_integral_value(rounding=ROUND_CEILING if change>0 else ROUND_FLOOR)*tick;parts={'fee':qty*px*fee,'half_spread':qty*ref*spread,'slippage':qty*ref*slip,'impact':qty*ref*impact,'tick_rounding':qty*abs(px-theory)};reason='participation' if part>D('.001') else 'lot_or_min_notional' if qty%lot or qty*px<D(meta['min_notional']) else 'fully_collateralized_1x_entry_cap' if opening and qty*px>cash-parts['fee'] else None
  assert tr['kind']=='trade' and tr['timestamp_ns']==t and tr['event_code']==code and tr['opening']==opening and numeric(tr['state_before'])==numeric(b) and D(tr['change_signed_units'])==change and D(tr['quantity'])==qty and D(tr['reference'])==ref and D(tr['lagged_ADV'])==adv and D(tr['lagged_sigma'])==sig and D(tr['participation'])==part
  if reason:assert tr['status']=='rejected' and tr['reason']==reason and numeric(tr['state_after'])==numeric(b);z['rejected_orders']+=1;rejects+=1;return
  assert tr['status']=='filled' and D(tr['execution'])==px and D(tr['theoretical_execution'])==theory and all(D(tr['cost_parts'][n])==v for n,v in parts.items()) and D(tr['cost_usdt'])==sum(parts.values())
  if opening:assert q==0;new={'cash':str(cash-parts['fee']),'signed_units':str(change),'entry_price':str(px),'entry_reference':str(ref)};realized=rpnl=D(0)
  else:assert change==-q;realized=q*(px-entry);rpnl=q*(ref-er);new={'cash':str(cash+realized-parts['fee']),'signed_units':'0','entry_price':'0','entry_reference':'0'}
  assert numeric(tr['state_after'])==numeric(new) and D(tr['realized_price_PnL_usdt'])==realized and D(tr['reference_price_PnL_usdt'])==rpnl;books[a][k]=new;z['executions']+=1;z['round_trips']+=int(not opening);z['cost_usdt']=str(D(z['cost_usdt'])+sum(parts.values()));z['gross_reference_price_PnL_usdt']=str(D(z['gross_reference_price_PnL_usdt'])+rpnl);fills+=1
 for row,key in zip(delta['NAV'],sorted(actions)):
  t,code=key;assert [row['timestamp_ns'],row['event_code']]==list(key) and tuple(before['last_key'])<key
  for a,p in sorted(actions[key].items()):
   prices[a]=float(p['price'])
   if code in [5,6,7]:
    dd=[d for d in contexts[a]['daily'] if d['day']<t//c.DAY];cls=[D(d['close']) for d in dd];assert dd[-1]['day']==t//c.DAY-1 and list(map(D,p['closes']))==cls;adv=D(str(statistics.mean(float(d['quote_volume']) for d in dd[-20:])));sigma=D(str(statistics.stdev([math.log(float(cls[j])/float(cls[j-1])) for j in range(len(cls)-20,len(cls))])));assert D(p['ADV'])==adv and D(p['sigma'])==sigma
   for k in ['1','2','3']:
    b=books[a][k];oldbook=copy.deepcopy(b);z=counts[a][k];es=journal[t,code,a,k];used+=len(es)
    if code==2:
     op=p['hour_open_ns'];stack=risk[a][k]
     if op>=c.START:
      for i,item in enumerate(stack):
       end=stack[i+1]['t'] if i+1<len(stack) else t;bb=item['state'];units=D(bb['signed_units'])
       if units and item['t']<t and end>op and end>item['t']:
        adverse=D(p['low'] if units>0 else p['high']);cushion=D(bb['cash'])+units*(adverse-D(bb['entry_price']))-D('.01')*abs(units)*adverse;cushions.append(float(cushion));marginchecks+=1;violations+=int(cushion<=0);z['margin_checks']+=1;z['margin_proxy_violations']+=int(cushion<=0)
     risk[a][k]=[{'t':t,'state':copy.deepcopy(b)}];assert not es
    elif code==4:
     assert len(es)==1;f=es[0];q=D(b['signed_units']);base=-q*D(p['price'])*D(p['rate']);amount=base*int(k) if base<0 else base;cash=D(b['cash']);assert f['kind']=='funding' and D(f['signed_units'])==q and D(f['mark_price'])==D(p['price']) and D(f['rate'])==D(p['rate']) and D(f['base_amount_usdt'])==base and D(f['amount_usdt'])==amount and D(f['cash_before'])==cash and D(f['cash_after'])==cash+amount
     if amount:b['cash']=str(cash+amount)
     z['funding_settlements']+=1;z['funding_usdt']=str(D(z['funding_usdt'])+amount);funding.append({'asset':a,'cost':k,'timestamp_ns':t,'base_usdt':str(base),'amount_usdt':str(amount),'mark':p['price'],'rate':p['rate']})
    elif code==6:
     q=D(b['signed_units']);actual=(q>0)-(q<0);rule=binding['rules'][a];L=rule['L'];rr=F(cls[-1])/F(cls[len(cls)-1-L])-1;h=F(str(rule['H']))
     if a=='BTC':e=F(str(rule['E']));target=1 if rr>h else -1 if rr<-h else 1 if actual==1 and rr>-e else -1 if actual==-1 and rr<e else 0;returns=[str(rr)]
     else:slow=F(cls[-1])/F(cls[len(cls)-1-rule['S']])-1;base=-1 if rr>h else 1 if rr<-h else actual if actual==1 and rr<0 or actual==-1 and rr>0 else 0;gate=(slow>0)-(slow<0);target=base if base==gate else 0;returns=[str(rr),str(slow)];assert rule['E']==0
     close=bool(q and actual!=target);assert len(es)==1+int(close);d=es[0];assert d['kind']=='decision' and d['wanted']==target and d['returns_exact']==returns and D(d['prior_complete_close'])==cls[-1] and D(d['ADV'])==adv and D(d['sigma'])==sigma;wanted[a,k]=target;decisions.append({'asset':a,'cost':k,'timestamp_ns':t,'wanted':target,'returns_exact':returns,'prior_complete_close':str(cls[-1])})
     if close:trade(a,k,p,-q,False,es[1],t,code)
    elif code==7:
     assert (a,k) in wanted;q=D(books[a][k]['signed_units']);opening=bool(wanted[a,k] and q==0);assert len(es)==int(opening)
     if opening:lot=D(binding['metadata'][a]['lot_size']);qty=(D(binding['rules'][a]['N'])/cls[-1]/lot).to_integral_value(rounding=ROUND_FLOOR)*lot;trade(a,k,p,D(wanted[a,k])*qty,True,es[0],t,code)
    else:assert not es
    if oldbook!=books[a][k]:risk[a][k].append({'t':t,'state':copy.deepcopy(books[a][k])})
    z['cash_violations']+=int(D(books[a][k]['cash'])<0)
  values={a:{k:float(b['cash'])+float(b['signed_units'])*(prices[a]-float(b['entry_price'])) for k,b in bb.items()} for a,bb in books.items()};values['COMBO']={k:values['BTC'][k]+values['ETH'][k] for k in ['1','2','3']};assert values==row['NAV'];chain=hashlib.sha256(bytes.fromhex(chain)+canonical(row)).hexdigest()
  if code==5:
   for a in values:
    for k,v in values[a].items():daily[a][k].append({'timestamp_ns':t,'equity_usdt':v})
 assert used==len(delta['journal']) and len(funding)==expected_funds and len(decisions)==6*len(daily_events) and state['books']==books and state['counters']==counts and state['risk']==risk and state['daily']==daily and state['last_prices']==prices and state['last_key']==list(sorted(actions)[-1]) and state['nav_points']==before['nav_points']+len(actions) and chain==state['nav_chain_sha256']==delta['nav_chain_sha256']==rep['NAV_chain_sha256']
 pointers=[];p=previous;ids=set()
 while p:
  assert sha(ROOT/p['delta'])==p['delta_sha256'];pointers.append(gz(ROOT/p['delta']));doc=read(ROOT/p['report']);assert len(doc['configs'])==3
  for cfg in doc['configs'].values():assert cfg['fingerprint'] not in ids;ids.add(cfg['fingerprint'])
  ref=p.get('previous_pointer');assert ref is None or sha(ROOT/ref['path'])==ref['sha256'];p=read(ROOT/ref['path']) if ref else None
 prefix=[x for d in reversed(pointers) for x in d['NAV']];assert len(prefix)==before['nav_points'];full=prefix+delta['NAV'];assert len(full)==state['nav_points'] and all((x['timestamp_ns'],x['event_code'])<(y['timestamp_ns'],y['event_code']) for x,y in zip(full,full[1:]));records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl')
 for a in ['BTC','ETH','COMBO']:
  sp=read(W/(a+'_spec.json'));fp=reg.fingerprint(sp);cfg=rep['configs'][stem+a];assert cfg['fingerprint']==fp and sp['parameters']['previous_state_sha256']==previous['state_sha256'] and records[fp]['result_available'] and records[fp]['status']==cfg['status']=='rejected' and records[fp]['report_sha256']==sha(W/'report.json');assert fp not in ids;ids.add(fp);rv=[x for x in events if x['fingerprint']==fp and x['status']=='reserved'];assert len(rv)==1 and int(datetime.fromisoformat(rv[0]['recorded_at_utc'].replace('Z','+00:00')).timestamp()*1e9)<(W/'state.json').stat().st_mtime_ns
  for k,z in cfg['scenes'].items():
   cap=sum(caps.values()) if a=='COMBO' else caps[a];v=np.array([x['NAV'][a][k] for x in full]);assert v[0]==cap and len(z['folds'])==0 and z['recent40'] is None and z['NAV_points']==len(v) and z['NAV_sha256_f64le']==hashlib.sha256(v.astype('<f8').tobytes()).hexdigest() and z['daily_equity_usdt']==daily[a][k];near(z['net_return_pct'],100*(v[-1]/cap-1));near(z['max_drawdown_pct'],100*max(1-v/np.maximum.accumulate(v)));rr=[y['equity_usdt']/x['equity_usdt']-1 for x,y in zip(daily[a][k],daily[a][k][1:])];sd=statistics.stdev(rr) if len(rr)>1 else None
   if sd:near(z['sharpe_365'],statistics.mean(rr)/sd*365**.5)
   else:assert z['sharpe_365'] is None
   cg=100*((v[-1]/cap)**(365/((cut-c.START)/c.DAY))-1);near(z['cagr_pct'],cg)
   if z['max_drawdown_pct']:near(z['calmar'],cg/z['max_drawdown_pct'])
   else:assert z['calmar'] is None
   cs=[counts[x][k] for x in ['BTC','ETH']] if a=='COMBO' else [counts[a][k]]
   for field in cs[0]:near(z[field],sum(float(x[field]) for x in cs))
  ss=cfg['scenes'];one=ss['1'];three=ss['3'];expected={'full180days':False,'six_complete_folds':False,'five_positive_30day_folds':False,'all_cost_net_positive':all(x['net_return_pct']>0 for x in ss.values()),'whole_DD3_le25':three['max_drawdown_pct']<=25,'round_trips1_ge4':one['round_trips']>=4,'cost_safety_1x':one['gross_reference_PnL_to_execution_cost'] is not None and one['gross_reference_PnL_to_execution_cost']>=2.5,'no_cash_order_margin_violations':all(not any(z[f] for f in ['cash_violations','rejected_orders','margin_proxy_violations']) for z in ss.values()),'recent40_6of8':False,'recent40_all_cost_positive':False};assert cfg['criteria']==expected and cfg['failed_criteria']==[x for x,v in expected.items() if not v] and cfg['partial_observation'] and cfg['does_not_cancel_or_reset_frozen_plan']
 assert len(ids)==3*(len(pointers)+1) and all(sha(Path(p))==h for p,h in guard.items()) and all(sha(ROOT/p)==h for p,h in read(R/'context.json')['account_hashes_before'].items())
 out={'passed':True,'actual_observation_configs':3,'first_actual_window':False,'window_start_utc':datetime.fromtimestamp(lo/1e9,timezone.utc).isoformat().replace('+00:00','Z'),'cutoff_utc':datetime.fromtimestamp(cut/1e9,timezone.utc).isoformat().replace('+00:00','Z'),'new_elapsed_minutes':120,'elapsed_minutes':(cut-c.START)//c.MIN,'cost_scenes':9,'complete30day_folds':0,'NAV_points_per_scene':len(full),'prior_NAV_prefix':before['nav_points'],'new_NAV_points_per_scene':len(actions),'full_NAV_points_checked':9*len(full),'new_exact_causal_decisions':len(decisions),'independent_decisions':decisions,'new_fills':fills,'new_rejected_orders':rejects,'new_funding_settlements':len(funding),'expected_from_actual_settlement_actions':expected_funds,'independent_funding_cashflows':funding,'new_closed_hour_risk_checks':marginchecks,'new_risk_proxy_violations':violations,'minimum_checked_cushion_usdt':min(cushions) if cushions else None,'actual_HTTP200_response_pages_verified':pages,'failed_HTTP_attempts_preserved':bad,'raw_minutes_per_asset':122,'daily_context_bars':{a:len(contexts[a]['daily']) for a in ['BTC','ETH']},'daily_NAV_boundaries':len(daily['COMBO']['1']),'event_assembly_reuses_unchanged_frozen_normalize':True,'signal_trade_cost_funding_risk_fullNAV_independently_checked':True,'partial_first_hour_not_full_liquidation_proof':True,'partial_annualized_metrics_not_interpreted':True,'new_strategy_trials':0,'no_financial_model_rerun':True,'report_sha256':sha(W/'report.json'),'state_sha256':sha(W/'state.json'),'pointer_sha256':sha(pointerpath),'plan_sha256':binding['plan_sha256'],'whole180day_qualified':False,'parent_returns_pct':{k:z['net_return_pct'] for k,z in rep['configs'][stem+'COMBO']['scenes'].items()},'parent_drawdowns_pct':{k:z['max_drawdown_pct'] for k,z in rep['configs'][stem+'COMBO']['scenes'].items()}}
 out['cumulative_finished_l4h02_observations' if isnew else 'cumulative_finished_candidate_observations']=len(ids);put(R/('l4h02_verification.json' if isnew else 'candidate_verification.json'),out);print(json.dumps(out),flush=True)
