"""Explain saved M4-to-M5 cliffs from existing validated policy records; no backtest."""
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
import json,gzip,hashlib
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
b=rd(R/'cliff_mechanism_binding.json');assert b['bound_before_readonly_execution'] and sha(Path(__file__))==b['source_sha256']
for s,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/s)==h
p=rd(R/'plan.json');r=rd(R/'report.json');rows=[]
for fp,x in p['read_only_references'].items():
 if x['asset']!='ETH' or x['role']!='component':continue
 archive=ROOT/x['archive'];ar=json.loads(gzip.decompress(archive.read_bytes()));assert sha(archive)==x['archive_sha256']
 for k,scene in ar['scenes'].items():
  fs=[d['policy_audit']['funding_filter'] for d in scene['decisions']];assert len(fs)==391
  row={'fingerprint':fp,'archive':x['archive'],'archive_sha256':sha(archive),'mature_count':int(x['K']),'maximum_age_hours':ar['spec']['parameters']['entry_funding_max_age_hours'],'cost':int(k),'days':len(fs),'selected_count_distribution':dict(Counter(len(z['selected_settlements']) for z in fs)),'missing_median_days':sum(z['median_realized_rate'] is None for z in fs),'applicable_entry_decisions':sum(z['applied'] for z in fs),'blocked_applicable_entry_decisions':sum(z['blocked'] and z['applied'] for z in fs),'saved_native_scene':{f:scene['summary'][f] for f in ['net_return_pct','executions','round_trips','funding_usdt','cost_usdt']}};rows.append(row)
  if int(x['K'])==5:assert row['maximum_age_hours']==36 and row['missing_median_days']==391 and row['selected_count_distribution']=={0:391} and row['applicable_entry_decisions']==row['blocked_applicable_entry_decisions']==23 and all(v==0 for v in row['saved_native_scene'].values())
edges=rd(R/'export_verification.json')['cliffs_over_two_std'];assert len(edges)==3 and all(abs(e['delta_net_pp']+5.04149618407223)<1e-10 for e in edges)
before=sha(R/'result.md');text=(R/'result.md').read_text();text+='\n敏感性陡变机制：固定36小时可用范围与至少1小时可得滞后下，ETH M5的391天均缺少五条合格成熟结算记录（保存决策中的selected_settlements为空、median为None），冻结missing_policy拦截了三档成本各23次适用入场。M3/M4分别保存三/四条成熟结算，3倍成本适用入场均22次，拦截分别3/1次；M5的ETH子账户三档成本均无成交、费用或资金费，净收益均为0，完整15000资本闲置；M5组合收益来自BTC子账户。M5相对M4新增门控变化改变了交易与收益。三个BTC窗口的M4→M5相邻边3倍净收益均下降约5.041496个百分点，触发三条Sharpe陡变警告。四个新组合虽均通过绝对历史门槛，本轮不把该区域认定为参数稳健或新的更优候选；不按结果扩网、重选代表或修改冻结账户。完整逐成本政策统计和原档哈希见sensitivity_cliff_mechanism.json。\n';(R/'result.md').write_text(text)
for s,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/s)==h
put(R/'sensitivity_cliff_mechanism.json',{'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'saved_policy_records_only':True,'source_binding':'cliff_mechanism_binding.json','all_cost_policy_counts':rows,'adjacent_warning_edges':edges,'history_absolute_gates_passed':len(r['summary']['passed']),'parameter_robustness_demonstrated':False,'new_superior_candidate':False,'financial_report_sha256_unchanged':sha(R/'report.json'),'SMA_report_sha256_unchanged':sha(R/'forward_report.json'),'result_before_sha256':before,'result_after_sha256':sha(R/'result.md'),'new_strategy_account_or_cashflow_evaluations':0})
print(json.dumps({'passed':True,'M5_missing_days':391,'all_cost_applicable_M5_entries_blocked_each':23,'cliff_warnings':3,'parameter_robustness_demonstrated':False,'new_evaluations':0}))
