"""Passive two-sleeve perpetual portfolios,reusing immutable component NAV evidence."""
import argparse,copy,gzip,hashlib,importlib.util,itertools,json,math,subprocess,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
LOOKS,HURDLES=[20,25,30],[.01,.02,.04]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
readgz=lambda p:json.loads(gzip.decompress(p.read_bytes()))
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
def gzwrite(p,x):p.write_bytes(gzip.compress(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode(),mtime=0))
def call(command,row,*args):
 p=subprocess.run([sys.executable,'research/automation/registry.py',command,row['spec'],*args],cwd=ROOT,capture_output=True,text=True);x={'name':row['name'],'fingerprint':row['fingerprint'],'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};print(json.dumps(x),flush=True);assert p.returncode==0 and p.stdout.strip()==row['fingerprint'];return x

def keys(ts,codes,start):
 delta=ts-np.int64(start);assert (delta>=0).all() and int(delta.max())<(2**63-16)//16 and ((codes>=0)&(codes<16)).all();out=delta*16+codes.astype(np.int64);assert np.all(np.diff(out)>0);return out

def align(axis):
 start=axis['BTC']['start_ns'];assert start==axis['ETH']['start_ns'];ka,kb=[keys(axis[a]['ts'],axis[a]['codes'],start) for a in ['BTC','ETH']];union=np.union1d(ka,kb);projections={}
 for asset,old in zip(['BTC','ETH'],[ka,kb]):
  ix=np.searchsorted(old,union,side='right')-1;assert ix.min()>=0 and np.all(old[ix]<=union) and np.array_equal(ix[np.searchsorted(union,old)],np.arange(len(old)));projections[asset]=ix
 days=np.searchsorted(union,ka[axis['BTC']['daily_indices']]);folds=np.searchsorted(union,ka[axis['BTC']['fold_indices']]);assert np.array_equal(union[days],kb[axis['ETH']['daily_indices']]) and np.array_equal(union[folds],kb[axis['ETH']['fold_indices']]);return {'keys':union,'projections':projections,'daily_indices':days,'fold_indices':folds,'sha256':hashlib.sha256(union.astype('<i8').tobytes()).hexdigest(),'source_keys':{'BTC':ka,'ETH':kb},'start_ns':start}

def freeze():
 assert not (R/'plan.json').exists();ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');base=ROOT/'research/experiments/20261023T144255Z';original=json.loads((base/'plan.json').read_text());s20=ROOT/'research/experiments/20261023T164355Z';s25=ROOT/'research/experiments/20261023T184400Z';p20=json.loads((s20/'plan.json').read_text());p25=json.loads((s25/'plan.json').read_text());assert p20['rules']==p25['rules'] and p20['costs']==p25['costs'] and sha(s20/'engine.py')==sha(s25/'engine.py');refs={}
 for source,looks in [(s20,[20]),(s25,[25,30])]:
  report=json.loads((source/'report.json').read_text())
  for name,c in report['configs'].items():
   if c['lookback_days'] not in looks:continue
   fp=c['fingerprint'];rec=records[fp];assert rec['result_available'] is True and rec['report_sha256']==sha(source/'report.json') and sha(ROOT/c['archive'])==c['archive_sha256'];arc=readgz(ROOT/c['archive']);assert reg.fingerprint(arc['spec'])==fp and arc['spec']['parameters']['initial_capital_usdt']==10000 and arc['spec']['parameters']['fixed_entry_notional_usdt']==2000
   refs[fp]={'name':name,'asset':c['asset'],'role':'candidate','lookback_days':c['lookback_days'],'return_hurdle':c['return_hurdle'],'report':rel(source/'report.json'),'report_sha256':sha(source/'report.json'),'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'archive':c['archive'],'archive_sha256':c['archive_sha256'],'original_status':rec['status'],'capital_usdt':10000,'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()}}
 assert len(refs)==18 and all(sum(x['asset']==a for x in refs.values())==9 for a in ['BTC','ETH'])
 reference_report=json.loads((base/'report.json').read_text());refname='perp_pair_constant_long_reference';ref=reference_report['configs'][refname];rec=records[ref['fingerprint']];assert rec['result_available'] is True and rec['report_sha256']==sha(base/'report.json');assert rec['spec']['parameters']['initial_capital_usdt']==20000 and [x['weight'] for x in rec['spec']['components']]==[1,1]
 hold={'report':rel(base/'report.json'),'report_sha256':sha(base/'report.json'),'name':refname,'fingerprint':ref['fingerprint'],'archive':ref['archive'],'archive_sha256':ref['archive_sha256'],'original_status':rec['status'],'policy':'Existing samebudget20000USDT/1+1funded constantlong parent readonly;no new reserve/backtest.'};assert sha(ROOT/hold['archive'])==hold['archive_sha256']
 rulehash=hashlib.sha256(json.dumps({'logic':p20['rules'],'costs':p20['costs']},sort_keys=True,separators=(',',':')).encode()).hexdigest();plan={'round':R.name,'frozen_at_utc':now(),'trigger_utc':'2026-10-23T20:43:26.146Z','hypothesis':'Known20/25/30day zero-exitperpetual BTC/ETH components may diversify foldtiming when funded independently. Evaluatefull4Dcrossgrid,not only priorETHpositivecells. This followsseenhistory and is not independentconfirmation.','grid':{'BTC_lookback_days':LOOKS,'BTC_return_hurdle':HURDLES,'ETH_lookback_days':LOOKS,'ETH_return_hurdle':HURDLES,'candidate_parent_configs':81,'new_parent_references':0,'new_component_backtests':0,'raw_component_multipliers':[1,1],'cost_multipliers':[1,2,3],'preset_center':{'BTC_lookback_days':25,'BTC_return_hurdle':.02,'ETH_lookback_days':25,'ETH_return_hurdle':.02}},'time_boundaries':p25['time_boundaries'],'data':p25['data'],'component_sources':refs,'component_rule_definition':p20['rules'],'component_costs':p20['costs'],'source_rules_and_costs_sha256':rulehash,'source_engine':{'path':rel(s20/'engine.py'),'sha256':sha(s20/'engine.py')},'read_only_hold_reference':hold,'rules':original['rules'],'sensitivity':original['sensitivity'],'gates':original['gates'],'sources':[{'url':'https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum','access_date':'2026-10-23','scope':'Original2012traditionalmultiassetfuturesown-returnmomentum background;this20/25/30daycrypto zero-exit portfolio is a separate hypothesis,notreplicationorprofitproof.'},{'url':'https://www.aqr.com/insights/research/journal-article/a-century-of-evidence-on-trend-following-investing','access_date':'2026-10-23','scope':'Author2017multi-markettrenddiversification motivation only;BTC/ETH actualcovariance/qualifications measuredhere.'},{'url':'https://www.binance.com/en/support/faq/detail/360033525031','access_date':'2026-10-23','scope':'Actualposition fundingcashflows;stored realizedrates onlyex-post accounting,not signals.'},{'url':'https://www.binance.com/en/support/faq/detail/360033525271','access_date':'2026-10-23','scope':'MarkvsLast andcollateralrisk;sourcehourlymark/1percentmarginproxy nottruetickliquidation.'}],'limits':p25['limits']+['No new market sample:known330dayhistoryandknowncomponents;fulljointgridnotindependentfinaltest.','Sourceshave identicalactualaxes here;asynchronouscarryonlysyntheticallytested.','Raw1/1fundedbanks20k;eachmarginproxy independent,nocross-sleevebailout.']}
 plan['sensitivity']='Full4D81grid,allfouraxesuse20/25/30lookbacksand1/2/4percenthurdles;inclusiveadjacentindexneighborhood;corner16,center81. Fixed-lookback2Dthresholdslices descriptiveonly. No post-result extension.'
 put(R/'plan.json',plan);(R/'specs').mkdir();batch=[];by={(x['asset'],x['lookback_days'],x['return_hurdle']):fp for fp,x in refs.items()}
 for lb,hb,le,he in itertools.product(LOOKS,HURDLES,LOOKS,HURDLES):
  name=f'perp_zero_pair_B{lb}H{int(hb*100):02d}_E{le}H{int(he*100):02d}';fps=[by['BTC',lb,hb],by['ETH',le,he]];spec={'kind':'combination','family':'two-asset-passive-perpetual-momentum-sleeves','name':name,'logic':plan['rules'],'parameters':{'initial_capital_usdt':20000,'raw_component_multipliers':[1,1],'component_capitals_usdt':[10000,10000],'component_initial_entry_notionals_usdt':[2000,2000],'BTC_lookback_days':lb,'BTC_return_hurdle':hb,'ETH_lookback_days':le,'ETH_return_hurdle':he,'start_utc':plan['time_boundaries']['oos_start_utc'],'end_utc':plan['time_boundaries']['oos_end_exclusive_utc'],'walk_forward_folds':11,'walk_forward_test_days':30,'warmup_days':30,'embargo_days':3,'cost_multipliers':[1,2,3],'source_rules_and_costs_sha256':rulehash},'components':[{'fingerprint':fp,'weight':1} for fp in fps],'validation_plan':rel(R/'plan.json'),'sources':plan['sources']};path=R/'specs'/(name+'.json');put(path,spec);fp=reg.fingerprint(spec);assert fp not in records or records[fp].get('result_available') is not True and records[fp]['status'] in ['blocked','abandoned'];batch.append({'name':name,'role':'candidate','spec':rel(path),'fingerprint':fp,'BTC_lookback_days':lb,'BTC_return_hurdle':hb,'ETH_lookback_days':le,'ETH_return_hurdle':he,'source_fingerprints':fps})
 assert len(batch)==len({x['fingerprint'] for x in batch})==81;put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/perp_zero_pair_B25H02_E25H02.json').read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_AND_RESERVED81_NO_OLD_COMPONENT_RETEST',sha(R/'plan.json'),flush=True)

