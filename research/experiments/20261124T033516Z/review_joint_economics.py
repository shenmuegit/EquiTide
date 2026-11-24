"""Compare saved actual results to predeclared same-cap baseline R.0075 and central controls."""
import json,gzip,csv
from common import *
rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');r=rd(R/'report.json');controls=p['additional_predeclared_baseR_report_controls'];rows=[];centerrows=[]
def cfg(z):
 assert sha(ROOT/z['report'])==z['report_sha256'];return next(x for x in rd(ROOT/z['report'])['configs'].values() if x['fingerprint']==z['fingerprint'])
def compare(c,old,k):
 s,b=c['scenes'][k],old['scenes'][k];z={'fingerprint':c['fingerprint'],'BTC_logvol_cap':c['W'],'ETH_budget_ratio':c['K'],'cost':int(k),'old_baseline_fingerprint':old['fingerprint'],'full_NAV_hash_identical':s['NAV_sha256_f64le']==b['NAV_sha256_f64le']}
 for f in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:z[f]=s[f];z['old_'+f]=b[f];z['delta_'+f]=s[f]-b[f]
 signs=[z['delta_net_return_pct'],-z['delta_max_drawdown_pct'],z['delta_sharpe_365'],z['delta_calmar']];z['strict_four_metric_improvement']=all(x>=-1e-10 for x in signs) and any(x>1e-10 for x in signs);z['old_weakly_dominates']=all(x<=1e-10 for x in signs) and any(x<-1e-10 for x in signs);return z
center=cfg(controls[str(.0275)])
for c in r['configs'].values():
 old=cfg(controls[str(c['W'])])
 for k in ['1','2','3']:rows.append(compare(c,old,k));centerrows.append(compare(c,center,k))
mechanism=[]
for asset,basefp in [('BTC','41de4309229b892489a07574af07a73ae93229a35c118558ed60362285e90c89'),('ETH',p['baseline_native_fingerprint'])]:
 base=json.loads(gzip.decompress((ROOT/p['read_only_references'][basefp]['archive']).read_bytes()))
 for fp,z in p['read_only_references'].items():
  if z['scope']!='native' or z['role']!='component' or z['asset']!=asset:continue
  ar=json.loads(gzip.decompress((ROOT/z['archive']).read_bytes()))
  for k,s in ar['scenes'].items():
   b=base['scenes'][k];pairs=list(zip(s['decisions'],b['decisions']));assert len(pairs)==391 and all(x['execution_ts_ns']==y['execution_ts_ns'] for x,y in pairs);sm,bm=s['summary'],b['summary'];m={'asset':asset,'fingerprint':fp,'coordinate':z['W'] if asset=='BTC' else z['K'],'cost':int(k),'desired_direction_changes':sum(x['desired_direction']!=y['desired_direction'] for x,y in pairs),'full_NAV_hash_identical':sm['NAV_sha256_f64le']==bm['NAV_sha256_f64le']}
   for f in ['executions','round_trips','gross_reference_price_PnL_usdt','funding_usdt','cost_usdt']:m['delta_'+f]=sm[f]-bm[f]
   if asset=='ETH':m['funding_budget_cap_changes']=sum(x['policy_audit']['funding_filter']['cap_fraction_per_settlement']!=y['policy_audit']['funding_filter']['cap_fraction_per_settlement'] for x,y in pairs);m['selected_mature_settlement_lists_changed']=sum(x['policy_audit']['funding_filter']['selected_settlements']!=y['policy_audit']['funding_filter']['selected_settlements'] for x,y in pairs);m['funding_block_flag_changes']=sum(x['policy_audit']['funding_filter']['blocked']!=y['policy_audit']['funding_filter']['blocked'] for x,y in pairs)
   mechanism.append(m)
for name,xs in [('same_cap_baseR_comparisons',rows),('central_cap_baseR_comparisons',centerrows)]:
 with (R/'exports'/(name+'.csv')).open('w',newline='') as f:w=csv.DictWriter(f,list(xs[0]),lineterminator='\n');w.writeheader();w.writerows(xs)
put(R/'joint_economic_review.json',{'passed':True,'saved_results_only':True,'new_models_or_account_evaluations':0,'comparison_rows':rows,'central_comparison_rows':centerrows,'native_mechanism_rows':mechanism,'allcost_path_alias_new_graphs':sum(all(z['full_NAV_hash_identical'] for z in rows if z['fingerprint']==c['fingerprint']) for c in r['configs'].values()),'strict_four_metric_improvement_rows':sum(z['strict_four_metric_improvement'] for z in rows),'old_weakly_dominated_rows':sum(z['old_weakly_dominates'] for z in rows),'central_strict_improvement_rows':sum(z['strict_four_metric_improvement'] for z in centerrows),'central_old_dominates_rows':sum(z['old_weakly_dominates'] for z in centerrows),'NAV_identity_scope':'14 predeclared readonly old results;not a global historical NAV search','no_reselection_or_grid_extension':True});print(json.dumps({'same_cap_alias_graphs':sum(all(z['full_NAV_hash_identical'] for z in rows if z['fingerprint']==c['fingerprint']) for c in r['configs'].values()),'strict_improvement_rows':sum(z['strict_four_metric_improvement'] for z in rows),'central_improvement_rows':sum(z['strict_four_metric_improvement'] for z in centerrows),'central_dominated_rows':sum(z['old_weakly_dominates'] for z in centerrows),'mechanisms':mechanism},ensure_ascii=False),flush=True)
