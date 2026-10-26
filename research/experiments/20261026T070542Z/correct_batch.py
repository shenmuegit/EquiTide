"""Preserve invalid uncomputed definitions, then pre-register corrected money fields."""
import argparse,copy,json
from run import ROOT,R,put,sha,rel,now,reg,call

def abandon():
 assert not (R/'report.json').exists() and not (R/'abandoned_batch.json').exists()
 failures=json.loads((R/'read_failures.json').read_text());assert len(failures['facts'])==1 and failures['facts'][0]['exit_code']==1
 batch=json.loads((R/'batch.json').read_text());put(R/'abandoned_batch.json',batch);put(R/'abandoned_reserve.json',json.loads((R/'reserve.json').read_text()));put(R/'abandoned_spec.json',json.loads((R/'spec.json').read_text()))
 report={'status':'abandoned','result_available':False,'reason':'Beforefinancialevaluation,actualnotionalpreflightfailed:fixedN1000/3000butinheritedraw_entry_notional_fraction_of_initial_capitalremained0.2. All54nativeand54dependentparentdefinitionsabandoneduncomputed. Originalspecs/plan/reservelog retained. Corrected10/30percentdefinitionswillreserveagainbeforeanysimulation.','failed_preflight_log':rel(R/'notional_preflight_initial.log'),'failed_preflight_log_sha256':sha(R/'notional_preflight_initial.log'),'original_plan':rel(R/'plan.json'),'original_plan_sha256':sha(R/'plan.json'),'actual_financial_evaluations':0,'actual_cost_scenes':0,'recorded_at_utc':now(),'configs':{x['name']:{**x,'status':'abandoned','result_available':False,'reason':'invalid_money_metadata_or_dependency;noactualbacktest','original_spec_sha256':sha(ROOT/x['spec'])} for x in batch}}
 put(R/'invalid_spec_report.json',report);done=[]
 for row in batch:done.append(call('finish',row,'abandoned',rel(R/'invalid_spec_report.json')));put(R/'abandoned_finish.json',done)
 print('ABANDONED_108_INVALID_UNCOMPUTED_DEFINITIONS_NO_FINANCIAL_RESULTS',flush=True)

def reserve():
 assert len(json.loads((R/'abandoned_finish.json').read_text()))==108 and not (R/'plan_corrected.json').exists();old=json.loads((R/'abandoned_batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(records[x['fingerprint']]['status']=='abandoned' and records[x['fingerprint']]['result_available'] is False for x in old)
 plan=copy.deepcopy(json.loads((R/'plan.json').read_text()));plan['frozen_at_utc']=now();plan['preflight_correction']={'original_plan':rel(R/'plan.json'),'original_plan_sha256':sha(R/'plan.json'),'abandoned_report':rel(R/'invalid_spec_report.json'),'abandoned_report_sha256':sha(R/'invalid_spec_report.json'),'invalid_uncomputed_definitions':108,'actual_financial_evaluations_before_correction':0,'change':'Onlynativeexplicitderivedraw_entry_fraction=N/10000anddependentparentcomponentfingerprints. IntendedfixedN,fullrules,dates,data,costs,gridsandgatesunchanged.'};put(R/'plan_corrected.json',plan);(R/'specs_corrected').mkdir();mapping={};batch=[]
 for oldrow in old:
  sp=copy.deepcopy(json.loads((ROOT/oldrow['spec']).read_text()));sp['validation_plan']=rel(R/'plan_corrected.json')
  if oldrow['scope']=='native':sp['parameters']['raw_entry_notional_fraction_of_initial_capital']=sp['parameters']['fixed_entry_notional_usdt']/sp['parameters']['initial_capital_usdt']
  else:sp['components']=[{**x,'fingerprint':mapping.get(x['fingerprint'],x['fingerprint'])} for x in sp['components']]
  path=R/'specs_corrected'/(oldrow['name']+'.json');put(path,sp);fp=reg.fingerprint(sp);assert fp!=oldrow['fingerprint'] and (fp not in records or records[fp]['status'] in ['abandoned','blocked'] and records[fp].get('result_available') is False);mapping[oldrow['fingerprint']]=fp
  row={**oldrow,'spec':rel(path),'fingerprint':fp,'abandoned_definition_fingerprint':oldrow['fingerprint']}
  if row['scope']=='parent':row['source_fingerprints']=[mapping.get(fp,fp) for fp in row['source_fingerprints']]
  batch.append(row)
 assert len(batch)==len({x['fingerprint'] for x in batch})==108;put(R/'batch.json',batch);put(R/'spec.json',json.loads((ROOT/batch[0]['spec']).read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('CORRECTED_108_DEFINITIONS_RESERVED_BEFORE_CALCULATION',sha(R/'plan_corrected.json'),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['abandon','reserve']);globals()[p.parse_args().command]()
