"""Seal 27 actual channel configurations, immutable controls and frozen observers."""
import ast,copy,gzip,hashlib,json,os,platform,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;P=ROOT/'research/experiments/20261030T133537Z'
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
phases=['initial',*[f'reserve_batch_{i}' for i in range(4)],'evaluate','audit','summary','exports','comparison',*[f'finish_batch_{i}' for i in range(4)],'finish','forward','candidate','observer_status','review','gates','feed']
required={phase+'_commands.json':read(R/(phase+'_commands.json')) for phase in phases};required['bootstrap_receipt.json']=[read(R/'bootstrap_receipt.json')]
assert all(x['exit_code']==0 for rows in required.values() for x in rows)
for n in ['definition_check.json','engine_change_verification.json','data_preflight.json','verification.json','comparison_verification.json','export_verification.json','finish_verification.json','visual_inspection.json','forward_verification.json','candidate_verification.json','risk_carry_verification.json','candidate_validation.json','source_verification.json','feed_verification.json']:
 assert read(R/n)['passed'],n
assert source['new_finished_IDs']==33 and source['registry_append_only_events']==66
assert source['actual_finish_exit0_receipts']==source['actual_reserve_receipts']==27 and source['old_unique_results_unchanged']==3
assert report['summary']['passed']==[] and len(report['summary']['rejected'])==27 and len(report['configs'])==27
assert summary['candidate_grid_cells']==27 and summary['reference_configs']==0 and summary['edges']==36 and summary['read_only_controls']==3
assert report['summary']['positive_configs_by_cost']=={'1':27,'2':26,'3':25}
assert sha(R/'report.json')==source['financial_report_sha256']==summary['report_sha256']==audit['report_sha256']==feed['financial_report_sha256']
assert sha(R/'plan.json')==report['frozen_plan_sha256']
assert audit['cost_scenes_audited']==84 and audit['new_cost_scenes_audited']==81 and audit['full_NAV_points_audited']==45781092
assert audit['source_recorded_trades_checked']==12 and audit['source_recorded_funding_checked']==6660
assert audit['new_native_components']==18 and audit['native_cost_scenes_audited']==54 and audit['actual_fills_independently_verified']==1560
assert audit['actual_funding_settlements_verified_including_flat']==59940 and audit['causal_daily_decisions_checked']==19980
assert audit['funding_feature_decisions_checked']==audit['available_funding_feature_records_independently_checked']==0
assert cv['cumulative_finished_candidate_observations']==132 and cv['elapsed_minutes']==5189 and cv['NAV_points_per_scene']==5308
assert cv['prior_NAV_prefix']==5186 and cv['new_NAV_points_per_scene']==122
assert cv['new_funding_settlements']==cv['new_exact_causal_decisions']==cv['new_fills']==0 and cv['new_closed_hour_risk_checks']==6 and cv['new_risk_proxy_violations']==0
assert fv['NAV_points_per_scene']==41219 and fv['cumulative_minutes']==41189 and fv['new_daily_decisions']==fv['new_executions']==0 and risk['funding08_not_recredited']
assert read(R/'visual_inspection.json')['panels_actually_seen']==18 and ctx['initial_16_missing_actual_results']==0 and len(ctx['prior_conclusions_read'])==241
assert len(ctx['additional_full_reads'])==16 and len(ctx['account_hashes_before'])==17715
binding=read(R/'code_binding_before_evaluation.json')
assert dt(binding['recorded_utc'])<dt(report['evaluation_started_utc']) and dt(read(R/'presentation_plan.json')['recorded_utc'])<dt(report['evaluation_started_utc'])
for path,h in binding['source_sha256'].items():assert sha(ROOT/path)==h,path
assert patch['unchanged_accounting_AST'] and patch['synthetic_channel_and_priority_fixtures']==135 and patch['synthetic_future_price_mutations']==135 and patch['new_engine_sha256']==sha(R/'engine.py')
sys.path.insert(0,str(ROOT/'research/automation'));import registry
records=registry.read_records(ROOT/'research/automation/registry.jsonl');events=registry.read_events(ROOT/'research/automation/registry.jsonl');batch=read(R/'batch.json')
refs=list(plan['all_read_only_references'].values());unique={x['fingerprint']:{**x,'status':x['original_status']} for x in refs}
assert len(unique)==3 and not(set(unique)&{x['fingerprint'] for x in batch})
for x in refs:assert records[x['fingerprint']]['status']==x['original_status'] and records[x['fingerprint']]['report_sha256']==x['report_sha256']
for row in batch:
 sp=read(ROOT/row['spec']);es=[e for e in events if e['fingerprint']==row['fingerprint'] and e['status']=='reserved']
 assert len(es)==1 and es[0]['spec']==sp==records[row['fingerprint']]['spec'] and dt(es[0]['recorded_at_utc'])<dt(report['evaluation_started_utc'])
 assert records[row['fingerprint']]['status']=='rejected' and records[row['fingerprint']]['result_available'] is True
