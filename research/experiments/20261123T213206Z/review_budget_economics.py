"""Read saved real results only; compare preset budget variants with old controls."""
import csv,json,gzip
from decimal import Decimal as D
from common import *
rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');r=rd(R/'report.json');rows=[]
for c in r['configs'].values():
 z=p['additional_predeclared_R0075_report_controls'][str(c['W'])];old=next(v for v in rd(ROOT/z['report'])['configs'].values() if v['fingerprint']==z['fingerprint']);assert sha(ROOT/z['report'])==z['report_sha256']
 for k,s in c['scenes'].items():
  b=old['scenes'][k];row={'fingerprint':c['fingerprint'],'BTC_N':c['W'],'ETH_budget_R':c['K'],'cost':int(k),'old_baseline_fingerprint':old['fingerprint'],'full_NAV_hash_identical':s['NAV_sha256_f64le']==b['NAV_sha256_f64le']}
  for f in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:row[f]=s[f];row['old_'+f]=b[f];row['delta_'+f]=s[f]-b[f]
  signs=[row['delta_net_return_pct'],-row['delta_max_drawdown_pct'],row['delta_sharpe_365'],row['delta_calmar']];row['strict_four_metric_improvement']=all(z>=-1e-10 for z in signs) and any(z>1e-10 for z in signs);row['old_weakly_dominates']=all(z<=1e-10 for z in signs) and any(z<-1e-10 for z in signs);rows.append(row)
base=p['baseline_native_fingerprint'];ref=p['read_only_references'][base];old=gzip.decompress((ROOT/ref['archive']).read_bytes());old=json.loads(old);mechanisms=[]
for fp,z in p['read_only_references'].items():
 if z['asset']!='ETH' or z['role']!='component':continue
 ar=json.loads(gzip.decompress((ROOT/z['archive']).read_bytes()))
 for k,s in ar['scenes'].items():
  b=old['scenes'][k];pairs=list(zip(s['decisions'],b['decisions']));assert len(pairs)==391 and all(x['execution_ts_ns']==y['execution_ts_ns'] for x,y in pairs)
  sm,bm=s['summary'],b['summary'];diff=lambda f:sm[f]-bm[f]
  mechanisms.append({'source_fingerprint':fp,'R':z['K'],'cost':int(k),'decision_count':len(pairs),'funding_block_flag_changes':sum(x['policy_audit']['funding_filter']['blocked']!=y['policy_audit']['funding_filter']['blocked'] for x,y in pairs),'desired_direction_changes':sum(x['desired_direction']!=y['desired_direction'] for x,y in pairs),'full_NAV_hash_identical':sm['NAV_sha256_f64le']==bm['NAV_sha256_f64le'],'delta_executions':diff('executions'),'delta_round_trips':diff('round_trips'),'delta_gross_reference_PnL_usdt':diff('gross_reference_price_PnL_usdt'),'delta_funding_usdt':diff('funding_usdt'),'delta_execution_cost_usdt':diff('cost_usdt'),'delta_final_NAV_usdt':(sm['daily_equity_usdt'][-1]-bm['daily_equity_usdt'][-1])})
path=R/'exports/baseline_budget_comparisons.csv'
with path.open('w',newline='') as f:w=csv.DictWriter(f,list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
put(R/'budget_economic_review.json',{'passed':True,'saved_results_only':True,'new_strategy_or_account_evaluations':0,'comparison_rows':rows,'native_mechanism_rows':mechanisms,'allcost_path_alias_new_graphs':sum(all(z['full_NAV_hash_identical'] for z in rows if z['fingerprint']==c['fingerprint']) for c in r['configs'].values()),'strict_four_metric_improvement_rows':sum(z['strict_four_metric_improvement'] for z in rows),'old_weakly_dominated_rows':sum(z['old_weakly_dominates'] for z in rows),'csv':rel(path),'csv_sha256':sha(path),'no_reselection_or_grid_extension':True})
print(json.dumps({'rows':len(rows),'strict_improvement_rows':sum(z['strict_four_metric_improvement'] for z in rows),'old_dominates_rows':sum(z['old_weakly_dominates'] for z in rows),'identical_NAV_rows':sum(z['full_NAV_hash_identical'] for z in rows),'mechanism':mechanisms},ensure_ascii=False),flush=True)
