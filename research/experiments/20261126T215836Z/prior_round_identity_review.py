"""Compare saved full-NAV hashes to the previous report fixed in the frozen plan."""
import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
b=rd(R/'prior_round_identity_binding.json');assert sha(Path(__file__))==b['source_sha256'] and b['bound_before_readonly_execution'] and b['no_new_model_or_configuration_evaluations']
p=rd(R/'plan.json');r=rd(R/'report.json');ref=p['prior_report'];assert ref==b['reference_fixed_in_plan_before_reserve'] and sha(ROOT/ref['path'])==ref['sha256'] and sha(R/'report.json')==b['financial_report_sha256'] and sha(R/'forward_report.json')==b['SMA_report_sha256']
old=rd(ROOT/ref['path']);same_axis=r['parent_axis']['union_axis_sha256']==old['parent_axis']['union_axis_sha256'];rows=[]
for c in r['configs'].values():
 signature=[c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']];matches=[]
 for d in old['configs'].values():
  assert c['capital_usdt']==d['capital_usdt']==18750 and c['raw_weights']==d['raw_weights']==[1,1]
  if same_axis and signature==[d['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']]:matches.append({'fingerprint':d['fingerprint'],'BTC_axis_value':d['W'],'ETH_axis_value':d['K']})
 rows.append({'fingerprint':c['fingerprint'],'BTC_axis_value':c['W'],'ETH_axis_value':c['K'],'all3_saved_full_NAV_hashes':signature,'previous_config_matches':matches})
aliases=sum(bool(z['previous_config_matches']) for z in rows);before=sha(R/'result.md');text=(R/'result.md').read_text();text+=f"\n前轮完整路径补充核对：冻结计划在reserve前已指定prior_report，本项只读比较该前轮{len(old['configs'])}个真实新结果，不做全历史搜索或模型重跑。共同事件轴一致性{same_axis}；本轮{len(rows)}个新参数定义中，{aliases}个在1/2/3倍成本下的完整连续OOS净值哈希均已见于前轮，因此相对于该前轮有{len(rows)-aliases}个未匹配配置定义（不是独立净值路径数，路径去重另见saved_result_review.json）。该范围不同于原{len(p['read_only_references'])}个预声明控制的NAV别名统计；不能将这些新定义数当作独立alpha试验数。完整指纹与三档NAV哈希见prior_round_NAV_identity.json。\n";(R/'result.md').write_text(text)
assert sha(R/'report.json')==b['financial_report_sha256'] and sha(R/'forward_report.json')==b['SMA_report_sha256'] and sha(ROOT/ref['path'])==ref['sha256']
put(R/'prior_round_NAV_identity.json',{'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':b['source_sha256'],'reference_fixed_before_current_reserve':ref,'same_common_event_axis':same_axis,'new_definitions':len(rows),'definitions_matching_previous_all3_full_NAVs':aliases,'not_matching_previous_scope':len(rows)-aliases,'comparisons':rows,'current_axes':p['axes'],'current_axis_semantics':p['axis_semantics'],'scope':'The previous report already named in plan.json;not a global historical search or parameter selection.','financial_report_sha256_unchanged':b['financial_report_sha256'],'SMA_report_sha256_unchanged':b['SMA_report_sha256'],'result_before_sha256':before,'result_after_sha256':sha(R/'result.md'),'new_strategy_account_or_cashflow_evaluations':0});print(json.dumps({'passed':True,'same_axis':same_axis,'new_definitions':len(rows),'previous_full_NAV_aliases':aliases,'new_evaluations':0}))
