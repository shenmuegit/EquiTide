"""Seal real results only after independent checks and immutable account continuity."""
import ast,gzip,json,re,subprocess
from common import *
rd=lambda p:json.loads(p.read_text());P=ROOT/'research/experiments/20261102T055753Z'
assert not(R/'data_manifest.json').exists()
ctx,start,plan,rep,old=[rd(p) for p in [R/'context.json',R/'startup.json',R/'plan.json',R/'report.json',P/'data_manifest.json']]
audit,source,feed,cv,fv,lv=[rd(R/n) for n in ['verification.json','source_verification.json','feed_verification.json','candidate_verification.json','forward_verification.json','l4h02_verification.json']]
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==start['base_commit']
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert any(len(x.split())>4 and x.split()[1]=='FLOCK' and x.split()[4]==str(start['branch_lock_broker_pid']) for x in Path('/proc/locks').read_text().splitlines())
all_commands={p.name:rd(p) for p in R.glob('*_commands.json')};failed_commands={n:rows for n,rows in all_commands.items() if any(z['exit_code']!=0 for z in rows)}
assert set(failed_commands)=={'initial_commands.json'} and failed_commands['initial_commands.json'][0]['exit_code']==1
assert rd(R/'pre_evaluation_test_repair.json')['financial_computations_before_repair']==0
required={n:rows for n,rows in all_commands.items() if n not in failed_commands}
for phase in ['initial_retry1','reserve_batch_0','reserve_batch_1','evaluate','audit','summary','exports','decisions','grid','finish_batch_0','finish_batch_1','finish','forward','candidate','l4h02','observer_status','review','gates','feed','collect']:assert phase+'_commands.json' in required,phase
assert all(z['exit_code']==0 for rows in required.values() for z in rows)
b=rd(R/'bootstrap_receipt.json');assert b['actual_exit_code']==0;required['bootstrap_receipt.json']=[{**b,'exit_code':0}]
for n in ['primitive_verification.json','definition_check.json','verification.json','decision_verification.json','sensitivity_diagnostics.json','export_verification.json','visual_inspection.json','finish_verification.json','forward_verification.json','candidate_verification.json','source_verification.json','feed_verification.json','l4h02_verification.json']:assert rd(R/n)['passed'],n
assert sha(R/'report.json')==audit['report_sha256']==source['financial_report_sha256']==feed['financial_report_sha256']
assert sha(R/'plan.json')==rep['frozen_plan_sha256']==audit['plan_sha256']
assert audit['new_native_curves']==audit['new_parent_curves']==18 and audit['independent_new_policy_decisions']==6660 and audit['counts']['rejects']==0
batch=rd(R/'batch.json');obsbatch=rd(R/'forward_batch.json')+rd(R/'candidate_batch.json')+rd(R/'l4h02_batch.json');assert len(batch)==12 and len(obsbatch)==9
newids=len(batch)+len(obsbatch);appends=2*newids;assert source['new_finished_IDs']==newids and source['registry_append_only_events']==appends
binding=rd(R/'code_binding_before_evaluation.json')
for path,h in {**ctx['account_hashes_before'],**binding['source_sha256'],**binding['immutable_source_sha256']}.items():assert sha(ROOT/path)==h,path
firstreserve=min(x['started_utc'] for p in (R/'reserve_batches').glob('*.json') for x in rd(p)['actual_command_receipts']);assert rd(R/'TDD_red_receipt.json')['finished_utc']<firstreserve and binding['recorded_utc']<firstreserve<rep['evaluation_started_utc']
for stem,proof,key in [('candidate',cv,'cumulative_finished_candidate_observations'),('l4h02',lv,'cumulative_finished_l4h02_observations')]:
 prev=rd(P/(stem+'_verification.json'));assert proof[key]==prev[key]+3 and proof['elapsed_minutes']==prev['elapsed_minutes']+120
 assert proof['prior_NAV_prefix']==prev['NAV_points_per_scene'] and proof['NAV_points_per_scene']==proof['prior_NAV_prefix']+proof['new_NAV_points_per_scene']
 assert proof['new_funding_settlements']==proof['expected_from_actual_settlement_actions']==len(proof['independent_funding_cashflows'])
 assert proof['new_exact_causal_decisions']==proof['new_fills']==proof['new_rejected_orders']==proof['new_risk_proxy_violations']==0 and not proof['whole180day_qualified']
 for file in ['report','state']:assert sha(R/(stem+'_observation')/(file+'.json'))==proof[file+'_sha256']
 assert sha(ROOT/'research/automation'/(stem+'_forward_latest.json'))==proof['pointer_sha256']
