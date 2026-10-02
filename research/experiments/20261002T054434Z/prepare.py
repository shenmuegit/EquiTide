"""Freeze confirmation lookback grid and continuous forward cutoff before computation."""
import copy,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=ROOT/'research/automation/registry.jsonl';records=registry.read_records(ledger);canonical={registry.fingerprint(v['spec']) for v in records.values()}
assert len(canonical)==377 and all(v.get('result_available') and v['status']!='reserved' for v in records.values())
base=json.loads((ROOT/'research/experiments/20261001T213902Z/spec.json').read_text())
plan={k:copy.deepcopy(base[k]) for k in ['walk_forward','execution','costs','gates','periods','forward_plan']}
plan.update(round=ROUND.name,trigger_utc='2026-10-02T05:44:34.477Z',actual_first_tool_utc='2026-10-02T05:45:13Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),
 hypothesis='Require consecutive completed daily confirmations beyond the SMA band to filter transient crossings. Delayed entry can miss gains and delayed exits can increase drawdown; test both risks on complete fixed grid.',
 grid={'lookback_days':[60,65,70],'confirmation_days':[2,3,4],'fixed_symmetric_band_fraction':.01,'raw_weight_pair':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':{'BTC':1500,'ETH':500}},
 rules={'entry':'Prior completed daily close > Decimal mean of prior N completed closes*(1.01) for Q consecutive OOS daily decisions sets desired-long.',
 'exit':'Prior completed daily close < corresponding SMA*(0.99) for Q consecutive OOS daily decisions sets desired-cash. Each counter resets to0 when its strict inequality fails; equality/deadband resets counters but preserves desired holding.',
 'sizing':base['rules']['sizing'],'portfolio':base['rules']['portfolio']},
 signal_initialization='Desired cash and both counters0 at first OOS decision index183; warmup closes determine SMA but do not prefill confirmation counters. Carry counters,desired state,cash,units across sixfolds.',
 sensitivity='Full3x3 SMA lookback x consecutive confirmation count,for each year and BTC/ETH/combination;fixed1%band and75/25. All54 concrete variants reserve first; publish all positive/negative metrics and descriptive adjacent2sd flags; no OOS parameter choice.',
 new_configs=54,new_cost_scenes=162,prior_canonical_trials=377,development_history_reused=True,
 interpretation='Both histories reused and earlier research motivates this rule. Causal decisions do not eliminate retrospective selection/multiple-trial bias; not pristine final holdout,statistical significance,or stable live profit.',
 cross_period_confirmation='Identical rule and raw allocation must pass separately in EACH sixfold period. No unregistered cross-period compounded curve.',
 reference={'implementation':'Original rule defined here; SMA mean uses exact completed daily Decimal closes. No external profitability claim.','market_data_docs':'https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints','accessed_utc':'2026-10-02'},
 forward_resume={'source_state':'research/experiments/20261002T014132Z/forward_state.json','state_sha256':sha(ROOT/'research/experiments/20261002T014132Z/forward_state.json'),'source_report':'research/experiments/20261002T014132Z/forward_report.json','report_sha256':sha(ROOT/'research/experiments/20261002T014132Z/forward_report.json'),'resume_utc':'2026-10-02T01:40:00Z','cutoff_utc':'2026-10-02T05:40:00Z','new_minutes':240,'cumulative_minutes':339,'action':'Mark completed new minutes only. NextdailydecisionOct3UTC00:01;no duplicate buy,no cash reset,all prior costs retained.','new_configs':3,'new_cost_scenes':9,'qualification':'Partial cumulative339minute observation insufficient for180day/sixfold;keep original long-run plan collecting.'})
plan['walk_forward']['fit']='No model or labels;fixed SMA confirmation.180train/3gap/6x30 chronological diagnostics;purge0. Desired state and consecutive counters begin at first OOS183 and carry across folds.'
plan['forward_plan']['status_at_freeze']='Collecting fromOct2UTC00:01;resume prior exact per-cost positions;original rule unchanged'
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
  for n in plan['grid']['lookback_days']:
   for q in plan['grid']['confirmation_days']:
    sp=copy.deepcopy(json.loads((ROOT/template['spec_path']).read_text()));sp.update(name=f'confirm_{y}_{asset}_n{n}_q{q}',family='daily-sma-consecutive-confirmation',logic={k:plan['rules'][k] for k in ('entry','exit','sizing')},validation_plan=str((ROUND/'spec.json').relative_to(ROOT)))
    sp['parameters'].update(lookback_days=n,confirmation_days=q,symmetric_band_fraction=.01,signal_initialization=plan['signal_initialization'])
    fps[(y,asset,n,q)]=save(sp,{'year':y,'role':'component','asset':asset,'lookback_days':n,'confirm_days':q},batch)
 for n in plan['grid']['lookback_days']:
  for q in plan['grid']['confirmation_days']:
   template=next(v for v in old['configs'].values() if v['role']=='combination');sp=copy.deepcopy(json.loads((ROOT/template['spec_path']).read_text()));sp.update(name=f'confirm_{y}_combo_n{n}_q{q}_btc0.75',family='sma-confirmation-initial-capital',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['components']=[{'fingerprint':fps[(y,a,n,q)],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))]
   save(sp,{'year':y,'role':'combination','lookback_days':n,'confirm_days':q,'raw_weights':[.75,.25]},batch)
(ROUND/'batch.json').write_text(json.dumps(batch,indent=2)+'\n');assert len(batch)==54
forward=[];source=ROOT/'research/experiments/20261002T014132Z'
for asset,capital in [('BTC',1500),('ETH',500)]:
 sp=json.loads((source/'specs'/f'forward_{asset}.json').read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc']
 fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)
sp=json.loads((source/'specs/forward_combo.json').read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];sp['components']=[{'fingerprint':fps[a],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))]
save(sp,{'capital_usdt':2000},forward);(ROUND/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n')
print('PASS:54 confirmation configurations and3 continuous forward cutoff configurations reserved before any computation')
