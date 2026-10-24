"""Freeze the joint +1/+1 lookback perturbation and its exact known comparison grid."""
import copy,hashlib,itertools,json
from run import ROOT,R,HURDLES,BUFFERS,reg,sha,put,rel,now,call

def main():
 assert not (R/'plan.json').exists();ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');base=ROOT/'research/experiments/20261024T184829Z';plan=copy.deepcopy(json.loads((base/'plan.json').read_text()));zero_root=ROOT/'research/experiments/20261024T104557Z';zero_doc=json.loads((zero_root/'report.json').read_text());bp=json.loads((ROOT/'research/experiments/20261024T164729Z/plan.json').read_text());zp=json.loads((ROOT/'research/experiments/20261024T084457Z/plan.json').read_text());assert bp['costs']==plan['component_costs'] and bp['data']==plan['data'] and bp['time_boundaries']==plan['time_boundaries'];refs={}
 for roundid in ['20261024T084457Z','20261024T124528Z','20261024T164729Z']:
  source=ROOT/'research/experiments'/roundid;doc=json.loads((source/'report.json').read_text())
  for name,c in doc['configs'].items():
   if c['lookback_days']!={'BTC':32,'ETH':29}[c['asset']] or c['return_hurdle'] not in HURDLES:continue
   E=c.get('exit_buffer_fraction',0)
   if E not in BUFFERS:continue
   fp=c['fingerprint'];rec=records[fp];assert rec['result_available'] is True and rec['status']==c['status'] and rec['report_sha256']==sha(source/'report.json') and sha(ROOT/c['archive'])==c['archive_sha256'];spec=json.loads((ROOT/c['spec']).read_text());assert spec['parameters']['initial_capital_usdt']==10000 and spec['parameters']['fixed_entry_notional_usdt']==2000
   refs[fp]={'name':name,'asset':c['asset'],'role':'candidate','lookback_days':c['lookback_days'],'return_hurdle':c['return_hurdle'],'exit_buffer_fraction':E,'report':rel(source/'report.json'),'report_sha256':sha(source/'report.json'),'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'archive':c['archive'],'archive_sha256':c['archive_sha256'],'original_status':rec['status'],'capital_usdt':10000,'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()}}
 assert len(refs)==24 and all(sum(x['asset']==a for x in refs.values())==12 for a in ['BTC','ETH'])
 rulehash=hashlib.sha256(json.dumps({'BTC':bp['rules'],'ETH':bp['rules'],'costs':bp['costs']},sort_keys=True,separators=(',',':')).encode()).hexdigest()
 plan.update(round=R.name,trigger_utc='2026-10-24T20:50:03.594Z',frozen_at_utc=now(),hypothesis='Jointly perturb the known BTC31/ETH28 parent grid by +1day forbothassets:fixedBTC32/ETH29,entryH2/4percent,exitE0/.25/.5/1/1.5/2percent.4oldzero/zero targetparents readonly,140unseen targetparents preregistered. Compare everynewcell tosameH/E priorBTC31/ETH28 actualresult. Jointperturbation cannotattribute individualasset effects;all330daydata andcomponents alreadyseen,not independentvalidation.',component_sources=refs,component_rule_definition={'BTC':bp['rules'],'ETH':bp['rules'],'zero_buffer_implemented_by_existing_zeroexit_specs':zp['rules']},component_costs=bp['costs'],source_rules_and_costs_sha256=rulehash)
 plan['grid']={'BTC_lookback_days':32,'ETH_lookback_days':29,'BTC_return_hurdle':HURDLES,'BTC_exit_buffer_fraction':BUFFERS,'ETH_return_hurdle':HURDLES,'ETH_exit_buffer_fraction':BUFFERS,'new_parent_configs':140,'read_only_anchor_configs':4,'full_grid_configs':144,'new_component_backtests':0,'raw_component_multipliers':[1,1],'cost_multipliers':[1,2,3],'preset_center':{'BTC_return_hurdle':.02,'BTC_exit_buffer_fraction':.01,'ETH_return_hurdle':.02,'ETH_exit_buffer_fraction':.01},'domain':'0<=E<=H;H1not compatible with rectangular E2upperbound. No outcome-based componentfilter.'}
 plan['sensitivity']='Full4D144targetcells H2/4 x E0/.25/.5/1/1.5/2 forbothassets withsimultaneousadjacent-index4axisneighborhoods.4oldtargetzero/zero statuses unchanged.144oldBTC31/ETH28cells onlymatchedcomparisons,not part ofnewtarget qualification neighborhood andnever recomputed/rerated. No post-result gridexpansion.'
 plan['novelty']={'initial16_missing_actual_results':0,'prior_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_non_observation_definitions':ctx['canonical_research_definitions_excluding_observations'],'prior_conclusions_read':len(ctx['prior_conclusions_read']),'selection_bias':'Knownlookbacks,all24components andentire330dayhistory reused;140parenttrials not independentconfirmations. No untouchedholdout,DSR/PBO orliveTCA.'}
 for s in plan['sources']:
  s['access_date']='2026-10-24'
  if 'aqr.com' in s['url']:s['scope']='Traditional12monthmulti-futuresmomentum background only;BTC32/ETH29 crypto pairedlookbackperturbation is a separate developmenthypothesis.'
 for files in plan['data']['assets'].values():
  for x in files:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 anchors={};comparisons={};source_counts=[]
 for roundid in ['20261024T104557Z','20261024T144658Z','20261024T184829Z']:
  source=ROOT/'research/experiments'/roundid;doc=json.loads((source/'report.json').read_text());n=0
  for name,c in doc['configs'].items():
   if c['BTC_return_hurdle'] not in HURDLES or c['ETH_return_hurdle'] not in HURDLES:continue
   target=c['BTC_lookback_days']==32 and c['ETH_lookback_days']==29 and roundid=='20261024T104557Z';reference=c['BTC_lookback_days']==31 and c['ETH_lookback_days']==28
   if not (target or reference):continue
   rec=records[c['fingerprint']];assert rec['result_available'] is True and rec['status']==c['status'] and rec['report_sha256']==sha(source/'report.json');ref={'name':name,'fingerprint':c['fingerprint'],'original_status':c['status'],'report':rel(source/'report.json'),'report_sha256':sha(source/'report.json'),'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'archive':c['archive'],'archive_sha256':c['archive_sha256'],'BTC_return_hurdle':c['BTC_return_hurdle'],'BTC_exit_buffer_fraction':c.get('BTC_exit_buffer_fraction',0),'ETH_return_hurdle':c['ETH_return_hurdle'],'ETH_exit_buffer_fraction':c.get('ETH_exit_buffer_fraction',0)}
   if target:anchors[name]=ref
   if reference:comparisons[name]=ref;n+=1
  source_counts.append({'report':rel(source/'report.json'),'report_sha256':sha(source/'report.json'),'comparison_cells':n})
 assert len(anchors)==4 and len(comparisons)==144 and [x['comparison_cells'] for x in source_counts]==[4,60,80]
 assert len({(v['BTC_return_hurdle'],v['BTC_exit_buffer_fraction'],v['ETH_return_hurdle'],v['ETH_exit_buffer_fraction']) for v in comparisons.values()})==144
 plan['anchor_sources']=[{'report':rel(zero_root/'report.json'),'report_sha256':sha(zero_root/'report.json'),'old_cells':4}];plan['read_only_lookback_reference_sources']=source_counts;plan['comparison_scope']='Same dates20000collateral/raw1/1/entry2000each/costmodels. Onlylookbacks change jointly31->32 and28->29. Priorvalues directlyread;no attribution tosingleasset,no new source backtests.'
 put(R/'plan.json',plan);put(R/'anchors.json',anchors);put(R/'lookback_references.json',comparisons);(R/'specs').mkdir();by={(x['asset'],x['return_hurdle'],x['exit_buffer_fraction']):fp for fp,x in refs.items()};batch=[]
 for hb,eb,he,ee in itertools.product(HURDLES,BUFFERS,HURDLES,BUFFERS):
  if eb==ee==0:continue
  assert eb<=hb and ee<=he;name=f'perp_dualbuffer_pair_B32H{int(hb*100):02d}E{int(round(eb*10000)):03d}bp_E29H{int(he*100):02d}E{int(round(ee*10000)):03d}bp';template=zero_doc['configs'][f'perp_zero_pair_B32H{int(hb*100):02d}_E29H{int(he*100):02d}'];spec=copy.deepcopy(json.loads((ROOT/template['spec']).read_text()));spec['name']=name;spec['parameters'].update(BTC_exit_buffer_fraction=eb,ETH_exit_buffer_fraction=ee,source_rules_and_costs_sha256=rulehash);fps=[by['BTC',hb,eb],by['ETH',he,ee]];spec['components']=[{'fingerprint':fp,'weight':1} for fp in fps];spec['validation_plan']=rel(R/'plan.json');spec['sources']=plan['sources'];path=R/'specs'/(name+'.json');put(path,spec);fp=reg.fingerprint(spec);assert fp not in records or records[fp].get('result_available') is not True and records[fp]['status'] in ['blocked','abandoned'];batch.append({'name':name,'role':'candidate','spec':rel(path),'fingerprint':fp,'BTC_lookback_days':32,'BTC_return_hurdle':hb,'BTC_exit_buffer_fraction':eb,'ETH_lookback_days':29,'ETH_return_hurdle':he,'ETH_exit_buffer_fraction':ee,'source_fingerprints':fps})
 assert len(batch)==len({x['fingerprint'] for x in batch})==140;put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/perp_dualbuffer_pair_B32H02E100bp_E29H02E100bp.json').read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_RESERVED140_NEIGHBOR_LOOKBACK_PARENTS_4OLD_144READONLY_COMPARISONS',sha(R/'plan.json'),flush=True)
if __name__=='__main__':main()
