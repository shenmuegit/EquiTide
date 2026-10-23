"""Pre-registered weekly relative momentum: recent-week skip and switching friction."""
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
prior=module(ROOT/'research/experiments/20261023T063824Z/run.py','weekly_native_market_inputs');core=prior.core
START,END,DAYS,SPAN=368,728,360,1443;POINTS=DAYS*SPAN+3;LOOKS,GAPS,SKIPS=[21,42,84],[0,.02,.04],[0,7]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
readgz=lambda p:json.loads(gzip.decompress(p.read_bytes()))
def call(command,row,*args):
 p=subprocess.run([sys.executable,'research/automation/registry.py',command,row['spec'],*args],cwd=ROOT,capture_output=True,text=True);out={'name':row['name'],'fingerprint':row['fingerprint'],'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};print(json.dumps(out),flush=True);assert p.returncode==0 and p.stdout.strip()==row['fingerprint'];return out

def choose(closes,j,look,skip,gap,held):
 """Only completed closes; exact rational ranking and contemporaneous cash gate."""
 score={a:F(v[j-skip])/F(v[j-skip-look])-1 for a,v in closes.items()};absolute={a:F(v[j])/F(v[j-look])-1 for a,v in closes.items()};eligible=[a for a in ['BTC','ETH'] if absolute[a]>0]
 best=max(eligible,key=lambda a:(score[a],a=='BTC')) if eligible else None
 if held in eligible:target=best if best!=held and score[best]-score[held]>F(str(gap)) else held
 else:target=best
 return target,{'scores':{a:str(x) for a,x in score.items()},'absolute_returns':{a:str(x) for a,x in absolute.items()},'eligible':eligible,'winner_before_switch_hurdle':best}

def freeze():
 assert not (R/'plan.json').exists();last=ROOT/'research/experiments/20261023T063824Z';source=json.loads((last/'plan.json').read_text());events=reg.read_events(ROOT/'research/automation/registry.jsonl');records=reg.read_records(ROOT/'research/automation/registry.jsonl');first=[json.loads(x)['fingerprint'] for x in (ROOT/'research/automation/registry.jsonl').read_text().splitlines()[:16]];initial={}
 for x in events:
  if x['fingerprint'] in first:initial.setdefault(x['fingerprint'],{}).update(x)
 assert len(initial)==16 and all(x.get('result_available') for x in initial.values())
 monitor=module(ROOT/'research/monitor/snapshot.py','weekly_readonly_registry_context');canonical={reg.fingerprint(x['spec']) for x in records.values() if not monitor.is_observation(x['spec'])};extra=[ROOT/'research/automation/README.md',*sorted((ROOT/'freqtrade_trial/results').glob('*.json')),*sorted((ROOT/'checks').glob('*oos.py'))];protected=[ROOT/'research/paper10/plan.json',ROOT/'research/paper10/state.json',last/'forward_state.json',last/'forward_report.json']
 ctx={'registry_events':len(events),'registry_ids':len(records),'canonical_research_definitions_excluding_observations':len(canonical),'main_registry_sha256_before_reserve':sha(ROOT/'research/automation/registry.jsonl'),'initial_16_missing_actual_results':0,'initial_16_evidence_audit':{'path':'research/experiments/20261012T035429Z/prior_evidence_audit.json','sha256':sha(ROOT/'research/experiments/20261012T035429Z/prior_evidence_audit.json')},'prior_conclusions_read':[{'path':rel(p),'sha256':sha(p),'opening':p.read_text()[:200]} for p in sorted((ROOT/'research/experiments').glob('*/result.md'))],'additional_full_reads':[{'path':rel(p),'bytes':len(p.read_bytes()),'sha256':sha(p)} for p in extra],'account_hashes_before':{rel(p):sha(p) for p in protected}};put(R/'context.json',ctx)
 plan={'round':R.name,'frozen_at_utc':now(),'trigger_utc':'2026-10-23T08:40:24.950Z','hypothesis':'Weekly scheduling and an explicit relative-score switching hurdle may reduce costly coin churn;skipping the most recent week tests whether short-horizon reversal contaminates relative formation. Both mechanisms are hypotheses,not evidence imported from equity papers.','grid':{'formation_days':LOOKS,'switching_return_gap':GAPS,'skip_recent_days':SKIPS,'financial_candidates':18,'cost_multipliers':[1,2,3]},'time_boundaries':source['time_boundaries'],'data':source['data'],'execution':source['execution'],'costs':source['costs'],'rules':{'signal':'At completed UTC day j=i-1,absoluteROC_a=C_a[j]/C_a[j-L]-1;rankROC_a=C_a[j-S]/C_a[j-S-L]-1. Only assets with current absoluteROC>0 eligible. Select highest rankROC among eligible;BTC priority on exact tie.','schedule':'Only Mondays at next00:01UTC;no initial off-schedule buy. Other days keep actual holding,do not exit on new signals. Calendar from UTC date,not fold offsets.','switching':'If incumbent is eligible,retain it unless another eligible asset rankROC strictly exceeds incumbent rankROC by G. If incumbent ineligible,select best eligible without switching hurdle,or cash if none. Equality retains incumbent. S=0 is contemporaneous rank;S=7 skips exactly seven completed days in ranking,while cash gate always uses current absoluteROC.','execution':'On target change,sell all held coin before buying target at same declared next00:01 nativeDecimalOPEN. Both real legs charged separately;rejected sale prevents purchase. Quantity-rounding residue remains shared cash. No trade if target stays same.','allocation':'One shared2000USDT spot cash account;at most one BTC or ETH holding with raw target exposure1,other0. No75/25normalization,fixed-sleeve NAV sum,cashyield,borrowing,leverage,short or external transfers. Original frozen75/25SMA account unchanged.','state':'One cold cash start;carry actual cash,held asset,units across all12folds. No independent old component NAV can represent stateful shared-cash rotations,so actual new fill paths required.'},'gates':{'all_cost_returns_positive':True,'positive_1x_folds_min':8,'max_3x_minute_drawdown_pct':25,'local_3x_positive_fraction_min':.6,'round_trips_1x_min':4,'gross_reference_pnl_to_cost_min':2.5,'negative_balances':0,'rejections':0,'terminal_flat':True},'sensitivity':'Each S=0/7 direction has full L×G3x3;inclusive adjacent-index rectangular neighborhoods separately. All18configs,54costs,648folds disclosed;skip-pair contrasts descriptive,no OOS selection.','validation':'365day initial historical context plus3day gap;12continuous30dayfolds,no fitting or future labels,purgeNA. At each fold context rolls causally. Reused development history,not untouched final test;no DSR/PBO or live profit claim.','NAV_axis':{'daily_span':SPAN,'points':POINTS,'definition':'Initial cash;each day predecisionnativeOPEN,post-saleOPEN,post-purchaseOPEN slots including duplicates when unused,then1440originalFloat64closedminute marks;at end preterminalOPEN then costed liquidation. This preserves both rotation-leg marks and gap risks.'},'read_only_context':{'prior_annual_countertest':{'report':rel(last/'report.json'),'sha256':sha(last/'report.json')},'old_daily_rotation_reports':[{'path':f'research/experiments/{s}/report.json','sha256':sha(ROOT/f'research/experiments/{s}/report.json')} for s in ['20261012T115927Z','20261013T123949Z']],'scope':'Old daily rotation rejected;not rerun or recast as new evidence. Same-capital360dayhold references read-only,with their original filter/metric conventions disclosed.'},'sources':[{'url':'https://www.aqr.com/-/media/AQR/Documents/Insights/White-Papers/The-Case-for-Momentum-Investing.pdf','access_date':'2026-10-23','scope':'Author equity research excludes recent month;our seven-daycrypto skip and weekly hysteresis are separately tested hypotheses,not paper replication.'},{'url':'https://www.nber.org/papers/w25882','access_date':'2026-10-23','scope':'Official indexed abstract supports crypto momentum motivation only;direct page403,fulltextnotread.'},{'url':'https://developers.binance.com/en/docs/products/spot/filters','access_date':'2026-10-23','scope':'Official current filter definitions;actualhistoricalexecution uses frozenOct1snapshot proxy.'}],'limits':['Only two liquid spot assets and reused history;no independent holdout.','FrozenOct1filters,halfspread/slippage/square-rootimpact and prior5minuteVWAP/IOC fill remain proxies,noL2,TCA,queue/latencyproof.','Weekly risk exits wait until Monday;intraweek losses intentionally retained,no implicit stop.']}
 put(R/'plan.json',plan);(R/'specs').mkdir();batch=[]
 for skip in SKIPS:
  for look in LOOKS:
   for gap in GAPS:
    name=f'weekly_S{skip}_L{look}_G{int(gap*100):02d}';spec={'kind':'strategy','family':'spot-weekly-relative-momentum-skip-switch-hysteresis','name':name,'market':'spot','timeframe':'1d','universe':['BTC/USDT','ETH/USDT'],'logic':plan['rules'],'parameters':{'initial_capital_usdt':2000,'raw_target_exposure_per_held_asset':1,'formation_days':look,'switching_return_gap':gap,'skip_recent_days':skip,'rebalance_weekday_UTC':0,'absolute_return_hurdle':0,'start_utc':plan['time_boundaries']['oos_start_utc'],'end_utc':plan['time_boundaries']['oos_end_exclusive_utc'],'warmup_days':365,'embargo_days':3,'walk_forward_folds':12,'walk_forward_test_days':30,'cost_multipliers':[1,2,3],'execution':plan['execution'],'costs':plan['costs']},'validation_plan':rel(R/'plan.json'),'sources':plan['sources']};path=R/'specs'/(name+'.json');put(path,spec);batch.append({'name':name,'spec':rel(path),'fingerprint':reg.fingerprint(spec),'skip_recent_days':skip,'formation_days':look,'switching_return_gap':gap,'capital_usdt':2000})
 assert len(batch)==len({x['fingerprint'] for x in batch})==18;put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/weekly_S0_L42_G02.json').read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_AND_RESERVED18',sha(R/'plan.json'),flush=True)

