"""Seal audited native capital results and unchanged original account continuations."""
import ast,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;P=ROOT/'research/experiments/20261029T212831Z'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
read=lambda p:json.loads(p.read_text())
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
assert not(R/'data_manifest.json').exists()
ctx=read(R/'context.json');start=read(R/'startup.json');plan=read(R/'plan.json');report=read(R/'report.json');old=read(P/'data_manifest.json');summary=read(R/'sensitivity_summary.json');source=read(R/'source_verification.json');feed=read(R/'feed_verification.json');cv=read(R/'candidate_verification.json');fv=read(R/'forward_verification.json');risk=read(R/'risk_carry_verification.json');state=read(R/'candidate_observation/state.json');im=read(R/'candidate_observation/input_manifest.json');rep=read(R/'representative.json');comp=read(R/'comparison_verification.json');execution=read(R/'execution_verification.json')
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip()==str(ROOT)
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==start['head_after_successful_SSH_fetch']
assert any(len(s.split())>4 and s.split()[1]=='FLOCK' and s.split()[4]==str(start['branch_lock_broker_pid']) for s in Path('/proc/locks').read_text().splitlines())
phases=['initial_retry','evaluate','audit','summary','exports','execution','comparison','finish','forward','candidate','observer_status','review','gates','feed','reserve_batch_retry0',*[f'reserve_batch_{i}' for i in range(1,6)],*[f'finish_batch_{i}' for i in range(6)]]
required={phase+'_commands.json':read(R/(phase+'_commands.json')) for phase in phases}
assert all(x['exit_code']==0 for rows in required.values() for x in rows)
for n in ['definition_check.json','engine_change_verification.json','data_preflight.json','verification.json','execution_verification.json','comparison_verification.json','export_verification.json','finish_verification.json','visual_inspection.json','forward_verification.json','candidate_verification.json','risk_carry_verification.json','candidate_validation.json','source_verification.json','feed_verification.json']:
 assert read(R/n)['passed'],n
assert source['new_finished_IDs']==48 and source['registry_append_only_events']==96
assert source['actual_finish_exit0_receipts']==source['actual_reserve_receipts']==42 and source['old_unique_results_unchanged']==12
assert len(report['summary']['passed'])==6 and len(report['summary']['rejected'])==12
assert summary['strict_individual_costfold_passes']==6 and summary['reference_configs']==24
assert comp['exact_ungated_matches']==6 and comp['passed_matches_to_ungated']==3 and comp['joint_full_return_DD_improvements']==0
assert execution['native_cost_scenes_verified']==63 and execution['old_scaled_orders_that_would_violate_LOT']==1860
assert sha(R/'report.json')==source['financial_report_sha256']==summary['report_sha256']==read(R/'verification.json')['report_sha256']==feed['financial_report_sha256']
assert cv['cumulative_finished_candidate_observations']==108 and cv['elapsed_minutes']==4229 and cv['NAV_points_per_scene']==4325
assert cv['prior_NAV_prefix']==4203 and cv['new_NAV_points_per_scene']==122
assert cv['new_funding_settlements']==cv['new_exact_causal_decisions']==cv['new_fills']==0 and cv['new_closed_hour_risk_checks']==6
assert fv['NAV_points_per_scene']==40258 and fv['cumulative_minutes']==40229 and fv['new_daily_decisions']==fv['new_executions']==0
assert read(R/'visual_inspection.json')['panels_actually_seen']==12 and ctx['initial_16_missing_actual_results']==0
binding=read(R/'code_binding_before_evaluation.json');assert binding['recorded_utc']<report['evaluation_started_utc']
for path,h in binding['source_sha256'].items():assert sha(ROOT/path)==h,path
sys.path.insert(0,str(ROOT/'research/automation'));import registry
records=registry.read_records(ROOT/'research/automation/registry.jsonl');events=registry.read_events(ROOT/'research/automation/registry.jsonl');batch=read(R/'batch.json')
for row in batch:
 sp=read(ROOT/row['spec']);es=[e for e in events if e['fingerprint']==row['fingerprint'] and e['status']=='reserved']
 assert len(es)==1 and es[0]['spec']==sp and records[row['fingerprint']]['spec']==sp
