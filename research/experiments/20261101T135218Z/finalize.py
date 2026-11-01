"""Seal only actual results, immutable source hashes and verified account continuations."""
import ast,gzip,json,re,subprocess
from datetime import datetime
from common import *
rd=lambda p:json.loads(p.read_text());P=ROOT/'research/experiments/20261101T115248Z'
assert not(R/'data_manifest.json').exists()
ctx,start,plan,rep=[rd(R/n) for n in ['context.json','startup.json','plan.json','report.json']];old=rd(P/'data_manifest.json')
audit,source,feed,cv,fv,lv=[rd(R/n) for n in ['verification.json','source_verification.json','feed_verification.json','candidate_verification.json','forward_verification.json','l4h02_verification.json']]
fr=rd(R/'forward_report.json');im=rd(R/'candidate_observation/input_manifest.json');state=rd(R/'candidate_observation/state.json');lim=rd(R/'l4h02_observation/input_manifest.json');ls=rd(R/'l4h02_observation/state.json')
future=ROOT/'research/experiments/20261031T174613Z/prospective_l4';fp=rd(future/'plan.json');fb=rd(future/'binding.json');fc=rd(future/'engineering_checks.json');ip=rd(R/'l4h02_resume_plan.json')
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip()==str(ROOT)
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==start['base_commit']
assert any(len(x.split())>4 and x.split()[1]=='FLOCK' and x.split()[4]==str(start['branch_lock_broker_pid']) for x in Path('/proc/locks').read_text().splitlines())
phases=['initial','reserve_batch_0','reserve_batch_1','evaluate','audit','summary','exports','finish_batch_0','finish_batch_1','finish','forward','candidate','l4h02','observer_status','review','gates','feed']
required={n+'_commands.json':rd(R/(n+'_commands.json')) for n in phases}
b=rd(R/'bootstrap_receipt.json');required['bootstrap_receipt.json']=[{**b,'exit_code':b['actual_exit_code']}]
for n in ['freeze_receipt.json','decision_check_receipt.json','grid_diagnostics_receipt.json','collect_evidence_receipt.json','engineering_scope_check.json']:required[n]=[rd(R/n)]
assert all(z['exit_code']==0 for rows in required.values() for z in rows)
for n in ['primitive_verification.json','definition_check.json','verification.json','decision_verification.json','sensitivity_diagnostics.json','export_verification.json','visual_inspection.json','finish_verification.json','forward_verification.json','candidate_verification.json','source_verification.json','feed_verification.json','l4h02_verification.json']:assert rd(R/n)['passed'],n
n=len(rep['configs']);passed=len(rep['summary']['passed']);assert n==plan['expected_counts']['new_configs']==12 and passed==2 and len(rep['summary']['candidate_rejected'])==4 and len(rep['summary']['benchmark_rejected'])==0
assert sum(c['role']=='component' for c in rep['configs'].values())==6 and sum(c['status']=='passed' for c in rep['configs'].values())==2
assert sha(R/'report.json')==audit['report_sha256']==source['financial_report_sha256']==feed['financial_report_sha256']
assert sha(R/'plan.json')==rep['frozen_plan_sha256']==audit['plan_sha256']
assert audit['new_native_curves']==18 and audit['new_parent_curves']==18 and audit['new_NAV_points']==19620468
assert audit['read_only_native_curves']==18 and audit['read_only_parent_hashes']==12 and audit['independent_new_policy_decisions']==6660
assert audit['counts']=={'funding':39960,'fills':1656,'rejects':0,'metric_checks':756,'margin_checks':136152}
batch=rd(R/'batch.json');obsbatch=rd(R/'forward_batch.json')+rd(R/'candidate_batch.json')+rd(R/'l4h02_batch.json');newids=len(batch)+len(obsbatch);append_events=2*newids;assert newids==21 and len(obsbatch)==9 and append_events==42
assert source['new_finished_IDs']==newids and source['registry_append_only_events']==append_events and source['actual_reserve_receipts']==source['actual_finish_exit0_receipts']==n
prevfv,prevcv,prevlv=[rd(P/x) for x in ['forward_verification.json','candidate_verification.json','l4h02_verification.json']]
assert fv['NAV_points_per_scene']==prevfv['NAV_points_per_scene']+120==43981 and fv['original_NAV_prefix']==prevfv['NAV_points_per_scene']==43861 and fv['cumulative_minutes']==prevfv['cumulative_minutes']+120==43949
assert fv['new_daily_decisions']==fv['new_reference_points']==fv['new_executions']==0 and fv['complete_days']==30
assert cv['cumulative_finished_candidate_observations']==prevcv['cumulative_finished_candidate_observations']+3==201 and cv['prior_NAV_prefix']==prevcv['NAV_points_per_scene']
assert cv['NAV_points_per_scene']==cv['prior_NAV_prefix']+cv['new_NAV_points_per_scene'] and cv['elapsed_minutes']==prevcv['elapsed_minutes']+120==7949
assert cv['new_funding_settlements']==cv['expected_from_actual_settlement_actions'] and cv['new_exact_causal_decisions']==cv['new_fills']==cv['new_rejected_orders']==cv['new_risk_proxy_violations']==0
assert cv['daily_context_bars']=={'BTC':38,'ETH':38} and cv['daily_NAV_boundaries']==6 and not cv['whole180day_qualified']
assert lv['passed'] and not lv['first_actual_window'] and lv['actual_observation_configs']==3 and lv['elapsed_minutes']==prevlv['elapsed_minutes']+120==849 and lv['NAV_points_per_scene']==prevlv['NAV_points_per_scene']+lv['new_NAV_points_per_scene']
assert lv['cumulative_finished_l4h02_observations']==24 and lv['new_exact_causal_decisions']==lv['new_fills']==lv['new_risk_proxy_violations']==0 and lv['new_funding_settlements']==lv['expected_from_actual_settlement_actions'] and not lv['whole180day_qualified']
for stem,proof in [('candidate',cv),('l4h02',lv)]:
 w=R/(stem+'_observation');pointer=ROOT/'research/automation'/(stem+'_forward_latest.json');assert sha(w/'report.json')==proof['report_sha256'] and sha(w/'state.json')==proof['state_sha256'] and sha(pointer)==proof['pointer_sha256']