def metric(v,days,terminal=False):
 daily=[float(v[d*SPAN]) for d in range(days+1)]
 if terminal:daily.append(float(v[-1]))
 s=core.engine.metrics(daily,days,terminal);s['daily_mark_drawdown_pct']=s['max_drawdown_pct'];s['max_drawdown_pct']=core.dd(v);s['calmar']=s['cagr_pct']/s['max_drawdown_pct'] if s['max_drawdown_pct'] else None;return s,daily

def summarize(v,trades,terminal_units):
 s,daily=metric(v,DAYS,True);s['folds']=[];start=datetime(2025,9,19,0,1,tzinfo=timezone.utc)
 for j in range(12):
  z,_=metric(v[j*30*SPAN:(j+1)*30*SPAN+1+2*(j==11)],30,j==11);s['folds'].append({'fold':j+1,'start_utc':(start+timedelta(days=j*30)).isoformat().replace('+00:00','Z'),'end_exclusive_utc':(start+timedelta(days=(j+1)*30)).isoformat().replace('+00:00','Z'),**z})
 assert abs(math.prod(1+x['net_return_pct']/100 for x in s['folds'])-v[-1]/v[0])<1e-12
 filled=[t for t in trades if t['status']=='filled'];parts={p:float(sum(D(t['cost_parts'][p]) for t in filled)) for p in ['fee','half_spread','slippage','impact','tick_rounding']};cost=sum(parts.values());gross=sum(float(D(t['quantity'])*D(t['reference']))*(1 if t['side']=='sell' else -1) for t in filled);assert abs(gross-cost-(v[-1]-2000))<1e-8
 s.update(initial_capital_usdt=2000,final_NAV_usdt=float(v[-1]),cost_usdt=cost,cost_pct_initial=cost/2000*100,cost_parts_usdt=parts,gross_reference_PnL_usdt=gross,gross_reference_PnL_to_execution_cost=gross/cost if cost else None,executions=len(filled),round_trips=sum(t['side']=='sell' for t in filled),rejected_orders=len(trades)-len(filled),cash_or_units_violations=sum(D(t['cash_after'])<0 or D(t['units_after'])<0 for t in trades),terminal_units=str(terminal_units),daily_equity_usdt=daily,NAV_points=len(v),NAV_sha256_f64le=core.navhash(v));return s

