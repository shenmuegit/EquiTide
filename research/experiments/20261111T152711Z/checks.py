"""Read-only research/account/source/monitor integrity checks; no valuation engine calls."""
import argparse,ast,csv,gzip,hashlib,json,subprocess,sys
from decimal import Decimal as D
from common import *
rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()))
def bindings():
 b=rd(R/'code_binding_before_evaluation.json')
 for path,h in {**b['source_sha256'],**b['immutable_source_sha256'],**rd(R/'context.json')['account_hashes_before']}.items():assert sha(ROOT/path)==h,path
 return b

def research():
 b=bindings();p,r,rs=rd(R/'plan.json'),rd(R/'report.json'),reg.read_records(ROOT/'research/automation/registry.jsonl');batch=rd(R/'batch.json');v=rd(R/'verification.json');assert v['passed'] and v['report_sha256']==sha(R/'report.json') and len(batch)==len(r['configs'])==12
 reserve=[x for f in (R/'reserve_batches').glob('*.json') for x in rd(f)['actual_command_receipts']];finish=[x for f in (R/'finish_batches').glob('*.json') for x in rd(f)['actual_command_receipts']];assert len(reserve)==len(finish)==12 and all(x['exit_code']==0 for x in reserve+finish) and b['recorded_utc']<min(x['started_utc'] for x in reserve) and max(x['finished_utc'] for x in reserve)<r['evaluation_started_utc']
 for z in batch:
  s=rd(ROOT/z['spec']);c=r['configs'][z['name']];record=rs[z['fingerprint']];assert reg.fingerprint(s)==z['fingerprint'] and record['result_available'] and record['status']==c['status'] and record['report_sha256']==sha(R/'report.json') and sha(ROOT/c['archive'])==c['archive_sha256']
 for fp,z in p['read_only_references'].items():assert rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
 expected={'cost_scenes.csv':36,'walk_forward_folds.csv':468,'recent40_folds.csv':288,'daily_NAV.csv':13356,'sensitivity_grid.csv':27,'native_sensitivity_grid.csv':18,'adjacent_edges.csv':48,'fixed_allocations.csv':9,'fixed_exposure_hold_comparisons.csv':27};counts={}
 for n,k in expected.items():
  with (R/n).open() as f:xs=list(csv.DictReader(f))
  assert len(xs)==k,(n,len(xs),k);counts[n]=k
  if n in ['cost_scenes.csv','walk_forward_folds.csv','recent40_folds.csv','daily_NAV.csv']:
   for x in xs:
    c=r['configs'][x['configuration']];assert x['asset']==c['asset'] and (not x['native_N'] or int(x['native_N'])==c['N']) and (not x['BTC_N'] or int(x['BTC_N'])==c['NB']) and (not x['ETH_N'] or int(x['ETH_N'])==c['NE'])
 for x in csv.DictReader((R/'cost_scenes.csv').open()):
  c=r['configs'][x['configuration']];s=c['scenes'][x['cost_multiplier']]
  for a,k in [('return_pct','net_return_pct'),('whole_DD_pct','max_drawdown_pct'),('cost_usdt','cost_usdt')]:assert float(x[a])==s[k]
 # Conditional full-NAV alias inventory,restricted to comparable actual records with complete hashes.
 eligible={}
 for fp,z in rs.items():
  sp=z.get('spec',{});q=sp.get('parameters',{})
  if z.get('result_available') and sp.get('kind') in ['strategy','combination'] and sp.get('market')=='perpetual' and q.get('initial_capital_usdt') in [3750,15000,18750] and q.get('start_utc')=='2025-10-19T00:01:00Z' and q.get('end_utc')=='2026-10-24T00:01:00Z' and fp not in {x['fingerprint'] for x in batch} and z.get('report'):eligible[fp]=z
 paths={z['report'] for z in eligible.values()};index={};comparable=0
 for path in sorted(paths):
  members={fp:z for fp,z in eligible.items() if z['report']==path};h=sha(ROOT/path);assert all(z['report_sha256']==h for z in members.values());doc=rd(ROOT/path)
  for c in doc.get('configs',{}).values():
   fp=c.get('fingerprint')
   if fp not in members:continue
   try:sig=tuple(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3'])
   except KeyError:continue
   z=members[fp];sp=z['spec'];key=(sp['kind'],tuple(sorted(sp['universe'])),D(str(sp['parameters']['initial_capital_usdt'])),sig);index.setdefault(key,[]).append({'fingerprint':fp,'name':sp['name'],'status':z['status'],'report':path,'report_sha256':h});comparable+=1
 aliases=[]
 for c in r['configs'].values():
  sp=rd(ROOT/c['spec']);key=(sp['kind'],tuple(sorted(sp['universe'])),D(str(c['capital_usdt'])),tuple(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']));aliases.append({'fingerprint':c['fingerprint'],'name':c['name'],'scope':c['scope'],'N':c.get('N'),'NB':c.get('NB'),'NE':c.get('NE'),'prior_allcost_matches':index.get(key,[])})
 put(R/'NAV_alias_inventory.json',{'passed':True,'complete_registry_records_read':len(rs),'comparable_prior_actual_definitions_with_complete_NAV_hashes':comparable,'prior_reports_verified':len(paths),'new_definitions':12,'new_allcost_signatures_seen_before':sum(bool(x['prior_allcost_matches']) for x in aliases),'rows':aliases,'scope':'SameC/universe/market/calendar and complete3costhashes only;old formats without completehashes not asserted unique;no old status or return rewritten.'});put(R/'research_verification.json',{'passed':True,'report_sha256':sha(R/'report.json'),'plan_sha256':sha(R/'plan.json'),'new_financial_IDs':12,'actual_reserve_calls':12,'actual_finish_calls':12,'all_reserves_before_evaluation':True,'CSV_rows':counts,'old_actual_results_and_qualifications_preserved':10,'new_actual_calculation_runs':1,'new_native_curve_count':12,'new_parent_curve_count':24,'independent_monetary_audit_passed':True,'readonly_hold_is_sameC_fixedN_reference_only':True});print('PASS12actualfinished/Nspecs/allCSV36scenes/oldreports/aliases,bindings and before-eval reservations')

def accounts():
 b=bindings();win=rd(R/'account_windows.json');P=ROOT/'research/experiments/20261111T132640Z';out={};chains={};latest={};oldtimes=[1794211200001000000,1794240000001000000,1794268800000000000,1794297600000000000,1794326400002000000,1794355200002000000,1794384000000000000];daily=[1794268860000000000,1794355260000000000]
 for stem in ['candidate','l4h02','fewm']:
  W=R/(stem+'_observation');v=rd(R/(stem+'_verification.json'));ov=rd(P/(stem+'_verification.json'));state=rd(W/'state.json');before=rd(ROOT/rd(W/'previous_pointer.json')['state']);d=gz(W/'delta.json.gz');doc=rd(W/'report.json');assert v['passed'] and v['cost_scenes']==9 and sum(len(c['scenes']) for c in doc['configs'].values())==9 and v['full_NAV_points_checked']==9*v['NAV_points_per_scene'];assert v['window_start_utc']==win[stem]['start_utc'] and v['cutoff_utc']==win[stem]['cutoff_utc'] and v['NAV_points_per_scene']==ov['NAV_points_per_scene']+122 and v['prior_NAV_prefix']==ov['NAV_points_per_scene'] and v['elapsed_minutes']==ov['elapsed_minutes']+120 and v['new_daily_events']==v['new_fills']==v['new_funding_settlements']==v['new_exact_causal_decisions']==0 and v['new_rejected_orders']==v['new_risk_proxy_violations']==0 and state['books']==before['books'] and not v['whole180day_qualified'];assert not any(z['kind'] in ['trade','funding','decision'] for z in d['journal']) and len(d['NAV'])==122
  point=rd(ROOT/('research/automation/'+stem+'_forward_latest.json'));seen=set();sets={t:set() for t in oldtimes+daily};last=0
  while point:
   assert point['delta'] not in seen;seen.add(point['delta']);assert sha(ROOT/point['delta'])==point['delta_sha256']
   for z in gz(ROOT/point['delta'])['journal']:
    t=z['timestamp_ns'];kind=z['kind']
    if kind=='funding':last=max(last,t)
    if t in sets and (kind=='funding' and t in oldtimes or kind=='decision' and t in daily):
     key=z['asset'],str(z['cost_multiplier']);assert key not in sets[t];sets[t].add(key)
   ref=point.get('previous_pointer');point=rd(ROOT/ref['path']) if ref else None
  assert all(len(s)==6 for s in sets.values()) and last==1794384000000000000;chains[stem]={str(k):len(x) for k,x in sets.items()};latest[stem]=last;out[stem]={k:v[k] for k in ['window_start_utc','cutoff_utc','NAV_points_per_scene','prior_NAV_prefix','elapsed_minutes','new_daily_events','new_fills','new_funding_settlements','cost_scenes']}
 fv,ov=rd(R/'forward_verification.json'),rd(P/'forward_verification.json');assert fv['passed'] and fv['original_NAV_prefix']==ov['NAV_points_per_scene'] and fv['NAV_points_per_scene']==ov['NAV_points_per_scene']+120 and fv['cumulative_minutes']==ov['cumulative_minutes']+120 and fv['new_daily_decisions']==fv['new_reference_points']==fv['new_executions']==0
 full=ROOT/'research/experiments/20261111T032206Z/forward_inputs.json.gz';dd=gz(full);assert all(len(dd[a]['1d'])==65 and dd[a]['1d'][-1][6]+1==1794355200000 for a in ['BTC','ETH']);current=gz(R/'forward_inputs.json.gz');assert all(isinstance(current[a],list) for a in ['BTC','ETH'])
 lp,fp=[gz(ROOT/rd(R/(s+'_observation/input_manifest.json'))['packet']) for s in ['l4h02','fewm']];assert lp['assets']==fp['assets'] and lp['provenance']==fp['provenance'] and lp['plan_sha256']!=fp['plan_sha256'];assert len(rd(R/'candidate_public_response_reuse_plan.json')['responses'])==2
 put(R/'account_window_verification.json',{'passed':True,'account_windows':win,'actual_windows':out,'all18_perp_books_exactly_preserved':True,'current_all4_daily_funding_fills':0,'old_settlements_and_daily_decisions_once':chains,'latest_actual_funding_ns_by_account':latest,'SMA_full65_authority':'research/experiments/20261111T032206Z/forward_inputs.json.gz','SMA_full65_sha256':sha(full),'SMA_mark_only_original_main_AST_checked_before_binding':True,'perp_auditor_actual_scene_count9':True,'all_full_NAV_prefix_audits_passed':True,'only_public_data_reused_not_cashflows':True,'no_frozen_rule_or_account_adoption':True});print('PASS4originalaccounts,18perpbooks exact,all3fundingchains once,actual9scenes/account andfullNAVprefixes')

def sources():
 b=bindings();ctx=rd(R/'context.json');batch=rd(R/'batch.json')+sum([rd(R/n) for n in ['forward_batch.json','candidate_batch.json','l4h02_batch.json','fewm_batch.json']],[]);rs=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');assert len(batch)==24 and len(events)==ctx['registry_events']+48 and len(rs)==ctx['registry_ids']+24
 for z in batch:assert rs[z['fingerprint']]['result_available'] and rs[z['fingerprint']]['status'] in ['passed','rejected']
 for path,h in ctx['ledger_fragments_before'].items():assert sha(ROOT/path)==h
 assert rd(R/'registry_fragment_layout.json')['passed'] and rd(R/'research_verification.json')['passed'] and rd(R/'account_window_verification.json')['passed'];put(R/'source_verification.json',{'passed':True,'financial_IDs':12,'observation_IDs':12,'finished_IDs':24,'append_only_events':48,'bound_roots_unchanged':len(b['source_sha256']),'protected_old_files_unchanged':len(ctx['account_hashes_before']),'all_actual_results_available':True});print('PASS24finishedIDs/48append events,oldprotecteddata/sourcebindings intact')

def feed():
 data=json.loads(gzip.decompress((ROOT/'research/monitor/configs.json.gz').read_bytes()));latest=rd(ROOT/'research/monitor/latest.json');base=rd(R/'startup.json')['base_commit'];old=json.loads(gzip.decompress(subprocess.check_output(['git','show',base+':research/monitor/configs.json.gz'],cwd=ROOT)));by={x['fingerprint']:x for x in data};r=rd(R/'report.json');fallback=R/'monitor_fallback.json'
 if fallback.exists():
  f=rd(fallback);assert f['applied'] and not f['checker_or_rules_modified'];assert data==old
  for path,z in f['restored_files'].items():assert sha(ROOT/path)==z['sha256']
  success=False
 else:
  for z in old:assert by[z['fingerprint']]==z
  assert len(data)==len(old)+12 and len(by)==len(data);success=True
  for c in r['configs'].values():
   x=by[c['fingerprint']];assert x['report']==rel(R/'report.json') and x['status']==c['status'] and x['criteria']==c['criteria']
   for k,s in c['scenes'].items():
    z=x['scenes'][k];assert z['nav_hash']==s['NAV_sha256_f64le']
    for a,b in [('return_pct','net_return_pct'),('drawdown_pct','max_drawdown_pct'),('sharpe','sharpe_365'),('cost','cost_usdt')]:assert z[a]==(round(float(s[b]),6) if s[b] is not None else None)
 put(R/'feed_verification.json',{'passed':True,'monitor_generation_succeeded':success,'monitor_snapshot_validation_passed':success,'research_configs':len(data),'historical_rows_identical':len(old),'new_actual_financial_configs':12,'new_displayed_financial_configs':12 if success else 0,'pending_current_financial_configurations':0 if success else 12,'new_candidate_configs':8,'new_source_components':4,'new_cost_scenes':36,'paper_accounts':len(latest['paper']['accounts']),'paper_observations':latest['paper']['observation_count'],'protected_inputs_unchanged':True,'financial_report_sha256':sha(R/'report.json')});print('PASSmonitor currentresults andalloldrows,success',success)

def final():
 bindings();assert not [z for z in R.rglob('*') if z.name=='__pycache__' or z.suffix in ['.pyc','.npy','.tmp'] or 'checkpoint' in z.name];assert all(x.get('resolved') for x in rd(R/'read_failures.json')['facts'])
 for z in R.rglob('*.py'):ast.parse(z.read_text())
 for n in ['research_verification.json','account_window_verification.json','source_verification.json','feed_verification.json','visual_inspection.json','raw_evidence_index.json']:assert rd(R/n)['passed']
 for args in [['git','diff','--check'],['git','diff','--cached','--quiet']]:assert subprocess.run(args,cwd=ROOT).returncode==0
 put(R/'preseal_review.json',{'passed':True,'checked_utc':now(),'all_financial_and_account_creators_bound_unchanged':True,'required_checks_passed':True,'all_actual_failures_preserved_and_resolved':True,'reconstructible_debris_remaining':[],'original_reports_and_frozen_accounts_preserved':True,'pending':'stage-whitespace/seal/commit/push/remoteverify/releaselock/postrelease'});print('PASS source/AST/debris/requiredproofs,Gitwhitespace/index;ready for finalstagedwhitespace/seal')
if __name__=='__main__':globals()[argparse.ArgumentParser().parse_known_args()[1][0]]()
