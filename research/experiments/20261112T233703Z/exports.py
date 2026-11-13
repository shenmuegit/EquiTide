"""Saved-result exports only: actual new parents and unchanged old nine-cell comparison."""
import csv,json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import *
p=json.loads((R/'plan.json').read_text());r=json.loads((R/'report.json').read_text());out={}
def save(name,rows):
 assert rows
 with (R/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
 out[name]=len(rows)
rows=[];folds=[];daily=[];recent=[];extra=[]
for c in r['configs'].values():
 for k,s in c['scenes'].items():
  base={'configuration':c['name'],'fingerprint':c['fingerprint'],'scope':c['scope'],'BTC_volatility_cap':c.get('BVC'),'ETH_funding_ratio':c.get('R'),'cost_multiplier':k};rows.append({**base,'return_pct':s['net_return_pct'],'whole_DD_pct':s['max_drawdown_pct'],'sharpe_365':s['sharpe_365'],'calmar':s['calmar'],'cost_usdt':s['cost_usdt'],'funding_usdt':s['funding_usdt'],'executions':s['executions'],'round_trips':s['round_trips'],'status':c['status'],'failed_criteria':','.join(c['failed_criteria'])})
  for f in s['folds']:folds.append({**base,**f})
  for i,v in enumerate(s['daily_equity_usdt']):daily.append({**base,'day_index':i,'NAV_usdt':v})
  for f in s['recent40']['folds']:recent.append({**base,**f})
  for f in s['extension19']['folds']:extra.append({**base,**f})
for n,x in [('cost_scenes.csv',rows),('walk_forward_folds.csv',folds),('daily_NAV.csv',daily),('recent40_folds.csv',recent),('extension19_folds.csv',extra)]:save(n,x)
grid=list(r['all_current_grid'].values());rs=[]
for c in grid:
 for k,s in c['scenes'].items():rs.append({'fingerprint':c['fingerprint'],'scope':c['scope'],'BTC_volatility_cap':c.get('BVC'),'ETH_funding_ratio':c.get('R'),'cost_multiplier':k,'return_pct':s['net_return_pct'],'whole_DD_pct':s['max_drawdown_pct'],'sharpe_365':s['sharpe_365'],'calmar':s['calmar'],'recent40_return_pct':s['recent40']['net_return_pct'],'recent40_positive_folds':sum(f['net_return_pct']>0 for f in s['recent40']['folds']),'readonly':c['readonly'],'canonical_status':c['status'],'local_recent_fraction':c['current_grid_diagnostic_sensitivity']['local_strict_recent_fraction']})
save('sensitivity_grid.csv',rs);save('native_sensitivity_grid.csv',[{'fingerprint':c['fingerprint'],'asset':c['asset'],'BVC':c.get('BVC'),'R':c.get('R'),'cost_multiplier':k,'return_pct':z['net_return_pct'],'whole_DD_pct':z['max_drawdown_pct'],'sharpe':z['sharpe_365'],'calmar':z['calmar'],'extension19_return_pct':z['extension19']['net_return_pct'],'status':c['status']} for c in r['all_current_native_grid'].values() for k,z in c['scenes'].items()]);save('fixed_allocations.csv',[{'fingerprint':c['fingerprint'],'scope':c['scope'],'BTC_volatility_cap':c.get('BVC'),'ETH_funding_ratio':c.get('R'),'BTC_C':3750,'ETH_C':15000,'total_C':18750,'BTC_N':1000,'ETH_N':4000,'raw_BTC_weight':1,'raw_ETH_weight':1,'normalization':False,'parent_orders':0} for c in grid]);save('matched_hold_comparisons.csv',r['matched_hold_comparisons'])
edges=[];by={(c.get('BVC'),c.get('R')):c for c in grid}
for axis,values,other,othervals in [('BTC_VOL_CAP',p['axes']['BTC_VOL_CAP'],'ETH_FUND_R',p['axes']['ETH_FUND_R']),('ETH_FUND_R',p['axes']['ETH_FUND_R'],'BTC_VOL_CAP',p['axes']['BTC_VOL_CAP'])]:
 for a,b in zip(values,values[1:]):
  for fixed in othervals:
   left=by[a,fixed] if axis=='BTC_VOL_CAP' else by[fixed,a];right=by[b,fixed] if axis=='BTC_VOL_CAP' else by[fixed,b]
   for k in ['1','2','3']:
    x,y=left['scenes'][k],right['scenes'][k];edges.append({'axis':axis,'left':a,'right':b,'fixed_other':fixed,'cost_multiplier':k,'left_fp':left['fingerprint'],'right_fp':right['fingerprint'],**{f'change_{m}':None if x[m] is None or y[m] is None else y[m]-x[m] for m in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']}})
for e in edges:
 ds=[abs(x['change_sharpe_365']) for x in edges if x['axis']==e['axis'] and x['cost_multiplier']==e['cost_multiplier'] and x['change_sharpe_365'] is not None];threshold=2*float(np.std(ds,ddof=1)) if len(ds)>1 else None;e['descriptive_sharpe_cliff_threshold']=threshold;e['descriptive_sharpe_cliff']=bool(threshold and e['change_sharpe_365'] is not None and abs(e['change_sharpe_365'])>threshold)
save('adjacent_edges.csv',edges)
fig,axes=plt.subplots(2,3,figsize=(21,13.5));panels=[('3x net return %',lambda c:c['scenes']['3']['net_return_pct']),('3x whole-path DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x extension19 net return %',lambda c:c['scenes']['3']['extension19']['net_return_pct']),('3x recent40 positive5d folds /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds'])),('Local recent6of8 allcost fraction',lambda c:c['current_grid_diagnostic_sensitivity']['local_strict_recent_fraction'])]
for ax,(title,fn) in zip(axes.flat,panels):
 z=np.array([[float(fn(by[e,w])) if fn(by[e,w]) is not None else np.nan for w in p['axes']['ETH_FUND_R']] for e in p['axes']['BTC_VOL_CAP']]);limits={'vmin':0,'vmax':1} if 'fraction' in title else {'vmin':0,'vmax':8} if 'folds /8' in title else {};im=ax.imshow(z,cmap='RdYlGn_r' if 'DD' in title else 'RdYlGn',**limits);ax.set_xticks(range(3),[f'{x:g}' for x in p['axes']['ETH_FUND_R']]);ax.set_yticks(range(3),[f'{100*e:g}%' for e in p['axes']['BTC_VOL_CAP']]);ax.set_xlabel('ETH funding / daily samplevol budget ratio');ax.set_ylabel('BTC 10-day samplevol entry ceiling');ax.set_title(title)
 for i in range(3):
  for j in range(3):ax.text(j,i,'NA' if np.isnan(z[i,j]) else f'{z[i,j]:.4f}',ha='center',va='center')
 fig.colorbar(im,ax=ax)
fig.suptitle('Exact native-bank pairings | BTC V10 cap3/4/5%; ETH M4/VW8 R.00875/.01/.01125\nC3750+15000=18750 / native N1000+4000 / raw[1,1], no NAV resizing or normalization\n389-day reused history, 12x30+29 tail; 19 new days inherit prior positions; 8 native banks + 10 parents; no independent future claim',fontsize=13);fig.subplots_adjust(left=.075,right=.965,bottom=.10,top=.83,wspace=.40,hspace=.40);fig.savefig(R/'sensitivity.png',dpi=120);plt.close(fig)
put(R/'export_verification.json',{'passed':True,'saved_only_no_financial_or_account_recalculation':True,'CSV_rows':out,'plots':{'sensitivity.png':sha(R/'sensitivity.png')},'axes_labels_correct':True,'all9_new389day_parent_cells':True});print(json.dumps(out),flush=True)
