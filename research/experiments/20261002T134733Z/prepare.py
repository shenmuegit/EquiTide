"""Freeze the volatility guard grid and cumulative shadow cutoff before any evaluation."""
import copy,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=ROOT/'research/automation/registry.jsonl';records=registry.read_records(ledger);canonical={registry.fingerprint(v['spec']) for v in records.values()}
assert len(canonical)==530 and all(v.get('result_available') and v['status']!='reserved' for v in records.values())
base=json.loads((ROOT/'research/experiments/20261002T094655Z/spec.json').read_text())
plan={k:copy.deepcopy(base[k]) for k in ['walk_forward','execution','costs','gates','periods','forward_plan']}
source=ROOT/'research/experiments/20261002T114625Z'
plan.update(round=ROUND.name,trigger_utc='2026-10-02T13:47:33.049Z',actual_first_tool_utc='2026-10-02T13:48:25Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),
 hypothesis='A lagged realized-volatility ceiling may avoid turbulent trend exposure and reduce early-fold losses;may also force whipsaw exits and miss high-volatility recoveries.Freeze full entry-buffer x volatility-ceiling grid before results.',
 grid={'entry_band_fraction':[.0125,.015,.02],'annual_volatility_ceiling':[.6,.8,1.0],'exit_band_fraction':.005,'SMA_lookback_days':65,'volatility_lookback_days':20,'raw_weight_pair':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':{'BTC':1500,'ETH':500}},
 rules={'entry':'At decision i,use only prior completed daily closes. If lagged annualized20-return volatility<=annual_volatility_ceiling and priorclose strictly>SMA65*(1+entry_band_fraction),set desired-long.',
 'exit':'If lagged annualized volatility>ceiling,set desired-cash immediately even during an uptrend.Otherwise priorclose strictly<SMA65*(1-exit_band_fraction) sets cash.Equality/deadband preserves desired.When volatility recovers,cash is not automatically restored to long;requires a valid above-entry crossing.No multi-day confirmation.',
 'sizing':base['rules']['sizing'],'portfolio':base['rules']['portfolio']},
 volatility_definition='Decimal precision28;20 returns log(C[t]/C[t-1]) from21 fully completed closes endingi-1.Sample variance=sum((r-mean)^2)/(20-1),annual volatility=sqrt(365*variance).<=cap eligible,>cap cash.Absolute annualizedfraction units,not annualized strategy returns.No current-day data or future realized volatility.',
 signal_initialization='Desired cash at OOS183;prior65closes and21close volatility window warm indicators.Carry desired,cash,units across folds.Guard resets desired to cash;after recovery deadband remains cash.',
 sensitivity='Full3x3 entry-buffer x volatility-ceiling grid for each year and BTC/ETH/combination;exit0.5%,SMA65,vollookback20,75/25 fixed.All54 variants reserve first.All costs/folds/risk metrics and adjacent descriptive2sd flags retained;no OOS retuning.',
 new_configs=54,new_cost_scenes=162,prior_canonical_trials=530,development_history_reused=True,
 interpretation='Both histories repeatedly reused;earlier concentrated gains motivated the volatility guard.Indicator decisions causal,rule/grid selection retrospective.Multiple trials correlated;not pristine final holdout,statistical significance,or stable live profit.',
 cross_period_confirmation='Same full rule/entry-buffer/volatility-ceiling/rawallocation must meet gates in EACH separately reported sixfold period.No unregistered cross-year compounded curve.',
 reference={'motivation':{'title':'Volatility Managed Portfolios','authors':['Alan Moreira','Tyler Muir'],'url':'https://www.nber.org/papers/w22208','version':'NBER WP22208,April2016,revisedJune2016','accessed_utc':'2026-10-02','scope':'Abstract motivates testing less exposure at high lagged volatility.Original paper studies equity factors/currency carry;this binary cash-ceiling crypto rule is our new hypothesis,not a paper replication or evidence of crypto profitability.'},'market_data_docs':'https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market','accessed_utc':'2026-10-02'},
 forward_resume={'source_state':str((source/'forward_state.json').relative_to(ROOT)),'state_sha256':sha(source/'forward_state.json'),'source_report':str((source/'forward_report.json').relative_to(ROOT)),'report_sha256':sha(source/'forward_report.json'),'resume_utc':'2026-10-02T11:40:00Z','cutoff_utc':'2026-10-02T13:40:00Z','new_minutes':120,'cumulative_minutes':819,'action':'Append closed marks only;retain original positions,desired,trades and costs.Next daily decisionOct3UTC00:01.','new_configs':3,'new_cost_scenes':9,'qualification':'Partial819minutes insufficient for180days/sixfold;keep original long-run plan collecting.'})
plan['walk_forward']['fit']='No fit or labels;fixedvolatility-guarded ASMA65.180train/3gap/6x30 chronological diagnostics,purge0.Desiredcash startsOOS183;state and actualcash/units carry.No per-fold reset.'
plan['forward_plan']['status_at_freeze']='Collecting fromOct2UTC00:01;resume114625 exact per-cost positions.Original symmetricSMA65/1% rule unchanged;do not apply new guard to original observer.'
comparators=[]
for y,period in plan['periods'].items():
 old=json.loads((ROOT/period['report']).read_text())
 for name,row in old['configs'].items():
  if row['role']=='comparator_combination' or (row['role']=='combination' and row['lookback_days']==65 and row['raw_weights']==[.75,.25]):comparators.append({'name':name,'year':y,'kind':'hold50/50' if row['role']=='comparator_combination' else 'symmetricSMA65','report':period['report'],'report_sha256':sha(ROOT/period['report'])})
 path=ROOT/'research/experiments/20261002T094655Z/report.json';old=json.loads(path.read_text())
 for name,row in old['configs'].items():
  if row['role']=='combination' and row['year']==y and row['entry_band']==.015 and row['exit_band']==.005:comparators.append({'name':name,'year':y,'kind':'unguardedASMA_center','report':str(path.relative_to(ROOT)),'report_sha256':sha(path)})
assert len(comparators)==6;plan['read_only_comparator_refs']=comparators
(ROUND/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
snap={'ledger_sha256':sha(ledger),'lines':len(ledger.read_text().splitlines()),'canonical':len(canonical),'records':records,'prior_conclusions':{str(p.relative_to(ROOT)):{'sha256':sha(p),'text':p.read_text()} for p in sorted((ROOT/'research/experiments').glob('*/result.md'))},'legacy_results':{str(p.relative_to(ROOT)):json.loads(p.read_text()) for p in (ROOT/'freqtrade_trial/results').glob('walk_forward*.json')},'checks_read':{str(p.relative_to(ROOT)):{'sha256':sha(p),'text':p.read_text()} for p in (ROOT/'checks').glob('*oos.py')}}
with (ROUND/'prior_summary.json.gz').open('wb') as f:
 with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:z.write(json.dumps(snap,ensure_ascii=False,separators=(',',':')).encode())
batch=[];fps={}
def save(sp,fields,target):
 fp=registry.fingerprint(sp);assert fp not in canonical
 path=ROUND/'specs'/f'{sp["name"]}.json';path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(sp,indent=2)+'\n')
 run=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(path)],cwd=ROOT,capture_output=True,text=True);print(sp['name'],run.returncode,run.stdout.strip(),flush=True)
 if run.returncode:raise RuntimeError('STOP before calculation:'+run.stdout+run.stderr)
 target.append({'name':sp['name'],'fingerprint':fp,'spec':str(path.relative_to(ROOT)),**fields});return fp
