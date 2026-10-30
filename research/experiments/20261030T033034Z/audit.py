"""Independent recorded-order/funding replay and structured-clock ownership audit."""
import ast,gzip,hashlib,json,math
from decimal import Decimal as D
import numpy as np
import engine
from run import ROOT,R,reg,sha,put,module,grid_configs
from audit_native import verify as verify_native
base=module(R/'audit_helpers.py','recorded_ledger_independent_audit')
near,metrics,verify_axis,verify_recent,replay=base.near,base.metrics,base.verify_axis,base.verify_recent,base.recover_from_recorded_events

def main():
 report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');assert len(batch)==20 and report['summary']['cost_scenarios']==60 and report['frozen_plan_sha256']==sha(R/'plan.json') and sha(R/'engine.py')==plan['new_engine_sha256'] and json.loads((R/'engine_change_verification.json').read_text())['passed'];markets={a:engine.load_market(a,fs) for a,fs in plan['data']['assets'].items()};assert sha(R/'btc_engine.py')==plan['new_BTC_engine_sha256']
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
 assert len(vectors)==15 and counters==plan['recorded_source_events'];grid={}
 grid=grid_configs(report['configs']);assert len(grid)==18 and sum(c['scope']=='native' for c in grid.values())==9
 checks=recentchecks=scenes=0
 newvectors,native_proof=verify_native(report,plan,markets,events,records)
 for (fp,k),v in newvectors.items():
  vectors[fp,k]=v[projections['ETH']];ss[fp,k]=next(c for c in report['configs'].values() if c['fingerprint']==fp)['scenes'][k]
 for row in batch:
  if row['scope']!='parent':continue
  c=report['configs'][row['name']];sp=json.loads((ROOT/row['spec']).read_text());arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));assert sha(ROOT/c['archive'])==c['archive_sha256'] and arc['spec']==sp and arc['fingerprint']==row['fingerprint']==reg.fingerprint(sp);p=sp['parameters'];w=row['BTC_capital_fraction'];ww=row['raw_component_multipliers'];fps=row['source_fingerprints'];capital=20000
  assert p['raw_component_multipliers']==ww==[x['weight'] for x in sp['components']] and [x['fingerprint'] for x in sp['components']]==fps and p['initial_capital_usdt']==capital and p['owned_component_capitals_usdt']==[20000*w,20000*(1-w)]
  srcparams=[records[fp]['spec']['parameters'] for fp in fps];assert p['source_component_parameters']==srcparams and p['component_capitals_usdt']==[x['initial_capital_usdt'] for x in srcparams] and sum(z*x['initial_capital_usdt'] for z,x in zip(ww,srcparams))==capital
  if row['mode']=='ownership':assert ww==[2*w,2*(1-w)] and p['component_capitals_usdt']==[10000,10000]
  else:assert ww==[1,1] and p['component_capitals_usdt']==[20000*w,20000*(1-w)] and [x['fixed_entry_notional_usdt'] for x in srcparams]==[2000*w,2000*(1-w)]
  rv=[e for e in events if e['fingerprint']==row['fingerprint'] and e['status']=='reserved'];assert len(rv)==1 and max(x['recorded_at_utc'] for x in rv)<report['evaluation_started_utc']
  if records[row['fingerprint']]['status']!='reserved':assert records[row['fingerprint']]['report_sha256']==sha(R/'report.json')
  for k,z in arc['scenes'].items():
   v=np.zeros(len(union))
   for fp,a in zip(fps,ww):v+=vectors[fp,k]*a
   s=z['summary'];parts=[ss[fp,k] for fp in fps];assert s==c['scenes'][k] and v[0]==capital and s['initial_capital_usdt']==capital and s['NAV_points']==len(v)==545013 and hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==s['NAV_sha256_f64le'] and z['source_fingerprints']==fps and z['source_full_NAV_sha256']==[x['NAV_sha256_f64le'] for x in parts];daily=v[days].tolist();assert daily==s['daily_equity_usdt'];metrics(v,daily,370,s);checks+=1
   for j,(a,b) in enumerate(zip(folds,folds[1:])):
    lo,hi=j*30,min((j+1)*30,370);f=s['folds'][j];assert f['duration_days']==hi-lo and f['start_utc']==engine.stamp(int(union['t'][a])) and f['end_exclusive_utc']==engine.stamp(int(union['t'][b]));metrics(v[a:b+1],daily[lo:hi+1],hi-lo,f);checks+=1
   assert len(s['folds'])==13 and abs(math.prod(1+f['net_return_pct']/100 for f in s['folds'])-v[-1]/capital)<1e-12;verify_recent(v,common,s);recentchecks+=9
   money=['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','gross_reference_price_PnL_usdt'];counts=['executions','round_trips','rejected_orders','cash_or_units_violations','funding_settlements','nonzero_funding_settlements']
   for f in money:near(s[f],sum(a*x[f] for a,x in zip(ww,parts)))
   for f in counts:assert s[f]==sum(x[f] for x in parts)
   for f,val in s['cost_parts_usdt'].items():near(val,sum(a*x['cost_parts_usdt'][f] for a,x in zip(ww,parts)))
   near(s['gross_reference_price_PnL_usdt']+s['funding_usdt']-s['cost_usdt'],v[-1]-capital);near(s['cost_pct_initial'],s['cost_usdt']/capital*100);assert all(D(x['terminal_units'])==0 for x in parts) and D(s['terminal_units'])==0
   assert s['margin']=={'independent_sleeve_violations':sum(x['margin']['violations'] for x in parts),'minimum_individual_sleeve_cushion_usdt':min((a*x['margin']['minimum_equity_minus_maintenance_usdt'] for a,x in zip(ww,parts) if x['margin']['minimum_equity_minus_maintenance_usdt'] is not None),default=None),'no_cross_margin_netting':True};scenes+=1
  if row['role']=='candidate':base.qualification(c,grid)
  else:assert c['status']=='rejected' and c['criteria']=={'reference_or_fixed_BTC_execution_component_only':False}
 assert scenes==30 and checks==420 and recentchecks==270 and all(sha(ROOT/p)==h for p,h in json.loads((R/'context.json').read_text())['account_hashes_before'].items())
 for path in ['audit.py','audit_native.py','audit_helpers.py']:
  tree=ast.parse((R/path).read_text());assert not any(isinstance(x,ast.Call) and ((isinstance(x.func,ast.Attribute) and x.func.attr in ['simulate','target','trade','funding_amount']) or (isinstance(x.func,ast.Name) and x.func.id in ['simulate','target','trade','funding_amount'])) for x in ast.walk(tree))
 out={'passed':True,'actual_financial_configs':20,'actual_candidates':18,'actual_benchmarks':2,'new_native_components':10,'new_passive_parents':10,'source_native_components_reused_readonly':5,'source_native_cost_NAVs_recovered':15,**counters,'cost_scenes_audited':scenes+30,'full_NAV_points_per_scene':len(union),'full_NAV_points_audited':len(union)*(scenes+30),'independent_overall_and_fold_metric_checks':checks+420,'independent_recent40_and_fold_metric_checks':recentchecks+270,'structured_clock_raw_units_capital20000_verified':True,'strict_new_eachcost_and_neighborhood_gates_verified':True,'external_ungated_and_hold_controls_unchanged':True,'source_models_not_rerun':True,'protected_inputs_unchanged':True,'report_sha256':sha(R/'report.json')};out.update(native_proof);put(R/'verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
