"""Independent stored-ledger playback and structured-clock portfolio verification."""
import gzip,hashlib,json,math,ast
from decimal import Decimal as D
import numpy as np
import engine
from run import ROOT,R,sha,put,reg,module,grid_configs
base=module(ROOT/'research/experiments/20261025T205634Z/audit.py','stored_ledger_independent_helpers')
near,metrics,verify_axis,verify_recent,replay,qualification=base.near,base.metrics,base.verify_axis,base.verify_recent,base.recover_from_recorded_events,base.verify_qualification

def main():
 report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');assert len(batch)==81 and report['summary']['cost_scenarios']==243 and report['frozen_plan_sha256']==sha(R/'plan.json');assert (R/'engine.py').read_bytes()==(ROOT/plan['native_engine_base']['path']).read_bytes();markets={a:engine.load_market(a,fs) for a,fs in plan['data']['assets'].items()}
 for m in markets.values():verify_axis(m)
 dtype=np.dtype([('t','<i8'),('k','<i8')]);structured={}
 for a,m in markets.items():
  keys=np.empty(len(m['ts']),dtype=dtype);keys['t']=m['ts'];keys['k']=m['codes'];structured[a]=keys
 union=np.union1d(structured['BTC'],structured['ETH']);packed=(union['t']-markets['BTC']['start_ns'])*16+union['k'];assert hashlib.sha256(packed.astype('<i8').tobytes()).hexdigest()==report['parent_axis']['union_axis_sha256'];ix={}
 for a,old in structured.items():
  j=np.searchsorted(old,union,side='right')-1;assert (j>=0).all() and ((old[j]['t']<union['t'])|((old[j]['t']==union['t'])&(old[j]['k']<=union['k']))).all() and np.array_equal(j[np.searchsorted(union,old)],np.arange(len(old)));ix[a]=j
 pre=np.flatnonzero(union['k']==5);assert len(pre)==370;daily_idx=np.asarray([0,*pre[1:],len(union)-1]);fold_idx=np.asarray([0,*pre[np.arange(30,370,30)],len(union)-1]);assert len(daily_idx)==371 and len(fold_idx)==14;common={'daily_indices':daily_idx,'ts':union['t']};vectors={};ss={};counters={'source_recorded_trades_checked':0,'source_recorded_funding_checked':0}
 for fp,ref in plan['component_sources'].items():
  assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['spec'])==ref['spec_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'] and records[fp]['status']==ref['original_status'] and records[fp]['report_sha256']==ref['report_sha256'];arc=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()));assert reg.fingerprint(arc['spec'])==fp and arc['spec']['parameters']['initial_capital_usdt']==10000 and arc['spec']['parameters']['fixed_entry_notional_usdt']==ref['fixed_entry_notional_usdt']
  for k,s in arc['scenes'].items():
   v=replay(markets[ref['asset']],s,counters,int(k));assert hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==ref['NAV_sha256_by_cost'][k];vectors[fp,k]=v[ix[ref['asset']]];ss[fp,k]=s['summary']
 assert len(vectors)==63 and all(counters[k]==plan['recorded_source_events'][k] for k in counters);checks=recentchecks=scenes=0;grid=grid_configs(report['configs'])
 for row in batch:
  c=report['configs'][row['name']];sp=json.loads((ROOT/row['spec']).read_text());arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));assert sha(ROOT/c['archive'])==c['archive_sha256'] and arc['spec']==sp and arc['fingerprint']==row['fingerprint']==reg.fingerprint(sp);p=sp['parameters'];weights=row['raw_component_multipliers'];a=row['ETH_A_ownership_fraction'];S=row['trend_filter_lookback_days'];capital=20000;assert p['initial_capital_usdt']==row['capital_usdt']==capital and p['component_capitals_usdt']==[10000]*3 and p['raw_component_multipliers']==weights==[1,a,1-a] and [x['weight'] for x in sp['components']]==weights;fps=row['source_fingerprints'];assert [x['fingerprint'] for x in sp['components']]==fps and [plan['component_sources'][fp]['asset'] for fp in fps]==['BTC','ETH','ETH'] and p['source_component_parameters']==[records[fp]['spec']['parameters'] for fp in fps]
  aa,ea,eb=[plan['component_sources'][fp] for fp in fps];assert aa['fixed_entry_notional_usdt']==1000 and ea['fixed_entry_notional_usdt']==eb['fixed_entry_notional_usdt']==3000 and p['effective_owned_entry_budgets_usdt']==[1000,3000*a,3000*(1-a)] and p['owned_component_capitals_usdt']==[10000,10000*a,10000*(1-a)] and sum(p['owned_component_capitals_usdt'])==20000
  assert aa['lookback_days']==31 and aa['return_hurdle']==.04 and aa['exit_buffer_fraction']==.01 and S in [27,28,29]
  for j,(ref,H,L) in enumerate([(ea,row['ETH_A_return_hurdle'],3),(eb,row['ETH_B_return_hurdle'],4)]):
   ep=json.loads((ROOT/ref['spec']).read_text())['parameters'];assert ep['trend_gate_mode']=='adjacent_horizon_majority' and ep['trend_gate_lookbacks_days']==p['ETH_slow_gate_lookbacks_days'][j]==[S-1,S,S+1] and ref['trend_lookback_days']==S and ref['lookback_days']==L and p['ETH_A_lookback_days' if j==0 else 'ETH_B_lookback_days']==L and ref['return_hurdle']==H==p['ETH_A_return_hurdle' if j==0 else 'ETH_B_return_hurdle'] and ref['exit_buffer_fraction']==0
  rv=[e for e in events if e['fingerprint']==row['fingerprint'] and e['status']=='reserved'];assert len(rv)==1 and rv[0]['recorded_at_utc']<report['evaluation_started_utc']
  if records[row['fingerprint']]['status']!='reserved':assert records[row['fingerprint']]['report_sha256']==sha(R/'report.json')
  for k,s in arc['scenes'].items():
   v=np.zeros(len(union))
   for fp,w in zip(fps,weights):v+=vectors[fp,k]*w
   z=s['summary'];parts=[ss[fp,k] for fp in fps];assert z==c['scenes'][k] and v[0]==capital and z['initial_capital_usdt']==capital and z['NAV_points']==len(v)==len(union)==545013 and hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==z['NAV_sha256_f64le'];assert s['source_fingerprints']==fps and s['source_full_NAV_sha256']==[x['NAV_sha256_f64le'] for x in parts];daily=v[daily_idx].tolist();assert daily==z['daily_equity_usdt'];metrics(v,daily,370,z);checks+=1
   for j,(a,b) in enumerate(zip(fold_idx,fold_idx[1:])):
    l,h=j*30,min((j+1)*30,370);f=z['folds'][j];assert f['duration_days']==h-l and f['start_utc']==engine.stamp(int(union['t'][a])) and f['end_exclusive_utc']==engine.stamp(int(union['t'][b]));metrics(v[a:b+1],daily[l:h+1],h-l,f);checks+=1
   assert len(z['folds'])==13 and abs(math.prod(1+f['net_return_pct']/100 for f in z['folds'])-v[-1]/capital)<1e-12;verify_recent(v,common,z);recentchecks+=9
   money=['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','gross_reference_price_PnL_usdt']
   counts=['executions','round_trips','rejected_orders','cash_or_units_violations','funding_settlements','nonzero_funding_settlements']
   for field in money:near(z[field],sum(w*x[field] for w,x in zip(weights,parts)))
   for field in counts:assert z[field]==sum(x[field] for x in parts)
   near(z['gross_reference_price_PnL_usdt']+z['funding_usdt']-z['cost_usdt'],v[-1]-capital);near(z['cost_pct_initial'],z['cost_usdt']/capital*100);assert z['funding_settlements']==3330 and all(D(x['terminal_units'])==0 for x in parts) and D(z['terminal_units'])==0
   for field,value in z['cost_parts_usdt'].items():near(value,sum(w*x['cost_parts_usdt'][field] for w,x in zip(weights,parts)))
   assert z['margin']=={'independent_sleeve_violations':sum(x['margin']['violations'] for x in parts),'minimum_individual_sleeve_cushion_usdt':min((w*x['margin']['minimum_equity_minus_maintenance_usdt'] for w,x in zip(weights,parts) if x['margin']['minimum_equity_minus_maintenance_usdt'] is not None),default=None),'no_cross_margin_netting':True};scenes+=1
  if row['role']=='candidate':qualification(c,grid)
  else:assert c['status']=='rejected' and c['criteria']=={'reference_only_no_alpha_qualification':False} and c['failed_criteria']==['reference_only_no_alpha_qualification'] and c['sensitivity']=={'reference_only':True}
 assert scenes==243 and checks==3402 and recentchecks==2187 and all(sha(ROOT/p)==h for p,h in json.loads((R/'context.json').read_text())['account_hashes_before'].items())
 for path in ['run.py','audit.py']:
  tree=ast.parse((R/path).read_text());assert not any(isinstance(x,ast.Call) and ((isinstance(x.func,ast.Attribute) and x.func.attr in ['simulate','target','trade','funding_amount']) or (isinstance(x.func,ast.Name) and x.func.id in ['simulate','target','trade','funding_amount'])) for x in ast.walk(tree))
 out={'passed':True,'actual_financial_configs':81,'new_native_components':0,'new_passive_parents':81,'source_native_components_reused_readonly':21,'source_native_cost_NAVs_recovered':63,**counters,'parent_cost_scenes_audited':scenes,'cost_scenes_audited':scenes,'full_NAV_points_per_scene':len(union),'full_NAV_points_audited':len(union)*scenes,'independent_overall_and_fold_metric_checks':checks,'independent_recent40_and_fold_metric_checks':recentchecks,'structured_ns_key_and_raw_ownership_variable_capital_verified':True,'full4D_81cells_18old_controls_unchanged':True,'source_signals_orders_funding_models_not_rerun':True,'protected_inputs_unchanged':True,'report_sha256':sha(R/'report.json')};put(R/'verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
