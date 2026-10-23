"""Independent trade-ledger NAV reconstruction and portfolio risk audit; no signals or fills rerun."""
import json,math
from decimal import Decimal as D
import numpy as np
from run import R,ROOT,core,reg,sha,readgz,module,sources,summarize_pair,put

def main():
 plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());batch=json.loads((R/'batch.json').read_text());frames,refs,arcs,vectors,folds,proof=sources(plan);metrics=module(ROOT/'research/experiments/20261001T213902Z/audit.py','independent_combo_metrics');source_checks=0;balance_checks=0;nav_checks=0
 for fp,ref in refs.items():
  f=frames[ref['year'],ref['asset']];close=np.asarray(f['close'].cast(__import__('polars').Float64))
  for k,z in arcs[fp]['scenes'].items():
   cash,qty=D(ref['capital_usdt']),D(0);v=np.empty(core.POINTS);v[0]=float(cash);by={}
   for t in z['trades']:by.setdefault(int(t['day_offset']),[]).append(t)
   for d in range(181):
    i=183+d;mi=i*1440+1
    for t in by.get(d,[]):
     assert t['trade_ts_ns']==int(f['open_ts'][mi]) and D(t['reference'])==f['open'][mi]
     c,q=D(t['cash_after']),D(t['units_after']);assert c>=0 and q>=0
     if t['status']=='filled':
      assert abs(cash+qty*D(t['reference'])-c-q*D(t['reference'])-D(t['cost_usdt']))<D('1e-18');balance_checks+=1
     else:assert c==cash and q==qty
     cash,qty=c,q
    if d<180:
     v[d*core.SPAN+1]=float(cash+qty*f['open'][mi]);v[d*core.SPAN+2:(d+1)*core.SPAN+1]=float(cash)+float(qty)*close[mi:mi+1440]
   v[-1]=float(cash+qty*f['open'][363*1440+1]);assert qty==0 and cash==D(z['terminal_cash']) and np.array_equal(v,vectors[fp,k]) and core.navhash(v)==z['summary']['NAV_sha256_f64le'];source_checks+=1
 events=reg.read_events(ROOT/'research/automation/registry.jsonl');ledger=reg.read_records(ROOT/'research/automation/registry.jsonl')
 for b in batch:
  cfg=report['configs'][b['name']];path=ROOT/cfg['archive'];assert sha(path)==cfg['archive_sha256'];saved=readgz(path);assert saved['fingerprint']==b['fingerprint'] and reg.fingerprint(saved['spec'])==b['fingerprint']
  reservations=[e for e in events if e['fingerprint']==b['fingerprint'] and e['status']=='reserved'];assert len(reservations)==1 and reservations[0]['recorded_at_utc']<report['evaluation_started_utc']
  scenes,full=summarize_pair(b,plan,arcs,vectors,folds);assert scenes==cfg['scenes'] and core.canonical(full)==saved['scenes']
  fps=[x['fingerprint'] for x in b['component_refs']];assert [refs[x]['capital_usdt'] for x in fps]==[1500,500] and [c['weight'] for c in saved['spec']['components']]==[.75,.25]
  for k,s in scenes.items():
   v=vectors[fps[0],k]+vectors[fps[1],k];assert v[0]==2000 and core.navhash(v)==s['NAV_sha256_f64le'];metrics.check_metrics(v,s,180,True)
   for j,fold in enumerate(s['folds']):metrics.check_metrics(v[j*30*core.SPAN:(j+1)*30*core.SPAN+1+(j==5)],fold,30,j==5)
   assert abs(math.prod(1+f['net_return_pct']/100 for f in s['folds'])-v[-1]/2000)<1e-12
   cost=sum(arcs[x]['scenes'][k]['summary']['cost_usdt'] for x in fps);assert abs(cost-s['cost_usdt'])<1e-8;nav_checks+=len(v)
  frac=cfg['sensitivity']['local_3x_neighbor_positive_fraction'];neighbors=[report['configs'][n] for n in cfg['sensitivity']['neighbor_names']];assert frac==sum(x['scenes']['3']['net_return_pct']>0 for x in neighbors)/len(neighbors)
  ss=scenes;ratio=ss['1']['gross_reference_PnL_to_execution_cost'];expected={'positive_all_costs':all(x['net_return_pct']>0 for x in ss.values()),'four_positive_1x_folds':sum(f['net_return_pct']>0 for f in ss['1']['folds'])>=4,'minute_DD3_lte25pct':ss['3']['max_drawdown_pct']<=25,'neighbourhood_positive3_gte60pct':frac>=.6,'two_round_trips1':ss['1']['round_trips']>=2,'gross_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_balance_violations':all(x['cash_or_units_violations']==0 for x in ss.values()),'no_exchange_or_capacity_rejections':all(x['rejected_orders']==0 for x in ss.values()),'terminal_flat':all(D(x['terminal_units'])==0 for x in ss.values())};assert expected==cfg['criteria'] and (cfg['status']=='passed')==all(expected.values());assert cfg['both_periods_meet_full_gates']==(cfg['status']==report['configs'][cfg['other_period_config']]['status']=='passed')
  if ledger[b['fingerprint']]['status']!='reserved':assert ledger[b['fingerprint']]['report_sha256']==sha(R/'report.json') and ledger[b['fingerprint']]['status']==cfg['status']
 ctx=json.loads((R/'context.json').read_text());assert all(sha(ROOT/p)==h for p,h in ctx['account_hashes_before'].items())
 out={'passed':True,'report_sha256':sha(R/'report.json'),'source_component_scenes_rebuilt_by_segments_and_independent_trade_ledgers':source_checks,'archived_source_balance_events_checked':balance_checks,'new_parent_cost_scenes_replayed':54,'new_portfolio_full_minute_NAV_points_checked':nav_checks,'independent_global_and_fold_return_DD_Sharpe_Calmar_checks':54*7,'source_signals_or_orders_recomputed':0,'original_source_statuses_or_reports_changed':False,'protected_inputs_unchanged':True};put(R/'verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