for asset,c in rep['centers'].items():
 assert asset in ['BTC','ETH','COMBO'] and c['status']=='rejected' and c['sensitivity']['neighbor_count']==9 and c['sensitivity']['local_recent6of8_allcost_fraction']==0
for g in summary['groups'].values():assert g['candidate_cells']==9 and g['passed']==0 and g['strict_individual_costfold_passes']==0
put(R/'economic_definition_preservation.json',{'passed':True,'new_complete_financial_specs':27,'new_candidates':27,'new_native_components':18,'new_passive_parents':9,'read_only_unique_results':3,'source_native_banks':2,'source_cost_curves':6,'old_qualifications_and_curves_unchanged':True,'three_separate_asset_scope_grids':True,'raw_1_1_not_normalized':True,'independent_bank_capitals_usdt':[10000,10000],'fixed_entry_notionals_usdt':[1000,2000],'source_holds_not_rerun':True,'successful_reservations_and_actual_evaluations_per_new_ID':1,'engine_signal_change_with_accounting_preserved':patch,'full_parameter_cells':27,'report_sha256':sha(R/'report.json')})
for path,h in ctx['account_hashes_before'].items():assert sha(ROOT/path)==h,path
for x in old['real_market_inputs']+old['source_annual_and_recent_inputs']:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
sharedpaths=['research/automation/registry.jsonl','research/automation/candidate_forward_latest.json','research/monitor/latest.json','research/monitor/configs.json.gz']
code={p:h for p,h in old['code_and_frozen_source_sha256'].items() if p not in sharedpaths};code.update(plan['helpers'])
for x in refs:
 for key in ['spec','report','archive']:code[x[key]]=x[key+'_sha256']