def recover(plan):
 oldengine=module(ROOT/plan['source_engine']['path'],'immutable_perp_axis_engine');assert sha(ROOT/plan['source_engine']['path'])==plan['source_engine']['sha256'];markets={a:oldengine.load_market(a,x) for a,x in plan['data']['assets'].items()};common=align(markets);vectors={};scenes={};records=reg.read_records(ROOT/'research/automation/registry.jsonl')
 for fp,ref in plan['component_sources'].items():
  assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'] and records[fp]['status']==ref['original_status'] and records[fp]['report_sha256']==ref['report_sha256'];arc=readgz(ROOT/ref['archive']);m=markets[ref['asset']];scenes[fp]={}
  for k,s in arc['scenes'].items():
   v=np.empty(len(m['ts']));coverage=0
   for seg in s['state_segments']:
    a,b=seg['axis_start'],seg['axis_end_exclusive'];assert a==coverage and b>a;v[a:b]=float(seg['cash'])+float(seg['signed_units'])*(m['axis_prices'][a:b]-float(seg['entry_price']));coverage=b
   assert coverage==len(v) and oldengine.navhash(v)==ref['NAV_sha256_by_cost'][k]==s['summary']['NAV_sha256_f64le'];vectors[fp,k]=v[common['projections'][ref['asset']]];scenes[fp][k]=s['summary']
 return oldengine,markets,common,vectors,scenes

