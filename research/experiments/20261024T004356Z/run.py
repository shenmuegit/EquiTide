"""Extend the ETH lookback boundary using immutable component NAV, not new trades."""
import argparse,copy,gzip,hashlib,importlib.util,itertools,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
from decimal import Decimal as D
import numpy as np
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
BTC_LOOKS,ETH_LOOKS,HURDLES=[20,25,30],[30,31,32],[.01,.02,.04]
LOOKS=BTC_LOOKS
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
 plan=json.loads((R/'plan.json').read_text());a=plan['anchor_source'];assert sha(ROOT/a['report'])==a['report_sha256'];doc=json.loads((ROOT/a['report']).read_text());refs=json.loads((R/'anchors.json').read_text());out={}
 for name,ref in refs.items():
  c=doc['configs'][name];assert c['fingerprint']==ref['fingerprint'] and c['status']==ref['original_status'] and c['ETH_lookback_days']==30;out[name]=c
 assert len(out)==27;return out
def grid_configs(configs):return {**anchor_configs(),**configs}
def neighbors(c,configs):
 axes={'BTC_lookback_days':BTC_LOOKS,'ETH_lookback_days':ETH_LOOKS,'BTC_return_hurdle':HURDLES,'ETH_return_hurdle':HURDLES}
 return [x for x in configs.values() if all(abs(a.index(x[p])-a.index(c[p]))<=1 for p,a in axes.items())]
def freeze():
 assert not (R/'plan.json').exists();ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');oldroot=ROOT/'research/experiments/20261023T204326Z';oldplan=json.loads((oldroot/'plan.json').read_text());oldreport=json.loads((oldroot/'report.json').read_text());plan=copy.deepcopy(oldplan)
 refs={fp:r for fp,r in oldplan['component_sources'].items() if r['asset']=='BTC' or r['lookback_days']==30}
 newroot=ROOT/'research/experiments/20261023T224328Z';newplan=json.loads((newroot/'plan.json').read_text());newreport=json.loads((newroot/'report.json').read_text())
 assert newplan['rules']==oldplan['component_rule_definition'] and newplan['costs']==oldplan['component_costs']
 assert sha(newroot/'engine.py')==oldplan['source_engine']['sha256']
 for name,c in newreport['configs'].items():
  fp=c['fingerprint'];rec=records[fp];assert c['asset']=='ETH' and c['lookback_days'] in [31,32] and rec['result_available'] is True and rec['report_sha256']==sha(newroot/'report.json') and sha(ROOT/c['archive'])==c['archive_sha256']
  refs[fp]={'name':name,'asset':'ETH','role':'candidate','lookback_days':c['lookback_days'],'return_hurdle':c['return_hurdle'],'report':rel(newroot/'report.json'),'report_sha256':sha(newroot/'report.json'),'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'archive':c['archive'],'archive_sha256':c['archive_sha256'],'original_status':rec['status'],'capital_usdt':10000,'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()}}
 assert len(refs)==18 and all(sum(x['asset']==a for x in refs.values())==9 for a in ['BTC','ETH'])
 for fp,ref in refs.items():
  assert records[fp]['status']==ref['original_status'] and records[fp]['report_sha256']==ref['report_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'] and sha(ROOT/ref['spec'])==ref['spec_sha256']
 plan.update(round=R.name,trigger_utc='2026-10-24T00:43:56.279Z',frozen_at_utc=now(),hypothesis='Extend the previously seen ETH30 boundary to31/32 in passive BTC/ETH portfolios. All81 cells predeclared:27 old ETH30 parents readonly,54 new ETH31/32 parents. Known-history extension,not independent confirmation.',component_sources=refs)
 plan['grid']={'BTC_lookback_days':BTC_LOOKS,'BTC_return_hurdle':HURDLES,'ETH_lookback_days':ETH_LOOKS,'ETH_return_hurdle':HURDLES,'candidate_parent_configs':54,'read_only_anchor_configs':27,'full_grid_configs':81,'new_component_backtests':0,'raw_component_multipliers':[1,1],'cost_multipliers':[1,2,3],'preset_center':{'BTC_lookback_days':25,'BTC_return_hurdle':.02,'ETH_lookback_days':31,'ETH_return_hurdle':.02}}
 plan['sensitivity']='Full4D81cells. Inclusive adjacent-index neighborhood across BTC20/25/30,ETH30/31/32,and each hurdle1/2/4percent. 27 oldETH30cells readonly with their original qualification unchanged; only54newcells qualified under this frozen grid. No post-result grid extension.'
 plan['anchor_source']={'report':rel(oldroot/'report.json'),'report_sha256':sha(oldroot/'report.json'),'policy':'27ETH30parents read-only;do not recompute NAV,original neighborhood,status or reserve/finish.'}
 plan['novelty']={'prior_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_conclusions_read':len(ctx['prior_conclusions_read']),'initial16_missing_actual_results':0,'lookback_ceiling':32,'L33_prohibited_with_current_inputs':True}
 plan['sources']=[x for x in plan['sources'] if 'a-century' not in x['url']]
 for s in plan['sources']:
  s['access_date']='2026-10-24'
  if 'aqr.com' in s['url']:s['scope']='2012 traditional 12month multi-futures own-return momentum background only;our crypto20/25/30 and30/31/32day zero-exit portfolio is a separate development hypothesis.'
 for files in plan['data']['assets'].values():
  for x in files:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 anchors={name:{'name':name,'fingerprint':c['fingerprint'],'original_status':c['status'],'report':rel(oldroot/'report.json'),'report_sha256':sha(oldroot/'report.json'),'archive':c['archive'],'archive_sha256':c['archive_sha256']} for name,c in oldreport['configs'].items() if c['ETH_lookback_days']==30}
 assert len(anchors)==27
 for ref in anchors.values():assert records[ref['fingerprint']]['report_sha256']==ref['report_sha256'] and records[ref['fingerprint']]['status']==ref['original_status']
 put(R/'plan.json',plan);put(R/'anchors.json',anchors);(R/'specs').mkdir();by={(x['asset'],x['lookback_days'],x['return_hurdle']):fp for fp,x in refs.items()};batch=[]
 for lb,hb,le,he in itertools.product(BTC_LOOKS,HURDLES,[31,32],HURDLES):
  name=f'perp_zero_pair_B{lb}H{int(hb*100):02d}_E{le}H{int(he*100):02d}';template=oldreport['configs'][f'perp_zero_pair_B{lb}H{int(hb*100):02d}_E30H{int(he*100):02d}'];spec=copy.deepcopy(json.loads((ROOT/template['spec']).read_text()));spec['name']=name;spec['parameters']['ETH_lookback_days']=le;fps=[by['BTC',lb,hb],by['ETH',le,he]];spec['components']=[{'fingerprint':fp,'weight':1} for fp in fps];spec['validation_plan']=rel(R/'plan.json');spec['sources']=plan['sources'];p=R/'specs'/(name+'.json');put(p,spec);fp=reg.fingerprint(spec);assert fp not in records or records[fp].get('result_available') is not True and records[fp]['status'] in ['blocked','abandoned'];batch.append({'name':name,'role':'candidate','spec':rel(p),'fingerprint':fp,'BTC_lookback_days':lb,'BTC_return_hurdle':hb,'ETH_lookback_days':le,'ETH_return_hurdle':he,'source_fingerprints':fps})
 assert len(batch)==len({x['fingerprint'] for x in batch})==54;put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/perp_zero_pair_B25H02_E31H02.json').read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_RESERVED54_NEW_PARENTS_27OLD_READONLY',sha(R/'plan.json'),flush=True)
