"""Freeze confirmation lookback grid and continuous forward cutoff before computation."""
import copy,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=ROOT/'research/automation/registry.jsonl';records=registry.read_records(ledger);canonical={registry.fingerprint(v['spec']) for v in records.values()}
assert len(canonical)==434 and all(v.get('result_available') and v['status']!='reserved' for v in records.values())
base=json.loads((ROOT/'research/experiments/20261001T213902Z/spec.json').read_text())
plan={k:copy.deepcopy(base[k]) for k in ['walk_forward','execution','costs','gates','periods','forward_plan']}
plan.update(round=ROUND.name,trigger_utc='2026-10-02T09:46:55.242Z',actual_first_tool_utc='2026-10-02T09:48:04Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),
 hypothesis='Use a wider entry buffer and narrower exit buffer around a fixed SMA65 to demand stronger trend evidence before entry and exit earlier when trend weakens. Test missed gains,whipsaw costs,drawdown and fold concentration on the full fixed grid.',
 grid={'entry_band_fraction':[.0125,.015,.02],'exit_band_fraction':[.0025,.005,.0075],'SMA_lookback_days':65,'raw_weight_pair':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':{'BTC':1500,'ETH':500}},
 rules={'entry':'Prior completed daily close strictly > Decimal mean of prior65 completed closes*(1+entry_band_fraction) sets desired-long immediately.',
 'exit':'Prior completed daily close strictly < corresponding SMA65*(1-exit_band_fraction) sets desired-cash immediately. Equality/deadband preserves desired state. No multi-day confirmation counters.',
 'sizing':base['rules']['sizing'],'portfolio':base['rules']['portfolio']},
 signal_initialization='Desired cash at first OOS index183; causal prior65closes warm SMA. Carry desired state,cash,units across six folds;no counter or per-fold reset.',
 sensitivity='Full3x3 entry/exit buffer grid,for each year and BTC/ETH/combination;fixedSMA65 and75/25. All54 concrete variants reserve first; publish all net return/DD/Sharpe/Calmar/fold/cost metrics and descriptive adjacent2sd flags;no OOS parameter choice.',
 new_configs=54,new_cost_scenes=162,prior_canonical_trials=434,development_history_reused=True,
 interpretation='Both histories repeatedly reused;prior results motivated the new rule. Causal decisions do not remove retrospective selection/multiple-trial bias;not pristine final holdout,statistical significance,or stable live profit.',
 cross_period_confirmation='Same rule and raw allocation must independently meet gates in EACH separately reported sixfold period. No unregistered cross-period compounded curve.',
 reference={'implementation':'Original asymmetric rule defined here;SMA mean uses exact completed daily Decimal closes. No external profitability claim.','market_data_docs':'https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market','accessed_utc':'2026-10-02'},
 forward_resume={'source_state':'research/experiments/20261002T054434Z/forward_state.json','state_sha256':sha(ROOT/'research/experiments/20261002T054434Z/forward_state.json'),'source_report':'research/experiments/20261002T054434Z/forward_report.json','report_sha256':sha(ROOT/'research/experiments/20261002T054434Z/forward_report.json'),'resume_utc':'2026-10-02T05:40:00Z','cutoff_utc':'2026-10-02T09:40:00Z','new_minutes':240,'cumulative_minutes':579,'action':'Mark new completed minutes only.Next daily decisionOct3UTC00:01;retain prior per-cost units,cash,desired state,all trades and cumulative costs.','new_configs':3,'new_cost_scenes':9,'qualification':'Partial cumulative579minute snapshot insufficient for180days/sixfold;keep frozen long-run plan collecting.'})
plan['walk_forward']['fit']='No fitting or labels;fixed asymmetricSMA65.180train/3gap/6x30 chronological diagnostics,purge0. Desired cash begins at firstOOS183 and position state carries across folds.'
plan['forward_plan']['status_at_freeze']='Collecting fromOct2UTC00:01;resume previous exact per-cost positions;original SMA65 symmetric1% rule unchanged'
(ROUND/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
snap={'ledger_sha256':sha(ledger),'lines':len(ledger.read_text().splitlines()),'canonical':len(canonical),'records':records,'prior_conclusions':{str(p.relative_to(ROOT)):{'sha256':sha(p),'text':p.read_text()} for p in sorted((ROOT/'research/experiments').glob('*/result.md'))},'legacy_results':{str(p.relative_to(ROOT)):json.loads(p.read_text()) for p in (ROOT/'freqtrade_trial/results').glob('walk_forward*.json')}}
with (ROUND/'prior_summary.json.gz').open('wb') as f:
 with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:z.write(json.dumps(snap,ensure_ascii=False,separators=(',',':')).encode())
batch=[];fps={}
def save(sp,fields,target):
 fp=registry.fingerprint(sp);assert fp not in canonical
 p=ROUND/'specs'/f'{sp["name"]}.json';p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(sp,indent=2)+'\n')
 r=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(p)],cwd=ROOT,capture_output=True,text=True);print(sp['name'],r.returncode,r.stdout.strip(),flush=True)
 if r.returncode:raise RuntimeError('STOP before evaluation:'+r.stdout+r.stderr)
 target.append({'name':sp['name'],'fingerprint':fp,'spec':str(p.relative_to(ROOT)),**fields});return fp
