"""Independent real-label cash flow, train-only model and complete archive audit."""
import argparse,bisect,gzip,hashlib,json,math
from collections import Counter
from pathlib import Path
import numpy as np
import polars as pl
from ridge import ROOT,ROUND,HOUR,MINUTE,DAY,VERSION,load,ns,FACTORS,module,native_config
reg=module('m1_audit_registry',ROOT/'research/automation/registry.py');parser=argparse.ArgumentParser();parser.add_argument('--finished',action='store_true');args=parser.parse_args()
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
r=json.loads((ROUND/'report.json').read_text());batch=json.loads((ROUND/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');reportsha=sha(ROUND/'report.json')
assert len(batch)==21 and len(r['trials'])==18 and len(r['native_recovery'])==2
for b in batch:
 s=json.loads((ROOT/b['spec']).read_text());assert reg.fingerprint(s)==b['fingerprint'];x=records[b['fingerprint']]
 if args.finished:assert x['status']=='rejected' and x['result_available'] and x['report_sha256']==reportsha
 else:assert x['status']=='reserved'
for p,expected in r['source_code_sha256'].items():assert sha(ROOT/p)==expected,p
assert sha(ROUND/'spec.json')==r['plan_sha256']
for m in r['data_source_manifests']:
 p=ROOT/m['path'];assert sha(p)==m['sha256'];manifest=json.loads(p.read_text())
 for a in manifest.get('archives',[]):assert a['sha256']==a['published_sha256'] and sha(ROOT/a['path'])==a['sha256']
assert sha(ROOT/r['metadata_snapshot']['path'])==r['metadata_snapshot']['sha256']
datasets={};frames={};labels_checked=0;model_fits=0
for asset in ('BTC','ETH'):
 ds=load(asset);datasets[asset]=ds;assert ds['hashes']==r['data'][asset]['hashes'];bytime={x['ts']:x for x in ds['rows']};events=ds['events'];eventtimes=[x['ts'] for x in events]
 p=ROOT/r['data'][asset]['derived_evidence_path'];assert sha(p)==r['data'][asset]['derived_evidence_sha256'];e=json.loads(gzip.decompress(p.read_bytes()))
 features=pl.DataFrame(e['features'],schema={'decision_ts':pl.Int64,'input_max_available_ts':pl.Int64,**{name:pl.Float64 for name in FACTORS}})
 assert features.filter(pl.col('input_max_available_ts')>pl.col('decision_ts')).height==0
 frames[(asset,'continuous')]=features.join(pl.DataFrame(e['continuous_labels']),on='decision_ts',how='left');native=pl.DataFrame(e['native_labels_24h'],infer_schema_length=None);frames[(asset,'native')]=features.join(native,on='decision_ts',how='left')
 # Recompute all continuous label cash flows independently, including real gap
 # funding, next-minute reference prices, volume impact and tick directions.
 for y in e['continuous_labels']:
  t=y['decision_ts'];assert y['entry_ts']==t+MINUTE and y['label_end_ts']==t+24*HOUR+MINUTE
  start,end=bytime[t],bytime[t+24*HOUR];q=y['target_quantity'];assert abs(q-math.floor(2500/float(start['close'])/ds['meta']['common_lot'])*ds['meta']['common_lot'])<1e-9
  cash=fees=friction=0.
  for row,change in ((start,q),(end,-q)):
   for k,field in enumerate(('fill','fill_perp')):
    ref=float(row[field]);ADV,vol=ds['costs'][k][row['ts']//DAY];participation=abs(change)*ref/ADV;impact=.5*vol*math.sqrt(participation);fee=.001 if k==0 else .0005;direction=change if k==0 else -change;tick=ds['meta']['spot_tick' if k==0 else 'perp_tick'];adverse=ref*(1+math.copysign(.0001+.0002+impact,direction));price=(math.ceil(adverse/tick-1e-9) if direction>0 else math.floor(adverse/tick+1e-9))*tick
    commission=abs(change*price)*fee;cash-=direction*price+commission;fees+=commission;friction+=abs(change)*abs(price-ref)+commission;assert participation<=.001
  selected=events[bisect.bisect_right(eventtimes,y['entry_ts']):bisect.bisect_right(eventtimes,y['label_end_ts'])];fund=sum(q*x['mark']*x['rate'] for x in selected);mature=max([y['label_end_ts']]+[x['available'] for x in selected])
  assert mature==y['label_available_ts'];assert abs(fund-y['funding_usdt'])<1e-9 and abs(fees-y['fees_usdt'])<1e-8 and abs(friction-y['execution_cost_usdt'])<1e-8
  assert abs((cash+fund)/10000-y['y_net'])<1e-10;labels_checked+=1
 # Cost tables must only use the previous20complete UTC days, no today's volume.
 for k,name in enumerate(('spot_bars','perp_bars')):
  daily=ds['frames'][name].group_by((pl.col('open_ts')//DAY).alias('day')).agg(pl.col('close').last().alias('close'),pl.col('quote_volume').sum().alias('volume')).sort('day');days=daily['day'].to_list();close=daily['close'].cast(pl.Float64).to_numpy();vol=daily['volume'].cast(pl.Float64).to_numpy()
  for day,(adv,sigma) in ds['costs'][k].items():
   i=days.index(day);assert i>=21
   assert abs(adv-float(vol[i-20:i].mean()))<1e-6*max(1,adv)
   expected=float(np.std(np.diff(np.log(close[i-21:i])),ddof=1));assert abs(sigma-expected)<1e-12
for a in r['models']:
 p=ROOT/a['path'];assert sha(p)==a['sha256'];audits=json.loads(gzip.decompress(p.read_bytes()));frame=frames[(a['asset'],a['role'])]
 times=frame['decision_ts'].to_numpy();ends=frame['label_end_ts'].fill_null(2**63-1).to_numpy();available=frame['label_available_ts'].fill_null(2**63-1).to_numpy();y=frame['y_net'].to_numpy()
 for audit in audits:
  mask=(times>=audit['train_start'])&(times<audit['train_end_exclusive'])&(ends<audit['train_end_exclusive'])&(available<audit['train_end_exclusive'])&np.isfinite(y);indices=np.flatnonzero(mask).tolist();assert indices==audit['training_row_indices'];train=frame.filter(pl.Series(mask))
  digest=hashlib.sha256(json.dumps(train.to_dicts(),sort_keys=True,allow_nan=False).encode()).hexdigest();assert digest==audit['training_data_sha256']
  assert max(ends[mask])==audit['train_max_label_end'] and max(available[mask])==audit['train_max_label_available'];assert audit['train_end_exclusive']+3*DAY==audit['test_start_signal_ns'];assert audit['model_available_ts']==audit['test_start_signal_ns']
  coverage={n:train[n].drop_nulls().len()/train.height for n in FACTORS};assert coverage==audit['factor_coverage'];active=[n for n in FACTORS if coverage[n]>=.98];assert active==audit['active_factors']
  x=train.select(active).to_numpy();median=np.nanmedian(x,axis=0);x=np.where(np.isnan(x),median,x);mean=x.mean(axis=0);scale=x.std(axis=0);scale=np.where(scale==0,1,scale)
  np.testing.assert_allclose(median,audit['imputer_medians'],rtol=1e-10,atol=1e-14);np.testing.assert_allclose(mean,audit['scale_mean'],rtol=1e-10,atol=1e-14);np.testing.assert_allclose(scale,audit['scale_scale'],rtol=1e-10,atol=1e-14)
  z=(x-mean)/scale;target=train['y_net'].to_numpy();coef=np.linalg.solve(z.T@z+audit['alpha']*np.eye(len(active)),z.T@(target-target.mean()));np.testing.assert_allclose(coef,audit['ridge_coefficients'],rtol=1e-8,atol=1e-12);assert abs(target.mean()-audit['ridge_intercept'])<1e-12
  test=frame.filter((pl.col('decision_ts')>=audit['test_start_signal_ns'])&(pl.col('decision_ts')<audit['test_end_signal_ns']));tx=test.select(active).to_numpy();tx=np.where(np.isnan(tx),median,tx);pred=((tx-mean)/scale)@np.array(audit['ridge_coefficients'])+audit['ridge_intercept'];archive=np.array(audit['predictions']);assert np.array_equal(test['decision_ts'].to_numpy(),archive[:,0]);np.testing.assert_allclose(pred,archive[:,1],rtol=1e-12,atol=1e-14);assert np.sum(pred>0)==audit['predicted_positive_hours'];model_fits+=1
curves=nav_points=0
for trial in r['trials']+r['native_recovery']:
 p=ROOT/trial['full_result_path'];assert sha(p)==trial['full_result_sha256'];full=json.loads(gzip.decompress(p.read_bytes()))
 for m,s in full.items():
  curves+=1
  if trial['role']=='native':
   summary=s['summary'];fills=s['full_native_artifacts']['fills'];eq=s['full_native_artifacts']['equity'];assert len(fills)==0 and summary['status']=='no_trade'
   for row in eq:
    total=sum(float(row[k]) for k in ('spot_cash_usdt','spot_base_value_usdt','perp_margin_balance_usdt','perp_unrealized_pnl_usdt'));assert abs(total-float(row['nav_usdt']))<5e-7
   assert abs(float(summary['final_nav_usdt'])-float(summary['reconciled_nav_usdt']))<1e-7
   continue
  eq=np.array(s['equity']);assert len(eq)==4034 and len(eq)==len(s['equity_signal_times'])+1;assert np.array_equal(eq,np.repeat(10000.,len(eq)));assert not s['trades'] and not s['funding_events'];assert s['executions']==0 and s['round_trips']==0;assert s['net_return_pct']==0 and s['sharpe_annualized'] is None and s['calmar'] is None
  assert abs(np.prod([x['end_nav']/x['start_nav'] for x in s['folds']])-eq[-1]/eq[0])<1e-9
  asset=trial['name'].split('_')[1];alpha=trial['parameters']['ridge_alpha'];model=next(x for x in r['models'] if x['role']=='continuous' and x['asset']==asset and x['alpha']==alpha);pred={t:v for f in json.loads(gzip.decompress((ROOT/model['path']).read_bytes())) for t,v in f['predictions']}
  for decision in s['decisions']:
   assert decision['prediction_y_net']==pred[decision['ts']];assert decision['predicted_net_usdt']==pred[decision['ts']]*10000;assert decision['action']=='skip';assert decision['predicted_net_usdt']<=trial['parameters']['buffer_usdt']
  nav_points+=len(eq)-1
for b in r['reused_benchmarks']:
 assert sha(ROOT/b['full_result_path'])==b['full_result_sha256'] and sha(ROOT/b['original_report'])==b['report_sha256'];assert records[b['fingerprint']]['result_available']
if args.finished:
 initial=[json.loads(x)['fingerprint'] for x in (ROOT/'research/automation/registry.jsonl').read_text().splitlines()[:16]];assert all(records[x]['result_available'] for x in initial);assert not any(x['status']=='reserved' for x in records.values());assert len({reg.fingerprint(x['spec']) for x in records.values()})==126
print('PASS:',labels_checked,'independent real24h cost/funding labels;',model_fits,'train-only Ridge fits/coefficients/predictions;',curves,'archived scenarios;',nav_points,'continuous hourly NAV points; raw/normalized/code hashes, lagged ADV, original engine account equality, reused comparator hashes'+('; initial16/16 actual evidence,126canonical,no pending' if args.finished else ''))