def metric(v,daily,days):
 r=[b/a-1 for a,b in zip(daily,daily[1:])];sd=__import__('statistics').stdev(r);dd=100*float(np.max(1-v/np.maximum.accumulate(v)));cagr=100*((v[-1]/v[0])**(365/days)-1)
 return {'net_return_pct':float(100*(v[-1]/v[0]-1)),'max_drawdown_pct':dd,'daily_mark_drawdown_pct':100*float(np.max(1-np.asarray(daily)/np.maximum.accumulate(daily))),'sharpe_365':__import__('statistics').mean(r)/sd*math.sqrt(365) if sd else None,'cagr_pct':float(cagr),'calmar':float(cagr/dd) if dd else None}

def summarize(v,parts,common):
 daily=v[common['daily_indices']].tolist();s=metric(v,daily,330);s['folds']=[];start=datetime.fromisoformat('2025-10-19T00:01:00+00:00')
 for j,(a,b) in enumerate(zip(common['fold_indices'],common['fold_indices'][1:])):
  dt=__import__('datetime').timedelta;s['folds'].append({'fold':j+1,'start_utc':(start+dt(days=j*30)).isoformat().replace('+00:00','Z'),'end_exclusive_utc':(start+dt(days=(j+1)*30)).isoformat().replace('+00:00','Z'),**metric(v[a:b+1],daily[j*30:(j+1)*30+1],30)})
 assert abs(math.prod(1+f['net_return_pct']/100 for f in s['folds'])-v[-1]/v[0])<1e-12;cost=sum(x['cost_usdt'] for x in parts);fund=sum(x['funding_usdt'] for x in parts);gross=sum(x['gross_reference_price_PnL_usdt'] for x in parts);assert abs(gross+fund-cost-(v[-1]-20000))<1e-8
 fields=['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','gross_reference_price_PnL_usdt','executions','round_trips','rejected_orders','cash_or_units_violations','funding_settlements','nonzero_funding_settlements'];s.update({f:sum(x[f] for x in parts) for f in fields});s.update(initial_capital_usdt=20000,final_NAV_usdt=float(v[-1]),cost_pct_initial=cost/20000*100,cost_parts_usdt={p:sum(x['cost_parts_usdt'][p] for x in parts) for p in ['fee','half_spread','slippage','impact','tick_rounding']},gross_reference_PnL_to_execution_cost=(gross+fund)/cost if cost else None,terminal_units=str(sum(D(x['terminal_units']) for x in parts)),daily_equity_usdt=daily,NAV_points=len(v),NAV_sha256_f64le=hashlib.sha256(v.astype('<f8',copy=False).tobytes()).hexdigest(),axis_sha256=common['sha256'],margin={'independent_sleeve_violations':sum(x['margin']['violations'] for x in parts),'minimum_individual_sleeve_cushion_usdt':min(x['margin']['minimum_equity_minus_maintenance_usdt'] for x in parts),'no_cross_margin_netting':True});return s

