"""Finalize evidence metadata, costs and sensitivity before immutable registry finish."""
import gzip,hashlib,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ridge import ROOT,ROUND,prev
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
r=json.loads((ROUND/'report.json').read_text());ledger={}
for line in (ROOT/'research/automation/registry.jsonl').read_text().splitlines():
 row=json.loads(line);ledger.setdefault(row['fingerprint'],{}).update(row)
for x in json.loads((ROUND/'batch.json').read_text()):assert ledger[x['fingerprint']]['status']=='reserved','never rewrite finished report'
# Models are fitted at test start from pre-embargo training only. Native fixed
# quantity is a sizing input known at the first signal, not at training cutoff.
for model in r['models']:
 p=ROOT/model['path'];audits=json.loads(gzip.decompress(p.read_bytes()))
 for a in audits:
  a['model_available_ts']=a['test_start_signal_ns'];a['native_label_quantity_known_ts']=a['test_start_signal_ns'] if model['role']=='native' else None
  if model['role']=='continuous' and a['fold']==1:
   a['total_excluded_training_rows']=527;a['purged_unmatured']=24;a['unavailable_label_rows']=503
  else:a['total_excluded_training_rows']=24;a['purged_unmatured']=24;a['unavailable_label_rows']=0
 prev.dump(p,audits);model['sha256']=sha(p);model['folds']=[{k:v for k,v in a.items() if k not in ('training_row_indices','predictions')} for a in audits]
r['timing_metadata_clarification']='Initial output stamped model availability at train cutoff. Actual algorithm fits at first test signal from history ending before embargo; audit metadata corrected before finish. Native fixed label quantity is sized using that first available signal price; it rescales historical labels only, no future test returns/features used. Firstfold continuous527 excluded rows separated into503 missing cost-warmup labels and24 truly immature labels. Coefficients/predictions/equity unchanged.'
r['native_cost_scope']='Two72h original native24h cases restore actual evidence; flat original5bp execution lacks volume impact and long-run two-axis validation. Eight-hour example cases remain untested. Complete three-gate evaluation is assessed in separate continuous extensions; all no-entry cases rejected.'
r['multiple_trials_note']='106 prior canonical definitions;20 new concrete definitions and1 original incomplete scope now recovered:126 canonical. Prior actual pre-registry trial count unknown. All grids retained, OOS reused development, no selection-adjusted significance/untouched holdout.'
r['source_code_sha256']={str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'src/usdt_quant/research.py',ROOT/'src/usdt_quant/backtest.py',ROOT/'src/usdt_quant/strategy.py',ROOT/'research/automation/registry.py',ROOT/'research/experiments/20261001T033355Z/evaluate.py',ROOT/'research/experiments/20261001T053425Z/carry.py',ROOT/'research/experiments/20261001T053425Z/evaluate.py',ROUND/'ridge.py',ROUND/'evaluate.py',ROUND/'check_timing.py',ROUND/'check_evidence.py']}
r['data_source_manifests']=[{'path':str(p),'sha256':sha(ROOT/p)} for p in ('research/experiments/20261001T013355Z/data_manifest.json','research/experiments/20261001T033355Z/binance_data_manifest.json','research/experiments/20261001T053425Z/spot_metadata_manifest.json')]
r['metadata_snapshot']={'path':'research/experiments/20261001T053425Z/spot_metadata_snapshot.json','sha256':sha(ROOT/'research/experiments/20261001T053425Z/spot_metadata_snapshot.json')}
r['source_references']=json.loads((ROUND/'spec.json').read_text())['sources'];r['sensitivity']={};r['label_statistics']={}
for asset in ('BTC','ETH'):
 group=[x for x in r['trials'] if asset in x['name']];bycost={}
 for m in ('1','2','3'):
  vals=[x['scenarios'][m] for x in group];adj=[]
  for x in group:
   for y in group:
    xp,yp=x['parameters'],y['parameters'];axis=None
    if xp['buffer_usdt']==yp['buffer_usdt'] and (xp['ridge_alpha'],yp['ridge_alpha']) in ((.1,1),(1,10)):axis='ridge_alpha'
    elif xp['ridge_alpha']==yp['ridge_alpha'] and (xp['buffer_usdt'],yp['buffer_usdt']) in ((0,1),(1,5)):axis='buffer_usdt'
    if axis:
     sx,sy=x['scenarios'][m],y['scenarios'][m];adj.append({'from':x['name'],'to':y['name'],'axis':axis,'net_return_delta_pct':sy['net_return_pct']-sx['net_return_pct'],'sharpe_delta':None if sx['sharpe_annualized'] is None or sy['sharpe_annualized'] is None else sy['sharpe_annualized']-sx['sharpe_annualized']})
  bycost[m]={'configs':len(vals),'positive_return_configs':sum(v['net_return_pct']>0 for v in vals),'positive_sharpe_configs':sum(v['sharpe_annualized'] is not None and v['sharpe_annualized']>0 for v in vals),'return_range_pct':[min(v['net_return_pct'] for v in vals),max(v['net_return_pct'] for v in vals)],'adjacent_differences':adj,'shape':'zero/no-entry region, no positive plateau; Sharpe/Calmar undefined'}
 r['sensitivity'][asset]=bycost
 evidence=json.loads(gzip.decompress((ROOT/r['data'][asset]['derived_evidence_path']).read_bytes()));labels=evidence['continuous_labels'];ys=np.array([x['y_net']*10000 for x in labels]);r['label_statistics'][asset]={'all_development_labels':len(labels),'range_net_usdt_at_NAV10000':[float(ys.min()),float(ys.max())],'positive_fraction':float(np.mean(ys>0)),'mean_execution_cost_usdt':float(np.mean([x['execution_cost_usdt'] for x in labels])),'mean_funding_usdt':float(np.mean([x['funding_usdt'] for x in labels])),'note':'descriptive reused-development labels, not extra strategy evaluation/feature input/OOS selection'}
r['validation_status']={'walk_forward':'completed6chronologicalfolds+train-onlycoverage/preprocessing/model+maturitypurge3dayembargo','sensitivity':'completed all18predeclared alpha/buffer cells; no positive neighborhood','costs':'all60actual scenario evaluations complete; zero executed fills at1/2/3. Fees/spread/slippage/volume impact included in continuous labels/gates but realized paths cash only, so not evidence of tradable capacity or cost robustness','qualification':'0passed,18continuousrejected,2nativeevidencecasesrejected,1scopeassociationrejected'}
r['reproduce_command']='OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python research/experiments/20261001T073555Z/evaluate.py --reproduce'
prev.dump(ROUND/'report.json',r)
fig,axes=plt.subplots(1,2,figsize=(8,4),layout='constrained')
for ax,asset in zip(axes,('BTC','ETH')):
 values=np.zeros((3,3));ax.imshow(values,cmap='RdYlGn',vmin=-1,vmax=1);ax.set_xticks(range(3),[0,1,5]);ax.set_yticks(range(3),[.1,1,10]);ax.set_xlabel('Buffer USDT');ax.set_ylabel('Ridge alpha');ax.set_title(asset+' / 3x costs')
 for y in range(3):
  for x in range(3):ax.text(x,y,'0.00%\n0 trades',ha='center',va='center')
fig.suptitle('M1 continuous carry: all preregistered grid cells retained');fig.savefig(ROUND/'sensitivity_3x.png',dpi=140);plt.close(fig)
print('Completed full provenance and sensitivity;126 canonical after finish; labels',r['label_statistics'])
