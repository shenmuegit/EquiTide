"""Read-only exports of actual native amount replication and prior NAV-interest differences."""
import collections,csv,gzip,json,statistics
from decimal import Decimal as D
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import *
from run import recent_ok
rep=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());cfgs=rep['configs'];full=rep['all_current_grid'];axis=plan['scales'];oldcache={};arcs={}
def oldcfg(fp):
 if fp not in oldcache:
  ref=plan['read_only_references'][fp];doc=json.loads((ROOT/ref['report']).read_text());oldcache[fp]=next(c for c in doc['configs'].values() if c['fingerprint']==fp)
 return oldcache[fp]
def arc(c):
 fp=c['fingerprint']
 if fp not in arcs:arcs[fp]=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()))
 return arcs[fp]
def write(name,cols,rows):
 with (R/name).open('w',newline='') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(cols);w.writerows(rows)
cost=[];fold=[];tail=[];daily=[];gridrows=[];matched=[];edges=[];lotrows=[];decomp=[]
for c in cfgs.values():
 for k,s in c['scenes'].items():
  cost.append([c['name'],c['scope'],c['role'],c['asset'],c['capital_usdt'],c.get('bank_scale'),c.get('raw_BTC_bank_scale'),c.get('raw_ETH_bank_scale'),k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(x['net_return_pct']>0 for x in s['recent40']['folds']),c['status']])
  fold.extend([c['name'],c['scope'],c['role'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  tail.extend([c['name'],c['scope'],c['role'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],c['role'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
  if c['scope']=='parent' and c['role']=='candidate':
   g=next(g for g in plan['grid'] if g['role']=='benchmark' and g['wB']==c['raw_BTC_bank_scale'] and g['wE']==c['raw_ETH_bank_scale']);b=full[g['fingerprint']]['scenes'][k];matched.append([c['name'],k,c['capital_usdt'],c['raw_BTC_bank_scale'],c['raw_ETH_bank_scale'],g['fingerprint'],g['readonly'],s['net_return_pct'],b['net_return_pct'],s['net_return_pct']-b['net_return_pct'],s['max_drawdown_pct'],b['max_drawdown_pct'],'Same actual bank initialcapital and fixed nominal entrybudgets; different signals/timing/held exposure, not equal-risk portfolios.'])
for scope,items in [('native',plan['native_grid']),('parent',plan['grid'])]:
 for g in items:
  c=full[g['fingerprint']];gridrows.append([scope,g['role'],g.get('asset','COMBO'),g.get('bank_scale'),g.get('wB'),g.get('wE'),c['capital_usdt'],g['fingerprint'],g['readonly'],c['status'],c['scenes']['3']['net_return_pct'],c['scenes']['3']['max_drawdown_pct'],c['scenes']['3']['sharpe_365'],c['scenes']['3']['calmar'],*[sum(z['net_return_pct']>0 for z in c['scenes'][k]['recent40']['folds']) for k in ['1','2','3']],recent_ok(c)])
for x in rep['NAV_interest_replication_comparisons']:
 k=str(x['cost_multiplier']);a=full[x['native_fp']]['scenes'][k];b=oldcfg(x['NAV_interest_fp'])['scenes'][k];gross=a['gross_reference_price_PnL_usdt']-b['gross_reference_price_PnL_usdt'];fund=a['funding_usdt']-b['funding_usdt'];costdiff=a['cost_usdt']-b['cost_usdt'];net=gross+fund-costdiff;assert abs(net-x['return_difference_pp']*x['capital_usdt']/100)<2e-8
 decomp.append([x['role'],x['wB'],x['wE'],k,x['native_fp'],x['native_readonly'],x['NAV_interest_fp'],x['capital_usdt'],x['native_return_pct'],x['NAV_interest_return_pct'],x['return_difference_pp'],x['native_DD_pct'],x['NAV_interest_DD_pct'],gross,fund,costdiff,net,'Native LOT changes pricePnL/exposure/funding as well as nonlinear execution costs; total return difference is not attributed solely to costs.'])
for g in plan['native_grid']:
 if g['bank_scale']==1:continue
 unit=next(x for x in plan['native_grid'] if x['role']==g['role'] and x['asset']==g['asset'] and x['bank_scale']==1);a,b=arc(full[g['fingerprint']]),arc(full[unit['fingerprint']]);scale=D(str(g['bank_scale']))
 meta=next(x for x in plan['data']['assets'][g['asset']] if x['path'].endswith('perp_instrument_meta.parquet'));assert sha(ROOT/meta['path'])==meta['sha256'];LOT=D(core.pl.read_parquet(ROOT/meta['path']).to_dicts()[0]['lot_size'])
 for k in ['1','2','3']:
  ts=lambda z:(z['trade_ts_ns'],z['opening'],z['terminal']);aa=[z for z in a['scenes'][k]['trades'] if z['status']=='filled'];bb={ts(z):z for z in b['scenes'][k]['trades'] if z['status']=='filled'};assert len(aa)==len(bb) and all(ts(t) in bb for t in aa)
  for t in aa:
   u=bb[ts(t)];actual=D(t['quantity']);scaled=scale*D(u['quantity']);lotrows.append([g['role'],g['asset'],g['bank_scale'],k,g['fingerprint'],unit['fingerprint'],t['trade_ts_ns'],t['opening'],t['terminal'],str(actual),str(scaled),str(actual-scaled),scaled%LOT==0,t['impact_rate'],u['impact_rate'],t['cost_parts']['impact'],str(scale*D(u['cost_parts']['impact'])),t['cost_usdt'],str(scale*D(u['cost_usdt']))])
for scope in ['native','parent']:
 groups=[(role,asset) for role in ['candidate','benchmark'] for asset in (['BTC','ETH'] if scope=='native' else ['COMBO'])]
 for role,asset in groups:
  entries=[g for g in (plan['native_grid'] if scope=='native' else plan['grid']) if g['role']==role and g.get('asset','COMBO')==asset]
  for k in ['1','2','3']:
   for g in entries:
    pairs=[]
    if scope=='native':
     ix=axis.index(g['bank_scale']);pairs=[h for h in entries if ix<2 and h['bank_scale']==axis[ix+1]]
    else:
     i,j=axis.index(g['wB']),axis.index(g['wE']);pairs=[h for h in entries if i<2 and h['wB']==axis[i+1] and h['wE']==g['wE'] or j<2 and h['wE']==axis[j+1] and h['wB']==g['wB']]
    for h in pairs:
     a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,role,asset,k,g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
write('cost_scenes.csv',['configuration','scope','role','asset','actual_initial_capital_usdt','bank_scale','BTC_bank_scale','ETH_bank_scale','cost_multiplier','net_return_pct','whole_OOS_DD_pct','sharpe365','calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','underlying_executions','underlying_closes','recent40_return_pct','recent_positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','role','cost_multiplier','fold','start_utc','end_exclusive_utc','days','net_return_pct','whole_fold_DD_pct','sharpe365','calmar'],fold)
write('recent40_folds.csv',['configuration','scope','role','cost_multiplier','fold','start_utc','end_exclusive_utc','net_return_pct','whole_fold_DD_pct','sharpe365','calmar'],tail)
write('daily_NAV.csv',['configuration','scope','role','cost_multiplier','boundary_index','actual_NAV_usdt'],daily)
write('sensitivity_grid.csv',['scope','role','asset','bank_scale','BTC_bank_scale','ETH_bank_scale','actual_capital_usdt','fingerprint','readonly_old_result','canonical_status','net3_pct','DD3_pct','Sharpe3','Calmar3','recent_positive5d_1','recent_positive5d_2','recent_positive5d_3','strict_recent_gate_diagnostic'],gridrows)
write('matched_hold_comparisons.csv',['candidate','cost_multiplier','same_actual_initial_capital_usdt','BTC_bank_scale','ETH_bank_scale','hold_fingerprint','hold_readonly','candidate_return_pct','hold_return_pct','difference_pp','candidate_DD_pct','hold_DD_pct','comparability_scope'],matched)
write('NAV_interest_replication_comparisons.csv',['role','BTC_bank_scale','ETH_bank_scale','cost_multiplier','native_fingerprint','native_readonly','prior_NAV_interest_fingerprint','same_initial_capital_usdt','native_return_pct','prior_return_pct','return_difference_pp','native_DD_pct','prior_DD_pct','reference_price_PnL_difference_usdt','funding_difference_usdt','execution_cost_difference_usdt','net_PnL_difference_usdt','scope'],decomp)
write('lot_impact_comparisons.csv',['role','asset','bank_scale','cost_multiplier','native_fp','unit_fp','trade_ns','opening','terminal','actual_native_quantity','linearly_scaled_unit_quantity','quantity_difference','scaled_quantity_native_LOT_valid','native_impact_rate','unit_impact_rate','native_impact_cost_usdt','linearly_scaled_unit_impact_usdt','native_execution_cost_usdt','linearly_scaled_unit_execution_cost_usdt'],lotrows)
write('adjacent_edges.csv',['scope','role','asset','cost_multiplier','from_fp','to_fp','absolute_Sharpe_change','absolute_return_difference_pp','absolute_DD_difference_pp'],edges)
flags={}
for scope,role,asset,k in {(x[0],x[1],x[2],x[3]) for x in edges}:
 ds=[x[6] for x in edges if x[:4]==[scope,role,asset,k]];threshold=2*statistics.stdev(ds) if len(ds)>1 else 0;flags['_'.join([scope,role,asset,k])]={'edge_count':len(ds),'max_Sharpe_change':max(ds),'two_std_change_threshold':threshold,'heuristic_flag':max(ds)>threshold,'scope':'Descriptive adjacent-edge statistic, not significance/PBO/DSR or independent samples.'}
put(R/'edge_flags.json',flags)
def chart(delta=False):
 fig,axs=plt.subplots(2,2 if delta else 4,figsize=(11,7) if delta else (17,8),layout='constrained')
 for row,role in enumerate(['candidate','benchmark']):
  functions=[('Native minus NAV-interest return pp',lambda c,g:next(x['return_difference_pp'] for x in rep['NAV_interest_replication_comparisons'] if x['role']==role and x['wB']==g['wB'] and x['wE']==g['wE'] and x['cost_multiplier']==3)),('Native minus NAV-interest DD pp',lambda c,g:next(x['native_DD_pct']-x['NAV_interest_DD_pct'] for x in rep['NAV_interest_replication_comparisons'] if x['role']==role and x['wB']==g['wB'] and x['wE']==g['wE'] and x['cost_multiplier']==3))] if delta else [('3x full370 return %',lambda c,g:c['scenes']['3']['net_return_pct']),('3x whole-curve DD %',lambda c,g:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c,g:c['scenes']['3']['sharpe_365']),('Recent positive5d at3x /8',lambda c,g:sum(z['net_return_pct']>0 for z in c['scenes']['3']['recent40']['folds']))]
  for col,(title,fn) in enumerate(functions):
   arr=np.empty((3,3))
   for g in plan['grid']:
    if g['role']==role:arr[axis.index(g['wB']),axis.index(g['wE'])]=fn(full[g['fingerprint']],g)
   ax=axs[row,col];opts={'vmin':0,'vmax':8} if not delta and col==3 else {};im=ax.imshow(arr,cmap='RdYlGn_r' if col==1 else 'RdYlGn',aspect='auto',**opts);ax.set_xticks(range(3),axis);ax.set_yticks(range(3),axis);ax.set_xlabel('Raw ETH native bank scale');ax.set_ylabel('Raw BTC native bank scale');ax.set_title(role+'\n'+title)
   for g in plan['grid']:
    if g['role']==role:
     i,j=axis.index(g['wB']),axis.index(g['wE']);ax.text(j,i,f'{arr[i,j]:.3f}'+(' O' if g['readonly'] else ' N'),ha='center',va='center',fontsize=8)
   fig.colorbar(im,ax=ax,shrink=.75)
 fig.suptitle(('Actual native replication minus prior funded-NAV-interest model\nLOT/exposure/pricePnL/funding and nonlinear costs all contribute' if delta else 'Actual native bank capital=10000*w, entrybudgets BTC1000*w / ETH3000*w\nO=old actual unchanged qualification, N=new actual | repeated development history'),fontsize=12);fig.savefig(R/('replication_difference.png' if delta else 'sensitivity.png'),dpi=140);plt.close(fig)
chart();chart(True)
fail={scope:{role:dict(collections.Counter(k for c in cfgs.values() if c['scope']==scope and c['role']==role for k in c['failed_criteria'])) for role in ['candidate','benchmark']} for scope in ['native','parent']};summary={'report_sha256':sha(R/'report.json'),'new_configs':20,'new_native':5,'new_parents':15,'cost_scenes':60,'failed_criteria_by_scope_role':fail,'positive_by_scope_role_cost':rep['summary']['positive_configs_by_scope_role_cost'],'strict_recent_parent_grid_qualified':{role:sum(recent_ok(full[g['fingerprint']]) for g in plan['grid'] if g['role']==role) for role in ['candidate','benchmark']},'native_lot_comparison_rows':len(lotrows),'actual_quantity_differs_from_scaled_unit_rows':sum(D(x[11])!=0 for x in lotrows),'scaled_unit_quantity_violates_LOT_rows':sum(not x[12] for x in lotrows),'CSV_rows':{'cost_scenes.csv':len(cost),'walk_forward_folds.csv':len(fold),'recent40_folds.csv':len(tail),'daily_NAV.csv':len(daily),'sensitivity_grid.csv':len(gridrows),'matched_hold_comparisons.csv':len(matched),'NAV_interest_replication_comparisons.csv':len(decomp),'lot_impact_comparisons.csv':len(lotrows),'adjacent_edges.csv':len(edges)}};put(R/'sensitivity_summary.json',summary)
g=next(g for g in plan['grid'] if g['role']=='candidate' and g['wB']==.5 and g['wE']==1.5);representative=full[g['fingerprint']];put(R/'representative.json',{'selection_policy':plan['representative_preset'],'configuration':representative})
lines=['# 原生资金规模与非线性成交成本复制','',
'本轮实际20个新定义／60成本场景：5个新原生银行＋15个父组合；其中3个原生候选＋8个候选父组合、2个原生持有＋7个持有父组合，全部rejected。新候选11个在1/2/3倍成本下均全年净正，9个持有对照均净负；全部正负收益、负折、失败和复现证据保留。7个原生格点及3个当前父格点已完成，直接复用，不因同family而排除新金额，也未改名重跑旧具体配置。','',
'固定原始银行尺度BTC、ETH各[0.5,1,1.5]，不归一化。BTC实际本金10000×wB、入场预算1000×wB；ETH实际本金10000×wE、入场预算3000×wE。两个完整实际银行按子组件原始乘数[1,1]相加，总本金10000×(wB+wE)。没有净值权益份额、线性缩放旧数量／费用、NAV复利调整、免费再平衡、跨银行借款或抵押抵消。BTC原规则L31/H4%/退出缓冲1%；ETH原S28/L3/H2%/零线退出、真实仓位决定是否保持，slow gate关闭即平仓、重开且现金时须新严格快ROC极值。所有源信号／成本与日期冻结后，20个具体定义逐项reserve成功才计算。','',
'新原生逐笔数量=floor(固定预算/前一完整日收盘/原生LOT)×LOT，下一UTC00:01真实OPEN加不利tick成交；同方向保持数量，反向先付费平旧仓，再按新预算开仓，终止付费平仓。5bp手续费、1bp半价差、2bp滑点、0.5×过去20完整日样本log波动×sqrt(实际q×OPEN/过去20日quoteADV)冲击，1/2/3倍压力，minnotional／参与率<=0.001／费用后抵押1x上限。实际settlement纳秒／mark／当时q记资金费，负支出加压、正收入不放大；永续不假设现货借币。1%闭合小时mark不利高低维护代理独立核对，仍非逐tick清算、历史完整档位或L2/TCA容量保证。','',
'三项验证：真实370日连续OOS从2025-10-19 UTC00:01至2026-10-24 UTC00:01，12完整30日折＋10日尾折；银行现金／数量／入场价／费用／资金费不重置，近期40日继承day330真实状态、8个5日折。无标签／新训练，purge horizon0，信号可得后60秒才执行。原生资产只改变资金与预算同比尺度一轴，信号参数固定；父组合同时改变BTC与ETH两个尺度，索引半径1含中心、角色／币种分开。沿用全部成本净正、9/12正月折、近期每档6/8正五日折、两个60%局部平台等原失败判据，不缩窄网格挽救旧结果。反复开发的历史不是未触碰最终测试集。','',
'|配置|范围/角色|本金|1x净%|2x净%|3x净%|3x完整DD%|正月折1x/12|正五日折1/2/3x|状态|','|---|---|---:|---:|---:|---:|---:|---:|---|---|']
for c in cfgs.values():lines.append('|'+c['name']+'|'+c['scope']+'/'+c['role']+f"|{c['capital_usdt']:.0f}|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|rejected|')
lines+=['',f"实际原生[0.5,1.5]预设代表本金20000（BTC5000／ETH15000；入场500／4500），三档净收益{representative['scenes']['1']['net_return_pct']:.6f}%／{representative['scenes']['2']['net_return_pct']:.6f}%／{representative['scenes']['3']['net_return_pct']:.6f}%，3倍完整DD{representative['scenes']['3']['max_drawdown_pct']:.6f}%；上轮纯净值权益模型三倍8.303062%，本轮8.208578%，差−0.094484个百分点。差异同时来自LOT取整导致的价格PnL、资金费敞口和非线性成交成本，不能把全部差值称额外手续费。54逐格／逐成本对比分解和真实逐笔数量／冲击对照保留。",'',
f"数量／冲击对照共{len(lotrows)}行，其中{summary['actual_quantity_differs_from_scaled_unit_rows']}行实际数量不同于旧单位数量×尺度，{summary['scaled_unit_quantity_violates_LOT_rows']}行直接线性缩放会违反原生LOT。每笔原始下单量、lagged ADV/sigma、成本分解、资金费和状态段均在源或本轮archive，可完整重建545013点净值；未提交可重建大数组。",'',
'两个新父组合[0.5,1]与[0.5,1.5]仍在单点达到全年三档净正、近期每档6/8及其余点指标，但局部严格近期合格只有1/3、1/2，低于60%，均淘汰；其余候选也缺近期一致性。旧1/1的历史passed及所有26个来源资格保持原样，未用当前更严门槛改写历史。持有对照按同实际初始本金及同入场预算匹配，实际信号、换手和风险仍不同；解析现金参考为0%，不伪造额外现金回测。','',
'父组合整体／逐折回撤、Sharpe与Calmar由联合完整净值计算，不平均单币指标。原生数量、资金规模和平方根冲击已经本轮实际建模核验；这不等于真实成交、精确清算或稳定实盘盈利。邻接Sharpe变化启发式、格点极值与重复来源依赖只作描述，未声称DSR/PBO或多重选择校正。','',
'独立审计以Fraction重算5550条新原生日决策、按每个spec真实初始本金和预算重算LOT数量，并Decimal逐笔重建成交／资金费／费用／现金／小时风险，核对新15原生＋45父曲线及全部折／近期指标。已完成旧源只从保存状态重建并核验原始NAV SHA，没有重跑旧信号。','',
'首次运行在5个原生／15成本场景完整保存后，首个父组合1倍摘要因缺失MONEY/COUNTS常量中断；该父摘要未完整保存。原失败代码和日志保留；独立修复父汇总模块／恢复driver只读这些原生archive并核验原SHA，完成尚未完成的父组合，未重跑任何完整原生或父回测。首个未完成父摘要的统计在恢复时重算，已如实记录，不混同于已完成结果。原冻结账户单独续接，不替换为本轮新金额；详细账户、失败、登记／监控／main实际发布证据在封存段落及manifest。','',
'一手背景：[AQR交易成本研究](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)讨论传统股票实施成本与容量，不能证明本轮加密策略容量或收益。复现命令、完整成本表／逐变体／数据SHA／必要代码和账本保留。']
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
