#!/usr/bin/env python3
import csv,gzip,hashlib,json,math,statistics,sys
from pathlib import Path
from statistics import NormalDist
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
report=json.loads((R/'report.json').read_text());batch=json.loads((R/'batch.json').read_text())
candidates=[x for x in batch if not x['is_comparator']]
rank=report['summary']['ranking_1x']
rows=[]
for b in candidates:
 s=json.loads((ROOT/b['spec']).read_text());c=report['configs'][b['name']]['scenarios']
 rows.append({'name':b['name'],'lookback_days':s['parameters']['lookback_days'],'absolute_return_hurdle':s['parameters']['absolute_return_hurdle'],'return_1x_pct':c['1']['net_return_pct'],'return_2x_pct':c['2']['net_return_pct'],'return_3x_pct':c['3']['net_return_pct'],'max_dd_1x_pct':c['1']['max_drawdown_pct'],'max_dd_3x_pct':c['3']['max_drawdown_pct'],'positive_1x_folds':c['1']['positive_1x_folds'],'cost_1x_usdt':c['1']['cost_usdt'],'round_trips_1x':c['1']['round_trips'],'gross_to_cost_1x':c['1']['gross_reference_pnl_to_cost'],'neighborhood_positive_fraction_3x':c['3']['neighborhood_positive_fraction_3x'],'status':report['configs'][b['name']]['status']})
with (R/'sensitivity.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# Full two-axis net-return surface at base cost.
surf=np.zeros((3,3));
for row in rows:
 i=[20,40,60].index(row['lookback_days']);j=[0.0,0.02,0.04].index(row['absolute_return_hurdle']);surf[i,j]=row['return_1x_pct']
fig,ax=plt.subplots(figsize=(7.2,4.6),constrained_layout=True);im=ax.imshow(surf,cmap='RdYlGn',aspect='auto',vmin=-35,vmax=10)
ax.set_xticks(range(3),['0%','2%','4%']);ax.set_yticks(range(3),['20d','40d','60d']);ax.set_xlabel('绝对动量门槛');ax.set_ylabel('回看期');ax.set_title('BTC/ETH相对强度轮动：1x净收益 (%)')
for i in range(3):
 for j in range(3):ax.text(j,i,f'{surf[i,j]:.1f}%',ha='center',va='center',color='black')
fig.colorbar(im,ax=ax,label='净收益 %');fig.savefig(R/'sensitivity_surface.svg',format='svg');plt.close(fig)
# Adjacent return jumps across the predeclared 3x3 surface.
diffs=[]
for h in (0.0,0.02,0.04):
 v=[next(x['return_1x_pct'] for x in rows if x['lookback_days']==l and x['absolute_return_hurdle']==h) for l in (20,40,60)]
 diffs.extend(abs(v[i+1]-v[i]) for i in range(2))
for l in (20,40,60):
 v=[next(x['return_1x_pct'] for x in rows if x['lookback_days']==l and x['absolute_return_hurdle']==h) for h in (0.0,0.02,0.04)]
 diffs.extend(abs(v[i+1]-v[i]) for i in range(2))
mean_diff=statistics.mean(diffs);sd_diff=statistics.stdev(diffs);max_diff=max(diffs);cliff=max_diff>2*sd_diff
# DSR using daily mark returns for the best 1x parameter and all completed unique historical fingerprints + current grid.
best=rank[0]
with gzip.open(ROOT/'data/runs'/R.name/f'{best}_cost1.json.gz','rt',encoding='utf-8') as f: archive=json.load(f)
nav=np.asarray(archive['daily_nav_usdt'],dtype=float);rets=nav[1:]/nav[:-1]-1
from scipy.stats import skew,kurtosis
sr=float(np.mean(rets)/np.std(rets,ddof=1)*math.sqrt(365))
sk=float(skew(rets,bias=False));ku=float(kurtosis(rets,fisher=False,bias=False))
records=registry.read_records(ROOT/'research/automation/registry.jsonl')
previous_completed=sum(1 for x in records.values() if x.get('result_available') is True)
trials=previous_completed+len(candidates)
em=0.5772156649;normal=NormalDist();expected=normal.inv_cdf(1-1/trials)*(1-em)+em*normal.inv_cdf(1-1/(trials*math.e))
srstd=math.sqrt((1-sk*sr+(ku-1)/4*sr**2)/(len(rets)-1))
dsr=normal.cdf((sr-expected)/srstd)
report['sensitivity_analysis']={'axes':['lookback_days','absolute_return_hurdle'],'grid_shape':[3,3],'robustness_fraction_net_positive':{str(m):sum(x[f'return_{m}x_pct']>0 for x in rows)/len(rows) for m in (1,2,3)},'adjacent_1x_return_abs_differences_percentage_points':diffs,'max_adjacent_difference_pp':max_diff,'mean_adjacent_difference_pp':mean_diff,'std_adjacent_difference_pp':sd_diff,'cliff_flag_2sd':cliff,'surface':'sensitivity_surface.svg','multiple_testing':{'previous_completed_unique_registry_configurations':previous_completed,'current_trials':len(candidates),'total_trials_for_dsr':trials,'best_1x_config':best,'daily_sharpe_365':sr,'daily_return_skew':sk,'daily_return_kurtosis_non_excess':ku,'deflated_sharpe_probability':dsr,'interpretation':'DSR is a multiple-testing diagnostic on reused development history, not independent evidence; cross-strategy trial dependence is not modeled.'}}
report['summary']['candidate_positive_fraction_1x']=report['sensitivity_analysis']['robustness_fraction_net_positive']['1']
report['summary']['candidate_positive_fraction_2x']=report['sensitivity_analysis']['robustness_fraction_net_positive']['2']
report['summary']['candidate_positive_fraction_3x']=report['sensitivity_analysis']['robustness_fraction_net_positive']['3']
(R/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
print(json.dumps(report['sensitivity_analysis'],ensure_ascii=False));
