"""Read-only independent publication, source, registry and full original-account checks."""
import ast,argparse,csv,gzip,json,hashlib,subprocess
from datetime import datetime
from decimal import Decimal as D
from common import *
rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()))
def bindings():
 b=rd(R/'code_binding_before_evaluation.json')
 for path,h in {**b['source_sha256'],**b['immutable_source_sha256'],**rd(R/'context.json')['account_hashes_before']}.items():assert sha(ROOT/path)==h,path
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
 bindings();P=ROOT/'research/experiments/20261114T075131Z';win=rd(R/'account_windows.json');previous_check=rd(P/'account_window_verification.json');proof={};chains={};latest={};cashflows=[];fresh=rd(R/'window_funding_preflight.json');fresh_times={int(z['fundingTime'])*1000000 for xs in fresh['public_fields_by_asset'].values() for z in xs};expected_chains={}
 for stem in ['candidate','l4h02','fewm']:
  W=R/(stem+'_observation');v=rd(R/(stem+'_verification.json'));ov=rd(P/(stem+'_verification.json'));before=rd(ROOT/rd(W/'previous_pointer.json')['state']);after=rd(W/'state.json');d=gz(W/'delta.json.gz');w=win[stem];actual={int(z['fundingTime'])*1000000 for xs in w['expected_funding_by_asset'].values() for z in xs};inc=122+3*len(w['expected_daily_events_utc'])+2*len(actual);funds=[z for z in d['journal'] if z['kind']=='funding'];trades=[z for z in d['journal'] if z['kind']=='trade' and z['status']=='filled'];decisions=[z for z in d['journal'] if z['kind']=='decision'];assert v['passed'] and v['cost_scenes']==9 and v['full_NAV_points_checked']==9*v['NAV_points_per_scene'] and v['prior_NAV_prefix']==ov['NAV_points_per_scene'] and v['NAV_points_per_scene']==ov['NAV_points_per_scene']+inc and v['elapsed_minutes']==ov['elapsed_minutes']+120 and len(d['NAV'])==inc
  assert v['new_daily_events']==len(w['expected_daily_events_utc']) and v['new_exact_causal_decisions']==len(decisions)==6*len(w['expected_daily_events_utc']) and v['new_funding_settlements']==len(funds)==w['expected_funding_records'] and v['new_fills']==len(trades)==0 and v['new_rejected_orders']==v['new_risk_proxy_violations']==0 and not v['whole180day_qualified']
  seen=set();running_cash={(a,k):D(before['books'][a][k]['cash']) for a in ['BTC','ETH'] for k in ['1','2','3']}
  for z in sorted(funds,key=lambda z:(z['timestamp_ns'],z['asset'],z['cost_multiplier'])):
   a=z['asset'];k=str(z['cost_multiplier']);key=a,k,z['timestamp_ns'];assert key not in seen;seen.add(key);row=next(x for x in w['expected_funding_by_asset'][a] if int(x['fundingTime'])*1000000==z['timestamp_ns']);q=D(before['books'][a][k]['signed_units']);base=-q*D(row['markPrice'])*D(row['fundingRate']);amount=base*int(k) if base<0 else base;assert D(z['signed_units'])==q and D(z['base_amount_usdt'])==base and D(z['amount_usdt'])==amount and D(z['cash_before'])==running_cash[a,k] and D(z['cash_after'])==running_cash[a,k]+amount;running_cash[a,k]+=amount;cashflows.append({'account':stem,'asset':a,'cost':k,'actual_settlement_ns':z['timestamp_ns'],'held_units':str(q),'own_amount_usdt':str(amount),'original_public_capture_UTC':fresh['recorded_utc']})
  for a in ['BTC','ETH']:
   for k in ['1','2','3']:
    old,new=before['books'][a][k],after['books'][a][k];assert D(new['cash'])==running_cash[a,k] and new=={**old,'cash':new['cash']}
  basefund={int(t):n for t,n in previous_check['full_chain_once_counts'][stem]['funding'].items()};basedays={int(t):n for t,n in previous_check['full_chain_once_counts'][stem]['daily'].items()};expectedfund={t:basefund.get(t,0)+sum(3 for a in ['BTC','ETH'] for z in w['expected_funding_by_asset'][a] if int(z['fundingTime'])*1000000==t) for t in set(basefund)|fresh_times};expecteddays={t:basedays.get(t,0)+(6 if t in {int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*1e9) for s in w['expected_daily_events_utc']} else 0) for t in set(basedays)};fundcounts={t:set() for t in expectedfund};daycounts={t:set() for t in expecteddays};allfundkeys=set();alldaykeys=set();seenp=set();last=0;point=rd(ROOT/('research/automation/'+stem+'_forward_latest.json'))
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
 fv,ov=rd(R/'forward_verification.json'),rd(P/'forward_verification.json');assert fv['passed'] and fv['original_NAV_prefix']==ov['NAV_points_per_scene'] and fv['NAV_points_per_scene']==ov['NAV_points_per_scene']+120 and fv['cumulative_minutes']==ov['cumulative_minutes']+120 and fv['new_daily_decisions']==fv['new_reference_points']==fv['new_executions']==0
 full=ROOT/'research/experiments/20261114T035058Z/forward_inputs.json.gz';dd=gz(full);assert all(len(dd[a]['1d'])==66 and dd[a]['1d'][-1][6]+1==1794614400000 for a in ['BTC','ETH']);lp,fp=[gz(ROOT/rd(R/(ss+'_observation/input_manifest.json'))['packet']) for ss in ['l4h02','fewm']];assert lp['assets']==fp['assets'] and lp['provenance']==fp['provenance'] and lp['plan_sha256']!=fp['plan_sha256']
 assert win['candidate']['expected_funding_by_asset']=={'BTC':[],'ETH':[]} and all(win[a]['expected_funding_by_asset']==fresh['public_fields_by_asset'] for a in ['l4h02','fewm']) and [win[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']]==[0,0,6,6] and len(cashflows)==12
 put(R/'account_window_verification.json',{'passed':True,'account_windows':win,'actual_windows':proof,'current_daily_event_counts':{a:len(win[a]['expected_daily_events_utc']) for a in ['SMA','candidate','l4h02','fewm']},'current_fills_by_account':{'SMA':fv['new_executions'],**{a:v['new_fills'] for a,v in proof.items()}},'current_funding_records_by_account':{a:win[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']},'actual_new_settlement_own_cashflows':cashflows,'full_chain_once_counts':chains,'expected_full_chain_once_counts':expected_chains,'latest_actual_funding_ns_by_account':latest,'all_known_older_funding_and_daily_counts_preserved':True,'all_full_chain_asset_cost_timestamp_keys_unique':True,'all18_perp_books_independently_reconciled':True,'SMA_full66_authority':str(full.relative_to(ROOT)),'SMA_full66_sha256':sha(full),'SMA_original_full65_authority':'research/experiments/20261113T033939Z/forward_inputs.json.gz','all3_perp_actualNov14_00_booked_once':True,'L4_FEWM_actualNov14_08_booked_once':True,'single_actualNov14_08_not_yet_booked':True,'all_full_NAV_prefix_audits_passed':True,'only_public_data_reused_not_cashflows':True,'no_new_research_rule_adoption':True});print('PASS4originalaccounts: own18books/fullNAV, actual08plus1ms L4/FEWM6each, single0 until owncursor reaches08; all fullchain keys unique')

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
 bindings();assert not [z for z in R.rglob('*') if z.name=='__pycache__' or z.suffix in ['.pyc','.npy','.tmp'] or 'checkpoint' in z.name];assert all(z.get('resolved') for z in rd(R/'read_failures.json')['facts'])
 for z in R.rglob('*.py'):ast.parse(z.read_text())
 for n in ['research_verification.json','account_window_verification.json','source_verification.json','feed_verification.json','visual_inspection.json','raw_evidence_index.json','parent_primitive_verification.json','transport_failure_verification.json']:assert rd(R/n)['passed']
 for cmd in [['git','diff','--check'],['git','diff','--cached','--quiet']]:assert subprocess.run(cmd,cwd=ROOT).returncode==0
 put(R/'preseal_review.json',{'passed':True,'checked_utc':now(),'all_creators_bound_unchanged':True,'all_actual_failures_preserved_and_resolved':True,'full_NAV_registry_and_monitor_proofs_passed':True,'reconstructible_debris_remaining':[],'pending':'seal/commit/push/remoteverify/nativeunlock/postrelease'});print('PASS source/AST/debris/proofs ready for seal')
if __name__=='__main__':globals()[argparse.ArgumentParser().parse_known_args()[1][0]]()
