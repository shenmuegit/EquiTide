"""Pre-register,backtest and finish a fixed two-parameter exit-buffer experiment."""
import argparse,copy,gzip,hashlib,importlib.util,itertools,json,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
import engine
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
LOOKS,HURDLES,EXITS=[30],[.01,.02,.04],[0,.0025,.005,.01]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
def gzwrite(p,x):p.write_bytes(gzip.compress(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode(),mtime=0))
def call(command,row,*args):
 p=subprocess.run([sys.executable,'research/automation/registry.py',command,row['spec'],*args],cwd=ROOT,capture_output=True,text=True);x={'name':row['name'],'fingerprint':row['fingerprint'],'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};print(json.dumps(x),flush=True);assert p.returncode==0 and p.stdout.strip()==row['fingerprint'];return x
def anchor_configs():
 p=json.loads((R/'plan.json').read_text())['anchor_source'];assert sha(ROOT/p['report'])==p['report_sha256'];old=json.loads((ROOT/p['report']).read_text());refs=json.loads((R/'anchors.json').read_text());out={}
 for name,ref in refs.items():
  c=old['configs'][name];assert c['fingerprint']==ref['fingerprint'] and c['status']==ref['original_status'] and c['lookback_days']==30;out[name]={**c,'exit_buffer_fraction':0,'read_only_anchor':True}
 assert len(out)==6;return out
def grid_configs(configs):return {**anchor_configs(),**configs}
def neighbors(c,configs):return [x for x in configs.values() if x['asset']==c['asset'] and abs(EXITS.index(x['exit_buffer_fraction'])-EXITS.index(c['exit_buffer_fraction']))<=1 and abs(HURDLES.index(x['return_hurdle'])-HURDLES.index(c['return_hurdle']))<=1]
def freeze():
 assert not (R/'plan.json').exists();ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');src=ROOT/'research/experiments/20261023T184400Z';plan=copy.deepcopy(json.loads((src/'plan.json').read_text()));old=json.loads((src/'report.json').read_text())
 signal='At daily decision i,priorcompletedperpetualROC=C[i-1]/C[i-1-L]-1. Flat enterslong iff ROC>H,short iff ROC<-H. Inside or on entrybands,existinglong persists strictly while ROC>-E;existingshort persists strictly while ROC<E. Long exits at ROC<=-E;short exits at ROC>=E. Crossing opposite strict fullentryband closesold then opensopposite at00:01. E<=H,at exact +/-H no newentry. State is actualsignedquantity,no unpublishedprice/funding input.'
 plan.update(round=R.name,trigger_utc='2026-10-24T02:43:26.625Z',frozen_at_utc=now(),hypothesis='A small symmetric exit buffer around zeroROC may reduce whipsaws/cost while increasing delayed-exit losses. Joint entryH and exitE grid at fixed30daylookback for BTC and ETH. This is a seen-history development hypothesis,not final independent validation.')
 plan['rules']['signal']=signal;plan['grid']={'lookback_days':[30],'return_hurdle':HURDLES,'exit_buffer_fraction':EXITS,'assets':['BTC','ETH'],'new_financial_candidates':18,'read_only_anchor_configs':6,'full_grid_configs':24,'preset_center':{'return_hurdle':.02,'exit_buffer_fraction':.005}}
 plan['anchor_source']={'report':rel(src/'report.json'),'report_sha256':sha(src/'report.json'),'plan':rel(src/'plan.json'),'plan_sha256':sha(src/'plan.json'),'engine':rel(src/'engine.py'),'engine_sha256':sha(src/'engine.py'),'policy':'Only6oldL30zero-exit anchorsreadonly;no oldbacktest,NAV/status rerating or registry event.'}
 plan['sensitivity']='Full2D perasset:entry1/2/4percent x exitbuffer0/.25/.5/1percent. Zero row6oldanchorsreadonly.18newcells preregistered;inclusiveadjacent-index neighbors in bothaxes. LargestE/H boundaries retained,notextendedafterresults.'
 plan['new_engine_change_scope']='Only target signature/persistence and passing E from spec. Signed collateral/costs/funding/marketaxis/margin/statistics byte-for-byte same functions as original zeroexit engine;tests compare original source functions.'
 plan['novelty']={'initial16_missing_actual_results':0,'prior_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_canonical_non_observation_definitions':ctx['canonical_research_definitions_excluding_observations'],'prior_conclusions_read':len(ctx['prior_conclusions_read']),'multiple_testing':'Same330dayhistory reused;no DSR/PBO or untouchedfinaltest.'}
 plan['read_only_hold_references']={}
 holdroot=ROOT/'research/experiments/20261023T124125Z';holds=json.loads((holdroot/'report.json').read_text())
 for a in ['BTC','ETH']:
  c=holds['configs']['perp_hold_'+a];rec=records[c['fingerprint']];assert rec['result_available'] is True and rec['report_sha256']==sha(holdroot/'report.json');plan['read_only_hold_references'][a]={'name':c['name'],'fingerprint':c['fingerprint'],'report':rel(holdroot/'report.json'),'report_sha256':sha(holdroot/'report.json'),'archive':c['archive'],'archive_sha256':c['archive_sha256'],'original_status':rec['status']}
 for s in plan['sources']:
  s['access_date']='2026-10-24'
  if 'aqr.com' in s['url']:s['scope']='2012authortraditional12monthmulti-futuresownreturnmomentum background only;30daycrypto buffered-exit grid is our developmenthypothesis,notreplication.'
 for files in plan['data']['assets'].values():
  for x in files:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 refs={}
 for name,c in old['configs'].items():
  if c['lookback_days']!=30:continue
  rec=records[c['fingerprint']];assert rec['result_available'] is True and rec['report_sha256']==sha(src/'report.json') and rec['status']==c['status'];refs[name]={'name':name,'fingerprint':c['fingerprint'],'asset':c['asset'],'lookback_days':30,'return_hurdle':c['return_hurdle'],'exit_buffer_fraction':0,'original_status':c['status'],'source_report':rel(src/'report.json'),'source_report_sha256':sha(src/'report.json'),'source_spec':c['spec'],'source_spec_sha256':sha(ROOT/c['spec']),'source_archive':c['archive'],'source_archive_sha256':c['archive_sha256'],'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()}}
 assert len(refs)==6;put(R/'plan.json',plan);put(R/'anchors.json',refs);(R/'specs').mkdir();batch=[]
 for asset,H,E in itertools.product(['BTC','ETH'],HURDLES,EXITS[1:]):
  template=old['configs'][f'perp_zeroexit_{asset}_L30_H{int(H*100):02d}'];spec=copy.deepcopy(json.loads((ROOT/template['spec']).read_text()));name=f'perp_bufferexit_{asset}_L30_H{int(H*100):02d}_E{int(E*10000):03d}bp';spec['name']=name;spec['family']='perpetual-daily-signed-momentum-buffered-exit-hysteresis';spec['logic']['signal']=signal;p=spec['parameters'];p.pop('exit_ROC');p['exit_buffer_fraction']=E;p['persistence']='Keep actual long while ROC>-E or short while ROC<E inside entrybands;strict entrybands have priority,unchanged quantity.';spec['validation_plan']=rel(R/'plan.json');spec['sources']=plan['sources'];path=R/'specs'/(name+'.json');put(path,spec);fp=reg.fingerprint(spec);assert fp not in records or records[fp].get('result_available') is not True and records[fp]['status'] in ['blocked','abandoned'];batch.append({'name':name,'role':'candidate','spec':rel(path),'fingerprint':fp,'asset':asset,'lookback_days':30,'return_hurdle':H,'exit_buffer_fraction':E,'capital_usdt':10000})
 assert len(batch)==len({x['fingerprint'] for x in batch})==18;put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/perp_bufferexit_ETH_L30_H02_E050bp.json').read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_RESERVED18_NEW_BUFFEREXIT_6OLD_ZEROEXIT_READONLY',sha(R/'plan.json'),flush=True)
def evaluate():
 assert not (R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(records[x['fingerprint']]['status']=='reserved' for x in batch);started=now();markets={a:engine.load_market(a,x) for a,x in plan['data']['assets'].items()};configs={};(R/'results').mkdir()
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());arc={'spec':spec,'fingerprint':row['fingerprint'],'scenes':{}};scenes={}
  for k in ['1','2','3']:v,z=engine.simulate(spec,markets[row['asset']],int(k));arc['scenes'][k]=z;scenes[k]=z['summary']
  path=R/'results'/(row['name']+'.json.gz');gzwrite(path,arc);configs[row['name']]={**row,'archive':rel(path),'archive_sha256':sha(path),'scenes':scenes,'positive_folds_1x':sum(x['net_return_pct']>0 for x in scenes['1']['folds'])};print(row['name'],scenes['1']['net_return_pct'],scenes['3']['net_return_pct'],flush=True)
 grid=grid_configs(configs)
 for c in configs.values():
  ns=neighbors(c,grid);frac=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);c['sensitivity']={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'local_3x_neighbor_positive_fraction':frac};s=c['scenes'];ratio=s['1']['gross_reference_PnL_to_execution_cost'];c['criteria']={'positive_all_costs':all(x['net_return_pct']>0 for x in s.values()),'eight_positive_1x_folds':c['positive_folds_1x']>=8,'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'neighbourhood_positive3_gte60pct':frac>=.6,'four_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_collateral':all(x['cash_or_units_violations']==0 for x in s.values()),'no_order_rejections':all(x['rejected_orders']==0 for x in s.values()),'no_margin_proxy_violations':all(x['margin']['violations']==0 for x in s.values()),'terminal_flat':all(float(x['terminal_units'])==0 for x in s.values())};c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 cs=list(configs.values());report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'anchor_source_report_sha256':plan['anchor_source']['report_sha256'],'time_boundaries':plan['time_boundaries'],'input_data':plan['data'],'configs':configs,'summary':{'new_configs':18,'candidate_configs':18,'benchmark_configs':0,'cost_scenarios':54,'read_only_anchor_configs':6,'read_only_anchor_cost_scenes':18,'full_grid_configs':24,'passed':[c['name'] for c in cs if c['status']=='passed'],'rejected':[c['name'] for c in cs if c['status']=='rejected'],'positive_configs_by_cost':{k:sum(c['scenes'][k]['net_return_pct']>0 for c in cs) for k in ['1','2','3']}},'scope':plan['limits'],'axis':{a:{'points':len(m['ts']),'axis_sha256':m['axis_sha256'],'axis_prices_sha256_f64le':m['axis_price_sha256_f64le'],'daily_boundary_count':len(m['daily_indices']),'folds':len(m['fold_indices'])-1} for a,m in markets.items()},'read_only_anchor_references':json.loads((R/'anchors.json').read_text()),'anchor_original_statuses_unchanged':True};put(R/'report.json',report);print(json.dumps(report['summary']),flush=True)
def finish():
 report=json.loads((R/'report.json').read_text());done=[]
 for row in json.loads((R/'batch.json').read_text()):done.append(call('finish',row,report['configs'][row['name']]['status'],rel(R/'report.json')));put(R/'finish.json',done)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','finish']);globals()[p.parse_args().command]()