put(R/'economic_definition_preservation.json',{'passed':True,'exact_new_specs':42,'successful_reservations_per_financial_ID':1,'same_full_spec_values_in_reservation_and_final_registry':True,'financial_evaluations_per_ID':1,'prefreeze_setup_failures_only_no_financial_reruns':True,'parameters_rules_capital_raw_weights_costs_boundaries_and_failure_criteria_unchanged':True,'full_feature_funding_history1212_OOS_cashflows1110':True,'report_sha256':sha(R/'report.json')})
for path,h in ctx['account_hashes_before'].items():assert sha(ROOT/path)==h,path
for x in old['real_market_inputs']+old['source_annual_and_recent_inputs']:
 assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
refs=[*plan['component_sources'].values(),*plan['read_only_anchor_references'].values(),*plan['read_only_hold_references'].values(),*plan['read_only_ungated_references'].values()]
unique={x['fingerprint']:{**x,'status':x['original_status']} for x in refs}
assert len(unique)==12
sharedpaths=['research/automation/registry.jsonl','research/automation/candidate_forward_latest.json','research/monitor/latest.json','research/monitor/configs.json.gz']
code={p:h for p,h in old['code_and_frozen_source_sha256'].items() if p not in sharedpaths};code.update(plan['helpers'])
for x in refs:
 for key in ['spec','report','archive']:code[x[key]]=x[key+'_sha256']
for path in ['research/experiments/20261029T212831Z/engine.py','research/experiments/20261025T065405Z/engine.py','research/experiments/20261026T110637Z/prospective_core.py','research/experiments/20261026T110637Z/prospective_observer.py','research/experiments/20261026T090537Z/candidate_prospective_plan.json','research/experiments/20261001T113625Z/forward_plan.json']:
 code[path]=sha(ROOT/path)
for path,h in code.items():assert sha(ROOT/path)==h,path
facts=read(R/'read_failures.json');attempts=read(R/'candidate_transport_attempts.json');seen={x.get('raw') for x in facts['facts'] if x.get('raw')}
for x in attempts:
 if (x['http_status']!=200 or x['curl_exit_code']!=0) and x['raw'] not in seen:
  facts['facts'].append({'phase':'candidate public verifiedTLS transport','eventual_window_successfully_audited':True,**x})
allreceipts={p.name:read(p) for p in R.glob('*_commands.json')};put(R/'all_command_receipts.json',allreceipts)
for filename,rows in allreceipts.items():
 for x in rows:
  if x['exit_code'] and not any(y.get('log')==x['log'] and y.get('exit_code')==x['exit_code'] for y in facts['facts']):facts['facts'].append({'phase':filename,**x})
put(R/'read_failures.json',facts)
for p in R.rglob('*.py'):ast.parse(p.read_text(),filename=str(p))
assert len(list(R.glob('*.csv')))==6 and all(b'\r' not in p.read_bytes() for p in R.glob('*.csv'))
put(R/'serialization_check.json',{'passed':True,'CSV_files':6,'all_LF':True,'all_42_financial_definitions_single_reserve_single_actual_evaluation_finish':True,'all_required_terminal_commands_exit0':True,'prefreeze_failed_setup_receipts_and_draft_hashes_preserved':True})
(R/'candidate_current_pointer.json').write_bytes((ROOT/'research/automation/candidate_forward_latest.json').read_bytes());assert sha(R/'candidate_current_pointer.json')==cv['pointer_sha256']
cleanup=[]
path=R/'prepare.py'
if path.exists():
 cleanup.append({'path':rel(path),'sha256':sha(path),'bytes':path.stat().st_size,'reason':'Own reconstructible setup-only helper. Preserve all successful/negative financial ledgers/specs/frozen code and failed freeze snapshot/logs.'});path.unlink()
