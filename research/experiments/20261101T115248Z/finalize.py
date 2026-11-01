"""Seal only actual results, immutable source hashes and verified account continuations."""
import ast,gzip,json,re,subprocess
from datetime import datetime
from common import *
rd=lambda p:json.loads(p.read_text());P=ROOT/'research/experiments/20261101T095117Z'
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
for n in ['freeze_receipt.json','decision_check_receipt.json','grid_diagnostics_receipt.json','collect_evidence_receipt.json','scope_annotation_receipt.json']:required[n]=[rd(R/n)]
assert all(z['exit_code']==0 for rows in required.values() for z in rows)
for n in ['primitive_verification.json','definition_check.json','verification.json','decision_verification.json','sensitivity_diagnostics.json','export_verification.json','visual_inspection.json','finish_verification.json','forward_verification.json','candidate_verification.json','source_verification.json','feed_verification.json','l4h02_verification.json']:assert rd(R/n)['passed'],n
n=len(rep['configs']);passed=len(rep['summary']['passed']);assert n==plan['expected_counts']['new_configs']==12 and passed==4 and len(rep['summary']['candidate_rejected'])==2 and len(rep['summary']['benchmark_rejected'])==4
assert sum(c['role']=='component' for c in rep['configs'].values())==2 and sum(c['status']=='passed' for c in rep['configs'].values())==4
assert sha(R/'report.json')==audit['report_sha256']==source['financial_report_sha256']==feed['financial_report_sha256']
assert sha(R/'plan.json')==rep['frozen_plan_sha256']==audit['plan_sha256']
assert audit['new_native_curves']==12 and audit['new_parent_curves']==24 and audit['new_NAV_points']==19620468
assert audit['read_only_native_curves']==18 and audit['read_only_parent_hashes']==12 and audit['independent_new_policy_decisions']==4440
assert audit['counts']=={'funding':33300,'fills':840,'rejects':0,'metric_checks':756,'margin_checks':214764}
batch=rd(R/'batch.json');obsbatch=rd(R/'forward_batch.json')+rd(R/'candidate_batch.json')+rd(R/'l4h02_batch.json');newids=len(batch)+len(obsbatch);append_events=2*newids;assert newids==21 and len(obsbatch)==9 and append_events==42
assert source['new_finished_IDs']==newids and source['registry_append_only_events']==append_events and source['actual_reserve_receipts']==source['actual_finish_exit0_receipts']==n
prevfv,prevcv,prevlv=[rd(P/x) for x in ['forward_verification.json','candidate_verification.json','l4h02_verification.json']]
assert fv['NAV_points_per_scene']==prevfv['NAV_points_per_scene']+120==43861 and fv['original_NAV_prefix']==prevfv['NAV_points_per_scene']==43741 and fv['cumulative_minutes']==prevfv['cumulative_minutes']+120==43829
assert fv['new_daily_decisions']==fv['new_reference_points']==fv['new_executions']==0 and fv['complete_days']==30
assert cv['cumulative_finished_candidate_observations']==prevcv['cumulative_finished_candidate_observations']+3==198 and cv['prior_NAV_prefix']==prevcv['NAV_points_per_scene']
assert cv['NAV_points_per_scene']==cv['prior_NAV_prefix']+cv['new_NAV_points_per_scene'] and cv['elapsed_minutes']==prevcv['elapsed_minutes']+120==7829
assert cv['new_funding_settlements']==cv['expected_from_actual_settlement_actions'] and cv['new_exact_causal_decisions']==cv['new_fills']==cv['new_rejected_orders']==cv['new_risk_proxy_violations']==0
assert cv['daily_context_bars']=={'BTC':38,'ETH':38} and cv['daily_NAV_boundaries']==6 and not cv['whole180day_qualified']
assert lv['passed'] and not lv['first_actual_window'] and lv['actual_observation_configs']==3 and lv['elapsed_minutes']==prevlv['elapsed_minutes']+120==729 and lv['NAV_points_per_scene']==prevlv['NAV_points_per_scene']+lv['new_NAV_points_per_scene']
assert lv['cumulative_finished_l4h02_observations']==21 and lv['new_exact_causal_decisions']==lv['new_fills']==lv['new_risk_proxy_violations']==0 and lv['new_funding_settlements']==lv['expected_from_actual_settlement_actions'] and not lv['whole180day_qualified']
for stem,proof in [('candidate',cv),('l4h02',lv)]:
 w=R/(stem+'_observation');pointer=ROOT/'research/automation'/(stem+'_forward_latest.json');assert sha(w/'report.json')==proof['report_sha256'] and sha(w/'state.json')==proof['state_sha256'] and sha(pointer)==proof['pointer_sha256']
