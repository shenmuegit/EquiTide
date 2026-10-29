"""Seal actual research,original accounts,provenance and required next state."""
import gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
read=lambda p:json.loads(p.read_text())
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
assert not(R/'data_manifest.json').exists()
startup=read(R/'startup.json');ctx=read(R/'context.json');plan=read(R/'plan.json');report=read(R/'report.json');summary=read(R/'summary.json');source=read(R/'source_verification.json');feed=read(R/'feed_verification.json');candidate=read(R/'candidate_verification.json');forward=read(R/'forward_verification.json');im=read(R/'candidate_observation/input_manifest.json');state=read(R/'candidate_observation/state.json');risk=read(R/'risk_carry_verification.json')
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip()==str(ROOT)
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==startup['head_after_successful_SSH_fetch']
assert any(len(s.split())>4 and s.split()[1]=='FLOCK' and s.split()[4]==str(startup['branch_lock_broker_pid']) for s in Path('/proc/locks').read_text().splitlines())
phases=['initial','evaluate','audit_retry','summary','exports','finish','forward','candidate','observer_status','gates','monitor_final','feed']
required={name+'_commands.json':read(R/(name+'_commands.json')) for name in phases}
for name in ['reserve_batch_commands.json','finish_batch_commands.json','finish_recovery_1_commands.json','finish_recovery_2_commands.json','review_effective_commands.json']:required[name]=read(R/name)
assert all(x['exit_code']==0 for rows in required.values() for x in rows)
for p in ['verification.json','export_verification.json','finish_verification.json','forward_verification.json','candidate_verification.json','risk_carry_verification.json','candidate_validation.json','source_verification.json','feed_verification.json']:assert read(R/p)['passed'],p
assert source['new_finished_IDs']==46 and source['registry_append_only_events']==92 and source['old_unique_results_unchanged']==22
assert summary['passed']==0 and summary['rejected_candidates']==36 and summary['candidate_eachcost_recent6of8_count']==6
assert sha(R/'report.json')==source['financial_report_sha256']==feed['financial_report_sha256']==summary['report_sha256']==read(R/'verification.json')['report_sha256']
assert candidate['cumulative_finished_candidate_observations']==96 and candidate['NAV_points_per_scene']==3835 and candidate['elapsed_minutes']==3749 and candidate['new_funding_settlements']==candidate['new_exact_causal_decisions']==candidate['new_fills']==0 and risk['passed']
assert forward['NAV_points_per_scene']==39778 and forward['cumulative_minutes']==39749 and forward['new_daily_decisions']==forward['new_executions']==0
assert read(R/'main_only_branch_check.json')['passed'] and read(R/'visual_inspection.json')['panels_actually_seen']==18
for path,h in ctx['account_hashes_before'].items():assert sha(ROOT/path)==h,path
oldmanifest=read(ROOT/'research/experiments/20261029T132528Z/data_manifest.json')
for item in oldmanifest['real_market_inputs']+oldmanifest['source_annual_and_recent_inputs']:assert sha(ROOT/item['path'])==item['sha256'] and (ROOT/item['path']).stat().st_size==item['bytes']
refs=[*plan['component_sources'].values(),*plan['read_only_anchor_references'].values(),*plan['read_only_hold_references'].values()];unique={x['fingerprint']:x for x in refs};assert len(unique)==22
sharedpaths=['research/automation/registry.jsonl','research/automation/candidate_forward_latest.json','research/monitor/latest.json','research/monitor/configs.json.gz']
code={p:h for p,h in oldmanifest['code_and_frozen_source_sha256'].items() if p not in sharedpaths}
code.update(plan['helpers'])
for x in refs:
 for name in ['spec','report','archive']:code[x[name]]=x[name+'_sha256']
for p in ['research/experiments/20261029T092426Z/run.py','research/experiments/20261029T132528Z/engine.py','research/experiments/20261025T205634Z/audit.py','research/experiments/20261026T110637Z/prospective_core.py','research/experiments/20261026T110637Z/prospective_observer.py','research/experiments/20261026T090537Z/candidate_prospective_plan.json','research/experiments/20261001T113625Z/forward_plan.json']:code[p]=sha(ROOT/p)
for p,h in code.items():assert sha(ROOT/p)==h,p
cleanup=[];temp=R/'audit_pre_import_fix.py'
if temp.exists():
 restored=(R/'audit.py').read_text().replace("R/'audit_helpers.py'","ROOT/'research/experiments/20261025T205634Z/audit.py'")
 assert restored.encode()==temp.read_bytes();cleanup.append({'path':rel(temp),'bytes':temp.stat().st_size,'sha256':sha(temp),'reason':'Reconstructible audit import precursor;actual failure logs,original function source and fix metadata retained.'});temp.unlink()
