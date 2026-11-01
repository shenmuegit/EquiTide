"""Seal only actual results, immutable source hashes and verified account continuations."""
import ast,gzip,json,re,subprocess
from datetime import datetime
from common import *
rd=lambda p:json.loads(p.read_text());P=ROOT/'research/experiments/20261101T075017Z'
assert not(R/'data_manifest.json').exists()
ctx,start,plan,rep=[rd(R/n) for n in ['context.json','startup.json','plan.json','report.json']];old=rd(P/'data_manifest.json')
audit,source,feed,cv,fv,lv=[rd(R/n) for n in ['verification.json','source_verification.json','feed_verification.json','candidate_verification.json','forward_verification.json','l4h02_verification.json']]
fr=rd(R/'forward_report.json');im=rd(R/'candidate_observation/input_manifest.json');state=rd(R/'candidate_observation/state.json');lim=rd(R/'l4h02_observation/input_manifest.json');ls=rd(R/'l4h02_observation/state.json')
future=ROOT/'research/experiments/20261031T174613Z/prospective_l4';fp=rd(future/'plan.json');fb=rd(future/'binding.json');fc=rd(future/'engineering_checks.json');ip=rd(R/'l4h02_resume_plan.json')
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip()==str(ROOT)
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==start['base_commit']
assert any(len(x.split())>4 and x.split()[1]=='FLOCK' and x.split()[4]==str(start['branch_lock_broker_pid']) for x in Path('/proc/locks').read_text().splitlines())
phases=['initial','reserve_batch_0','evaluate','audit','summary','exports','finish_batch_0','finish','forward','candidate','l4h02','observer_status','review','gates','feed']
required={n+'_commands.json':rd(R/(n+'_commands.json')) for n in phases}
b=rd(R/'bootstrap_receipt.json');required['bootstrap_receipt.json']=[{**b,'exit_code':b['actual_exit_code']}]
for n in ['freeze_receipt.json','decision_check_receipt.json','grid_diagnostics_receipt.json','collect_evidence_receipt.json']:required[n]=[rd(R/n)]
assert all(z['exit_code']==0 for rows in required.values() for z in rows)
for n in ['primitive_verification.json','definition_check.json','verification.json','decision_verification.json','sensitivity_diagnostics.json','export_verification.json','visual_inspection.json','finish_verification.json','forward_verification.json','candidate_verification.json','source_verification.json','feed_verification.json','l4h02_verification.json']:assert rd(R/n)['passed'],n
n=len(rep['configs']);passed=len(rep['summary']['passed']);assert n==plan['expected_counts']['new_configs']==6 and passed==0 and len(rep['summary']['candidate_rejected'])==3 and len(rep['summary']['benchmark_rejected'])==2
assert sum(c['role']=='component' for c in rep['configs'].values())==1 and all(c['status']=='rejected' for c in rep['configs'].values())
assert sha(R/'report.json')==audit['report_sha256']==source['financial_report_sha256']==feed['financial_report_sha256']
assert sha(R/'plan.json')==rep['frozen_plan_sha256']==audit['plan_sha256']
assert audit['new_native_curves']==6 and audit['new_parent_curves']==12 and audit['new_NAV_points']==9810234
assert audit['read_only_native_curves']==24 and audit['read_only_parent_hashes']==24 and audit['independent_new_policy_decisions']==2220
assert audit['counts']=={'funding':33300,'fills':840,'rejects':0,'metric_checks':588,'margin_checks':214764}
batch=rd(R/'batch.json');obsbatch=rd(R/'forward_batch.json')+rd(R/'candidate_batch.json')+rd(R/'l4h02_batch.json');newids=len(batch)+len(obsbatch);append_events=2*newids;assert newids==15 and len(obsbatch)==9 and append_events==30
assert source['new_finished_IDs']==newids and source['registry_append_only_events']==append_events and source['actual_reserve_receipts']==source['actual_finish_exit0_receipts']==n
prevfv,prevcv,prevlv=[rd(P/x) for x in ['forward_verification.json','candidate_verification.json','l4h02_verification.json']]
assert fv['NAV_points_per_scene']==prevfv['NAV_points_per_scene']+120==43741 and fv['original_NAV_prefix']==prevfv['NAV_points_per_scene']==43621 and fv['cumulative_minutes']==prevfv['cumulative_minutes']+120==43709
assert fv['new_daily_decisions']==fv['new_reference_points']==fv['new_executions']==0 and fv['complete_days']==30
assert cv['cumulative_finished_candidate_observations']==prevcv['cumulative_finished_candidate_observations']+3==195 and cv['prior_NAV_prefix']==prevcv['NAV_points_per_scene']
assert cv['NAV_points_per_scene']==cv['prior_NAV_prefix']+cv['new_NAV_points_per_scene'] and cv['elapsed_minutes']==prevcv['elapsed_minutes']+120==7709
assert cv['new_funding_settlements']==cv['expected_from_actual_settlement_actions'] and cv['new_exact_causal_decisions']==cv['new_fills']==cv['new_rejected_orders']==cv['new_risk_proxy_violations']==0
assert cv['daily_context_bars']=={'BTC':38,'ETH':38} and cv['daily_NAV_boundaries']==6 and not cv['whole180day_qualified']
assert lv['passed'] and not lv['first_actual_window'] and lv['actual_observation_configs']==3 and lv['elapsed_minutes']==prevlv['elapsed_minutes']+120==609 and lv['NAV_points_per_scene']==prevlv['NAV_points_per_scene']+lv['new_NAV_points_per_scene']
assert lv['cumulative_finished_l4h02_observations']==18 and lv['new_exact_causal_decisions']==lv['new_fills']==lv['new_risk_proxy_violations']==0 and lv['new_funding_settlements']==lv['expected_from_actual_settlement_actions'] and not lv['whole180day_qualified']
for stem,proof in [('candidate',cv),('l4h02',lv)]:
 w=R/(stem+'_observation');pointer=ROOT/'research/automation'/(stem+'_forward_latest.json');assert sha(w/'report.json')==proof['report_sha256'] and sha(w/'state.json')==proof['state_sha256'] and sha(pointer)==proof['pointer_sha256']
