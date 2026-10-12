#!/usr/bin/env python3
import csv,gzip,hashlib,json,math,statistics,sys
from pathlib import Path
from statistics import NormalDist
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
r=json.loads((R/'report.json').read_text());batch=json.loads((R/'batch.json').read_text());rows=[]
for b in batch:
 if b['is_comparator']:continue
 spec=json.loads((ROOT/b['spec']).read_text());sc=r['configs'][b['name']]['scenarios']
 rows.append({'name':b['name'],'lookback_days':spec['parameters']['lookback_days'],'entry_zscore_threshold':spec['parameters']['entry_zscore_threshold'],'return_1x_pct':sc['1']['net_return_pct'],'return_2x_pct':sc['2']['net_return_pct'],'return_3x_pct':sc['3']['net_return_pct'],'max_drawdown_1x_pct':sc['1']['max_drawdown_pct'],'max_drawdown_3x_pct':sc['3']['max_drawdown_pct'],'positive_1x_folds':sc['1']['positive_1x_folds'],'round_trips_1x':sc['1']['round_trips'],'cost_1x_usdt':sc['1']['cost_usdt'],'gross_reference_pnl_to_cost_1x':sc['1']['gross_reference_pnl_to_cost'],'neighborhood_positive_fraction_3x':sc['3']['neighborhood_positive_fraction_3x'],'status':r['configs'][b['name']]['status']})
with (R/'sensitivity.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
look=[20,40,60];thrs=[1.0,1.5,2.0];surf=np.zeros((3,3))
for x in rows:surf[look.index(x['lookback_days']),thrs.index(x['entry_zscore_threshold'])]=x['return_1x_pct']
fig,ax=plt.subplots(figsize=(7.2,4.6),constrained_layout=True);im=ax.imshow(surf,cmap='RdYlGn',aspect='auto',vmin=-50,vmax=10)
ax.set_xticks(range(3),['1.0','1.5','2.0']);ax.set_yticks(range(3),['20d','40d','60d']);ax.set_xlabel('Entry z-score');ax.set_ylabel('Ratio reference window');ax.set_title('BTC/ETH ratio mean-reversion rotation: 1x net return (%)')
for i in range(3):
 for j in range(3):ax.text(j,i,f'{surf[i,j]:.1f}%',ha='center',va='center',color='black')
fig.colorbar(im,ax=ax,label='Net return %');fig.savefig(R/'sensitivity_surface.svg',format='svg');plt.close(fig)
# Adjacent 1x return differences for both grid dimensions.
diffs=[]
for h in thrs:
 v=[next(x['return_1x_pct'] for x in rows if x['lookback_days']==l and x['entry_zscore_threshold']==h) for l in look];diffs.extend(abs(v[i+1]-v[i]) for i in range(2))
for l in look:
 v=[next(x['return_1x_pct'] for x in rows if x['lookback_days']==l and x['entry_zscore_threshold']==h) for h in thrs];diffs.extend(abs(v[i+1]-v[i]) for i in range(2))
mu=statistics.mean(diffs);sd=statistics.stdev(diffs);cliff=max(diffs)>2*sd
best=r['summary']['ranking_1x'][0]
with gzip.open(ROOT/'data/runs'/R.name/f'{best}_cost1.json.gz','rt',encoding='utf-8') as f:arc=json.load(f)
nav=np.asarray(arc['daily_nav_usdt'],dtype=float);ret=nav[1:]/nav[:-1]-1
from scipy.stats import skew,kurtosis
sr=float(np.mean(ret)/np.std(ret,ddof=1)*math.sqrt(365));sk=float(skew(ret,bias=False));ku=float(kurtosis(ret,fisher=False,bias=False))
completed=sum(1 for x in registry.read_records(ROOT/'research/automation/registry.jsonl').values() if x.get('result_available') is True);trials=completed+len(rows);em=0.5772156649;nd=NormalDist();expected=nd.inv_cdf(1-1/trials)*(1-em)+em*nd.inv_cdf(1-1/(trials*math.e));srstd=math.sqrt((1-sk*sr+(ku-1)/4*sr*sr)/(len(ret)-1));dsr=nd.cdf((sr-expected)/srstd)
r['sensitivity_analysis']={'axes':['lookback_days','entry_zscore_threshold'],'grid_shape':[3,3],'positive_fraction_net_returns':{f'{m}x':sum(x[f'return_{m}x_pct']>0 for x in rows)/len(rows) for m in (1,2,3)},'adjacent_1x_return_differences_pp':diffs,'max_adjacent_difference_pp':max(diffs),'mean_adjacent_difference_pp':mu,'std_adjacent_difference_pp':sd,'cliff_flag_2sd':cliff,'surface':'sensitivity_surface.svg','multiple_testing':{'previous_unique_completed_trials':completed,'current_trials':len(rows),'total_trials':trials,'best_config':best,'daily_sharpe_365':sr,'return_skew':sk,'return_kurtosis_non_excess':ku,'deflated_sharpe_probability':dsr,'interpretation':'DSR diagnostic on reused development history; normal-moment approximation and correlated trials limit the value as independent evidence.'}}
r['summary'].update({'positive_fraction_1x':r['sensitivity_analysis']['positive_fraction_net_returns']['1x'],'positive_fraction_2x':r['sensitivity_analysis']['positive_fraction_net_returns']['2x'],'positive_fraction_3x':r['sensitivity_analysis']['positive_fraction_net_returns']['3x']})
(R/'report.json').write_text(json.dumps(r,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
print(json.dumps(r['sensitivity_analysis'],ensure_ascii=False))
