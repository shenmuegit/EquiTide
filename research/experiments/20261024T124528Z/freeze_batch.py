"""Freeze all lookback/entry/exit cells and reserve each unseen exact definition."""
import copy,itertools,json
from run import ROOT,R,LOOKS,HURDLES,EXITS,LOOKS_BY_ASSET,NEW_LOOKS,reg,sha,put,rel,now,call,validate_lookback

def main():
 assert not (R/'plan.json').exists()
 ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');base=ROOT/'research/experiments/20261024T024326Z';plan=copy.deepcopy(json.loads((base/'plan.json').read_text()));templates=json.loads((base/'report.json').read_text())
 assert sha(R/'engine.py')==sha(base/'engine.py')
 plan.update(round=R.name,trigger_utc='2026-10-24T12:45:28.098Z',frozen_at_utc=now(),hypothesis='After the zero-exit local lookback and passive-parent studies, test whether exit buffers preserve any nearby improvement in actual single books. Joint BTC L30/31/32 and ETH L28/29/30, entry H1/2/4percent, exit E0/.25/.5/1percent.36oldcells readonly,36missing exact buffered cells new. Same seen history;not independent confirmation.')
 plan.pop('anchor_source',None)
 plan['grid']={'lookback_days_by_asset':LOOKS_BY_ASSET,'new_lookbacks_by_asset':NEW_LOOKS,'return_hurdle':HURDLES,'exit_buffer_fraction':EXITS,'assets':['BTC','ETH'],'new_financial_candidates':36,'read_only_anchor_configs':36,'full_grid_configs':72,'new_parent_backtests':0,'preset_center':{'BTC':{'lookback_days':31,'return_hurdle':.02,'exit_buffer_fraction':.005},'ETH':{'lookback_days':29,'return_hurdle':.02,'exit_buffer_fraction':.005}}}
 plan['sensitivity']='Each asset full3x3x4 joint lookback/entry/exit surface. Inclusive adjacent-index neighbors along all3 axes simultaneously.36 oldresults retain original qualification/status/neighbor grids.36 newcells use this preregistered neighborhood. Report all metrics,fullNAV DD,adjacentSharpe changes and boundaries;no adaptive expansion or untouchedtest claim.'
 plan['new_engine_change_scope']='No engine change: exact bytes of 20261024T024326Z/engine.py. Newlookback parameter only;original native signed accounting,fees,square-root impact,actual funding,axes and margin proxy unchanged.'
 plan['source_engine']={'path':rel(base/'engine.py'),'sha256':sha(base/'engine.py')}
 plan['lookback_availability']={'first_decision_day_index':33,'maximum_lookback':32,'earliest_completed_close_index':0,'indices_by_lookback':{str(L):32-L for L in LOOKS},'rule':'FirstROC C32/C(32-L),L32 uses firstavailable C0;L33 prohibited. Fixed OOS start and context not shifted.'}
 for L in LOOKS:validate_lookback(L)
 plan['novelty']={'initial16_missing_actual_results':0,'prior_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_canonical_non_observation_definitions':ctx['canonical_research_definitions_excluding_observations'],'all_prior_conclusions_read':len(ctx['prior_conclusions_read']),'multiple_testing':'Thisgrid selectedbetweenrounds from previouslyseenhistory. No DSR/PBO or untouchedholdout.36newtests are not36independentconfirmations.'}
 for source in plan['sources']:
  source['access_date']='2026-10-24'
  if 'aqr.com' in source['url']:source['scope']='Author2012traditional12monthmulti-futuresmomentum background only;our28to32daycrypto exit-buffer research is not a replication.'
 for files in plan['data']['assets'].values():
  for x in files:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 refs={};source_counts=[]
 for roundid in ['20261023T184400Z','20261024T024326Z','20261024T084457Z']:
  source=ROOT/'research/experiments'/roundid;doc=json.loads((source/'report.json').read_text());n=0
  for name,c in doc['configs'].items():
   a,L=c['asset'],c['lookback_days'];E=c.get('exit_buffer_fraction',0)
   if L not in LOOKS_BY_ASSET[a] or c['return_hurdle'] not in HURDLES or E not in EXITS:continue
   if (L==30) != (roundid!='20261024T084457Z'):continue
   rec=records[c['fingerprint']];assert rec['result_available'] is True and rec['report_sha256']==sha(source/'report.json') and rec['status']==c['status']
   refs[name]={'name':name,'fingerprint':c['fingerprint'],'asset':a,'lookback_days':L,'return_hurdle':c['return_hurdle'],'exit_buffer_fraction':E,'original_status':c['status'],'source_report':rel(source/'report.json'),'source_report_sha256':sha(source/'report.json'),'source_spec':c['spec'],'source_spec_sha256':sha(ROOT/c['spec']),'source_archive':c['archive'],'source_archive_sha256':c['archive_sha256'],'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()}};n+=1
  source_counts.append({'report':rel(source/'report.json'),'report_sha256':sha(source/'report.json'),'cells':n})
 assert len(refs)==36 and [x['cells'] for x in source_counts]==[6,18,12]
 assert len({(x['asset'],x['lookback_days'],x['return_hurdle'],x['exit_buffer_fraction']) for x in refs.values()})==36
 plan['anchor_sources']=source_counts
 put(R/'plan.json',plan);put(R/'anchors.json',refs);(R/'specs').mkdir();batch=[]
 for asset in ['BTC','ETH']:
  for L,H,E in itertools.product(NEW_LOOKS[asset],HURDLES,EXITS[1:]):
   validate_lookback(L);template=templates['configs'][f'perp_bufferexit_{asset}_L30_H{int(H*100):02d}_E{int(E*10000):03d}bp'];spec=copy.deepcopy(json.loads((ROOT/template['spec']).read_text()));name=f'perp_bufferexit_{asset}_L{L}_H{int(H*100):02d}_E{int(E*10000):03d}bp';spec['name']=name;spec['parameters']['lookback_days']=L;spec['validation_plan']=rel(R/'plan.json');spec['sources']=plan['sources'];path=R/'specs'/(name+'.json');put(path,spec);fp=reg.fingerprint(spec)
   assert fp not in records or records[fp].get('result_available') is not True and records[fp]['status'] in ['blocked','abandoned']
   batch.append({'name':name,'role':'candidate','spec':rel(path),'fingerprint':fp,'asset':asset,'lookback_days':L,'return_hurdle':H,'exit_buffer_fraction':E,'capital_usdt':10000})
 assert len(batch)==len({x['fingerprint'] for x in batch})==36
 put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/perp_bufferexit_ETH_L29_H02_E050bp.json').read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_RESERVED36_NEW_BUFFER_COMPONENTS_36OLD_READONLY',sha(R/'plan.json'),flush=True)
if __name__=='__main__':main()