def simulate(spec,market,mult):
 p=spec['parameters'];closes={a:[x['close'] for x in z['rows']] for a,z in market.items()};cash,units,held=D(2000),D(0),None;v=np.empty(POINTS);v[0]=2000;decisions=[];trades=[];states=[]
 def wealth(i):return cash+(units*market[held]['rows'][i]['trade_open'] if held else D(0))
 def execute(asset,buy,i,terminal=False):
  nonlocal cash,units,held
  assert (buy and held is None and units==0) or (not buy and held==asset and units>0)
  m=market[asset];rows=m['rows'];f=m['frame'];mi=i*1440+1;h=f.slice(mi-5,5);assert int(h['available_ts'].max())<=rows[i]['trade_ts'];proxy=h['quote_volume'].sum()/h['base_volume'].sum();adv,sigma=core.engine.lagged_cost_inputs(rows,i);cb,qb,hb=cash,units,held;cash,units,t=core.fill(cash,units,buy,f['open'][mi],D(str(adv)),D(str(sigma)),mult,p['execution']['filters'][asset+'USDT'],proxy)
  if t['status']=='filled':held=asset if buy else None
  t.update(asset=asset,decision_index=i,day_offset=i-START,trade_ts_ns=rows[i]['trade_ts'],terminal=terminal,cash_before=str(cb),units_before=str(qb),held_before=hb,held_after=held);trades.append(t)
 for d,i in enumerate(range(START,END)):
  assert market['BTC']['rows'][i-1]['close_available_ts']<market['BTC']['rows'][i]['trade_ts'];scheduled=datetime.fromisoformat(market['BTC']['rows'][i]['date']).weekday()==0;hb=held;v[d*SPAN+1]=float(wealth(i));target=held;detail={}
  if scheduled:target,detail=choose(closes,i-1,p['formation_days'],p['skip_recent_days'],p['switching_return_gap'],held)
  if target!=held and held:execute(held,False,i)
  v[d*SPAN+2]=float(wealth(i))
  if target is not None and held is None:execute(target,True,i)
  v[d*SPAN+3]=float(wealth(i));decisions.append({'decision_index':i,'signal_index':i-1,'scheduled_Monday':scheduled,'held_before':hb,'desired_target':target,'held_after':held,**detail});state={'day_offset':d,'end_day_exclusive':d+1,'cash':str(cash),'units':str(units),'asset':held}
  if states and all(states[-1][z]==state[z] for z in ['cash','units','asset']):states[-1]['end_day_exclusive']=d+1
  else:states.append(state)
  v[d*SPAN+4:(d+1)*SPAN+1]=float(cash)+(float(units)*market[held]['closes'][i*1440+1:(i+1)*1440+1] if held else np.zeros(1440))
 v[-2]=float(wealth(END))
 if held:execute(held,False,END,True)
 v[-1]=float(wealth(END));assert held is None and units==0 and (v>0).all() and np.isfinite(v).all()
 return v,{'decisions':decisions,'trades':trades,'position_segments':states,'terminal_cash':str(cash),'terminal_units':str(units),'terminal_asset':held,'summary':summarize(v,trades,units)}

