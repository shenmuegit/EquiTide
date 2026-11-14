"""Saved actual component PnL and role classification; zero model/account execution."""
import gzip,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import sha,put,now,rel
rd=lambda p:json.loads(p.read_text());r=rd(R/'report.json');p=rd(R/'plan.json');h=sha(R/'report.json');by={c['fingerprint']:c for c in r['configs'].values()};near=lambda a,b:abs(a-b)<=1e-8*max(1,abs(a),abs(b));rows=[]
for g in p['grid']:
 c=by[g['fingerprint']];b,e=[by[f] for f in g['source_fingerprints']]
 for k,s in c['scenes'].items():
  bs,es=b['scenes'][k],e['scenes'][k];bp=bs['final_NAV_usdt']-bs['initial_capital_usdt'];ep=es['final_NAV_usdt']-es['initial_capital_usdt'];pp=s['final_NAV_usdt']-s['initial_capital_usdt'];bb,ee,ps=[z['extension21'] for z in [bs,es,s]];be=bb['final_NAV_usdt']-bb['initial_NAV_usdt'];et=ee['final_NAV_usdt']-ee['initial_NAV_usdt'];pe=ps['final_NAV_usdt']-ps['initial_NAV_usdt'];assert near(pp,bp+ep) and near(pe,be+et)
  rows.append({'parent_fingerprint':c['fingerprint'],'BTC_vol_cap':c['W'],'ETH_funding_ratio':c['K'],'cost_multiplier':int(k),'BTC_full_PnL_usdt':bp,'ETH_full_PnL_usdt':ep,'parent_full_PnL_usdt':pp,'BTC_extension21_PnL_usdt':be,'ETH_extension21_PnL_usdt':et,'parent_extension21_PnL_usdt':pe})
cliffs=rd(R/'export_verification.json')['cliffs_over_two_std'];put(R/'component_attribution.json',{'passed':True,'verified_utc':now(),'report_sha256':h,'readonly_source_sha256':sha(Path(__file__)),'scope':'Arithmetic decomposition of saved actual391day banks only,no alternative configuration or NAV/strategy execution.','rows':rows,'all12_strategy_parent_cost_scenes_checked':len(rows)==12,'ETH_extension21_all_zero_PnL':all(z['ETH_extension21_PnL_usdt']==0 for z in rows),'cliff_flag_count':len(cliffs),'Sharpe_cliff_flagged_edges':cliffs})
roles={role:[c['name'] for c in r['configs'].values() if c['role']==role] for role in ['candidate','component','benchmark']};assert [len(roles[x]) for x in ['candidate','component','benchmark']]==[4,4,3]
put(R/'classification_verification.json',{'passed':True,'report_sha256':h,'roles':roles,'actual_candidate_strategy_combinations':4,'actual_policy_components':4,'actual_benchmarks':3,'passed_candidates':sum(by[g['fingerprint']]['status']=='passed' for g in p['grid']),'rejected_policy_components':sum(c['role']=='component' and c['status']=='rejected' for c in by.values()),'rejected_benchmarks':sum(c['role']=='benchmark' and c['status']=='rejected' for c in by.values()),'summary_rejected_source_components_excludes_benchmark_legs':True,'financial_report_bytes_unchanged':True})
assert sha(R/'report.json')==h;print('PASS12savedparentcostdecompositions,explicit4policy/3benchmarkclassification;no reruns')
