#!/usr/bin/env python3
import csv,gzip,json,math,statistics,sys
from pathlib import Path
from statistics import NormalDist
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'research/automation'));import registry
report=json.loads((R/'report.json').read_text());batch=json.loads((R/'batch.json').read_text());rows=[]
for b in batch:
 if b['is_comparator']:continue
 p=json.load(open(b['spec']));c=report['configs'][b['name']]['scenarios']
 rows.append({'name':b['name'],'asset':b['asset'],'entry_15m_drop_fraction':p['parameters']['entry_15m_drop_fraction'],'max_holding_15m_bars':p['parameters']['max_holding_15m_bars'],'return_1x_pct':c['1']['net_return_pct'],'return_2x_pct':c['2']['net_return_pct'],'return_3x_pct':c['3']['net_return_pct'],'max_drawdown_1x_pct':c['1']['max_drawdown_pct'],'max_drawdown_3x_pct':c['3']['max_drawdown_pct'],'positive_1x_folds':c['1']['positive_1x_folds'],'round_trips_1x':c['1']['round_trips'],'cost_1x_usdt':c['1']['cost_usdt'],'gross_reference_pnl_to_cost_1x':c['1']['gross_reference_pnl_to_cost'],'neighborhood_positive_fraction_3x':c['3']['neighborhood_positive_fraction_3x'],'status':report['configs'][b['name']]['status']})
with (R/'sensitivity.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
holds=[1,4,12];thresholds=[.005,.01,.02];surfaces={};diffs=[]
for asset in ('BTC','ETH'):
 z=np.zeros((3,3))
 for x in rows:
  if x['asset']==asset:z[holds.index(x['max_holding_15m_bars']),thresholds.index(x['entry_15m_drop_fraction'])]=x['return_1x_pct']
 surfaces[asset]=z
 for i in range(2):
  for j in range(3):diffs.append(float(abs(z[i+1,j]-z[i,j])))
 for i in range(3):
  for j in range(2):diffs.append(float(abs(z[i,j+1]-z[i,j])))
 fig,ax=plt.subplots(figsize=(7,4.5),constrained_layout=True);im=ax.imshow(z,cmap='RdYlGn',aspect='auto',vmin=-100,vmax=5)
 ax.set_xticks(range(3),['0.5%','1%','2%']);ax.set_yticks(range(3),['1 bar','4 bars','12 bars']);ax.set_xlabel('Entry drop threshold');ax.set_ylabel('Maximum holding horizon');ax.set_title(f'{asset} 15m shock-rebound: 1x net return (%)')
 for i in range(3):
  for j in range(3):ax.text(j,i,f'{z[i,j]:.1f}%',ha='center',va='center',color='black')
 fig.colorbar(im,ax=ax,label='Net return %');fig.savefig(R/f'sensitivity_surface_{asset}.svg',format='svg');plt.close(fig)
# Adjacent differences and DSR trial-count diagnostic on the best 1x variant.
mu=statistics.mean(diffs);sd=statistics.stdev(diffs);best=report['summary']['ranking_1x'][0]
with gzip.open(ROOT/'data/runs'/R.name/f'{best}_cost1.json.gz','rt',encoding='utf-8') as f:arc=json.load(f)
nav=np.asarray(arc['daily_nav_usdt'],dtype=float);ret=nav[1:]/nav[:-1]-1
from scipy.stats import skew,kurtosis
sr=float(np.mean(ret)/np.std(ret,ddof=1)*math.sqrt(365));sk=float(skew(ret,bias=False));ku=float(kurtosis(ret,fisher=False,bias=False));completed=sum(v.get('result_available') is True for v in registry.read_records(ROOT/'research/automation/registry.jsonl').values());trials=completed+len(rows);e=.5772156649;nd=NormalDist();emax=nd.inv_cdf(1-1/trials)*(1-e)+e*nd.inv_cdf(1-1/(trials*math.e));srstd=math.sqrt((1-sk*sr+(ku-1)/4*sr**2)/(len(ret)-1));dsr=nd.cdf((sr-emax)/srstd)
sa={'axes':['entry_15m_drop_fraction','max_holding_15m_bars'],'grid_per_asset':[3,3],'net_positive_fraction':{f'{m}x':sum(x[f'return_{m}x_pct']>0 for x in rows)/len(rows) for m in (1,2,3)},'adjacent_1x_return_abs_differences_pp':diffs,'max_adjacent_difference_pp':max(diffs),'mean_adjacent_difference_pp':mu,'std_adjacent_difference_pp':sd,'cliff_flag_2sd':max(diffs)>2*sd,'surfaces':{'BTC':'sensitivity_surface_BTC.svg','ETH':'sensitivity_surface_ETH.svg'},'multiple_testing':{'previous_completed_unique_configs':completed,'current_candidates':len(rows),'total_trials':trials,'best_1x_config':best,'daily_sharpe_365':sr,'daily_return_skew':sk,'daily_return_kurtosis_non_excess':ku,'deflated_sharpe_probability':dsr,'interpretation':'Approximate DSR on repeated history; correlated strategies violate the independent-trial ideal.'}}
report['sensitivity_analysis']=sa
for m in (1,2,3):report['summary'][f'positive_fraction_{m}x']=sa['net_positive_fraction'][f'{m}x']
(R/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
print(json.dumps(sa,ensure_ascii=False))
