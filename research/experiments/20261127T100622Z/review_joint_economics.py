"""Compare saved results and real policy fields to the predeclared same-ETH-funding-max-age BTC confirmation-hurdle.0025 controls."""
import csv,gzip,json,math
from common import *
rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');r=rd(R/'report.json');controls=p['additional_predeclared_BTCConfirm0p0025_report_controls'];rows=[];centerrows=[]
def cfg(z):
 assert sha(ROOT/z['report'])==z['report_sha256'];return next(c for c in rd(ROOT/z['report'])['configs'].values() if c['fingerprint']==z['fingerprint'])
def compare(c,old,k):
 s,b=c['scenes'][k],old['scenes'][k];z={'fingerprint':c['fingerprint'],'BTC_selected_confirmation_hurdle':c['W'],'ETH_selected_funding_max_age_hours':c['K'],'cost':int(k),'old_baseline_fingerprint':old['fingerprint'],'full_NAV_hash_identical':s['NAV_sha256_f64le']==b['NAV_sha256_f64le']}
 for f in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:z[f]=s[f];z['old_'+f]=b[f];z['delta_'+f]=s[f]-b[f]
 signs=[z['delta_net_return_pct'],-z['delta_max_drawdown_pct'],z['delta_sharpe_365'],z['delta_calmar']];z['strict_four_metric_improvement']=all(x>=-1e-10 for x in signs) and any(x>1e-10 for x in signs);z['old_weakly_dominates']=all(x<=1e-10 for x in signs) and any(x<-1e-10 for x in signs);return z
center=cfg(controls[str(p['default_control_preset']['K'])])
for c in r['configs'].values():
 old=cfg(controls[str(c['K'])])
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
   before='raw_desired_before_entry_filter';after='raw_desired_before_confirmation_filter' if asset=='BTC' else 'raw_desired_before_funding_filter'
   assert all(before in d['policy_audit'] and after in d['policy_audit'] and 'observed_sample_logvol' in d['policy_audit'] for pair in pairs for d in pair)
   m['entry_return_hurdle']=ar['spec']['parameters']['return_hurdle'];m['exit_buffer_fraction']=ar['spec']['parameters']['exit_buffer_fraction'];m['entry_volatility_window_days']=ar['spec']['parameters']['entry_volatility_window_days'];m['entry_volatility_ceiling']=ar['spec']['parameters']['entry_volatility_ceiling'];m['entry_volatility_block_flag_changes']=sum((x['policy_audit'][before]!=x['policy_audit'][after])!=(y['policy_audit'][before]!=y['policy_audit'][after]) for x,y in pairs);m['observed_sample_logvol_changes']=sum(abs(x['policy_audit']['observed_sample_logvol']-y['policy_audit']['observed_sample_logvol'])>1e-12 for x,y in pairs)
   if asset=='BTC':
    m['entry_directional_confirmation_hurdle']=ar['spec']['parameters']['entry_directional_confirmation_hurdle'];m['confirmation_gate_flag_changes']=sum((x['policy_audit']['raw_desired_before_confirmation_filter']!=x['desired_direction'])!=(y['policy_audit']['raw_desired_before_confirmation_filter']!=y['desired_direction']) for x,y in pairs)
   if asset=='ETH':
    m['entry_funding_max_age_hours']=ar['spec']['parameters']['entry_funding_max_age_hours'];m['entry_funding_settlement_count']=ar['spec']['parameters']['entry_funding_settlement_count'];m['trend_slope_lag_days']=ar['spec']['parameters']['trend_slope_lag_days'];m['funding_budget_volatility_window_days']=ar['spec']['parameters']['entry_funding_budget_volatility_window_days'];m['entry_funding_volatility_ratio']=ar['spec']['parameters']['entry_funding_volatility_ratio']
    m['trend_gate_direction_changes']=sum(x['policy_audit']['slowgate_direction']!=y['policy_audit']['slowgate_direction'] for x,y in pairs);m['funding_budget_cap_changes']=sum(x['policy_audit']['funding_filter']['cap_fraction_per_settlement']!=y['policy_audit']['funding_filter']['cap_fraction_per_settlement'] for x,y in pairs);m['selected_mature_settlement_lists_changed']=sum(x['policy_audit']['funding_filter']['selected_settlements']!=y['policy_audit']['funding_filter']['selected_settlements'] for x,y in pairs);m['funding_block_flag_changes']=sum(x['policy_audit']['funding_filter']['blocked']!=y['policy_audit']['funding_filter']['blocked'] for x,y in pairs)
   mechanism.append(m)
for name,xs in [('matched_ETHFundingAge_BTCConfirm0p0025_comparisons',rows),('default_BTCConfirm0p0025_ETHAge36h_comparisons',centerrows)]:
 with (R/'exports'/(name+'.csv')).open('w',newline='') as f:w=csv.DictWriter(f,list(xs[0]),lineterminator='\n');w.writeheader();w.writerows(xs)
out={'passed':True,'saved_results_only':True,'new_models_or_account_evaluations':0,'comparison_rows':rows,'default_comparison_rows':centerrows,'native_mechanism_rows':mechanism,'allcost_path_alias_new_graphs':sum(all(z['full_NAV_hash_identical'] for z in rows if z['fingerprint']==c['fingerprint']) for c in r['configs'].values()),'strict_four_metric_improvement_rows':sum(z['strict_four_metric_improvement'] for z in rows),'old_weakly_dominated_rows':sum(z['old_weakly_dominates'] for z in rows),'default_strict_improvement_rows':sum(z['strict_four_metric_improvement'] for z in centerrows),'default_old_dominates_rows':sum(z['old_weakly_dominates'] for z in centerrows),'NAV_identity_scope':'12 predeclared read-only old results;not a global historical NAV search','only_present_actual_policy_fields_used':True,'no_reselection_or_grid_extension':True};put(R/'joint_economic_review.json',out);print(json.dumps({k:out[k] for k in ['passed','allcost_path_alias_new_graphs','strict_four_metric_improvement_rows','default_strict_improvement_rows','default_old_dominates_rows']},ensure_ascii=False))
