"""Seal 27 actual consensus configurations, immutable signal sources and original observers."""
import ast,copy,gzip,hashlib,json,os,platform,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;P=ROOT/'research/experiments/20261030T153707Z'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
read=lambda p:json.loads(p.read_text())
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
dt=lambda x:datetime.fromisoformat(x.replace('Z','+00:00'))
assert not (R/'data_manifest.json').exists()
ctx=read(R/'context.json');start=read(R/'startup.json');plan=read(R/'plan.json');report=read(R/'report.json');old=read(P/'data_manifest.json')
summary=read(R/'sensitivity_summary.json');source=read(R/'source_verification.json');feed=read(R/'feed_verification.json');cv=read(R/'candidate_verification.json');fv=read(R/'forward_verification.json');risk=read(R/'risk_carry_verification.json');state=read(R/'candidate_observation/state.json');im=read(R/'candidate_observation/input_manifest.json');rep=read(R/'representative.json');comp=read(R/'comparison_verification.json');audit=read(R/'verification.json');patch=read(R/'engine_change_verification.json')
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip()==str(ROOT)
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==start['head_after_successful_SSH_fetch']
assert any(len(s.split())>4 and s.split()[1]=='FLOCK' and s.split()[4]==str(start['branch_lock_broker_pid']) for s in Path('/proc/locks').read_text().splitlines())
phases=['initial',*[f'reserve_batch_{i}' for i in range(4)],'evaluate','audit','summary','exports','comparison',*[f'finish_batch_{i}' for i in range(4)],'finish','forward','candidate_checks_retry1','observer_status','review','gates','feed']
required={phase+'_commands.json':read(R/(phase+'_commands.json')) for phase in phases};required['bootstrap_receipt.json']=[read(R/'bootstrap_receipt.json')];required['candidate_finance_and_audit_actual_exit0']=read(R/'candidate_commands.json')[:2]
assert all(x['exit_code']==0 for rows in required.values() for x in rows)
for n in ['definition_check.json','engine_change_verification.json','data_preflight.json','verification.json','comparison_verification.json','export_verification.json','finish_verification.json','visual_inspection.json','source_signal_verification.json','forward_verification.json','candidate_verification.json','risk_carry_verification.json','candidate_validation.json','source_verification.json','feed_verification.json']:
 assert read(R/n)['passed'],n
