"""Seal outward sensitivity results, unchanged future plan and original account evidence."""
import ast,json,re,subprocess
from datetime import datetime
from common import *
rd=lambda p:json.loads(p.read_text())
P=ROOT/'research/experiments/20261031T174613Z'
assert not(R/'data_manifest.json').exists()
ctx,start,plan,rep=[rd(R/n) for n in ['context.json','startup.json','plan.json','report.json']]
old=rd(P/'data_manifest.json')
audit,source,feed,cv,fv=[rd(R/n) for n in ['verification.json','source_verification.json','feed_verification.json','candidate_verification.json','forward_verification.json']]
fr=rd(R/'forward_report.json');im=rd(R/'candidate_observation/input_manifest.json');state=rd(R/'candidate_observation/state.json')
future=P/'prospective_l4';fp=rd(future/'plan.json');fb=rd(future/'binding.json');fc=rd(future/'engineering_checks.json');fs=rd(R/'future_status_receipt.json')
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip()==str(ROOT)
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==start['base_commit']
assert any(len(x.split())>4 and x.split()[1]=='FLOCK' and x.split()[4]==str(start['branch_lock_broker_pid']) for x in Path('/proc/locks').read_text().splitlines())
phases=['initial','reserve_batch_0','reserve_batch_1','evaluate','audit','summary','exports','finish_batch_0','finish_batch_1','finish','forward','candidate','observer_status','review','gates','feed']
required={n+'_commands.json':rd(R/(n+'_commands.json')) for n in phases}
b=rd(R/'bootstrap_receipt.json');required['bootstrap_receipt.json']=[{**b,'exit_code':b['actual_exit_code']}]
for n in ['freeze_receipt.json','decision_check_receipt.json','grid_diagnostics_receipt.json','future_status_receipt.json','collect_evidence_receipt.json']:required[n]=[rd(R/n)]
assert all(z['exit_code']==0 for rows in required.values() for z in rows)
for n in ['primitive_verification.json','definition_check.json','verification.json','decision_verification.json','sensitivity_diagnostics.json','export_verification.json','visual_inspection.json','finish_verification.json','forward_verification.json','candidate_verification.json','risk_carry_verification.json','source_verification.json','feed_verification.json']:assert rd(R/n)['passed'],n
n=len(rep['configs']);passed=len(rep['summary']['passed']);rejected=len(rep['summary']['rejected'])
assert n==plan['expected_counts']['new_configs']==14 and passed==6 and rejected==8
assert sha(R/'report.json')==audit['report_sha256']==source['financial_report_sha256']==feed['financial_report_sha256']
assert sha(R/'plan.json')==rep['frozen_plan_sha256']==audit['plan_sha256']
assert audit['new_native_curves']==audit['new_parent_curves']==21 and audit['new_NAV_points']==22890546
assert audit['read_only_native_curves']==18 and audit['read_only_parent_hashes']==12 and audit['independent_new_policy_decisions']==7770 and audit['counts']['rejects']==0
batch=rd(R/'batch.json');obsbatch=rd(R/'forward_batch.json')+rd(R/'candidate_batch.json');newids=len(batch)+len(obsbatch);append_events=2*newids
assert newids==20 and len(obsbatch)==6 and append_events==40
assert source['new_finished_IDs']==newids and source['registry_append_only_events']==append_events and source['actual_reserve_receipts']==source['actual_finish_exit0_receipts']==n
previous_fv=rd(P/'forward_verification.json');previous_cv=rd(P/'candidate_verification.json')
assert fv['NAV_points_per_scene']==previous_fv['NAV_points_per_scene']+120 and fv['original_NAV_prefix']==previous_fv['NAV_points_per_scene'] and fv['cumulative_minutes']==previous_fv['cumulative_minutes']+120 and fv['new_daily_decisions']==fv['new_executions']==0
assert cv['cumulative_finished_candidate_observations']==previous_cv['cumulative_finished_candidate_observations']+3 and cv['prior_NAV_prefix']==previous_cv['NAV_points_per_scene']
assert cv['NAV_points_per_scene']==cv['prior_NAV_prefix']+cv['new_NAV_points_per_scene'] and cv['elapsed_minutes']==previous_cv['elapsed_minutes']+120
assert cv['new_funding_settlements']==cv['expected_from_actual_settlement_actions'] and cv['new_exact_causal_decisions']==cv['new_fills']==cv['new_risk_proxy_violations']==0
binding=rd(R/'code_binding_before_evaluation.json');assert binding['recorded_utc']<rep['evaluation_started_utc']
for path,h in {**binding['source_sha256'],**binding['immutable_source_sha256'],**ctx['account_hashes_before']}.items():assert sha(ROOT/path)==h,path
assert fc['passed'] and fc['engineering_only_no_financial_trials'] and fc['readonly_actual_baseline_decision_identity_checks']==2220 and fc['actual_future_accounts']==fc['actual_future_observations']==fc['new_backtests']==0
assert not(ROOT/'research/automation/l4h02_forward_latest.json').exists()
assert sha(future/'plan.json')==fb['plan_sha256']==fc['plan_sha256']==fs['plan_sha256']=='08e650a257ec9a0dbe27fe545f796a061a8538c05b8f9512821dc71a9cce3462'
assert sha(future/'binding.json')==fc['binding_sha256']==fs['binding_sha256']=='01177303b7999cef85b3bbb8a534ef5804ee79c9a83b533f3a110822801ff1eb'
for path,h in fb['code_and_source_sha256'].items():assert sha(ROOT/path)==h
s=fs['status'];assert s['status']=='waiting_for_planned_start' and not s['account_created'] and s['actual_observations_created']==s['network_requests']==s['filesystem_writes']==s['registry_writes']==0
assert datetime.fromisoformat(fp['frozen_at_utc'].replace('Z','+00:00'))<datetime.fromisoformat(rep['evaluation_started_utc'].replace('Z','+00:00'))<datetime.fromisoformat(fp['time_boundaries']['planned_start_utc'].replace('Z','+00:00'))
assert not fp['result_available'] and fp['actual_observations']==0 and not(R/'prospective_l4').exists()
for item in old['real_market_inputs']+old['source_annual_and_recent_inputs']:assert sha(ROOT/item['path'])==item['sha256'] and (ROOT/item['path']).stat().st_size==item['bytes']
records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl')
assert len(events)==ctx['registry_events']+append_events and len(records)==ctx['registry_ids']+newids
for row in batch:
 z=records[row['fingerprint']];rv=[e for e in events if e['fingerprint']==row['fingerprint'] and e['status']=='reserved']
 assert len(rv)==1 and rv[0]['recorded_at_utc']<rep['evaluation_started_utc'] and z['result_available'] and z['status']==rep['configs'][row['name']]['status'] and z['report_sha256']==sha(R/'report.json')
