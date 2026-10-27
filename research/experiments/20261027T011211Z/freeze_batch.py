"""Freeze missing BTC-entry-hurdle/budget interactions using exact existing source pairs."""
import copy,gzip,itertools,json,hashlib,subprocess,sys
from run import ROOT,R,reg,put,sha,rel,now,call,NOTIONALS,SLOWS,LOOKS,HURDLES,EXITS,BTC_HURDLES

def main():
 assert not(R/'plan.json').exists();ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');oldR=ROOT/'research/experiments/20261026T231011Z';prior=json.loads((oldR/'plan.json').read_text());docs={};pool={}
 def ref(c,path,scope='native'):
  p=json.loads((ROOT/c['spec']).read_text())['parameters'];return {**{k:c[k] for k in ['name','fingerprint','spec','archive','archive_sha256']},'report':path,'report_sha256':sha(ROOT/path),'spec_sha256':sha(ROOT/c['spec']),'asset':('COMBO' if scope=='parent' else c['asset']),'scope':scope,'role':c['role'],'original_status':c['status'],'capital_usdt':10000 if scope=='native' else 20000,'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()},**{k:c.get(k,p.get(k)) for k in ['fixed_entry_notional_usdt','lookback_days','return_hurdle','exit_buffer_fraction','trend_lookback_days']}}
 path='research/experiments/20261025T065405Z/report.json';docs[path]=json.loads((ROOT/path).read_text());b={};nativeholds={}
 for c in docs[path]['configs'].values():
  if c['role']=='candidate' and c['asset']=='BTC' and c['lookback_days']==31 and c['exit_buffer_fraction']==.01 and c['return_hurdle'] in [.02,.04]:
   x=ref(c,path);pool[x['fingerprint']]=x;b[int(c['fixed_entry_notional_usdt']),c['return_hurdle']]=x['fingerprint']
  if c['role']=='benchmark':nativeholds[c['asset'],int(c['fixed_entry_notional_usdt'])]=c['fingerprint']
 hpath='research/experiments/20261026T130738Z/report.json';docs[hpath]=json.loads((ROOT/hpath).read_text())
 for c in docs[hpath]['configs'].values():
  if c.get('scope')=='native' and c['asset']=='BTC':
   x=ref(c,hpath);pool[x['fingerprint']]=x;b[int(c['fixed_entry_notional_usdt']),c['return_hurdle']]=x['fingerprint']
 e={}
 for fp,x in prior['component_sources'].items():
  if x['asset']=='ETH' and x['role']=='candidate' and x['lookback_days']==3:pool[fp]=x;e[int(x['fixed_entry_notional_usdt']),x['trend_lookback_days'],x['return_hurdle']]=fp
 refs=pool;assert len(b)==9 and len(e)==18 and len(refs)==27 and len(nativeholds)==6
 seen={}
 for fp,rec in records.items():
  sp=rec.get('spec',{});p=sp.get('parameters',{});cc=sp.get('components',[])
  if sp.get('kind')=='combination' and len(cc)==2 and all(x['weight']==1 for x in cc) and p.get('initial_capital_usdt')==20000 and p.get('start_utc')==prior['time_boundaries']['oos_start_utc'] and p.get('end_utc')==prior['time_boundaries']['oos_end_exclusive_utc'] and (rec.get('result_available') is True or rec['status']=='reserved'):seen[tuple(sorted(x['fingerprint'] for x in cc))]=rec
 def oldparent(rec):
  assert rec['result_available'] is True and rec['status'] in ['passed','rejected'];path=rec['report']
  if path not in docs:docs[path]=json.loads((ROOT/path).read_text())
  c=next(x for x in docs[path]['configs'].values() if x['fingerprint']==rec['fingerprint']);return ref(c,path,'parent')
 anchors={};holds={};new=[]
 for B,E,S,H,X in itertools.product(NOTIONALS,NOTIONALS,SLOWS,HURDLES,BTC_HURDLES):
  fps=[b[B,X],e[E,S,H]];pair=tuple(sorted(fps))
  if pair in seen:x=oldparent(seen[pair]);anchors[x['name']]=x
  else:new.append((B,E,S,H,X,fps))
 for B,E in itertools.product(NOTIONALS,NOTIONALS):holds[f'B{B}_E{E}']=oldparent(seen[tuple(sorted([nativeholds['BTC',B],nativeholds['ETH',E]]))])
 assert len(anchors)==72 and len(new)==90 and len(holds)==9
 rules=copy.deepcopy(prior['rules']);rules['composition']='BTCtrendL31H2/4/6percent with fixedexitE1percent,ETHslow28/31 trend-gatedreversal fixedfast3days,H2/4/6percent. IndependentNB/NE1000/2000/3000 exactexistingquantity/cost/funding/riskpaths. Full5D NB3xNE3xS2xETHH3xBTCH3=162cells;72old immutableanchors,90missingpairs only.'
 rules['allocation']='Raw1/1 means one whole10000BTC bank plus one whole10000ETH bank,parent20000. NB and NE independently1000/2000/3000,totalentry2000..6000 (10..30percent initialparent),fixedentrybudgets notcapitalweights. No normalization,compoundresizing,transfer,crossmargin,cashyield or parentrebalance.'
 rules['native_ETH_rule']['signal']=rules['native_ETH_rule']['signal'].replace('L1/2/3','L3').replace('S7/14/21/28/31','S28/31').replace('S7/14/28','S28/31')
 sources=[{**x,'access_date':'2026-10-27'} for x in prior['sources']];counts={'source_recorded_trades_checked':0,'source_recorded_funding_checked':0}
 for fp,x in refs.items():
  assert sha(ROOT/x['report'])==x['report_sha256'] and sha(ROOT/x['spec'])==x['spec_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256'] and records[fp]['status']==x['original_status'] and records[fp]['report_sha256']==x['report_sha256'];arc=json.loads(gzip.decompress((ROOT/x['archive']).read_bytes()));assert reg.fingerprint(arc['spec'])==fp;counts['source_recorded_trades_checked']+=sum(len(z['trades']) for z in arc['scenes'].values());counts['source_recorded_funding_checked']+=sum(len(z['funding_events']) for z in arc['scenes'].values())
 assert counts['source_recorded_funding_checked']==27*3*1110
 srcpath='research/experiments/20261026T231011Z/engine.py';assert sha(R/'engine.py')==sha(ROOT/srcpath)
 plan={'round':R.name,'trigger_utc':'2026-10-27T01:12:11.472Z','frozen_at_utc':now(),'hypothesis':'Knownpast budget/exit tests did not repair recent6of8. Test predeclared BTCentryH2/4/6percent jointly with independentNB/NE and ETHfast3/S28or31/H2or4or6. Do not use candidate-forward data to select parameters or change frozenoriginalcandidate. Compare samebudgetH4 and heldlong;entry changes exposure/turnover.','grid':{'BTC_fixed_entry_notional_usdt':NOTIONALS,'ETH_fixed_entry_notional_usdt':NOTIONALS,'trend_filter_lookback_days':SLOWS,'reversal_lookback_days':[3],'reversal_return_hurdle':HURDLES,'BTC_return_hurdle':BTC_HURDLES,'trend_exit_buffer_fraction':[.01],'full_candidate_cells':162,'readonly_old_cells':72,'new_candidate_cells':90,'new_benchmark_parents':0,'old_benchmark_parents':9,'new_financial_configs':90,'new_native_backtests':0,'cost_scenes':270,'adjacent_edges':513,'raw_component_multipliers':[1,1],'component_capitals_usdt':[10000,10000],'parent_capital_usdt':20000,'entry_budget_sum_range_usdt':[2000,6000]},'time_boundaries':prior['time_boundaries'],'data':prior['data'],'component_sources':refs,'read_only_anchor_references':anchors,'read_only_hold_references':holds,'source_engine':{'path':srcpath,'sha256':sha(ROOT/srcpath)},'native_engine_base':{'path':srcpath,'sha256':sha(ROOT/srcpath)},'rules':rules,'component_costs':prior['component_costs'],'sources':sources,'gates':prior['gates'],'validation':prior['validation'],'sensitivity':'Fiveaxes NB3,NE3,slow2,H3,BTChurdle3;adjacentsortedindexradius1,selfincluded,162cells/513edges. Slowspacing3days and BTChurdlespacing2percentagepoints;neighborsareindexbased,not equalphysicaldistance. Only90newrated,72oldqualificationsunchanged;9existingholdcontrolsreadonly.','limits':['Repeatedlyused370dayhistory;90newcorrelatedportfolio trials after earlierexperiments. No untouchedholdout,DSR/PBOorstableliveprofit.','All27native81costNAVs recovered from savedactualcash/q/entrystates,originalSHAverified. No oldsignal/lot/tick/funding/cost modelrerun,NAVrescaling or syntheticnewmarketdata.','Bothbudget and entryhurdle affectrisk/timeinmarket;matchednominalbudgets are not equalrealizedrisk.','Minute/hour/funding NAV sampling,estimatedspread/slippage/impact and1percentmaintenanceproxy lacktick/L2/TCA/fullhistoricalmargin-tier guarantees.','OriginalBTC31H4/E1 N1000 +ETHslow28L3H2 N3000 prospectivecandidate staysfrozen,starts2026-10-27UTC00:01;SMAandpaper10immutable.'],'novelty':{'initial16_missing_actual_results':0,'prior_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_conclusions_read':len(ctx['prior_conclusions_read']),'semantic_pair_check':'ExacttwoN/entryhurdle-specific sourcefingerprints,raw1/1,20000capital,370dayboundaries checked against all completed/reserved records;90missingcandidatepairs only.'},'recorded_source_events':counts,'original_candidate_preserved':prior['original_candidate_preserved'],'helpers':prior['helpers']}
 for fs in plan['data']['assets'].values():
  for x in fs:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 put(R/'plan.json',plan);put(R/'anchors.json',anchors);put(R/'holds.json',holds);(R/'specs').mkdir(exist_ok=True);batch=[]
 def params(x):return records[x['fingerprint']]['spec']['parameters']
 template=next(x for x in anchors.values() if params(x)['BTC_return_hurdle']==.04);rulehash=hashlib.sha256(json.dumps({'rules':rules,'costs':plan['component_costs']},sort_keys=True,separators=(',',':')).encode()).hexdigest()
 for B,E,S,H,X,fps in new:
  sp=copy.deepcopy(json.loads((ROOT/template['spec']).read_text()));name=f'entryind370_B{B}_E{E}_S{S}_EH{int(H*100):02d}_BH{int(X*100):02d}';sp.update(name=name,family='btc-trend-eth-gated-reversal-independent-budgets-entry-hurdle',logic=rules,validation_plan=rel(R/'plan.json'),sources=sources);sp['components']=[{'fingerprint':fp,'weight':1} for fp in fps];sp['parameters'].update(component_initial_entry_notionals_usdt=[B,E],BTC_fixed_entry_notional_usdt=B,ETH_fixed_entry_notional_usdt=E,trend_filter_lookback_days=S,ETH_trend_lookback_days=S,reversal_lookback_days=3,ETH_lookback_days=3,reversal_return_hurdle=H,ETH_return_hurdle=H,BTC_lookback_days=31,BTC_return_hurdle=X,BTC_exit_buffer_fraction=.01,trend_exit_buffer_fraction=.01,ETH_exit_buffer_fraction=0,source_rules_and_costs_sha256=rulehash)
  old1=next(x for x in anchors.values() if params(x)['BTC_return_hurdle']==.04 and params(x)['BTC_fixed_entry_notional_usdt']==B and params(x)['ETH_fixed_entry_notional_usdt']==E and params(x)['ETH_trend_lookback_days']==S and params(x)['ETH_return_hurdle']==H);path=R/'specs'/(name+'.json');put(path,sp);fp=reg.fingerprint(sp);assert fp not in records or records[fp].get('result_available') is False and records[fp]['status'] in ['blocked','abandoned'];batch.append({'name':name,'role':'candidate','scope':'parent','asset':'COMBO','capital_usdt':20000,'BTC_fixed_entry_notional_usdt':B,'ETH_fixed_entry_notional_usdt':E,'trend_filter_lookback_days':S,'reversal_lookback_days':3,'reversal_return_hurdle':H,'trend_exit_buffer_fraction':.01,'BTC_lookback_days':31,'BTC_return_hurdle':X,'source_fingerprints':fps,'matched_entry4_reference':old1['name'],'spec':rel(path),'fingerprint':fp})
 assert len(batch)==len({x['fingerprint'] for x in batch})==90;put(R/'batch.json',batch);put(R/'spec.json',json.loads((ROOT/batch[0]['spec']).read_text()));cmd=[sys.executable,str(R/'check_definitions.py')];start=now();z=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);(R/'definition_preflight.log').write_text(z.stdout+z.stderr);put(R/'definition_preflight_command.json',{'command':cmd,'cwd':str(ROOT),'started_utc':start,'finished_utc':now(),'exit_code':z.returncode,'stdout':z.stdout,'stderr':z.stderr});assert z.returncode==0,z.stderr;done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_RESERVED_90_ENTRY_BUDGET_PARENTS',sha(R/'plan.json'),json.dumps(counts),flush=True)
if __name__=='__main__':main()