assert source['new_finished_IDs']==33 and source['registry_append_only_events']==66
assert source['actual_finish_exit0_receipts']==source['actual_reserve_receipts']==27 and source['old_unique_results_unchanged']==21
assert report['summary']['passed']==[] and len(report['summary']['rejected'])==27 and len(report['configs'])==27
assert summary['candidate_grid_cells']==27 and summary['reference_configs']==0 and summary['edges']==36 and summary['read_only_controls']==3
assert report['summary']['positive_configs_by_cost']=={'1':27,'2':27,'3':27}
assert sha(R/'report.json')==source['financial_report_sha256']==summary['report_sha256']==audit['report_sha256']==feed['financial_report_sha256']
assert sha(R/'plan.json')==report['frozen_plan_sha256']
assert audit['cost_scenes_audited']==84 and audit['new_cost_scenes_audited']==81 and audit['full_NAV_points_audited']==45781092
assert audit['source_recorded_trades_checked']==12 and audit['source_recorded_funding_checked']==6660
assert audit['new_native_components']==18 and audit['native_cost_scenes_audited']==54 and audit['actual_fills_independently_verified']==1212
assert audit['actual_funding_settlements_verified_including_flat']==59940 and audit['causal_daily_decisions_checked']==19980
assert audit['funding_feature_decisions_checked']==audit['available_funding_feature_records_independently_checked']==0
assert cv['cumulative_finished_candidate_observations']==135 and cv['elapsed_minutes']==5309 and cv['NAV_points_per_scene']==5432
assert cv['prior_NAV_prefix']==5308 and cv['new_NAV_points_per_scene']==124
assert cv['new_funding_settlements']==6 and cv['new_exact_causal_decisions']==cv['new_fills']==0 and cv['new_closed_hour_risk_checks']==6 and cv['new_risk_proxy_violations']==0
assert fv['NAV_points_per_scene']==41339 and fv['cumulative_minutes']==41309 and fv['new_daily_decisions']==fv['new_executions']==0 and risk['funding08_not_recredited']
assert read(R/'visual_inspection.json')['panels_actually_seen']==18 and ctx['initial_16_missing_actual_results']==0 and len(ctx['prior_conclusions_read'])==242
assert len(ctx['additional_full_reads'])==16 and len(ctx['account_hashes_before'])==17975
binding=read(R/'code_binding_before_evaluation.json')
assert dt(binding['recorded_utc'])<dt(report['evaluation_started_utc']) and dt(read(R/'presentation_plan.json')['recorded_utc'])<dt(report['evaluation_started_utc'])
for path,h in binding['source_sha256'].items():assert sha(ROOT/path)==h,path
assert patch['unchanged_accounting_AST'] and patch['synthetic_vote_and_priority_fixtures']==1485 and patch['synthetic_future_vote_mutations']==1485 and patch['new_engine_sha256']==sha(R/'engine.py')
sys.path.insert(0,str(ROOT/'research/automation'));import registry
records=registry.read_records(ROOT/'research/automation/registry.jsonl');events=registry.read_events(ROOT/'research/automation/registry.jsonl');batch=read(R/'batch.json')
refs=list(plan['all_read_only_references'].values());unique={x['fingerprint']:{**x,'status':x['original_status']} for x in refs}
assert len(unique)==21 and not(set(unique)&{x['fingerprint'] for x in batch})
for x in refs:assert records[x['fingerprint']]['status']==x['original_status'] and records[x['fingerprint']]['report_sha256']==x['report_sha256']
for row in batch:
 sp=read(ROOT/row['spec']);es=[e for e in events if e['fingerprint']==row['fingerprint'] and e['status']=='reserved']
 assert len(es)==1 and es[0]['spec']==sp==records[row['fingerprint']]['spec'] and dt(es[0]['recorded_at_utc'])<dt(report['evaluation_started_utc'])
 assert records[row['fingerprint']]['status']=='rejected' and records[row['fingerprint']]['result_available'] is True
for asset,c in rep['centers'].items():
 assert asset in ['BTC','ETH','COMBO'] and c['status']=='rejected' and c['sensitivity']['neighbor_count']==9 and c['sensitivity']['local_recent6of8_allcost_fraction']==0
for g in summary['groups'].values():assert g['candidate_cells']==9 and g['passed']==0 and g['strict_individual_costfold_passes']==0
put(R/'economic_definition_preservation.json',{'passed':True,'new_complete_financial_specs':27,'new_candidates':27,'new_native_components':18,'new_passive_parents':9,'read_only_unique_results':21,'source_signal_models':18,'source_native_banks':2,'source_cost_curves':6,'old_qualifications_and_curves_unchanged':True,'three_separate_asset_scope_grids':True,'raw_1_1_not_normalized':True,'independent_bank_capitals_usdt':[10000,10000],'fixed_entry_notionals_usdt':[1000,2000],'source_holds_not_rerun':True,'successful_reservations_and_actual_evaluations_per_new_ID':1,'engine_signal_change_with_accounting_preserved':patch,'full_parameter_cells':27,'report_sha256':sha(R/'report.json')})
for path,h in ctx['account_hashes_before'].items():assert sha(ROOT/path)==h,path
for x in old['real_market_inputs']+old['source_annual_and_recent_inputs']:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
sharedpaths=['research/automation/registry.jsonl','research/automation/candidate_forward_latest.json','research/monitor/latest.json','research/monitor/configs.json.gz']
code={p:h for p,h in old['code_and_frozen_source_sha256'].items() if p not in sharedpaths};code.update(plan['helpers'])
for x in refs:
 for key in ['spec','report','archive']:code[x[key]]=x[key+'_sha256']
