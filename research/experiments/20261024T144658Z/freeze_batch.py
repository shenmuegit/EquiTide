"""Pre-register the complete fixed-lookback,dual-buffer passive portfolio grid."""
import copy,hashlib,itertools,json
from run import ROOT,R,HURDLES,BUFFERS,reg,sha,put,rel,now,call

def main():
 assert not (R/'plan.json').exists();ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');oldroot=ROOT/'research/experiments/20261024T104557Z';old=json.loads((oldroot/'report.json').read_text());base=ROOT/'research/experiments/20261024T064457Z';plan=copy.deepcopy(json.loads((base/'plan.json').read_text()));bufferroot=ROOT/'research/experiments/20261024T124528Z';zeroroot=ROOT/'research/experiments/20261024T084457Z';bp=json.loads((bufferroot/'plan.json').read_text());zp=json.loads((zeroroot/'plan.json').read_text());assert bp['costs']==zp['costs'] and bp['data']==zp['data'] and bp['time_boundaries']==zp['time_boundaries'];refs={}
 for source,Ezero in [(zeroroot,True),(bufferroot,False)]:
  doc=json.loads((source/'report.json').read_text())
  for name,c in doc['configs'].items():
   if c['lookback_days']!={'BTC':31,'ETH':28}[c['asset']]:continue
   fp=c['fingerprint'];rec=records[fp];assert rec['result_available'] is True and rec['status']==c['status'] and rec['report_sha256']==sha(source/'report.json') and sha(ROOT/c['archive'])==c['archive_sha256'];spec=json.loads((ROOT/c['spec']).read_text());assert spec['parameters']['initial_capital_usdt']==10000 and spec['parameters']['fixed_entry_notional_usdt']==2000
   refs[fp]={'name':name,'asset':c['asset'],'role':'candidate','lookback_days':c['lookback_days'],'return_hurdle':c['return_hurdle'],'exit_buffer_fraction':0 if Ezero else c['exit_buffer_fraction'],'report':rel(source/'report.json'),'report_sha256':sha(source/'report.json'),'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'archive':c['archive'],'archive_sha256':c['archive_sha256'],'original_status':rec['status'],'capital_usdt':10000,'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()}}
 assert len(refs)==24 and all(sum(x['asset']==a for x in refs.values())==12 for a in ['BTC','ETH'])
 rulehash=hashlib.sha256(json.dumps({'BTC':bp['rules'],'ETH':bp['rules'],'costs':bp['costs']},sort_keys=True,separators=(',',':')).encode()).hexdigest()
 plan.update(round=R.name,trigger_utc='2026-10-24T14:46:58.531Z',frozen_at_utc=now(),hypothesis='Reuse every completed BTC31/ETH28 component,including source-rejected cells,in a full entry/exit passiveparent grid. Thislookbackpair was selectedbetweenrounds fromseencomponenthistory,not an independent test.144cells frozen:9oldzero/zero parentresults readonly,135newparents withoneorboth exitbuffersnonzero. No component backtest or new simulated fill.',component_sources=refs,component_rule_definition={'BTC':bp['rules'],'ETH':bp['rules'],'zero_buffer_implemented_by_existing_zeroexit_specs':zp['rules']},component_costs=bp['costs'],source_rules_and_costs_sha256=rulehash)
 plan['source_engine']={'path':rel(bufferroot/'engine.py'),'sha256':sha(bufferroot/'engine.py'),'use':'load real market axes/prices only;never run source signal/trade/funding/simulate'}
 plan['grid']={'BTC_lookback_days':31,'ETH_lookback_days':28,'BTC_return_hurdle':HURDLES,'BTC_exit_buffer_fraction':BUFFERS,'ETH_return_hurdle':HURDLES,'ETH_exit_buffer_fraction':BUFFERS,'new_parent_configs':135,'read_only_anchor_configs':9,'full_grid_configs':144,'new_component_backtests':0,'raw_component_multipliers':[1,1],'cost_multipliers':[1,2,3],'preset_center':{'BTC_return_hurdle':.02,'BTC_exit_buffer_fraction':.005,'ETH_return_hurdle':.02,'ETH_exit_buffer_fraction':.005}}
 plan['anchor_sources']=[{'report':rel(oldroot/'report.json'),'report_sha256':sha(oldroot/'report.json'),'old_cells':9}]
 plan['sensitivity']='Full4D144cells:eachasset H1/2/4percent x E0/.25/.5/1percent at fixedBTC31/ETH28.9oldzero/zero parentcells readonly withoriginal5x5x3x3 gridqualification unchanged.135newcells assessed in simultaneous adjacent-index4axis neighborhoods. No post-result gridextension or changedcapital/weights.'
 assert plan['gates']['four_dimensional_local_3x_positive_fraction_min']==.6
 plan['lookback_availability']=bp['lookback_availability'];assert 32-31>=0 and 32-28>=0
 plan['novelty']={'initial16_missing_actual_results':0,'prior_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_non_observation_definitions':ctx['canonical_research_definitions_excluding_observations'],'prior_conclusions_read':len(ctx['prior_conclusions_read']),'selection_bias':'All24components and330dayhistory seen before;135parenttests are not independent confirmations. No DSR/PBO or untouchedholdout.'}
 for s in plan['sources']:
  s['access_date']='2026-10-24'
  if 'aqr.com' in s['url']:s['scope']='Traditional12monthmulti-futuresmomentum background only;BTC31/ETH28 cryptopassive buffers are a separate developmenthypothesis.'
 for files in plan['data']['assets'].values():
  for x in files:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 anchors={}
 for name,c in old['configs'].items():
  if c['BTC_lookback_days']!=31 or c['ETH_lookback_days']!=28:continue
  anchors[name]={'name':name,'fingerprint':c['fingerprint'],'original_status':c['status'],'report':rel(oldroot/'report.json'),'report_sha256':sha(oldroot/'report.json'),'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'archive':c['archive'],'archive_sha256':c['archive_sha256']}
 assert len(anchors)==9
 for ref in anchors.values():assert records[ref['fingerprint']]['status']==ref['original_status'] and records[ref['fingerprint']]['report_sha256']==ref['report_sha256']
 put(R/'plan.json',plan);put(R/'anchors.json',anchors);(R/'specs').mkdir();by={(x['asset'],x['return_hurdle'],x['exit_buffer_fraction']):fp for fp,x in refs.items()};batch=[]
 for hb,eb,he,ee in itertools.product(HURDLES,BUFFERS,HURDLES,BUFFERS):
  if eb==ee==0:continue
  name=f'perp_dualbuffer_pair_B31H{int(hb*100):02d}E{int(eb*10000):03d}bp_E28H{int(he*100):02d}E{int(ee*10000):03d}bp';template=old['configs'][f'perp_zero_pair_B31H{int(hb*100):02d}_E28H{int(he*100):02d}'];spec=copy.deepcopy(json.loads((ROOT/template['spec']).read_text()));spec['name']=name;spec['parameters'].update(BTC_exit_buffer_fraction=eb,ETH_exit_buffer_fraction=ee,source_rules_and_costs_sha256=rulehash);fps=[by['BTC',hb,eb],by['ETH',he,ee]];spec['components']=[{'fingerprint':fp,'weight':1} for fp in fps];spec['validation_plan']=rel(R/'plan.json');spec['sources']=plan['sources'];path=R/'specs'/(name+'.json');put(path,spec);fp=reg.fingerprint(spec)
  assert fp not in records or records[fp].get('result_available') is not True and records[fp]['status'] in ['blocked','abandoned']
  batch.append({'name':name,'role':'candidate','spec':rel(path),'fingerprint':fp,'BTC_lookback_days':31,'BTC_return_hurdle':hb,'BTC_exit_buffer_fraction':eb,'ETH_lookback_days':28,'ETH_return_hurdle':he,'ETH_exit_buffer_fraction':ee,'source_fingerprints':fps})
 assert len(batch)==len({x['fingerprint'] for x in batch})==135
 put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/perp_dualbuffer_pair_B31H02E050bp_E28H02E050bp.json').read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_RESERVED135_NEW_PARENTS_9OLD_24COMPONENTS_READONLY_MAIN',sha(R/'plan.json'),flush=True)
if __name__=='__main__':main()
