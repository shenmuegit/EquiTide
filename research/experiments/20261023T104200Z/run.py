"""Daily three-day negative-shock rebound, fixed half-recovery or holding timeout."""
import argparse,copy,gzip,hashlib,importlib.util,json,math,subprocess,sys
from datetime import datetime,timezone,timedelta
from decimal import Decimal as D
from fractions import Fraction as F
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
prior=module(ROOT/'research/experiments/20261023T063824Z/run.py','shock_native_inputs');core=prior.core
START,END,DAYS,SPAN=368,728,360,1442;POINTS=DAYS*SPAN+3;DROPS,HOLDS=[.03,.06,.09],[2,4,8]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
readgz=lambda p:json.loads(gzip.decompress(p.read_bytes()))
def call(command,row,*args):
 p=subprocess.run([sys.executable,'research/automation/registry.py',command,row['spec'],*args],cwd=ROOT,capture_output=True,text=True);out={'name':row['name'],'fingerprint':row['fingerprint'],'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};print(json.dumps(out),flush=True);assert p.returncode==0 and p.stdout.strip()==row['fingerprint'];return out

def decision(closes,i,drop,hold,position):
 j=i-1;last,anchor=F(closes[j]),F(closes[j-3]);roc=last/anchor-1;age=i-position['entry_index'] if position else None;recovery=2*last>=F(position['shock_start_close'])+F(position['entry_signal_close']) if position else None;timeout=age>=hold if position else None
 action=('exit' if recovery or timeout else 'hold') if position else ('entry' if roc < -F(str(drop)) else 'cash')
 return {'decision_index':i,'prior_close':str(closes[j]),'shock_start_close':str(closes[j-3]),'three_day_return_exact':str(roc),'action':action,'holding_age_days':age,'half_recovery_hit':recovery,'timeout_hit':timeout,'position_before':copy.deepcopy(position)}

def freeze():
 assert not (R/'plan.json').exists();last=ROOT/'research/experiments/20261023T084024Z';source=json.loads((ROOT/'research/experiments/20261023T063824Z/plan.json').read_text());events=reg.read_events(ROOT/'research/automation/registry.jsonl');records=reg.read_records(ROOT/'research/automation/registry.jsonl');first=[json.loads(x)['fingerprint'] for x in (ROOT/'research/automation/registry.jsonl').read_text().splitlines()[:16]];initial={}
 for x in events:
  if x['fingerprint'] in first:initial.setdefault(x['fingerprint'],{}).update(x)
 assert len(initial)==16 and all(x.get('result_available') for x in initial.values())
 monitor=module(ROOT/'research/monitor/snapshot.py','shock_registry_context');canonical={reg.fingerprint(x['spec']) for x in records.values() if not monitor.is_observation(x['spec'])};extra=[ROOT/'research/automation/README.md',*sorted((ROOT/'freqtrade_trial/results').glob('*.json')),*sorted((ROOT/'checks').glob('*oos.py'))];protected=[ROOT/'research/paper10/plan.json',ROOT/'research/paper10/state.json',last/'forward_state.json',last/'forward_report.json'];ctx={'registry_events':len(events),'registry_ids':len(records),'canonical_research_definitions_excluding_observations':len(canonical),'main_registry_sha256_before_reserve':sha(ROOT/'research/automation/registry.jsonl'),'initial_16_missing_actual_results':0,'initial_16_evidence_audit':{'path':'research/experiments/20261012T035429Z/prior_evidence_audit.json','sha256':sha(ROOT/'research/experiments/20261012T035429Z/prior_evidence_audit.json')},'prior_conclusions_read':[{'path':rel(p),'sha256':sha(p),'opening':p.read_text()[:200]} for p in sorted((ROOT/'research/experiments').glob('*/result.md'))],'additional_full_reads':[{'path':rel(p),'bytes':len(p.read_bytes()),'sha256':sha(p)} for p in extra],'account_hashes_before':{rel(p):sha(p) for p in protected}};put(R/'context.json',ctx)
 plan={'round':R.name,'frozen_at_utc':now(),'trigger_utc':'2026-10-23T10:42:00.014Z','hypothesis':'Large three-day negative moves may contain temporary overreaction recoverable before a short fixed timeout. Tested separately on BTC/ETH;daily horizon is an unproven extension of intraday reversal research,and liquid-coin momentum evidence is a contrary prior.','grid':{'entry_three_day_loss':DROPS,'maximum_holding_days':HOLDS,'assets':['BTC','ETH'],'financial_candidates':18,'cost_multipliers':[1,2,3]},'time_boundaries':source['time_boundaries'],'data':source['data'],'execution':source['execution'],'costs':source['costs'],'rules':{'entry':'At daily decision i,use only completed close j=i-1. If cash and C[j]/C[j-3]-1 strictly less than -D,attempt one full-cash spot buy at i00:01UTC. Equality does not enter;no crossing requirement.','frozen_recovery':'On actual filled entry at indexe,freeze pre-shock anchorA=C[e-4] and signal closeB=C[e-1]. Hold until a completed close satisfies2*C[j]>=A+B (half arithmetic price recovery),or i-e>=H complete daily execution intervals. No re-anchoring or moving target.','exit':'Check exits only when held at decision start;exit at next00:01OPEN,never at an intraday target or old close. An exit decision cannot reenter the same day,even if the current3dayloss still qualifies. Earliest reentry next daily decision.','state':'One cold cash start per configuration;carry actual cash/units,entry index,A/B across all12folds. Successful sell clears state;rejected order leaves actual state unchanged. No stop,averaging down,pyramiding or fold reset.','allocation':'Each config independent2000USDT in one spot asset. Raw maximum asset exposure1 via affordable lot,cash residue retained. No portfolio weighting/normalization,transfers,leverage,short,borrowing or cash yield. Original ongoingSMA75/25 unchanged.','terminal':'OOSend is known in advance;allow normal late entries then costed terminal liquidation. Terminal truncation and entry index disclosed,not filtered using future outcome.'},'gates':{'all_cost_returns_positive':True,'positive_1x_folds_min':8,'max_3x_minute_drawdown_pct':25,'local_3x_positive_fraction_min':.6,'round_trips_1x_min':4,'gross_reference_pnl_to_cost_min':2.5,'negative_balances':0,'rejections':0,'terminal_flat':True},'sensitivity':'For each asset full D×H3x3. Inclusive adjacent-index neighborhoods within asset;all18configs/54costs/648folds disclosed,no OOS choice or adaptive grid extension.','validation':'365dayinitial historicalcontext plus3daygap;12continuous30dayfolds. Fixed causal rules,no fitting/futurelabels,purgeNA. Reused developmenthistory,not untouched finaltest. NoDSR/PBO orliveprofitclaim.','NAV_axis':{'daily_span':SPAN,'points':POINTS,'definition':'Initial cash;each day predecisionnativeOPEN and postdecisionnativeOPEN (duplicates allowed),then1440originalFloat64closedminute marks;end preterminalOPEN and costed liquidation. Preserve pre-fill gap peaks;do not rewrite old metric conventions.'},'sources':[{'url':'https://doi.org/10.5195/ledger.2021.213','access_date':'2026-10-23','scope':'DeNicola2021 author journal abstract reports1/2/4hournegativeautocorrelation and stronger large-move reversals. Our3dayentry/half-recovery/timeout is a separately tested extension,not replication.'},{'url':'https://www.sciencedirect.com/science/article/pii/S1057521921002349','access_date':'2026-10-23','scope':'Zarembaetal2021 indexed author abstract distinguishes illiquidcoinreversal from largest/liquidcoinmomentum. Directpage403 recorded;contrary prior,not support for BTC/ETHdaily reversal.'},{'url':'https://developers.binance.com/en/docs/products/spot/filters','access_date':'2026-10-23','scope':'Current official definitions;actualexecution uses originalfrozenOct1historical proxy snapshot.'}],'read_only_context':{'previous_weekly_rotation':{'report':rel(last/'report.json'),'sha256':sha(last/'report.json')},'old_intraday_shock':{'report':'research/experiments/20261013T012732Z/report.json','sha256':sha(ROOT/'research/experiments/20261013T012732Z/report.json')},'hold_reference_report':{'path':'research/experiments/20261013T123949Z/report.json','sha256':sha(ROOT/'research/experiments/20261013T123949Z/report.json')}},'limits':['Daily meanreversion in two highlyliquidcoins may be absent;do not infer edge from trigger size.','FrozenOct1filters,halfspread/slippage/sqrtimpact and5minVWAP/IOCfill remain proxies,nohistoricalL2,TCA,queue or latencyproof.','Downside unconstrained until close-based recovery/timeout;no intraday stop,no independently untouched finaltest.']};put(R/'plan.json',plan);(R/'specs').mkdir();batch=[]
 for asset in ['BTC','ETH']:
  for drop in DROPS:
   for hold in HOLDS:
    name=f'shock3_{asset}_D{int(drop*100):02d}_H{hold}';spec={'kind':'strategy','family':'spot-daily-three-day-shock-half-recovery-timeout','name':name,'market':'spot','timeframe':'1d','universe':[asset+'/USDT'],'logic':plan['rules'],'parameters':{'initial_capital_usdt':2000,'raw_maximum_asset_exposure':1,'shock_lookback_days':3,'entry_three_day_loss':drop,'maximum_holding_days':hold,'recovery_fraction_of_arithmetic_price_drop':.5,'start_utc':plan['time_boundaries']['oos_start_utc'],'end_utc':plan['time_boundaries']['oos_end_exclusive_utc'],'warmup_days':365,'embargo_days':3,'walk_forward_folds':12,'walk_forward_test_days':30,'cost_multipliers':[1,2,3],'execution':plan['execution'],'costs':plan['costs']},'validation_plan':rel(R/'plan.json'),'sources':plan['sources']};path=R/'specs'/(name+'.json');put(path,spec);batch.append({'name':name,'spec':rel(path),'fingerprint':reg.fingerprint(spec),'asset':asset,'entry_three_day_loss':drop,'maximum_holding_days':hold,'capital_usdt':2000})
 assert len(batch)==len({x['fingerprint'] for x in batch})==18;put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/shock3_BTC_D06_H4.json').read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_AND_RESERVED18',sha(R/'plan.json'),flush=True)

