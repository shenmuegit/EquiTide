"""Read-only independent publication, source, registry and full original-account checks."""
import ast,argparse,csv,gzip,json,hashlib,subprocess
from datetime import datetime
from decimal import Decimal as D
from common import *
rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()))
def bindings():
 b=rd(R/'code_binding_before_evaluation.json')
 for path,h in {**b['source_sha256'],**b['immutable_source_sha256'],**rd(R/'context.json')['account_hashes_before']}.items():assert sha(ROOT/path)==h,path
 if (R/'candidate_transport_recovery_binding.json').exists():
  recovery=rd(R/'candidate_transport_recovery_binding.json');assert recovery['passed'] and recovery['first_finished_research_report_sha256']==sha(R/'report.json')
  for path,h in {**recovery['source_sha256'],**recovery['original_frozen_kernel_SHA256'],**recovery['prior_failed_raw_files']}.items():assert sha(ROOT/path)==h,path
 if (R/'audit_repair_binding.json').exists():
  repair=rd(R/'audit_repair_binding.json');assert repair['passed'] and repair['completed_report_sha256']==sha(R/'report.json')
  for path,h in repair['supplemental_readonly_source_sha256'].items():assert sha(ROOT/path)==h
 return b

def research():
 b=bindings();p,r,rs=rd(R/'plan.json'),rd(R/'report.json'),reg.read_records(ROOT/'research/automation/registry.jsonl');v=rd(R/'verification.json');batch=rd(R/'batch.json');assert v['passed'] and v['report_sha256']==sha(R/'report.json') and len(batch)==len(r['configs'])==6 and (v['new_native_curves'],v['new_parent_curves'],v['independent_new_policy_decisions'])==(6,12,2346)
 res=[x for f in (R/'reserve_batches').glob('*.json') for x in rd(f)['actual_command_receipts']];fin=[x for f in (R/'finish_batches').glob('*.json') for x in rd(f)['actual_command_receipts']];assert len(res)==len(fin)==6 and all(x['exit_code']==0 for x in res+fin)
 events=reg.read_events(ROOT/'research/automation/registry.jsonl')
 for c in r['configs'].values():
  rec=rs[c['fingerprint']];assert rec['result_available'] and rec['status']==c['status'] and rec['report_sha256']==sha(R/'report.json');sp=rd(ROOT/c['spec']);assert reg.fingerprint(sp)==c['fingerprint'];assert sha(ROOT/c['archive'])==c['archive_sha256'];reserves=[x for x in events if x['fingerprint']==c['fingerprint'] and x['status']=='reserved'];assert len(reserves)==1 and max(x['recorded_at_utc'] for x in reserves)<r['evaluation_started_utc'];assert c['sensitivity']['dimension_count']==(0 if c['role']=='benchmark' else 1 if c['scope']=='native' else 2)
  assert c['status']==('passed' if all(c['criteria'].values()) else 'rejected')
  for s in c['scenes'].values():assert len(s['folds'])==14 and len(s['recent40']['folds'])==8 and len(s['extension21']['folds'])==4 and len(s['daily_equity_usdt'])==392
 assert rd(R/'export_verification.json')['passed']
 put(R/'research_verification.json',{'passed':True,'financial_IDs':6,'new_native_models':2,'passive_parents':4,'cost_curves':18,'joint_parameter_axes':2,'all42new_and_readonly_scenes_and_folds_audited':True,'all_new_reserve_before_actual_calculation':True,'read_only_native_curves_audited':15,'read_only_parent_curves_audited':9,'completed_model_evaluation_runs':1,'all_actual_results_finished':True});print('PASS6newconfigs/18newscenes plus8readonly/24scenes,allpre-reserved/finished,twoaxes/fullNAV/WF/recent/costproofs')

