"""Add frozen provenance, full sensitivity and descriptives before registry finish."""
import gzip,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from long_carry import ROOT,ROUND,module,prev,sha
reg=module('reg0936_complete',ROOT/'research/automation/registry.py');records=reg.read_records(ROOT/'research/automation/registry.jsonl')
for b in json.loads((ROUND/'batch.json').read_text()):assert records[b['fingerprint']]['status']=='reserved','refuse finished-report mutation'
r=json.loads((ROUND/'report.json').read_text());plan=json.loads((ROUND/'spec.json').read_text());r['source_references']=plan['sources'];r['gates']=plan['gates'];r['multiple_trials_note']='126 prior canonical configurations+22 new concrete configurations=148. All18horizon/alpha cells retained; pre-registry historical trialcount unknown. Reused development history; no independent final holdout or selection-adjusted significance.'
r['source_code_sha256']={str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'src/usdt_quant/research.py',ROOT/'src/usdt_quant/backtest.py',ROOT/'src/usdt_quant/strategy.py',ROOT/'research/automation/registry.py',ROOT/'.agents/skills/walk-forward-validation/scripts/walk_forward.py',ROOT/'research/experiments/20261001T033355Z/evaluate.py',ROOT/'research/experiments/20261001T053425Z/carry.py',ROOT/'research/experiments/20261001T053425Z/evaluate.py',ROOT/'research/experiments/20261001T073555Z/ridge.py',ROUND/'long_carry.py',ROUND/'evaluate.py',ROUND/'check_timing.py',ROUND/'check_evidence.py']}
r['data_source_manifests']=[{'path':p,'sha256':sha(ROOT/p)} for p in ('research/experiments/20261001T013355Z/data_manifest.json','research/experiments/20261001T033355Z/binance_data_manifest.json','research/experiments/20261001T053425Z/spot_metadata_manifest.json')];r['metadata_snapshot']={'path':plan['costs']['metadata_snapshot'],'sha256':sha(ROOT/plan['costs']['metadata_snapshot'])};r['sensitivity']={};r['label_statistics']={}
for asset in ('BTC','ETH'):
 group=[x for x in r['trials'] if asset in x['name']];bycost={}
 for m in ('1','2','3'):
  vals=[x['scenarios'][m] for x in group];adj=[]
  for x in group:
   for y in group:
    xp,yp=x['parameters'],y['parameters'];axis=None
    if xp['ridge_alpha']==yp['ridge_alpha'] and (xp['holding_hours'],yp['holding_hours']) in ((168,336),(336,672)):axis='holding_hours'
    elif xp['holding_hours']==yp['holding_hours'] and (xp['ridge_alpha'],yp['ridge_alpha']) in ((.1,1),(1,10)):axis='ridge_alpha'
    if axis:
     sx,sy=x['scenarios'][m],y['scenarios'][m];adj.append({'from':x['name'],'to':y['name'],'axis':axis,'return_delta_pct':sy['net_return_pct']-sx['net_return_pct'],'sharpe_delta':None if sx['sharpe_annualized'] is None or sy['sharpe_annualized'] is None else sy['sharpe_annualized']-sx['sharpe_annualized']})
  bycost[m]={'configs':len(vals),'positive_return_configs':sum(v['net_return_pct']>0 for v in vals),'positive_sharpe_configs':sum(v['sharpe_annualized'] is not None and v['sharpe_annualized']>0 for v in vals),'return_range_pct':[min(v['net_return_pct'] for v in vals),max(v['net_return_pct'] for v in vals)],'adjacent_differences':adj,'shape':'BTC28d marginal basecost profit only at horizon grid edge; zero3xpositive plateau' if asset=='BTC' else 'no positive return cells, no entries'}
 r['sensitivity'][asset]=bycost;labels=json.loads(gzip.decompress((ROOT/r['data'][asset]['derived_evidence_path']).read_bytes()));r['label_statistics'][asset]={}
 for h in ('168','336','672'):
  vals=labels[h];net=np.array([v['y_net']*10000 for v in vals]);r['label_statistics'][asset][h]={'all_development_labels':len(vals),'net_usdt_range_at_NAV10000':[float(net.min()),float(net.max())],'positive_fraction':float(np.mean(net>0)),'mean_execution_cost_usdt':float(np.mean([v['execution_cost_usdt'] for v in vals])),'mean_funding_usdt':float(np.mean([v['funding_usdt'] for v in vals])),'note':'descriptive label distribution only; no additional strategy evaluation or OOS selection'}
r['native_recovery_scope']='New BTC/ETH8h concrete cases use originalnativeM1 and horizon-specific8h labels, preserving firstsignal quantity-known time,180d maturetrain/3dayembargo and originalflat5bp execution. Together with previous24h cases, abbreviated8/24examples now have actual perasset records; native72h no-trade cases are not long-run/volume-impact qualification. Old report/registry scope unchanged.'
r['validation_status']={'walk_forward':'4chronological28dfolds,180d rollingtrain,56dayembargo,mature horizon-specific labels and train-onlymodel/preprocessing complete; no qualified stable candidate','sensitivity':'18independent horizon/alpha configurations complete;3xpositive neighborhood0/9for eachasset','costs':'66actual scenarios:3BTC28d candidates trade once each and lose at2x/3x,15continuous+2native8 no-entry;2separately reservedspotbenchmarks actuallytrade; no zero-path capacity claim','passed_candidates':r['qualified']}
r['cost_note']='Base1x model forecasts held fixed across cost scenarios; actually paid funding/fees/spread/slip/volume impact stressed. Current metadata and1%maintenance are assumptions. Costs are computed for all labels and all executed orders; no-entry paths do not prove tradable execution robustness.'
r['benchmark_note']='25%initialcapital directionalspot and75%cash, same112dayOOS and actualexecutioncosts; distinct fingerprint/date/allocation from earlier benchmarks, no equal-risk claim versusmatchedcarry50%gross'
r['reproduce_command']='OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python research/experiments/20261001T093625Z/evaluate.py --reproduce';prev.dump(ROUND/'report.json',r)
fig,axes=plt.subplots(1,2,figsize=(9,4),layout='constrained')
for ax,asset in zip(axes,('BTC','ETH')):
 group=[x for x in r['trials'] if asset in x['name']];values=np.array([[next(x['scenarios']['3']['net_return_pct'] for x in group if x['parameters']['holding_hours']==h and x['parameters']['ridge_alpha']==a) for a in (.1,1,10)] for h in (168,336,672)]);ax.imshow(values,cmap='RdYlGn',vmin=-.25,vmax=.25);ax.set_xticks(range(3),[.1,1,10]);ax.set_yticks(range(3),[7,14,28]);ax.set_xlabel('Ridge alpha');ax.set_ylabel('Hold days');ax.set_title(asset+' /3x costs')
 for y in range(3):
  for x in range(3):ax.text(x,y,f'{values[y,x]:+.3f}%',ha='center',va='center')
fig.suptitle('Long M1 carry: every preregistered grid cell retained');fig.savefig(ROUND/'sensitivity_3x.png',dpi=140);plt.close(fig)
print('Completed frozen source/data/model provenance and all sensitivity cells; labels',r['label_statistics'])