binding=rd(R/'code_binding_before_evaluation.json');assert binding['recorded_utc']<rep['evaluation_started_utc']
for path,h in {**binding['source_sha256'],**binding['immutable_source_sha256'],**ctx['account_hashes_before']}.items():assert sha(ROOT/path)==h,path
assert fc['passed'] and fc['engineering_only_no_financial_trials']
assert sha(future/'plan.json')==fb['plan_sha256']==fc['plan_sha256']==lv['plan_sha256']=='08e650a257ec9a0dbe27fe545f796a061a8538c05b8f9512821dc71a9cce3462'
assert sha(future/'binding.json')==fc['binding_sha256']=='01177303b7999cef85b3bbb8a534ef5804ee79c9a83b533f3a110822801ff1eb'
for path,h in {**fb['code_and_source_sha256'],**ip['source_sha256']}.items():assert sha(ROOT/path)==h,path
assert ip['cutoff_ns']==ls['cutoff_ns']==1793542200000000000 and ip['previous_pointer']['cutoff_ns']==1793535000000000000 and sha(R/'l4h02_observation/previous_pointer.json')==ip['previous_pointer_sha256']
assert datetime.fromisoformat(ip['recorded_utc'].replace('Z','+00:00'))<datetime.fromisoformat(lim['provenance'][0]['started_utc'].replace('Z','+00:00'))
closure=rd(R/'l4h02_reference_closure.json');assert closure['actual_launch_ns']>=closure['required_closed_reference_after_ns']==ip['cutoff_ns']+MIN and closure['future_window_not_evaluated_before_reference_closed']
l4raw=rd(R/'l4h02_raw_manifest.json')['artifacts']
for item in l4raw:assert sha(ROOT/item['path'])==item['sha256'] and (ROOT/item['path']).stat().st_size==item['bytes']
for item in old['real_market_inputs']+old['source_annual_and_recent_inputs']:assert sha(ROOT/item['path'])==item['sha256'] and (ROOT/item['path']).stat().st_size==item['bytes']
records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');assert len(events)==ctx['registry_events']+append_events and len(records)==ctx['registry_ids']+newids
for row in batch:
 z=records[row['fingerprint']];rv=[e for e in events if e['fingerprint']==row['fingerprint'] and e['status']=='reserved'];assert len(rv)==1 and rv[0]['recorded_at_utc']<rep['evaluation_started_utc'] and z['result_available'] and z['status']==rep['configs'][row['name']]['status'] and z['report_sha256']==sha(R/'report.json')