for y,period in plan['periods'].items():
 old=json.loads((ROOT/period['report']).read_text())
 for asset,capital in plan['grid']['component_capitals_usdt'].items():
  template=next(v for v in old['configs'].values() if v['role']=='component' and v['asset']==asset and v['parameters']['initial_capital_usdt']==capital)
  for e in plan['grid']['entry_band_fraction']:
   for x in plan['grid']['exit_band_fraction']:
    sp=copy.deepcopy(json.loads((ROOT/template['spec_path']).read_text()));sp.update(name=f'asym_{y}_{asset}_e{e}_x{x}',family='daily-sma-asymmetric-hysteresis',logic={k:plan['rules'][k] for k in ('entry','exit','sizing')},validation_plan=str((ROUND/'spec.json').relative_to(ROOT)))
    sp['parameters'].pop('symmetric_band_fraction');sp['parameters'].update(lookback_days=65,entry_band_fraction=e,exit_band_fraction=x,signal_initialization=plan['signal_initialization'])
    fps[(y,asset,e,x)]=save(sp,{'year':y,'role':'component','asset':asset,'lookback_days':65,'entry_band':e,'exit_band':x},batch)
 for e in plan['grid']['entry_band_fraction']:
  for x in plan['grid']['exit_band_fraction']:
   template=next(v for v in old['configs'].values() if v['role']=='combination');sp=copy.deepcopy(json.loads((ROOT/template['spec_path']).read_text()));sp.update(name=f'asym_{y}_combo_e{e}_x{x}_btc0.75',family='asymmetric-sma-initial-capital',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['components']=[{'fingerprint':fps[(y,a,e,x)],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))]
   save(sp,{'year':y,'role':'combination','lookback_days':65,'entry_band':e,'exit_band':x,'raw_weights':[.75,.25]},batch)
(ROUND/'batch.json').write_text(json.dumps(batch,indent=2)+'\n');assert len(batch)==54
forward=[];source=ROOT/'research/experiments/20261002T054434Z'
for asset,capital in [('BTC',1500),('ETH',500)]:
 src=json.loads((source/'forward_batch.json').read_text());previous=next(b for b in src if b.get('asset')==asset)
 sp=json.loads((ROOT/previous['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc']
 fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)
previous=next(b for b in src if b['name']=='forward_snapshot_combo');sp=json.loads((ROOT/previous['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];sp['components']=[{'fingerprint':fps[a],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))]
save(sp,{'capital_usdt':2000},forward);(ROUND/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n')
print('PASS:54 asymmetric configurations and3 continuous cutoff configurations reserved before any calculation')
