"""Export only completed financial evidence; never calculate new strategy paths."""
import collections,csv,json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import *
from run import grid_axes,recent_ok
report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());configs=report['configs'];full={**report['read_only_grid'],**{c['fingerprint']:c for c in configs.values()}}
def write(name,columns,rows):
 with (R/name).open('w',newline='') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(columns);w.writerows(rows)
cost=[];fold=[];recent=[];daily=[];sensitivity=[];comparisons=[]
for c in configs.values():
 S,H=grid_axes(c)
 for k,z in c['scenes'].items():
  cost.append([c['name'],c['scope'],S,H,k,c['capital_usdt'],1000 if c['scope']=='parent' else 0,3000,z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar'],z['cost_usdt'],z['funding_usdt'],z['gross_reference_PnL_to_execution_cost'],z['executions'],z['round_trips'],z['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in z['recent40']['folds']),c['status']])
  fold.extend([c['name'],k,f['fold'],f['start_utc'],f['end_exclusive_utc'],f['duration_days'],f['net_return_pct'],f['max_drawdown_pct'],f['sharpe_365']] for f in z['folds'])
  recent.extend([c['name'],k,f['fold'],f['start_utc'],f['end_exclusive_utc'],f['net_return_pct'],f['max_drawdown_pct'],f['sharpe_365']] for f in z['recent40']['folds'])
  daily.extend([[c['name'],k,i,v] for i,v in enumerate(z['daily_equity_usdt'])])
  ref=next(x for x in report['read_only_grid'].values() if grid_axes(x)==(28,.02) and x['scope']==c['scope']);rz=ref['scenes'][k]
  comparisons.append([c['name'],c['scope'],k,ref['fingerprint'],ref['status'],c['capital_usdt'],4000 if c['scope']=='parent' else 3000,z['net_return_pct'],rz['net_return_pct'],z['net_return_pct']-rz['net_return_pct'],z['max_drawdown_pct'],rz['max_drawdown_pct'],z['max_drawdown_pct']-rz['max_drawdown_pct'],'same initial capital and entry budget; different signals/turnover/exposure, not equal-risk comparison'])
for g in plan['grid']:
 c=full[g['fingerprint']];sensitivity.append([g['scope'],g['S'],g['H'],g['fingerprint'],g['readonly'],c['status'],c['scenes']['3']['net_return_pct'],c['scenes']['3']['max_drawdown_pct'],c['scenes']['3']['recent40']['net_return_pct'],*[sum(f['net_return_pct']>0 for f in c['scenes'][k]['recent40']['folds']) for k in ['1','2','3']],recent_ok(c)])