for path in ['research/experiments/20261030T153707Z/engine.py','research/experiments/20261026T110637Z/prospective_core.py','research/experiments/20261026T110637Z/prospective_observer.py','research/experiments/20261026T090537Z/candidate_prospective_plan.json','research/experiments/20261001T113625Z/forward_plan.json']:code[path]=sha(ROOT/path)
for path,h in code.items():assert sha(ROOT/path)==h,path
facts=read(R/'read_failures.json');attempts=read(R/'candidate_transport_attempts.json');seen={x.get('raw') for x in facts['facts'] if x.get('raw')}
for x in attempts:
 if (x['http_status']!=200 or x['curl_exit_code']!=0) and x['raw'] not in seen:facts['facts'].append({'phase':'candidate_public_GET','eventual_window_successfully_audited':True,**x})
allreceipts={p.name:read(p) for p in R.glob('*_commands.json')};put(R/'all_command_receipts.json',allreceipts)
for filename,rows in allreceipts.items():
 for x in rows:
  if x['exit_code'] and not any(y.get('log')==x['log'] and y.get('exit_code')==x['exit_code'] for y in facts['facts']):facts['facts'].append({'phase':filename,**x})
  if 'curl: (35)' in x.get('stderr',''):
   facts['facts'].append({'phase':'original_SMA_public_GET_transport','command_group':filename,'log':x['log'],'stderr':x['stderr'],'eventual_command_exit_code':x['exit_code'],'eventual_closed_window_audited':True,'individual_failed_attempt_raw_response_was_not_captured':True,'evidence_policy':'Preserve actual stderr/success raw only; do not invent a failed response body or HTTP status.'})
failed=[x for rows in allreceipts.values() for x in rows if x['exit_code']];assert len(failed)==1 and failed[0]['log'].endswith('/risk_carry.log') and read(R/'risk_check_diagnosis.json')['frozen_core_unchanged'];put(R/'read_failures.json',facts)
for p in R.rglob('*.py'):ast.parse(p.read_text(),filename=str(p))
assert len(list(R.glob('*.csv')))==6 and all(b'\r' not in p.read_bytes() for p in R.glob('*.csv'))
put(R/'serialization_check.json',{'passed':True,'CSV_files':6,'all_LF':True,'all_required_actual_terminal_commands_exit0':True,'transport_transient_facts_preserved':len(facts['facts']),'financial_or_observation_reruns':0})
import numpy,polars,matplotlib
put(R/'runtime.json',{'python':sys.version,'executable':sys.executable,'platform':platform.platform(),'packages':{'numpy':numpy.__version__,'polars':polars.__version__,'matplotlib':matplotlib.__version__},'thread_policy':{'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'},'Freqtrade_gitlink':subprocess.check_output(['git','ls-tree','HEAD','Freqtrade'],cwd=ROOT,text=True).strip()})
(R/'candidate_current_pointer.json').write_bytes((ROOT/'research/automation/candidate_forward_latest.json').read_bytes());assert sha(R/'candidate_current_pointer.json')==cv['pointer_sha256']
cleanup=[];path=R/'prepare.py'
if path.exists():
 cleanup.append({'path':rel(path),'sha256':sha(path),'bytes':path.stat().st_size,'reason':'Own reconstructible setup helper; all actual financial/audit code, specs, ledgers, rules and actual failures retained.'});path.unlink()
put(R/'cleanup.json',{'removed':cleanup,'other_files_removed':False,'preexisting_data_normalized_preserved':True})
# Descriptive comparisons use completed reports only; they are no new financial trial.
previous=read(P/'report.json');diversity={};center_comparisons=[]
for asset in ['BTC','ETH','COMBO']:
 current=[c for c in report['configs'].values() if c['asset']==asset];prior=[c for c in previous['configs'].values() if c['asset']==asset]
 diversity[asset]={k:{'current_configs':9,'unique_current_paths':len({c['scenes'][k]['NAV_sha256_f64le'] for c in current}),'configs_matching_a_prior_channel_path':sum(c['scenes'][k]['NAV_sha256_f64le'] in {z['scenes'][k]['NAV_sha256_f64le'] for z in prior} for c in current)} for k in ['1','2','3']}
 new=report['configs'][rep['centers'][asset]['name']];oldcenter=next(c for c in prior if c['entry_lookback_days']==25 and c['exit_lookback_days']==10)
 center_comparisons.append({'asset':asset,'new_center':new['name'],'prior_prespecified_center':oldcenter['name'],'same_capital_notional_dates_and_costs':True,'scenes':{k:{'new_net_return_pct':new['scenes'][k]['net_return_pct'],'old_net_return_pct':oldcenter['scenes'][k]['net_return_pct'],'new_DD_pct':new['scenes'][k]['max_drawdown_pct'],'old_DD_pct':oldcenter['scenes'][k]['max_drawdown_pct'],'new_executions':new['scenes'][k]['executions'],'old_executions':oldcenter['scenes'][k]['executions'],'new_recent40_return_pct':new['scenes'][k]['recent40']['net_return_pct'],'old_recent40_return_pct':oldcenter['scenes'][k]['recent40']['net_return_pct']} for k in ['1','2','3']}})
