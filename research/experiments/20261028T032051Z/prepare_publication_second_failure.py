"""Prepare fixed-window continuity and publication metadata before financial results are inspected."""
from pathlib import Path
R=Path(__file__).resolve().parent
def edit(n,pairs):
 p=R/n;s=p.read_text()
 for a,b in pairs:
  if a not in s and b in s:continue
  assert a in s,(n,a);s=s.replace(a,b)
 p.write_text(s)
edit('summarize.py',[("ETH入场阈值1/2/3%","ETH入场阈值1.5/2/2.5%"),("H1/H3新12原生","H1.5/H2.5新12原生"),("原H4/ETH慢28反转3日冻结候选和旧SMA按完整原账本从UTC20:30续接至22:30，不重复08和16资金费，不改长期规则/本金/持仓，不强制截止平仓。依据真实已闭合行情延迟重建，不是十策略实时报价账户或成熟长期资格；paper10只读，partial观察rejected不取消原计划。下个00:01日事件必须由原冻结日决策规则续接并独立核验，不能沿用仅mark驱动跨越。","原H4/ETH慢28反转3日冻结候选和旧SMA从Oct28UTC00:30续接至02:30，保留刚完成00:01日决策、00:00.001资金费及完整风险状态，不重开本金/持仓，不重复日决策或资金费，不强制截止平仓。独立检查01:00闭合小时中资金费前后两个现金状态。依据真实闭合行情延迟重建，不是十策略实时报价账户或成熟长期资格；paper10只读，partial的rejected不取消长期计划。下一日决策Oct29UTC00:01。")] )
edit('finalize.py',[("20261027T211845Z","20261028T012050Z"),("['cumulative_finished_candidate_observations']==36","['cumulative_finished_candidate_observations']==42"),("==1257+cv","==1506+cv"),("['prior_NAV_prefix']==1257","['prior_NAV_prefix']==1506"),("['elapsed_minutes']==1349","['elapsed_minutes']==1589"),("'actual_finished_observation_configs':36","'actual_finished_observation_configs':42"),("'cutoff_utc':'2026-10-27T22:30:00Z'","'cutoff_utc':'2026-10-28T02:30:00Z'"),("'actual_observations':36","'actual_observations':42"),("'actual_candidate_observations':36","'actual_candidate_observations':42")])
s=(R/'finalize.py').read_text();a=s.index("'next_window_policy':'");b=s.index("'};put(R/'candidate_active_state.json'",a);s=s[:a]+"'next_window_policy':'ContinueafterOct28UTC02:30carryingexactcash/q/entry/cost/funding/context34/daily2/risk/NAVchain. Oct28daily00:01and00:00.001fundingalreadyprocessed;do notrepeat. Nextfund08:00,nextdailyOct29UTC00:01. OriginalH4/ETH28L3futureplanandpaper10unchanged."+s[b:]
a=s.index("'next_research_priority':'");b=s.index("','monitor_compressed_bytes'",a);s=s[:a]+"'next_research_priority':'CompletedETHH1.5/H2.5 xS28/31 xL3/4/5atN3000:12native+12parents,fixedBTCN1000H4;oldH2cellsreadonly. Consultactualqualification andavoidexactreruns. Newnativeledgers/NAVsreusablefornewconcretepairs;do notlinearscalequantityorchangeoriginalfutureplan. ActivepointerOct28UTC02:30,context34/daily2;carryfundingcashandfullriskstate. Next05:20cyclecut04:30ismarkonly,nextfund08:00,nextdailyOct29. Mostrecent65dailySMAcontextfrom012050,notcurrentmark-onlyminuteinputs."+s[b:]
a=s.index("'next_window_funding_audit_requirement':'");b=s.index("','paper10_policy'",a);s=s[:a]+"'next_window_funding_audit_requirement':'AfterOct28UTC02:30carrycash/fundingcountersandcurrenthourrisksegments. Oct28UTC00:00.001settlementsand00:01dailydecisionalreadydone. Readactualeventsnotzeroassumptions;nextfund08:00. Check-Q*mark*rate,outflow*k/incomeunamplified,prepostNAVandstatehourrisk. Originalcoreunchanged."+s[b:]
s=s.replace("'分钟，0新增日决策/成交，实际新增资金费记录'","'分钟，0新增日决策/成交，实际新增资金费记录'")
(R/'finalize.py').write_text(s)
edit('publish.py',[("research: test ETH reversal entry thresholds with native cost-aware paths","research: validate ETH threshold perturbations at 1.5 and 2.5 percent"),("['actual_candidate_observations']==36","['actual_candidate_observations']==42")])
print('PUBLICATION_AND_CONTINUITY_TOOLS_PREPARED')