prev=rd(P/'forward_verification.json');assert fv['original_NAV_prefix']==prev['NAV_points_per_scene'] and fv['NAV_points_per_scene']==prev['NAV_points_per_scene']+120 and fv['cumulative_minutes']==prev['cumulative_minutes']+120
assert fv['new_daily_decisions']==fv['new_executions']==0
future=ROOT/'research/experiments/20261031T174613Z/prospective_l4';fp=rd(future/'plan.json');fb=rd(future/'binding.json');ip=rd(R/'l4h02_resume_plan.json');ls=rd(R/'l4h02_observation/state.json');cs=rd(R/'candidate_observation/state.json')
assert sha(future/'plan.json')==fb['plan_sha256']==lv['plan_sha256']=='08e650a257ec9a0dbe27fe545f796a061a8538c05b8f9512821dc71a9cce3462'
assert ip['cutoff_ns']==ls['cutoff_ns']==ip['previous_pointer']['cutoff_ns']+120*MIN
closure=rd(R/'l4h02_reference_closure.json');assert closure['actual_launch_ns']>=closure['required_closed_reference_after_ns']==ip['cutoff_ns']+MIN
for path,h in {**fb['code_and_source_sha256'],**ip['source_sha256']}.items():assert sha(ROOT/path)==h,path
for item in old['real_market_inputs']+old['source_annual_and_recent_inputs']:assert sha(ROOT/item['path'])==item['sha256'] and (ROOT/item['path']).stat().st_size==item['bytes']
fr=rd(R/'forward_report.json');im=rd(R/'candidate_observation/input_manifest.json');lim=rd(R/'l4h02_observation/input_manifest.json');l4raw=rd(R/'l4h02_raw_manifest.json')['artifacts'];attempts=rd(R/'candidate_transport_attempts.json')
rawpaths={ROOT/x['raw'] for x in attempts}|{ROOT/im['packet']};rawart=[{'path':rel(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(rawpaths)]
for item in rd(R/'raw_evidence_index.json')['artifacts']:assert sha(ROOT/item['original_path'])==sha(ROOT/item['committed_copy'])==item['sha256']
fail=[x for x in attempts+lim['provenance'] if x.get('curl_exit_code',0) or x['http_status']!=200]
forward_errors=[{'log':x['log'],'stderr':x['stderr'],'observed_curl_error_codes':re.findall(r'curl: \((\d+)\)',x['stderr'])} for x in rd(R/'forward_commands.json') if 'curl:' in x.get('stderr','')]
httpfail=len(fail)+sum(len(x['observed_curl_error_codes']) for x in forward_errors)
put(R/'failure_receipts.json',{'failed_pipeline_commands':failed_commands,'expected_TDD_red':rd(R/'TDD_red_receipt.json'),'candidate_and_L4_HTTP_failures':fail,'forward_transport_errors':forward_errors,'exact_forward_HTTP_attempt_count_instrumented':False,'observed_HTTP_or_transport_failures':httpfail,'actual_read_tool_failures':rd(R/'read_failures.json')['facts'],'completed_native_or_parent_backtest_reruns':0,'completed_observation_reruns':0})
cleanup=rd(R/'cleanup_verification.json');assert cleanup['passed'] and cleanup['actual_financial_results_removed']==cleanup['account_ledger_files_removed']==0 and not cleanup['remaining_rebuild_intermediates']
ns=rd(R/'next_research_state.json');assert ns['original_single_S28']['books']==cs['books'] and ns['new_L4H02_forward']['books']==ls['books'] and ns['new_L4H02_forward']['risk']==ls['risk']
records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');assert len(events)==ctx['registry_events']+appends and len(records)==ctx['registry_ids']+newids
candidate=[c for c in rep['configs'].values() if c['role']=='candidate'];components=[c for c in rep['configs'].values() if c['scope']=='native'];assert len(candidate)==len(components)==6
for row in batch:
 z=records[row['fingerprint']];c=rep['configs'][row['name']];assert z['result_available'] and z['status']==c['status'] and z['report_sha256']==sha(R/'report.json')
for key,ref in plan['read_only_references'].items():assert records[key]['status']==ref['status'] and records[key]['report_sha256']==ref['report_sha256']
strict=lambda c:all(s['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in s['recent40']['folds'])>=6 for s in c['scenes'].values())
lo=min(c['scenes']['3']['net_return_pct'] for c in candidate);hi=max(c['scenes']['3']['net_return_pct'] for c in candidate);ddlo=min(c['scenes']['3']['max_drawdown_pct'] for c in candidate);ddhi=max(c['scenes']['3']['max_drawdown_pct'] for c in candidate)
pe=rd(R/'passed_candidate_evidence.json');assert len(pe['passed_candidates'])==len(rep['summary']['passed'])==2 and pe['passed_alias_count']==pe['all_new_config_aliases']==0
passed=[c for c in candidate if c['status']=='passed'];assert len(passed)==2 and all(c['L']==3 for c in passed)
interior=next(c for c in passed if c['HL']==.015);control=next(c for c in rep['all_current_grid'].values() if c['L']==3 and c['HL']==.02)
delta={k:interior['scenes'][k]['net_return_pct']-control['scenes'][k]['net_return_pct'] for k in ['1','2','3']}
assert all(interior['scenes'][k]['max_drawdown_pct']==control['scenes'][k]['max_drawdown_pct'] for k in ['1','2','3']) and delta['1']>0 and delta['2']>0 and delta['3']<0
append=['',f"封存：12个新定义逐项finish，6组合中{len(passed)}历史通过、{len(candidate)-len(passed)}淘汰；6ETH组件均未达到独立近期与局部支持门槛。组合3倍370日净收益{lo:.6f}%至{hi:.6f}%，整体DD{ddlo:.6f}%至{ddhi:.6f}%。所有年度、逐折、负收益期间及失败结果保留；12新定义相对同L旧HL2%完整NAV均不同，没有按本轮结果延伸批次或重跑已完成配置。",'',
"L3/HL1.5%（shortHS2.5%固定）组合1/2/3倍净收益12.627302%/10.998578%/9.369068%，对应完整曲线DD3.035647%/3.169982%/3.305465%；1倍10/12正月，近期三成本均6/8正折，局部严格近期支持5/6=83.33%。匹配旧HL2%收益12.544468%/10.969628%/9.394103%，DD相同。逐成本收益差+0.082834/+0.028949/−0.025035个百分点：附近存在接近表现，但降低HL没有全部成本改善，不能把微小历史差异称独立alpha或未来盈利。",'',
"另一个通过的L3/HL1%：1/2/3倍收益11.226601%/9.590221%/7.953185%，三倍DD4.098726%，各成本收益下降且DD上升，受同L旧HL2%历史对照支配。两L4新组合中HL1%近期仅5/8正折；HL1.5%虽近期6/8，九格局部严格近期支持仅5/9=55.56%而淘汰。两个L5新组合年收益更高，近期均仅4/8正折而淘汰。年度峰值不替代预设近期/邻域门槛，未因收益增加放宽标准。",'',
f"完整9格严格近期组合{sum(strict(c) for c in rep['all_current_grid'].values())}/9、原生{sum(strict(c) for c in rep['all_current_native_grid'].values())}/9。三成本Sharpe全格正，峰值在L5/HL1.5%这一回望边界，却未获近期资格；两面描述性相邻边2std悬崖仍存在。局部通过不代表整个参数面稳健，未做DSR/PBO显著性推断。结论仅为重复开发历史上的候选，所有三冻结账户保持原规则，没有新前向账户/定时任务/规则采用或180日资格。",'',
f"独立审计：{audit['new_NAV_points']}个完整新对齐NAV点、{audit['independent_new_policy_decisions']}决策，实际核算{audit['counts']}。Fraction独立价格阈值和Decimal数量/费用/冲击/资金费/小时维护代理/完整NAV审计通过，父只对齐加总真实银行，不另产生成交。新原生实际19980条funding、1290笔成交，旧只读19980条funding、678笔成交；不把方向决策当订单。{len(ctx['account_hashes_before'])}旧保护文件字节不变，{newids}新ID/{appends}条追加事件完整。",'',
f"SMA65续至{fr['cutoff_utc']}：旧NAV{fv['original_NAV_prefix']}+120={fv['NAV_points_per_scene']}，累计{fv['cumulative_minutes']}分钟/{fv['complete_days']}完整日，0新日决策/成交，cash/q/desired/cost/trades连续；65日上下文仍引用20261102T015622Z。singleS28续{cv['window_start_utc']}至{cv['cutoff_utc']}，NAV{cv['NAV_points_per_scene']}、累计ID{cv['cumulative_finished_candidate_observations']}，新决策/成交0、资金费{cv['independent_funding_cashflows']}，小时风险检查{cv['new_closed_hour_risk_checks']}。",'',
f"独立未过滤L4/H2续{lv['window_start_utc']}至{lv['cutoff_utc']}，仅08:11参考闭合后采集；NAV{lv['NAV_points_per_scene']}、累计{lv['elapsed_minutes']}分钟/{lv['cumulative_finished_l4h02_observations']}ID，新决策/成交0，实际资金费{lv['independent_funding_cashflows']}。真实08:00:00.001结算、BTC q−.006、mark78083与rate.00008758，各成本BTC收入0.04103105484USDT，ETHflat为0；不把结算时间强行取整，不重复之前00资金费，正收入不按成本倍增。小时检查{lv['new_closed_hour_risk_checks']}、风险违规0，cash/q/risk/上下文和NAV前缀完整续接。下一L4窗08:10→10:10须等10:11参考闭合；single/SMA下一06:30→08:30须等08:31参考闭合，原single实际08资金费留待那一新窗口处理。三份部分延迟shadow不替代十策略实时报价模拟，也不取消原长期计划。",'',
f"只读监控检查通过：{feed['research_configs']}研究行、{feed['historical_rows_identical']}旧行完整字典不变，10原报价账户/{feed['paper_observations']}观察，gzip{(ROOT/'research/monitor/configs.json.gz').stat().st_size}字节，5MB预算保持。本轮可确认HTTP/传输失败{httpfail}次；初次合成检查的fixture条件替换错误发生在金融登记前，实际失败退出/完整stderr保留于initial_commands、primitive_check和pre_evaluation_test_repair；只修测试分支，再次全部通过后才绑定代码/reserve。expected_TDD_red为另一条预期旧对称规则失败。失败与重试均留档，没有金融或完成观察重跑。",'',
f"本轮无需移除可重建临时文件，清理核验显示0字节/0金融结果/0账户账本删除。完整必要代码、轻量结果、spec、来源hash和短窗原始响应保留；main非强制push和完整远端tree/blob、真实进程终态与解锁证明保存在.git/automation_proofs/{R.name}.json。"]
with(R/'result.md').open('a') as f:f.write('\n'.join(append)+'\n')
# The financial report is immutable after finish; seal only adds explanatory evidence.
assert sha(R/'report.json')==audit['report_sha256']
for p in R.rglob('*.py'):ast.parse(p.read_text())
assert not any(p.name=='__pycache__' or p.suffix in ['.pyc','.npy','.tmp'] or 'checkpoint' in p.name for p in R.rglob('*'))
mutable={'research/automation/registry.jsonl','research/automation/candidate_forward_latest.json','research/automation/l4h02_forward_latest.json','research/monitor/latest.json','research/monitor/configs.json.gz'}
frozen={p:h for p,h in old['code_and_frozen_source_sha256'].items() if p not in mutable};frozen.update(binding['immutable_source_sha256']);frozen.update(fb['code_and_source_sha256']);frozen.update(ip['source_sha256'])
for ref in plan['read_only_references'].values():
 for k in ['spec','report','archive']:frozen[ref[k]]=ref[k+'_sha256']
for p,h in frozen.items():assert sha(ROOT/p)==h,p
put(R/'all_command_receipts.json',{p.name:rd(p) for p in R.glob('*_commands.json')})
artifacts={rel(p):sha(p) for p in sorted(R.rglob('*')) if p.is_file() and p.name!='data_manifest.json'}
m={'round':R.name,'recorded_at_utc':now(),'working_directory':str(ROOT),'branch':'main','base_commit':start['base_commit'],'branch_lock_broker_pid':start['branch_lock_broker_pid'],'initial_main_branch_verification':rd(R/'main_only_branch_check.json'),'frozen_plan_sha256':sha(R/'plan.json'),'finished_report_sha256':sha(R/'report.json'),'finished_forward_report_sha256':sha(R/'forward_report.json'),'finished_candidate_report_sha256':sha(R/'candidate_observation/report.json'),'real_market_inputs':old['real_market_inputs'],'source_annual_and_recent_inputs':old['source_annual_and_recent_inputs'],'forward_raw_responses':fr['provenance'],'observer_preflight_raw_responses':[],'candidate_raw_artifacts':rawart,'candidate_input_manifest':im,'l4h02_input_manifest':lim,'l4h02_raw_artifacts':l4raw,'prospective_readiness':{'actual_candidate_observations':cv['cumulative_finished_candidate_observations'],'new_actual_observation_IDs':3,'original_frozen_rules_unchanged':True,'current_cutoff_utc':cv['cutoff_utc']},'new_independent_future_plan':{'path':rel(future/'plan.json'),'sha256':sha(future/'plan.json'),'binding_sha256':sha(future/'binding.json'),'engineering_only_passed':True,'actual_accounts':1,'actual_observations':lv['cumulative_finished_l4h02_observations'],'current_window_observation_IDs':3,'actual_cutoff_ns':ls['cutoff_ns'],'actual_cutoff_utc':lv['cutoff_utc'],'actual_verification_sha256':sha(R/'l4h02_verification.json'),'whole180day_qualified':False,'start_utc':fp['time_boundaries']['planned_start_utc'],'status':'running_partial_delayed_observation'},'registry':{'main_sha256_before_reserve':ctx['main_registry_sha256_before_reserve'],'before_events':ctx['registry_events'],'before_IDs':ctx['registry_ids'],'append_only_events':appends,'new_finished_IDs':newids,'financial_IDs':12,'observation_IDs':9},'read_only_source_results':plan['read_only_references'],'code_and_frozen_source_sha256':frozen,'protected_inputs_sha256':ctx['account_hashes_before'],'shared_files':{p:{'sha256':sha(ROOT/p),'bytes':(ROOT/p).stat().st_size} for p in sorted(mutable)},'required_command_receipts':required,'all_command_receipts':{p.name:rd(p) for p in R.glob('*_commands.json')},'failure_facts':rd(R/'read_failures.json'),'new_actual_results':{'financial_configs':12,'candidate_configs':6,'new_source_components':6,'new_native_models':6,'new_passive_parents':6,'new_benchmark_configs':0,'cost_scenes':36,'passed':len(rep['summary']['passed']),'rejected_candidates':len(rep['summary']['candidate_rejected']),'old_readonly_unique_results':len(plan['read_only_references']),'invalid_attempts_and_curves_retained':0,'expected_TDD_red':1,'observed_HTTP_or_transport_failures':httpfail,'completed_native_or_parent_backtest_reruns':0,'completed_observation_reruns':0,'true_exchange_execution_or_capacity_validated':False,'independent_future_validated':False},'artifacts':artifacts}
put(R/'data_manifest.json',m)
print(json.dumps({'sealed':True,'artifacts':len(artifacts),'protected_old_files':len(ctx['account_hashes_before']),'financial_configs':12,'new_finished_IDs':newids,'append_only_events':appends,'report_sha256':sha(R/'report.json'),'manifest_sha256':sha(R/'data_manifest.json')}),flush=True)
