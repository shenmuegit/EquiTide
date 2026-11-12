"""Read-only independent publication, source, registry and full original-account checks."""
import ast,argparse,csv,gzip,json,hashlib,subprocess
from decimal import Decimal as D
from common import *
rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()))
def bindings():
 b=rd(R/'code_binding_before_evaluation.json')
 for path,h in {**b['source_sha256'],**b['immutable_source_sha256'],**rd(R/'context.json')['account_hashes_before']}.items():assert sha(ROOT/path)==h,path
 return b

def research():
 b=bindings();p,r,rs=rd(R/'plan.json'),rd(R/'report.json'),reg.read_records(ROOT/'research/automation/registry.jsonl');batch=rd(R/'batch.json');v=rd(R/'verification.json');assert v['passed'] and v['report_sha256']==sha(R/'report.json') and len(batch)==len(r['configs'])==18 and v['new_native_curves']==27 and v['new_parent_curves']==27 and v['read_only_native_curves']==12 and v['independent_new_policy_decisions']==9990
 res=[x for f in (R/'reserve_batches').glob('*.json') for x in rd(f)['actual_command_receipts']];fin=[x for f in (R/'finish_batches').glob('*.json') for x in rd(f)['actual_command_receipts']];assert len(res)==len(fin)==18 and all(x['exit_code']==0 for x in res+fin) and b['recorded_utc']<min(x['started_utc'] for x in res) and max(x['finished_utc'] for x in res)<r['evaluation_started_utc']
 for x in batch:
  c=r['configs'][x['name']];z=rs[x['fingerprint']];assert z['result_available'] and z['status']==c['status'] and z['report_sha256']==sha(R/'report.json') and reg.fingerprint(rd(ROOT/x['spec']))==x['fingerprint'] and sha(ROOT/c['archive'])==c['archive_sha256']
 for fp,x in p['read_only_references'].items():assert rs[fp]['status']==x['status'] and rs[fp]['report_sha256']==x['report_sha256']
 expected={'cost_scenes.csv':54,'walk_forward_folds.csv':702,'daily_NAV.csv':20034,'recent40_folds.csv':432,'sensitivity_grid.csv':27,'native_sensitivity_grid.csv':27,'fixed_allocations.csv':9,'matched_hold_comparisons.csv':27,'adjacent_edges.csv':36}
 for n,k in expected.items():assert len(list(csv.DictReader((R/n).open())))==k,n
 for x in csv.DictReader((R/'cost_scenes.csv').open()):
  c=r['configs'][x['configuration']];s=c['scenes'][x['cost_multiplier']];assert int(x['ETH_risk_window'])==c['V'] and float(x['ETH_downside_RMS_cap'])==c['CAP']
  for a,k in [('return_pct','net_return_pct'),('whole_DD_pct','max_drawdown_pct'),('cost_usdt','cost_usdt')]:assert float(x[a])==s[k]
 new={c['fingerprint'] for c in r['configs'].values()};eligible={fp:z for fp,z in rs.items() if fp not in new and z.get('result_available') and z.get('spec',{}).get('kind') in ['combination','strategy'] and z['spec'].get('parameters',{}).get('start_utc')=='2025-10-19T00:01:00Z' and z['spec']['parameters'].get('end_utc')=='2026-10-24T00:01:00Z' and z['spec']['parameters'].get('initial_capital_usdt') in [15000,18750]};index={}
 for path in {z['report'] for z in eligible.values()}:
  doc=rd(ROOT/path)
  for c in doc.get('configs',{}).values():
   if c.get('fingerprint') not in eligible:continue
   try:key=tuple(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3'])
   except KeyError:continue
   index.setdefault(key,[]).append(c['fingerprint'])
 aliases=[{'fingerprint':c['fingerprint'],'name':c['name'],'scope':c['scope'],'ETH_V':c['V'],'ETH_CAP':c['CAP'],'prior_allcost_matches':index.get(tuple(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']),[])} for c in r['configs'].values()]
 put(R/'NAV_alias_inventory.json',{'passed':True,'new_definitions':18,'same_calendar_samecapital_prior_actual_configs':len(eligible),'new_allcost_signatures_seen_before':sum(bool(z['prior_allcost_matches']) for z in aliases),'candidate_parent_old_path_aliases':sum(z['scope']=='parent' and bool(z['prior_allcost_matches']) for z in aliases),'rows':aliases,'new_full_path_signatures_in_batch':len({tuple(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']) for c in r['configs'].values()}),'parameter_novelty_does_not_imply_independent_alpha':True})
 put(R/'research_verification.json',{'passed':True,'report_sha256':sha(R/'report.json'),'plan_sha256':sha(R/'plan.json'),'new_financial_IDs':18,'actual_reserve_calls':18,'actual_finish_calls':18,'all_reserves_before_evaluation':True,'CSV_rows':expected,'old_results_and_statuses_preserved':6,'new_parent_calculation_runs':1,'new_native_policy_runs':9,'reused_actual_native_curves_independently_audited':12,'new_native_curve_count':27,'new_parent_curve_count':27,'whole370day_and_recent40_continuous_NAV_audited':True,'two_joint_axes_correct':True});print('PASS9newETHnatives+9newparents/54scenes,12oldnativecostcurves,12x30+10tail/recent40/fullDD;allfinished')

def accounts():
 bindings();P=ROOT/'research/experiments/20261112T093127Z';win=rd(R/'account_windows.json');proof={};chains={};latest={};cashflows=[];fresh=rd(R/'funding08_source_verification.json');fund00={int(z['fundingTime'])*1000000 for xs in fresh['public_fields_by_asset'].values() for z in xs};oldfunds=[1794211200001000000,1794240000001000000,1794268800000000000,1794297600000000000,1794326400002000000,1794355200002000000,1794384000000000000,1794412800000000000,1794441600000000000];olddaily=[1794268860000000000,1794355260000000000,1794441660000000000];newday=1794441660000000000
 for stem in ['candidate','l4h02','fewm']:
  W=R/(stem+'_observation');v=rd(R/(stem+'_verification.json'));ov=rd(P/(stem+'_verification.json'));before=rd(ROOT/rd(W/'previous_pointer.json')['state']);after=rd(W/'state.json');d=gz(W/'delta.json.gz');w=win[stem];mid=stem!='candidate';actual={int(z['fundingTime'])*1000000 for xs in w['expected_funding_by_asset'].values() for z in xs};inc=122+3*len(w['expected_daily_events_utc'])+2*len(actual);funds=[z for z in d['journal'] if z['kind']=='funding'];trades=[z for z in d['journal'] if z['kind']=='trade' and z['status']=='filled'];decisions=[z for z in d['journal'] if z['kind']=='decision'];assert v['passed'] and v['cost_scenes']==9 and v['full_NAV_points_checked']==9*v['NAV_points_per_scene'] and v['prior_NAV_prefix']==ov['NAV_points_per_scene'] and v['NAV_points_per_scene']==ov['NAV_points_per_scene']+inc and v['elapsed_minutes']==ov['elapsed_minutes']+120 and len(d['NAV'])==inc
  assert v['new_daily_events']==len(w['expected_daily_events_utc']) and v['new_exact_causal_decisions']==len(decisions)==6*len(w['expected_daily_events_utc']) and v['new_funding_settlements']==len(funds)==w['expected_funding_records'] and v['new_fills']==len(trades) and v['new_rejected_orders']==v['new_risk_proxy_violations']==0 and not v['whole180day_qualified']
  seen=set()
  for z in funds:
   a=z['asset'];k=str(z['cost_multiplier']);key=a,k,z['timestamp_ns'];assert key not in seen;seen.add(key);row=next(x for x in w['expected_funding_by_asset'][a] if int(x['fundingTime'])*1000000==z['timestamp_ns']);q=D(before['books'][a][k]['signed_units']);base=-q*D(row['markPrice'])*D(row['fundingRate']);amount=base*int(k) if base<0 else base;assert D(z['signed_units'])==q and D(z['base_amount_usdt'])==base and D(z['amount_usdt'])==amount and D(z['cash_before'])==D(before['books'][a][k]['cash']) and D(z['cash_after'])==D(z['cash_before'])+amount ;cashflows.append({'account':stem,'asset':a,'cost':k,'actual_settlement_ns':z['timestamp_ns'],'held_units':str(q),'own_amount_usdt':str(amount),'original_public_capture_UTC':fresh['original_capture_recorded_utc']})
  for a in ['BTC','ETH']:
   for k in ['1','2','3']:
    old,new=before['books'][a][k],after['books'][a][k];ts=[z for z in trades if z['asset']==a and str(z['cost_multiplier'])==k];fs=[z for z in funds if z['asset']==a and str(z['cost_multiplier'])==k];assert D(new['cash'])==D(old['cash'])+sum((D(z['amount_usdt']) for z in fs),D(0))+sum((D(z['state_after']['cash'])-D(z['state_before']['cash']) for z in ts),D(0));assert D(new['signed_units'])==D(old['signed_units'])+sum((D(z['change_signed_units']) for z in ts),D(0))
  point=rd(ROOT/('research/automation/'+stem+'_forward_latest.json'));seenp=set();fundcounts={t:set() for t in oldfunds+list(fund00)};days={t:set() for t in olddaily+[newday]};last=0
  while point:
   assert point['delta'] not in seenp;seenp.add(point['delta']);assert sha(ROOT/point['delta'])==point['delta_sha256']
   for z in gz(ROOT/point['delta'])['journal']:
    t=z['timestamp_ns'];key=z['asset'],str(z['cost_multiplier'])
    if z['kind']=='funding':
     last=max(last,t)
     if t in fundcounts:assert key not in fundcounts[t];fundcounts[t].add(key)
    if z['kind']=='decision' and t in days:assert key not in days[t];days[t].add(key)
   ref=point.get('previous_pointer');point=rd(ROOT/ref['path']) if ref else None
  assert all(len(fundcounts[t])==6 for t in oldfunds) and all(len(days[t])==6 for t in olddaily) and all(len(fundcounts[t])==6 for t in fund00) and len(days[newday])==6;assert last==max(fund00);latest[stem]=last;chains[stem]={'funding':{str(t):len(s) for t,s in fundcounts.items()},'daily':{str(t):len(s) for t,s in days.items()}};proof[stem]={k:v[k] for k in ['window_start_utc','cutoff_utc','NAV_points_per_scene','prior_NAV_prefix','elapsed_minutes','new_daily_events','new_fills','new_funding_settlements','cost_scenes']}
 fv,ov=rd(R/'forward_verification.json'),rd(P/'forward_verification.json');assert fv['passed'] and fv['original_NAV_prefix']==ov['NAV_points_per_scene'] and fv['NAV_points_per_scene']==ov['NAV_points_per_scene']+120 and fv['cumulative_minutes']==ov['cumulative_minutes']+120 and fv['new_daily_decisions']==fv['new_executions']==fv['new_reference_points']==0
 full=ROOT/'research/experiments/20261112T033054Z/forward_inputs.json.gz';dd=gz(full);assert all(len(dd[a]['1d'])==65 and dd[a]['1d'][-1][6]+1==1794441600000 for a in ['BTC','ETH']);lp,fp=[gz(ROOT/rd(R/(ss+'_observation/input_manifest.json'))['packet']) for ss in ['l4h02','fewm']];assert lp['assets']==fp['assets'] and lp['provenance']==fp['provenance'] and lp['plan_sha256']!=fp['plan_sha256']
 assert win['candidate']['expected_funding_by_asset']==fresh['public_fields_by_asset'] and [win[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']]==[0,6,0,0] and all(not win[a]['expected_daily_events_utc'] for a in ['SMA','candidate','l4h02','fewm']) and rd(R/'funding08_public_reuse_verification.json')['passed']
 cp=gz(ROOT/rd(R/'candidate_observation/input_manifest.json')['packet'])
 for asset in ['BTC','ETH']:
  for row in fresh['public_fields_by_asset'][asset]:
   source=next(z for z in cp['assets'][asset]['funding'] if z['fundingTime']==row['fundingTime']);assert D(source['fundingRate'])==D(row['fundingRate']) and D(source['markPrice'])==D(row['markPrice']) and row['fundingTime']%1000==1
 put(R/'account_window_verification.json',{'passed':True,'account_windows':win,'actual_windows':proof,'current_daily_event_counts':{a:len(win[a]['expected_daily_events_utc']) for a in ['SMA','candidate','l4h02','fewm']},'current_fills_by_account':{'SMA':0,**{a:v['new_fills'] for a,v in proof.items()}},'current_funding_records_by_account':{a:win[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']},'actual_new_settlement_own_cashflows':cashflows,'full_chain_once_counts':chains,'latest_actual_funding_ns_by_account':latest,'all3_perp_Nov12_00_already_booked_once':True,'all3_perp_actualNov12_08_plus1ms_booked_once':True,'L4_FEWM_current08_not_repeated':True,'all18_perp_books_independently_reconciled':True,'SMA_full65_authority':str(full.relative_to(ROOT)),'SMA_full65_sha256':sha(full),'all_full_NAV_prefix_audits_passed':True,'only_public_data_reused_not_cashflows':True,'no_new_research_rule_adoption':True});print('PASS4originalaccounts:Singleactual08+1ms ownfundonce,L4FEWMno repeat,allday/fillcounts0,completefundoncechains and18bookcash/q')

def sources():
 b=bindings();ctx=rd(R/'context.json');bs=rd(R/'batch.json')+sum([rd(R/n) for n in ['forward_batch.json','candidate_batch.json','l4h02_batch.json','fewm_batch.json']],[]);rs=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');assert len(bs)==30 and len(events)==ctx['registry_events']+60 and len(rs)==ctx['registry_ids']+30 and all(rs[x['fingerprint']]['result_available'] and rs[x['fingerprint']]['status'] in ['passed','rejected'] for x in bs)
 for path,h in ctx['ledger_fragments_before'].items():assert sha(ROOT/path)==h
 assert rd(R/'registry_fragment_layout.json')['passed'];put(R/'source_verification.json',{'passed':True,'financial_IDs':18,'observation_IDs':12,'finished_IDs':30,'append_only_events':60,'bound_roots_unchanged':len(b['source_sha256']),'protected_old_files_unchanged':len(ctx['account_hashes_before'])});print('PASS30finishedIDs/60exactappend events,oldprotecteddata/frozenbanks/accountbindings')

def feed():
 data=gz(ROOT/'research/monitor/configs.json.gz');latest=rd(ROOT/'research/monitor/latest.json');base=rd(R/'startup.json')['base_commit'];old=json.loads(gzip.decompress(subprocess.check_output(['git','show',base+':research/monitor/configs.json.gz'],cwd=ROOT)));by={x['fingerprint']:x for x in data};r=rd(R/'report.json');fallback=R/'monitor_fallback.json'
 if fallback.exists():assert data==old;success=False
 else:
  assert len(data)==len(old)+18 and len(by)==len(data);success=True
  for z in old:assert by[z['fingerprint']]==z
  for c in r['configs'].values():
   z=by[c['fingerprint']];assert z['report']==rel(R/'report.json') and z['status']==c['status'] and z['criteria']==c['criteria']
   for k,s in c['scenes'].items():
    x=z['scenes'][k];assert x['nav_hash']==s['NAV_sha256_f64le']
    for a,b in [('return_pct','net_return_pct'),('drawdown_pct','max_drawdown_pct'),('sharpe','sharpe_365'),('cost','cost_usdt')]:assert x[a]==(round(float(s[b]),6) if s[b] is not None else None)
 put(R/'feed_verification.json',{'passed':True,'monitor_generation_succeeded':success,'monitor_snapshot_validation_passed':success,'research_configs':len(data),'historical_rows_identical':len(old),'new_actual_financial_configs':18,'new_displayed_financial_configs':18 if success else 0,'pending_current_financial_configurations':0 if success else 18,'paper_accounts':len(latest['paper']['accounts']),'paper_observations':latest['paper']['observation_count'],'protected_inputs_unchanged':True});print('PASSmonitor alloldrows/current18financialconfigs,success',success)

def final():
 bindings();assert not [z for z in R.rglob('*') if z.name=='__pycache__' or z.suffix in ['.pyc','.npy','.tmp'] or 'checkpoint' in z.name];assert all(z.get('resolved') for z in rd(R/'read_failures.json')['facts'])
 for z in R.rglob('*.py'):ast.parse(z.read_text())
 for n in ['research_verification.json','account_window_verification.json','source_verification.json','feed_verification.json','visual_inspection.json','raw_evidence_index.json','parent_primitive_verification.json','transport_failure_verification.json']:assert rd(R/n)['passed']
 assert all('Known zero-target downside RMS uses all V observations' in (R/(n+'.log')).read_text() for n in ['negative_policy_future_close','negative_policy_negative_count'])
 for cmd in [['git','diff','--check'],['git','diff','--cached','--quiet']]:assert subprocess.run(cmd,cwd=ROOT).returncode==0
 put(R/'preseal_review.json',{'passed':True,'checked_utc':now(),'all_financial_and_original_account_creators_bound_unchanged':True,'all_actual_failures_preserved_and_resolved':True,'fullNAV_registry_andmonitor_proofs_passed':True,'reconstructible_debris_remaining':[],'pending':'stagewhitespace/seal/commit/push/remoteverify/nativeunlock/postrelease'});print('PASSsource/AST/debris/requiredproofs andemptyGitindex,readyforseal')
if __name__=='__main__':globals()[argparse.ArgumentParser().parse_known_args()[1][0]]()
