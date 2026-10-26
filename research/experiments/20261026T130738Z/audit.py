"""Independent stored-ledger playback and structured-clock portfolio verification."""
import gzip,hashlib,json,math,ast
from decimal import Decimal as D
import numpy as np
import engine
from run import ROOT,R,sha,put,reg,module,grid_configs
from audit_helpers import near,metrics,verify_axis,verify_recent,replay,qualification
from audit_native import verify as verify_native

def main():
 report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');assert len(batch)==84 and report['summary']['cost_scenarios']==252 and report['frozen_plan_sha256']==sha(R/'plan.json');assert (R/'engine.py').read_bytes()==(ROOT/plan['native_engine_base']['path']).read_bytes();markets={a:engine.load_market(a,fs) for a,fs in plan['data']['assets'].items()}
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
 assert len(vectors)==261 and all(counters[k]==plan['recorded_source_events'][k] for k in counters);newvectors,native_proof=verify_native(report,plan,markets,events,records)
 for (fp,k),v in newvectors.items():vectors[fp,k]=v[ix['BTC']];ss[fp,k]=next(c for c in report['configs'].values() if c['fingerprint']==fp)['scenes'][k]
 all_sources={**plan['component_sources'],**{c['fingerprint']:c for c in report['configs'].values() if c['scope']=='native'}}
 checks=recentchecks=scenes=0;grid=grid_configs(report['configs'])
 for row in batch:
  if row['scope']!='parent':continue
  c=report['configs'][row['name']];sp=json.loads((ROOT/row['spec']).read_text());arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));assert sha(ROOT/c['archive'])==c['archive_sha256'] and arc['spec']==sp and arc['fingerprint']==row['fingerprint']==reg.fingerprint(sp);p=sp['parameters'];assert p['initial_capital_usdt']==20000 and p['component_capitals_usdt']==[10000,10000] and p['component_initial_entry_notionals_usdt']==[row['BTC_fixed_entry_notional_usdt'],row['ETH_fixed_entry_notional_usdt']] and p['raw_component_multipliers']==[1,1] and [x['weight'] for x in sp['components']]==[1,1];fps=row['source_fingerprints'];assert [x['fingerprint'] for x in sp['components']]==fps and [all_sources[fp]['asset'] for fp in fps]==['BTC','ETH']
  src=all_sources[fps[0]];assert src['asset']=='BTC' and src['lookback_days']==p['BTC_lookback_days']==31 and src['return_hurdle']==p['BTC_return_hurdle']==row['BTC_return_hurdle']==.06 and src['exit_buffer_fraction']==row['trend_exit_buffer_fraction']==p['BTC_exit_buffer_fraction'] and src['fixed_entry_notional_usdt']==row['BTC_fixed_entry_notional_usdt']==p['BTC_fixed_entry_notional_usdt']
  src=plan['component_sources'][fps[1]];assert src['asset']=='ETH' and src['trend_lookback_days']==row['trend_filter_lookback_days']==p['ETH_trend_lookback_days'] and src['lookback_days']==row['reversal_lookback_days']==p['ETH_lookback_days'] and src['return_hurdle']==row['reversal_return_hurdle']==p['ETH_return_hurdle'] and src['exit_buffer_fraction']==p['ETH_exit_buffer_fraction']==0 and src['fixed_entry_notional_usdt']==row['ETH_fixed_entry_notional_usdt']==p['ETH_fixed_entry_notional_usdt']
  assert row['ETH_fixed_entry_notional_usdt'] in [1000,2000,3000] and row['trend_exit_buffer_fraction']==.01 and sum(p['component_initial_entry_notionals_usdt'])==4000
  rv=[e for e in events if e['fingerprint']==row['fingerprint'] and e['status']=='reserved'];assert len(rv)==1 and rv[0]['recorded_at_utc']<report['evaluation_started_utc']
  if records[row['fingerprint']]['status']!='reserved':assert records[row['fingerprint']]['report_sha256']==sha(R/'report.json')
  for k,s in arc['scenes'].items():
   v=vectors[fps[0],k]+vectors[fps[1],k];z=s['summary'];parts=[ss[fp,k] for fp in fps];assert z==c['scenes'][k] and v[0]==20000 and z['initial_capital_usdt']==20000 and z['NAV_points']==len(v)==len(union)==545013 and hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==z['NAV_sha256_f64le'];assert s['source_fingerprints']==fps and s['source_full_NAV_sha256']==[x['NAV_sha256_f64le'] for x in parts];daily=v[daily_idx].tolist();assert daily==z['daily_equity_usdt'];metrics(v,daily,370,z);checks+=1
   for j,(a,b) in enumerate(zip(fold_idx,fold_idx[1:])):
    l,h=j*30,min((j+1)*30,370);f=z['folds'][j];assert f['duration_days']==h-l and f['start_utc']==engine.stamp(int(union['t'][a])) and f['end_exclusive_utc']==engine.stamp(int(union['t'][b]));metrics(v[a:b+1],daily[l:h+1],h-l,f);checks+=1
   assert len(z['folds'])==13 and abs(math.prod(1+f['net_return_pct']/100 for f in z['folds'])-v[-1]/20000)<1e-12;verify_recent(v,common,z);recentchecks+=9
   for field in ['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','gross_reference_price_PnL_usdt','executions','round_trips','rejected_orders','cash_or_units_violations','funding_settlements','nonzero_funding_settlements']:near(z[field],sum(x[field] for x in parts))
   near(z['gross_reference_price_PnL_usdt']+z['funding_usdt']-z['cost_usdt'],v[-1]-20000);assert z['funding_settlements']==2220 and all(D(x['terminal_units'])==0 for x in parts) and D(z['terminal_units'])==0
   for field,value in z['cost_parts_usdt'].items():near(value,sum(x['cost_parts_usdt'][field] for x in parts))
   assert z['margin']=={'independent_sleeve_violations':sum(x['margin']['violations'] for x in parts),'minimum_individual_sleeve_cushion_usdt':min((x['margin']['minimum_equity_minus_maintenance_usdt'] for x in parts if x['margin']['minimum_equity_minus_maintenance_usdt'] is not None),default=None),'no_cross_margin_netting':True};scenes+=1
  qualification(c,grid)
 assert scenes==243 and checks==3402 and recentchecks==2187 and all(sha(ROOT/p)==h for p,h in json.loads((R/'context.json').read_text())['account_hashes_before'].items())
 for path in ['audit.py','audit_native.py','audit_helpers.py']:
  tree=ast.parse((R/path).read_text());assert not any(isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr in ['simulate','target','trade','funding_amount'] for x in ast.walk(tree))
 out={'passed':True,'actual_financial_configs':84,'new_native_components':3,'new_passive_parents':81,'source_native_components_reused_readonly':87,'source_native_cost_NAVs_recovered':261,**counters,'parent_cost_scenes_audited':scenes,'cost_scenes_audited':scenes+native_proof['native_cost_scenes_audited'],'full_NAV_points_per_scene':len(union),'full_NAV_points_audited':len(union)*(scenes+native_proof['native_cost_scenes_audited']),'independent_overall_and_fold_metric_checks':checks+native_proof['native_metric_checks'],'independent_recent40_and_fold_metric_checks':recentchecks+native_proof['native_recent_metric_checks'],'structured_ns_key_and_raw1_1_20000_sum_verified':True,'full5D_parent243_native2D9_old168_qualification_unchanged':True,**native_proof,'source_signals_orders_funding_models_not_rerun':True,'protected_inputs_unchanged':True,'report_sha256':sha(R/'report.json')};put(R/'verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