def metric(v,days,terminal=False):
 daily=[float(v[d*SPAN]) for d in range(days+1)]
 if terminal:daily.append(float(v[-1]))
 s=core.engine.metrics(daily,days,terminal);s['daily_mark_drawdown_pct']=s['max_drawdown_pct'];s['max_drawdown_pct']=core.dd(v);s['calmar']=s['cagr_pct']/s['max_drawdown_pct'] if s['max_drawdown_pct'] else None;return s,daily

def summarize(v,trades,units):
 s,daily=metric(v,DAYS,True);s['folds']=[];start=datetime(2025,9,19,0,1,tzinfo=timezone.utc)
 for j in range(12):
  z,_=metric(v[j*30*SPAN:(j+1)*30*SPAN+1+2*(j==11)],30,j==11);s['folds'].append({'fold':j+1,'start_utc':(start+timedelta(days=30*j)).isoformat().replace('+00:00','Z'),'end_exclusive_utc':(start+timedelta(days=30*(j+1))).isoformat().replace('+00:00','Z'),**z})
 assert abs(math.prod(1+x['net_return_pct']/100 for x in s['folds'])-v[-1]/v[0])<1e-12
 filled=[t for t in trades if t['status']=='filled'];parts={p:float(sum(D(t['cost_parts'][p]) for t in filled)) for p in ['fee','half_spread','slippage','impact','tick_rounding']};cost=sum(parts.values());gross=sum(float(D(t['quantity'])*D(t['reference']))*(1 if t['side']=='sell' else -1) for t in filled);assert abs(gross-cost-(v[-1]-2000))<1e-8
 s.update(initial_capital_usdt=2000,final_NAV_usdt=float(v[-1]),cost_usdt=cost,cost_pct_initial=cost/2000*100,cost_parts_usdt=parts,gross_reference_PnL_usdt=gross,gross_reference_PnL_to_execution_cost=gross/cost if cost else None,executions=len(filled),round_trips=sum(t['side']=='sell' for t in filled),rejected_orders=len(trades)-len(filled),cash_or_units_violations=sum(D(t['cash_after'])<0 or D(t['units_after'])<0 for t in trades),terminal_units=str(units),daily_equity_usdt=daily,NAV_points=len(v),NAV_sha256_f64le=core.navhash(v));return s