def evaluate():
 assert not (R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(records[x['fingerprint']]['status']=='reserved' for x in batch);started=now();market=prior.markets(plan);configs={};(R/'results').mkdir()
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());scenes={};arc={'spec':spec,'fingerprint':row['fingerprint'],'scenes':{}}
  for k in ['1','2','3']:v,z=simulate(spec,market,int(k));arc['scenes'][k]=z;scenes[k]=z['summary']
  path=R/'results'/(row['name']+'.json.gz');core.gzwrite(path,arc);configs[row['name']]={**row,'spec_path':row['spec'],'archive':rel(path),'archive_sha256':sha(path),'scenes':scenes,'positive_folds_1x':sum(x['net_return_pct']>0 for x in scenes['1']['folds'])};print(row['name'],scenes['1']['net_return_pct'],scenes['3']['net_return_pct'],flush=True)
 for c in configs.values():
  neighbors=[x for x in configs.values() if x['skip_recent_days']==c['skip_recent_days'] and abs(LOOKS.index(x['formation_days'])-LOOKS.index(c['formation_days']))<=1 and abs(GAPS.index(x['switching_return_gap'])-GAPS.index(c['switching_return_gap']))<=1];frac=sum(x['scenes']['3']['net_return_pct']>0 for x in neighbors)/len(neighbors);c['sensitivity']={'neighbor_names':[x['name'] for x in neighbors],'neighbor_count':len(neighbors),'local_3x_neighbor_positive_fraction':frac};s=c['scenes'];ratio=s['1']['gross_reference_PnL_to_execution_cost'];c['criteria']={'positive_all_costs':all(x['net_return_pct']>0 for x in s.values()),'eight_positive_1x_folds':c['positive_folds_1x']>=8,'minute_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'neighbourhood_positive3_gte60pct':frac>=.6,'four_round_trips1':s['1']['round_trips']>=4,'gross_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_balance_violations':all(x['cash_or_units_violations']==0 for x in s.values()),'no_order_rejections':all(x['rejected_orders']==0 for x in s.values()),'terminal_flat':all(D(x['terminal_units'])==0 for x in s.values())};c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':plan['time_boundaries'],'curve_formula':plan['NAV_axis'],'input_data':plan['data'],'configs':configs,'summary':{'new_configs':18,'candidate_configs':18,'cost_scenarios':54,'passed':[x['name'] for x in configs.values() if x['status']=='passed'],'rejected':[x['name'] for x in configs.values() if x['status']=='rejected'],'positive_configs_by_cost':{k:sum(x['scenes'][k]['net_return_pct']>0 for x in configs.values()) for k in ['1','2','3']}},'scope':plan['limits']};put(R/'report.json',report);print('SUMMARY',json.dumps(report['summary']),flush=True)

def finish():
 report=json.loads((R/'report.json').read_text());done=[]
 for row in json.loads((R/'batch.json').read_text()):done.append(call('finish',row,report['configs'][row['name']]['status'],rel(R/'report.json')));put(R/'finish.json',done)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','finish']);globals()[p.parse_args().command]()