put(R/'cleanup_intermediates.json',{'removed_own_reconstructible_files':cleanup,'removed_count':len(cleanup),'account_ledgers_frozen_rules_registry_and_required_audit_evidence_preserved':True,'no_other_work_cleaned':True})
(R/'candidate_current_pointer.json').write_bytes((ROOT/'research/automation/candidate_forward_latest.json').read_bytes())
assert sha(R/'candidate_current_pointer.json')==candidate['pointer_sha256']
facts=read(R/'read_failures.json')
put(R/'review_resolution.json',{'passed':True,'financial_evaluations_repeated':0,'original_report_status_bytes_preserved':True,'audit_interface':'audit.log exit1;exact original utility bodies isolated;actual audit_retry exit0/full65401560points.','source_count':'Review literal21 omitted oldconstantlong parent;pre-reserve inventory22 correct;all22hash/status checks actual retryexit0.','finish_driver':'Actual exit143,causeunknown;31completed events retained,1unacknowledgedcompletion reconciled;only9reserved IDs finished in8+1calls.40financial+6partial IDs finished;92events append-only.','transport':'SMA curl2TLSerrorlines before successful200;candidate1failedTLSattempt rawgzip preserved then8successful200pages.Bothaccountaudits/forwardexactreproduce exit0.','monitor':'Initialregistry/snapshot/checkexit0;aftercorrectedreviewexit0,finalsnapshot/checkexit0;feedall8317oldrowsunchanged.','generation':'Initial finalizer generation here-doc had nested-string SyntaxError before any file/finance mutation;direct source generation corrected.','failures_preserved_in':'read_failures.json and original logs/receipts','failure_fact_records':len(facts['facts'])})
nextstate={'round':R.name,'branch_policy':'main only;fixed root;no subagents/orders/branches/worktrees','report':rel(R/'report.json'),'report_sha256':sha(R/'report.json'),'plan':rel(R/'plan.json'),'plan_sha256':sha(R/'plan.json'),'context':rel(R/'context.json'),'initial16_missing_actual_results':0,'finished_financial_configs':40,'finished_candidates':36,'finished_reference_only':4,'new_native_models':0,'passed':0,'rejected_candidates':36,'source_native_reused':12,'source_cost_curves':36,'complete_sensitivity':{'axes':plan['grid'],'old9qualification_unchanged':True,'edges':96,'strict_eachcost6of8_individually':6,'all36failed_strict_neighbor_plateau':True},'best_observed':summary['best_new'],'qualification_fragility':{'path':rel(R/'qualification_fragility.json'),'sha256':sha(R/'qualification_fragility.json')},'next_research_priority':'No exactrepeat. RawBTC0.5/ETH1.5 at allE andS28/29 achieved recent6of8 at1/2/3x,but adjacentw0.75columnfell5of8;all36failed predeclared>=60percent strict-fold neighborhood.Bestnew3x10.9028percent/DD3.19075percent is on lowerBTCweight gridboundary.A future separately preregistered allocation neighborhood may test narrowfoldsigncliff;do not expand this round,relax gates,or call reusedhistory untouched/futurevalidated.Native models notrerun;ownershipindex not pooledexecutioncapacity.OriginalsingleS28/SMA65 unchanged.','original_SMA':{'state':rel(R/'forward_state.json'),'state_sha256':sha(R/'forward_state.json'),'report':rel(R/'forward_report.json'),'report_sha256':sha(R/'forward_report.json'),'cutoff_utc':'2026-10-29T14:30:00Z','NAV_points':39778,'elapsed_minutes':39749,'next_expected_mark_only_cutoff_utc':'2026-10-29T16:30:00Z','next_daily_decision_utc':'2026-10-30T00:01:00Z','most_recent65daily_context':{'path':'research/experiments/20261029T012253Z/forward_inputs.json.gz','sha256':sha(ROOT/'research/experiments/20261029T012253Z/forward_inputs.json.gz')},'frozen_terminal_plan_unchanged':'2027-03-31'},'original_candidate':{'pointer':'research/automation/candidate_forward_latest.json','pointer_snapshot':rel(R/'candidate_current_pointer.json'),'pointer_snapshot_sha256':sha(R/'candidate_current_pointer.json'),'state':rel(R/'candidate_observation/state.json'),'state_sha256':sha(R/'candidate_observation/state.json'),'report':rel(R/'candidate_observation/report.json'),'report_sha256':sha(R/'candidate_observation/report.json'),'delta':rel(R/'candidate_observation/delta.json.gz'),'delta_sha256':sha(R/'candidate_observation/delta.json.gz'),'completed_observation_IDs':96,'cutoff_utc':'2026-10-29T14:30:00Z','NAV_points':3835,'elapsed_minutes':3749,'daily_context_bars_per_asset':35,'daily_NAV_boundaries_per_scene':3,'new_fills':0,'new_funding_entries':0,'14hour_one_state_stacks_carried':True,'BTC_signed_units':'-0.012000000000000000','cash_and_entries':state['books'],'next_window':'Continue originalsingleS28 from14:30to16:30;includesactual16UTCfunding.Capture actualsettlementns/mark/rate,apply preexisting signedq/cash exactlyonce,outflowsstress/incomeunamplified.Preserve subsecondpre/postcashriskstates andpositive-overlapdurations;closed14/15hours checked at15/16closes,current16hourfundingstates carried.Neverrecredit prior00/08.NextdailyOct30UTC00:01.No rule,weight oraccountswitch.','frozen180day_end_utc':'2027-04-25T00:01:00Z','mode':'delayedclosedbar/funding reconstruction;not livequote/paper10 execution or stableprofit'},'monitor':{'research_rows':feed['research_configs'],'historical_rows_unchanged':feed['historical_rows_identical'],'paper_observations':feed['paper_observations'],'paper_accounts':feed['paper_accounts'],'gzip_bytes':(ROOT/'research/monitor/configs.json.gz').stat().st_size,'budget_bytes':4000000},'registration_note':'Driverexit143unknowncause recoveredwithoutduplicatefinish/financialrerun.Prefer one<=8realregistrybatch percall;retainactualreceipts.','paper10_policy':'Readonly;btc-eth-2 owns existingfrozenaccounts/observations.'}
put(R/'next_research_state.json',nextstate)
with (R/'result.md').open('a') as f:
 f.write('\n最终实际核验：40金融定义/120成本场景全部finish，36候选淘汰、4恒多参考；46实际ID/92事件仅追加。独立回放12原生/36曲线、1920成交与39960资金费账本，65401560完整NAV点、1680全期/逐折及1080近期/逐折指标通过；22旧来源资格/哈希与14546保护文件保持。\n')
 f.write('只有BTC原值0.5/ETH1.5、S28或29的6格达到每档近期6/8；邻列w0.75均5/8，全36不满足事前严格邻域60%门槛，未放宽或事后扩网格。最佳3倍370日净收益10.9028167337%、整体DD3.1907499633%，仅边界观测而非合格/最优/稳定实盘收益。\n')
 f.write('原候选累计96观察ID、3835点/场景、3749分钟；本窗122新NAV动作、0决策/成交/资金费，12/13闭合小时6个BTC成本风险检查且0违规，当前14小时状态承接。旧SMA累计39778点、39749分钟、0新日决策/成交；原SMA65与候选单S28规则、资金、数量、费用前缀保留。下一16:30候选窗口须计实际16时资金费一次并保留精确纳秒前后现金/风险状态。\n')
 f.write(f'登记门禁与最终只读监控实际exit0：{feed["research_configs"]}研究行、{feed["paper_observations"]}既有观察/10账户；{feed["historical_rows_identical"]}旧展示行完整字典相同。3图18面板已实际打开，数据与导出逐项核验。\n')
 f.write('实际异常均留档：rg缺失；独审旧模块导入接口失败；旧对照计数硬编码少1；finish进程exit143原因未知，保留31完成只续9未完成；SMA2行TLS重试与候选1次TLS失败后成功；finalizer源码初次嵌套字符串生成失败。均已在真实证据基础上恢复，金融计算未重跑。全部原始日志/退出/失败与恢复见read_failures.json、review_resolution.json。\n')
 f.write('仅移除可重建的审计导入修复前副本，SHA及重建关系留cleanup_intermediates.json；完整账本、规则、结果、登记及必要核验代码保留。实际发布状态和commit SHA以.git/automation_proofs/20261029T152659Z.json为准，本说明不预先声称push成功。\n')