def accounts():
 import copy
 bindings();P=ROOT/'research/experiments/20261117T082021Z';win=rd(R/'account_windows.json');previous_check=rd(P/'account_window_verification.json');proof={};chains={};latest={};cashflows=[];tradeproof=[];fresh=rd(R/'window_funding_preflight.json');fresh_times={int(z['fundingTime'])*1000000 for xs in fresh['public_fields_by_asset'].values() for z in xs};expected_chains={};daily_context={}
 for stem in ['candidate','l4h02','fewm']:
  W=R/(stem+'_observation');v=rd(R/(stem+'_verification.json'));ov=rd(P/(stem+'_verification.json'));before=rd(ROOT/rd(W/'previous_pointer.json')['state']);after=rd(W/'state.json');d=gz(W/'delta.json.gz');w=win[stem];actual={int(z['fundingTime'])*1000000 for xs in w['expected_funding_by_asset'].values() for z in xs};newdays={int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*1e9) for s in w['expected_daily_events_utc']};inc=122+3*len(newdays)+2*len(actual);funds=[z for z in d['journal'] if z['kind']=='funding'];trades=[z for z in d['journal'] if z['kind']=='trade' and z['status']=='filled'];decisions=[z for z in d['journal'] if z['kind']=='decision'];assert v['passed'] and v['cost_scenes']==9 and v['full_NAV_points_checked']==9*v['NAV_points_per_scene'] and v['prior_NAV_prefix']==ov['NAV_points_per_scene'] and v['NAV_points_per_scene']==ov['NAV_points_per_scene']+inc and v['elapsed_minutes']==ov['elapsed_minutes']+120 and len(d['NAV'])==inc
  assert v['new_daily_events']==len(newdays) and v['new_exact_causal_decisions']==len(decisions)==6*len(newdays) and v['new_funding_settlements']==len(funds)==w['expected_funding_records'] and v['new_fills']==len(trades) and 0<=len(trades)<=12*len(newdays) and v['new_rejected_orders']==v['new_risk_proxy_violations']==0 and not v['whole180day_qualified']
  own=copy.deepcopy(before['books']);seen=set()
  for z in d['journal']:
   a=z['asset'];k=str(z['cost_multiplier']);book=own[a][k]
   if z['kind']=='funding':
    key=a,k,z['timestamp_ns'];assert key not in seen;seen.add(key);row=next(x for x in w['expected_funding_by_asset'][a] if int(x['fundingTime'])*1000000==z['timestamp_ns']);q=D(book['signed_units']);base=-q*D(row['markPrice'])*D(row['fundingRate']);amount=base*int(k) if base<0 else base;assert D(z['signed_units'])==q and D(z['base_amount_usdt'])==base and D(z['amount_usdt'])==amount and D(z['cash_before'])==D(book['cash']) and D(z['cash_after'])==D(book['cash'])+amount
    if amount:book['cash']=str(D(book['cash'])+amount)
    cashflows.append({'account':stem,'asset':a,'cost':k,'actual_settlement_ns':z['timestamp_ns'],'held_units':str(q),'own_amount_usdt':str(amount),'current_window_public_query_capture_UTC':fresh['recorded_utc'],'first_actual_Nov17_00_public_capture_UTC':rd(R/'funding00_nov17_preflight.json')['recorded_utc']})
   elif z['kind']=='decision':assert z['timestamp_ns'] in newdays and any(x['asset']==a and x['cost']==k and x['timestamp_ns']==z['timestamp_ns'] and x['wanted']==z['wanted'] for x in v['independent_decisions'])
   elif z['kind']=='trade':
    assert z['status']=='filled' and z['timestamp_ns'] in newdays and all(D(z['state_before'][key])==D(val) for key,val in book.items());cash,q,entry=[D(book[x]) for x in ['cash','signed_units','entry_price']];fee=D(z['quantity'])*D(z['execution'])*D('.0005')*int(k);assert D(z['cost_parts']['fee'])==fee
    if z['opening']:assert q==0 and D(z['state_after']['cash'])==cash-fee and D(z['state_after']['signed_units'])==D(z['change_signed_units']) and D(z['state_after']['entry_price'])==D(z['execution'])
    else:assert D(z['change_signed_units'])==-q and D(z['state_after']['cash'])==cash+q*(D(z['execution'])-entry)-fee and D(z['state_after']['signed_units'])==0
    own[a][k]=copy.deepcopy(z['state_after']);tradeproof.append({'account':stem,'asset':a,'cost':k,'timestamp_ns':z['timestamp_ns'],'opening':z['opening'],'fee_usdt':str(fee),'own_state_before':z['state_before'],'own_state_after':z['state_after']})
   else:raise AssertionError(z['kind'])
  assert own==after['books']
  for a in ['BTC','ETH']:
   old=before['context'][a];new=after['context'][a];assert len(new['daily'])==len(old['daily'])+len(newdays) and new['daily'][:len(old['daily'])]==old['daily']
   if newdays:assert old['partial']['count']<1440 and new['daily'][-1]['day']==old['partial']['day'] and new['daily'][-1]['count']==1440
  daily_context[stem]={'before':{a:len(before['context'][a]['daily']) for a in ['BTC','ETH']},'after':{a:len(after['context'][a]['daily']) for a in ['BTC','ETH']},'prior_daily_prefix_exact':True,'completed_day_volume_close_independently_audited':True}
  basefund={int(t):n for t,n in previous_check['full_chain_once_counts'][stem]['funding'].items()};basedays={int(t):n for t,n in previous_check['full_chain_once_counts'][stem]['daily'].items()};expectedfund={t:basefund.get(t,0)+sum(3 for a in ['BTC','ETH'] for z in w['expected_funding_by_asset'][a] if int(z['fundingTime'])*1000000==t) for t in set(basefund)|fresh_times};expecteddays={t:basedays.get(t,0)+(6 if t in newdays else 0) for t in set(basedays)|newdays};fundcounts={t:set() for t in expectedfund};daycounts={t:set() for t in expecteddays};allfundkeys=set();alldaykeys=set();seenp=set();last=0;point=rd(ROOT/('research/automation/'+stem+'_forward_latest.json'))
  while point:
   assert point['delta'] not in seenp;seenp.add(point['delta']);assert sha(ROOT/point['delta'])==point['delta_sha256']
   for z in gz(ROOT/point['delta'])['journal']:
    t=z['timestamp_ns'];key=z['asset'],str(z['cost_multiplier']);unique=t,*key
    if z['kind']=='funding':
     assert unique not in allfundkeys;allfundkeys.add(unique);last=max(last,t)
     if t in fundcounts:fundcounts[t].add(key)
    if z['kind']=='decision':
     assert unique not in alldaykeys;alldaykeys.add(unique)
     if t in daycounts:daycounts[t].add(key)
   ref=point.get('previous_pointer');point=rd(ROOT/ref['path']) if ref else None
  assert {t:len(s) for t,s in fundcounts.items()}==expectedfund and {t:len(s) for t,s in daycounts.items()}==expecteddays;assert last==max({previous_check['latest_actual_funding_ns_by_account'][stem]}|actual);latest[stem]=last;chains[stem]={'funding':{str(t):len(s) for t,s in sorted(fundcounts.items())},'daily':{str(t):len(s) for t,s in sorted(daycounts.items())}};expected_chains[stem]={'funding':{str(t):n for t,n in sorted(expectedfund.items())},'daily':{str(t):n for t,n in sorted(expecteddays.items())}};proof[stem]={k:v[k] for k in ['window_start_utc','cutoff_utc','NAV_points_per_scene','prior_NAV_prefix','elapsed_minutes','new_daily_events','new_fills','new_funding_settlements','cost_scenes']}
 fv,ov=rd(R/'forward_verification.json'),rd(P/'forward_verification.json');assert fv['passed'] and fv['original_NAV_prefix']==ov['NAV_points_per_scene'] and fv['NAV_points_per_scene']==ov['NAV_points_per_scene']+120 and fv['cumulative_minutes']==ov['cumulative_minutes']+120 and fv['new_daily_decisions']==0 and fv['new_reference_points']==0 and fv['new_executions']==0
 full=ROOT/'research/experiments/20261114T035058Z/forward_inputs.json.gz';dd=gz(full);assert all(len(dd[a]['1d'])==66 and dd[a]['1d'][-1][6]+1==1794614400000 for a in ['BTC','ETH']);lp,fp=[gz(ROOT/rd(R/(ss+'_observation/input_manifest.json'))['packet']) for ss in ['l4h02','fewm']];assert lp['assets']==fp['assets'] and lp['provenance']==fp['provenance'] and lp['plan_sha256']!=fp['plan_sha256']
 full67=ROOT/'research/experiments/20261115T075947Z/forward_inputs.json.gz';d67=gz(full67);assert all(len(d67[a]['1d'])==67 and d67[a]['1d'][:66]==dd[a]['1d'] and d67[a]['1d'][-1][6]+1==1794700800000 for a in ['BTC','ETH'])
 full68=ROOT/rd(P/'next_research_state.json')['UTC_midnight_handoff']['SMA_full68_authority'];d68=gz(full68);assert all(len(d68[a]['1d'])==68 and d68[a]['1d'][:67]==d67[a]['1d'] and d68[a]['1d'][-1][6]+1==1794787200000 for a in ['BTC','ETH'])
 full69=ROOT/rd(R/'SMA_background_authorities.json')['authorities']['69']['path'];d69=gz(full69);assert all(len(d69[a]['1d'])==69 and d69[a]['1d'][:68]==d68[a]['1d'] and d69[a]['1d'][-1][6]+1==1794873600000 for a in ['BTC','ETH'])
 assert {a:win[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']}=={'SMA':0,'candidate':0,'l4h02':0,'fewm':0} and len(cashflows)==0;assert all(z['actual_settlement_ns']==1794873600000000000 and z['account'] in ['l4h02','fewm'] for z in cashflows)
 assert {a:len(win[a]['expected_daily_events_utc']) for a in ['SMA','candidate','l4h02','fewm']}=={'SMA':0,'candidate':0,'l4h02':0,'fewm':0};assert all(chains[a]['funding'].get('1794873600000000000',0)==6 and chains[a]['daily'].get('1794873660000000000',0)==6 for a in ['candidate','l4h02','fewm'])
 put(R/'account_window_verification.json',{'passed':True,'account_windows':win,'actual_windows':proof,'current_daily_event_counts':{a:len(win[a]['expected_daily_events_utc']) for a in ['SMA','candidate','l4h02','fewm']},'current_fills_by_account':{'SMA':fv['new_executions'],**{a:v['new_fills'] for a,v in proof.items()}},'current_funding_records_by_account':{a:win[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']},'actual_new_settlement_own_cashflows':cashflows,'actual_own_original_kernel_trades':tradeproof,'daily_context_reconciliation':daily_context,'full_chain_once_counts':chains,'expected_full_chain_once_counts':expected_chains,'latest_actual_funding_ns_by_account':latest,'all_known_older_funding_and_daily_counts_preserved':True,'all_full_chain_asset_cost_timestamp_keys_unique':True,'all18_perp_books_independently_reconciled':True,'SMA_full66_authority':str(full.relative_to(ROOT)),'SMA_full66_sha256':sha(full),'SMA_full67_authority':rel(full67),'SMA_full67_sha256':sha(full67),'SMA_full68_authority':rel(full68),'SMA_full68_sha256':sha(full68),'SMA_full69_authority':rel(full69),'SMA_full69_sha256':sha(full69),'SMA_original_daily_decisions_per_asset':0,'SMA_original_full65_authority':'research/experiments/20261113T033939Z/forward_inputs.json.gz','all3_perp_actualNov14_00_booked_once':True,'L4_FEWM_actualNov14_08_booked_once':True,'single_actualNov14_08_not_yet_booked':False,'all3_perp_actualNov14_08_booked_once':True,'all3_perp_actualNov14_16_booked_once':True,'single_actualNov14_16_not_yet_booked':False,'L4_FEWM_actualNov15_00_booked_once':True,'single_actualNov15_00_not_yet_booked':False,'all3_perp_actualNov15_00_booked_once':True,'L4_FEWM_actualNov15_08_booked_once':True,'single_actualNov15_08_not_yet_booked':False,'all3_perp_actualNov15_08_booked_once':True,'all_full_NAV_prefix_audits_passed':True,'only_public_data_reused_not_cashflows':True,'no_new_research_rule_adoption':True});print('PASS4originalaccounts: own18books/fullNAV/funding/trades,currentActualFundingSplit0/0/0/0,daily0/0/0/0,SMA69SpotContextAnd120NAV,actualfrozenKernelFillsAudited,Nov17all3perpsmidnightonce;allchainkeysunique')

def sources():
 b=bindings();ctx=rd(R/'context.json');bs=rd(R/'batch.json')+sum([rd(R/n) for n in ['forward_batch.json','candidate_batch.json','l4h02_batch.json','fewm_batch.json']],[]);rs=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');assert len(bs)==18 and len(events)==ctx['registry_events']+36 and len(rs)==ctx['registry_ids']+18 and all(rs[x['fingerprint']]['result_available'] and rs[x['fingerprint']]['status'] in ['passed','rejected'] for x in bs)
 for path,h in ctx['ledger_fragments_before'].items():assert sha(ROOT/path)==h
 assert rd(R/'registry_fragment_layout.json')['passed'];put(R/'source_verification.json',{'passed':True,'financial_IDs':6,'observation_IDs':12,'finished_IDs':18,'append_only_events':36,'bound_roots_unchanged':len(b['source_sha256']),'protected_old_files_unchanged':len(ctx['account_hashes_before'])});print('PASS18finishedIDs/36exactappend events,oldprotecteddata/frozenbanks/accountbindings')

def feed():
 data=gz(ROOT/'research/monitor/configs.json.gz');latest=rd(ROOT/'research/monitor/latest.json');base=rd(R/'startup.json')['base_commit'];old=json.loads(gzip.decompress(subprocess.check_output(['git','show',base+':research/monitor/configs.json.gz'],cwd=ROOT)));by={x['fingerprint']:x for x in data};r=rd(R/'report.json');fallback=R/'monitor_fallback.json'
 if fallback.exists():assert data==old;success=False
 else:
  assert len(data)==len(old)+6 and len(by)==len(data);success=True
  for z in old:assert by[z['fingerprint']]==z
  for c in r['configs'].values():
   z=by[c['fingerprint']];assert z['report']==rel(R/'report.json') and z['status']==c['status'] and z['criteria']==c['criteria']
   for k,s in c['scenes'].items():
    x=z['scenes'][k];assert x['nav_hash']==s['NAV_sha256_f64le']
    for a,b in [('return_pct','net_return_pct'),('drawdown_pct','max_drawdown_pct'),('sharpe','sharpe_365'),('cost','cost_usdt')]:assert x[a]==(round(float(s[b]),6) if s[b] is not None else None)
 put(R/'feed_verification.json',{'passed':True,'monitor_generation_succeeded':success,'monitor_snapshot_validation_passed':success,'research_configs':len(data),'historical_rows_identical':len(old),'new_actual_financial_configs':6,'new_displayed_financial_configs':6 if success else 0,'pending_current_financial_configurations':0 if success else 6,'paper_accounts':len(latest['paper']['accounts']),'paper_observations':latest['paper']['observation_count'],'protected_inputs_unchanged':True});print('PASSmonitor alloldrows/current6financialconfigs,success',success)

def final():
 bindings();assert all('/'+R.name+'/forward_raw/' in z['raw_gzip_path'] for z in rd(R/'forward_report.json')['provenance']);assert rd(R/'historical_path_alias_verification.json')['passed'];assert not [z for z in R.rglob('*') if z.name=='__pycache__' or z.suffix in ['.pyc','.npy','.tmp'] or 'checkpoint' in z.name];assert all(z.get('resolved') for z in rd(R/'read_failures.json')['facts'])
 for z in R.rglob('*.py'):
  tree=ast.parse(z.read_text());assert not [n for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id in ['ROOT','R','P']],str(z)
 for name in ['research_verification.json','account_window_verification.json','source_verification.json','feed_verification.json','visual_inspection.json','raw_evidence_index.json','parent_primitive_verification.json','transport_failure_verification.json']:assert rd(R/name)['passed']
 for cmd in [['git','diff','--check'],['git','diff','--cached','--quiet']]:assert subprocess.run(cmd,cwd=ROOT).returncode==0
 put(R/'preseal_review.json',{'passed':True,'checked_utc':now(),'all_creators_bound_unchanged':True,'all_actual_failures_preserved_and_resolved':True,'full_NAV_registry_and_monitor_proofs_passed':True,'previous_blocked_round_noresult_records_preserved':True,'reconstructible_debris_remaining':[],'pending':'seal/commit/push/remoteverify/nativeunlock/postrelease'});print('PASS realfinancial/accountresults,allAST/pathjoins/debris/monitor readyforseal')
if __name__=='__main__':globals()[argparse.ArgumentParser().parse_known_args()[1][0]]()