for key,ref in plan['read_only_references'].items():assert records[key]['status']==ref['status'] and records[key]['report_sha256']==ref['report_sha256']
attempts=rd(R/'candidate_transport_attempts.json');bad=[x for x in attempts if x['curl_exit_code'] or x['http_status']!=200];bad_future=[x for x in lim['provenance'] if x.get('curl_exit_code') or x.get('http_status')!=200]
assert sum(x['curl_exit_code']==0 and x['http_status']==200 for x in attempts)==len(im['provenance'])==8
rawpaths={ROOT/x['raw'] for x in attempts}|{ROOT/im['packet']};raw_artifacts=[{'path':rel(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(rawpaths)]
for item in rd(R/'raw_evidence_index.json')['artifacts']:assert sha(ROOT/item['original_path'])==sha(ROOT/item['committed_copy'])==item['sha256'] and (ROOT/item['committed_copy']).stat().st_size==item['bytes']
allreceipts={p.name:rd(p) for p in R.glob('*_commands.json')};failed=[z for rows in allreceipts.values() for z in rows if z['exit_code']];assert not failed
put(R/'all_command_receipts.json',allreceipts)
forward_errors=[{'log':x['log'],'stderr':x['stderr'],'observed_curl_error_codes':re.findall(r'curl: \((\d+)\)',x['stderr'])} for x in rd(R/'forward_commands.json') if 'curl:' in x.get('stderr','')]
httpfail=len(bad)+len(bad_future)+sum(len(x['observed_curl_error_codes']) for x in forward_errors)
put(R/'failure_receipts.json',{'failed_pipeline_commands':failed,'candidate_failed_HTTP_attempts':bad,'L4_failed_transport_attempts':bad_future,'forward_transport_error_messages':forward_errors,'exact_forward_HTTP_attempt_count_instrumented':False,'completed_financial_backtest_reruns':0,'completed_observation_reruns':0,'recorded_command_failures':rd(R/'read_failures.json')['facts']})
cleanup=rd(R/'cleanup_verification.json');assert cleanup['passed'] and cleanup['actual_financial_results_removed']==cleanup['account_ledger_files_removed']==0 and not cleanup['remaining_rebuild_intermediates']
ns=rd(R/'next_research_state.json');assert ns['original_single_S28']['books']==state['books'] and ns['original_single_S28']['NAV_points']==cv['NAV_points_per_scene'] and ns['original_single_S28']['cumulative_observation_IDs']==201
assert ns['new_L4H02_forward']['actual_observations']==24 and ns['new_L4H02_forward']['books']==ls['books'] and ns['new_L4H02_forward']['risk']==ls['risk'] and ns['new_L4H02_forward']['elapsed_minutes']==849
assert ns['research']['new_configurations']==12 and ns['research']['new_candidates']==6 and ns['research']['new_native_evaluations']==6
candidate=[c for c in rep['configs'].values() if c['role']=='candidate'];accepted=[c for c in candidate if c['status']=='passed'];denied=[c for c in candidate if c['status']=='rejected'];components=[c for c in rep['configs'].values() if c['scope']=='native']
assert len(candidate)==6 and len(accepted)==2 and len(denied)==4 and len(components)==6 and all(c['status']=='rejected' for c in components)
assert {(c['L'],c['H']) for c in accepted}=={(3,.02),(3,.025)} and all(c['recent40_positive_5d_folds_by_cost']=={'1':6,'2':6,'3':6} for c in accepted)
assert all('recent40_six_of_eight_positive5d_all_costs' in c['failed_criteria'] and 'local_recent6of8_allcost_gte60pct' in c['failed_criteria'] for c in denied)
assert cv['new_funding_settlements']==cv['expected_from_actual_settlement_actions']==lv['new_funding_settlements']==lv['expected_from_actual_settlement_actions']==0 and cv['new_closed_hour_risk_checks']==lv['new_closed_hour_risk_checks']==6
strict=lambda c:all(s['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in s['recent40']['folds'])>=6 for s in c['scenes'].values());assert sum(strict(c) for c in rep['all_current_grid'].values())==4 and sum(strict(c) for c in rep['all_current_native_grid'].values())==0
center=next(c for c in rep['all_current_grid'].values() if c['L']==4 and c['H']==.025);assert center['readonly'] and center['status']=='passed' and center['current_grid_diagnostic_sensitivity']['local_strict_recent_fraction']==4/9
low=min(c['scenes']['3']['net_return_pct'] for c in accepted);high=max(c['scenes']['3']['net_return_pct'] for c in accepted);ddlo=min(c['scenes']['3']['max_drawdown_pct'] for c in accepted);ddhi=max(c['scenes']['3']['max_drawdown_pct'] for c in accepted)
append=['',f"封存结论：6新组合候选2项历史通过/4项淘汰。通过项为ETH L3交叉H2%/2.5%，固定BTC3750/N375与ETH15000/N4500、原权重1/1；3倍成本370日净收益{low:.6f}%至{high:.6f}%，完整DD{ddlo:.6f}%至{ddhi:.6f}%，每档近期6/8正5日折，局部严格近期支持100%或2/3，其他原门槛也满足。L3/H3与全部L5父候选因近期折数及局部近期支持不足淘汰，L5/H2.5和H3还未满足每档近期净正。",'',
'六个新原生ETH配置全期净正但近期仅1至4个3倍正5日折，全部单币资格失败，不能把父组合资格当单币资格。原生和父各完整3×3面每档9/9正Sharpe，但严格近期原生0/9、父4/9；旧L4/H2.5仍是各成本内部Sharpe峰值，其本轮父全邻域严格近期支持只有4/9。旧canonical passed按原批次语义保持，不代表通过当前更宽L/H邻域。两面各档描述性相邻悬崖都触发；正收益/局部通过不等于广域稳健、未触碰最终测试或稳定实盘盈利。', '',
f"12个新定义/36成本场景全部实际reserve后计算并逐项finish；另9观察/27场景完成，合计21新ID/42追加事件。6旧L4格点、旧匹配持有父及来源共10唯一旧定义只读，{len(ctx['account_hashes_before'])}旧保护文件字节保持；无新持有控制计算、无旧报告或资格改写。登记事件总数/ID不是独立金融试验数，规范化非观察研究定义为{ctx['canonical_research_definitions_excluding_observations']}，其中仍可能有无结果记录；多重选择偏差未由简单局部比例消除。",'',
f"独立审计actualexit0：18新ETH原生成本曲线和18新父曲线，共19620468完整NAV点；18旧原生曲线与12旧父哈希只读。6660次新决策用Fraction独立重建；39960资金费、1656成交、756整体/月指标与136152小时风险状态用Decimal/独立指标核验，零拒单/负抵押/维护代理违规。核对所有新q/LOT/信号可得时间、成本和funding/全NAV/逐折DD，不调用simulate/decide/trade进行金融重跑。仍无真实TCA/L2、完整历史抵押阶梯或逐tick清算/容量证明。",'',
f"原SMA65续10:30至12:30：{fv['original_NAV_prefix']}旧NAV+120={fv['NAV_points_per_scene']}点，{fv['cumulative_minutes']}分钟/30天，无新日决策/成交；原Float现金/q/desired/trades与所有NAV前缀保持，nextdailyNov2UTC00:01。原singleS28同窗保留10000/10000,N1000/3000,ETHL3零退出缓冲原规则：{cv['prior_NAV_prefix']}旧点+{cv['new_NAV_points_per_scene']}={cv['NAV_points_per_scene']}点，7949分钟/201ID/67窗。本窗0新日决策/成交/资金费，6小时风险检查/0违规，08资金费不重复入账。该原S28不等于本轮带退出缓冲和波动过滤的新L3研究策略。",'',
f"独立未过滤L4/H2保留5000/15000,N500/4500,S28zeroexit，从12:10续14:10，在14:11参考分钟闭合后才采集：{lv['prior_NAV_prefix']}旧NAV+{lv['new_NAV_points_per_scene']}={lv['NAV_points_per_scene']}点，849分钟/24ID/8窗；0新日决策/成交/资金费，6小时风险检查/0违规。三账户原plan/core/observer/binding SHA、资金/q/费用/risk和长期终止计划保持，部分rejected不取消各自180日计划，不注入本轮L3/L5或过滤规则。下一L4建议14:10至16:10会跨16资金费，须16:11后按真实精确纳秒/rate/mark/当时q入账一次并保留前后风险状态；本轮未提前计算该未来窗口。",'',
f"只读快照在同main锁内，registry/snapshot/monitor及所有旧行逐字典门禁实际通过：{feed['research_configs']}研究配置、旧{feed['historical_rows_identical']}行完全相等、{feed['paper_accounts']}报价账户/{feed['paper_observations']}既有真实观察，gzip{(ROOT/'research/monitor/configs.json.gz').stat().st_size}字节，沿用5MB预算。不改监控代码/预算/冻结规则/本金/持仓，不重新部署网站或新建定时器，不下真实订单，不把延迟shadow当十策略真实报价成交。",'',
f"实际HTTP失败{httpfail}次，所有真实尝试/stderr/原始响应和回执完整保存；一次发布辅助只读检查因子串匹配过宽误报，AST依赖核验恢复exit0并保留原失败，无模型/报告/账户/判据改动；已完成金融模型/观察0重跑。核验后只清理可重建语义元数据{cleanup['removed_bytes']}字节，原SHA/行数/基准版本保留，金融结果/账户账本删除0，npy/pyc/tmp/checkpoint残留0。保留11CSV、全部原生逐笔/资金费/状态段与父档、完整SHA、当前轻量HTTP/packet和下轮必要状态。main非强制push、完整远端tree/必要blob、201ID原S28链/24ID独立L4链、实际publisher终态和解锁证明在.git/automation_proofs/{R.name}.json；封存不预写commit SHA。"]
with(R/'result.md').open('a') as f:f.write('\n'.join(append)+'\n')
for p in R.rglob('*.py'):ast.parse(p.read_text())
assert not any(p.name=='__pycache__' or p.suffix in ['.pyc','.npy','.tmp'] or 'checkpoint' in p.name for p in R.rglob('*'))
mutable={'research/automation/registry.jsonl','research/automation/candidate_forward_latest.json','research/automation/l4h02_forward_latest.json','research/monitor/latest.json','research/monitor/configs.json.gz'}
frozen={p:h for p,h in old['code_and_frozen_source_sha256'].items() if p not in mutable};frozen.update(binding['immutable_source_sha256']);frozen.update(fb['code_and_source_sha256']);frozen.update(ip['source_sha256'])
for ref in plan['read_only_references'].values():
 for key in ['spec','report','archive']:frozen[ref[key]]=ref[key+'_sha256']
for gp in ['checks/monitor_snapshot.py','research/monitor/README.md']:
 assert sha(ROOT/gp)==old['code_and_frozen_source_sha256'][gp];frozen[gp]=sha(ROOT/gp)
for p,h in frozen.items():assert sha(ROOT/p)==h,p
artifacts={rel(p):sha(p) for p in sorted(R.rglob('*')) if p.is_file() and p.name!='data_manifest.json'}
m={'round':R.name,'recorded_at_utc':now(),'working_directory':str(ROOT),'branch':'main','base_commit':start['base_commit'],'branch_lock_broker_pid':start['branch_lock_broker_pid'],'initial_main_branch_verification':rd(R/'main_only_branch_check.json'),'frozen_plan_sha256':sha(R/'plan.json'),'finished_report_sha256':sha(R/'report.json'),'finished_forward_report_sha256':sha(R/'forward_report.json'),'finished_candidate_report_sha256':sha(R/'candidate_observation/report.json'),'real_market_inputs':old['real_market_inputs'],'source_annual_and_recent_inputs':old['source_annual_and_recent_inputs'],'forward_raw_responses':fr['provenance'],'observer_preflight_raw_responses':[],'candidate_raw_artifacts':raw_artifacts,'candidate_input_manifest':im,'l4h02_input_manifest':lim,'l4h02_raw_artifacts':l4raw,'prospective_readiness':{'actual_candidate_observations':cv['cumulative_finished_candidate_observations'],'new_actual_observation_IDs':3,'original_frozen_rules_unchanged':True,'current_cutoff_utc':cv['cutoff_utc']},'new_independent_future_plan':{'path':rel(future/'plan.json'),'sha256':sha(future/'plan.json'),'binding_sha256':sha(future/'binding.json'),'engineering_only_passed':True,'actual_accounts':1,'actual_observations':lv['cumulative_finished_l4h02_observations'],'current_window_observation_IDs':3,'actual_cutoff_ns':ls['cutoff_ns'],'actual_cutoff_utc':lv['cutoff_utc'],'actual_verification_sha256':sha(R/'l4h02_verification.json'),'whole180day_qualified':False,'start_utc':fp['time_boundaries']['planned_start_utc'],'status':'running_partial_delayed_observation'},'registry':{'main_sha256_before_reserve':ctx['main_registry_sha256_before_reserve'],'before_events':ctx['registry_events'],'before_IDs':ctx['registry_ids'],'append_only_events':append_events,'new_finished_IDs':newids,'financial_IDs':n,'observation_IDs':len(obsbatch)},'read_only_source_results':plan['read_only_references'],'code_and_frozen_source_sha256':frozen,'protected_inputs_sha256':ctx['account_hashes_before'],'shared_files':{p:{'sha256':sha(ROOT/p),'bytes':(ROOT/p).stat().st_size} for p in sorted(mutable)},'required_command_receipts':required,'all_command_receipts':allreceipts,'failure_facts':rd(R/'read_failures.json'),'new_actual_results':{'financial_configs':n,'candidate_configs':6,'new_source_components':6,'new_native_models':6,'new_passive_parents':6,'new_benchmark_configs':0,'cost_scenes':3*n,'passed':passed,'rejected_candidates':4,'old_readonly_unique_results':len(plan['read_only_references']),'invalid_attempts_and_curves_retained':0,'failed_pipeline_commands':len(failed),'pre_reservation_engineering_failures':0,'report_scope_annotations':0,'pre_publication_helper_failures':1,'repaired_readonly_audit_failures':0,'actual_HTTP_failures':httpfail,'completed_native_or_parent_backtest_reruns':0,'completed_observation_reruns':0,'all_old_registry_qualifications_unchanged':True,'actual_native_quantity_and_model_impact_validated':True,'true_exchange_execution_or_capacity_validated':False,'independent_future_validated':False,'new_independent_future_observation_IDs':3,'new_independent_future_elapsed_minutes':lv['elapsed_minutes']},'artifacts':artifacts}
put(R/'data_manifest.json',m)
print(json.dumps({'sealed':True,'artifacts':len(artifacts),'protected_old_files':len(ctx['account_hashes_before']),'financial_configs':n,'new_finished_IDs':newids,'append_only_events':append_events,'report_sha256':sha(R/'report.json'),'manifest_sha256':sha(R/'data_manifest.json')}),flush=True)