for key,ref in plan['read_only_references'].items():assert records[key]['status']==ref['status'] and records[key]['report_sha256']==ref['report_sha256']
attempts=rd(R/'candidate_transport_attempts.json');bad=[x for x in attempts if x['curl_exit_code'] or x['http_status']!=200]
assert sum(x['curl_exit_code']==0 and x['http_status']==200 for x in attempts)==len(im['provenance'])==8
rawpaths={ROOT/x['raw'] for x in attempts}|{ROOT/im['packet']}
raw_artifacts=[{'path':rel(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(rawpaths)]
for item in rd(R/'raw_evidence_index.json')['artifacts']:assert sha(ROOT/item['original_path'])==sha(ROOT/item['committed_copy'])==item['sha256'] and (ROOT/item['committed_copy']).stat().st_size==item['bytes']
allreceipts={p.name:rd(p) for p in R.glob('*_commands.json')};failed=[z for rows in allreceipts.values() for z in rows if z['exit_code']];assert not failed
put(R/'all_command_receipts.json',allreceipts)
forward_errors=[{'log':x['log'],'stderr':x['stderr'],'observed_curl_error_codes':re.findall(r'curl: \((\d+)\)',x['stderr'])} for x in rd(R/'forward_commands.json') if 'curl:' in x.get('stderr','')]
put(R/'failure_receipts.json',{'failed_pipeline_commands':failed,'candidate_failed_HTTP_attempts':bad,'forward_transport_error_messages':forward_errors,'exact_forward_HTTP_attempt_count_instrumented':False,'completed_financial_backtest_reruns':0,'completed_observation_reruns':0,'current_future_status_only_no_engineering_rerun':True})
ns=rd(R/'next_research_state.json');assert ns['original_single_S28']['books']==state['books'] and ns['original_single_S28']['NAV_points']==cv['NAV_points_per_scene'] and ns['original_single_S28']['cumulative_observation_IDs']==cv['cumulative_finished_candidate_observations']
assert ns['new_L4H02_forward']['plan']==rel(future/'plan.json') and ns['new_L4H02_forward']['plan_sha256']==sha(future/'plan.json')
counts=audit['counts'];qualified=[c for c in rep['configs'].values() if c['status']=='passed'];low=min(c['scenes']['3']['net_return_pct'] for c in qualified);high=max(c['scenes']['3']['net_return_pct'] for c in qualified);ddlo=min(c['scenes']['3']['max_drawdown_pct'] for c in qualified);ddhi=max(c['scenes']['3']['max_drawdown_pct'] for c in qualified)
append=['',f"封存核验：{n}完整新定义／{3*n}成本场景，{passed}父组合passed、{rejected}项rejected；另{len(obsbatch)}真实部分观察finish rejected但不取消原计划，合计{newids}新ID／{append_events}追加事件。读取{ctx['registry_events']}事件、{ctx['registry_ids']}ID及{len(ctx['prior_conclusions_read'])}份完整结论，初始16项实际证据齐全，{len(ctx['account_hashes_before'])}旧文件／{len(plan['read_only_references'])}来源资格与报告保持。",'',f"独立审计actualexit0：7770条新日决策、21新原生＋21新父共22890546完整净值点、18只读原生及12只读父NAV SHA；{counts['funding']}资金费、{counts['fills']}成交、{counts['margin_checks']}小时风险状态、{counts['metric_checks']}整体／月折指标及全部近期折，零拒单／负抵押／维护代理违规，14套资格独立复核。",'',f"6合格父的三倍成本累计收益{low:.6f}%至{high:.6f}%，整体DD{ddlo:.6f}%至{ddhi:.6f}%，每档均6/8正五日折、至少9/12正月折及局部严格近期比例100%。7新原生均未达到近期6/8；V15/C3.5父仅8/12正月折而淘汰，所有净正结果与淘汰证据均保存。完整原生及父网格各9/9正Sharpe，但相邻边描述性悬崖仍在，不称全域稳健或真实容量。",'','旧V10/C4.5父的原passed资格及历史报告／邻域原字段不重写；本轮单列外扩邻域9/9近期门槛合格、9/9三倍净正，且1/2/3成本的最高Sharpe均为内部旧V10/C4.5。旧三倍净7.175780%／DD3.658749%，未过滤L4/H2基线三倍6.150142%／DD3.812565%；全部新父收益均低于未过滤基线，部分回撤也更大，不能宣称过滤普遍优于基线或事后挑峰即独立验证。','',f"独立未来旧L4/H2计划继续引用{rel(future/'plan.json')}，{fp['time_boundaries']['planned_start_utc']}至{fp['time_boundaries']['planned_end_exclusive_utc']}，原5000/15000银行、500/4500预算、无波动过滤和全部规则／代码SHA保持。本轮仅原observer status actual0，waiting、0HTTP／文件／registry写入，未重跑工程、未新建／克隆账户或未来计划，0未来观察。",'',f"原SMA65续接{fv['original_NAV_prefix']}点＋120闭合分钟至{fv['NAV_points_per_scene']}点/{fv['cumulative_minutes']}分钟，29完整日，零新日决策/成交/费用。原singleS28保留{cv['prior_NAV_prefix']}点＋{cv['new_NAV_points_per_scene']}真实事件至{cv['NAV_points_per_scene']}点/{cv['elapsed_minutes']}分钟、累计{cv['cumulative_finished_candidate_observations']}观察ID；0新日决策/成交，{cv['new_funding_settlements']}实际新资金费记录，{cv['new_closed_hour_risk_checks']}小时维护检查0违规。新资金费数由实际packet／journal推导，16UTC已入账现金不重记，00+2ms和08UTC不重复；18UTC正持续风险栈及原q/entry/现金保持。原10000/10000 singleS28和SMA终止计划、Nov1UTC00:01下一日决策不变。",'',f"同锁内registry/snapshot/monitor及逐旧行字典检查通过：{feed['research_configs']}研究配置，旧{feed['historical_rows_identical']}行保持，{feed['paper_accounts']}账户/{feed['paper_observations']}真实报价观察，gzip{(ROOT/'research/monitor/configs.json.gz').stat().st_size}字节。完整账本、冻结规则、登记、失败响应及必要原始证据保留，仅清理本轮可重建中间文件，无网站重部署、重复定时器或真实订单。",'',f"main实际commit／非强制push／完整远端tree和所有必要blob、动态原候选完整观察链计数、publisher真实退出0及解锁证明在.git/automation_proofs/{R.name}.json；封存先于提交，不预写成功SHA。"]
with(R/'result.md').open('a') as f:f.write('\n'.join(append)+'\n')
for p in R.rglob('*.py'):ast.parse(p.read_text())
assert not any(p.name=='__pycache__' or p.suffix in ['.pyc','.npy','.tmp'] or 'checkpoint' in p.name for p in R.rglob('*'))
mutable={'research/automation/registry.jsonl','research/automation/candidate_forward_latest.json','research/monitor/latest.json','research/monitor/configs.json.gz'}
frozen={p:h for p,h in old['code_and_frozen_source_sha256'].items() if p not in mutable};frozen.update(binding['immutable_source_sha256']);frozen.update(fb['code_and_source_sha256'])
for ref in plan['read_only_references'].values():
 for key in ['spec','report','archive']:frozen[ref[key]]=ref[key+'_sha256']
for p,h in frozen.items():assert sha(ROOT/p)==h,p
artifacts={rel(p):sha(p) for p in sorted(R.rglob('*')) if p.is_file() and p.name!='data_manifest.json'}
m={'round':R.name,'recorded_at_utc':now(),'working_directory':str(ROOT),'branch':'main','base_commit':start['base_commit'],'branch_lock_broker_pid':start['branch_lock_broker_pid'],'initial_main_branch_verification':rd(R/'main_only_branch_check.json'),'frozen_plan_sha256':sha(R/'plan.json'),'finished_report_sha256':sha(R/'report.json'),'finished_forward_report_sha256':sha(R/'forward_report.json'),'finished_candidate_report_sha256':sha(R/'candidate_observation/report.json'),'real_market_inputs':old['real_market_inputs'],'source_annual_and_recent_inputs':old['source_annual_and_recent_inputs'],'forward_raw_responses':fr['provenance'],'observer_preflight_raw_responses':[],'candidate_raw_artifacts':raw_artifacts,'candidate_input_manifest':im,'prospective_readiness':{'actual_candidate_observations':cv['cumulative_finished_candidate_observations'],'new_actual_observation_IDs':3,'original_frozen_rules_unchanged':True,'current_cutoff_utc':cv['cutoff_utc']},'new_independent_future_plan':{'path':rel(future/'plan.json'),'sha256':sha(future/'plan.json'),'binding_sha256':sha(future/'binding.json'),'engineering_only_passed':True,'actual_accounts':0,'actual_observations':0,'start_utc':fp['time_boundaries']['planned_start_utc'],'status':'waiting_for_planned_start','current_round_status_only':True},'registry':{'main_sha256_before_reserve':ctx['main_registry_sha256_before_reserve'],'before_events':ctx['registry_events'],'before_IDs':ctx['registry_ids'],'append_only_events':append_events,'new_finished_IDs':newids,'financial_IDs':n,'observation_IDs':len(obsbatch)},'read_only_source_results':plan['read_only_references'],'code_and_frozen_source_sha256':frozen,'protected_inputs_sha256':ctx['account_hashes_before'],'shared_files':{p:{'sha256':sha(ROOT/p),'bytes':(ROOT/p).stat().st_size} for p in sorted(mutable)},'required_command_receipts':required,'all_command_receipts':allreceipts,'failure_facts':rd(R/'read_failures.json'),'new_actual_results':{'financial_configs':n,'candidate_configs':n,'new_native_models':7,'new_passive_parents':7,'new_benchmark_configs':0,'cost_scenes':3*n,'passed':passed,'rejected_candidates':rejected,'old_readonly_unique_results':len(plan['read_only_references']),'invalid_attempts_and_curves_retained':0,'failed_pipeline_commands':len(failed),'actual_HTTP_failures':len(bad)+sum(len(x['observed_curl_error_codes']) for x in forward_errors),'completed_native_or_parent_backtest_reruns':0,'completed_observation_reruns':0,'all_old_registry_qualifications_unchanged':True,'actual_native_quantity_and_model_impact_validated':True,'true_exchange_execution_or_capacity_validated':False,'independent_future_validated':False},'artifacts':artifacts}
put(R/'data_manifest.json',m)
print(json.dumps({'sealed':True,'artifacts':len(artifacts),'protected_old_files':len(ctx['account_hashes_before']),'financial_configs':n,'new_finished_IDs':newids,'append_only_events':append_events,'report_sha256':sha(R/'report.json'),'manifest_sha256':sha(R/'data_manifest.json')}),flush=True)
