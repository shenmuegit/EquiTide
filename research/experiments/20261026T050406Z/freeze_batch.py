"""Freeze BTC gated reversal plus ETH trend, with a complete four-axis grid."""
import copy,gzip,itertools,json,hashlib
from run import ROOT,R,SLOWS,LOOKS,HURDLES,BUFFERS,reg,sha,rel,put,now,call

def main():
 assert not (R/'plan.json').exists()
 ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl')
 prior=json.loads((ROOT/'research/experiments/20261026T030210Z/plan.json').read_text())
 mixed_path=ROOT/'research/experiments/20261025T145537Z/report.json';mixed=json.loads(mixed_path.read_text())
 mp=json.loads((mixed_path.parent/'plan.json').read_text());refs={}
 for fp,ref in prior['component_sources'].items():
  if ref['asset']=='BTC':refs[fp]=copy.deepcopy(ref);refs[fp]['style']='gated_reversal'
 for fp,ref in mp['component_sources'].items():
  if ref['asset']=='ETH' and ref['style']=='trend':refs[fp]={**copy.deepcopy(ref),'fingerprint':fp,'scope':'native'}
 assert len(refs)==30 and sum(x['asset']=='BTC' for x in refs.values())==27
 anchors={}
 for c in mixed['configs'].values():
  if c['style']!='btc_reversal_eth_trend':continue
  sp=json.loads((ROOT/c['spec']).read_text());assert sp['parameters']['initial_capital_usdt']==20000 and sp['parameters']['component_initial_entry_notionals_usdt']==[2000,2000]
  anchors[c['name']]={**{p:c[p] for p in ['name','fingerprint','spec','archive','archive_sha256','style','trend_exit_buffer_fraction','reversal_lookback_days','reversal_return_hurdle']},'report':rel(mixed_path),'report_sha256':sha(mixed_path),'spec_sha256':sha(ROOT/c['spec']),'original_status':c['status'],'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()},'reference_kind':'same_L_H_ETH_E_without_BTC_slow_gate'}
 holds=copy.deepcopy(prior['read_only_hold_references']);assert len(anchors)==27 and len(holds)==1
 counts={'source_recorded_trades_checked':0,'source_recorded_funding_checked':0,'source_native_components':30,'source_cost_NAVs':90}
 for x in [*refs.values(),*anchors.values(),*holds.values()]:
  rec=records[x['fingerprint']];assert rec['result_available'] is True and rec['status']==x['original_status'] and rec['report_sha256']==x['report_sha256'];assert sha(ROOT/x['report'])==x['report_sha256'] and sha(ROOT/x['spec'])==x['spec_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256']
  if x['fingerprint'] in refs:
   arc=json.loads(gzip.decompress((ROOT/x['archive']).read_bytes()));assert reg.fingerprint(arc['spec'])==x['fingerprint'] and arc['spec']['parameters']['initial_capital_usdt']==10000 and arc['spec']['parameters']['fixed_entry_notional_usdt']==2000
   counts['source_recorded_trades_checked']+=sum(len(s['trades']) for s in arc['scenes'].values());counts['source_recorded_funding_checked']+=sum(len(s['funding_events']) for s in arc['scenes'].values())
 assert counts['source_recorded_funding_checked']==99900
 bybtc={(x['trend_lookback_days'],x['lookback_days'],x['return_hurdle']):fp for fp,x in refs.items() if x['asset']=='BTC'}
 byeth={x['exit_buffer_fraction']:fp for fp,x in refs.items() if x['asset']=='ETH'}
 assert len(bybtc)==27 and len(byeth)==3 and all(refs[fp]['lookback_days']==28 and refs[fp]['return_hurdle']==.02 for fp in byeth.values())
 bs=json.loads((ROOT/refs[next(iter(bybtc.values()))]['spec']).read_text());es=json.loads((ROOT/refs[next(iter(byeth.values()))]['spec']).read_text())
 rules={k:copy.deepcopy(prior['rules'][k]) for k in ['allocation','ledger','alignment','state','risk']}
 rules.update(composition='BTCslow-trend-conditionedfastROCcontrarianS7/14/28,L1/2/3,H2/4/6percent;ETHown-returntrendL28,H2percent,exitE.5/1/2percent.81allpresetnewparentpairs,four-axisSxLxHxE.27oldungatedBTCcontrarian+ETHtrendparentsonlymatchedreadonlycontrols,notgridcells.',native_BTC_rule=bs['logic'],native_ETH_rule=es['logic'],interpretation='Trend-followingETHmayremainactivewhenBTCgateiscash;nocorrelation/returnimprovementassumed. Assetstylesfixedbeforeevaluation,nofuturebasedswitching. Sourcefingerprintsretaincompleteoriginalquantity/cost/funding/cash paths.')
 sources=[{'url':'https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum','access_date':'2026-10-26','version':'Moskowitz,Ooi,Pedersen officialpage2012-05-01','scope':'Officialpagereadthisround;12monthtraditionalfuturesown-returnpredictabilityisbackgroundonly. BTCshort1/2/3reversalconditionedon7/14/28andETH28daytrendareourhypothesis,notreplicationorcrypto profitproof.'},{'url':'https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies','access_date':'2026-10-26','version':'Frazzini,Israel,Moskowitz officialpage2012-12-05','scope':'Officialpagereadthisround;equityreversalimplementationcostfragilitymotivatesstrictcoststress. No equitycapacity/profitresulttransferredtocrypto.'}]
 plan={'round':R.name,'trigger_utc':'2026-10-26T05:04:06.385Z','frozen_at_utc':now(),'hypothesis':'PriorBTC+ETHgatedreversalparentsfailedrecentconsistency. TestfixedBTCgatedreversalplusETHtrendtochangeactivityandlossfoldtiming,notmerelyfaster/slowerbothreversal. Assetassignmentfixed;no benefitassumed.','grid':{'BTC_trend_lookback_days':SLOWS,'reversal_lookback_days':LOOKS,'reversal_return_hurdle':HURDLES,'trend_exit_buffer_fraction':BUFFERS,'new_financial_configs':81,'new_native_backtests':0,'new_parent_configs':81,'readonly_ungated_parent_controls':27,'full_4D_parent_cells':81,'cost_scenes':243,'cost_multipliers':[1,2,3],'raw_component_multipliers':[1,1],'component_capitals_usdt':[10000,10000],'parent_capital_usdt':20000,'entry_budget_each_usdt':2000,'entry_budget_total_usdt':4000,'readonly_native_components':30},'time_boundaries':prior['time_boundaries'],'data':prior['data'],'component_sources':refs,'read_only_anchor_references':anchors,'read_only_hold_references':holds,'source_engine':prior['source_engine'],'native_engine_base':prior['native_engine_base'],'new_engine_sha256':sha(R/'engine.py'),'rules':rules,'component_costs':prior['component_costs'],'sources':sources,'gates':prior['gates'],'sensitivity':'Full81newcell4D SxLxHxETH_E,216adjacentedges,inclusiveadjacentindexneighborhoods. Old27ungatedcontrolsarecomparisononly,originalqualification/status/reportbytesunchanged. Noafter-resultgridextension.','validation':prior['validation'],'limits':[x for x in prior['limits'] if '54' not in x and 'No-gatecontrolsreadonly' not in x]+['81correlatednewpairtrialsafterknownhistory;notindependentunseenconfirmation.','All30nativeledgersalreadyactual;recoveroriginalNAVSHAfromsavedstateandrealprices,nosignal/order/fundingmodelrerun.','27matchedoldungatedportfoliosshareETHcomponentandBTCshortL/H/N2000;newBTCslowgatechangesentirecash/funding/quantityhistory,notaposthocNAVfilter.'],'novelty':{'initial16_missing_actual_results':0,'prior_registry_events':ctx['registry_events'],'prior_registry_ids':ctx['registry_ids'],'prior_conclusions_read':len(ctx['prior_conclusions_read']),'semantic_resolution':'Fullledgerchecksortedcomponentfingerprintpairs/raw1/1/20000capital/datesbeforeeveryreserve. BTCgate+ETHtrenddiffersfromoldBTCtrend+ETHgateandBTCgate+ETHgate. Reordered/numericformattedcopiesexcluded.','selection_bias':'Known370day/recent40historyafterprioroutcomes;81correlatedtrialsnotunseenconfirmation,DSR/PBOorstableliveprofit.'},'recorded_source_events':counts,'helpers':prior['helpers']}
 for fs in plan['data']['assets'].values():
  for x in fs:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 seen=set()
 for rec in records.values():
  sp=rec.get('spec',{});cc=sp.get('components',[]);p=sp.get('parameters',{})
  if sp.get('kind')=='combination' and len(cc)==2 and all(x['weight']==1 for x in cc) and p.get('initial_capital_usdt')==20000 and p.get('start_utc')==plan['time_boundaries']['oos_start_utc'] and p.get('end_utc')==plan['time_boundaries']['oos_end_exclusive_utc'] and (rec.get('result_available') is True or rec['status']=='reserved'):seen.add(tuple(sorted(x['fingerprint'] for x in cc)))
 put(R/'plan.json',plan);put(R/'anchors.json',anchors);put(R/'holds.json',holds);(R/'specs').mkdir();batch=[];rulehash=hashlib.sha256(json.dumps({'rules':rules,'costs':plan['component_costs']},sort_keys=True,separators=(',',':')).encode()).hexdigest()
 for S,L,H,E in itertools.product(SLOWS,LOOKS,HURDLES,BUFFERS):
  fps=[bybtc[S,L,H],byeth[E]];assert tuple(sorted(fps)) not in seen
  old=next(c for c in mixed['configs'].values() if c['style']=='btc_reversal_eth_trend' and c['trend_exit_buffer_fraction']==E and c['reversal_lookback_days']==L and c['reversal_return_hurdle']==H)
  sp=json.loads((ROOT/old['spec']).read_text());name=f'mixedgate370_BG_ET_S{S}_L{L}_H{int(H*100):02d}_E{int(E*10000):03d}'
  sp.update(name=name,family='btc-gated-reversal-eth-trend-passive-perpetual-sleeves',logic=rules,validation_plan=rel(R/'plan.json'),sources=sources)
  sp['parameters'].update(style='btc_gated_reversal_eth_trend',BTC_trend_lookback_days=S,trend_exit_buffer_fraction=E,reversal_lookback_days=L,reversal_return_hurdle=H,BTC_lookback_days=L,BTC_return_hurdle=H,BTC_exit_buffer_fraction=0,ETH_lookback_days=28,ETH_return_hurdle=.02,ETH_exit_buffer_fraction=E,source_rules_and_costs_sha256=rulehash)
  sp['components']=[{'fingerprint':fp,'weight':1} for fp in fps];path=R/'specs'/(name+'.json');put(path,sp);fp=reg.fingerprint(sp);assert fp not in records or records[fp].get('result_available') is not True and records[fp]['status'] in ['blocked','abandoned']
  batch.append({'name':name,'role':'candidate','scope':'parent','asset':'COMBO','capital_usdt':20000,'BTC_fixed_entry_notional_usdt':2000,'ETH_fixed_entry_notional_usdt':2000,'BTC_trend_lookback_days':S,'reversal_lookback_days':L,'reversal_return_hurdle':H,'trend_exit_buffer_fraction':E,'style':'btc_gated_reversal_eth_trend','source_fingerprints':fps,'matched_ungated_control':old['name'],'spec':rel(path),'fingerprint':fp})
 assert len(batch)==len({x['fingerprint'] for x in batch})==81;put(R/'batch.json',batch);put(R/'spec.json',json.loads((ROOT/batch[0]['spec']).read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_RESERVED_81_BTC_GATE_ETH_TREND_PARENTS_ZERO_NEW_NATIVE',sha(R/'plan.json'),json.dumps(counts),flush=True)
if __name__=='__main__':main()
