"""Export saved actual BTC sizing, reused ETH and L/N parent results only."""
import collections,csv,gzip,json,statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import *
r=json.loads((R/'report.json').read_text());p=json.loads((R/'plan.json').read_text());rows={};full={**r['all_current_grid'],**r['all_current_native_grid'],**{x['fingerprint']:x for x in r['configs'].values()}}
def write(name,cols,items):
 with (R/name).open('w',newline='') as f:w=csv.writer(f,lineterminator='\n');w.writerow(cols);w.writerows(items)
 rows[name]=len(items)
cost=[];wf=[];rec=[];daily=[]
for c in r['configs'].values():
 for k,s in c['scenes'].items():
  cost.append([c['name'],c['fingerprint'],c['scope'],c['role'],c['asset'],c['L'],c['N'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['role'],c['L'],c['N'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  rec.extend([c['name'],c['role'],c['L'],c['N'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['role'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
write('cost_scenes.csv',['configuration','fingerprint','scope','role','asset','fast_L','BTC_fixed_N_USDT','capital','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','executions','closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','role','L','BTC_N','cost_multiplier','fold','start','end_exclusive','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','role','L','BTC_N','cost_multiplier','fold','start','end_exclusive','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],rec)
write('daily_NAV.csv',['configuration','role','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['fast_L','BTC_fixed_N_USDT','fingerprint','readonly','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_strict_recent_fraction'];edges=[];flags={};readonly=[]
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 fs=r[key];items=[];ls=p['lookbacks'] if scope=='parent' else [31]
 for g in grid:
  c=fs[g['fingerprint']]
  for k,s in c['scenes'].items():
   d=c['current_grid_diagnostic_sensitivity'];z=[g['L'],g['N'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),d['local_positive3_fraction'],d['local_strict_recent_fraction']];items.append(z)
   if scope=='parent' and g['readonly']:readonly.append(z)
 for k in ['1','2','3']:
  for g in grid:
   i,j=ls.index(g['L']),p['entry_notionals'].index(g['N']);neighbors=[h for h in grid if i+1<len(ls) and h['L']==ls[i+1] and h['N']==g['N'] or j<2 and h['N']==p['entry_notionals'][j+1] and h['L']==g['L']]
   for h in neighbors:
    a,b=fs[g['fingerprint']]['scenes'][k],fs[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['L'],g['N'],h['L'],h['N'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
 flags[scope]={}
 for k in ['1','2','3']:
  vals=[z[8] for z in edges if z[0]==scope and z[1]==k];threshold=2*statistics.stdev(vals);flags[scope][k]={'edge_count':len(vals),'max_Sharpe_change':max(vals),'two_std_change_threshold':threshold,'descriptive_cliff_flag':max(vals)>threshold,'scope':'Dependent-edge descriptive heuristic; native only two edges,not significance,DSR or PBO.'}
 write('sensitivity_grid.csv' if scope=='parent' else 'native_sensitivity_grid.csv',cols,items)
write('readonly_reused_scenes.csv',cols,readonly);write('adjacent_edges.csv',['scope','cost','from_L','from_N','to_L','to_N','from_fp','to_fp','absolute_Sharpe_change','return_change_pp','DD_change_pp'],edges)
cs=r['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs]);sources=[]
for fp,ref in p['read_only_references'].items():
 if ref['scope']!='native':continue
 sp=json.loads((ROOT/ref['spec']).read_text());cfg=next(x for x in json.loads((ROOT/ref['report']).read_text())['configs'].values() if x['fingerprint']==fp)
 for k,s in cfg['scenes'].items():sources.append([fp,ref['asset'],ref['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],ref['report'],ref['report_sha256']])
write('source_curves.csv',['fingerprint','asset','actual_bank','actual_fixed_N','cost','return_pct','whole_DD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','source_report','report_sha256'],sources)
alloc=[[g['fingerprint'],g['role'],g['L'],g['N'],3750,15000,18750,g['N'],4500,1,1,.2,.8,g['readonly']] for g in p['grid']+p['benchmarks']];write('fixed_allocations.csv',['fingerprint','role','ETH_L','BTC_N','BTC_bank','ETH_bank','total_capital','BTC_entry_N','ETH_entry_N','raw_BTC_weight','raw_ETH_weight','capital_share_BTC','capital_share_ETH','readonly'],alloc);put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(16,9),layout='constrained')
for row,(scope,key,ls) in enumerate([('BTC native bank3750','all_current_native_grid',[31]),('BTC3750 + ETH15000 parent','all_current_grid',[3,4,5])]):
 fs=r[key]
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((len(ls),3))
  for c in fs.values():arr[ls.index(c['L']),p['entry_notionals'].index(c['N'])]=fn(c)
  ax=axs[row,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',aspect='auto',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['N250','N375 old','N500']);ax.set_yticks(range(len(ls)),[f'L{L}' for L in ls]);ax.set_xlabel('Actual BTC fixed entry N (USDT)');ax.set_ylabel('BTC fixed L31' if row==0 else 'ETH fast L');ax.set_title(scope+'\n'+label,fontsize=10)
  for c in fs.values():i,k=ls.index(c['L']),p['entry_notionals'].index(c['N']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if c['readonly'] else ' N'),ha='center',va='center',fontsize=10)
  fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('Actual BTC sizing N250/375/500 x ETH fast L3/4/5 | ETH fixed S28,E0.5%,HL1.5%/HS2.5%,V10/cap4.5%\nBanks3750/15000, raw[1,1], capitalshares20/80%, no oldNAV scaling | O=readonly,N=new | reused development history')
fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
# Exact original comparisons use saved NAV hashes and metrics; no original engine call.
records=reg.read_records(ROOT/'research/automation/registry.jsonl');cache={}
def original(fp):
 if fp not in cache:
  z=records[fp];assert z['result_available'] and sha(ROOT/z['report'])==z['report_sha256'];cache[fp]=next(c for c in json.loads((ROOT/z['report']).read_text())['configs'].values() if c['fingerprint']==fp)
 return cache[fp]
btc0=next(g['fingerprint'] for g in p['native_grid'] if g['N']==375);hold0=p['benchmark_parent_fingerprint'];holdsp=records[hold0]['spec'];bh=next(x['fingerprint'] for x in holdsp['components'] if records[x['fingerprint']]['spec']['universe']==['BTC/USDT']);comp=[]
for c in r['configs'].values():
 ctrl=bh if c['scope']=='native' and c['role'].startswith('benchmark') else btc0 if c['scope']=='native' else hold0 if c['role'].startswith('benchmark') else next(g['fingerprint'] for g in p['grid'] if g['L']==c['L'] and g['N']==375);old=original(ctrl);co={k:{'new_return_pct':s['net_return_pct'],'control_return_pct':old['scenes'][k]['net_return_pct'],'delta_return_to_control_pp':s['net_return_pct']-old['scenes'][k]['net_return_pct'],'new_DD_pct':s['max_drawdown_pct'],'control_DD_pct':old['scenes'][k]['max_drawdown_pct'],'delta_DD_to_control_pp':s['max_drawdown_pct']-old['scenes'][k]['max_drawdown_pct'],'NAV_identical':s['NAV_sha256_f64le']==old['scenes'][k]['NAV_sha256_f64le']} for k,s in c['scenes'].items()};comp.append({'fingerprint':c['fingerprint'],'name':c['name'],'scope':c['scope'],'role':c['role'],'L':c['L'],'N':c['N'],'control_fingerprint':ctrl,'control_report':records[ctrl]['report'],'control_report_sha256':records[ctrl]['report_sha256'],'all_cost_NAV_identical':all(z['NAV_identical'] for z in co.values()),'cost_comparisons':co})
put(R/'equivalent_realized_NAV_paths.json',{'report_sha256':sha(R/'report.json'),'comparisons':comp,'new_definitions_matching_control_path':sum(x['all_cost_NAV_identical'] for x in comp),'comparison_scope':'Same actual banks; N375 matched original native/parent/hold source,allcost whole-NAV hashes. Different raw sizing is not independent alpha.'})
prior=json.loads((ROOT/p['prior_report']['path']).read_text());priorcmp=[]
for c in r['configs'].values():
 if c['role']!='candidate':continue
 for old in prior['all_current_grid'].values():
  if old['L']!=c['L']:continue
  priorcmp.append({'fingerprint':c['fingerprint'],'old_fingerprint':old['fingerprint'],'old_S':records[old['fingerprint']]['spec']['parameters']['ETH_trend_lookback_days'],'allcost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==old['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3'])})
put(R/'prior_grid_NAV_aliases.json',{'new_parent_comparisons':priorcmp,'new_definitions_matching_a_prior_path':len({x['fingerprint'] for x in priorcmp if x['allcost_NAV_identical']}),'scope':'Saved actual previous S27/28/29 same-L parents only; no new valuation.'})
ctx=json.loads((R/'context.json').read_text());own={x['fingerprint'] for x in json.loads((R/'batch.json').read_text())};isobs=lambda sp:sp.get('family')=='paper-live-portfolio-observation' or sp.get('name','').startswith('forward_snapshot_') or 'observation_terminal_action' in sp.get('parameters',{});priorids={fp:z for fp,z in records.items() if fp not in own and 'spec' in z and not isobs(z['spec'])};trials={'canonical_prior_research_definitions':len({reg.fingerprint(z['spec']) for z in priorids.values()}),'registry_marked_actual':sum(bool(z.get('result_available')) for z in priorids.values()),'not_marked_actual':sum(not z.get('result_available') for z in priorids.values()),'initial16_actual_evidence':16,'new_financial_definitions':12,'observations_excluded':True};put(R/'prior_actual_research_counts.json',trials)
s={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(r['summary']['passed']),'rejected':len(r['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(f for c in r['configs'].values() for f in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',s)
lines=['BTC实际入场额与ETH回看双轴研究','',p['hypothesis'],'',f"完整读取{ctx['registry_events']}事件/{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份既往结论；初始16均有原档真实证据。此前完整研究定义{trials['canonical_prior_research_definitions']}，登记有结果{trials['registry_marked_actual']}、未标结果{trials['not_marked_actual']}，不能把全部登记当完成回测。大量历史搜索存在多重选择偏差。",'', '预设BTC入场N=[250,375,500]USDT × ETH快L=[3,4,5]，固定真实银行3750/15000与ETH入场4500。N是每次开仓名义敞口，不是本金重配；BTC初始资本占比20%、ETH80%，raw[1,1]只把两个完整银行净值相加，不重复乘资本比例、不归一化。不线性缩放旧BTC净值，两个新N逐项实际LOT/手续费/冲击/资金费计算。4新BTC原生（2动量、2恒定持有）和8新父（6候选、2匹配持有）共12/36场景，10旧结果只读。', '', 'Walk-forward：真实2025-10-19UTC00:01至2026-10-24UTC00:01连续370日，12×30日完整折+10日尾折。现金/数量/成本跨折连续，完整分钟/事件OOS NAV算整体DD。近期40日继承day330状态、8×5日折，固定信号不拟合、无标签，purge0，30日预热+3日间隔，仅当时已完成收盘和past20成本输入，次日00:01原生OPEN。反复开发历史不称未触碰最终测试、独立未来或DSR/PBO显著。', '', '成本：5bp手续费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际订单q×OPEN/past20完整日quoteADV)，LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押、独立1%闭合小时不利mark维持保证金代理。真实settlement ns/rate/mark/heldq资金费，1/2/3倍压力放大支出、收入不放大。永续空头不借现货，不虚构借币费；缺盘口/TCA/历史全层级/逐tick强平和真实容量证据。三个BTC N均用同本金、同入场N的恒定持有对照，现金0%另列。', '', '判据不放宽：各成本全年净收益>0；1倍至少9/12正完整月；各成本近期40日>0且至少6/8正5日折；3倍整体DD<=25%；索引半径1含中心的局部3倍正收益与严格近期支持均>=60%；至少4原生成交平仓、毛参考PnL+资金费/执行成本>=2.5；0订单/现金/保证金代理违规、终点flat。组合双轴L/N，BTC源模型仅N单轴，不能冒充两种信号参数同时扰动。4实际持有基准只作参照，rejected表示不是策略候选，不是没有实际结果。', '', '|配置|角色|L|BTC N|1x收益%|2x收益%|3x收益%|3x整体DD%|1x正月|近期正折1/2/3|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in r['configs'].values():lines.append('|'+ '|'.join([c['name'],c['role'],str(c['L']),str(c['N']),*[f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3']],f"{c['scenes']['3']['max_drawdown_pct']:.6f}",str(c['positive_complete_30d_folds_1x']),'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3']),c['status']])+'|')
lines.extend(['',f"新组合历史通过{len(r['summary']['passed'])}、淘汰{len(r['summary']['candidate_rejected'])}；逐项失败判据{ {c['name']:c['failed_criteria'] for c in r['configs'].values()} }。旧N375原canonical status/criteria/sensitivity/报告字节均保留，本轮L/N诊断单列；原S扰动失败不能被新的N邻域掩盖。",'',f"相对匹配旧N375，完整NAV全同{sum(x['all_cost_NAV_identical'] for x in comp)}/12；对上一轮同L的S27/28/29父净值同路径数量见prior_grid_NAV_aliases。收益/DD/Sharpe/Calmar、全部逐折及成本、36场景、持有与现金、42相邻边见11CSV和8图。描述性悬崖不当显著性、边界峰不引发本轮事后扩参。",'', '三个冻结账户只延续：SMA65和single从Nov3_00:30到02:30，L4/H2从02:10到04:10，仅04:11参考闭合后采集。Nov3午夜日决策和资金费以前已记不重复；现金/q/desired/累计成本/risk/完整NAV前缀不改，不采纳本批新N、不重置本金、不强制平仓。SMA真实65日上下文仍引用20261103T020232Z/forward_inputs.json.gz。部分延迟shadow与十策略真实报价模拟分开，短样本不作180天/六折资格。','',f"一手资料2026-11-03实际访问：[Binance市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。原始年行情/mark/资金费/约束8文件的单位/边界/SHA见plan和data_manifest；官方字段不证明盈利或实时执行。",'','全部实际定义先成功reserve再计算，所有正负结果及必要代码、数据哈希、实际命令留档并finish；同main排他锁内检查、只读snapshot、提交推送。真实push终态与解锁证据见.git/automation_proofs/'+R.name+'.json。'])
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(s),flush=True)