def simulate(spec,market,mult):
 p=spec['parameters'];asset=spec['universe'][0].split('/')[0];rows,f,closes=market['rows'],market['frame'],market['closes'];values=[x['close'] for x in rows];cash,units,position=D(2000),D(0),None;v=np.empty(POINTS);v[0]=2000;decisions=[];trades=[];states=[]
 def execute(i,buy,terminal=False):
  nonlocal cash,units,position
  mi=i*1440+1;h=f.slice(mi-5,5);assert int(h['available_ts'].max())<=rows[i]['trade_ts'];proxy=h['quote_volume'].sum()/h['base_volume'].sum();adv,sigma=core.engine.lagged_cost_inputs(rows,i);cb,qb,pb=cash,units,copy.deepcopy(position);cash,units,t=core.fill(cash,units,buy,f['open'][mi],D(str(adv)),D(str(sigma)),mult,p['execution']['filters'][asset+'USDT'],proxy)
  if t['status']=='filled':position={'entry_index':i,'entry_signal_close':str(values[i-1]),'shock_start_close':str(values[i-4])} if buy else None
  t.update(asset=asset,decision_index=i,day_offset=i-START,trade_ts_ns=rows[i]['trade_ts'],terminal=terminal,cash_before=str(cb),units_before=str(qb),position_before=pb,position_after=copy.deepcopy(position));trades.append(t)
 for d,i in enumerate(range(START,END)):
  assert rows[i-1]['close_available_ts']<rows[i]['trade_ts'];v[d*SPAN+1]=float(cash+units*rows[i]['trade_open']);dec=decision(values,i,p['entry_three_day_loss'],p['maximum_holding_days'],position)
  if dec['action'] in ['entry','exit']:execute(i,dec['action']=='entry')
  dec['position_after']=copy.deepcopy(position);decisions.append(dec);v[d*SPAN+2]=float(cash+units*rows[i]['trade_open']);v[d*SPAN+3:(d+1)*SPAN+1]=float(cash)+float(units)*closes[i*1440+1:(i+1)*1440+1];state={'day_offset':d,'end_day_exclusive':d+1,'cash':str(cash),'units':str(units),'position':copy.deepcopy(position)}
  if states and all(states[-1][z]==state[z] for z in ['cash','units','position']):states[-1]['end_day_exclusive']=d+1
  else:states.append(state)
 v[-2]=float(cash+units*rows[END]['trade_open'])
 if units:execute(END,False,True)
 v[-1]=float(cash);assert units==0 and position is None and np.isfinite(v).all() and (v>0).all()
 return v,{'decisions':decisions,'trades':trades,'position_segments':states,'terminal_cash':str(cash),'terminal_units':str(units),'terminal_position':position,'summary':summarize(v,trades,units)}

