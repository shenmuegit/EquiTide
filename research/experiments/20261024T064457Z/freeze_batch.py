"""Freeze the complete two-asset entry/exit grid before any new evaluation."""
import copy,itertools,json,hashlib
from run import ROOT,R,HURDLES,BUFFERS,reg,sha,put,rel,now,call
def main():
 assert not (R/'plan.json').exists();ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');oldroot=ROOT/'research/experiments/20261023T204326Z';old=json.loads((oldroot/'report.json').read_text());priorroot=ROOT/'research/experiments/20261024T044326Z';prior=json.loads((priorroot/'report.json').read_text());plan=copy.deepcopy(json.loads((priorroot/'plan.json').read_text()));broot=ROOT/'research/experiments/20261024T024326Z';zroot=ROOT/'research/experiments/20261023T184400Z';bp=json.loads((broot/'plan.json').read_text());zp=json.loads((zroot/'plan.json').read_text());assert bp['costs']==zp['costs'] and bp['data']==zp['data'] and bp['time_boundaries']==zp['time_boundaries'];refs={}
 for source,zero_only in [(zroot,True),(broot,False)]:
  doc=json.loads((source/'report.json').read_text())
  for name,c in doc['configs'].items():
   if c['lookback_days']!=30 or zero_only and c['asset']!='BTC':continue
   fp=c['fingerprint'];rec=records[fp];assert rec['result_available'] is True and rec['status']==c['status'] and rec['report_sha256']==sha(source/'report.json') and sha(ROOT/c['archive'])==c['archive_sha256'];spec=json.loads((ROOT/c['spec']).read_text());assert spec['parameters']['initial_capital_usdt']==10000 and spec['parameters']['fixed_entry_notional_usdt']==2000
   refs[fp]={'name':name,'asset':c['asset'],'role':'candidate','lookback_days':30,'return_hurdle':c['return_hurdle'],'exit_buffer_fraction':c.get('exit_buffer_fraction',0),'report':rel(source/'report.json'),'report_sha256':sha(source/'report.json'),'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'archive':c['archive'],'archive_sha256':c['archive_sha256'],'original_status':rec['status'],'capital_usdt':10000,'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()}}
 assert len(refs)==21 and sum(x['asset']=='BTC' for x in refs.values())==12 and sum(x['asset']=='ETH' for x in refs.values())==9
 rulehash=hashlib.sha256(json.dumps({'BTC':bp['rules'],'ETH':bp['rules'],'costs':bp['costs']},sort_keys=True,separators=(',',':')).encode()).hexdigest()
 plan.update(round=R.name,trigger_utc='2026-10-24T06:44:57.062Z',frozen_at_utc=now(),hypothesis='Extend the alreadyseen BTC-buffer/ETH-zero parent grid across ETHexitbuffer,including zeroBTCbuffer and jointlybuffered parents. Full144cells preregistered:36oldETHzero cells readonly,108newETHpositivebuffer cells. No result-selected subgroup or independentconfirmation.',component_sources=refs,component_rule_definition={'BTC':bp['rules'],'ETH':bp['rules'],'zeroBTCbuffer_implemented_by_original_zeroexit_spec':zp['rules']},component_costs=bp['costs'],source_rules_and_costs_sha256=rulehash)
 plan['grid']={'BTC_lookback_days':30,'ETH_lookback_days':30,'BTC_return_hurdle':HURDLES,'BTC_exit_buffer_fraction':BUFFERS,'ETH_return_hurdle':HURDLES,'ETH_exit_buffer_fraction':BUFFERS,'new_parent_configs':108,'read_only_anchor_configs':36,'full_grid_configs':144,'new_component_backtests':0,'raw_component_multipliers':[1,1],'cost_multipliers':[1,2,3],'preset_center':{'BTC_return_hurdle':.02,'BTC_exit_buffer_fraction':.005,'ETH_return_hurdle':.02,'ETH_exit_buffer_fraction':.005}}
 plan.pop('anchor_source',None);plan['anchor_sources']=[{'report':rel(oldroot/'report.json'),'report_sha256':sha(oldroot/'report.json'),'old_cells':9},{'report':rel(priorroot/'report.json'),'report_sha256':sha(priorroot/'report.json'),'old_cells':27}]
 plan['sensitivity']='Full4D144cells: eachassetentry1/2/4percent x eachassetexitbuffer0/.25/.5/1percent. All36oldETHbuffer0cellsreadonly,oldoriginalqualification not rerated.108newcellswithETHbuffer>0 assessed. Inclusiveadjacentindex4axisneighborhood,corner16,interior81;no post-result expansion.'
 assert plan['gates'].pop('three_dimensional_local_3x_positive_fraction_min')==.6;plan['gates']['four_dimensional_local_3x_positive_fraction_min']=.6
 plan['novelty']={'initial16_missing_actual_results':0,'prior_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_non_observation_definitions':ctx['canonical_research_definitions_excluding_observations'],'prior_conclusions_read':len(ctx['prior_conclusions_read']),'selection_bias':'Entire330dayhistory and allsourcecomponents seen before;no DSR/PBO or untouchedholdout.'}
 for x in plan['sources']:
  x['access_date']='2026-10-24'
  if 'aqr.com' in x['url']:x['scope']='2012traditional12monthfuturesmomentum background only;thiscrypto30daypassive entry/exit jointgrid is a separate developmenthypothesis.'
 for files in plan['data']['assets'].values():
  for x in files:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 anchors={}
 for source,doc in [(oldroot,old),(priorroot,prior)]:
  for name,c in doc['configs'].items():
   if c['BTC_lookback_days']!=30 or c['ETH_lookback_days']!=30:continue
   anchors[name]={'name':name,'fingerprint':c['fingerprint'],'original_status':c['status'],'report':rel(source/'report.json'),'report_sha256':sha(source/'report.json'),'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'archive':c['archive'],'archive_sha256':c['archive_sha256']}
 assert len(anchors)==36
 for ref in anchors.values():assert records[ref['fingerprint']]['status']==ref['original_status'] and records[ref['fingerprint']]['report_sha256']==ref['report_sha256']
 put(R/'plan.json',plan);put(R/'anchors.json',anchors);(R/'specs').mkdir();by={(x['asset'],x['return_hurdle'],x['exit_buffer_fraction']):fp for fp,x in refs.items()};batch=[]
 for hb,eb,he,ee in itertools.product(HURDLES,BUFFERS,HURDLES,BUFFERS[1:]):
  name=f'perp_dualbuffer_pair_B30H{int(hb*100):02d}E{int(eb*10000):03d}bp_E30H{int(he*100):02d}E{int(ee*10000):03d}bp';template=old['configs'][f'perp_zero_pair_B30H{int(hb*100):02d}_E30H{int(he*100):02d}'];spec=copy.deepcopy(json.loads((ROOT/template['spec']).read_text()));spec['name']=name;spec['parameters'].update(BTC_exit_buffer_fraction=eb,ETH_exit_buffer_fraction=ee,source_rules_and_costs_sha256=rulehash);fps=[by['BTC',hb,eb],by['ETH',he,ee]];spec['components']=[{'fingerprint':fp,'weight':1} for fp in fps];spec['validation_plan']=rel(R/'plan.json');spec['sources']=plan['sources'];path=R/'specs'/(name+'.json');put(path,spec);fp=reg.fingerprint(spec);assert fp not in records or records[fp].get('result_available') is not True and records[fp]['status'] in ['blocked','abandoned'];batch.append({'name':name,'role':'candidate','spec':rel(path),'fingerprint':fp,'BTC_lookback_days':30,'BTC_return_hurdle':hb,'BTC_exit_buffer_fraction':eb,'ETH_lookback_days':30,'ETH_return_hurdle':he,'ETH_exit_buffer_fraction':ee,'source_fingerprints':fps})
 assert len(batch)==len({x['fingerprint'] for x in batch})==108;put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/perp_dualbuffer_pair_B30H02E050bp_E30H02E050bp.json').read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_RESERVED108NEWPARENTS_36OLDREADONLY_21SOURCECOMPONENTS',sha(R/'plan.json'),flush=True)
