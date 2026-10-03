"""Freeze jointly confirmed channel/EMA rules and every concrete parameter configuration."""
import copy,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=ROOT/'research/automation/registry.jsonl';records=registry.read_records(ledger);canonical={registry.fingerprint(v['spec']) for v in records.values()}
assert len(canonical)==773 and all(v.get('result_available') and v['status']!='reserved' for v in records.values())
source=ROOT/'research/experiments/20261002T215033Z';channel_source=ROOT/'research/experiments/20261002T174933Z';base=json.loads((source/'spec.json').read_text());old=json.loads((channel_source/'report.json').read_text())
plan={k:copy.deepcopy(base[k]) for k in ['periods','execution','costs','gates','walk_forward','forward_plan','reference','market_data_reference']}
logic={'entry':'At decision i, enter only when prior completed close C[i-1] strictly exceeds max(C[i-entry-1:i-1]) AND float(C[i-1])>EMA[i-1]*(1+band).The channel reference ends at i-2;no delayed arming memory.',
 'exit':'Set desired cash when C[i-1]<min(C[i-exit-1:i-1]) OR float(C[i-1])<EMA[i-1]*(1-band).Exit takes precedence;otherwise joint entry sets long;all other cases/equality preserve desired.',
 'EMA':'alpha=2/(span+1);E[0]=float(first completed daily close),E[j]=(1-alpha)*E[j-1]+alpha*float(C[j]);Python float,adjust=False from datasetday0;never reset across folds.',
 'state':'OOS183 starts with cash and desired-cash;no pending entry or warmup position;daily decisions only using closes through i-1;no fit/labels/OOS tuning.',
 'sizing':'All affordable independent sleeve cash subject to Decimal28 tick/LOT/filter/participation and next00:01-minute IOC fill assumptions;no leverage,short,stop,scale-in or rebalance.'}
