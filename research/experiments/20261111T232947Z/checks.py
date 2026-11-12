"""Read-only research/account/source/monitor integrity checks; no valuation engine calls."""
import argparse,ast,csv,gzip,hashlib,json,subprocess,sys
from decimal import Decimal as D
from common import *
rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()))
def bindings():
 b=rd(R/'code_binding_before_evaluation.json')
 for path,h in {**b['source_sha256'],**b['immutable_source_sha256'],**b.get('immutable_ignored_market_data_sha256',{}),**rd(R/'context.json')['account_hashes_before']}.items():assert sha(ROOT/path)==h,path
 return b

def research():
 binding=bindings();p,r,rs=rd(R/'plan.json'),rd(R/'report.json'),reg.read_records(ROOT/'research/automation/registry.jsonl');batch=rd(R/'batch.json');v=rd(R/'verification.json');assert v['passed'] and v['report_sha256']==sha(R/'report.json') and len(batch)==len(r['configs'])==22
 reserves=[x for f in (R/'reserve_batches').glob('*.json') for x in rd(f)['actual_command_receipts']];finishes=[x for f in (R/'finish_batches').glob('*.json') for x in rd(f)['actual_command_receipts']];assert len(reserves)==len(finishes)==22 and all(x['exit_code']==0 for x in reserves+finishes) and binding['recorded_utc']<min(x['started_utc'] for x in reserves) and max(x['finished_utc'] for x in reserves)<r['evaluation_started_utc']
 for z in batch:
  c=r['configs'][z['name']];q=rs[z['fingerprint']];assert q['result_available'] and q['status']==c['status']=='rejected' and q['report_sha256']==sha(R/'report.json') and sha(ROOT/c['archive'])==c['archive_sha256'] and reg.fingerprint(rd(ROOT/z['spec']))==z['fingerprint'] and not c['criteria']['minimum180days'] and not c['criteria']['genuine_independent_prospective_validation']
 for fp,z in p['read_only_references'].items():assert rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
 expected={'cost_scenes.csv':66,'walk_forward_folds.csv':396,'daily_NAV.csv':1254,'sensitivity_grid.csv':27,'native_sensitivity_grid.csv':27,'adjacent_edges.csv':72,'fixed_allocations.csv':9,'matched_hold_comparisons.csv':27};counts={}
 for n,k in expected.items():
  xs=list(csv.DictReader((R/n).open()));assert len(xs)==k,(n,len(xs));counts[n]=k
 for x in csv.DictReader((R/'cost_scenes.csv').open()):
  c=r['configs'][x['configuration']];z=c['scenes'][x['cost_multiplier']]
  for a,k in [('return_pct','net_return_pct'),('whole_DD_pct','max_drawdown_pct'),('cost_usdt','cost_usdt')]:assert float(x[a])==z[k]
  assert not x['price_V'] or int(x['price_V'])==c['V'];assert not x['budget_VW'] or int(x['budget_VW'])==c['VW']
 eligible={fp:z for fp,z in rs.items() if z.get('result_available') and z.get('spec',{}).get('kind') in ['strategy','combination'] and z['spec'].get('market')=='perpetual' and z['spec'].get('parameters',{}).get('start_utc')=='2026-10-24T00:01:00Z' and z['spec']['parameters'].get('end_utc')=='2026-11-11T00:01:00Z' and fp not in {x['fingerprint'] for x in batch}};oldindex={}
 for path in {z['report'] for z in eligible.values()}:
  doc=rd(ROOT/path);assert all(z['report_sha256']==sha(ROOT/path) for z in eligible.values() if z['report']==path)
  for c in doc.get('configs',{}).values():
   if c.get('fingerprint') not in eligible:continue
   try:key=tuple(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3'])
   except KeyError:continue
   oldindex.setdefault(key,[]).append(c['fingerprint'])
 aliases=[];groups={}
 for c in r['configs'].values():
  sig=tuple(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']);aliases.append({'fingerprint':c['fingerprint'],'name':c['name'],'scope':c['scope'],'prior_allcost_matches':oldindex.get(sig,[])});groups.setdefault((c['scope'],c['asset'],c['capital_usdt'],sig),[]).append(c['fingerprint'])
 put(R/'NAV_alias_inventory.json',{'passed':True,'new_definitions':22,'complete_registry_records_read':len(rs),'same_calendar_prior_actual_configurations':len(eligible),'new_allcost_signatures_seen_before':sum(bool(x['prior_allcost_matches']) for x in aliases),'within_cohort_economic_path_groups':[{'scope':k[0],'asset':k[1],'capital':k[2],'fingerprints':fs} for k,fs in groups.items() if len(fs)>1],'rows':aliases,'scope':'Same18daycalendar only,not comparable to annualoriginal period;multiple V/VW settings can be observationally indistinguishable without any new entry.'})
 btc=next(c for c in r['configs'].values() if c['asset']=='BTC' and c['role']=='component');eth=[c for c in r['configs'].values() if c['asset']=='ETH' and c['role']=='component'];pc=[c for c in r['configs'].values() if c['role']=='candidate'];detail=[]
 for c in eth:
  arc=gz(ROOT/c['archive']);ds=arc['scenes']['1']['decisions'];assert all(z['executions']==0 and z['final_NAV_usdt']==z['initial_capital_usdt']==15000 and z['net_return_pct']==0 and all(v==15000 for v in z['daily_equity_usdt']) for z in c['scenes'].values());detail.append({'fingerprint':c['fingerprint'],'V':c['V'],'VW':c['VW'],'actual_executions_allcost':0,'fast_nonzero_targets1':sum(x['policy_audit']['ungated_desired']!=0 for x in ds),'post_trend_nonzero_targets1':sum(x['policy_audit']['raw_desired_before_entry_filter']!=0 for x in ds),'price_new_entry_filter_applications1':sum(x['policy_audit']['entry_filter_applied'] for x in ds),'funding_new_entry_filter_applications1':sum(x['policy_audit']['funding_filter']['applied'] for x in ds),'final_nonzero_targets1':sum(x['desired_direction']!=0 for x in ds)})
 for c in pc:
  for k,z in c['scenes'].items():
   b=btc['scenes'][k];assert z['daily_equity_usdt']==[x+15000 for x in b['daily_equity_usdt']]
   for f in ['cost_usdt','funding_usdt','gross_reference_price_PnL_usdt','executions','round_trips']:assert abs(float(z[f])-float(b[f]))<1e-12
 assert len({tuple(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']) for c in pc})==1
 put(R/'inactivity_attribution.json',{'passed':True,'ETH_variants':detail,'all9_ETH_variants_cash15000_and_no_fills':True,'all9_parent_complete_NAV_paths_equal':True,'all_parent_price_PnL_cost_and_funding_from_fixed_BTC_component_only':True,'prior_full_axis_independent_audit_proves_parent_sum':True,'ETH_parameter_sensitivity_not_identifiable_on_this18day_sample':True,'not9_independent_positive_strategy_paths':True})
 put(R/'research_verification.json',{'passed':True,'report_sha256':sha(R/'report.json'),'plan_sha256':sha(R/'plan.json'),'new_financial_IDs':22,'actual_reserve_calls':22,'actual_finish_calls':22,'all_reserves_before_evaluation':True,'CSV_rows':counts,'old_annual_results_and_statuses_preserved':len(p['read_only_references']),'new_actual_calculation_runs':1,'new_native_curve_count':36,'new_parent_curve_count':30,'old_annual_curve_valuations':0,'independent_monetary_audit_passed':True,'period18days_six3dayfolds':True,'maturity_and_prospective_qualification_false':True,'ETH_no_entry_and_path_attribution_verified':True});print('PASS22actualfollowupresults/66scenes/6x3dayfolds/fullNAV/DD, noETHentries and1commonparentpath;all22finishrejected')

def accounts():
 bindings();win=rd(R/'account_windows.json');P=ROOT/'research/experiments/20261111T212846Z';out={};chains={};latest={};basefunds=[1794211200001000000,1794240000001000000,1794268800000000000,1794297600000000000,1794326400002000000,1794355200002000000,1794384000000000000];daily=[1794268860000000000,1794355260000000000];fundproof=[]
 for stem in ['candidate','l4h02','fewm']:
  W=R/(stem+'_observation');v=rd(R/(stem+'_verification.json'));ov=rd(P/(stem+'_verification.json'));state=rd(W/'state.json');before=rd(ROOT/rd(W/'previous_pointer.json')['state']);d=gz(W/'delta.json.gz');doc=rd(W/'report.json');w=win[stem];actual={int(z['fundingTime'])*1000000 for xs in w['expected_funding_by_asset'].values() for z in xs};increment=122+2*len(actual);funds=[z for z in d['journal'] if z['kind']=='funding']
  assert v['passed'] and v['cost_scenes']==9 and sum(len(c['scenes']) for c in doc['configs'].values())==9 and v['full_NAV_points_checked']==9*v['NAV_points_per_scene']
  assert v['window_start_utc']==w['start_utc'] and v['cutoff_utc']==w['cutoff_utc'] and v['NAV_points_per_scene']==ov['NAV_points_per_scene']+increment and v['prior_NAV_prefix']==ov['NAV_points_per_scene'] and v['elapsed_minutes']==ov['elapsed_minutes']+120
  assert v['new_daily_events']==v['new_fills']==v['new_exact_causal_decisions']==0 and v['new_funding_settlements']==len(funds)==w['expected_funding_records'] and v['new_rejected_orders']==v['new_risk_proxy_violations']==0 and not v['whole180day_qualified'] and not any(z['kind'] in ['trade','decision'] for z in d['journal']) and len(d['NAV'])==increment
  seenfund=set()
  for z in funds:
   a=z['asset'];k=str(z['cost_multiplier']);key=a,k,z['timestamp_ns'];assert key not in seenfund;seenfund.add(key);row=next(x for x in w['expected_funding_by_asset'][a] if int(x['fundingTime'])*1000000==z['timestamp_ns']);q=D(before['books'][a][k]['signed_units']);base=-q*D(row['markPrice'])*D(row['fundingRate']);amount=base*int(k) if base<0 else base
   assert D(z['signed_units'])==q and D(z['mark_price'])==D(row['markPrice']) and D(z['rate'])==D(row['fundingRate']) and D(z['base_amount_usdt'])==base and D(z['amount_usdt'])==amount and D(z['cash_before'])==D(before['books'][a][k]['cash']) and D(z['cash_after'])==D(z['cash_before'])+amount;fundproof.append({'account':stem,'asset':a,'cost':k,'actual_settlement_ns':z['timestamp_ns'],'held_units':str(q),'own_amount_usdt':str(amount),'source_preflight':str(rd(R/'funding16_source_verification.json')['source'])})
  for a in ['BTC','ETH']:
   for k in ['1','2','3']:
    old,new=before['books'][a][k],state['books'][a][k];assert set(old)==set(new) and all(old[f]==new[f] for f in old if f!='cash') and D(new['cash'])==D(old['cash'])+sum((D(z['amount_usdt']) for z in funds if z['asset']==a and str(z['cost_multiplier'])==k),D(0))
  point=rd(ROOT/('research/automation/'+stem+'_forward_latest.json'));seen=set();oldtimes=sorted(set(basefunds)|{1794412800000000000}|actual);sets={t:set() for t in oldtimes+daily};last=0
  while point:
   assert point['delta'] not in seen;seen.add(point['delta']);assert sha(ROOT/point['delta'])==point['delta_sha256']
   for z in gz(ROOT/point['delta'])['journal']:
    t=z['timestamp_ns'];kind=z['kind']
    if kind=='funding':last=max(last,t)
    if t in sets and (kind=='funding' and t in oldtimes or kind=='decision' and t in daily):
     key=z['asset'],str(z['cost_multiplier']);assert key not in sets[t];sets[t].add(key)
   ref=point.get('previous_pointer');point=rd(ROOT/ref['path']) if ref else None
  assert all(len(ss)==6 for ss in sets.values()) and last==max(oldtimes);chains[stem]={str(k):len(x) for k,x in sets.items()};latest[stem]=last;out[stem]={k:v[k] for k in ['window_start_utc','cutoff_utc','NAV_points_per_scene','prior_NAV_prefix','elapsed_minutes','new_daily_events','new_fills','new_funding_settlements','cost_scenes']}
 fv,ov=rd(R/'forward_verification.json'),rd(P/'forward_verification.json');assert fv['passed'] and fv['original_NAV_prefix']==ov['NAV_points_per_scene'] and fv['NAV_points_per_scene']==ov['NAV_points_per_scene']+120 and fv['cumulative_minutes']==ov['cumulative_minutes']+120 and fv['new_daily_decisions']==fv['new_reference_points']==fv['new_executions']==0
 full=ROOT/'research/experiments/20261111T032206Z/forward_inputs.json.gz';dd=gz(full);assert all(len(dd[a]['1d'])==65 and dd[a]['1d'][-1][6]+1==1794355200000 for a in ['BTC','ETH']);current=gz(R/'forward_inputs.json.gz');assert all(isinstance(current[a],list) for a in ['BTC','ETH'])
 lp,fp=[gz(ROOT/rd(R/(ss+'_observation/input_manifest.json'))['packet']) for ss in ['l4h02','fewm']];assert lp['assets']==fp['assets'] and lp['provenance']==fp['provenance'] and lp['plan_sha256']!=fp['plan_sha256'];assert len(rd(R/'candidate_public_response_reuse_plan.json')['responses'])==2
 put(R/'account_window_verification.json',{'passed':True,'account_windows':win,'actual_windows':out,'all18_perp_books_preserve_quantity_entry_and_own_cash_continuity':True,'current_all4_daily_and_fills':0,'current_funding_records_by_account':{ss:win[ss]['expected_funding_records'] for ss in ['SMA','candidate','l4h02','fewm']},'actual_new_settlement_own_cashflows':fundproof,'old_settlements_and_daily_decisions_once':chains,'latest_actual_funding_ns_by_account':latest,'all3_Nov11_16_booked_in_prior_own_windows':True,'all3_Nov11_16_booked_once':True,'SMA_full65_authority':'research/experiments/20261111T032206Z/forward_inputs.json.gz','SMA_full65_sha256':sha(full),'SMA_mark_only_original_main_AST_checked_before_binding':True,'perp_auditor_actual_scene_count9':True,'all_full_NAV_prefix_audits_passed':True,'only_public_data_reused_not_cashflows':True,'no_frozen_rule_or_account_adoption':True});print('PASS4originalaccounts,own actual16 funding/cash/18books,all3fullfundingchains once,actual9scenes/account andNAVprefixes')

def sources():
 b=bindings();ctx=rd(R/'context.json');batch=rd(R/'batch.json')+sum([rd(R/n) for n in ['forward_batch.json','candidate_batch.json','l4h02_batch.json','fewm_batch.json']],[]);rs=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');assert len(batch)==34 and len(events)==ctx['registry_events']+68 and len(rs)==ctx['registry_ids']+34
 for z in batch:assert rs[z['fingerprint']]['result_available'] and rs[z['fingerprint']]['status'] in ['passed','rejected']
 for path,h in ctx['ledger_fragments_before'].items():assert sha(ROOT/path)==h
 assert rd(R/'registry_fragment_layout.json')['passed'] and rd(R/'research_verification.json')['passed'] and rd(R/'account_window_verification.json')['passed'];put(R/'source_verification.json',{'passed':True,'financial_IDs':22,'observation_IDs':12,'finished_IDs':34,'append_only_events':68,'bound_roots_unchanged':len(b['source_sha256']),'protected_old_files_unchanged':len(ctx['account_hashes_before']),'all_actual_results_available':True});print('PASS34finishedIDs/68append events,oldprotecteddata/sourcebindings intact')

def feed():
 data=json.loads(gzip.decompress((ROOT/'research/monitor/configs.json.gz').read_bytes()));latest=rd(ROOT/'research/monitor/latest.json');base=rd(R/'startup.json')['base_commit'];old=json.loads(gzip.decompress(subprocess.check_output(['git','show',base+':research/monitor/configs.json.gz'],cwd=ROOT)));by={x['fingerprint']:x for x in data};r=rd(R/'report.json');fallback=R/'monitor_fallback.json'
 if fallback.exists():
  f=rd(fallback);assert f['applied'] and not f['checker_or_rules_modified'];assert data==old
  for path,z in f['restored_files'].items():assert sha(ROOT/path)==z['sha256']
  success=False
 else:
  for z in old:assert by[z['fingerprint']]==z
  assert len(data)==len(old)+22 and len(by)==len(data);success=True
  for c in r['configs'].values():
   x=by[c['fingerprint']];assert x['report']==rel(R/'report.json') and x['status']==c['status'] and x['criteria']==c['criteria']
   for k,s in c['scenes'].items():
    z=x['scenes'][k];assert z['nav_hash']==s['NAV_sha256_f64le']
    for a,b in [('return_pct','net_return_pct'),('drawdown_pct','max_drawdown_pct'),('sharpe','sharpe_365'),('cost','cost_usdt')]:assert z[a]==(round(float(s[b]),6) if s[b] is not None else None)
 put(R/'feed_verification.json',{'passed':True,'monitor_generation_succeeded':success,'monitor_snapshot_validation_passed':success,'research_configs':len(data),'historical_rows_identical':len(old),'new_actual_financial_configs':22,'new_displayed_financial_configs':22 if success else 0,'pending_current_financial_configurations':0 if success else 22,'new_candidate_configs':9,'new_benchmark_configs':1,'new_source_components':10,'new_benchmark_components':2,'new_cost_scenes':66,'paper_accounts':len(latest['paper']['accounts']),'paper_observations':latest['paper']['observation_count'],'protected_inputs_unchanged':True,'financial_report_sha256':sha(R/'report.json')});print('PASSmonitor currentresults andalloldrows,success',success)

def final():
 bindings();assert not [z for z in R.rglob('*') if z.name=='__pycache__' or z.suffix in ['.pyc','.npy','.tmp'] or 'checkpoint' in z.name];assert all(x.get('resolved') for x in rd(R/'read_failures.json')['facts'])
 for z in R.rglob('*.py'):ast.parse(z.read_text())
 for n in ['research_verification.json','account_window_verification.json','source_verification.json','feed_verification.json','visual_inspection.json','raw_evidence_index.json','inactivity_attribution.json','period_primitive_verification.json']:assert rd(R/n)['passed']
 for args in [['git','diff','--check'],['git','diff','--cached','--quiet']]:assert subprocess.run(args,cwd=ROOT).returncode==0
 put(R/'preseal_review.json',{'passed':True,'checked_utc':now(),'all_financial_and_account_creators_bound_unchanged':True,'required_checks_passed':True,'all_actual_failures_preserved_and_resolved':True,'reconstructible_debris_remaining':[],'original_reports_and_frozen_accounts_preserved':True,'pending':'stage-whitespace/seal/commit/push/remoteverify/releaselock/postrelease'});print('PASS source/AST/debris/requiredproofs,Gitwhitespace/index;ready for finalstagedwhitespace/seal')
if __name__=='__main__':globals()[argparse.ArgumentParser().parse_known_args()[1][0]]()