def evaluate():
 assert not (R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(records[x['fingerprint']]['status']=='reserved' for x in batch);started=now();market=prior.markets(plan);configs={};(R/'results').mkdir()
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());arc={'spec':spec,'fingerprint':row['fingerprint'],'scenes':{}};scenes={}
  for k in ['1','2','3']:v,z=simulate(spec,market[row['asset']],int(k));arc['scenes'][k]=z;scenes[k]=z['summary']
  path=R/'results'/(row['name']+'.json.gz');core.gzwrite(path,arc);configs[row['name']]={**row,'spec_path':row['spec'],'archive':rel(path),'archive_sha256':sha(path),'scenes':scenes,'positive_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'])};print(row['name'],scenes['1']['net_return_pct'],scenes['3']['net_return_pct'],flush=True)
 for c in configs.values():
  neighbors=[x for x in configs.values() if x['asset']==c['asset'] and abs(DROPS.index(x['entry_three_day_loss'])-DROPS.index(c['entry_three_day_loss']))<=1 and abs(HOLDS.index(x['maximum_holding_days'])-HOLDS.index(c['maximum_holding_days']))<=1];frac=sum(x['scenes']['3']['net_return_pct']>0 for x in neighbors)/len(neighbors);c['sensitivity']={'neighbor_names':[x['name'] for x in neighbors],'neighbor_count':len(neighbors),'local_3x_neighbor_positive_fraction':frac};s=c['scenes'];ratio=s['1']['gross_reference_PnL_to_execution_cost'];c['criteria']={'positive_all_costs':all(z['net_return_pct']>0 for z in s.values()),'eight_positive_1x_folds':c['positive_folds_1x']>=8,'minute_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'neighbourhood_positive3_gte60pct':frac>=.6,'four_round_trips1':s['1']['round_trips']>=4,'gross_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_balance_violations':all(z['cash_or_units_violations']==0 for z in s.values()),'no_order_rejections':all(z['rejected_orders']==0 for z in s.values()),'terminal_flat':all(D(z['terminal_units'])==0 for z in s.values())};c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':plan['time_boundaries'],'curve_formula':plan['NAV_axis'],'input_data':plan['data'],'configs':configs,'summary':{'new_configs':18,'candidate_configs':18,'cost_scenarios':54,'passed':[x['name'] for x in configs.values() if x['status']=='passed'],'rejected':[x['name'] for x in configs.values() if x['status']=='rejected'],'positive_configs_by_cost':{k:sum(x['scenes'][k]['net_return_pct']>0 for x in configs.values()) for k in ['1','2','3']}},'scope':plan['limits']};put(R/'report.json',report);print('SUMMARY',json.dumps(report['summary']),flush=True)

def finish():
 report=json.loads((R/'report.json').read_text());done=[]
 for row in json.loads((R/'batch.json').read_text()):done.append(call('finish',row,report['configs'][row['name']]['status'],rel(R/'report.json')));put(R/'finish.json',done)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','finish']);globals()[p.parse_args().command]()