binding=rd(R/'code_binding_before_evaluation.json');assert binding['recorded_utc']<rep['evaluation_started_utc']
for path,h in {**binding['source_sha256'],**binding['immutable_source_sha256'],**ctx['account_hashes_before']}.items():assert sha(ROOT/path)==h,path
assert fc['passed'] and fc['engineering_only_no_financial_trials']
assert sha(future/'plan.json')==fb['plan_sha256']==fc['plan_sha256']==lv['plan_sha256']=='08e650a257ec9a0dbe27fe545f796a061a8538c05b8f9512821dc71a9cce3462'
assert sha(future/'binding.json')==fc['binding_sha256']=='01177303b7999cef85b3bbb8a534ef5804ee79c9a83b533f3a110822801ff1eb'
for path,h in {**fb['code_and_source_sha256'],**ip['source_sha256']}.items():assert sha(ROOT/path)==h,path
assert ip['cutoff_ns']==ls['cutoff_ns']==1793527800000000000 and ip['previous_pointer']['cutoff_ns']==1793520600000000000 and sha(R/'l4h02_observation/previous_pointer.json')==ip['previous_pointer_sha256']
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
ns=rd(R/'next_research_state.json');assert ns['original_single_S28']['books']==state['books'] and ns['original_single_S28']['NAV_points']==cv['NAV_points_per_scene'] and ns['original_single_S28']['cumulative_observation_IDs']==195
assert ns['new_L4H02_forward']['actual_observations']==18 and ns['new_L4H02_forward']['books']==ls['books'] and ns['new_L4H02_forward']['risk']==ls['risk'] and ns['new_L4H02_forward']['elapsed_minutes']==609
assert ns['research']['new_configurations']==6 and ns['research']['new_candidates']==3 and ns['research']['new_native_evaluations']==2
candidate=[c for c in rep['configs'].values() if c['role']=='candidate'];assert all(c['status']=='rejected' and 'recent40_six_of_eight_positive5d_all_costs' in c['failed_criteria'] and 'local_recent6of8_allcost_gte60pct' in c['failed_criteria'] for c in candidate)
assert [c['recent40_positive_5d_folds_by_cost']['3'] for c in candidate]==[5,5,4]
assert cv['new_funding_settlements']==cv['expected_from_actual_settlement_actions']==6 and lv['new_funding_settlements']==lv['expected_from_actual_settlement_actions']==0
fund=cv['independent_funding_cashflows'];assert len(fund)==6 and all(1793520000000000000<=x['timestamp_ns']<=1793521800000000000 for x in fund)
strict=lambda c:all(s['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in s['recent40']['folds'])>=6 for s in c['scenes'].values());assert sum(strict(c) for c in rep['all_current_grid'].values())==4
center=next(c for c in rep['all_current_grid'].values() if c['BTC_capital_usdt']==3750 and c['H']==.025);assert center['readonly'] and center['status']=='passed' and center['current_grid_diagnostic_sensitivity']['local_strict_recent_fraction']==4/9
append=['',f"封存结论：3个新组合候选全淘汰；三倍成本370日净收益分别{[c['scenes']['3']['net_return_pct'] for c in candidate]}%，整体DD分别{[c['scenes']['3']['max_drawdown_pct'] for c in candidate]}%，全年/成本/DD等门槛达标，但三倍近期正5日折5/8、5/8、4/8，局部严格近期支持50%、33.33%、25%，低于6/8与60%原门槛。原生BTC2500动量也因近期4/8与邻域近期失败淘汰；原生持有−2.885871%、组合持有−12.238020%三倍真实负结果保存。全部6定义/18成本场景、9观察/27场景完成实际登记，合计15新ID/30追加事件。",'',
'较小银行边界被夹住：完整9格点每档全年收益和Sharpe均正，严格近期只有4/9。最大Sharpe仍为旧3750/H2.5%，现是网格内部点；但其本轮完整3×3邻域严格近期支持也只有4/9，低于60%。旧canonical passed按原历史语义保留，不能据此称通过当前扩展网格的稳健性；没有重写旧报告/资格，也没有新增该旧配置评估。所有成本档描述性相邻Sharpe悬崖仍触发，非统计显著性/DSR/PBO。', '',
f"独立审计实际exit0：6新原生和12新父成本曲线，共9810234完整NAV点；24旧原生曲线和24旧父NAV哈希只读。2220次独立新策略决策、33300资金费、840成交、588整体/月指标及214764小时风险检查，无拒单/负抵押/维护代理违规。16个旧实际来源和{len(ctx['account_hashes_before'])}个旧保护文件字节不变。",'',
f"原SMA65续06:30至08:30：{fv['original_NAV_prefix']}旧点+120={fv['NAV_points_per_scene']}NAV，{fv['cumulative_minutes']}分钟/30天，0日决策/成交。原singleS28同窗保留10000/10000,N1000/3000,ETHL3：{cv['prior_NAV_prefix']}旧点+{cv['new_NAV_points_per_scene']}={cv['NAV_points_per_scene']}NAV，7709分钟/195ID/65窗；本窗真实08资金费{fund}，正BTC收入不乘成本，ETHflat为0；{cv['new_closed_hour_risk_checks']}次小时风险检查/0违规，无日决策/成交。",'',
f"独立未过滤L4/H2保留5000/15000,N500/4500,S28zeroexit，08:10续10:10，在10:11闭合后才采集：{lv['prior_NAV_prefix']}旧点+{lv['new_NAV_points_per_scene']}={lv['NAV_points_per_scene']}NAV，609分钟/18ID/6窗；本窗0资金费/日决策/成交，{lv['new_closed_hour_risk_checks']}小时风险状态/0违规。上轮08资金费只记一次，继承pre08与post08.003现金的正时长风险状态，不压平成最终book。三账户均未成熟180日，拒绝部分资格不取消原计划，完整账本/冻结规则/本金与持仓保留。",'',
f"同锁registry/snapshot/monitor及全旧行逐字典核验实际通过：{feed['research_configs']}研究行，旧{feed['historical_rows_identical']}行完整相等，{feed['paper_accounts']}固定报价账户/{feed['paper_observations']}真实观察，gzip{(ROOT/'research/monitor/configs.json.gz').stat().st_size}字节。沿用5MB门禁，不改快照代码/预算，不重新部署网页/建定时器或改变paper状态，不下真实订单。",'',
f"实际HTTP失败{httpfail}次，完整原始尝试/响应/stderr和回执保存；查找一个不存在的旧脚本文件名触发一次真实只读FileNotFoundError，已记录，后续读取正确文件名，无金融计算或账务影响。模型/已完成观察均0重跑。保留10CSV、完整状态段/必要逐笔、SHA、当前轻量HTTP/packet及下轮必要状态；0npy/pyc/tmp/checkpoint。main非强制push与远端全tree/必要blob、195ID原S28链/18ID独立L4链、实际publisher终态和解锁后证明在.git/automation_proofs/{R.name}.json，封存不预写commit SHA。重复开发历史不是最终未触碰测试，正收益不是稳定实盘盈利。"]
append+=['',f"核验后清理：仅本轮可重建语义元数据清单{cleanup['removed_bytes']}字节，原哈希/定义数/基准版本保存在cleanup_verification.json；实际金融结果/账户账本删除均0，剩余npy/pyc/tmp/checkpoint为0。当前原始证据实际20项（原SMA2响应、原S28和独立L4各9项），索引中的继承说明已纠正为实际SMA响应数，原说明透明保留。"]
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
m={'round':R.name,'recorded_at_utc':now(),'working_directory':str(ROOT),'branch':'main','base_commit':start['base_commit'],'branch_lock_broker_pid':start['branch_lock_broker_pid'],'initial_main_branch_verification':rd(R/'main_only_branch_check.json'),'frozen_plan_sha256':sha(R/'plan.json'),'finished_report_sha256':sha(R/'report.json'),'finished_forward_report_sha256':sha(R/'forward_report.json'),'finished_candidate_report_sha256':sha(R/'candidate_observation/report.json'),'real_market_inputs':old['real_market_inputs'],'source_annual_and_recent_inputs':old['source_annual_and_recent_inputs'],'forward_raw_responses':fr['provenance'],'observer_preflight_raw_responses':[],'candidate_raw_artifacts':raw_artifacts,'candidate_input_manifest':im,'l4h02_input_manifest':lim,'l4h02_raw_artifacts':l4raw,'prospective_readiness':{'actual_candidate_observations':cv['cumulative_finished_candidate_observations'],'new_actual_observation_IDs':3,'original_frozen_rules_unchanged':True,'current_cutoff_utc':cv['cutoff_utc']},'new_independent_future_plan':{'path':rel(future/'plan.json'),'sha256':sha(future/'plan.json'),'binding_sha256':sha(future/'binding.json'),'engineering_only_passed':True,'actual_accounts':1,'actual_observations':lv['cumulative_finished_l4h02_observations'],'current_window_observation_IDs':3,'actual_cutoff_ns':ls['cutoff_ns'],'actual_cutoff_utc':lv['cutoff_utc'],'actual_verification_sha256':sha(R/'l4h02_verification.json'),'whole180day_qualified':False,'start_utc':fp['time_boundaries']['planned_start_utc'],'status':'running_partial_delayed_observation'},'registry':{'main_sha256_before_reserve':ctx['main_registry_sha256_before_reserve'],'before_events':ctx['registry_events'],'before_IDs':ctx['registry_ids'],'append_only_events':append_events,'new_finished_IDs':newids,'financial_IDs':n,'observation_IDs':len(obsbatch)},'read_only_source_results':plan['read_only_references'],'code_and_frozen_source_sha256':frozen,'protected_inputs_sha256':ctx['account_hashes_before'],'shared_files':{p:{'sha256':sha(ROOT/p),'bytes':(ROOT/p).stat().st_size} for p in sorted(mutable)},'required_command_receipts':required,'all_command_receipts':allreceipts,'failure_facts':rd(R/'read_failures.json'),'new_actual_results':{'financial_configs':n,'candidate_configs':3,'new_source_components':1,'new_native_models':2,'new_passive_parents':4,'new_benchmark_configs':2,'cost_scenes':3*n,'passed':passed,'rejected_candidates':3,'old_readonly_unique_results':len(plan['read_only_references']),'invalid_attempts_and_curves_retained':0,'failed_pipeline_commands':len(failed),'pre_reservation_engineering_failures':1,'pre_publication_helper_failures':0,'repaired_readonly_audit_failures':0,'actual_HTTP_failures':httpfail,'completed_native_or_parent_backtest_reruns':0,'completed_observation_reruns':0,'all_old_registry_qualifications_unchanged':True,'actual_native_quantity_and_model_impact_validated':True,'true_exchange_execution_or_capacity_validated':False,'independent_future_validated':False,'new_independent_future_observation_IDs':3,'new_independent_future_elapsed_minutes':lv['elapsed_minutes']},'artifacts':artifacts}
put(R/'data_manifest.json',m)
print(json.dumps({'sealed':True,'artifacts':len(artifacts),'protected_old_files':len(ctx['account_hashes_before']),'financial_configs':n,'new_finished_IDs':newids,'append_only_events':append_events,'report_sha256':sha(R/'report.json'),'manifest_sha256':sha(R/'data_manifest.json')}),flush=True)