for path in ['research/experiments/20261030T073235Z/engine.py','research/experiments/20261026T110637Z/prospective_core.py','research/experiments/20261026T110637Z/prospective_observer.py','research/experiments/20261026T090537Z/candidate_prospective_plan.json','research/experiments/20261001T113625Z/forward_plan.json']:code[path]=sha(ROOT/path)
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
assert all(x['exit_code']==0 for rows in allreceipts.values() for x in rows);put(R/'read_failures.json',facts)
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
nextpriority='All27closechannelcellsfailedfixedmonthly/recentfoldandstrictneighborhoodgates. Do not rerun these exact configs or pick N30/M15 from annual maximum. A genuinely new signal proposal is cross-parameter channel-state consensus using all9 registered causal states per asset, not outcome/NAV weighting. Entry threshold votes [5,6,7], retention threshold [2,3,4], preset center6/3, majority-of9 prevents simultaneous opposing entry. Fresh opposite majority reverses first; otherwise existing long/short retained only while same-direction votes>=retention, else cash; cash needs fresh majority. Native fixed entry notional BTC1000/ETH2000 on independent10000banks, parentraw[1,1]/total20000. Verify source signals cost-independent and causal with prior-close information only before choosing any reuse. New execution must use actual native OPEN/LOT/tick/fees/impact/funding/collateral; source decisions may be reused, never relabel/scale old NAV or fills. Check complete registry for true economic novelty first; preregister full rules/time/gates/parameters/code then reserve every evaluated native/parent variant. Preserve original strict gates and full3xwholeNAV DD, allfolds/recent40, no relaxed tests. This is planning only, zero reservations/evaluations now. Historical development reuse is not untouched final test/independentfuture or stableliveprofit. OriginalSMA65/singleS28 and paper10 frozen accounts remain under original rules.'
proposal={'status':'planning_only_not_tested','financial_evaluations':0,'reservations':0,'direction':'Causal cross-parameter channel-state consensus with entry/retention vote hysteresis','source_entry_lookbacks':[20,25,30],'source_exit_lookbacks':[5,10,15],'source_cells_per_asset':9,'entry_vote_thresholds':[5,6,7],'retention_vote_thresholds':[2,3,4],'prespecified_center':{'entry_votes':6,'retention_votes':3},'bank_capitals_usdt':[10000,10000],'fixed_entry_notionals_usdt':[1000,2000],'raw_parent_weights':[1,1],'total_capital_usdt':20000,'complete_next_round_requirements':nextpriority}
put(R/'next_direction_proposal.json',proposal)
noqual={'passed':True,'meaning':'All actual finished configurations rejected by unchanged preregistered qualification gates.','actual_candidates':27,'strict_individual_costfold_passes':0,'passed_candidates':0,'groups':summary['groups'],'centers':rep['centers'],'all_old_qualifications_unchanged':True,'no_grid_boundary_expansion_or_gate_relaxation_after_results':True,'next_direction_proposed_only':proposal['direction'],'financial_evaluations_in_decision':0,'report_sha256':sha(R/'report.json')}
put(R/'direction_review.json',noqual)
oldnext=read(P/'next_research_state.json')
nextstate={'round':R.name,'plan':rel(R/'plan.json'),'plan_sha256':sha(R/'plan.json'),'report':rel(R/'report.json'),'report_sha256':sha(R/'report.json'),'spec':rel(R/'spec.json'),'actual_new_financial_configs':27,'new_native_components':18,'new_passive_parents':9,'passed_candidates':0,'rejected_candidates':27,'new_cost_scenes':81,'all_results_finished':True,'read_only_source_results':unique,'centers':rep['centers'],'groups':summary['groups'],'engine_change':patch,'next_research_priority':nextpriority,'next_direction_planning_only':proposal,'prior_ROC_S_boundary_direction_retired_for_now':{'source':rel(P/'direction_stop_decision.json'),'sha256':sha(P/'direction_stop_decision.json'),'old_canonical_qualifications_preserved':True},'original_SMA':copy.deepcopy(oldnext['original_SMA']),'original_candidate':copy.deepcopy(oldnext['original_candidate']),'monitor':copy.deepcopy(oldnext['monitor']),'paper10_policy':oldnext['paper10_policy'],'independent_future_qualified':False}
nextstate['original_SMA'].update(state=rel(R/'forward_state.json'),state_sha256=sha(R/'forward_state.json'),report=rel(R/'forward_report.json'),report_sha256=sha(R/'forward_report.json'),cutoff_utc='2026-10-30T14:30:00Z',NAV_points=41219,elapsed_minutes=41189,next_window='14:30to16:30 spot closed marks; original float cash/quantity/desired/trades/costs, no perp funding or account reset. Read saved65daily context separately from current minute-array input.')
nextstate['original_candidate'].update(saved_pointer=rel(R/'candidate_current_pointer.json'),saved_pointer_sha256=sha(R/'candidate_current_pointer.json'),state=rel(R/'candidate_observation/state.json'),state_sha256=sha(R/'candidate_observation/state.json'),report=rel(R/'candidate_observation/report.json'),report_sha256=sha(R/'candidate_observation/report.json'),delta=rel(R/'candidate_observation/delta.json.gz'),delta_sha256=sha(R/'candidate_observation/delta.json.gz'),cutoff_utc='2026-10-30T14:30:00Z',observations=132,NAV_points=5308,elapsed_minutes=5189,books=state['books'],risk=state['risk'],next_window='14:30to16:30 crosses16UTC funding: derive actual ns/mark/rate/quantity cashflows exactly once from verified packet. Do not assume zero events or whole-hour timestamp; keep true positive-duration pre/postfund states. Current14hour stack1793368800000000000 single carried state. 08:00:00.001 already credited; retain BTCq-.012/ETHflat and all cash/entry. Original singleS28/10000eachbank/BTCN1000/ETHN3000 unchanged, not newchannel or consensus rules.')
nextstate['monitor'].update(research_rows=feed['research_configs'],old_rows_unchanged=feed['historical_rows_identical'],paper_observations=feed['paper_observations'],paper_accounts=feed['paper_accounts'],gzip_bytes=(ROOT/'research/monitor/configs.json.gz').stat().st_size)
put(R/'next_research_state.json',nextstate)
text=(R/'result.md').read_text();lines=text.splitlines();text='\n'.join('27 个新候选均淘汰。全期净正配置在1/2/3倍成本分别为27/26/25个；27个均未达到完整月折≥9/12及近期各成本正五日折≥6/8。21个近期40日未能各成本净正，全部局部严格率为0。三组最高全期收益均在N30/M15边缘，不能据此称全局最优。' if line.startswith('27候选通过0') else line for line in lines)+'\n'
text+='\n封存核验：27项全部先成功reserve、实际评估、独立finish；18新单币账本与9原值[1,1]父组合共81新成本场景。3旧同本金/固定名义常持对照只读复用，未重新登记或改变历史资格。三组中心均为事前固定N25/M10，各9格完整邻域严格率为0。\n\n'
for asset,c in rep['centers'].items():text+=f"{asset}中心三倍成本：全期净收益{c['return3_pct']:.6f}%，完整连续NAV最大回撤{c['whole_DD3_pct']:.6f}%，近期40日{c['recent_return3_pct']:.6f}%，正五日折1/2/3倍为"+'/'.join(str(c['positive_recent_folds_by_cost'][str(k)]) for k in [1,2,3])+'（要求各≥6/8），rejected。\n\n'
text+='全部27项在三档全期收益/回撤上均优于同本金常持；仍未达到原严格资格门槛。年度收益正、收益优于常持和当前历史范围的表现，不构成近期/折间稳健或稳定实盘盈利证据。未基于结果扩大通道边界、放宽门槛或临时挑选参数。\n\n'
text+='实际独审exit0：84场景共45,781,092完整NAV点（含81新与3旧父组合），核对1,176整体/逐折与756近期/分折指标。54新单币成本场景独立核对1,560逐笔成交、59,940资金费结算、19,980因果日决策和319,974状态/闭合小时保证金代理；另只读恢复两旧银行6曲线，核对12成交及6,660资金费。资金费不作为新信号，特征决策为0。6CSV逐值核验及3图18面板实际查看已完成。\n\n'
text+='原冻结SMA65与singleS28仅从12:30续至14:30 UTC：累计41219点/41189分钟及132观察ID/5308点/5189分钟。本窗0新日决策、成交、资金费，现金/数量/entry连续，6闭合小时风险检查0违规；08:00:00.001资金费不重复入账。下窗14:30至16:30将跨16UTC真实资金费，须保留实际纳秒与pre/post状态，不预设零事件或整点。原冻结策略、观察计划和十策略账户未切换为新通道规则，不称十策略实时报价模拟。\n\n'
text+=f"原冻结观察共6新ID，加27金融结果共33新完成ID、66追加登记事件。旧3对照及{len(ctx['account_hashes_before'])}受保护文件保持。必要登记/只读monitor检查实际exit0，网页汇总8672研究配置与10账户189观察，gzip{(ROOT/'research/monitor/configs.json.gz').stat().st_size}字节；不部署网页、不新增模拟成交。实际网络失败事实{len(facts['facts'])}项（见read_failures.json），不虚构失败响应。\n\n"
text+='下轮仅提出基于九格因果信号的跨参数共识及入场/保留票数迟滞，事前候选票数5/6/7×2/3/4、中心6/3，详见next_direction_proposal.json；本轮没有该新方向的reserve或结果。须完整查重、冻结完整规则和独立执行成本后才能计算，不能直接缩放旧NAV当新策略。既往ROC/S边界方向停止准则继续有效。\n\n'
text+='全部正负收益、淘汰配置、账户账本、原规则和核验必需证据保留；清理仅本轮可重建准备脚本，原data/normalized保持。本证据封存后在同一main锁内提交推送；真实commit/push、完整远端tree/blob、发布进程exit0及释放锁证明保存在.git/automation_proofs/20261030T153707Z.json，未以预写SHA替代实际发布状态。\n'
(R/'result.md').write_text(text)
(R/'reproduce.md').write_text('''# 复现与只读核验

固定工作目录 /home/desktop/Documents/Codex/EquiTide；main only，持有research/automation/branch.lock。解释器 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python；环境PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1，版本见runtime.json。

执行顺序和实际退出、时间、stdout日志及stderr见all_command_receipts.json：bootstrap→initial→reserve_batch_0..3（8/8/8/3）→evaluate一次→audit→summary→exports→comparison→finish_batch_0..3→finish→forward→candidate→observer_status→review→gates→feed。已完成配置不可再次reserve/重算；应只读核验已有结果。所有27候选与81成本场景真实执行且独立finish，无新benchmark。旧同本金常持3项只读。

事前完整规则/参数/时间/成本/失败门槛见plan.json/spec.json及27specs。通道N20/25/30×M5/10/15按BTC、ETH、COMBO三组各9格；中心25/10事前固定。入/退出通道均排除被测已完成收盘，次日00:01真实OPEN，原数量退出/反手先平后开。两银行各10000，固定名义1000/2000，父原值[1,1]总20000不归一化。信号改动独立135边界/优先级与135未来价格扰动验证，原费用/资金费/风险/数据/统计AST保持，code_binding_before_evaluation绑定计算前代码。

只读复核已有结果（不执行run.py evaluate/reserve/finish、不再次获取观察窗口）：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T153707Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T153707Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T153707Z/forward.py --reproduce
```

独审整数价格信号/Fraction持仓/Decimal成交费用与资金费/保证金状态/完整NAV；无调用新simulate/target/trade。84场景45,781,092点。6CSV逐数值及3图18面板实际查看。数据清单含8真实Parquet、16来源输入、原公共响应路径和SHA；缺输入即停止，不合成行情。完整账本和实际正负结果保留，大行情留本地ignoreddata。

原冻结SMA65和singleS28只续12:30至14:30 UTC，6原观察ID加27金融ID共33新ID/66追加事件；规则/本金/持仓不改。当前14小时单一风险状态与08:00:00.001已入账资金费保留，下一窗14:30至16:30跨真实16UTC结算须按实际ns/mark/rate/旧数量入账一次，不能假设零结算或整小时。次日日决策2026-10-31UTC00:01，36日上下文及4日NAV边界连续；SMA65旧日上下文见next_research_state。旧延迟观察不称十策略实时报价模拟。

27项均被原月折/近期五日折/邻域严格门槛淘汰；1/2/3成本全期净正27/26/25项不替代资格。事前中心全期净正而近期负，不能选边缘年度最优点称稳健。三旧控制/17715受保护文件不变，旧canonical资格保持历史范围。历史重复开发不是未触碰最终测试或独立未来盈利。

next_direction_proposal仅提出九格因果信号共识与迟滞门槛，零reserve/零实际结果。下轮完整查重/冻结定义/独立登记后才能计算。原ROC/S边界停止决定保留，不继续追逐边界或放宽门槛。

检查与只读snapshot在同一main排他锁中实际执行；paper10只读，页面自动读取main，不需重部署或新定时任务。publish.py提交并推送main，fetch/独立lsremote/全递归tree与每个所需blob及数据哈希核验，发布进程真实exit0后释放本人锁。实际SHA和进程/解锁/发布后核验见.git/automation_proofs/20261030T153707Z.json；其他任务以后正常推进按保存pointer与本轮commit核对，不回滚共享账户。
''')
pp=R/'implementation_plan.md';pp.write_text(pp.read_text().replace('- [ ]','- [x]')+'\n研究、必要核验与封存完成；实际main推送、发布进程exit0和锁释放见.git证明。\n')
rawpaths={x['raw'] for x in attempts}|{im['packet']};rawartifacts=[{'path':p,'sha256':sha(ROOT/p),'bytes':(ROOT/p).stat().st_size} for p in sorted(rawpaths)]
fr=read(R/'forward_report.json');shared={p:{'sha256':sha(ROOT/p),'bytes':(ROOT/p).stat().st_size} for p in sharedpaths}
artifacts={rel(p):sha(p) for p in sorted(R.rglob('*')) if p.is_file() and p.name!='data_manifest.json'}
assert not any(p.name=='__pycache__' or 'checkpoint' in p.name or p.suffix in ['.pyc','.npy','.tmp'] for p in R.rglob('*'))
m={'round':R.name,'recorded_at_utc':now(),'working_directory':str(ROOT),'branch':'main','base_commit':start['head_after_successful_SSH_fetch'],'branch_lock_broker_pid':start['branch_lock_broker_pid'],'initial_main_branch_verification':read(R/'main_only_branch_check.json'),'frozen_plan_sha256':sha(R/'plan.json'),'finished_report_sha256':sha(R/'report.json'),'finished_forward_report_sha256':sha(R/'forward_report.json'),'finished_candidate_report_sha256':sha(R/'candidate_observation/report.json'),'real_market_inputs':old['real_market_inputs'],'source_annual_and_recent_inputs':old['source_annual_and_recent_inputs'],'forward_raw_responses':fr['provenance'],'observer_preflight_raw_responses':[],'candidate_raw_artifacts':rawartifacts,'candidate_input_manifest':im,'prospective_readiness':{'actual_candidate_observations':132,'new_actual_observation_IDs':3,'original_frozen_rules_unchanged':True,'current_cutoff_utc':'2026-10-30T14:30:00Z'},'registry':{'main_sha256_before_reserve':ctx['main_registry_sha256_before_reserve'],'before_events':ctx['registry_events'],'before_IDs':ctx['registry_ids'],'append_only_events':66,'new_finished_IDs':33,'financial_IDs':27,'invalid_financial_attempts':0},'read_only_source_results':unique,'code_and_frozen_source_sha256':code,'protected_inputs_sha256':ctx['account_hashes_before'],'shared_files':shared,'required_command_receipts':required,'all_command_receipts':allreceipts,'failure_facts':facts,'new_actual_results':{'financial_configs':27,'candidate_configs':27,'reference_only':0,'cost_scenes':81,'new_native_models':18,'new_parent_configs':9,'source_bank_curves_reused':6,'passed':0,'rejected_candidates':27,'individual_eachcost_recent6of8_full_grid':0,'old_readonly_unique_results':3,'full_sensitivity_cells':27,'separate_asset_scope_grids':3,'edges':36,'invalid_attempts_and_curves_retained':0,'positive_configs_by_cost':report['summary']['positive_configs_by_cost'],'prespecified_centers':rep['centers'],'all_old_registry_qualifications_unchanged':True,'signal_engine_change_with_old_accounting_verified':True,'new_direction_only_proposed_not_evaluated':True,'independent_future_validated':False},'artifacts':artifacts}
put(R/'data_manifest.json',m)
print(json.dumps({'manifest':rel(R/'data_manifest.json'),'artifacts':len(artifacts),'round_bytes':sum(p.stat().st_size for p in R.rglob('*') if p.is_file()),'protected_files':len(ctx['account_hashes_before']),'old_unique_results':len(unique),'all_required_actual_terminal_checks_exit0':True,'transport_failure_facts_preserved':len(facts['facts']),'financial_or_observation_reruns':0,'passed_candidates':0,'removed_own_reconstructible_files':len(cleanup)}),flush=True)