put(R/'path_diversity.json',{'passed':True,'report_sha256':sha(R/'report.json'),'prior_report_sha256':sha(P/'report.json'),'groups':diversity,'financial_evaluations':0,'different_parameters_are_new_configs_but_same_NAV_is_not_independent_evidence':True})
put(R/'source_center_comparison.json',{'passed':True,'financial_evaluations':0,'descriptive_only_not_new_qualification':True,'new_report_sha256':sha(R/'report.json'),'prior_report_sha256':sha(P/'report.json'),'rows':center_comparisons})
nextpriority='All27 nine-channel consensus variants failed unchanged monthly/recent5dfold/strict-neighborhood gates, despite allcost annualnetpositive. Do not rerun these exact finished configurations or tune E8/H1 to chase this history. Prior ROC/S-boundary direction remains retired for now. Next hypothesis proposal: price-relative BTC/ETH hourly spread mean-reversion, not another directional channel aggregation. First inspect complete registry and existing pairs/hedge code for exact economic duplicates and real results. Proposed rolling720completedhour OLS of logETH on intercept+logBTC, fitted on prior hours EXCLUDING tested closed hour; zscore tested closedhour residual using prior training residual sample mean/std. No future prices/funding or OOS threshold selection, no cointegration/profit claim. Entry absz [2,2.5,3], exit absz [.5,1,1.5],preset2.5/1,maximumholding48hours;noentryif beta outside[.5,2] orzero/invalidresidualstd. Above positive entry threshold shortETH/longBTC,negative reverse;fixedETHentrynotional2000 andBTCbeta*2000,eachindependent10000bank,total20000/raw[1,1],actualnativeLOT/adversetick and no resizing while held. Execute after signal at next hourly+1minute OPEN;pair reversal/oneleg rejection/unwind/terminal and margin failure rules must be fully fixed before reserve, never assume atomic costfree fills. True per-leg fees/spread/slip/ADVimpact and realizedfunding,postfee1xcollateral/hourmarkrisk;no crossmargin or spotborrow invented. Same370dayOOS is feasible only after verifying prior720h availability with33context; preserve12x30d+10tail/recent40inherited/1/2/3cost and unchangedstrictgates,otherwise record blocked with true data insufficiency. Freeze complete engine/spec/code/time/parameters before any actual variant, reserve every evaluated paired configuration;reuse only genuinely identical completed components. This is planning only, zero new pair reservations/evaluations now. Reused history remains development, no untouched final test/independentfuture/liveprofit. OriginalSMA65/singleS28 andpaper10 continue original frozen rules.'
proposal={'status':'planning_only_not_tested','financial_evaluations':0,'reservations':0,'direction':'Causal rolling hourly BTC/ETH relative-price spread mean-reversion','rolling_training_completed_hours':720,'tested_hour_excluded_from_training':True,'entry_abs_z':[2,2.5,3],'exit_abs_z':[.5,1,1.5],'prespecified_center':{'entry_abs_z':2.5,'exit_abs_z':1},'maximum_holding_hours':48,'eligible_beta_interval':[.5,2],'ETH_entry_notional_usdt':2000,'BTC_entry_notional_usdt':'beta_at_entry*2000','independent_bank_capitals_usdt':[10000,10000],'raw_funded_bank_units':[1,1],'total_capital_usdt':20000,'implementation_choices_still_required_before_reserve':['Exact two-leg execution, partial rejection, immediate unwind, reversal and terminal rules','Missing-hour and invalid fit handling, risk/margin failure and funding event ordering','Exact novelty against all previous pairs and hedged results','Training-only stationarity diagnostics if used; never retrospective test filtering'],'complete_next_round_requirements':nextpriority}
put(R/'next_direction_proposal.json',proposal)
put(R/'direction_review.json',{'passed':True,'meaning':'All actual finished consensus configurations rejected by unchanged preregistered qualification gates. This post-result research direction choice is not a claimed preregistered stopping rule.','actual_candidates':27,'strict_individual_costfold_passes':0,'passed_candidates':0,'groups':summary['groups'],'centers':rep['centers'],'old_qualifications_unchanged':True,'no_boundary_expansion_or_gate_relaxation_after_results':True,'next_direction_proposed_only':proposal['direction'],'financial_evaluations_in_decision':0,'report_sha256':sha(R/'report.json')})
oldnext=read(P/'next_research_state.json')
nextstate={'round':R.name,'plan':rel(R/'plan.json'),'plan_sha256':sha(R/'plan.json'),'report':rel(R/'report.json'),'report_sha256':sha(R/'report.json'),'spec':rel(R/'spec.json'),'actual_new_financial_configs':27,'new_native_components':18,'new_passive_parents':9,'passed_candidates':0,'rejected_candidates':27,'new_cost_scenes':81,'all_results_finished':True,'read_only_source_results':unique,'source_signal_models_reused':18,'centers':rep['centers'],'groups':summary['groups'],'path_diversity':diversity,'engine_change':patch,'next_research_priority':nextpriority,'next_direction_planning_only':proposal,'prior_ROC_S_boundary_direction_retired_for_now':copy.deepcopy(oldnext['prior_ROC_S_boundary_direction_retired_for_now']),'original_SMA':copy.deepcopy(oldnext['original_SMA']),'original_candidate':copy.deepcopy(oldnext['original_candidate']),'monitor':copy.deepcopy(oldnext['monitor']),'paper10_policy':oldnext['paper10_policy'],'independent_future_qualified':False,'supplementary_check_correction':{'diagnosis':rel(R/'risk_check_diagnosis.json'),'failed_code':rel(R/'check_risk_carry_initial.py'),'successful_receipts':rel(R/'candidate_checks_retry1_commands.json'),'no_financial_or_observation_rerun':True}}
nextstate['original_SMA'].update(state=rel(R/'forward_state.json'),state_sha256=sha(R/'forward_state.json'),report=rel(R/'forward_report.json'),report_sha256=sha(R/'forward_report.json'),cutoff_utc='2026-10-30T16:30:00Z',NAV_points=41339,elapsed_minutes=41309,next_window='16:30to18:30 spot closed marks; keep original float cash/quantity/desired/trades/costs, no perp funding/reset/forcedexit. Use saved65daily context separately from latest minute-array input.')
nextstate['original_candidate'].update(saved_pointer=rel(R/'candidate_current_pointer.json'),saved_pointer_sha256=sha(R/'candidate_current_pointer.json'),state=rel(R/'candidate_observation/state.json'),state_sha256=sha(R/'candidate_observation/state.json'),report=rel(R/'candidate_observation/report.json'),report_sha256=sha(R/'candidate_observation/report.json'),delta=rel(R/'candidate_observation/delta.json.gz'),delta_sha256=sha(R/'candidate_observation/delta.json.gz'),cutoff_utc='2026-10-30T16:30:00Z',observations=135,NAV_points=5432,elapsed_minutes=5309,books=state['books'],risk=state['risk'],last_actual_funding_cashflows=cv['independent_funding_cashflows'],next_window='16:30to18:30 derive real packet, do not assume zero events. Actual16:00:00 funding1793376000000000000 already credited;BTC receives .093099965652168 per costunamplified,ETHflat0. KeepBTCq-.012/cash/entry andETHflat. Current16hour BTCrisk has two stored same-ns states, prefundthenpostfund;prefundzero duration is skipped by frozen positive-duration risk rules, do not change/compress core/state. OriginalsingleS28/BTCN1000/ETHN3000/banks10000each unchanged. NextdailyOct31UTC00:01 andfrozen180dayendApr25 unchanged.')
nextstate['monitor'].update(research_rows=feed['research_configs'],old_rows_unchanged=feed['historical_rows_identical'],paper_observations=feed['paper_observations'],paper_accounts=feed['paper_accounts'],gzip_bytes=(ROOT/'research/monitor/configs.json.gz').stat().st_size)
put(R/'next_research_state.json',nextstate)
text=(R/'result.md').read_text()+'\n封存结论：27项在1/2/3倍成本下全期均净正，但全部完整月折不足9/12、近期五日折不足6/8且严格邻域率0，全部rejected；19项近期40日未能各成本净正。新共识改善了年度收益，并未形成严格稳健平台。\n\n'
for a,c in rep['centers'].items():text+=f"{a}事前E6/H3中心：三倍净收益{c['return3_pct']:.6f}%、完整DD{c['whole_DD3_pct']:.6f}%、近期40日{c['recent_return3_pct']:.6f}%，各成本正五日折"+'/'.join(str(c['positive_recent_folds_by_cost'][str(k)]) for k in [1,2,3])+'（原门槛各≥6/8）。\n\n'
text+='同本金/名义/时间/成本的上一轮事前25/10中心比较另存source_center_comparison.json，仅描述已有报告，不产生新回测或替代资格门槛。部分新参数的实际NAV与旧通道或本批其他参数完全相同，逐币种/成本哈希去重见path_diversity.json；27个新定义不是27份独立市场证据。\n\n'
text+=f"实际独审exit0：84场景共45,781,092完整NAV点（81新、3旧父组合），1,176整体/逐折与756近期/分折指标。54新单币场景独立核对{audit['actual_fills_independently_verified']}成交、59,940资金费结算、19,980因果日决策及{audit['independent_state_hour_margin_checks']}闭合小时/状态风险检查；另核对18源信号模型的19,980个pre-OPEN方向、三成本一致及排除被测收盘的通道边界。两旧常持银行6曲线只读核对12成交与6,660资金费；21旧来源与{len(ctx['account_hashes_before'])}受保护文件保持，原金融核算及账户冻结规则不改。6CSV逐值核验和3图18面板实际查看完成。\n\n"
text+='原冻结SMA65和singleS28仅续14:30至16:30 UTC：累计41339点/41309分钟及135观察ID/5432点/5309分钟。本窗0新日决策/成交，真实16:00整点资金费产生6条各资产/成本记录，BTC空仓位q=−0.012在mark77583.30471014、rate0.0001下每成本收入0.093099965652168，收入不放大；ETH空仓金额0。08:00:00.001未重复入账。现金按实际资金费更新，数量/entry保持，6闭合小时风险检查0违规。\n\n'
text+='补充检查首次exit1：我误要求风险栈时间严格递增，实际冻结core在16:00整点闭合小时mark(code2)与资金费(code4)前后保留同纳秒两状态，原独审已正确只检查正持续时段。仅将补充检查改为事件非递减顺序，并逐项要求同纳秒现金差等于真实资金费、数量和entry相等、终态等于原账本，复查exit0。失败源码、日志、诊断及成功复查回执保留；没有更改/压缩风险栈、重跑观察窗口、重新reserve或重置账户。下窗按实际packet继续，不预设整点/零资金费。\n\n'
text+=f"27金融配置全部各自reserve/实际计算/finish，加6原冻结观察，共33新完成ID与66追加事件。必要登记检查、同锁只读snapshot/monitor检查和新旧网页行核验实际exit0，网页研究{feed['research_configs']}行、10账户{feed['paper_observations']}观察、gzip{(ROOT/'research/monitor/configs.json.gz').stat().st_size}字节；不产生十策略新成交、不重部署网页。当前read_failures共{len(facts['facts'])}条真实事实（含读取上一轮已清理准备脚本及本次补充检查失败），公共GET均以实际响应/日志为准，不虚构失败记录。\n\n"
text+='下轮仅提出价格相对的BTC/ETH小时残差价差均值回复，滚动720已完成小时拟合（排除被测小时）、E2/2.5/3×X0.5/1/1.5、中心2.5/1及48小时最长持有，仅为待查重/补全双腿执行规则的计划，零reserve/零实际结果，不称协整或可盈利。下一轮先核对已有pairs精确配置和可复用引擎，完整冻结/成本约束及逐项reserve后才能计算。原SMA65/singleS28及paper10继续冻结规则，不采用共识或价差新规则。\n\n'
text+='全部正负折、淘汰结果、账本、冻结规则和核验必要证据保留，仅清理本轮可重建准备助手。原data/normalized保持。封存后main提交/push、完整远端tree/blob、发布进程exit0与解锁证明见.git/automation_proofs/20261030T173813Z.json；不以预写SHA代替真实发布状态。\n'
(R/'result.md').write_text(text)
(R/'reproduce.md').write_text('''# 复现与只读核验

固定目录/home/desktop/Documents/Codex/EquiTide、main only、持有research/automation/branch.lock。解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python，环境PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1，版本见runtime.json。

实际命令、时间、退出和stdout/stderr日志见all_command_receipts：bootstrap→initial（数据、1485票数/1485未来扰动、冻结、定义）→reserve_batch_0..3（8/8/8/3）→evaluate一次→audit→summary/exports/comparison→finish_batch_0..3/finish→forward→candidate。candidate原账户执行和独审exit0，后补充risk_carry检查因严格递增假设exit1，失败原样保留。只执行candidate_checks_retry1复查/索引现有3ID，未重新GET/执行账户/登记；其后observer_status/review/gates/feed全部exit0。

完整规则和27spec见plan.json/specs。E5/6/7×H2/3/4，中心6/3；源N20/25/30×M5/10/15九格的pre-OPEN方向三成本一致且独立因果核验，排除被测收盘，无源当次OPEN/fill/PnL/funding特征。原交易/资金费/风险/数据/统计函数AST保持，完整代码在计算前绑定。BTC/ETH银行各10000，固定名义1000/2000；父raw[1,1]总20000，不归一化或缩放旧NAV。18新native真实执行，9父组合复用新NAV；18源信号与3旧常持只读，均未重新金融回测。

已有结果只读复核，不重复reserve或evaluate：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T173813Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T173813Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T173813Z/forward.py --reproduce
```

独审整数源信号/Fraction数量/Decimal成交费用、实际纳秒资金费、小时状态风险/完整NAV与逐折。84场景45,781,092点、6CSV逐值、3图18面板实际查看。数据清单保留8真实Parquet/16来源输入与公共原响应SHA，缺数据即停止，不合成。原始行情留ignoreddata，必要账本/规格/代码/实际失败证据保留。

原冻结SMA65/singleS28从14:30至16:30续接，原规则/本金/数量/entry保持。本窗原singleS28实际16:00整点funding每成本BTC+.093099965652168、ETH0，6流水/124新增NAV点，累计135ID/5432点/5309分钟；6闭合小时风险检查0违规。原core保留同纳秒pre/postfund状态，只有正持续区间计风险；失败补充检查改为验证这种实际语义，未改core/状态/报告。下一窗16:30至18:30按真实packet续接，16资金费已计入不重记，次日00:01决策与180日终点保持；SMA65旧日上下文在next_research_state保留。两旧延迟shadow不称十策略实时报价模拟。

33新完成ID/66追加事件，全部正收益/负折/淘汰保存。27配置全期三成本净正仍全部月折/近期5日折/邻域严格门槛失败；新参数重复旧/本批NAV不构成独立市场证据，见path_diversity。21旧结果与17975保护文件哈希不变。next_direction_proposal仅未测试价差假设，零新reserve/计算，下一轮先查重、补全双腿执行/失败规则、冻结和登记，不能据此称协整/盈利。

所有必要登记/只读snapshot/monitor检查在同main锁内实际执行，paper10仅汇总已有10账户190观察，网页读取main不重部署。publish.py提交推送main，再fetch/独立lsremote/全递归tree及所有必要blob与原输入哈希核验；发布进程实际exit0后释放本人锁。实际SHA、进程退出、解锁和发布后核验见.git/automation_proofs/20261030T173813Z.json。以后其他任务正常推进按保存pointer/本轮commit核验，不回滚共享账户或main。
''')
pp=R/'implementation_plan.md';pp.write_text(pp.read_text().replace('- [ ]','- [x]')+'\n研究及最终必要检查完成，补充检查一次失败/修正留档；实际main发布与解锁见.git证明。\n')
rawpaths={x['raw'] for x in attempts}|{im['packet']};rawartifacts=[{'path':p,'sha256':sha(ROOT/p),'bytes':(ROOT/p).stat().st_size} for p in sorted(rawpaths)]
fr=read(R/'forward_report.json');shared={p:{'sha256':sha(ROOT/p),'bytes':(ROOT/p).stat().st_size} for p in sharedpaths}
artifacts={rel(p):sha(p) for p in sorted(R.rglob('*')) if p.is_file() and p.name!='data_manifest.json'}
assert not any(p.name=='__pycache__' or 'checkpoint' in p.name or p.suffix in ['.pyc','.npy','.tmp'] for p in R.rglob('*'))
m={'round':R.name,'recorded_at_utc':now(),'working_directory':str(ROOT),'branch':'main','base_commit':start['head_after_successful_SSH_fetch'],'branch_lock_broker_pid':start['branch_lock_broker_pid'],'initial_main_branch_verification':read(R/'main_only_branch_check.json'),'frozen_plan_sha256':sha(R/'plan.json'),'finished_report_sha256':sha(R/'report.json'),'finished_forward_report_sha256':sha(R/'forward_report.json'),'finished_candidate_report_sha256':sha(R/'candidate_observation/report.json'),'real_market_inputs':old['real_market_inputs'],'source_annual_and_recent_inputs':old['source_annual_and_recent_inputs'],'forward_raw_responses':fr['provenance'],'observer_preflight_raw_responses':[],'candidate_raw_artifacts':rawartifacts,'candidate_input_manifest':im,'prospective_readiness':{'actual_candidate_observations':135,'new_actual_observation_IDs':3,'original_frozen_rules_unchanged':True,'current_cutoff_utc':'2026-10-30T16:30:00Z'},'registry':{'main_sha256_before_reserve':ctx['main_registry_sha256_before_reserve'],'before_events':ctx['registry_events'],'before_IDs':ctx['registry_ids'],'append_only_events':66,'new_finished_IDs':33,'financial_IDs':27,'invalid_financial_attempts':0},'read_only_source_results':unique,'code_and_frozen_source_sha256':code,'protected_inputs_sha256':ctx['account_hashes_before'],'shared_files':shared,'required_command_receipts':required,'all_command_receipts':allreceipts,'failure_facts':facts,'new_actual_results':{'financial_configs':27,'candidate_configs':27,'reference_only':0,'cost_scenes':81,'new_native_models':18,'new_parent_configs':9,'source_bank_curves_reused':6,'source_signal_models_reused':18,'source_preexecution_targets_checked':19980,'passed':0,'rejected_candidates':27,'individual_eachcost_recent6of8_full_grid':0,'old_readonly_unique_results':21,'full_sensitivity_cells':27,'separate_asset_scope_grids':3,'edges':36,'invalid_attempts_and_curves_retained':0,'nonfinancial_supplement_failure_preserved':1,'positive_configs_by_cost':report['summary']['positive_configs_by_cost'],'prespecified_centers':rep['centers'],'all_old_registry_qualifications_unchanged':True,'signal_engine_change_with_old_accounting_verified':True,'new_direction_only_proposed_not_evaluated':True,'independent_future_validated':False},'artifacts':artifacts}
put(R/'data_manifest.json',m)
print(json.dumps({'manifest':rel(R/'data_manifest.json'),'artifacts':len(artifacts),'round_bytes':sum(p.stat().st_size for p in R.rglob('*') if p.is_file()),'protected_files':len(ctx['account_hashes_before']),'old_unique_results':len(unique),'all_final_required_checks_exit0':True,'actual_failure_facts_preserved':len(facts['facts']),'financial_or_observation_reruns':0,'passed_candidates':0,'removed_own_reconstructible_files':len(cleanup)}),flush=True)
