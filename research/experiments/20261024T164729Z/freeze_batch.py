"""Freeze the upper exit-buffer boundary before evaluating any of its cells."""
import copy,itertools,json
from run import ROOT,R,LOOKS,HURDLES,EXITS,NEW_EXITS,LOOKS_BY_ASSET,reg,sha,put,rel,now,call,validate_lookback

def main():
 assert not (R/'plan.json').exists();ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');base=ROOT/'research/experiments/20261024T124528Z';plan=copy.deepcopy(json.loads((base/'plan.json').read_text()));templates=json.loads((base/'report.json').read_text());assert sha(R/'engine.py')==sha(base/'engine.py')
 plan.update(round=R.name,trigger_utc='2026-10-24T16:47:29.056Z',frozen_at_utc=now(),hypothesis='Extend the previously fixed1percent upper exit-buffer edge to1.5/2percent at BTC31/32 andETH28/29,entry H2/4percent. H1excluded because E<=H would be violated,not because of past returns. Wider exits can reduce churn but delay loss recognition.16new exactcomponent cells,32oldcells readonly in48cell fullsurface. Previouslyseen330dayhistory;not independentconfirmation.')
 plan['grid']={'lookback_days_by_asset':LOOKS_BY_ASSET,'return_hurdle':HURDLES,'exit_buffer_fraction':EXITS,'new_exit_buffer_fraction':NEW_EXITS,'assets':['BTC','ETH'],'new_financial_candidates':16,'read_only_anchor_configs':32,'full_grid_configs':48,'new_parent_backtests':0,'preset_center':{'BTC':{'lookback_days':31,'return_hurdle':.04,'exit_buffer_fraction':.015},'ETH':{'lookback_days':28,'return_hurdle':.02,'exit_buffer_fraction':.015}},'domain':'0<=exitbuffer<=entryhurdle;E2percent equals H2percent is valid,strict entry and equalityexit retained.'}
 plan['sensitivity']='Perasset2lookbacks x2entryhurdles x6exitbuffers,24cells;full48 across2assets. Inclusive adjacent-index3axis neighborhoods;H2/4 andEgrid steps are heterogeneous.32oldqualifications unchanged.16newcells rated on thisdeclaredgrid only;do not expand afterresults. Preplanned contrasts against exact matched E0 and E1percent oldcells.'
 plan['new_engine_change_scope']='No engine changes:exact bytes of 20261024T024326Z bufferengine. Only spec exit_buffer_fraction changes from1percent template to1.5/2percent;fixed lookback,signal accounting,costs,actualfunding andnative constraints preserved.'
 plan['source_engine']={'path':rel(base/'engine.py'),'sha256':sha(base/'engine.py')}
 plan['lookback_availability']={'first_decision_day_index':33,'maximum_lookback':32,'earliest_completed_close_index':0,'indices_by_lookback':{str(L):32-L for L in LOOKS},'rule':'L32 firstROC C32/C0;L33 prohibited. OOS start/end andsourcecontext unchanged.'}
 for L in LOOKS:validate_lookback(L)
 plan['novelty']={'initial16_missing_actual_results':0,'prior_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_canonical_non_observation_definitions':ctx['canonical_research_definitions_excluding_observations'],'all_prior_conclusions_read':len(ctx['prior_conclusions_read']),'multiple_testing':'Upperedge extension selectedbetweenrounds onseenhistory. No untouchedholdout,DSR/PBO or independent/liveprofit claim.'}
 for s in plan['sources']:
  s['access_date']='2026-10-24'
  if 'aqr.com' in s['url']:s['scope']='Author2012traditional12monthmulti-futuresmomentum background only;our28to32daycrypto buffered-exit research is not a replication.'
 for files in plan['data']['assets'].values():
  for x in files:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 refs={};source_counts=[]
 for roundid in ['20261024T084457Z','20261024T124528Z']:
  source=ROOT/'research/experiments'/roundid;doc=json.loads((source/'report.json').read_text());n=0
  for name,c in doc['configs'].items():
   a,L,H=c['asset'],c['lookback_days'],c['return_hurdle'];E=c.get('exit_buffer_fraction',0)
   if L not in LOOKS_BY_ASSET[a] or H not in HURDLES or E not in EXITS[:4]:continue
   rec=records[c['fingerprint']];assert rec['result_available'] is True and rec['report_sha256']==sha(source/'report.json') and rec['status']==c['status'];refs[name]={'name':name,'fingerprint':c['fingerprint'],'asset':a,'lookback_days':L,'return_hurdle':H,'exit_buffer_fraction':E,'original_status':c['status'],'source_report':rel(source/'report.json'),'source_report_sha256':sha(source/'report.json'),'source_spec':c['spec'],'source_spec_sha256':sha(ROOT/c['spec']),'source_archive':c['archive'],'source_archive_sha256':c['archive_sha256'],'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()}};n+=1
  source_counts.append({'report':rel(source/'report.json'),'report_sha256':sha(source/'report.json'),'cells':n})
 assert len(refs)==32 and [x['cells'] for x in source_counts]==[8,24];plan['anchor_sources']=source_counts;put(R/'plan.json',plan);put(R/'anchors.json',refs);(R/'specs').mkdir();batch=[]
 for asset in ['BTC','ETH']:
  for L,H,E in itertools.product(LOOKS_BY_ASSET[asset],HURDLES,NEW_EXITS):
   assert E<=H;template=templates['configs'][f'perp_bufferexit_{asset}_L{L}_H{int(H*100):02d}_E100bp'];spec=copy.deepcopy(json.loads((ROOT/template['spec']).read_text()));name=f'perp_bufferexit_{asset}_L{L}_H{int(H*100):02d}_E{int(round(E*10000)):03d}bp';spec['name']=name;spec['parameters']['exit_buffer_fraction']=E;spec['validation_plan']=rel(R/'plan.json');spec['sources']=plan['sources'];path=R/'specs'/(name+'.json');put(path,spec);fp=reg.fingerprint(spec);assert fp not in records or records[fp].get('result_available') is not True and records[fp]['status'] in ['blocked','abandoned'];batch.append({'name':name,'role':'candidate','spec':rel(path),'fingerprint':fp,'asset':asset,'lookback_days':L,'return_hurdle':H,'exit_buffer_fraction':E,'capital_usdt':10000})
 assert len(batch)==len({x['fingerprint'] for x in batch})==16;put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/perp_bufferexit_ETH_L28_H02_E150bp.json').read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_RESERVED16_NEW_UPPER_EXITBUFFER_CELLS_32OLD_READONLY',sha(R/'plan.json'),flush=True)
if __name__=='__main__':main()
