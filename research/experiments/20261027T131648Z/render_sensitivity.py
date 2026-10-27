"""Re-render existing saved metrics with readable rectangular cells; no financial evaluation."""
import hashlib,itertools,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import R,SLOWS,LOOKS,grid_configs,sha,put
r=json.loads((R/'report.json').read_text());before=sha(R/'report.json');grid=grid_configs(r['configs']);old={n:sha(R/n) for n in ['sensitivity_native.png','sensitivity_parent.png']}
for scope in ['native','parent']:
 cells=[c for c in grid.values() if c['scope']==scope];fields=['trend_lookback_days','lookback_days'] if scope=='native' else ['trend_filter_lookback_days','reversal_lookback_days'];by={tuple(c[p] for p in fields):c for c in cells};assert set(by)==set(itertools.product(SLOWS,LOOKS));fig,axs=plt.subplots(3,2,figsize=(12,10),layout='constrained')
 for i,field in enumerate(['net_return_pct','sharpe_365','max_drawdown_pct']):
  values=[(c['scenes']['3']['recent40'] if recent else c['scenes']['3'])[field] for c in cells for recent in [False,True]];limit=max([abs(v) for v in values if v is not None] or [1]) or 1
  for j,recent in enumerate([False,True]):
   mat=np.asarray([[(by[S,L]['scenes']['3']['recent40'] if recent else by[S,L]['scenes']['3'])[field] for L in LOOKS] for S in SLOWS],dtype=float);im=axs[i,j].imshow(mat,aspect='auto',cmap='RdYlGn_r' if field=='max_drawdown_pct' else 'RdYlGn',vmin=0 if field=='max_drawdown_pct' else -limit,vmax=limit);axs[i,j].set_title(('Inherited40days' if recent else '370days')+' / 3x '+field);axs[i,j].set_xticks(range(len(LOOKS)),LOOKS);axs[i,j].set_yticks(range(len(SLOWS)),SLOWS);axs[i,j].set_xlabel('ETH reversal lookback L(days)');axs[i,j].set_ylabel('ETH slow gate S(days)')
   for y,x in itertools.product(range(len(SLOWS)),range(len(LOOKS))):axs[i,j].text(x,y,('n/a' if np.isnan(mat[y,x]) else f'{mat[y,x]:+.3f}')+('*' if by[SLOWS[y],LOOKS[x]].get('read_only_anchor') else ''),ha='center',va='center',fontsize=10)
   fig.colorbar(im,ax=axs[i,j])
 fig.suptitle(scope+' / '+('ETH10000bank,N3000' if scope=='native' else 'BTC1000+ETH3000entrybudgets,two10000banks raw1/1')+'\nH2%/ETHzeroexit; *old actual S25/28/31 cells;knownhistory');fig.savefig(R/f'sensitivity_{scope}.png',dpi=120);plt.close(fig)
assert sha(R/'report.json')==before
put(R/'figure_revision.json',{'reason':'Visual inspection showed annotations touching adjacent columns with5rows/defaultsquareaspect. Use aspect=auto and10ptannotation;all metric values,source rows andreport bytes unchanged.','old_figure_sha256':old,'new_figure_sha256':{n:sha(R/n) for n in old},'financial_report_sha256':before,'financial_evaluations':0,'figures':2,'panels':12});print('PASS:two saved-metric figures/12panels rendered with readable rectangular cells;financial report byteidentical,no backtest.')