binding=rd(R/'code_binding_before_evaluation.json');assert binding['recorded_utc']<rep['evaluation_started_utc']
for path,h in {**binding['source_sha256'],**binding['immutable_source_sha256'],**ctx['account_hashes_before']}.items():assert sha(ROOT/path)==h,path
assert fc['passed'] and fc['engineering_only_no_financial_trials']
assert sha(future/'plan.json')==fb['plan_sha256']==fc['plan_sha256']==lv['plan_sha256']=='08e650a257ec9a0dbe27fe545f796a061a8538c05b8f9512821dc71a9cce3462'
assert sha(future/'binding.json')==fc['binding_sha256']=='01177303b7999cef85b3bbb8a534ef5804ee79c9a83b533f3a110822801ff1eb'
for path,h in {**fb['code_and_source_sha256'],**ip['source_sha256']}.items():assert sha(ROOT/path)==h,path
assert ip['cutoff_ns']==ls['cutoff_ns']==1793535000000000000 and ip['previous_pointer']['cutoff_ns']==1793527800000000000 and sha(R/'l4h02_observation/previous_pointer.json')==ip['previous_pointer_sha256']
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
ns=rd(R/'next_research_state.json');assert ns['original_single_S28']['books']==state['books'] and ns['original_single_S28']['NAV_points']==cv['NAV_points_per_scene'] and ns['original_single_S28']['cumulative_observation_IDs']==198
assert ns['new_L4H02_forward']['actual_observations']==21 and ns['new_L4H02_forward']['books']==ls['books'] and ns['new_L4H02_forward']['risk']==ls['risk'] and ns['new_L4H02_forward']['elapsed_minutes']==729
assert ns['research']['new_configurations']==12 and ns['research']['new_candidates']==6 and ns['research']['new_native_evaluations']==4
ann=rd(R/'scope_annotation.json');assert ann['passed'] and ann['financial_or_observation_reruns']==0 and ann['corrected_report_sha256']==sha(R/'report.json')
original_raw=gzip.decompress((ROOT/ann['original_report_compressed']).read_bytes());original=json.loads(original_raw);import hashlib
assert hashlib.sha256(original_raw).hexdigest()==ann['original_report_sha256'] and sha(ROOT/ann['original_report_compressed'])==ann['original_report_compressed_sha256']
assert {k:v for k,v in original.items() if k!='execution_scope'}=={k:v for k,v in rep.items() if k!='execution_scope'} and original['execution_scope']==ann['before'] and rep['execution_scope']==ann['after']
candidate=[c for c in rep['configs'].values() if c['role']=='candidate'];accepted=[c for c in candidate if c['status']=='passed'];denied=[c for c in candidate if c['status']=='rejected'];components=[c for c in rep['configs'].values() if c['role']=='component'];controls=[c for c in rep['configs'].values() if c['role'].startswith('benchmark')]
assert len(candidate)==6 and len(accepted)==4 and len(denied)==2 and len(components)==2 and len(controls)==4
assert {(c['BTC_capital_usdt'],c['H']) for c in accepted}=={(C,H) for C in [3125,4375] for H in [.02,.025]}
assert all(c['H']==.03 and 'recent40_six_of_eight_positive5d_all_costs' in c['failed_criteria'] and 'local_recent6of8_allcost_gte60pct' in c['failed_criteria'] for c in denied)
assert all(c['recent40_positive_5d_folds_by_cost']['3']==5 for c in denied) and all(c['recent40_positive_5d_folds_by_cost']=={'1':6,'2':6,'3':6} for c in accepted)
assert cv['new_funding_settlements']==cv['expected_from_actual_settlement_actions']==lv['new_funding_settlements']==lv['expected_from_actual_settlement_actions']==0
assert cv['new_closed_hour_risk_checks']==9 and lv['new_closed_hour_risk_checks']==6
strict=lambda c:all(s['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in s['recent40']['folds'])>=6 for s in c['scenes'].values());assert sum(strict(c) for c in rep['all_current_grid'].values())==6
center=next(c for c in rep['all_current_grid'].values() if c['BTC_capital_usdt']==3750 and c['H']==.025);assert center['readonly'] and center['status']=='passed' and center['current_grid_diagnostic_sensitivity']['local_strict_recent_fraction']==6/9
low=min(c['scenes']['3']['net_return_pct'] for c in accepted);high=max(c['scenes']['3']['net_return_pct'] for c in accepted);ddlo=min(c['scenes']['3']['max_drawdown_pct'] for c in accepted);ddhi=max(c['scenes']['3']['max_drawdown_pct'] for c in accepted)
append=['',f"封存结论：6个新父候选4项历史门槛通过、2项淘汰。通过为BTC3125/4375银行各自交叉ETH H2%/2.5%，三倍成本370日净收益{low:.6f}%至{high:.6f}%，完整DD{ddlo:.6f}%至{ddhi:.6f}%。各通过项每档近期6/8正5天折、局部严格近期支持至少2/3，其余原冻结门槛均满足。H3%的两新候选近期仅5/8，局部严格近期支持50%，按原标准淘汰。",'',
'两个新BTC原生动量组件单独近期4/8和局部近期失败，不能把组合资格当单币资格；4个常多控制实际负收益单列保留，非策略候选。完整12定义/36场景、9观察/27场景均成功reserve后计算并finish，共21新ID/42追加事件。', '',
f"当前更近的3×3资金/H邻域9点每档全年收益/Sharpe全正，严格近期6/9；最大Sharpe仍在旧3750/H2.5内部点，旧canonical资格/报告字节保持。所有成本档的描述性相邻悬崖仍触发，提示对ETH阈值的依赖。这是由既往研究启发的窄开发邻域，不覆盖先前BTC2500的失败区，不能称广域稳健、独立未触碰最终测试或稳定实盘盈利。",'',
f"独立审计actualexit0：12新原生、24新父成本曲线，共19620468完整NAV点；18旧原生曲线和12旧父NAV哈希只读。4440次独立新原生决策、33300资金费、840成交、756整体/月指标、214764小时风险检查，无拒单/负抵押/维护代理违规。10个唯一旧来源及{len(ctx['account_hashes_before'])}个旧保护文件字节保持。实际LOT数量、规模冲击和成本完整验证，但无真实TCA/盘口/完整清算档位或容量证明。",'',
f"原SMA65续08:30至10:30：{fv['original_NAV_prefix']}旧NAV+120={fv['NAV_points_per_scene']}点，{fv['cumulative_minutes']}分钟/30天，0新日决策/成交；完整Float现金/q/desired/trades与所有旧NAV前缀保持。原singleS28同窗保留10000/10000,N1000/3000,ETHL3：{cv['prior_NAV_prefix']}旧点+{cv['new_NAV_points_per_scene']}={cv['NAV_points_per_scene']}点，7829分钟/198ID/66窗。本窗无新日决策/成交/资金费；9次小时风险检查包括08资金费前后正时长现金状态，0违规，08资金费不重复记账。",'',
f"独立未过滤L4/H2保留5000/15000,N500/4500,S28zeroexit，10:10续12:10，仅12:11参考闭合后采集：{lv['prior_NAV_prefix']}旧NAV+{lv['new_NAV_points_per_scene']}={lv['NAV_points_per_scene']}点，729分钟/21ID/7窗。本窗0新日决策/成交/资金费，6次小时风险检查/0违规；独立pointer/book/risk和累计链不与原S28混用。三账户都未成熟180天，部分rejected不取消原冻结长期计划，不使用本轮参数替换规则或重开现金。",'',
f"只读监控同锁registry/snapshot/monitor门禁及每个旧行完整字典核验actualexit0：{feed['research_configs']}研究行，旧{feed['historical_rows_identical']}行完全一致，{feed['paper_accounts']}固定报价账户/{feed['paper_observations']}真实观察，gzip{(ROOT/'research/monitor/configs.json.gz').stat().st_size}字节，沿用5MB预算。未改监控代码/预算、paper计划/本金/持仓，未部署网页/新增定时器或下真实订单。",'',
f"报告说明更正：执行器继承了上一轮execution_scope文字，实际36场景结果/规格/状态均正确；原始报告逐字节压缩保存为{ann['original_report_compressed']}（解压SHA {ann['original_report_sha256']}），仅更正该说明，全部其他字段完全相等。未修改已绑定金融代码、规则、判据、收益、成交、账户或归档，模型/已完成观察0重跑；更正代码/回执/前后哈希公开留档。实际HTTP失败{httpfail}次，真实原始尝试/stderr/响应和回执全保留。",'',
f"核验后只清理本轮可重建语义元数据清单{cleanup['removed_bytes']}字节，原SHA/定义数/基准版本在cleanup_verification.json；金融结果/账户账本删除均0，剩余npy/pyc/tmp/checkpoint为0。保留10CSV、全部归档/状态段/必要逐笔、当前轻量HTTP/packet及下轮必要状态。main非强制push与完整远端tree/必要blob、198ID原S28链/21ID独立L4链、实际publisher终态/解锁证明在.git/automation_proofs/{R.name}.json；封存不预写commit SHA。"]
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
m={'round':R.name,'recorded_at_utc':now(),'working_directory':str(ROOT),'branch':'main','base_commit':start['base_commit'],'branch_lock_broker_pid':start['branch_lock_broker_pid'],'initial_main_branch_verification':rd(R/'main_only_branch_check.json'),'frozen_plan_sha256':sha(R/'plan.json'),'finished_report_sha256':sha(R/'report.json'),'finished_forward_report_sha256':sha(R/'forward_report.json'),'finished_candidate_report_sha256':sha(R/'candidate_observation/report.json'),'real_market_inputs':old['real_market_inputs'],'source_annual_and_recent_inputs':old['source_annual_and_recent_inputs'],'forward_raw_responses':fr['provenance'],'observer_preflight_raw_responses':[],'candidate_raw_artifacts':raw_artifacts,'candidate_input_manifest':im,'l4h02_input_manifest':lim,'l4h02_raw_artifacts':l4raw,'prospective_readiness':{'actual_candidate_observations':cv['cumulative_finished_candidate_observations'],'new_actual_observation_IDs':3,'original_frozen_rules_unchanged':True,'current_cutoff_utc':cv['cutoff_utc']},'new_independent_future_plan':{'path':rel(future/'plan.json'),'sha256':sha(future/'plan.json'),'binding_sha256':sha(future/'binding.json'),'engineering_only_passed':True,'actual_accounts':1,'actual_observations':lv['cumulative_finished_l4h02_observations'],'current_window_observation_IDs':3,'actual_cutoff_ns':ls['cutoff_ns'],'actual_cutoff_utc':lv['cutoff_utc'],'actual_verification_sha256':sha(R/'l4h02_verification.json'),'whole180day_qualified':False,'start_utc':fp['time_boundaries']['planned_start_utc'],'status':'running_partial_delayed_observation'},'registry':{'main_sha256_before_reserve':ctx['main_registry_sha256_before_reserve'],'before_events':ctx['registry_events'],'before_IDs':ctx['registry_ids'],'append_only_events':append_events,'new_finished_IDs':newids,'financial_IDs':n,'observation_IDs':len(obsbatch)},'read_only_source_results':plan['read_only_references'],'code_and_frozen_source_sha256':frozen,'protected_inputs_sha256':ctx['account_hashes_before'],'shared_files':{p:{'sha256':sha(ROOT/p),'bytes':(ROOT/p).stat().st_size} for p in sorted(mutable)},'required_command_receipts':required,'all_command_receipts':allreceipts,'failure_facts':rd(R/'read_failures.json'),'new_actual_results':{'financial_configs':n,'candidate_configs':6,'new_source_components':2,'new_native_models':4,'new_passive_parents':8,'new_benchmark_configs':4,'cost_scenes':3*n,'passed':passed,'rejected_candidates':2,'old_readonly_unique_results':len(plan['read_only_references']),'invalid_attempts_and_curves_retained':0,'failed_pipeline_commands':len(failed),'pre_reservation_engineering_failures':0,'report_scope_annotations':1,'pre_publication_helper_failures':0,'repaired_readonly_audit_failures':0,'actual_HTTP_failures':httpfail,'completed_native_or_parent_backtest_reruns':0,'completed_observation_reruns':0,'all_old_registry_qualifications_unchanged':True,'actual_native_quantity_and_model_impact_validated':True,'true_exchange_execution_or_capacity_validated':False,'independent_future_validated':False,'new_independent_future_observation_IDs':3,'new_independent_future_elapsed_minutes':lv['elapsed_minutes']},'artifacts':artifacts}
put(R/'data_manifest.json',m)
print(json.dumps({'sealed':True,'artifacts':len(artifacts),'protected_old_files':len(ctx['account_hashes_before']),'financial_configs':n,'new_finished_IDs':newids,'append_only_events':append_events,'report_sha256':sha(R/'report.json'),'manifest_sha256':sha(R/'data_manifest.json')}),flush=True)
