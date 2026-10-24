"""Passive BTC buffered-exit / ETH zero-exit portfolios from immutable NAV."""
import argparse,copy,gzip,hashlib,importlib.util,itertools,json,subprocess,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
HURDLES,BUFFERS=[.01,.02,.04],[0,.0025,.005,.01]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
readgz=lambda p:json.loads(gzip.decompress(p.read_bytes()))
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
base=module(ROOT/'research/experiments/20261023T204326Z/run.py','immutable_parent_helpers')
keys,align,metric,summarize,recover=base.keys,base.align,base.metric,base.summarize,base.recover
def gzwrite(p,x):p.write_bytes(gzip.compress(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode(),mtime=0))
def call(command,row,*args):
 p=subprocess.run([sys.executable,'research/automation/registry.py',command,row['spec'],*args],cwd=ROOT,capture_output=True,text=True);x={'name':row['name'],'fingerprint':row['fingerprint'],'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};print(json.dumps(x),flush=True);assert p.returncode==0 and p.stdout.strip()==row['fingerprint'];return x
def anchor_configs():
 source=json.loads((R/'plan.json').read_text())['anchor_source'];assert sha(ROOT/source['report'])==source['report_sha256'];doc=json.loads((ROOT/source['report']).read_text());refs=json.loads((R/'anchors.json').read_text());out={}
 for name,ref in refs.items():
  c=doc['configs'][name];assert c['fingerprint']==ref['fingerprint'] and c['status']==ref['original_status'] and c['BTC_lookback_days']==c['ETH_lookback_days']==30;out[name]={**c,'BTC_exit_buffer_fraction':0,'read_only_anchor':True}
 assert len(out)==9;return out
def grid_configs(configs):return {**anchor_configs(),**configs}
def neighbors(c,configs):
 axes={'BTC_return_hurdle':HURDLES,'BTC_exit_buffer_fraction':BUFFERS,'ETH_return_hurdle':HURDLES}
 return [x for x in configs.values() if all(abs(a.index(x[p])-a.index(c[p]))<=1 for p,a in axes.items())]
def freeze():
 assert not (R/'plan.json').exists();ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');parentroot=ROOT/'research/experiments/20261023T204326Z';parent=json.loads((parentroot/'report.json').read_text());plan=copy.deepcopy(json.loads((parentroot/'plan.json').read_text()));broot=ROOT/'research/experiments/20261024T024326Z';eroot=ROOT/'research/experiments/20261023T184400Z';bp=json.loads((broot/'plan.json').read_text());ep=json.loads((eroot/'plan.json').read_text());assert bp['costs']==ep['costs'] and bp['data']==ep['data'] and bp['time_boundaries']==ep['time_boundaries'];refs={}
 for source,asset in [(broot,'BTC'),(eroot,'ETH')]:
  doc=json.loads((source/'report.json').read_text())
  for name,c in doc['configs'].items():
   if c['asset']!=asset or c['lookback_days']!=30:continue
   fp=c['fingerprint'];rec=records[fp];assert rec['result_available'] is True and rec['status']==c['status'] and rec['report_sha256']==sha(source/'report.json') and sha(ROOT/c['archive'])==c['archive_sha256'];spec=json.loads((ROOT/c['spec']).read_text());assert spec['parameters']['initial_capital_usdt']==10000 and spec['parameters']['fixed_entry_notional_usdt']==2000
   refs[fp]={'name':name,'asset':asset,'role':'candidate','lookback_days':30,'return_hurdle':c['return_hurdle'],'exit_buffer_fraction':c.get('exit_buffer_fraction',0),'report':rel(source/'report.json'),'report_sha256':sha(source/'report.json'),'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'archive':c['archive'],'archive_sha256':c['archive_sha256'],'original_status':rec['status'],'capital_usdt':10000,'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()}}
 assert len(refs)==12 and sum(x['asset']=='BTC' for x in refs.values())==9 and sum(x['asset']=='ETH' for x in refs.values())==3
 rulehash=hashlib.sha256(json.dumps({'BTC':bp['rules'],'ETH':ep['rules'],'costs':bp['costs']},sort_keys=True,separators=(',',':')).encode()).hexdigest()
 plan.update(round=R.name,trigger_utc='2026-10-24T04:43:26.733Z',frozen_at_utc=now(),hypothesis='BTC buffered exits may diversify ETH zero-exit fold timing despite each component failing standalone qualifications. Predeclare all27 new parents,not only profitable BTCcells. Entire component/history reused;not independent confirmation.',component_sources=refs,component_rule_definition={'BTC':bp['rules'],'ETH':ep['rules']},component_costs=bp['costs'],source_rules_and_costs_sha256=rulehash)
 plan['grid']={'BTC_lookback_days':30,'ETH_lookback_days':30,'BTC_return_hurdle':HURDLES,'BTC_exit_buffer_fraction':BUFFERS,'ETH_return_hurdle':HURDLES,'ETH_exit_buffer_fraction':0,'new_parent_configs':27,'read_only_anchor_configs':9,'full_grid_configs':36,'new_component_backtests':0,'raw_component_multipliers':[1,1],'cost_multipliers':[1,2,3],'preset_center':{'BTC_return_hurdle':.02,'BTC_exit_buffer_fraction':.005,'ETH_return_hurdle':.02}}
 plan['anchor_source']={'report':rel(parentroot/'report.json'),'report_sha256':sha(parentroot/'report.json'),'policy':'9oldBTC30/ETH30zero-exit parent results readonly;do not recomputeoldNAV,original4Dneighborhood,qualification or registry.'}
 plan['sensitivity']='Full3D36cells:BTCH1/2/4percent x BTCbuffer0/.25/.5/1percent x ETHH1/2/4percent. Bothlookbacks30,ETHbuffer0.9oldzeroBTCbuffer parents readonly;27newparents assessed. Inclusive adjacent-index3axis neighborhood,corner8,interior27;oldoriginalqualification unchanged.'
 oldkey='four_dimensional_local_3x_positive_fraction_min';assert plan['gates'].pop(oldkey)==.6;plan['gates']['three_dimensional_local_3x_positive_fraction_min']=.6
 plan['novelty']={'initial16_missing_actual_results':0,'prior_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_non_observation_definitions':ctx['canonical_research_definitions_excluding_observations'],'prior_conclusions_read':len(ctx['prior_conclusions_read']),'selection_bias':'Both components and entire330dayhistory previously seen;no DSR/PBO or untouchedfinaltest.'}
 plan['sources']=[x for x in plan['sources'] if 'a-century' not in x['url']]
 for x in plan['sources']:
  x['access_date']='2026-10-24'
  if 'aqr.com' in x['url']:x['scope']='2012traditional12monthfuturesmomentum background only;our30daycrypto bufferedBTC/zeroETH passive combination is a separate seen-historydevelopment hypothesis.'
 for files in plan['data']['assets'].values():
  for x in files:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 anchors={name:{'name':name,'fingerprint':c['fingerprint'],'original_status':c['status'],'report':rel(parentroot/'report.json'),'report_sha256':sha(parentroot/'report.json'),'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'archive':c['archive'],'archive_sha256':c['archive_sha256']} for name,c in parent['configs'].items() if c['BTC_lookback_days']==c['ETH_lookback_days']==30};assert len(anchors)==9
 for ref in anchors.values():assert records[ref['fingerprint']]['report_sha256']==ref['report_sha256'] and records[ref['fingerprint']]['status']==ref['original_status']
 put(R/'plan.json',plan);put(R/'anchors.json',anchors);(R/'specs').mkdir();batch=[];by={(r['asset'],r['return_hurdle'],r['exit_buffer_fraction']):fp for fp,r in refs.items()}
 for hb,eb,he in itertools.product(HURDLES,BUFFERS[1:],HURDLES):
  name=f'perp_buffer_pair_B30H{int(hb*100):02d}E{int(eb*10000):03d}bp_E30H{int(he*100):02d}';template=parent['configs'][f'perp_zero_pair_B30H{int(hb*100):02d}_E30H{int(he*100):02d}'];spec=copy.deepcopy(json.loads((ROOT/template['spec']).read_text()));spec['name']=name;p=spec['parameters'];p.update(BTC_exit_buffer_fraction=eb,ETH_exit_buffer_fraction=0,source_rules_and_costs_sha256=rulehash);fps=[by['BTC',hb,eb],by['ETH',he,0]];spec['components']=[{'fingerprint':fp,'weight':1} for fp in fps];spec['validation_plan']=rel(R/'plan.json');spec['sources']=plan['sources'];path=R/'specs'/(name+'.json');put(path,spec);fp=reg.fingerprint(spec);assert fp not in records or records[fp].get('result_available') is not True and records[fp]['status'] in ['blocked','abandoned'];batch.append({'name':name,'role':'candidate','spec':rel(path),'fingerprint':fp,'BTC_lookback_days':30,'BTC_return_hurdle':hb,'BTC_exit_buffer_fraction':eb,'ETH_lookback_days':30,'ETH_return_hurdle':he,'source_fingerprints':fps})
 assert len(batch)==len({x['fingerprint'] for x in batch})==27;put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/perp_buffer_pair_B30H02E050bp_E30H02.json').read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_RESERVED27NEWPARENTS_9OLDREADONLY_12SOURCECOMPONENTS',sha(R/'plan.json'),flush=True)
def evaluate():
 assert not (R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(records[x['fingerprint']]['status']=='reserved' for x in batch);started=now();oldengine,markets,common,vectors,ss=recover(plan);(R/'results').mkdir();configs={}
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());fps=row['source_fingerprints'];scenes={};arc={'spec':spec,'fingerprint':row['fingerprint'],'source_fingerprints':fps,'scenes':{}}
  for k in ['1','2','3']:
   v=vectors[fps[0],k]+vectors[fps[1],k];s=summarize(v,[ss[fp][k] for fp in fps],common);scenes[k]=s;arc['scenes'][k]={'summary':s,'source_full_NAV_sha256':[plan['component_sources'][fp]['NAV_sha256_by_cost'][k] for fp in fps]}
  p=R/'results'/(row['name']+'.json.gz');gzwrite(p,arc);configs[row['name']]={**row,'archive':rel(p),'archive_sha256':sha(p),'scenes':scenes,'positive_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'])};print(row['name'],scenes['1']['net_return_pct'],scenes['3']['net_return_pct'],flush=True)
 grid=grid_configs(configs)
 for c in configs.values():
  ns=neighbors(c,grid);frac=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);c['sensitivity']={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'three_dimensional_local_3x_positive_fraction':frac};s=c['scenes'];ratio=s['1']['gross_reference_PnL_to_execution_cost'];c['criteria']={'positive_all_costs':all(x['net_return_pct']>0 for x in s.values()),'eight_positive_1x_folds':c['positive_folds_1x']>=8,'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'full3D_neighbourhood_positive3_gte60pct':frac>=.6,'four_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_sleeve_collateral':all(x['cash_or_units_violations']==0 for x in s.values()),'no_source_order_rejections':all(x['rejected_orders']==0 for x in s.values()),'no_either_sleeve_margin_violations':all(x['margin']['independent_sleeve_violations']==0 for x in s.values()),'terminal_flat':all(D(x['terminal_units'])==0 for x in s.values())};c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 cs=list(configs.values());report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':plan['time_boundaries'],'component_sources':plan['component_sources'],'input_data':plan['data'],'configs':configs,'read_only_anchor_references':json.loads((R/'anchors.json').read_text()),'summary':{'new_configs':27,'candidate_configs':27,'benchmark_configs':0,'new_component_backtests':0,'source_configs_reused_read_only':12,'source_cost_scenes_hash_verified':36,'cost_scenarios':81,'read_only_anchor_configs':9,'full_grid_configs':36,'passed':[c['name'] for c in cs if c['status']=='passed'],'rejected':[c['name'] for c in cs if c['status']=='rejected'],'positive_configs_by_cost':{k:sum(c['scenes'][k]['net_return_pct']>0 for c in cs) for k in ['1','2','3']}},'axis':{'source_points':{a:len(m['ts']) for a,m in markets.items()},'union_points':len(common['keys']),'union_axis_sha256':common['sha256'],'projection_policy':'Last completed(ts,eventcode)sourceNAV,not interpolation or normalization.','daily_boundaries':len(common['daily_indices']),'folds':len(common['fold_indices'])-1},'scope':plan['limits']};put(R/'report.json',report);print(json.dumps(report['summary']),flush=True)
def finish():
 report=json.loads((R/'report.json').read_text());done=[]
 for row in json.loads((R/'batch.json').read_text()):done.append(call('finish',row,report['configs'][row['name']]['status'],rel(R/'report.json')));put(R/'finish.json',done)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','finish']);globals()[p.parse_args().command]()
