"""Readonly matched-ungated equivalence;do not treat inactive gates as independentalpha."""
import json
from run import R,sha,put
from controls import matched
r=json.loads((R/'report.json').read_text());own,ungated,holds=matched(r['configs']);out=[]
for c in r['configs'].values():
 if c['role']!='candidate':continue
 ref=ungated[c['scope'],c['BTC_capital_fraction']];same=all(c['scenes'][k]['NAV_sha256_f64le']==ref['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']);joint=all(c['scenes'][k]['net_return_pct']>ref['scenes'][k]['net_return_pct'] and c['scenes'][k]['max_drawdown_pct']<ref['scenes'][k]['max_drawdown_pct'] for k in ['1','2','3']);out.append({'name':c['name'],'scope':c['scope'],'status':c['status'],'matched_actualscale_ungated':ref['name'],'same_threecost_complete_NAVs':same,'joint_full_return_DD_improvement_everycost':joint})
proof={'passed':True,'new_financial_evaluations':0,'financial_report_sha256':sha(R/'report.json'),'candidate_comparisons':out,'exact_ungated_matches':sum(x['same_threecost_complete_NAVs'] for x in out),'passed_matches_to_ungated':sum(x['status']=='passed' and x['same_threecost_complete_NAVs'] for x in out),'joint_full_return_DD_improvements':sum(x['joint_full_return_DD_improvement_everycost'] for x in out),'comparison_scope':'Thisbatchmatchedactualscalecontrols,not globalhistoricalNAVnovelty orindependentfuture evidence.'};put(R/'comparison_verification.json',proof)
with (R/'result.md').open('a') as f:f.write('\n同规模无过滤对照只读核验：'+str(proof['exact_ungated_matches'])+'个候选的三成本完整净值与无过滤完全一致，其中历史passed有'+str(proof['passed_matches_to_ungated'])+'个；不能把该资金费上限未生效的路径当作新增独立alpha。全成本同时提高全期收益且降低整体DD的候选有'+str(proof['joint_full_return_DD_improvements'])+'个。资格保持原预设判据，仅补充证据范围，不改旧/新登记状态。\n')
print(json.dumps({k:v for k,v in proof.items() if k!='candidate_comparisons'},ensure_ascii=False))