put(R/'cleanup.json',{'removed':cleanup,'other_files_removed':False,'preexisting_data_normalized_preserved':True})
center=next(x for x in read(R/'qualification_fragility.json')['rows'] if x['fingerprint']==rep['fingerprint'])
put(R/'spec_clarification.json',{'financial_recalculation':False,'specs_unchanged':True,'specific_parameter_fields_take_precedence_in_identifying_execution_branch':'Each spec fixes capital_policy,initial_capital,entry_notional,source_component_parameters and raw_component_multipliers. Generic logic describes the entire experiment and separately explains ownership reference branches.','actual_bank_parents':{'raw_weights':[1,1],'meaning':'Sum the actual funded native banks:3750/16250,5000/15000,6250/13750 of20000USDT. No transfers,rebalancing,normalization,NAV sizing or shared margin.'},'old_bank_ownership_comparisons':{'raw_weights_rule':'[2*w,2*(1-w)],w in[.1875,.25,.3125]','meaning':'Ownership of original10000USDT bank NAVs;center [.5,1.5] reused readonly. Scaled historical quantities are comparisons,not executable new order sizes.'}})
with (R/'result.md').open('a') as f:
 f.write('\n封存核验：42份完整spec在计算前各成功reserve一次，126成本场景共68,671,638完整净值点独审通过；21原生新规模账本含2,538笔模拟成交、69,930条资金费结算（含空仓）、23,310个因果日决策与330,939次状态小时风险检查。6实际分仓候选历史通过、12候选淘汰、24组件/对照仅参考；48本轮ID全部finish，登记只追加96事件，12旧结果资格不变。\n')
 f.write('执行差异证据：旧银行简单缩放的1,860条数量不符合lot步长，1,986条实际新规模数量与线性缩放不同，2,538笔冲击率在新数量上重新计算。中心BTC/ETH本金5000/15000、固定新开名义500/4500、raw[1,1]、N6/C0.5bp，三倍370日净收益'+str(rep['return3_pct'])+'%、连续整体DD'+str(rep['whole_DD3_pct'])+'%、近期40日净收益'+str(rep['recent_return3_pct'])+'%；各成本6/8正五日折、局部严格通过2/3，最小正五日折'+str(center['minimum_positive_recent_fold_pct_by_cost'])+'。旧10000银行raw[.5,1.5]对照收益10.209169963888009%，差−0.095196302941368个百分点；这仅是同历史模型的数量取整/规模成本差，未证明真实成交与容量。\n')
 f.write('匹配对照：6候选三成本完整净值等于同规模未筛选对照，其中3为历史通过项。没有候选在每个成本同时提高完整收益并降低整体回撤。C0分仓仅5/8正近期折，ETH原生仅1/4/4最差成本正折；均未放宽失败判据。图2张共12面板实际打开核对。\n')
 f.write('冻结账户：旧SMA/singleS28只从20:30续至22:30。SMA累计40258点/场景、40229分钟，现金/持仓/成本/完整前缀不变；singleS28累计108观察ID、4325点/场景、4229分钟，本窗0资金费/日决策/新成交、6次闭合小时风险检查0违规。两者均是延迟真实闭合数据重建，不等于十账户真实报价模拟，不满足180天独立未来资格。原账户未采用本轮筛选或本金变更。\n')
 f.write('工程前置失败：最初freeze因旧常持对照缺未使用lookback字段失败，提前批次调用因batch尚未生成失败；当时没有成功reserve或金融计算。原日志/退出/草稿哈希/失败代码保留，修正显式未使用参数后完整冻结，42个有效配置各计算一次。公共传输失败如有逐次保留原响应与真实状态。\n')
 f.write('只读monitor与门禁实际成功：'+str(feed['research_configs'])+'研究项、'+str(feed['paper_observations'])+'既有观察/10账户；'+str(feed['historical_rows_identical'])+'旧展示行完整字典不变。仅清理本人可重建setup文件，保留完整实际结果与账本。实际commit/push全远端证据及本人锁释放见.git/automation_proofs/'+R.name+'.json。\n')
