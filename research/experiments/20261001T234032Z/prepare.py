"""Freeze a complete EMA span/band grid before calculation."""
import copy,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=ROOT/'research/automation/registry.jsonl';records=registry.read_records(ledger)
canonical={registry.fingerprint(r['spec']) for r in records.values()}
assert len(canonical)==284 and all(r.get('result_available') and r['status']!='reserved' for r in records.values())
sources={'2025':'20261001T173606Z','2026':'20261001T133655Z'}
reports={y:json.loads((ROOT/'research/experiments'/s/'report.json').read_text()) for y,s in sources.items()}
base=reports['2026']['plan'];oldmixed=json.loads((ROOT/'research/experiments/20261001T213902Z/spec.json').read_text())
plan={'round':ROUND.name,'trigger_utc':'2026-10-01T23:40:32.160Z','actual_first_tool_utc':'2026-10-01T23:41:12Z','frozen_at_utc':datetime.now(timezone.utc).isoformat(),
 'hypothesis':'A recursive EMA reacts to recent price changes differently from a finite SMA. Predefine slow span and hysteresis bands to test low-turnover trend persistence, including periods of loss, without selecting parameters from either test period.',
 'grid':{'span_days':[50,65,80],'symmetric_band_fraction':[.005,.01,.015],'raw_weight_pair':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':{'BTC':1500,'ETH':500}},
 'new_configs':54,'new_cost_scenes':162,'prior_canonical_trials':284,
 'EMA_definition':'alpha=2/(span+1), E[0]=first dataset completed daily close; E[j]=(1-alpha)*E[j-1]+alpha*C[j] (adjust=False). At decision index i compare only C[i-1] with E[i-1]*(1+/-band); initialise desired state cash at first OOS decision183, preserve in deadband/equality; update recursively from dataset day0 without resets across folds. EMA seed memory extends earlier than rolling train window; no model fit or label.',
 'rules':{'entry':'Prior completed daily close strictly above prior-close EMA*(1+band) enters desired-long; start desired cash at OOS183.', 'exit':'Prior completed daily close strictly below EMA*(1-band) enters desired-cash; equality/deadband preserves desired state.', 'sizing':base['rules']['sizing'],'portfolio':base['rules']['portfolio']},
 'walk_forward':{**base['walk_forward'],'fit':'No fitting or labels; fixed EMA rules, seed dataset firstclose. Rolling180day training split is a chronological diagnostic boundary, not a reset of indicator/position state;3day gap, six contiguous30day tests.'},
 'execution':base['execution'],'costs':base['costs'],'gates':oldmixed['gates'],
 'sensitivity':'Per year, separately BTC,ETH,combination full3x3 span/band grid. All nine variants independently reserved; compute positive return/Sharpe fraction, full metrics and adjacent descriptive2sd differences. No OOS retuning; rawweights fixed75/25.',
 'periods':oldmixed['periods'],'development_history_reused':True,
 'interpretation':'Both periods previously observed and later2026 outcomes influenced exploration. Causal daily signals do not make retrospective parameter selection a pristine final holdout or prospective test. Correlated repeated trials and EMA bootstrap dependence preclude significance/stable live claims.',
 'cross_period_confirmation':'Same asset/role, span/band and rawweights passes both periods only when each separate sixfold meets frozen gates. Do not concatenate curves or multiply returns into an unregistered multi-period strategy.',
 'forward_plan':oldmixed['forward_plan'],
 'reference':{'official_EMA_definition':'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html','accessed_utc':'2026-10-01','formula':'span alpha=2/(span+1),adjust=False recursive first observation seed','historical_exchange_filters':'Frozen October1 metadata; declared uniform historical stress assumption, not historical rules.'}}
plan['forward_plan']['status_at_freeze']='OriginalOctober2UTC00:01 future start;unchanged,no forward outcomes collected'
(ROUND/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
snapshot={'ledger_sha256':sha(ledger),'lines':len(ledger.read_text().splitlines()),'canonical':284,'records':records,'prior_conclusions':{str(p.relative_to(ROOT)):{'sha256':sha(p),'text':p.read_text()} for p in sorted((ROOT/'research/experiments').glob('*/result.md'))}}
with (ROUND/'prior_summary.json.gz').open('wb') as f:
 with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:z.write(json.dumps(snapshot,ensure_ascii=False,separators=(',',':')).encode())
batch=[];fps={}
def save(sp,fields):
 name=sp['name'];fp=registry.fingerprint(sp);assert fp not in canonical
 p=ROUND/'specs'/f'{name}.json';p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(sp,indent=2)+'\n')
 r=subprocess.run(['python3','research/automation/registry.py','reserve',str(p)],cwd=ROOT,capture_output=True,text=True)
 print(name,r.returncode,r.stdout.strip(),flush=True)
 if r.returncode:raise RuntimeError('STOP before evaluation:'+r.stdout+r.stderr)
 batch.append({'name':name,'fingerprint':fp,'spec':str(p.relative_to(ROOT)),**fields});return fp
for y,old in reports.items():
 for asset,capital in plan['grid']['component_capitals_usdt'].items():
  template=next(r for r in old['configs'].values() if r['role']=='component' and r['asset']==asset and r['parameters']['initial_capital_usdt']==capital)
  for span in plan['grid']['span_days']:
   for band in plan['grid']['symmetric_band_fraction']:
    name=f'ema_{y}_{asset}_s{span}_b{band}';sp=copy.deepcopy(json.loads((ROOT/template['spec_path']).read_text()))
    sp.update(name=name,family='daily-ema-hysteresis',logic={k:plan['rules'][k] for k in ('entry','exit','sizing')},validation_plan=str((ROUND/'spec.json').relative_to(ROOT)))
    sp['parameters'].pop('lookback_days');sp['parameters'].update(span_days=span,symmetric_band_fraction=band,EMA_adjust=False,EMA_seed='First completed daily close at source dataset start; preserve recurrence across folds',signal_initial_state='cash at first OOS index183')
    fps[(y,asset,span,band)]=save(sp,{'year':y,'role':'component','asset':asset,'span_days':span,'band':band})
 for span in plan['grid']['span_days']:
  for band in plan['grid']['symmetric_band_fraction']:
   template=next(r for r in old['configs'].values() if r['role']=='combination');sp=copy.deepcopy(json.loads((ROOT/template['spec_path']).read_text()))
   name=f'ema_{y}_combo_s{span}_b{band}_btc0.75';sp.update(name=name,family='daily-ema-hysteresis-initial-capital',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)))
   sp['components']=[{'fingerprint':fps[(y,a,span,band)],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))]
   save(sp,{'year':y,'role':'combination','span_days':span,'band':band,'raw_weights':[.75,.25]})
assert len(batch)==54 and len({b['fingerprint'] for b in batch})==54
(ROUND/'batch.json').write_text(json.dumps(batch,indent=2)+'\n')
print('PASS:all54 EMA component/combination configurations reserved before any signals/backtests.')
