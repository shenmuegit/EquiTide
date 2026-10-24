"""Freeze the near-30-day zero-exit component neighborhood before evaluation."""
import copy,itertools,json
from run import ROOT,R,LOOKS,HURDLES,reg,sha,put,rel,now,call,validate_lookback
def main():
 assert not (R/'plan.json').exists();ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');base=ROOT/'research/experiments/20261023T184400Z';extended=ROOT/'research/experiments/20261023T224328Z';plan=copy.deepcopy(json.loads((base/'plan.json').read_text()));base_report=json.loads((base/'report.json').read_text());assert sha(R/'engine.py')==sha(base/'engine.py')==sha(extended/'engine.py')
 plan.update(round=R.name,trigger_utc='2026-10-24T08:44:57.143Z',frozen_at_utc=now(),hypothesis='Check whether the previously observed30dayzero-exit momentum performance is a local lookback plateau or an isolated cell. JointL28/29/30/31/32 andH1/2/4percent forbothassets. Twelve oldcellsreadonly;18missingexactcells new. Entiremarket history alreadyseen,not independentconfirmation.')
 plan['grid']={'lookback_days':LOOKS,'return_hurdle':HURDLES,'assets':['BTC','ETH'],'new_financial_candidates':18,'read_only_anchor_configs':12,'full_grid_configs':30,'new_parent_backtests':0,'preset_center':{'lookback_days':30,'return_hurdle':.02},'new_lookbacks_by_asset':{'BTC':[28,29,31,32],'ETH':[28,29]}}
 plan.pop('anchor_source',None);plan['anchor_sources']=[{'report':rel(base/'report.json'),'report_sha256':sha(base/'report.json'),'cells':6},{'report':rel(extended/'report.json'),'report_sha256':sha(extended/'report.json'),'cells':6}]
 plan['sensitivity']='Eachasset full5x3 grid L28/29/30/31/32 x H1/2/4percent.12oldcellsreadonly,18newcellspreregistered. Inclusiveadjacentindex2axisneighbors. Onlynewqualification computed;oldoriginalL20/25/30 orL30/31/32 grid qualification unchanged. No post-result expansion.'
 plan['lookback_availability']={'first_decision_day_index':33,'maximum_lookback':32,'earliest_completed_close_index':0,'indices_by_lookback':{str(L):32-L for L in LOOKS},'rule':'Fixed33completedcontextdays. L32 firstROC C32/C0;L33 wouldnegative-index the futuretail andisprohibited. No OOSstartshift.'}
 for L in LOOKS:validate_lookback(L)
 plan['novelty']={'initial16_missing_actual_results':0,'prior_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_canonical_non_observation_definitions':ctx['canonical_research_definitions_excluding_observations'],'all_prior_conclusions_read':len(ctx['prior_conclusions_read']),'multiple_testing':'Localgrid chosenbetweenrounds fromseenhistory;no untouchedfinaltest orDSR/PBO.'}
 plan['read_only_hold_references']={};holdroot=ROOT/'research/experiments/20261023T124125Z';holds=json.loads((holdroot/'report.json').read_text())
 for asset in ['BTC','ETH']:
  c=holds['configs']['perp_hold_'+asset];rec=records[c['fingerprint']];assert rec['result_available'] and rec['report_sha256']==sha(holdroot/'report.json');plan['read_only_hold_references'][asset]={'name':c['name'],'fingerprint':c['fingerprint'],'report':rel(holdroot/'report.json'),'report_sha256':sha(holdroot/'report.json'),'archive':c['archive'],'archive_sha256':c['archive_sha256'],'original_status':rec['status']}
 for s in plan['sources']:
  s['access_date']='2026-10-24'
  if 'aqr.com' in s['url']:s['scope']='Author2012traditional12monthmulti-futuresmomentum background only;our28to32daycryptozero-exitgrid is a separate development hypothesis,not a replication.'
 for files in plan['data']['assets'].values():
  for x in files:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 refs={}
 for source,valid in [(base,[30]),(extended,[31,32])]:
  doc=json.loads((source/'report.json').read_text())
  for name,c in doc['configs'].items():
   if c['lookback_days'] not in valid:continue
   rec=records[c['fingerprint']];assert rec['result_available'] is True and rec['report_sha256']==sha(source/'report.json') and rec['status']==c['status'];refs[name]={'name':name,'fingerprint':c['fingerprint'],'asset':c['asset'],'lookback_days':c['lookback_days'],'return_hurdle':c['return_hurdle'],'original_status':c['status'],'source_report':rel(source/'report.json'),'source_report_sha256':sha(source/'report.json'),'source_spec':c['spec'],'source_spec_sha256':sha(ROOT/c['spec']),'source_archive':c['archive'],'source_archive_sha256':c['archive_sha256'],'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()}}
 assert len(refs)==12;put(R/'plan.json',plan);put(R/'anchors.json',refs);(R/'specs').mkdir();batch=[]
 for asset in ['BTC','ETH']:
  for L,H in itertools.product(plan['grid']['new_lookbacks_by_asset'][asset],HURDLES):
   validate_lookback(L);template=base_report['configs'][f'perp_zeroexit_{asset}_L30_H{int(H*100):02d}'];spec=copy.deepcopy(json.loads((ROOT/template['spec']).read_text()));name=f'perp_zeroexit_{asset}_L{L}_H{int(H*100):02d}';spec['name']=name;spec['parameters']['lookback_days']=L;spec['validation_plan']=rel(R/'plan.json');spec['sources']=plan['sources'];path=R/'specs'/(name+'.json');put(path,spec);fp=reg.fingerprint(spec);assert fp not in records or records[fp].get('result_available') is not True and records[fp]['status'] in ['blocked','abandoned'];batch.append({'name':name,'role':'candidate','spec':rel(path),'fingerprint':fp,'asset':asset,'lookback_days':L,'return_hurdle':H,'capital_usdt':10000})
 assert len(batch)==len({x['fingerprint'] for x in batch})==18;assert not ({x['fingerprint'] for x in batch}&{x['fingerprint'] for x in refs.values()});put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/perp_zeroexit_ETH_L29_H02.json').read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_RESERVED18_NEW_ZEROEXIT_COMPONENTS_12OLDREADONLY',sha(R/'plan.json'),flush=True)