for y,period in plan['periods'].items():
 old=json.loads((ROOT/period['report']).read_text())
 for asset,capital in plan['grid']['component_capitals_usdt'].items():
  template=next(v for v in old['configs'].values() if v['role']=='component' and v['asset']==asset and v['parameters']['initial_capital_usdt']==capital)
  for entry in plan['grid']['entry_band_fraction']:
   for cap in plan['grid']['annual_volatility_ceiling']:
    sp=copy.deepcopy(json.loads((ROOT/template['spec_path']).read_text()));sp.update(name=f'volguard_{y}_{asset}_e{entry}_v{cap}',family='daily-sma-volatility-ceiling',logic={k:plan['rules'][k] for k in ('entry','exit','sizing')},validation_plan=str((ROUND/'spec.json').relative_to(ROOT)))
    sp['parameters'].pop('symmetric_band_fraction');sp['parameters'].update(lookback_days=65,entry_band_fraction=entry,exit_band_fraction=.005,volatility_lookback_days=20,annual_volatility_ceiling=cap,volatility_definition=plan['volatility_definition'],signal_initialization=plan['signal_initialization'])
    fps[(y,asset,entry,cap)]=save(sp,{'year':y,'role':'component','asset':asset,'lookback_days':65,'entry_band':entry,'volatility_ceiling':cap},batch)
 for entry in plan['grid']['entry_band_fraction']:
  for cap in plan['grid']['annual_volatility_ceiling']:
   template=next(v for v in old['configs'].values() if v['role']=='combination');sp=copy.deepcopy(json.loads((ROOT/template['spec_path']).read_text()));sp.update(name=f'volguard_{y}_combo_e{entry}_v{cap}_btc0.75',family='volatility-guarded-initial-capital',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['components']=[{'fingerprint':fps[(y,a,entry,cap)],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))]
   save(sp,{'year':y,'role':'combination','lookback_days':65,'entry_band':entry,'volatility_ceiling':cap,'raw_weights':[.75,.25]},batch)
assert len(batch)==54 and len({b['fingerprint'] for b in batch})==54;(ROUND/'batch.json').write_text(json.dumps(batch,indent=2)+'\n')
forward=[];prior=json.loads((source/'forward_batch.json').read_text())
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(b for b in prior if b.get('asset')==asset);sp=json.loads((ROOT/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)
b=next(b for b in prior if b['name']=='forward_snapshot_combo');sp=json.loads((ROOT/b['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];sp['components']=[{'fingerprint':fps[a],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward);(ROUND/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n')
print('PASS:54 volatility-guarded configurations and3 cumulative cutoff snapshots reserved before actual computation.')