write('cost_scenes.csv',['configuration','scope','S','H','cost_multiplier','initial_capital_usdt','BTC_entry_budget_usdt','ETH_entry_budget_usdt','net_return_pct','whole_OOS_drawdown_pct','sharpe365','calmar','cost_usdt','funding_usdt','gross_plus_funding_to_cost','executions','independent_bank_closing_roundtrips','recent40_net_return_pct','recent_positive5d_folds','new_status'],cost)
write('walk_forward_folds.csv',['configuration','cost_multiplier','fold','start_utc','end_exclusive_utc','days','net_return_pct','whole_fold_drawdown_pct','sharpe365'],fold)
write('recent40_folds.csv',['configuration','cost_multiplier','fold','start_utc','end_exclusive_utc','net_return_pct','whole_fold_drawdown_pct','sharpe365'],recent)
write('daily_NAV.csv',['configuration','cost_multiplier','boundary_index','NAV_usdt'],daily)
write('sensitivity_grid.csv',['scope','S','H','fingerprint','readonly_old_result','canonical_status','net3_pct','DD3_pct','recent40_net3_pct','positive5d_1','positive5d_2','positive5d_3','current_strict_recent_diagnostic'],sensitivity)
write('reference_comparisons.csv',['configuration','scope','cost_multiplier','original_S28_H02_fingerprint','original_qualification_unchanged','same_initial_capital_usdt','same_nominal_entry_budget_usdt','new_return_pct','old_return_pct','return_difference_pp','new_DD_pct','old_DD_pct','DD_difference_pp','comparability_scope'],comparisons)
fig,axs=plt.subplots(2,3,figsize=(13,7),layout='constrained')
for row,scope in enumerate(['native','parent']):
 cells=[g for g in plan['grid'] if g['scope']==scope]
 for col,(title,fn) in enumerate([('3x full370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x complete-curve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('Recent positive5d folds at3x /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for g in cells:arr[[21,28,35].index(g['S']),[.01,.02,.03].index(g['H'])]=fn(full[g['fingerprint']])
  ax=axs[row,col];im=ax.imshow(arr,cmap='RdYlGn_r' if col==1 else 'RdYlGn',aspect='auto');ax.set_xticks(range(3),['1%','2%','3%']);ax.set_yticks(range(3),[21,28,35]);ax.set_xlabel('Fast3d return hurdle');ax.set_ylabel('Slow trend days');ax.set_title(('ETH bank10000' if row==0 else 'BTC+ETH parent20000')+'\n'+title)
  for g in cells:
   i,j=[21,28,35].index(g['S']),[.01,.02,.03].index(g['H']);ax.text(j,i,f'{arr[i,j]:.2f}'+(' O' if g['readonly'] else ' N'),ha='center',va='center',color='black',fontsize=10)
  fig.colorbar(im,ax=ax,shrink=.8)
fig.suptitle('Fixed S21/28/35 x H1/2/3% | O=old result, N=new | repeated development history\nOld canonical qualification unchanged; no cell meets current all-cost recent gate',fontsize=12);fig.savefig(R/'sensitivity.png',dpi=145);plt.close(fig)
fail=collections.Counter(k for c in configs.values() for k in c['failed_criteria']);summary={'report_sha256':sha(R/'report.json'),'new_configs':10,'new_native':5,'new_parents':5,'new_cost_scenes':30,'old_grid_cells':8,'old_canonical_status_unchanged':True,'positive_by_cost':report['summary']['positive_configs_by_cost'],'failed_criteria_counts':dict(fail),'strict_recent_qualified_cells_by_scope':{scope:sum(recent_ok(full[g['fingerprint']]) for g in plan['grid'] if g['scope']==scope) for scope in ['native','parent']},'positive_sharpe_fraction':{k:sum(c['scenes'][k]['sharpe_365']>0 for c in configs.values())/10 for k in ['1','2','3']},'neighbor_platform_scope':'Scope separated; index-radius1 includes center/old actual cells, 4/6/9 bounded neighbors; no unseen extrapolation; recent strict qualification diagnostic cannot overwrite any old status.'};put(R/'sensitivity_summary.json',summary)
representative=next(c for c in configs.values() if c['scope']=='parent' and grid_axes(c)==(35,.02));put(R/'representative.json',{'selection_policy':'Preset continuation S35/H2 on original H2 axis; descriptive, not selected by maximum OOS return','configuration':representative})
lines=['# ETH慢趋势过滤反转联合邻域验证','',f"10个新完整定义（5个ETH原生、5个BTC/ETH父组合）、30个成本场景真实执行；全部rejected。1/2/3倍成本净正配置数为10/9/8。旧4个ETH和4个父组合只读，BTC旧原生只复用账本。负收益、逐折亏损及所有失败保留。",'',
'预先固定ETH快ROC为3日、零线退出，慢ROC为21/28/35日×入场门槛1/2/3%；严格快ROC>H做空、<-H做多，带内只保留实际同方向仓位且快ROC符号相容，再要求多仓慢ROC>0／空仓慢ROC<0，否则现金。没有隐藏反转仓位；门槛等值不新开、零ROC退出，gate重开且现金时须重新满足严格快极值。先全部10次reserve成功，才执行真实信号／收益计算。不同参数是新定义，但4个具体旧格点没有改名重跑。','',
'BTC固定原L31/H4%/退出缓冲1%/入场1000，独立银行10000；ETH入场3000、银行10000。父组合总本金20000、原始份额[1,1]直接相加且不归一化；入场预算合计4000为初始总本金20%，不是持续资金配置或等风险敞口。各银行不转账、不交叉抵押、不随NAV或同向信号免费调整数量；父组合无新增订单。父往返次数为两个独立银行的已平仓次数之和，不是同步配对交易。','',
'S35首个信号需要2025-09-13收盘，补抓Sep13至Sep16四根真实ETH永续日线，与既有Sep16分钟聚合收盘完全相同、quote成交额差<0.001。Sep13–15以明确−3/−2/−1字典键保存，禁止负Python列表下标绕到未来。八个原始Parquet与370日OOS轴/日期不动，绝不移除早期亏损。原始响应、HTTP回执及SHA保留。','',
'三项验证：2025-10-19 UTC00:01至2026-10-24 UTC00:01连续370日，12完整30日折＋10日尾折、不中途重置银行；近期40日继承day330真实状态、8个连续5日折。无训练监督标签，purge horizon0，信号仅前一完整收盘且60秒后00:01真实OPEN执行。参数双轴索引半径1含中心、同scope邻域；所有成本全年净正、1倍9/12正月折、近期每档6/8正五日折与两个60%局部平台门槛冻结。反复使用的历史属于开发数据，非未触碰测试集或独立未来证据。','',
'1/2/3倍成本包含5bp手续费、1bp半价差、2bp滑点、0.5×过去20完整日样本log波动×sqrt(实际数量×OPEN/过去20日quoteADV)冲击；原生Decimal28、逆向tick／LOT／minnotional、参与率<=0.001、开仓后费用抵押1x上限。永续不假设借现货，实际settlement纳秒／mark／当时数量记资金费，负支出乘压力、正收入不放大，未来资金费不进入信号或数量。1%闭合小时mark不利高低维护代理不是逐tick清算、历史完整档位、L2/TCA或容量证明。','',
'|配置|1x净%|2x净%|3x净%|3x完整DD%|正月折1x/12|正五日折1/2/3x|状态|','|---|---:|---:|---:|---:|---:|---|---|']
for c in configs.values():lines.append('|'+c['name']+'|'+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|rejected|')
lines+=['',f'失败项计数：{json.dumps(dict(fail),ensure_ascii=False)}。全部新配置近期一致性不足，完整9格中两个scope各0格满足当前全部成本近期6/8规则；全年正收益平台不能替代近期稳健性。旧S28/H2父组合原passed仅指当时较窄历史门槛，登记资格和原报告字节保持，未按当前更严门槛改写。','',f"预设延伸S35/H2父组合三档收益{representative['scenes']['1']['net_return_pct']:.6f}%／{representative['scenes']['2']['net_return_pct']:.6f}%／{representative['scenes']['3']['net_return_pct']:.6f}%，3倍完整回撤{representative['scenes']['3']['max_drawdown_pct']:.6f}%，近期五日正折4/8；旧S28/H2三倍收益6.202339%，新值更低。两个父组合本金及名义入场预算相同，但实际信号、换手和风险不同，不称等风险比较。单ETH银行与父组合分scope比较，不能直接以其更高收益证明更优配置。",'',
'独立审计按Fraction重算5550条新决策，按Decimal逐笔重建成交、费用、资金费、状态段和完整净值，再核对全部月折／近期折与小时维护代理；旧源从实际保存现金／数量／入场价重建并核验原始NAV SHA，不调用原策略模拟。详见verification.json；旧原SMA65及单S28账户按保存状态另行续接，未替换成这批新参数，paper10只读。','',
'文献只提供研究背景：[AQR Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)的传统期货12个月证据并不验证本研究短周期ETH策略。所有成本假设和数据局限保留，回测正收益不代表稳定实盘盈利。','',
'复现与核验命令见reproduce.md；完整原始账本/逐配置spec/report/数据哈希、负结果及前向状态保留。main提交、push及完整远端tree/blob证明写入.git/automation_proofs/20261031T054241Z.json，不预写成功SHA。']
(R/'result.md').write_text('\n'.join(lines)+'\n')
print(json.dumps(summary),flush=True)