def neighbors(c,configs):
 axes={'BTC_lookback_days':LOOKS,'ETH_lookback_days':LOOKS,'BTC_return_hurdle':HURDLES,'ETH_return_hurdle':HURDLES};return [x for x in configs.values() if x['role']=='candidate' and all(abs(a.index(x[p])-a.index(c[p]))<=1 for p,a in axes.items())]

def evaluate():
 assert not (R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(records[x['fingerprint']]['status']=='reserved' for x in batch);started=now();oldengine,markets,common,vectors,ss=recover(plan);(R/'results').mkdir();configs={}
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());scenes={};fps=row['source_fingerprints'];arc={'spec':spec,'fingerprint':row['fingerprint'],'source_fingerprints':fps,'scenes':{}}
  for k in ['1','2','3']:
   v=vectors[fps[0],k]+vectors[fps[1],k];s=summarize(v,[ss[fp][k] for fp in fps],common);scenes[k]=s;arc['scenes'][k]={'summary':s,'source_full_NAV_sha256':[plan['component_sources'][fp]['NAV_sha256_by_cost'][k] for fp in fps]}
  path=R/'results'/(row['name']+'.json.gz');gzwrite(path,arc);configs[row['name']]={**row,'archive':rel(path),'archive_sha256':sha(path),'scenes':scenes,'positive_folds_1x':sum(x['net_return_pct']>0 for x in scenes['1']['folds'])};print(row['name'],scenes['1']['net_return_pct'],scenes['3']['net_return_pct'],flush=True)
 for c in configs.values():
  if c['role']=='benchmark':c.update(status='rejected',criteria={'reference_only_no_alpha_qualification':False},sensitivity={'reference_only':True});continue
  ns=neighbors(c,configs);frac=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);c['sensitivity']={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'four_dimensional_local_3x_positive_fraction':frac};s=c['scenes'];ratio=s['1']['gross_reference_PnL_to_execution_cost'];c['criteria']={'positive_all_costs':all(x['net_return_pct']>0 for x in s.values()),'eight_positive_1x_folds':c['positive_folds_1x']>=8,'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'full4D_neighbourhood_positive3_gte60pct':frac>=.6,'four_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_sleeve_collateral':all(x['cash_or_units_violations']==0 for x in s.values()),'no_source_order_rejections':all(x['rejected_orders']==0 for x in s.values()),'no_either_sleeve_margin_violations':all(x['margin']['independent_sleeve_violations']==0 for x in s.values()),'terminal_flat':all(D(x['terminal_units'])==0 for x in s.values())};c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 cs=[x for x in configs.values() if x['role']=='candidate'];report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':plan['time_boundaries'],'component_sources':plan['component_sources'],'input_data':plan['data'],'configs':configs,'summary':{'new_configs':81,'candidate_configs':81,'benchmark_configs':0,'new_component_backtests':0,'source_configs_reused_read_only':18,'source_cost_scenes_hash_verified':54,'cost_scenarios':243,'passed':[x['name'] for x in cs if x['status']=='passed'],'rejected':[x['name'] for x in cs if x['status']=='rejected'],'positive_configs_by_cost':{k:sum(x['scenes'][k]['net_return_pct']>0 for x in cs) for k in ['1','2','3']}},'axis':{'source_points':{a:len(m['ts']) for a,m in markets.items()},'union_points':len(common['keys']),'union_axis_sha256':common['sha256'],'projection_policy':'Lastcompleted (ts,eventcode)sourceNAVobservation;nointerpolation,no normalization.','daily_boundaries':len(common['daily_indices']),'folds':len(common['fold_indices'])-1},'scope':plan['limits']};put(R/'report.json',report);print('SUMMARY',json.dumps(report['summary']),flush=True)

def finish():
 report=json.loads((R/'report.json').read_text());done=[]
 for row in json.loads((R/'batch.json').read_text()):done.append(call('finish',row,report['configs'][row['name']]['status'],rel(R/'report.json')));put(R/'finish.json',done)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','finish']);globals()[p.parse_args().command]()
