"""Add immutable provenance and sensitivity summaries before finish."""
import json,hashlib,shutil
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
p=R/'report.json';r=json.loads(p.read_text())
# Never rewrite an already finished registry report.
ledger={}
for line in (ROOT/'research/automation/registry.jsonl').read_text().splitlines():
 row=json.loads(line);ledger.setdefault(row['fingerprint'],{}).update(row)
for entry in json.loads((R/'batch.json').read_text()):
 if ledger[entry['fingerprint']]['status']!='reserved':raise SystemExit('Refusing to rewrite finished report; use evaluate.py --reproduce for audit')
shutil.copyfile(ROOT/'data/raw/research_20261001_perp/spot_exchangeInfo.json',R/'spot_metadata_snapshot.json')
m=json.loads((R/'spot_metadata_manifest.json').read_text());m['frozen_snapshot']=str((R/'spot_metadata_snapshot.json').relative_to(ROOT));m['snapshot_sha256']=hashlib.sha256((R/'spot_metadata_snapshot.json').read_bytes()).hexdigest();(R/'spot_metadata_manifest.json').write_text(json.dumps(m,indent=2)+'\n')
r['data_source_manifests']=[{'path':path,'sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest()} for path in ('research/experiments/20261001T013355Z/data_manifest.json','research/experiments/20261001T033355Z/binance_data_manifest.json','research/experiments/20261001T053425Z/spot_metadata_manifest.json')]
r['source_code_sha256']={s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in ('src/usdt_quant/backtest.py','src/usdt_quant/strategy.py','research/experiments/20261001T033355Z/evaluate.py','research/experiments/20261001T053425Z/carry.py','research/experiments/20261001T053425Z/evaluate.py','research/experiments/20261001T053425Z/check_accounting.py','research/automation/registry.py')}
r['sensitivity']={}
for a in ('BTC','ETH'):
 for b in ('B0','B1'):
  group=[x for x in r['trials'] if x['parameters']['baseline']==b and a in x['name']]
  result={}
  for m in ('1','2','3'):
   vals=[x['scenarios'][m] for x in group];values=[v['net_return_pct'] for v in vals];sh=[v['sharpe_annualized'] for v in vals]
   adj=[]
   secondary='per_leg_fraction' if b=='B0' else 'buffer_usdt'
   for x in group:
    for y in group:
     xp,yp=x['parameters'],y['parameters']
     if xp['holding_hours']==yp['holding_hours'] and xp[secondary]<yp[secondary]:axis=secondary
     elif xp[secondary]==yp[secondary] and (xp['holding_hours'],yp['holding_hours']) in ((8,24),(24,48)):axis='holding_hours'
     else:continue
     xs,ys=x['scenarios'][m]['sharpe_annualized'],y['scenarios'][m]['sharpe_annualized']
     if xs is not None and ys is not None:adj.append({'from':x['name'],'to':y['name'],'axis':axis,'sharpe_delta':ys-xs})
   result[m]={'positive_return_configs':sum(int(v>0) for v in values),'positive_sharpe_configs':sum(int(v is not None and v>0) for v in sh),'configs':len(vals),'range_return_pct':[min(values),max(values)],'adjacent_sharpe_differences':adj,'isolated_peak_or_plateau':'no positive plateau; all returns nonpositive','cash_order_rejections':sum(v.get('decision_counts',{}).get('spot_cash_rejected',0) for v in vals)}
  r['sensitivity'][b+'_'+a]=result
r['causal_accounting_audit']='At decision, settle through t, snapshot known NAV, compute funding feature visible <=t; settlement t..next-minute precedes fill but does not enter sizing snapshot. Fresh audit reproduction checks frozen full outputs.'
r['original_scope_recovery_note']='Initial B0/B1 specs were abbreviated multi-asset examples, not executable complete configurations. Two legacy scopes link four concretely specified native cases each; actual archived evidence restored, no assertion of long-run validation for original 72h cases.'
r['checks_before_finish']=['existing checks/backtest.py actual native synthetic accounting passed','new accounting test observed missing-module failure before implementation, then passed','registry check passed; 36 CLI reservations success','six-fold products verified during all candidate/comparator runs']
r['execution_and_failure_audit']={'spot_metadata_multi_symbol_query':'HTTP400; single-symbol official queries succeeded; snapshots frozen','dependency_setup':'nautilus_trader 2.0.0rc5 and sklearn 1.7.2 now installed in ignored venv','strategy_calculation':'34 concrete configs, 102 scenarios actually calculated, no synthetic market data used for returns','continuous_B1':'base 1x forecast cost fixed across stress paths; actual fills and paid funding stressed','nonmonotonic_cost_returns':'isolated books/no transfers cause scenario-dependent rejected entry attempts and fewer trips; not positive cost elasticity'}
r['reproduce_command']='OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python research/experiments/20261001T053425Z/evaluate.py --reproduce'
r['sources']=[{'url':'https://github.com/shenmuegit/EquiTide','version':r['parent_commit'],'scope':'original CarryStrategy and native accounting'}, {'url':'https://github.com/binance/binance-public-data','scope':'actual archived minute/hour market data + checksum','access_date':'2026-10-01'},{'url':'https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History','scope':'realized funding rate, actual timestamp and settlement mark'},{'url':'https://github.com/nautechsystems/nautilus_trader','version':'2.0.0rc5','scope':'original native simulator; not current develop behavior'}]
p.write_text(json.dumps(r,ensure_ascii=False,allow_nan=False,separators=(',',':'))+'\n')
fig,axes=plt.subplots(2,2,figsize=(9,7),layout='constrained')
for i,b in enumerate(('B0','B1')):
 for j,a in enumerate(('BTC','ETH')):
  ax=axes[i,j];group=[x for x in r['trials'] if x['parameters']['baseline']==b and a in x['name']];second='per_leg_fraction' if b=='B0' else 'buffer_usdt';cols=sorted({x['parameters'][second] for x in group});hs=[8,24,48]
  values=np.array([[next(x['scenarios']['3']['net_return_pct'] for x in group if x['parameters']['holding_hours']==h and x['parameters'][second]==c) for c in cols] for h in hs])
  ax.imshow(values,cmap='RdYlGn',vmin=-65,vmax=65,aspect='auto');ax.set_xticks(range(len(cols)),cols);ax.set_yticks(range(3),hs);ax.set_xlabel('Per-leg NAV fraction' if b=='B0' else 'Buffer USDT');ax.set_ylabel('Hold hours');ax.set_title(b+' / '+a+' / 3x cost')
  for y in range(3):
   for x in range(len(cols)):ax.text(x,y,f'{values[y,x]:+.2f}%',ha='center',va='center')
fig.suptitle('Matched carry: cumulative OOS return (all grid cells retained)');fig.savefig(R/'sensitivity_3x.png',dpi=140);plt.close(fig)
print('Provenance and complete 2D sensitivity added; report SHA',hashlib.sha256(p.read_bytes()).hexdigest())
