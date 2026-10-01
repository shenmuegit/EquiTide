"""Visualize every frozen sensitivity cell, without any further strategy calculations."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROUND=Path(__file__).resolve().parent
r=json.loads((ROUND/'report.json').read_text());grid=r['plan']['grid'];ns=grid['lookback_days']
fig,axs=plt.subplots(1,3,figsize=(15,4.8))
for ax,group in zip(axs,('BTC','ETH','combination')):
    xs=grid['raw_BTC_capital_weights'] if group=='combination' else grid['symmetric_band_fraction']
    arr=np.empty((3,3))
    for name,row in r['configs'].items():
        if group=='combination' and row['role']=='combination':a,b=row['lookback_days'],row['raw_weights'][0]
        elif row['role']=='core' and row['asset']==group:a,b=row['parameters']['lookback_days'],row['parameters']['symmetric_band_fraction']
        else:continue
        arr[ns.index(a),xs.index(b)]=row['scenes']['3']['net_return_pct']
    bound=max(1,float(np.max(np.abs(arr))))
    im=ax.imshow(arr,cmap='RdYlGn',vmin=-bound,vmax=bound)
    ax.set_xticks(range(3),[f'{v:.0%}' if group=='combination' else f'{v:.1%}' for v in xs]);ax.set_yticks(range(3),ns)
    ax.set_xlabel('BTC initial weight' if group=='combination' else 'Symmetric band');ax.set_ylabel('SMA days')
    ax.set_title(group+' / 3x costs')
    for i in range(3):
        for j in range(3):ax.text(j,i,f'{arr[i,j]:+.2f}%',ha='center',va='center',fontsize=11)
fig.suptitle('Preregistered SMA hysteresis: all cells retained; development history')
fig.tight_layout();fig.savefig(ROUND/'sensitivity_3x.png',dpi=150);plt.close(fig)
print('Saved all27 core/portfolio grid cells;12 capital variants are in CSV/report')
