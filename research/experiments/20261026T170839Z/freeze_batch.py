"""Freeze the missing BTC28day/H6 interaction cell across nativeN and ETH grids."""
import copy,gzip,itertools,json,hashlib
from decimal import Decimal as D
from run import ROOT,R,SLOWS,LOOKS,HURDLES,NOTIONALS,reg,sha,rel,put,now,call

def main():
 assert not(R/'plan.json').exists();ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl')
 dirs={k:ROOT/'research/experiments'/v for k,v in {'trend':'20261025T065405Z','gate':'20261025T185633Z','budget':'20261026T070542Z','hold':'20261025T085436Z','entry6':'20261026T130738Z','look':'20261026T150838Z'}.items()};docs={k:json.loads((p/'report.json').read_text()) for k,p in dirs.items()};prior=json.loads((dirs['look']/'plan.json').read_text());refs={};anchors={};holds={}
 def ref(c,key,scope,kind):
  folder=dirs[key];sp=json.loads((ROOT/c['spec']).read_text());fp=c['fingerprint'];rec=records[fp];assert rec['result_available'] is True and rec['status']==c['status'] and rec['report_sha256']==sha(folder/'report.json') and sha(ROOT/c['archive'])==c['archive_sha256'] and reg.fingerprint(sp)==fp
  x={**{q:c[q] for q in ['name','fingerprint','role','spec','archive','archive_sha256']},'asset':c.get('asset','COMBO'),'scope':scope,'reference_kind':kind,'report':rel(folder/'report.json'),'report_sha256':sha(folder/'report.json'),'spec_sha256':sha(ROOT/c['spec']),'original_status':c['status'],'capital_usdt':sp['parameters']['initial_capital_usdt'],'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()}}
  for q in ['fixed_entry_notional_usdt','lookback_days','return_hurdle','exit_buffer_fraction','trend_lookback_days','trend_filter_lookback_days','reversal_lookback_days','reversal_return_hurdle','trend_exit_buffer_fraction','BTC_lookback_days','BTC_return_hurdle','BTC_fixed_entry_notional_usdt','ETH_fixed_entry_notional_usdt']:
   if q in c:x[q]=c[q]
  if scope=='native':assert D(str(sp['parameters']['fixed_entry_notional_usdt']))==D(str(sp['parameters']['raw_entry_notional_fraction_of_initial_capital']))*D(str(sp['parameters']['initial_capital_usdt']))
  return x
 def native(c,key):
  x=ref(c,key,'native','cached_native');refs[x['fingerprint']]=x;anchors[x['name']]=x
 for c in docs['trend']['configs'].values():
  if c['role']=='candidate' and c['asset']=='BTC' and c['return_hurdle']==.04 and c['exit_buffer_fraction']==.01:native(c,'trend')
 for key in ['gate','budget']:
  for c in docs[key]['configs'].values():
   if c['scope']=='native':
    x=ref(c,key,'native','cached_native');refs[x['fingerprint']]=x
   elif c['trend_exit_buffer_fraction']==.01:anchors[c['name']]=ref(c,key,'parent','immutable_old_parent')
 for c in docs['entry6']['configs'].values():
  if c['scope']=='native':native(c,'entry6')
  else:anchors[c['name']]=ref(c,'entry6','parent','immutable_old_parent')
 for c in docs['look']['configs'].values():
  if c['scope']=='native' and c['lookback_days']==28:native(c,'look')
  elif c['scope']=='parent' and c['BTC_lookback_days']==28:anchors[c['name']]=ref(c,'look','parent','immutable_old_parent')
 for c in docs['hold']['configs'].values():
  if c['role']=='benchmark':holds['B'+str(c['BTC_fixed_entry_notional_usdt'])+'_E'+str(c['ETH_fixed_entry_notional_usdt'])]=ref(c,'hold','parent','matched_hold')
 assert len(refs)==90 and len(anchors)==252 and len(holds)==3 and len({x['fingerprint'] for x in [*refs.values(),*anchors.values(),*holds.values()]})==336
 bybtc={(x['fixed_entry_notional_usdt'],x['lookback_days'],x['return_hurdle']):fp for fp,x in refs.items() if x['asset']=='BTC'};byeth={(x['fixed_entry_notional_usdt'],x['trend_lookback_days'],x['lookback_days'],x['return_hurdle']):fp for fp,x in refs.items() if x['asset']=='ETH'};assert len(bybtc)==9 and len(byeth)==81
 rules=copy.deepcopy(prior['rules']);rules['composition']='BTCROClook28/31 x entryH4/6percent,exitE1percent. ETHslow-gatedreversalN1000/2000/3000,S7/14/28,L1/2/3,H2/4/6percent;BTC_N=4000-ETH_N. Raw1/1means2whole10000banks,parent20000,totalfixedentry4000. Fullnative3D12cells(N,BTC_L,BTC_H):9old+3newL28H6. Fullparent6D324cells(N_ETH,S,L_ETH,H_ETH,BTC_L,BTC_H):243old+81newL28H6. Do not infer interaction from separate one-axis experiments.';rules['interpretation']='ExistingL31H6entryfilterreducedcostsandL28H4horizonschangedregimeexposure;theirjointL28H6effectisnotknown. Predeclareone missingrectangularcellfor3Nandall81ETHpairs,notpostresultpick. OriginalL31H4/E1prospectivecandidateunchanged,noNAVresizingorweightnormalization.'
 sources=[{**x,'access_date':'2026-10-26','scope':'Officialpage readthisround;traditionalown-returntrend/equitycoststudyisbackground. CryptoBTClook/entryinteractionandETHgatebudgetareourhypothesis,notpaperreplicationorprofit/capacitytransfer.'} for x in prior['sources']]
 counts={'source_recorded_trades_checked':0,'source_recorded_funding_checked':0,'source_native_components':90,'source_cost_NAVs':270}
 for x in refs.values():
  a=json.loads(gzip.decompress((ROOT/x['archive']).read_bytes()));counts['source_recorded_trades_checked']+=sum(len(s['trades']) for s in a['scenes'].values());counts['source_recorded_funding_checked']+=sum(len(s['funding_events']) for s in a['scenes'].values())
 assert counts['source_recorded_funding_checked']==90*3*1110
 original=prior['original_candidate_preserved'];assert sha(ROOT/original['spec'])==original['spec_sha256'] and records[original['fingerprint']]['status']=='passed';source_engine={'path':'research/experiments/20261025T065405Z/engine.py','sha256':sha(ROOT/'research/experiments/20261025T065405Z/engine.py')};assert sha(R/'engine.py')==source_engine['sha256']
 gates=copy.deepcopy(prior['gates']);gates['native_BTC_3D_local_3x_positive_fraction_min']=.6;gates['parent_6D_local_3x_positive_fraction_min']=.6
 plan={'round':R.name,'trigger_utc':'2026-10-26T17:08:39.689Z','frozen_at_utc':now(),'hypothesis':'CompletejointBTClook28/31 andentry4/6 rectangle:3newL28H6nativeN and81newmixedparents. ExistingL28H4/L31H4/L31H6areimmutablecontrols. Reusedhistory,separateaxesarenotindependentconfirmation,originalprospectivecandidateunchanged.','grid':{'ETH_fixed_entry_notional_usdt':NOTIONALS,'trend_filter_lookback_days':SLOWS,'reversal_lookback_days':LOOKS,'reversal_return_hurdle':HURDLES,'BTC_lookback_days':[28,31],'BTC_return_hurdle':[.04,.06],'BTC_exit_fixed':.01,'new_condition':'BTC_lookback_days==28 and BTC_return_hurdle==.06','new_financial_configs':84,'new_native_backtests':3,'new_parent_configs':81,'cost_scenes':252,'readonly_old_native_cells':9,'readonly_old_parent_cells':243,'full_3D_native_cells':12,'full_6D_parent_cells':324,'adjacent_edges_native':20,'adjacent_edges_parent':1188,'cost_multipliers':[1,2,3],'raw_component_multipliers':[1,1],'component_capitals_usdt':[10000,10000],'parent_capital_usdt':20000,'entry_budget_sum_usdt':4000,'BTC_entry_formula':'4000-ETH_N'},'time_boundaries':prior['time_boundaries'],'data':prior['data'],'component_sources':refs,'read_only_anchor_references':anchors,'read_only_hold_references':holds,'source_engine':source_engine,'native_engine_base':source_engine,'new_engine_sha256':sha(R/'engine.py'),'rules':rules,'component_costs':prior['component_costs'],'sources':sources,'gates':gates,'sensitivity':'FullnativeN3 xBTC_L2 xBTC_H2=12cells/20edges;parentN3 xS3 xL_ETH3 xH_ETH3 xBTC_L2 xBTC_H2=324cells/1188edges. Inclusiveadjacentindexneighbors;only84newclassified. Old252keeporiginalqualifications/status/reportbytes,notreratedwithnewdimensions.','validation':prior['validation'],'limits':['Allhistoryrepeatedlyused;84newcorrelatedtrialsafterpriorresults. No untouchedholdout,DSR/PBOorstableliveprofit.','3newnativeBTCN-specificq/cost/lot/tick/funding/riskpaths;90cachednative270costNAVsrecoveredfromsavedstateswithoriginalSHA,nooldmodelrerun.','33completecontextdayssupportmaxlook31withnonegativeindex/futurewarmup.','OriginalL31H4/E1candidatefrozenforindependentnewdata,newinteractionresultcannotreplaceit.','NoL2/queues/TCA/fullmargin-tiermodel; sampledNAV and1percentmaintenanceproxyarelimited.'],'novelty':{'initial16_missing_actual_results':0,'prior_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_conclusions_read':len(ctx['prior_conclusions_read']),'semantic_resolution':'Fullnativeparam/rules/dates/inputSHAandparentcomponentpair/rawweightscheckedbeforeeveryreserve;only3newL28H6native+81parents.'},'recorded_source_events':counts,'original_candidate_preserved':original,'helpers':prior['helpers']}
 for fs in plan['data']['assets'].values():
  for x in fs:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 put(R/'plan.json',plan);put(R/'anchors.json',anchors);put(R/'holds.json',holds);(R/'specs').mkdir();batch=[]
 for N in NOTIONALS:
  old31=refs[bybtc[N,31,.06]];old4=refs[bybtc[N,28,.04]];sp=copy.deepcopy(json.loads((ROOT/old31['spec']).read_text()));sp['parameters']['lookback_days']=28;name=f'jointnative370_BTC_L28_H06_E100_N{N}';sp.update(name=name,validation_plan=rel(R/'plan.json'),sources=sources);assert sp['parameters']['return_hurdle']==.06 and sp['parameters']['fixed_entry_notional_usdt']==N and sp['parameters']['raw_entry_notional_fraction_of_initial_capital']==N/10000
  path=R/'specs'/(name+'.json');put(path,sp);fp=reg.fingerprint(sp);assert fp not in records or records[fp].get('result_available') is False and records[fp]['status'] in ['blocked','abandoned'];bybtc[N,28,.06]=fp;batch.append({'name':name,'role':'candidate','scope':'native','asset':'BTC','capital_usdt':10000,'fixed_entry_notional_usdt':N,'lookback_days':28,'return_hurdle':.06,'exit_buffer_fraction':.01,'matched_old_BTC_L31':old31['name'],'matched_old_BTC_H4':old4['name'],'spec':rel(path),'fingerprint':fp})
 seen=set()
 for rec in records.values():
  sp=rec.get('spec',{});cc=sp.get('components',[]);p=sp.get('parameters',{})
  if sp.get('kind')=='combination' and len(cc)==2 and all(x['weight']==1 for x in cc) and p.get('initial_capital_usdt')==20000 and p.get('start_utc')==plan['time_boundaries']['oos_start_utc'] and p.get('end_utc')==plan['time_boundaries']['oos_end_exclusive_utc'] and (rec.get('result_available') is True or rec['status']=='reserved'):seen.add(tuple(sorted(x['fingerprint'] for x in cc)))
 rulehash=hashlib.sha256(json.dumps({'rules':rules,'costs':plan['component_costs']},sort_keys=True,separators=(',',':')).encode()).hexdigest()
 for NE,S,L,H in itertools.product(NOTIONALS,SLOWS,LOOKS,HURDLES):
  NB=4000-NE;fps=[bybtc[NB,28,.06],byeth[NE,S,L,H]];assert tuple(sorted(fps)) not in seen
  matches=lambda c:c['scope']=='parent' and c.get('ETH_fixed_entry_notional_usdt',2000)==NE and c['trend_filter_lookback_days']==S and c['reversal_lookback_days']==L and c['reversal_return_hurdle']==H
  old31=next(c for c in docs['entry6']['configs'].values() if matches(c));old4=next(c for c in docs['look']['configs'].values() if matches(c) and c['BTC_lookback_days']==28)
  sp=json.loads((ROOT/old31['spec']).read_text());sp.update(family='btc-trend-eth-gated-reversal-fixed-total-entry-budget',logic=rules);sp['parameters'].update(BTC_lookback_days=28,BTC_return_hurdle=.06,trend_exit_buffer_fraction=.01,BTC_exit_buffer_fraction=.01,source_rules_and_costs_sha256=rulehash);sp['components']=[{'fingerprint':fp,'weight':1} for fp in fps];name=f'jointbudget370_B{NB}_E{NE}_S{S}_L{L}_H{int(H*100):02d}_BL28_BH06';sp.update(name=name,validation_plan=rel(R/'plan.json'),sources=sources);path=R/'specs'/(name+'.json');put(path,sp);fp=reg.fingerprint(sp);assert fp not in records or records[fp].get('result_available') is False and records[fp]['status'] in ['blocked','abandoned'];batch.append({'name':name,'role':'candidate','scope':'parent','asset':'COMBO','capital_usdt':20000,'BTC_fixed_entry_notional_usdt':NB,'ETH_fixed_entry_notional_usdt':NE,'trend_filter_lookback_days':S,'reversal_lookback_days':L,'reversal_return_hurdle':H,'trend_exit_buffer_fraction':.01,'BTC_lookback_days':28,'BTC_return_hurdle':.06,'source_fingerprints':fps,'matched_old_BTC_L31':old31['name'],'matched_old_BTC_H4':old4['name'],'spec':rel(path),'fingerprint':fp})
 assert len(batch)==len({x['fingerprint'] for x in batch})==84;put(R/'batch.json',batch);put(R/'spec.json',json.loads((ROOT/batch[0]['spec']).read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_RESERVED_3_NEW_NATIVE_AND_81_JOINT_PARENTS',sha(R/'plan.json'),json.dumps(counts),flush=True)
if __name__=='__main__':main()
