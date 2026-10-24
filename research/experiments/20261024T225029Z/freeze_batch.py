"""Preregister both missing off-diagonals of the fixed two-lookback factorial."""
import copy,hashlib,itertools,json
from run import ROOT,R,HURDLES,BUFFERS,reg,sha,put,rel,now,call

def main():
 assert not (R/'plan.json').exists();ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');plan=copy.deepcopy(json.loads((ROOT/'research/experiments/20261024T205003Z/plan.json').read_text()));bp=json.loads((ROOT/'research/experiments/20261024T164729Z/plan.json').read_text());zp=json.loads((ROOT/'research/experiments/20261024T084457Z/plan.json').read_text());zero_root=ROOT/'research/experiments/20261024T104557Z';zero_doc=json.loads((zero_root/'report.json').read_text());refs={}
 assert bp['costs']==plan['component_costs'] and bp['data']==plan['data'] and bp['time_boundaries']==plan['time_boundaries']
 for rid in ['20261024T084457Z','20261024T124528Z','20261024T164729Z']:
  src=ROOT/'research/experiments'/rid;doc=json.loads((src/'report.json').read_text())
  for name,c in doc['configs'].items():
   if c['lookback_days'] not in {'BTC':[31,32],'ETH':[28,29]}[c['asset']] or c['return_hurdle'] not in HURDLES:continue
   e=c.get('exit_buffer_fraction',0)
   if e not in BUFFERS:continue
   fp=c['fingerprint'];rec=records[fp];assert rec['result_available'] is True and rec['status']==c['status'] and rec['report_sha256']==sha(src/'report.json') and sha(ROOT/c['archive'])==c['archive_sha256'];sp=json.loads((ROOT/c['spec']).read_text());assert sp['parameters']['initial_capital_usdt']==10000 and sp['parameters']['fixed_entry_notional_usdt']==2000
   refs[fp]={'name':name,'asset':c['asset'],'role':'candidate','lookback_days':c['lookback_days'],'return_hurdle':c['return_hurdle'],'exit_buffer_fraction':e,'report':rel(src/'report.json'),'report_sha256':sha(src/'report.json'),'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'archive':c['archive'],'archive_sha256':c['archive_sha256'],'original_status':rec['status'],'capital_usdt':10000,'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()}}
 assert len(refs)==48 and all(sum(x['asset']==a for x in refs.values())==24 for a in ['BTC','ETH'])
 rulehash=hashlib.sha256(json.dumps({'BTC':bp['rules'],'ETH':bp['rules'],'costs':bp['costs']},sort_keys=True,separators=(',',':')).encode()).hexdigest();assert rulehash==plan['source_rules_and_costs_sha256']
 plan.update(round=R.name,trigger_utc='2026-10-24T22:50:29.888Z',frozen_at_utc=now(),hypothesis='Complete the missing BTC-only and ETH-only +1day lookback perturbations: BTC32/ETH28 and BTC31/ETH29. Each fixed pair has entry H2/4 percent and exit E0/.25/.5/1/1.5/2 percent,140 unseen nonzero/zero parent cells. Reuse296 actual old cells including BTC31/ETH28 baseline and BTC32/ETH29 joint perturbation. Same-history descriptive matched comparisons, not independent confirmation.',component_sources=refs,component_rule_definition={'BTC':bp['rules'],'ETH':bp['rules'],'zero_buffer_implemented_by_existing_zeroexit_specs':zp['rules']},component_costs=bp['costs'])
 plan['grid']={'BTC_lookback_days':[31,32],'ETH_lookback_days':[28,29],'new_lookback_pairs':[[32,28],[31,29]],'BTC_return_hurdle':HURDLES,'BTC_exit_buffer_fraction':BUFFERS,'ETH_return_hurdle':HURDLES,'ETH_exit_buffer_fraction':BUFFERS,'new_parent_configs':280,'read_only_anchor_configs':296,'full_grid_configs':576,'new_component_backtests':0,'raw_component_multipliers':[1,1],'cost_multipliers':[1,2,3],'preset_center_by_pair':{'BTC_return_hurdle':.02,'BTC_exit_buffer_fraction':.01,'ETH_return_hurdle':.02,'ETH_exit_buffer_fraction':.01},'domain':'0<=E<=H; rectangular E2upperbound only H2/4. No outcome-based sourcefilter.'}
 plan['sensitivity']='Qualification uses original four H/E axes within each fixed lookback pair, simultaneous adjacent-index neighbors; old296 statuses never rerated. Full576 six-axis factorial and2112 forward adjacent edges are descriptive only, not a changed gate. Matched baseline31/28 contrasts separate BTC-only and ETH-only changes. Return interaction must be zero by additive fixed-funded-bank definition, not empirical causality. No post-result expansion.'
 plan['novelty']={'initial16_missing_actual_results':0,'prior_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_non_observation_definitions':ctx['canonical_research_definitions_excluding_observations'],'prior_conclusions_read':len(ctx['prior_conclusions_read']),'selection_bias':'All48components and entire330dayhistory reused;280 exact new parent configurations are not independent confirmations. No untouchedholdout,DSR/PBO orliveTCA.'}
 for s in plan['sources']:
  s['access_date']='2026-10-24'
  if 'aqr.com' in s['url']:s['scope']='Traditional12monthmulti-futuresmomentum background only;singleasset crypto lookback perturbations are separate development hypotheses.'
 for files in plan['data']['assets'].values():
  for x in files:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 anchors={};sources=[]
 for rid in ['20261024T104557Z','20261024T144658Z','20261024T184829Z','20261024T205003Z']:
  src=ROOT/'research/experiments'/rid;doc=json.loads((src/'report.json').read_text());n=0
  for name,c in doc['configs'].items():
   if c['BTC_lookback_days'] not in [31,32] or c['ETH_lookback_days'] not in [28,29] or c['BTC_return_hurdle'] not in HURDLES or c['ETH_return_hurdle'] not in HURDLES:continue
   eb,ee=c.get('BTC_exit_buffer_fraction',0),c.get('ETH_exit_buffer_fraction',0)
   if eb not in BUFFERS or ee not in BUFFERS:continue
   rec=records[c['fingerprint']];assert rec['result_available'] is True and rec['status']==c['status'] and rec['report_sha256']==sha(src/'report.json') and sha(ROOT/c['archive'])==c['archive_sha256'];anchors[name]={'name':name,'fingerprint':c['fingerprint'],'original_status':c['status'],'report':rel(src/'report.json'),'report_sha256':sha(src/'report.json'),'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'archive':c['archive'],'archive_sha256':c['archive_sha256'],'BTC_lookback_days':c['BTC_lookback_days'],'ETH_lookback_days':c['ETH_lookback_days'],'BTC_return_hurdle':c['BTC_return_hurdle'],'BTC_exit_buffer_fraction':eb,'ETH_return_hurdle':c['ETH_return_hurdle'],'ETH_exit_buffer_fraction':ee};n+=1
  sources.append({'report':rel(src/'report.json'),'report_sha256':sha(src/'report.json'),'old_cells':n})
 assert len(anchors)==296 and [s['old_cells'] for s in sources]==[16,60,80,140]
 comparisons={n:v for n,v in anchors.items() if v['BTC_lookback_days']==31 and v['ETH_lookback_days']==28};assert len(comparisons)==144
 plan['anchor_sources']=sources;plan['read_only_lookback_reference_sources']=[{'report':x['report'],'report_sha256':x['report_sha256'],'comparison_cells':sum(v['report']==x['report'] for v in comparisons.values())} for x in sources];plan['comparison_scope']='Same330days,20000collateral/raw1/1,2000entryeach,costmodels. New32/28 isolates BTC31->32 withETH28 fixed;new31/29 isolates ETH28->29 withBTC31 fixed. Fullfactorial includesold31/28 and32/29. Oldvalues read directly,never recomputed or rerated. Return interaction zero is accounting identity.'
 put(R/'plan.json',plan);put(R/'anchors.json',anchors);put(R/'lookback_references.json',comparisons);(R/'specs').mkdir();by={(x['asset'],x['lookback_days'],x['return_hurdle'],x['exit_buffer_fraction']):fp for fp,x in refs.items()};batch=[]
 for (lb,le),(hb,eb,he,ee) in itertools.product([(32,28),(31,29)],itertools.product(HURDLES,BUFFERS,HURDLES,BUFFERS)):
  if eb==ee==0:continue
  assert eb<=hb and ee<=he;name=f'perp_dualbuffer_pair_B{lb}H{int(hb*100):02d}E{int(round(eb*10000)):03d}bp_E{le}H{int(he*100):02d}E{int(round(ee*10000)):03d}bp';template=zero_doc['configs'][f'perp_zero_pair_B{lb}H{int(hb*100):02d}_E{le}H{int(he*100):02d}'];spec=copy.deepcopy(json.loads((ROOT/template['spec']).read_text()));spec['name']=name;spec['parameters'].update(BTC_exit_buffer_fraction=eb,ETH_exit_buffer_fraction=ee,source_rules_and_costs_sha256=rulehash);fps=[by['BTC',lb,hb,eb],by['ETH',le,he,ee]];spec['components']=[{'fingerprint':fp,'weight':1} for fp in fps];spec['validation_plan']=rel(R/'plan.json');spec['sources']=plan['sources'];path=R/'specs'/(name+'.json');put(path,spec);fp=reg.fingerprint(spec);assert fp not in records or records[fp].get('result_available') is not True and records[fp]['status'] in ['blocked','abandoned'];batch.append({'name':name,'role':'candidate','spec':rel(path),'fingerprint':fp,'BTC_lookback_days':lb,'BTC_return_hurdle':hb,'BTC_exit_buffer_fraction':eb,'ETH_lookback_days':le,'ETH_return_hurdle':he,'ETH_exit_buffer_fraction':ee,'source_fingerprints':fps})
 assert len(batch)==len({x['fingerprint'] for x in batch})==280;put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/perp_dualbuffer_pair_B32H02E100bp_E28H02E100bp.json').read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_RESERVED280_OFFDIAGONAL_PARENTS_296READONLY_FULL576',sha(R/'plan.json'),flush=True)
if __name__=='__main__':main()
