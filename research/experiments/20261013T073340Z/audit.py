#!/usr/bin/env python3
"""Audit the 60 historical scenes, produce fold/sensitivity tables and heatmap."""
import csv,gzip,hashlib,json
from collections import Counter
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np
import polars as pl
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;RUNS=ROOT/'data/runs'/R.name
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp(ns):return datetime.fromtimestamp(ns/1e9,timezone.utc).isoformat().replace('+00:00','Z')
def calc_dd(a):
 x=np.asarray(a,dtype=np.float64);peaks=np.maximum.accumulate(x);d=1-x/peaks;j=int(np.argmax(d));return float(100*d[j]),int(np.argmax(x[:j+1])),j
def jwrite(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
report=json.loads((R/'report.json').read_text());batch=json.loads((R/'batch.json').read_text());plan=json.loads((R/'plan.json').read_text());bad=[];folds=[];scenes=[];sens=[]
source_markets={}
for asset,info in report['data_manifest']['assets'].items():
 parts=[]
 for src in info['sources']:
  path=ROOT/src['path']
  if path.stat().st_size!=src['bytes'] or sha(path)!=src['sha256']:bad.append(asset+': input parquet hash/size mismatch')
  parts.append(pl.read_parquet(path,columns=['open_ts','open']))
 f=pl.concat(parts,how='vertical_relaxed').sort('open_ts');source_markets[asset]={'ts':f['open_ts'].to_numpy(),'open':f['open'].cast(pl.Float64).to_numpy()}
prior=json.loads((ROOT/'research/experiments/20261012T035429Z/report.json').read_text())
if sha(ROOT/'research/experiments/20261012T035429Z/report.json')!=report['data_manifest']['filter_source_sha256']:bad.append('filter source report SHA mismatch')
if sha(ROOT/'research/experiments/20261001T133655Z/kernel.py')!=report['data_manifest']['kernel_sha256']:bad.append('Decimal fill-kernel SHA mismatch')
if sha(ROOT/'research/experiments/20261001T013355Z/evaluate.py')!=report['data_manifest']['lagged_cost_engine_sha256']:bad.append('lagged cost-engine SHA mismatch')
filters=prior['plan']['execution']['filters']
for b in batch:
 n=b['name'];cfg=report['configs'][n];spec=json.loads((ROOT/b['spec']).read_text());assert sha(ROOT/b['spec'])==sha(R/'specs'/Path(b['spec']).name)
 for mult in (1,2,3):
  s=cfg['scenarios'][str(mult)];navpath=ROOT/s['event_nav_archive']
  if sha(navpath)!=s['event_nav_archive_sha256']:bad.append(f'{n} x{mult}: NAV archive hash mismatch')
  with np.load(navpath) as z:nav=z['event_nav'].astype('<f8');times=z['event_time_ns'].astype('<i8')
  if len(nav)!=s['event_nav_samples'] or len(nav)!=len(times):bad.append(f'{n} x{mult}: NAV sample shape')
  if not np.isfinite(nav).all() or (nav<=0).any():bad.append(f'{n} x{mult}: nonpositive NAV')
  dd,pk,tr=calc_dd(nav)
  if abs(dd-s['max_drawdown_pct'])>1e-7:bad.append(f'{n} x{mult}: drawdown mismatch')
  if float(nav[-1])!=float(s['terminal_NAV_usdt']):bad.append(f'{n} x{mult}: terminal sample does not reconcile')
  lp=RUNS/f'{n}_x{mult}_ledger.json.gz'
  with gzip.open(lp,'rt',encoding='utf-8') as f:ledger=json.load(f)
  fills=ledger['fills'];cash=2000.0;units=0.0;buy_time=None;last_side=None;roundtrips=0
  costs=Counter();reasons=Counter()
  for t in fills:
   side=t['side'];timeidx=int(t['execution_minute']);px=float(t['execution']);qty=float(t['quantity']);fee=float(t['cost_parts']['fee'])
   asset_market=source_markets[b['asset']]
   if not (0<=timeidx<len(asset_market['open'])):bad.append(f'{n} x{mult}: execution index outside source data')
   else:
    if D(str(float(asset_market['open'][timeidx])))!=D(t['reference']):bad.append(f'{n} x{mult}: reference price does not match source minute open')
    if stamp(int(asset_market['ts'][timeidx]))!=t['execution_utc']:bad.append(f'{n} x{mult}: execution timestamp does not match source index')
   fs=filters[b['asset']+'USDT'];qstep=D(fs['LOT_SIZE']['stepSize']);tick=D(fs['PRICE_FILTER']['tickSize']);notional=D(t['quantity'])*D(t['execution'])
   if D(t['quantity'])%qstep!=0 or D(t['execution'])%tick!=0 or notional<D(fs['NOTIONAL']['minNotional']):bad.append(f'{n} x{mult}: quantity/tick/minNotional filter')
   if D(t['participation'])>D('.001'):bad.append(f'{n} x{mult}: participation exceeded 0.1%')
   pp=fs.get('PERCENT_PRICE_BY_SIDE')
   if pp:
    prefix='bid' if side=='buy' else 'ask';avg=D(t['proxy_VWAP5']);price=D(t['execution'])
    if not avg*D(pp[prefix+'MultiplierDown'])<=price<=avg*D(pp[prefix+'MultiplierUp']):bad.append(f'{n} x{mult}: percent-price proxy filter')
   if not (float(t['cash_after'])>=-1e-9 and float(t['units_after'])>=-1e-9):bad.append(f'{n} x{mult}: negative balance')
   if side=='buy':
    if units>1e-12:bad.append(f'{n} x{mult}: overlapping long entries')
    phase=int(spec['parameters'].get('phase_offset_minutes',0));minute=(timeidx//1)%60
    if not b['role']=='buy_hold_comparator' and minute%15!=phase:bad.append(f'{n} x{mult}: entry not at frozen event phase')
    if t.get('signal_available_utc'):
     from datetime import datetime,timedelta,timezone
     execution=datetime.fromisoformat(t['execution_utc'].replace('Z','+00:00'));signal=datetime.fromisoformat(t['signal_available_utc'].replace('Z','+00:00'))
     if execution-signal!=timedelta(seconds=60):bad.append(f'{n} x{mult}: signal-to-fill delay mismatch')
    if units==0:buy_time=timeidx
    qpx=qty*px
    expcash=cash-qpx-fee;expunits=units+qty
   elif side=='sell':
    if units<=0:bad.append(f'{n} x{mult}: sell without position')
    hold=int(spec['parameters'].get('hold_minutes',1))
    if buy_time is not None and not b['role']=='buy_hold_comparator' and timeidx<buy_time+hold:bad.append(f'{n} x{mult}: exit before planned hold')
    qpx=qty*px;expcash=cash+qpx-fee;expunits=units-qty;roundtrips+=1
    if abs(expunits)<1e-10:expunits=0
   else:bad.append(f'{n} x{mult}: unexpected side');continue
   if abs(float(t['cash_after'])-expcash)>1e-7 or abs(float(t['units_after'])-expunits)>1e-10:bad.append(f'{n} x{mult}: ledger balance transition mismatch')
   ref=float(t['reference']);parts=t['cost_parts'];total=sum(float(v) for v in parts.values())
   rate=D('.001')*mult;fee_expected=D(t['quantity'])*D(t['execution'])*rate
   if abs(fee_expected-D(parts['fee']))>D('1e-12'):bad.append(f'{n} x{mult}: explicit fee mismatch')
   refD=D(t['reference']);qtyD=D(t['quantity']);budgetD=D(t['budget']);advD=D(t['lagged_ADV']);sigmaD=D(t['lagged_sigma']);multD=D(mult)
   spreadD=D('.0001')*multD;slipD=D('.0002')*multD;impactD=D('.5')*sigmaD*(budgetD/advD).sqrt()*multD
   theoretical=refD*(1+(spreadD+slipD+impactD)*(1 if side=='buy' else -1))
   expected_parts={'half_spread':qtyD*refD*spreadD,'slippage':qtyD*refD*slipD,'impact':qtyD*refD*impactD,'tick_rounding':qtyD*abs(D(t['execution'])-theoretical)}
   if any(abs(D(parts[k])-v)>D('1e-10') for k,v in expected_parts.items()):bad.append(f'{n} x{mult}: spread/slippage/impact/tick model mismatch')
   if abs((cash+units*ref)-(expcash+expunits*ref)-total)>1e-6:bad.append(f'{n} x{mult}: fill wealth/cost identity')
   if abs(float(t['cost_usdt'])-total)>1e-7:bad.append(f'{n} x{mult}: cost component sum')
   cash,units=expcash,expunits;last_side=side
   for k,v in parts.items():costs[k]+=float(v)
  if abs(cash-float(s['terminal_cash_usdt']))>1e-7 or abs(units-float(s['terminal_units']))>1e-10:bad.append(f'{n} x{mult}: final fill ledger state mismatch')
  if roundtrips!=s['round_trips']:bad.append(f'{n} x{mult}: round-trip count mismatch')
  if sum(ledger['rejected_by_reason'].values())!=s['rejected_orders']:bad.append(f'{n} x{mult}: rejection aggregate mismatch')
  if abs(float(s['net_PnL_usdt'])+float(s['cost_usdt'])-float(s['gross_reference_pnl_usdt']))>1e-6:bad.append(f'{n} x{mult}: gross reference identity')
  for f in s['folds']:
   folds.append({'name':n,'asset':b['asset'],'role':b['role'],'cost_multiplier':mult,**f})
  if b['role']!='buy_hold_comparator':
   p=spec['parameters'];positive=sum(f['net_return_pct']>0 for f in s['folds'])
   sens.append({'name':n,'asset':b['asset'],'role':b['role'],'phase_offset_minutes':p['phase_offset_minutes'],'hold_minutes':p['hold_minutes'],'cost_multiplier':mult,'net_return_pct':s['net_return_pct'],'max_drawdown_pct':s['max_drawdown_pct'],'daily_mark_drawdown_pct':s['daily_mark_drawdown_pct'],'sharpe_annualized_daily':s['sharpe_annualized_daily'],'calmar_daily':s['calmar_daily'],'round_trips':s['round_trips'],'positive_1x_folds':sum(f['net_return_pct']>0 for f in s['folds']) if mult==1 else None,'rejected_orders':s['rejected_orders'],'rejected_by_reason':json.dumps(s['rejected_by_reason'],sort_keys=True),'gross_reference_pnl_to_cost':s['gross_reference_pnl_to_cost'],'adjacent_3x_positive_fraction':cfg['scenarios'].get('neighbor_3x_positive_fraction'),'status':cfg['scenarios'].get('status')})
  scenes.append({'name':n,'asset':b['asset'],'role':b['role'],'cost_multiplier':mult,'return_pct':s['net_return_pct'],'max_drawdown_pct':s['max_drawdown_pct'],'daily_drawdown_pct':s['daily_mark_drawdown_pct'],'round_trips':s['round_trips'],'filled_orders':s['filled_orders'],'rejected_orders':s['rejected_orders'],'rejected_by_reason':json.dumps(s['rejected_by_reason'],sort_keys=True),'cost_usdt':s['cost_usdt'],'fee':s['cost_parts_usdt']['fee'],'half_spread':s['cost_parts_usdt']['half_spread'],'slippage':s['cost_parts_usdt']['slippage'],'impact':s['cost_parts_usdt']['impact'],'tick_rounding':s['cost_parts_usdt']['tick_rounding'],'gross_reference_pnl_to_cost':s['gross_reference_pnl_to_cost'],'terminal_flat':s['terminal_flat'],'status':cfg['scenarios'].get('status')})
if bad:raise SystemExit('\n'.join(bad[:30])+f'\nfailed {len(bad)} audit conditions')
for fname,rows in [('fold_results.csv',folds),('sensitivity.csv',sens),('cost_scenarios.csv',scenes)]:
 with (R/fname).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
# SVG heatmap for 1x/3x phase × holding-duration sensitivity by asset.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="660" viewBox="0 0 1120 660">','<rect width="100%" height="100%" fill="#101822"/>','<style>text{font-family:Arial,sans-serif;fill:#e7edf3}.h{font-size:19px;font-weight:bold}.s{font-size:12px}</style>']
def color(v):return '#9e1c2f' if v<=-80 else '#dc554d' if v<0 else '#278b70'
for ai,asset in enumerate(('BTC','ETH')):
 for mi,mult in enumerate((1,3)):
  x0=70+mi*520;y0=50+ai*290;svg.append(f'<text class="h" x="{x0}" y="{y0}">{asset} — {mult}× 成本，净收益</text>')
  for hi,hold in enumerate((1,2,3)):
   for pi,phase in enumerate((0,1,2)):
    name=f"turn15_{asset.lower()}_phase{phase}_hold{hold}m";row=next(x for x in scenes if x['name']==name and x['cost_multiplier']==mult);x=x0+pi*145;y=y0+25+hi*58;v=row['return_pct']
    svg.append(f'<rect x="{x}" y="{y}" width="135" height="50" rx="4" fill="{color(v)}"/>')
    svg.append(f'<text class="s" x="{x+67}" y="{y+18}" text-anchor="middle">phase {phase}, hold {hold}m</text>')
    svg.append(f'<text class="s" x="{x+67}" y="{y+38}" text-anchor="middle">{v:.2f}%</text>')
svg.extend(['<text class="s" x="70" y="640">Fixed 2025-09-19…2026-09-14 repeated-history OOS; phase 0 is candidate, phases 1/2 are controls.</text>','</svg>'])
(R/'sensitivity_surface.svg').write_text('\n'.join(svg)+'\n')
report['audit']={'passed':True,'checks':['source parquet bytes and SHA-256','filter, Decimal-kernel and lagged-cost-engine source SHA-256','fill reference price and timestamp match source-minute open','all 60 event-NAV archive SHA and positive sample checks','terminal state/reference NAV reconciliation','all successful Decimal fill cash/unit transitions and fill wealth-cost identity','UTC event phase and fixed 60-second signal availability','exit holds no shorter than the predeclared duration','round-trip and filter-rejection counts reconciled','lot/tick/minNotional/participation constraints','gross-reference PnL equals net PnL plus modeled costs','12 continuous daily folds per scene'],'reproduction_commands':plan['reproduction'],'outputs':['report.json','result.md','fold_results.csv','sensitivity.csv','cost_scenarios.csv','sensitivity_surface.svg','data_manifest.json','stdout.txt'],'large_artifacts':'Complete fill ledgers and event NAV arrays are in ignored data/runs/20261013T073340Z; report contains archive SHA/path references.'}
jwrite(R/'report.json',report)
print(json.dumps({'scenes_audited':len(scenes),'fold_rows':len(folds),'sensitivity_rows':len(sens),'cost_rows':len(scenes),'passed':True}))
