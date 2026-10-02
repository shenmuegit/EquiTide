"""Freeze close-only channel breakout and cumulative shadow cutoff before evaluation."""
import copy,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=ROOT/'research/automation/registry.jsonl';records=registry.read_records(ledger);canonical={registry.fingerprint(v['spec']) for v in records.values()}
assert len(canonical)==587 and all(v.get('result_available') and v['status']!='reserved' for v in records.values())
base=json.loads((ROOT/'research/experiments/20261002T134733Z/spec.json').read_text())
plan={k:copy.deepcopy(base[k]) for k in ['walk_forward','execution','costs','gates','periods','forward_plan']}
source=ROOT/'research/experiments/20261002T134733Z'
plan.update(round=ROUND.name,trigger_utc='2026-10-02T15:49:03.346Z',actual_first_tool_utc='2026-10-02T15:49:45Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),
 hypothesis='Close-based range breakout may enter persistent trends and leave downside breaks with different timing than SMA/EMA. Longer entry versus shorter exit may reduce prolonged declining exposure;false breakouts and delayed entry can harm returns. Fix the full two-axis grid before results.',
 grid={'entry_lookback_days':[20,40,60],'exit_lookback_days':[10,20,30],'raw_weight_pair':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':{'BTC':1500,'ETH':500},'predeclared_center':[40,20]},
 rules={'entry':'At daily decision i,use completed prior close C[i-1]. Strictly above max(C[i-entry_lookback_days-1:i-1]) sets desired-long. The entry comparison range contains exactly entry_lookback_days completed closes ending i-2;it EXCLUDES the tested close i-1.',
 'exit':'Prior close C[i-1] strictly below min(C[i-exit_lookback_days-1:i-1]) sets desired-cash. Exit range contains exactly exit_lookback_days closes ending i-2. Equality or neither event preserves desired-state. No shorting,buffer,volatility filter,confirmation,stop or pyramiding.',
 'sizing':base['rules']['sizing'],'portfolio':base['rules']['portfolio']},
 channel_definition='Decimal precision28 using daily CLOSE extrema only,not intraday highs/lows. Integer range widths include exactly L prior closes excluding tested prior close. All window timestamps end by i-2 daily completion;tested close available at UTC00:00 of decision day,trade reference next UTC00:01.',
 signal_initialization='Desired cash at OOS183;warm prior max60+1 closes;state and actual cash/units carry across all six folds.No prefilled position or per-fold reset.',
 sensitivity='Full3x3 entry20/40/60 x exit10/20/30 grid in each year and BTC/ETH/combination.All54 reserve first.All costs/folds/metrics and adjacent descriptive2sd flags retained;no OOS grid updates or gate changes.',
 new_configs=54,new_cost_scenes=162,prior_canonical_trials=587,development_history_reused=True,
 interpretation='Both historical periods repeatedly used for research.Previous trend-grid results motivated new range rules.The per-day indicators are causal,while family/grid selection is retrospective,not pristine final holdout or stable live profit.Multiple tests correlated.',
 cross_period_confirmation='Same full entry/exit ranges and raw allocation must meet fixed gates in EACH separately reported sixfold period.No new cross-year compounded curve.',
 reference={'motivation':{'title':'Simple Technical Trading Rules and the Stochastic Properties of Stock Returns','authors':['William Brock','Josef Lakonishok','Blake LeBaron'],'url':'https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1992.tb04681.x','version':'Journal of Finance47(5),December1992,1731-1764,DOI10.1111/j.1540-6261.1992.tb04681.x','accessed_utc':'2026-10-02','scope':'Publisher abstract considers moving averages and trading range breaks on DJIA1897-1986.It motivates this new close-only long/cash crypto channel hypothesis;not a replication of paper rules,its bootstrap tests,or proof of crypto profitability.'},'market_data_docs':'https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market','accessed_utc':'2026-10-02'},
 read_only_comparator_refs=copy.deepcopy(base['read_only_comparator_refs']),
 forward_resume={'source_state':str((source/'forward_state.json').relative_to(ROOT)),'state_sha256':sha(source/'forward_state.json'),'source_report':str((source/'forward_report.json').relative_to(ROOT)),'report_sha256':sha(source/'forward_report.json'),'resume_utc':'2026-10-02T13:40:00Z','cutoff_utc':'2026-10-02T15:40:00Z','new_minutes':120,'cumulative_minutes':939,'action':'Append closed marks only;preserve original positions,desired,trades and costs.Next daily decisionOct3UTC00:01.','new_configs':3,'new_cost_scenes':9,'qualification':'Partial939minutes insufficient for180days/sixfold;keep frozen long-run plan collecting.'})
plan['walk_forward']['fit']='No fit or labels;fixed completed-close channel breakout.180train/3gap/6x30 chronological diagnostics,purge0.Desired cash startsOOS183;cash/units/state carry,no fold reset.'
plan['forward_plan']['status_at_freeze']='Collecting fromOct2UTC00:01;resume134733 exact per-cost positions.Original symmetricSMA65/1% rule unchanged;do not apply new channel to original observer.'
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
  for entry in plan['grid']['entry_lookback_days']:
   for exit in plan['grid']['exit_lookback_days']:
    sp=copy.deepcopy(json.loads((ROOT/template['spec_path']).read_text()));sp.update(name=f'channel_{y}_{asset}_e{entry}_x{exit}',family='daily-close-range-breakout',logic={k:plan['rules'][k] for k in ('entry','exit','sizing')},validation_plan=str((ROUND/'spec.json').relative_to(ROOT)))
    for key in ('symmetric_band_fraction','lookback_days'):sp['parameters'].pop(key)
    sp['parameters'].update(entry_lookback_days=entry,exit_lookback_days=exit,channel_definition=plan['channel_definition'],signal_initialization=plan['signal_initialization'])
    fps[(y,asset,entry,exit)]=save(sp,{'year':y,'role':'component','asset':asset,'entry_days':entry,'exit_days':exit},batch)
 for entry in plan['grid']['entry_lookback_days']:
  for exit in plan['grid']['exit_lookback_days']:
   template=next(v for v in old['configs'].values() if v['role']=='combination');sp=copy.deepcopy(json.loads((ROOT/template['spec_path']).read_text()));sp.update(name=f'channel_{y}_combo_e{entry}_x{exit}_btc0.75',family='close-channel-initial-capital',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['components']=[{'fingerprint':fps[(y,a,entry,exit)],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))]
   save(sp,{'year':y,'role':'combination','entry_days':entry,'exit_days':exit,'raw_weights':[.75,.25]},batch)
assert len(batch)==54 and len({b['fingerprint'] for b in batch})==54;(ROUND/'batch.json').write_text(json.dumps(batch,indent=2)+'\n')
forward=[];prior=json.loads((source/'forward_batch.json').read_text())
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(b for b in prior if b.get('asset')==asset);sp=json.loads((ROOT/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)
b=next(b for b in prior if b['name']=='forward_snapshot_combo');sp=json.loads((ROOT/b['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];sp['components']=[{'fingerprint':fps[a],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward);(ROUND/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n')
print('PASS:54 close-channel configurations and3 cumulative cutoff snapshots reserved before computation.')
