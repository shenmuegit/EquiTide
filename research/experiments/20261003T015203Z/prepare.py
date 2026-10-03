"""Freeze faster exits with exact completed exit30 cells read-only;reserve every new configuration."""
import copy,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=ROOT/'research/automation/registry.jsonl';records=registry.read_records(ledger);canonical={registry.fingerprint(v['spec']) for v in records.values()}
assert len(canonical)==830 and len(records)==832 and all(v.get('result_available') and v['status']!='reserved' for v in records.values())
prior=json.loads(gzip.decompress((ROUND/'prior_summary.json.gz').read_bytes()));assert sha(ledger)==prior['ledger_sha256'] and prior['lines']==1684
source=ROOT/'research/experiments/20261002T235103Z';plan=copy.deepcopy(json.loads((source/'spec.json').read_text()));old=json.loads((source/'report.json').read_text());oldbatch=json.loads((source/'batch.json').read_text())
plan.pop('count_correction',None)
plan.update(round=ROUND.name,trigger_utc='2026-10-03T01:52:03.657Z',actual_first_tool_utc='2026-10-03T01:52:46Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),
 hypothesis='Faster10/20day close-channel exits,with unchanged joint confirmation EMA50/band1.5percent,may limit giveback and final-fold concentration.It can add whipsaws and miss rebounds.Full3x3 entry/exit batch fixed before results;18 exact exit30 definitions reused read-only.',
 grid={'entry_lookback_days':[10,15,20],'exit_lookback_days':[10,20,30],'EMA_span_days':50,'EMA_symmetric_band':.015,'raw_weights':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':{'BTC':1500,'ETH':500},'predeclared_center':[15,20]},
 sensitivity='Six3x3 entry10/15/20 x exit10/20/30 surfaces,EMA50/band1.5percent fixed.36 new exact configurations and108 new cost scenes reserved first;18 exact exit30 configs/54 scenes read-only reuse.No exact historical strategy retest.',
 new_configs=36,new_component_configs=24,new_combination_configs=12,new_cost_scenes=108,reused_grid_configs=18,reused_cost_scenes=54,full_grid_configs=54,prior_canonical_trials=830,
 reuse_source={'round':source.name,'report':str((source/'report.json').relative_to(ROOT)),'report_sha256':sha(source/'report.json')},
 qualification_scope='New definitions use unchanged gates and full9cell entry/exit neighbourhood.Old exit30 cells keep original ledger status/criteria;expanded neighbourhood metrics only descriptive.',
 cross_period_confirmation='Identical entry/exit/EMA/band and asset or raw weights must pass each historical period separately.No pooled cross-year reset returns.',
 knowledge_sources=[{'url':'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html','accessed_utc_date':'2026-10-03','scope':'EMA recurrence;parameter hypothesis ours,no profitability evidence.'},{'url':'https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market','accessed_utc_date':'2026-10-03','scope':'Real completed daily and minute kline interface for delayed original-plan continuation.'}],
 forward_resume={'source_state':str((source/'forward_state.json').relative_to(ROOT)),'state_sha256':sha(source/'forward_state.json'),'source_report':str((source/'forward_report.json').relative_to(ROOT)),'report_sha256':sha(source/'forward_report.json'),'resume_utc':'2026-10-02T23:40:00Z','cutoff_utc':'2026-10-03T01:40:00Z','daily_decision_utc':'2026-10-03T00:01:00Z','new_minutes':120,'cumulative_minutes':1539,'prior_NAV_points':1421,'new_reference_points':1,'total_NAV_points':1542,'action':'Execute unchanged originalSMA65/1percent daily decision from65 completed daily bars at00:01 minute open,retain original per-cost cash/units/desired/trades/costs;append execution reference even if hold plus120 closed-minute marks;no reset or forced terminal sell.','new_configs':3,'new_cost_scenes':9,'qualification':'Partial1539minutes/1full day insufficient180days/sixfold;original long-run plan collecting.'})
plan['forward_plan']['status_at_freeze']='Original frozenSMA65/1percent remains collecting;executeOct3UTC00:01 daily rule without applying new historical channel parameters.TerminalMar31 unchanged.'
(ROUND/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
batch=[];grid=[];fps={}
def save(sp,fields,target):
 fp=registry.fingerprint(sp);assert fp not in canonical
 path=ROUND/'specs'/f'{sp["name"]}.json';path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(sp,indent=2)+'\n')
 run=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(path.relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True)
 print(sp['name'],run.returncode,run.stdout.strip(),flush=True)
 if run.returncode:raise RuntimeError('STOP before calculation:'+run.stdout+run.stderr)
 row={'name':sp['name'],'fingerprint':fp,'spec':str(path.relative_to(ROOT)),**fields};target.append(row);return row

def cell(sp,fields):
 fp=registry.fingerprint(sp)
 if fp in canonical:
  assert fields['exit_days']==30
  prev=next(b for b in oldbatch if b['fingerprint']==fp);r=old['configs'][prev['name']]
  assert records[fp]['result_available'] and records[fp]['report_sha256']==sha(source/'report.json')
  b={**prev,'is_new':False,'source_ref':{'source_round':source.name,'report':plan['reuse_source']['report'],'report_sha256':plan['reuse_source']['report_sha256'],'archive':r['archive'],'archive_sha256':r['archive_sha256'],'spec_sha256':sha(ROOT/prev['spec'])}}
  print('READ_ONLY_EXACT',prev['name'],flush=True)
 else:b=save(sp,{**fields,'is_new':True},batch)
 grid.append(b);return fp
for y in plan['periods']:
 for asset in ('BTC','ETH'):
  t=next(c for c in old['configs'].values() if c['year']==y and c.get('asset')==asset and c['entry_days']==15 and c['span_days']==50)
  for entry in plan['grid']['entry_lookback_days']:
   for exit in plan['grid']['exit_lookback_days']:
    sp=copy.deepcopy(json.loads((ROOT/t['spec']).read_text()));sp.update(name=f'filtered_exit_{y}_{asset}_e{entry}_x{exit}_s50',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)))
    sp['parameters'].update(entry_lookback_days=entry,exit_lookback_days=exit)
    fps[(y,asset,entry,exit)]=cell(sp,{'year':y,'role':'component','asset':asset,'entry_days':entry,'exit_days':exit,'span_days':50})
 t=next(c for c in old['configs'].values() if c['year']==y and c['role']=='combination' and c['entry_days']==15 and c['span_days']==50)
 for entry in plan['grid']['entry_lookback_days']:
  for exit in plan['grid']['exit_lookback_days']:
   sp=copy.deepcopy(json.loads((ROOT/t['spec']).read_text()));sp.update(name=f'filtered_exit_{y}_combo_e{entry}_x{exit}_s50_btc0.75',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['components']=[{'fingerprint':fps[(y,a,entry,exit)],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))]
   cell(sp,{'year':y,'role':'combination','entry_days':entry,'exit_days':exit,'span_days':50,'raw_weights':[.75,.25]})
assert len(batch)==36 and len(grid)==54 and sum(not b['is_new'] for b in grid)==18
(ROUND/'batch.json').write_text(json.dumps(batch,indent=2)+'\n');(ROUND/'grid_batch.json').write_text(json.dumps(grid,indent=2)+'\n')
forward=[];oldfb=json.loads((source/'forward_batch.json').read_text())
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(b for b in oldfb if b.get('asset')==asset);sp=json.loads((ROOT/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)['fingerprint']
b=oldfb[-1];sp=json.loads((ROOT/b['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];sp['components']=[{'fingerprint':fps[a],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward)
(ROUND/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n');print('PASS:36new historical/3new snapshot definitions reserved;18exact historical completed cells read-only.')
