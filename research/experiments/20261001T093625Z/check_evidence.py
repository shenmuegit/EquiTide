"""Independent label funding/cashflow, Ridge algebra, and every actual OOS NAV."""
import argparse,bisect,gzip,hashlib,json,math
from decimal import Decimal,ROUND_CEILING,ROUND_FLOOR
from pathlib import Path
import numpy as np
import polars as pl
from long_carry import ROOT,ROUND,HOUR,MINUTE,DAY,VERSION,load,ns,FACTORS,module,native_config
reg=module('audit0936_registry',ROOT/'research/automation/registry.py');parser=argparse.ArgumentParser();parser.add_argument('--finished',action='store_true');args=parser.parse_args();sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
r=json.loads((ROUND/'report.json').read_text());batch=json.loads((ROUND/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');reportsha=sha(ROUND/'report.json');assert len(batch)==22 and len(r['trials'])==18 and len(r['native_recovery'])==2 and len(r['benchmarks'])==2
for b in batch:
 spec=json.loads((ROOT/b['spec']).read_text());assert reg.fingerprint(spec)==b['fingerprint'];record=records[b['fingerprint']]
 if args.finished:assert record['status']==next((x['qualification'] for x in r['trials'] if x['fingerprint']==b['fingerprint']),'rejected') and record['result_available'] and record['report_sha256']==reportsha
 else:assert record['status']=='reserved'
for p,expected in r['source_code_sha256'].items():assert sha(ROOT/p)==expected,p
assert sha(ROUND/'spec.json')==r['plan_sha256']
for m in r['data_source_manifests']:
 p=ROOT/m['path'];assert sha(p)==m['sha256'];manifest=json.loads(p.read_text())
 for a in manifest.get('archives',[]):assert a['sha256']==a['published_sha256'] and sha(ROOT/a['path'])==a['sha256']
assert sha(ROOT/r['metadata_snapshot']['path'])==r['metadata_snapshot']['sha256']
datasets={};frames={};continuous_checked=native_checked=model_fits=0
for asset in ('BTC','ETH'):
 ds=load(asset);datasets[asset]=ds;assert ds['hashes']==r['data'][asset]['hashes'];bytime={x['ts']:x for x in ds['rows']};events=ds['events'];eventtimes=[x['ts'] for x in events]
 ref=r['data'][asset]['feature_reference'];assert sha(ROOT/ref['path'])==ref['sha256'] and sha(ROOT/ref['original_report'])==ref['original_report_sha256'];old=json.loads(gzip.decompress((ROOT/ref['path']).read_bytes()));features=pl.DataFrame(old['features'],schema={'decision_ts':pl.Int64,'input_max_available_ts':pl.Int64,**{n:pl.Float64 for n in FACTORS}});assert not features.filter(pl.col('input_max_available_ts')>pl.col('decision_ts')).height
 path=ROOT/r['data'][asset]['derived_evidence_path'];assert sha(path)==r['data'][asset]['derived_evidence_sha256'];e=json.loads(gzip.decompress(path.read_bytes()))
 for horizon,labels in e.items():
  frame=pl.DataFrame(labels,infer_schema_length=None);role='native' if horizon=='native8' else 'continuous';h=8 if role=='native' else int(horizon);frames[(asset,role,h)]=features.join(frame,on='decision_ts',how='left')
  for y in labels:
   if y['y_net'] is None:continue
   t=y['decision_ts'];q=float(native_config(ds).target_spot_base) if role=='native' else y['target_quantity']
   entry=t+(HOUR if role=='native' else MINUTE);exit=t+h*HOUR+(0 if role=='native' else MINUTE);assert y['entry_ts']==entry and y['label_end_ts']==exit
   cash=fees=friction=0.
   if role=='continuous':
    assert abs(q-math.floor(2500/float(bytime[t]['close'])/ds['meta']['common_lot'])*ds['meta']['common_lot'])<1e-9
    for row,change in ((bytime[t],q),(bytime[t+h*HOUR],-q)):
     for k,key in enumerate(('fill','fill_perp')):
      price=float(row[key]);adv,vol=ds['costs'][k][row['ts']//DAY];part=abs(change)*price/adv;impact=.5*vol*math.sqrt(part);fee=.001 if k==0 else .0005;direction=change if k==0 else -change;tick=ds['meta']['spot_tick' if k==0 else 'perp_tick'];adverse=price*(1+math.copysign(.0001+.0002+impact,direction));px=(math.ceil(adverse/tick-1e-9) if direction>0 else math.floor(adverse/tick+1e-9))*tick;commission=abs(change*px)*fee;cash-=direction*px+commission;fees+=commission;friction+=abs(change)*abs(px-price)+commission;assert part<=.001
    selected=events[bisect.bisect_right(eventtimes,entry):bisect.bisect_right(eventtimes,exit)];fund=sum(q*x['mark']*x['rate'] for x in selected);mature=max([exit]+[x['available'] for x in selected]);assert abs(fees-y['fees_usdt'])<1e-8 and abs(friction-y['execution_cost_usdt'])<1e-8 and abs(fund-y['funding_usdt'])<1e-9;continuous_checked+=1
   else:
    # Independent original8h native label accounting, Decimal tick and fee precision.
    cashd=Decimal(0);feed=Decimal(0);qty=Decimal(str(q));precision=Decimal('.00000001')
    for row,change in ((bytime[entry],qty),(bytime[exit],-qty)):
     for k,key in enumerate(('close','close_perp')):
      direction=change if k==0 else -change;tick=Decimal(str(ds['meta']['spot_tick' if k==0 else 'perp_tick']));price=Decimal(row[key]);adjusted=price*(Decimal(1)+Decimal('.0005')*(1 if direction>0 else -1));px=(adjusted/tick).to_integral_value(rounding=ROUND_CEILING if direction>0 else ROUND_FLOOR)*tick;fee=Decimal('.001' if k==0 else '.0002');commission=(abs(change*px)*fee).quantize(precision);cashd-=direction*px+commission;feed+=commission
    selected=events[bisect.bisect_right(eventtimes,entry):bisect.bisect_right(eventtimes,exit)];fundd=sum(((qty*Decimal(str(x['mark']))*Decimal(str(x['rate']))).quantize(precision) for x in selected),Decimal(0));fund=float(fundd);cash=float(cashd);mature=max([exit]+[x['available'] for x in selected]);assert abs(float(feed)-y['fees_usdt'])<1e-8;native_checked+=1
   assert mature==y['label_available_ts'];assert abs((cash+fund)/10000-y['y_net'])<1e-10
 # Verify volume/volatility features for every day against strictly past source bars.
 for k,name in enumerate(('spot_bars','perp_bars')):
  daily=ds['frames'][name].group_by((pl.col('open_ts')//DAY).alias('day')).agg(pl.col('close').last().alias('close'),pl.col('quote_volume').sum().alias('volume')).sort('day');days=daily['day'].to_list();close=daily['close'].cast(pl.Float64).to_numpy();volume=daily['volume'].cast(pl.Float64).to_numpy()
  for day,(adv,vol) in ds['costs'][k].items():
   i=days.index(day);assert i>=21;assert abs(adv-float(volume[i-20:i].mean()))<max(1,adv)*1e-6;assert abs(vol-float(np.std(np.diff(np.log(close[i-21:i])),ddof=1)))<1e-12
predictions={}
for model in r['models']:
 path=ROOT/model['path'];assert sha(path)==model['sha256'];audits=json.loads(gzip.decompress(path.read_bytes()));frame=frames[(model['asset'],model['role'],model['holding_hours'])];times=frame['decision_ts'].to_numpy();ends=frame['label_end_ts'].fill_null(2**63-1).to_numpy();available=frame['label_available_ts'].fill_null(2**63-1).to_numpy();ys=frame['y_net'].to_numpy();modelpred={}
 for a in audits:
  range_mask=(times>=a['train_start'])&(times<a['train_end_exclusive']);mask=range_mask&(ends<a['train_end_exclusive'])&(available<a['train_end_exclusive'])&np.isfinite(ys);train=frame.filter(pl.Series(mask));assert np.flatnonzero(mask).tolist()==a['training_row_indices'];digest=hashlib.sha256(json.dumps(train.to_dicts(),sort_keys=True,allow_nan=False).encode()).hexdigest();assert digest==a['training_data_sha256'];assert int(train['label_end_ts'].max())==a['train_max_label_end'] and int(train['label_available_ts'].max())==a['train_max_label_available']
  embargo=(3 if model['role']=='native' else 56)*DAY;assert a['train_end_exclusive']+embargo==a['test_start_signal_ns'];assert a['model_available_ts']==a['test_start_signal_ns'];assert int(np.sum(range_mask&np.isfinite(ys)&((ends>=a['train_end_exclusive'])|(available>=a['train_end_exclusive']))))==a['purged_unmatured'];assert int(np.sum(range_mask&~np.isfinite(ys)))==a['unavailable_label_rows']
  coverage={n:train[n].drop_nulls().len()/train.height for n in FACTORS};assert coverage==a['factor_coverage'];active=[n for n in FACTORS if coverage[n]>=.98];assert active==a['active_factors'];x=train.select(active).to_numpy();median=np.nanmedian(x,axis=0);x=np.where(np.isnan(x),median,x);mean=x.mean(axis=0);scale=x.std(axis=0);scale=np.where(scale==0,1,scale);np.testing.assert_allclose(median,a['imputer_medians'],rtol=1e-10,atol=1e-14);np.testing.assert_allclose(mean,a['scale_mean'],rtol=1e-10,atol=1e-14);np.testing.assert_allclose(scale,a['scale_scale'],rtol=1e-10,atol=1e-14)
  z=(x-mean)/scale;y=train['y_net'].to_numpy();coef=np.linalg.solve(z.T@z+a['alpha']*np.eye(len(active)),z.T@(y-y.mean()));np.testing.assert_allclose(coef,a['ridge_coefficients'],rtol=1e-8,atol=1e-12);assert abs(y.mean()-a['ridge_intercept'])<1e-12;test=frame.filter((pl.col('decision_ts')>=a['test_start_signal_ns'])&(pl.col('decision_ts')<a['test_end_signal_ns']));tx=test.select(active).to_numpy();tx=np.where(np.isnan(tx),median,tx);predict=((tx-mean)/scale)@np.array(a['ridge_coefficients'])+a['ridge_intercept'];archive=np.array(a['predictions']);assert np.array_equal(test['decision_ts'].to_numpy(),archive[:,0]);np.testing.assert_allclose(predict,archive[:,1],rtol=1e-12,atol=1e-14);modelpred.update(a['predictions']);model_fits+=1
 predictions[(model['asset'],model['role'],model['holding_hours'],model['alpha'])]=modelpred
curves=nav_points=funding_checked=0
for trial in r['trials']+r['native_recovery']+r['benchmarks']:
 path=ROOT/trial['full_result_path'];assert sha(path)==trial['full_result_sha256'];full=json.loads(gzip.decompress(path.read_bytes()));asset=trial['name'].split('_')[-1] if trial['role']!='candidate' else trial['name'].split('_')[1];ds=datasets[asset];bytime={x['ts']:x for x in ds['rows']}
 for m,s in full.items():
  curves+=1
  if trial['role']=='native':
   summary=s['summary'];fills=s['full_native_artifacts']['fills'];funds=s['full_native_artifacts']['funding'];equity=s['full_native_artifacts']['equity'];assert len(fills) in (0,4)
   for row in equity:assert abs(sum(float(row[k]) for k in ('spot_cash_usdt','spot_base_value_usdt','perp_margin_balance_usdt','perp_unrealized_pnl_usdt'))-float(row['nav_usdt']))<5e-7
   assert abs(float(summary['final_nav_usdt'])-float(summary['reconciled_nav_usdt']))<1e-7;assert abs(sum(float(x['commission']) for x in fills)-float(summary['fees_usdt']))<1e-7
   actual={x['ts']:x for x in s['actual_source_funding']}
   for event in funds:
    source=actual[event['settlement_ts']];rate=source['rate']*(int(m) if source['rate']<0 else 1);assert abs(float(event['realized_rate'])-rate)<1e-15;assert abs(float(event['native_amount_usdt'])+float(event['signed_contracts'])*float(event['contract_multiplier'])*source['mark']*rate)<1e-7
   continue
  eq=np.array(s['equity']);assert len(eq)==2690 and len(eq)==len(s['equity_signal_times'])+1;assert abs((eq[-1]/10000-1)*100-s['net_return_pct'])<1e-9;assert abs((1-eq/np.maximum.accumulate(eq)).max()*100-s['max_drawdown_pct'])<1e-9;assert abs(np.prod([f['end_nav']/f['start_nav'] for f in s['folds']])-eq[-1]/10000)<1e-9;assert abs(sum(x['cost_usdt'] for x in s['trades'])-s['execution_cost_usdt'])<1e-7
  events=[(x['ts'],1,'trade',x) for x in s['trades']]+[(x['ts'],0,'funding',x) for x in s.get('funding_events',[])];events.sort(key=lambda x:(x[0],x[1]));cash=10000.;spotq=perpq=0.;idx=0;spot_cash=5000.;perp_cash=5000.;entry_perp=0.;decision_bytime={x['ts']:x for x in s.get('decisions',[])}
  def process(cutoff):
   global cash,spotq,perpq,idx,spot_cash,perp_cash,entry_perp,funding_checked
   while idx<len(events) and events[idx][0]<=cutoff:
    _,_,kind,x=events[idx]
    if kind=='funding':
     source=next(v for v in ds['events'] if v['ts']==x['ts']);assert x['rate']==source['rate'] and x['mark']==source['mark'] and x['available']==source['available'];assert abs(-perpq-x['quantity'])<1e-8;raw=-perpq*x['mark']*x['rate'];expected=raw if raw>=0 else raw*int(m);assert abs(raw-x['base_amount_usdt'])<1e-8 and abs(expected-x['amount_usdt'])<1e-8;cash+=x['amount_usdt'];perp_cash+=x['amount_usdt'];funding_checked+=1
    else:
     if trial['role']=='benchmark':change=x['quantity'];leg='spot'
     else:change=x['quantity']*(1 if x['side']=='buy' else -1);leg=x['leg']
     reference=float(bytime[x['ts']-MINUTE]['fill' if leg=='spot' else 'fill_perp']);assert x['reference']==reference;adv,vol=ds['costs'][0 if leg=='spot' else 1][(x['ts']-MINUTE)//DAY];part=abs(change)*reference/adv;impact=.5*vol*math.sqrt(part);basefee=.001 if leg=='spot' else .0005;tick=ds['meta']['spot_tick' if leg=='spot' else 'perp_tick'];px=reference*(1+math.copysign((.0001+.0002+impact)*int(m),change));px=(math.ceil(px/tick-1e-9) if change>0 else math.floor(px/tick+1e-9))*tick;fee=abs(change*px)*basefee*int(m);assert abs(px-x['execution'])<1e-8 and abs(fee-x['fee_usdt'])<1e-8;assert abs(abs(change)*abs(px-reference)+fee-x['cost_usdt'])<1e-8
     cash-=change*x['execution']+x['fee_usdt']
     if leg=='spot':spotq+=change;spot_cash-=change*x['execution']+x['fee_usdt']
     else:
      perp_cash-=x['fee_usdt']
      if change<0:entry_perp=x['execution']
      else:perp_cash+=(-perpq)*(entry_perp-x['execution']);entry_perp=0.
      perpq+=change
     assert x['participation']<=.001
    idx+=1
  for j,t in enumerate(s['equity_signal_times']):
   row=bytime[t];process(t);known=cash+spotq*float(row['close'])+perpq*float(row['close_perp'])
   if t in decision_bytime:
    x=decision_bytime[t];prediction=predictions[(asset,'continuous',trial['parameters']['holding_hours'],trial['parameters']['ridge_alpha'])][t];assert x['prediction_y_net']==prediction;assert abs(x['predicted_net_usdt']-prediction*known)<1e-8;assert abs(x['target_quantity']-math.floor(.25*known/float(row['close'])/ds['meta']['common_lot'])*ds['meta']['common_lot'])<1e-9
    if x['action']=='enter':assert x['predicted_net_usdt']>1 and any(a['ts']==t+MINUTE and a['reason']=='entry' for a in s['trades'])
    elif x['action']=='skip':assert x['predicted_net_usdt']<=1
   process(t+MINUTE);value=cash+spotq*float(row['fill'])+perpq*float(row['fill_perp']);assert abs(value-eq[j+1])<1e-6,(trial['name'],m,j,value,eq[j+1]);nav_points+=1
   if trial['role']=='candidate':
    assert spot_cash>=-.00001
    if perpq<0:high=float(ds['marks'][t]['high']);assert perp_cash+(-perpq)*(entry_perp-high)>.01*(-perpq)*high
  assert abs(spotq)<1e-8 and abs(perpq)<1e-8
  if trial['role']=='candidate':assert s['round_trips']*4==s['executions'] and not s['cash_margin_violations']
if args.finished:
 initial=[json.loads(x)['fingerprint'] for x in (ROOT/'research/automation/registry.jsonl').read_text().splitlines()[:16]];assert all(records[x]['result_available'] for x in initial);assert not any(x['status']=='reserved' for x in records.values());assert len({reg.fingerprint(x['spec']) for x in records.values()})==148
print('PASS:',continuous_checked,'long real labels,',native_checked,'native8 true labels;',model_fits,'training-only Ridge fits;',curves,'actual scenarios;',nav_points,'independent hourly NAV points;',funding_checked,'actual carried funding settlements;56dayembargo, signs/costs/folds/maturity/hash/cash-margin checks'+(';148canonical,no pending,initial16/16actualevidence' if args.finished else ''))