(R/'reproduce.md').write_text("""# 复现与核验

固定工作目录 `/home/desktop/Documents/Codex/EquiTide`，Python `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。每个spec先成功reserve；40金融及6partial均已finish，禁止对正式登记重复reserve/evaluate/finish或重开账户。

实际命令/原始exit/log在各 `*_commands.json`、reserve_batches及finish_batches；失败与恢复均保留。required_command_receipts选取实际有效完成凭据，不表示原始运行从未失败。finish_interruption_reconciliation.json绑定那个已完成但未收到进程回执的terminal事件。

本轮封存版本可执行：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T152659Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T152659Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T152659Z/forward.py --reproduce
```

审计从已保存真实成交/资金费独立回放原生NAV，按结构化(ns,eventcode)逐点归属加权；不调用源信号/交易模型。所有Parquet、16年度/近期源、源spec/report/archive及代码SHA见data_manifest。未进Git的大行情及公开HTTPpacket原字节留ignoreddata；缺失任何SHA匹配输入必须停止，不可合成替代。

审计保护当轮账户快照：未来paper10或候选正常继续后，共享状态/监控可能不同，防护应阻止混入未来账户。读取本轮提交blob与完整只读代码/账本核验历史，不为通过旧审计回滚正式main、共享账户或切分支；当时候选pointer原字节另存candidate_current_pointer.json。原候选独审实际命令见candidate_commands.json，原SMA精确回放实际exit0见forward_commands.json。

这是原固定规模银行净值的静态所有权，复现不得归一化、重设N、线性缩放订单解释非线性冲击、重算源模型或新增父层成交。旧资格不变，完整正负结果均在report及results归档。
""")
p=R/'implementation_plan.md';p.write_text(p.read_text()+'\n所有实际异常、未知原因exit143及恢复见review_resolution.json；金融定义各执行一次。发布状态以.git实际完成证明为准。\n')
rawpaths={x['raw'] for x in read(R/'candidate_transport_attempts.json')}|{im['packet']}
rawartifacts=[{'path':p,'sha256':sha(ROOT/p),'bytes':(ROOT/p).stat().st_size} for p in sorted(rawpaths)]
forwardrep=read(R/'forward_report.json')
shared={p:{'sha256':sha(ROOT/p),'bytes':(ROOT/p).stat().st_size} for p in sharedpaths}
artifacts={rel(p):sha(p) for p in sorted(R.rglob('*')) if p.is_file() and p.name!='data_manifest.json'}
assert not any(p.name=='__pycache__' or 'checkpoint' in p.name or p.suffix in ['.pyc','.npy','.tmp'] for p in R.rglob('*'))
manifest={'round':R.name,'recorded_at_utc':now(),'working_directory':str(ROOT),'branch':'main','base_commit':startup['head_after_successful_SSH_fetch'],'branch_lock_broker_pid':startup['branch_lock_broker_pid'],'initial_main_branch_verification':read(R/'main_only_branch_check.json'),'frozen_plan_sha256':sha(R/'plan.json'),'finished_report_sha256':sha(R/'report.json'),'finished_forward_report_sha256':sha(R/'forward_report.json'),'finished_candidate_report_sha256':sha(R/'candidate_observation/report.json'),'real_market_inputs':oldmanifest['real_market_inputs'],'source_annual_and_recent_inputs':oldmanifest['source_annual_and_recent_inputs'],'forward_raw_responses':forwardrep['provenance'],'observer_preflight_raw_responses':[],'candidate_raw_artifacts':rawartifacts,'candidate_input_manifest':im,'prospective_readiness':{'actual_candidate_observations':96,'new_actual_observation_IDs':3,'original_frozen_rules_and_plan_unchanged':True,'current_cutoff_utc':'2026-10-29T14:30:00Z','pointer_snapshot':{'path':rel(R/'candidate_current_pointer.json'),'sha256':sha(R/'candidate_current_pointer.json')}},'registry':{'main_sha256_before_reserve':ctx['main_registry_sha256_before_reserve'],'before_events':ctx['registry_events'],'before_IDs':ctx['registry_ids'],'append_only_events':92,'new_finished_IDs':46,'financial_IDs':40,'acknowledged_financial_finish_exit0_receipts':39,'completed_before_interrupted_acknowledgement_reconciled':1},'read_only_source_results':unique,'code_and_frozen_source_sha256':code,'protected_inputs_sha256':ctx['account_hashes_before'],'shared_files':shared,'required_command_receipts':required,'original_failures_and_recoveries':read(R/'review_resolution.json'),'failure_facts':facts,'new_actual_results':{'financial_configs':40,'candidates':36,'reference_only':4,'cost_scenes':120,'new_native_models':0,'passed':0,'rejected_candidates':36,'eachcost6of8_individually':6,'strict_neighborhood_passes':0},'artifacts':artifacts}
put(R/'data_manifest.json',manifest)
print(json.dumps({'manifest':rel(R/'data_manifest.json'),'artifacts':len(artifacts),'round_bytes':sum(p.stat().st_size for p in R.rglob('*') if p.is_file()),'protected_files':len(ctx['account_hashes_before']),'old_unique_results':22,'all_required_actual_command_exits0':True,'original_failure_fact_records':len(facts['facts']),'own_reconstructible_files_removed':len(cleanup)}),flush=True)
