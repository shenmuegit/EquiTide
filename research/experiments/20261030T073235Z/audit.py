"""Independent recorded-order/funding replay and structured-clock ownership audit."""
import ast,gzip,hashlib,json,math
from decimal import Decimal as D
import numpy as np
import engine
import audit_native
from run import ROOT,R,reg,sha,put,module,grid_configs
base=module(R/'audit_helpers.py','recorded_ledger_independent_audit')
near,metrics,verify_axis,verify_recent,replay=base.near,base.metrics,base.verify_axis,base.verify_recent,base.recover_from_recorded_events

def main():
 report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');assert len(batch)==66 and report['summary']['cost_scenarios']==198 and report['frozen_plan_sha256']==sha(R/'plan.json') and json.loads((R/'engine_change_verification.json').read_text())['passed'];markets={a:engine.load_market(a,fs) for a,fs in plan['data']['assets'].items()}
 for m in markets.values():verify_axis(m)
 dt=np.dtype([('t','<i8'),('k','<i8')]);structured={}
 for a,m in markets.items():
  q=np.empty(len(m['ts']),dtype=dt);q['t']=m['ts'];q['k']=m['codes'];structured[a]=q
 union=np.union1d(structured['BTC'],structured['ETH']);packed=(union['t']-markets['BTC']['start_ns'])*16+union['k'];assert hashlib.sha256(packed.astype('<i8').tobytes()).hexdigest()==report['parent_axis']['union_axis_sha256'];projections={}
 for a,old in structured.items():
  j=np.searchsorted(old,union,side='right')-1;assert (j>=0).all() and ((old[j]['t']<union['t'])|((old[j]['t']==union['t'])&(old[j]['k']<=union['k']))).all() and np.array_equal(j[np.searchsorted(union,old)],np.arange(len(old)));projections[a]=j
 pre=np.flatnonzero(union['k']==5);assert len(pre)==370;days=np.asarray([0,*pre[1:],len(union)-1]);folds=np.asarray([0,*pre[np.arange(30,370,30)],len(union)-1]);common={'daily_indices':days,'ts':union['t']};vectors={};ss={};counters={'source_recorded_trades_checked':0,'source_recorded_funding_checked':0}
 for fp,x in plan['component_sources'].items():
  assert sha(ROOT/x['report'])==x['report_sha256'] and sha(ROOT/x['spec'])==x['spec_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256'] and records[fp]['status']==x['original_status'] and records[fp]['report_sha256']==x['report_sha256'];arc=json.loads(gzip.decompress((ROOT/x['archive']).read_bytes()));assert reg.fingerprint(arc['spec'])==fp and arc['spec']['parameters']['initial_capital_usdt']==x['capital_usdt'] and arc['spec']['parameters']['fixed_entry_notional_usdt']==x['fixed_entry_notional_usdt']
  for k,z in arc['scenes'].items():
   v=replay(markets[x['asset']],z,counters,int(k));assert hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==x['NAV_sha256_by_cost'][k];vectors[fp,k]=v[projections[x['asset']]];ss[fp,k]=z['summary']
 assert len(vectors)==42 and counters==plan['recorded_source_events'];grid=grid_configs(report['configs']);assert len(grid)==27;checks=recentchecks=scenes=0
 native_vectors,native_counts=audit_native.verify(report,plan,markets,events,records)
 for (fp,k),v in native_vectors.items():vectors[fp,k]=v[projections['ETH']];ss[fp,k]=next(c['scenes'][k] for c in report['configs'].values() if c['fingerprint']==fp)
 for row in [x for x in batch if x['scope']=='parent']:
  c=report['configs'][row['name']];sp=json.loads((ROOT/row['spec']).read_text());arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));p=sp['parameters'];fps=row['source_fingerprints'];ww=row['raw_component_multipliers'];a=row['fast_ETH_bank_units'];assert sha(ROOT/c['archive'])==c['archive_sha256'] and arc['spec']==sp and reg.fingerprint(sp)==row['fingerprint']==arc['fingerprint'];assert ww==[1,1,1]==p['raw_component_multipliers']==[x['weight'] for x in sp['components']] and p['source_component_parameters']==[records[f]['spec']['parameters'] for f in fps] and p['component_capitals_usdt']==[5000,15000*a,15000*(1-a)] and sum(p['component_capitals_usdt'])==20000
  rv=[e for e in events if e['fingerprint']==row['fingerprint'] and e['status']=='reserved'];assert len(rv)==1 and rv[0]['recorded_at_utc']<report['evaluation_started_utc']
  for k,z in arc['scenes'].items():
   v=np.zeros(len(union))
   for fp,w in zip(fps,ww):v+=w*vectors[fp,k]
   s=z['summary'];parts=[ss[fp,k] for fp in fps];assert s==c['scenes'][k] and v[0]==20000 and s['initial_capital_usdt']==20000 and s['NAV_points']==len(v)==545013 and hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==s['NAV_sha256_f64le'] and z['source_fingerprints']==fps and z['source_full_NAV_sha256']==[x['NAV_sha256_f64le'] for x in parts];daily=v[days].tolist();assert daily==s['daily_equity_usdt'];metrics(v,daily,370,s);checks+=1
   for j,(lo,hi) in enumerate(zip(folds,folds[1:])):
    a0,b0=j*30,min((j+1)*30,370);f=s['folds'][j];assert f['duration_days']==b0-a0 and f['start_utc']==engine.stamp(int(union['t'][lo])) and f['end_exclusive_utc']==engine.stamp(int(union['t'][hi]));metrics(v[lo:hi+1],daily[a0:b0+1],b0-a0,f);checks+=1
   assert len(s['folds'])==13 and abs(math.prod(1+f['net_return_pct']/100 for f in s['folds'])-v[-1]/20000)<1e-12;verify_recent(v,common,s);recentchecks+=9
   money=['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','gross_reference_price_PnL_usdt'];counts=['executions','round_trips','rejected_orders','cash_or_units_violations','funding_settlements','nonzero_funding_settlements']
   for field in money:near(s[field],sum(w*x[field] for w,x in zip(ww,parts)))
   for field in counts:assert s[field]==sum(x[field] for x in parts)
   for field,val in s['cost_parts_usdt'].items():near(val,sum(w*x['cost_parts_usdt'][field] for w,x in zip(ww,parts)))
   near(s['gross_reference_price_PnL_usdt']+s['funding_usdt']-s['cost_usdt'],v[-1]-20000);near(s['cost_pct_initial'],s['cost_usdt']/200);assert all(D(x['terminal_units'])==0 for x in parts) and D(s['terminal_units'])==0
   expected={'independent_sleeve_violations':sum(x['margin']['violations'] for x in parts),'minimum_individual_sleeve_cushion_usdt':min((w*x['margin']['minimum_equity_minus_maintenance_usdt'] for w,x in zip(ww,parts) if x['margin']['minimum_equity_minus_maintenance_usdt'] is not None),default=None),'no_cross_margin_netting':True};assert s['margin']==expected;scenes+=1
  if row['role']=='candidate':base.qualification(c,grid)
  else:assert c['status']=='rejected' and c['criteria']=={'reference_or_fixed_BTC_execution_component_only':False}
 assert scenes==90 and checks==1260 and recentchecks==810 and all(sha(ROOT/p)==h for p,h in json.loads((R/'context.json').read_text())['account_hashes_before'].items())
 proof={'passed':True,'actual_financial_configs':66,'actual_candidates':27,'actual_benchmarks':39,'new_native_components':36,'new_passive_parents':30,'source_native_components_reused_readonly':14,'source_native_cost_NAVs_recovered':42,**counters,**native_counts,'cost_scenes_audited':198,'parent_cost_scenes_audited':90,'full_NAV_points_per_scene':len(union),'full_NAV_points_audited':len(union)*198,'independent_overall_and_fold_metric_checks':checks+native_counts['native_metric_checks'],'independent_recent40_and_fold_metric_checks':recentchecks+native_counts['native_recent_metric_checks'],'structured_clock_raw_units_capital20000_verified':True,'strict_new_eachcost_and_neighborhood_gates_verified':True,'source_models_not_rerun':True,'protected_inputs_unchanged':True,'native_new_bank_execution_verified':True,'no_real_capacity_or_future_profit_proof':True,'report_sha256':sha(R/'report.json')};put(R/'verification.json',proof);print(json.dumps(proof),flush=True)
if __name__=='__main__':main()