plan.update(round=ROUND.name,trigger_utc='2026-10-02T23:51:03.589Z',actual_first_tool_utc='2026-10-02T23:51:39Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),
 hypothesis='Joint channel breakout AND recursively smoothed trend confirmation may exclude weak breakouts;OR exit may reduce adverse trend exposure but increase whipsaws or miss rebounds.Explicit new causal rule,not separately weighted old signals.Freeze full grid and gates before computing new strategies.Existing same-history components motivated hypothesis,not independent efficacy evidence.',
 grid={'entry_lookback_days':[10,15,20],'exit_lookback_days':30,'EMA_span_days':[50,65,80],'EMA_symmetric_band':.015,'raw_weights':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':{'BTC':1500,'ETH':500},'predeclared_center':[15,65]},
 rules=logic,channel_definition=base['CHANNEL_definition'],EMA_definition=base['EMA_definition'],
 allocation='RawBTC75/ETH25 means initial1500/500USDT out of2000.Separate spot cash/units retained,capital never transferred or rebalanced.No auto-normalisation.Components simulated at actual1500/500 amounts with size-dependent impact;combination=sum corresponding absolute NAVs,no second weighting.',
 sensitivity='Full3x3 channel entry10/15/20 x EMAspan50/65/80,exit30/band1.5pct fixed;allBTC,ETH,combination for bothyears=54concrete definitions reserved first.All162costscenes and six surfaces retained.No OOS parameter selection.',
 new_configs=54,new_component_configs=36,new_combination_configs=18,new_cost_scenes=162,prior_canonical_trials=773,development_history_reused=True,
 interpretation='Both periods have repeatedly been used for development;new rule derived after prior research.Not untouched final test,statistical significance or live profit.Different realised NAV need not be independent samples.',
 cross_period_confirmation='Same full rule/entry/span/exit/band/asset or rawweights must pass each historical period separately.No cross-year reset-return pooling.',
 forward_resume={'source_state':str((source/'forward_state.json').relative_to(ROOT)),'state_sha256':sha(source/'forward_state.json'),'source_report':str((source/'forward_report.json').relative_to(ROOT)),'report_sha256':sha(source/'forward_report.json'),'resume_utc':'2026-10-02T21:40:00Z','cutoff_utc':'2026-10-02T23:40:00Z','new_minutes':120,'cumulative_minutes':1419,'action':'Append closed minutes to original positions/costs before next daily decisionOct3UTC00:01;no reset/new buys/forced liquidation.','new_configs':3,'new_cost_scenes':9,'qualification':'Partial1419minutes/0full days insufficient180day/sixfold;original long-run plan collecting.'})
plan['walk_forward']['fit']='No fit/labels or per-fold tuning;fixed causal joint confirmation/OR-exit rule.180train/3gap/purge0,continuous6x30diagnostic folds.EMAseed earlier than train window;cash/units/desired remain continuous.'
plan['forward_plan']['status_at_freeze']='Collecting original SMA65/1percent;resume215033 cumulative1299minutes.Original frozen hash/end2027Mar31 unchanged;new confirmation rule not applied to observer.'
refs=[]
for y,p in plan['periods'].items():
 candidates=[(ROOT/p['report'],'SMA_or_hold'),(channel_source/'report.json','CHANNEL15_30'),(ROOT/'research/experiments/20261001T234032Z/report.json','EMA65'),(source/'report.json','mixed_center')]
 for rp,kind in candidates:
  report=json.loads(rp.read_text())
  for name,c in report['configs'].items():
   if c.get('year',y)!=y:continue
   keep=(kind=='SMA_or_hold' and (c['role']=='comparator_combination' or (c['role']=='combination' and c['lookback_days']==65 and c['raw_weights']==[.75,.25]))) or (kind=='CHANNEL15_30' and c['role']=='combination' and c['entry_days']==15 and c['exit_days']==30) or (kind=='EMA65' and c['role']=='combination' and c['span_days']==65 and c['band']==.015) or (kind=='mixed_center' and c['direction']=='BTC_CHANNEL_ETH_EMA' and c['CHANNEL_entry_days']==15 and c['EMA_span_days']==65)
   if keep:refs.append({'name':name,'year':y,'kind':kind,'report':str(rp.relative_to(ROOT)),'report_sha256':sha(rp)})
assert len(refs)==10;plan['read_only_comparator_refs']=refs
(ROUND/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
batch=[];fps={}
def save(sp,fields,target):
 fp=registry.fingerprint(sp);assert fp not in canonical
 path=ROUND/'specs'/f'{sp["name"]}.json';path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(sp,indent=2)+'\n')
 run=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(path.relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True);print(sp['name'],run.returncode,run.stdout.strip(),flush=True)
 if run.returncode:raise RuntimeError('STOP before calculation:'+run.stdout+run.stderr)
 row={'name':sp['name'],'fingerprint':fp,'spec':str(path.relative_to(ROOT)),**fields};target.append(row);return fp
for y in plan['periods']:
 for asset in ('BTC','ETH'):
  t=next(c for c in old['configs'].values() if c['year']==y and c.get('asset')==asset and c['entry_days']==15 and c['exit_days']==30)
  for entry in plan['grid']['entry_lookback_days']:
   for span in plan['grid']['EMA_span_days']:
    sp=copy.deepcopy(json.loads((ROOT/t['spec']).read_text()));sp.update(name=f'filtered_{y}_{asset}_e{entry}_s{span}',family='daily-channel-ema-confirmation',logic=logic,validation_plan=str((ROUND/'spec.json').relative_to(ROOT)))
    sp['parameters'].update(entry_lookback_days=entry,exit_lookback_days=30,EMA_span_days=span,EMA_symmetric_band=.015)
    fps[(y,asset,entry,span)]=save(sp,{'year':y,'role':'component','asset':asset,'entry_days':entry,'exit_days':30,'span_days':span,'is_new':True},batch)
 t=next(c for c in old['configs'].values() if c['year']==y and c['role']=='combination' and c['entry_days']==15 and c['exit_days']==30)
 for entry in plan['grid']['entry_lookback_days']:
  for span in plan['grid']['EMA_span_days']:
   sp=copy.deepcopy(json.loads((ROOT/t['spec']).read_text()));sp.update(name=f'filtered_{y}_combo_e{entry}_s{span}_btc0.75',family='channel-ema-confirmation-initial-capital',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['components']=[{'fingerprint':fps[(y,a,entry,span)],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))]
   save(sp,{'year':y,'role':'combination','entry_days':entry,'exit_days':30,'span_days':span,'raw_weights':[.75,.25],'is_new':True},batch)
assert len(batch)==54 and len({b['fingerprint'] for b in batch})==54
(ROUND/'batch.json').write_text(json.dumps(batch,indent=2)+'\n')
forward=[];oldfb=json.loads((source/'forward_batch.json').read_text())
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(b for b in oldfb if b.get('asset')==asset);sp=json.loads((ROOT/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)
b=next(b for b in oldfb if b['name']=='forward_snapshot_combo');sp=json.loads((ROOT/b['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];sp['components']=[{'fingerprint':fps[a],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward)
(ROUND/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n')
print('PASS:54new causal rule configurations and3new cutoff snapshots independently reserved before calculation.')
