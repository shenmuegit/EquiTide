"""Freeze the complete local zero-exit portfolio grid on main before evaluation."""
import copy,hashlib,itertools,json
from run import ROOT,R,LOOKS,HURDLES,reg,sha,put,rel,now,call
def main():
 assert not (R/'plan.json').exists();ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');p0=ROOT/'research/experiments/20261023T204326Z';p1=ROOT/'research/experiments/20261024T004356Z';base=json.loads((p0/'report.json').read_text());plan=copy.deepcopy(json.loads((p0/'plan.json').read_text()));latest=ROOT/'research/experiments/20261024T084457Z';lp=json.loads((latest/'plan.json').read_text());refs={}
 assert lp['rules']==plan['component_rule_definition'] and lp['costs']==plan['component_costs'] and lp['time_boundaries']==plan['time_boundaries'] and lp['data']==plan['data']
 for source,valid in [(ROOT/'research/experiments/20261023T184400Z',[30]),(ROOT/'research/experiments/20261023T224328Z',[31,32]),(latest,[28,29,31,32])]:
  assert sha(source/'engine.py')==plan['source_engine']['sha256'];doc=json.loads((source/'report.json').read_text())
  for name,c in doc['configs'].items():
   if c['lookback_days'] not in valid:continue
   fp=c['fingerprint'];rec=records[fp];assert rec['result_available'] is True and rec['status']==c['status'] and rec['report_sha256']==sha(source/'report.json') and sha(ROOT/c['archive'])==c['archive_sha256'];spec=json.loads((ROOT/c['spec']).read_text());assert spec['parameters']['initial_capital_usdt']==10000 and spec['parameters']['fixed_entry_notional_usdt']==2000
   refs[fp]={'name':name,'asset':c['asset'],'role':'candidate','lookback_days':c['lookback_days'],'return_hurdle':c['return_hurdle'],'report':rel(source/'report.json'),'report_sha256':sha(source/'report.json'),'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'archive':c['archive'],'archive_sha256':c['archive_sha256'],'original_status':rec['status'],'capital_usdt':10000,'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()}}
 assert len(refs)==30 and all(sum(x['asset']==a for x in refs.values())==15 for a in ['BTC','ETH'])
 plan.update(round=R.name,trigger_utc='2026-10-24T10:45:57.398Z',frozen_at_utc=now(),hypothesis='Check joint diversification across the completed localL28to32 zero-exit components forbothassets. Full225cell4D grid frozen:27oldparentsreadonly,198newparents. Includeall H/Lcells,not only4qualified components. Samehistoryandcomponents reused,not independentconfirmation.',component_sources=refs)
 plan['grid']={'BTC_lookback_days':LOOKS,'BTC_return_hurdle':HURDLES,'ETH_lookback_days':LOOKS,'ETH_return_hurdle':HURDLES,'new_parent_configs':198,'read_only_anchor_configs':27,'full_grid_configs':225,'new_component_backtests':0,'raw_component_multipliers':[1,1],'cost_multipliers':[1,2,3],'preset_center':{'BTC_lookback_days':30,'BTC_return_hurdle':.02,'ETH_lookback_days':30,'ETH_return_hurdle':.02}}
 plan['anchor_sources']=[{'report':rel(p0/'report.json'),'report_sha256':sha(p0/'report.json'),'old_cells':9},{'report':rel(p1/'report.json'),'report_sha256':sha(p1/'report.json'),'old_cells':18}]
 plan['sensitivity']='Full4D225cells:eachassetL28/29/30/31/32 x H1/2/4percent.27oldparentsread-only,198newparentspreregistered. Inclusiveadjacentindex4axis neighborhoods,corner16,interior81;oldoriginalqualification unchanged. No post-result expansion.'
 plan['novelty']={'initial16_missing_actual_results':0,'prior_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_non_observation_definitions':ctx['canonical_research_definitions_excluding_observations'],'prior_conclusions_read':len(ctx['prior_conclusions_read']),'selection_bias':'Allcomponents and entire330daymarket previouslyseen;gridcountnot independentconfirmations.No DSR/PBO or untouchedfinalholdout.'}
 plan['lookback_availability']=lp['lookback_availability'];assert plan['lookback_availability']['earliest_completed_close_index']==0
 for s in plan['sources']:
  s['access_date']='2026-10-24'
  if 'aqr.com' in s['url']:s['scope']='Traditional12monthmulti-futuresmomentum background only;our local28to32daycryptopassiveportfolio is a separate developmenthypothesis.'
 for files in plan['data']['assets'].values():
  for x in files:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 anchors={}
 for source in [p0,p1]:
  doc=json.loads((source/'report.json').read_text())
  for name,c in doc['configs'].items():
   if c['BTC_lookback_days'] not in LOOKS or c['ETH_lookback_days'] not in LOOKS:continue
   anchors[name]={'name':name,'fingerprint':c['fingerprint'],'original_status':c['status'],'report':rel(source/'report.json'),'report_sha256':sha(source/'report.json'),'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'archive':c['archive'],'archive_sha256':c['archive_sha256']}
 assert len(anchors)==27
 for ref in anchors.values():assert records[ref['fingerprint']]['status']==ref['original_status'] and records[ref['fingerprint']]['report_sha256']==ref['report_sha256']
 put(R/'plan.json',plan);put(R/'anchors.json',anchors);(R/'specs').mkdir();by={(x['asset'],x['lookback_days'],x['return_hurdle']):fp for fp,x in refs.items()};batch=[]
 for lb,hb,le,he in itertools.product(LOOKS,HURDLES,LOOKS,HURDLES):
  name=f'perp_zero_pair_B{lb}H{int(hb*100):02d}_E{le}H{int(he*100):02d}'
  if name in anchors:continue
  template=base['configs'][f'perp_zero_pair_B30H{int(hb*100):02d}_E30H{int(he*100):02d}'];spec=copy.deepcopy(json.loads((ROOT/template['spec']).read_text()));spec['name']=name;spec['parameters'].update(BTC_lookback_days=lb,ETH_lookback_days=le);fps=[by['BTC',lb,hb],by['ETH',le,he]];spec['components']=[{'fingerprint':fp,'weight':1} for fp in fps];spec['validation_plan']=rel(R/'plan.json');spec['sources']=plan['sources'];path=R/'specs'/(name+'.json');put(path,spec);fp=reg.fingerprint(spec);assert fp not in records or records[fp].get('result_available') is not True and records[fp]['status'] in ['blocked','abandoned'];batch.append({'name':name,'role':'candidate','spec':rel(path),'fingerprint':fp,'BTC_lookback_days':lb,'BTC_return_hurdle':hb,'ETH_lookback_days':le,'ETH_return_hurdle':he,'source_fingerprints':fps})
 assert len(batch)==len({x['fingerprint'] for x in batch})==198;put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/perp_zero_pair_B29H02_E29H02.json').read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_RESERVED198_NEW_LOCALPARENTS_27OLD_30COMPONENTS_READONLY_MAIN',sha(R/'plan.json'),flush=True)
