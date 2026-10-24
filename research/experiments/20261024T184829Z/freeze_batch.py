"""Pre-register only unseen wide-buffer parents;reuse all exact old inner cells."""
import copy,hashlib,itertools,json
from run import ROOT,R,HURDLES,BUFFERS,reg,sha,put,rel,now,call

def main():
 assert not (R/'plan.json').exists();ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');base=ROOT/'research/experiments/20261024T144658Z';plan=copy.deepcopy(json.loads((base/'plan.json').read_text()));zero_root=ROOT/'research/experiments/20261024T104557Z';zero_doc=json.loads((zero_root/'report.json').read_text());bp=json.loads((ROOT/'research/experiments/20261024T164729Z/plan.json').read_text());zp=json.loads((ROOT/'research/experiments/20261024T084457Z/plan.json').read_text());assert bp['costs']==zp['costs']==plan['component_costs'] and bp['data']==plan['data'] and bp['time_boundaries']==plan['time_boundaries'];refs={}
 for roundid in ['20261024T084457Z','20261024T124528Z','20261024T164729Z']:
  source=ROOT/'research/experiments'/roundid;doc=json.loads((source/'report.json').read_text())
  for name,c in doc['configs'].items():
   if c['lookback_days']!={'BTC':31,'ETH':28}[c['asset']] or c['return_hurdle'] not in HURDLES:continue
   E=c.get('exit_buffer_fraction',0)
   if E not in BUFFERS:continue
   fp=c['fingerprint'];rec=records[fp];assert rec['result_available'] is True and rec['status']==c['status'] and rec['report_sha256']==sha(source/'report.json') and sha(ROOT/c['archive'])==c['archive_sha256'];spec=json.loads((ROOT/c['spec']).read_text());assert spec['parameters']['initial_capital_usdt']==10000 and spec['parameters']['fixed_entry_notional_usdt']==2000
   refs[fp]={'name':name,'asset':c['asset'],'role':'candidate','lookback_days':c['lookback_days'],'return_hurdle':c['return_hurdle'],'exit_buffer_fraction':E,'report':rel(source/'report.json'),'report_sha256':sha(source/'report.json'),'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'archive':c['archive'],'archive_sha256':c['archive_sha256'],'original_status':rec['status'],'capital_usdt':10000,'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()}}
 assert len(refs)==24 and all(sum(x['asset']==a for x in refs.values())==12 for a in ['BTC','ETH'])
 rulehash=hashlib.sha256(json.dumps({'BTC':bp['rules'],'ETH':bp['rules'],'costs':bp['costs']},sort_keys=True,separators=(',',':')).encode()).hexdigest()
 plan.update(round=R.name,trigger_utc='2026-10-24T18:48:29.166Z',frozen_at_utc=now(),hypothesis='Extend the fixedBTC31/ETH28 passive parent entry/exit surface to source exitbuffers1.5/2percent. Reuse every eligible component,including rejected BTCbooks.144cells frozen:64old E<=1percent parents readonly,80new parents where at leastoneE>1percent. Same330dayhistory andall24components previouslyseen;not independentconfirmation.',component_sources=refs,component_rule_definition={'BTC':bp['rules'],'ETH':bp['rules'],'zero_buffer_implemented_by_existing_zeroexit_specs':zp['rules']},component_costs=bp['costs'],source_rules_and_costs_sha256=rulehash)
 engine=ROOT/'research/experiments/20261024T164729Z/engine.py';plan['source_engine']={'path':rel(engine),'sha256':sha(engine),'use':'load realmarket axes/prices only;never call source simulate/signal/trade/funding'}
 plan['grid']={'BTC_lookback_days':31,'ETH_lookback_days':28,'BTC_return_hurdle':HURDLES,'BTC_exit_buffer_fraction':BUFFERS,'ETH_return_hurdle':HURDLES,'ETH_exit_buffer_fraction':BUFFERS,'new_parent_configs':80,'read_only_anchor_configs':64,'full_grid_configs':144,'new_component_backtests':0,'raw_component_multipliers':[1,1],'cost_multipliers':[1,2,3],'preset_center':{'BTC_return_hurdle':.02,'BTC_exit_buffer_fraction':.015,'ETH_return_hurdle':.02,'ETH_exit_buffer_fraction':.015},'domain':'0<=E<=H always. H1excluded because extended E2 wouldviolate existingdomain;not an outcome filter.'}
 plan['sensitivity']='Full4D144cells H2/4percent x E0/.25/.5/1/1.5/2percent forbothassets;all64oldinnercells retain originalqualifications.80newoutercells in simultaneousadjacent-index4axisneighborhoods. Preplanned contrasts with matched Eclampedto1percent oldparent andwithmatched doubleE0oldparent. No adaptive gridextension.'
 plan['lookback_availability']=bp['lookback_availability'];plan['novelty']={'initial16_missing_actual_results':0,'prior_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_non_observation_definitions':ctx['canonical_research_definitions_excluding_observations'],'prior_conclusions_read':len(ctx['prior_conclusions_read']),'selection_bias':'Knownlookbacks,all24component paths andwhole330dayhistory reused;80parenttrials are not independent confirmations. No untouchedholdout,DSR/PBO orliveTCA.'}
 for s in plan['sources']:
  s['access_date']='2026-10-24'
  if 'aqr.com' in s['url']:s['scope']='Traditional12monthmulti-futuresmomentum background only;BTC31/ETH28 crypto wide-buffer passiveportfolio is a separate developmenthypothesis.'
 for files in plan['data']['assets'].values():
  for x in files:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 anchors={};source_counts=[]
 for source in [zero_root,base]:
  doc=json.loads((source/'report.json').read_text());n=0
  for name,c in doc['configs'].items():
   if c['BTC_lookback_days']!=31 or c['ETH_lookback_days']!=28 or c['BTC_return_hurdle'] not in HURDLES or c['ETH_return_hurdle'] not in HURDLES:continue
   assert c.get('BTC_exit_buffer_fraction',0)<=.01 and c.get('ETH_exit_buffer_fraction',0)<=.01;rec=records[c['fingerprint']];assert rec['result_available'] is True and rec['status']==c['status'] and rec['report_sha256']==sha(source/'report.json');anchors[name]={'name':name,'fingerprint':c['fingerprint'],'original_status':c['status'],'report':rel(source/'report.json'),'report_sha256':sha(source/'report.json'),'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'archive':c['archive'],'archive_sha256':c['archive_sha256']};n+=1
  source_counts.append({'report':rel(source/'report.json'),'report_sha256':sha(source/'report.json'),'old_cells':n})
 assert len(anchors)==64 and [x['old_cells'] for x in source_counts]==[4,60];plan['anchor_sources']=source_counts;put(R/'plan.json',plan);put(R/'anchors.json',anchors);(R/'specs').mkdir();by={(x['asset'],x['return_hurdle'],x['exit_buffer_fraction']):fp for fp,x in refs.items()};batch=[]
 for hb,eb,he,ee in itertools.product(HURDLES,BUFFERS,HURDLES,BUFFERS):
  if eb<=.01 and ee<=.01:continue
  assert eb<=hb and ee<=he;name=f'perp_dualbuffer_pair_B31H{int(hb*100):02d}E{int(round(eb*10000)):03d}bp_E28H{int(he*100):02d}E{int(round(ee*10000)):03d}bp';template=zero_doc['configs'][f'perp_zero_pair_B31H{int(hb*100):02d}_E28H{int(he*100):02d}'];spec=copy.deepcopy(json.loads((ROOT/template['spec']).read_text()));spec['name']=name;spec['parameters'].update(BTC_exit_buffer_fraction=eb,ETH_exit_buffer_fraction=ee,source_rules_and_costs_sha256=rulehash);fps=[by['BTC',hb,eb],by['ETH',he,ee]];spec['components']=[{'fingerprint':fp,'weight':1} for fp in fps];spec['validation_plan']=rel(R/'plan.json');spec['sources']=plan['sources'];path=R/'specs'/(name+'.json');put(path,spec);fp=reg.fingerprint(spec);assert fp not in records or records[fp].get('result_available') is not True and records[fp]['status'] in ['blocked','abandoned'];batch.append({'name':name,'role':'candidate','spec':rel(path),'fingerprint':fp,'BTC_lookback_days':31,'BTC_return_hurdle':hb,'BTC_exit_buffer_fraction':eb,'ETH_lookback_days':28,'ETH_return_hurdle':he,'ETH_exit_buffer_fraction':ee,'source_fingerprints':fps})
 assert len(batch)==len({x['fingerprint'] for x in batch})==80;put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/perp_dualbuffer_pair_B31H02E150bp_E28H02E150bp.json').read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_RESERVED80_WIDE_BUFFER_PARENTS_64OLD_24SOURCE_COMPONENTS_READONLY',sha(R/'plan.json'),flush=True)
if __name__=='__main__':main()