nextstate={'round':R.name,'branch_policy':'main only;fixedroot;no subagents/orders/worktrees','report':rel(R/'report.json'),'report_sha256':sha(R/'report.json'),'plan':rel(R/'plan.json'),'plan_sha256':sha(R/'plan.json'),'initial16_missing_actual_results':0,'new_financial_configs':42,'new_native_models':21,'new_parents':21,'new_candidates':18,'new_references':24,'passed':6,'rejected_candidates':12,'grid':plan['grid'],'all_old_control_statuses_unchanged':True,'representative_historical_grid_center':rep,'center_min_positive5day_fold_pct_by_cost':center['minimum_positive_recent_fold_pct_by_cost'],'execution_verification':{'path':rel(R/'execution_verification.json'),'sha256':sha(R/'execution_verification.json'),'old_scaled_offlot_quantities':1860,'different_actual_quantities':1986,'newsize_impact_recalculated':2538,'L2_TCA_capacity_not_established':True},'matched_control_comparisons':{'path':rel(R/'comparison_verification.json'),'sha256':sha(R/'comparison_verification.json'),'matched_ungated_candidate_complete_threecost_NAVs':6,'matched_passed_candidates':3,'joint_return_DD_improvements_everycost':0,'not_global_history_novelty_or_independent_future':True},'next_research_priority':'Do not repeat these42finishedexactspecs. Native unequal-capital orders and cost/lot differences are now verified;6conditionalhistoricalparentspass only atC0.5/1bp. C1bp matches matchedungated NAV. C0.5bp is different butnojointreturn/DDimprovement. Consider preregistered S/fastL/threshold or new non-equivalentcombination/regime direction usingactualnativebanks ratherthan oldownershipscaling. Preserve complete1212fundingfeaturehistory separatelyfrom1110OOSsettlementcashflows. All history reuseddevelopment,no untouchedfinaltest. No furtherclaims until independentfuture/actualexecutionevidence.','original_SMA':{'state':rel(R/'forward_state.json'),'state_sha256':sha(R/'forward_state.json'),'report':rel(R/'forward_report.json'),'report_sha256':sha(R/'forward_report.json'),'cutoff_utc':'2026-10-29T22:30:00Z','NAV_points':40258,'elapsed_minutes':40229,'daily_context65_path':'research/experiments/20261029T012253Z/forward_inputs.json.gz','daily_context65_sha256':sha(ROOT/'research/experiments/20261029T012253Z/forward_inputs.json.gz'),'next_daily_decision_utc':'2026-10-30T00:01:00Z','terminal_plan_unchanged':'2027-03-31'},'original_candidate':{'pointer':'research/automation/candidate_forward_latest.json','saved_pointer':rel(R/'candidate_current_pointer.json'),'saved_pointer_sha256':sha(R/'candidate_current_pointer.json'),'state':rel(R/'candidate_observation/state.json'),'state_sha256':sha(R/'candidate_observation/state.json'),'report':rel(R/'candidate_observation/report.json'),'report_sha256':sha(R/'candidate_observation/report.json'),'delta':rel(R/'candidate_observation/delta.json.gz'),'delta_sha256':sha(R/'candidate_observation/delta.json.gz'),'cutoff_utc':'2026-10-29T22:30:00Z','observations':108,'NAV_points':4325,'elapsed_minutes':4229,'daily_context_bars':35,'daily_NAV_boundaries':3,'books':state['books'],'risk':state['risk'],'next_window':'NextwindowlikelycrossesUTCmidnight. DoNOTextendthismark-onlySMAwrapperpastnext00:01dailydecision. UseoriginalcrossdaySMAobserver research/experiments/20261029T012253Z andoriginalcandidatecore. Oct30UTC00funding precedes00:01originalsingleS28decision;preserveexactnanosecondordering/cash/q/entry/context andcompleteNAVprefix. Carry22hourriskstate,current6checksclose20/21positive-durationstates. DoNOTrecreditpriorOct29UTC16funding. Neverreplaceoldaccountwithnewmajority/fundingfilter.','frozen180day_end_utc':'2027-04-25T00:01:00Z','mode':'delayedrealclosedbar/funding reconstruction,not livequote/paper10/orders'},'monitor':{'research_rows':feed['research_configs'],'old_rows_unchanged':feed['historical_rows_identical'],'paper_observations':feed['paper_observations'],'paper_accounts':feed['paper_accounts'],'gzip_bytes':(ROOT/'research/monitor/configs.json.gz').stat().st_size,'budget_bytes':4000000},'paper10_policy':'Readonly;btc-eth-2 owns its existingfrozenaccounts.'}
put(R/'next_research_state.json',nextstate)
(R/'reproduce.md').write_text('''# 复现与只读核验

固定目录 `/home/desktop/Documents/Codex/EquiTide`，解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。42金融配置各保存完整spec并先成功reserve，21原生执行与21父组合各实际评估一次，再分别finish；另6原冻结账户观察独立reserve/finish，共48新ID、96追加事件。已完成精确配置只读结果，不在正式登记中重复回测、重开账户或改本金/冻结规则。

完整复现调用、每批实际reserve/finish及实际退出见all_command_receipts.json、reserve_batches和finish_batches。initial freeze的旧hold缺未使用字段、过早reserve找不到batch在成功冻结/42有效预约之前发生，无实际金融结果。保留failed freeze代码、草稿哈希与失败日志；unusedL/H/E显式填写后从头冻结，未发生已登记金融配置重试。所有实际正负结果完整保留，不把工程通过当金融passed。

8合并真实Parquet、16原始/近期输入、所有源spec/report/archive与冻结源版本SHA见data_manifest。原行情/公共HTTP原响应留ignoreddata并绑定SHA，不提交大行情；缺真实匹配输入必须停止。资金费特征使用1212条完整历史、available_ts及settlement_ts均不晚于信号时点；1110条OOS资金费只用于实际现金入账。固定原始权重不归一化：实际父组合raw[1,1]相加两已分配资金银行；旧银行所有权对照raw[2w,2(1-w)]仅比较净值。各spec的capital_policy/entry_notional/source_component_parameters固定具体分支。

封存版本可只读核验已有账本（不产生新策略结果或账户成交）：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T232932Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T232932Z/check_execution.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T232932Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T232932Z/forward.py --reproduce
```

审计独立重建信号、Decimal成交/资金费/保证金状态与全净值，按(ns,eventcode)组合，不调用simulate/target/trade。未来共享账户推进后，读取本轮提交blob、保存pointer和完整账本，不回滚账户或main。历史通过仅限预设资本/资金费网格，无独立未来或实盘盈利证明。只读monitor不产生模拟成交。下一轮跨UTC00资金费和00:01日决策，必须用原跨日observer与完整65/35日上下文，不能将当前mark-only续记直接越过日决策。
''')
pp=R/'implementation_plan.md';pp.write_text(pp.read_text().replace('- [ ]','- [x]')+'\n研究/核验/封存完成；实际发布、全远端SHA核验及本人锁释放以.git真实证明为准。\n')
rawpaths={x['raw'] for x in attempts}|{im['packet']}
rawartifacts=[{'path':p,'sha256':sha(ROOT/p),'bytes':(ROOT/p).stat().st_size} for p in sorted(rawpaths)]
fr=read(R/'forward_report.json');shared={p:{'sha256':sha(ROOT/p),'bytes':(ROOT/p).stat().st_size} for p in sharedpaths}
artifacts={rel(p):sha(p) for p in sorted(R.rglob('*')) if p.is_file() and p.name!='data_manifest.json'}
assert not any(p.name=='__pycache__' or 'checkpoint' in p.name or p.suffix in ['.pyc','.npy','.tmp'] for p in R.rglob('*'))
m={'round':R.name,'recorded_at_utc':now(),'working_directory':str(ROOT),'branch':'main','base_commit':start['head_after_successful_SSH_fetch'],'branch_lock_broker_pid':start['branch_lock_broker_pid'],'initial_main_branch_verification':read(R/'main_only_branch_check.json'),'frozen_plan_sha256':sha(R/'plan.json'),'finished_report_sha256':sha(R/'report.json'),'finished_forward_report_sha256':sha(R/'forward_report.json'),'finished_candidate_report_sha256':sha(R/'candidate_observation/report.json'),'real_market_inputs':old['real_market_inputs'],'source_annual_and_recent_inputs':old['source_annual_and_recent_inputs'],'forward_raw_responses':fr['provenance'],'observer_preflight_raw_responses':[],'candidate_raw_artifacts':rawartifacts,'candidate_input_manifest':im,'prospective_readiness':{'actual_candidate_observations':108,'new_actual_observation_IDs':3,'original_frozen_rules_unchanged':True,'current_cutoff_utc':'2026-10-29T22:30:00Z'},'registry':{'main_sha256_before_reserve':ctx['main_registry_sha256_before_reserve'],'before_events':ctx['registry_events'],'before_IDs':ctx['registry_ids'],'append_only_events':96,'new_finished_IDs':48,'financial_IDs':42,'invalid_financial_attempts':0},'read_only_source_results':unique,'code_and_frozen_source_sha256':code,'protected_inputs_sha256':ctx['account_hashes_before'],'shared_files':shared,'required_command_receipts':required,'all_command_receipts':allreceipts,'failure_facts':facts,'new_actual_results':{'financial_configs':42,'candidate_configs':18,'reference_only':24,'cost_scenes':126,'new_native_models':21,'new_parent_configs':21,'new_actual_bank_parents':15,'new_oldbank_ownership_comparisons':6,'passed':6,'rejected_candidates':12,'individual_eachcost_recent6of8':6,'old_readonly_unique_results':12,'full_sensitivity_cells':18,'edges':24,'invalid_attempts_and_curves_retained':0,'matched_actualscale_ungated_complete_NAV_paths':6,'passed_matched_ungated':3,'joint_return_DD_improvements_everycost':0,'global_history_path_novelty_not_claimed':True},'artifacts':artifacts}
put(R/'data_manifest.json',m)
print(json.dumps({'manifest':rel(R/'data_manifest.json'),'artifacts':len(artifacts),'round_bytes':sum(p.stat().st_size for p in R.rglob('*') if p.is_file()),'protected_files':len(ctx['account_hashes_before']),'old_unique_results':len(unique),'all_required_terminal_checks_exit0':True,'failure_facts':len(facts['facts']),'removed_own_reconstructible_files':len(cleanup)}),flush=True)