def evaluate():
 assert not (R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(records[x['fingerprint']]['status']=='reserved' for x in batch);started=now();oldengine,markets,common,vectors,ss=recover(plan);(R/'results').mkdir();configs={}
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());fps=row['source_fingerprints'];scenes={};arc={'spec':spec,'fingerprint':row['fingerprint'],'source_fingerprints':fps,'scenes':{}}
  for k in ['1','2','3']:
   v=vectors[fps[0],k]+vectors[fps[1],k];s=summarize(v,[ss[fp][k] for fp in fps],common);scenes[k]=s;arc['scenes'][k]={'summary':s,'source_full_NAV_sha256':[plan['component_sources'][fp]['NAV_sha256_by_cost'][k] for fp in fps]}
  p=R/'results'/(row['name']+'.json.gz');gzwrite(p,arc);configs[row['name']]={**row,'archive':rel(p),'archive_sha256':sha(p),'scenes':scenes,'positive_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'])};print(row['name'],scenes['1']['net_return_pct'],scenes['3']['net_return_pct'],flush=True)
 grid=grid_configs(configs)
 for c in configs.values():
  ns=neighbors(c,grid);frac=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);c['sensitivity']={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'four_dimensional_local_3x_positive_fraction':frac};s=c['scenes'];ratio=s['1']['gross_reference_PnL_to_execution_cost'];c['criteria']={'positive_all_costs':all(x['net_return_pct']>0 for x in s.values()),'eight_positive_1x_folds':c['positive_folds_1x']>=8,'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'full4D_neighbourhood_positive3_gte60pct':frac>=.6,'four_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_sleeve_collateral':all(x['cash_or_units_violations']==0 for x in s.values()),'no_source_order_rejections':all(x['rejected_orders']==0 for x in s.values()),'no_either_sleeve_margin_violations':all(x['margin']['independent_sleeve_violations']==0 for x in s.values()),'terminal_flat':all(D(x['terminal_units'])==0 for x in s.values())};c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 cs=list(configs.values());report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':plan['time_boundaries'],'component_sources':plan['component_sources'],'input_data':plan['data'],'configs':configs,'read_only_anchor_references':json.loads((R/'anchors.json').read_text()),'summary':{'new_configs':54,'candidate_configs':54,'benchmark_configs':0,'new_component_backtests':0,'source_configs_reused_read_only':18,'source_cost_scenes_hash_verified':54,'cost_scenarios':162,'read_only_anchor_configs':27,'full_grid_configs':81,'passed':[x['name'] for x in cs if x['status']=='passed'],'rejected':[x['name'] for x in cs if x['status']=='rejected'],'positive_configs_by_cost':{k:sum(x['scenes'][k]['net_return_pct']>0 for x in cs) for k in ['1','2','3']}},'axis':{'source_points':{a:len(m['ts']) for a,m in markets.items()},'union_points':len(common['keys']),'union_axis_sha256':common['sha256'],'projection_policy':'Last completed(ts,eventcode)sourceNAV observation;no interpolation or normalization.','daily_boundaries':len(common['daily_indices']),'folds':len(common['fold_indices'])-1},'scope':plan['limits']};put(R/'report.json',report);print(json.dumps(report['summary']),flush=True)
def finish():
 report=json.loads((R/'report.json').read_text());done=[]
 for row in json.loads((R/'batch.json').read_text()):done.append(call('finish',row,report['configs'][row['name']]['status'],rel(R/'report.json')));put(R/'finish.json',done)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','finish']);globals()[p.parse_args().command]()
