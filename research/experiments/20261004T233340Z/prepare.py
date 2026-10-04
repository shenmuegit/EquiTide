"""Freeze allocation/entry grid with real sleeve capitals and read-only exact60/40 results."""
import copy,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=ROOT/'research/automation/registry.jsonl';records=registry.read_records(ledger);canonical={registry.fingerprint(v['spec']) for v in records.values()}
assert len(canonical)==1298 and len(records)==1300 and all(v.get('result_available') and v['status']!='reserved' for v in records.values())
prior=json.loads(gzip.decompress((ROUND/'prior_summary.json.gz').read_bytes()));assert sha(ledger)==prior['ledger_sha256'] and prior['lines']==2695
latest=ROOT/'research/experiments/20261004T213240Z';source=ROOT/'research/experiments/20261003T212439Z'
plan=copy.deepcopy(json.loads((latest/'spec.json').read_text()));old=json.loads((source/'report.json').read_text());oldbatch=json.loads((source/'batch.json').read_text())
plan.update(round=ROUND.name,trigger_utc='2026-10-04T23:33:40.315Z',actual_first_tool_utc='not recorded precisely; registry and computation UTC authoritative',frozen_at_utc=datetime.now(timezone.utc).isoformat(),
 hypothesis='Prior nearby allocations did not repair2026 lastfold concentration. Predeclare wider61.5/67.5/73.5percent initial allocation xentry10/15/20,with67.5existing read-only. Describe performance sensitivity without OOS optimization or independent-evidence claims.',
 grid={'entry_lookback_days':[10,15,20],'exit_lookback_days':30,'EMA_span_days':50,'EMA_symmetric_band':.015,'BTC_initial_weights':[.615,.675,.735],'raw_weight_pairs':[[.615,.385],[.675,.325],[.735,.265]],'capital_usdt':2000,'component_capital_pairs_usdt':[[1230,770],[1350,650],[1470,530]],'predeclared_center':[15,.675],'center_is_read_only_existing_anchor':True},
 allocation='Rawinitialfractions .615/.385,.675/.325,.735/.265 of2000USDT:1230/770,1350/650,1470/530. Independent actual-size sleeves,no normalization,maintained exposure,rebalancing,or transfers. New-sized components resimulate own impact/tick/LOT;sum absoluteNAV once.',
 sensitivity='Two axes entry10/15/20 andBTC61.5/67.5/73.5percent;exit30,EMA50/band1.5percent fixed.36new configurations108scenes plus18old67.5configurations54read-only scenes. Component capital axis means size/rounding/impact sensitivity.',
 reuse_source={'round':source.name,'report':str((source/'report.json').relative_to(ROOT)),'report_sha256':sha(source/'report.json')},
 qualification_scope='Unchanged fixed gates; original67.5ledger/report/spec/archive untouched; expanded neighbourhood descriptive,not independent final holdout.',
 cross_period_confirmation='Same full rule/parameters/asset/capital or rawweights must pass2025and2026 separately;do not pool separately-reset periods.',
 forward_resume={'source_state':str((latest/'forward_state.json').relative_to(ROOT)),'state_sha256':sha(latest/'forward_state.json'),'source_report':str((latest/'forward_report.json').relative_to(ROOT)),'report_sha256':sha(latest/'forward_report.json'),'resume_utc':'2026-10-04T21:10:00Z','cutoff_utc':'2026-10-04T23:10:00Z','new_minutes':120,'cumulative_minutes':4269,'prior_NAV_points':4153,'new_reference_points':0,'total_NAV_points':4273,'action':'Append120closed marks to unchanged originalOct4positions;no daily decision,reference,fills beforeOct5UTC00:01,no resets/rescaling/rebalancing/forced exits.','new_configs':3,'new_cost_scenes':9,'qualification':'Actual4269minute/2complete days partial snapshot is insufficient180days/sixfolds; original long plan collecting.'})
plan['forward_plan']['status_at_freeze']='Original frozenSMA65/1percent75/25 collecting;Oct4decision processed;nextOct5UTC00:01;terminal2027Mar31 unchanged.'
plan['knowledge_sources']=[{'url':'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html','accessed_utc_date':'2026-10-04','scope':'Same EMA recurrence; localpandas2.2.3 independently audited.'},{'url':'https://developers.binance.com/en/docs/binance-spot-api-docs/rest-api/market-data-endpoints','accessed_utc_date':'2026-10-04','scope':'Actual closedminute bars; retained raw responses/URL/hashes.'}]
plan['next_research_basis']='After this broader diagnostic,prioritize predeclared exit-window/rule sensitivity since nearby allocation refinements have not reduced lastfold dependence. Do not choose winner on same OOS and claim independent validation.'
(ROUND/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
batch=[];grid=[];fps={}
def save(sp,fields,target):
 fp=registry.fingerprint(sp);assert fp not in canonical
 path=ROUND/'specs'/f'{sp["name"]}.json';path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(sp,indent=2)+'\n')
 run=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(path.relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True);print(sp['name'],run.returncode,run.stdout.strip(),flush=True)
 if run.returncode:raise RuntimeError('STOP before calculation:'+run.stdout+run.stderr)
 row={'name':sp['name'],'fingerprint':fp,'spec':str(path.relative_to(ROOT)),**fields};target.append(row);return row

def cell(sp,fields):
 fp=registry.fingerprint(sp)
 if fp in canonical:
  assert fields['BTC_weight']==.675
  prev=next(b for b in oldbatch if b['fingerprint']==fp);r=old['configs'][prev['name']]
  assert records[fp]['result_available'] and records[fp]['report_sha256']==sha(source/'report.json')
  b={**prev,**fields,'is_new':False,'source_ref':{'source_round':source.name,'report':plan['reuse_source']['report'],'report_sha256':plan['reuse_source']['report_sha256'],'archive':r['archive'],'archive_sha256':r['archive_sha256'],'spec_sha256':sha(ROOT/prev['spec'])}}
  print('READ_ONLY_EXACT',prev['name'],flush=True)
 else:b=save(sp,{**fields,'is_new':True},batch)
 grid.append(b);return fp
for y in plan['periods']:
 for ia,asset in enumerate(('BTC','ETH')):
  t=next(c for c in old['configs'].values() if c['year']==y and c.get('asset')==asset and c['entry_days']==15 and c['span_days']==50 and c['BTC_weight']==.675)
  for entry in plan['grid']['entry_lookback_days']:
   for weights in plan['grid']['raw_weight_pairs']:
    capital=int(D('2000')*D(str(weights[ia])));sp=copy.deepcopy(json.loads((ROOT/t['spec']).read_text()));sp.update(name=f'filtered_alloc_{y}_{asset}_e{entry}_s50_c{capital}',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters'].update(entry_lookback_days=entry,initial_capital_usdt=capital)
    fps[(y,asset,entry,weights[0])]=cell(sp,{'year':y,'role':'component','asset':asset,'entry_days':entry,'exit_days':30,'span_days':50,'BTC_weight':weights[0],'raw_weights':weights,'capital_usdt':capital})
 t=next(c for c in old['configs'].values() if c['year']==y and c['role']=='combination' and c['entry_days']==15 and c['span_days']==50 and c['BTC_weight']==.675)
 for entry in plan['grid']['entry_lookback_days']:
  for weights in plan['grid']['raw_weight_pairs']:
   sp=copy.deepcopy(json.loads((ROOT/t['spec']).read_text()));sp.update(name=f'filtered_alloc_{y}_combo_e{entry}_s50_btc{weights[0]}',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['components']=[{'fingerprint':fps[(y,a,entry,weights[0])],'weight':w} for a,w in zip(('BTC','ETH'),weights)]
   cell(sp,{'year':y,'role':'combination','entry_days':entry,'exit_days':30,'span_days':50,'BTC_weight':weights[0],'raw_weights':weights,'capital_usdt':2000})
assert len(batch)==36 and len(grid)==54 and sum(not b['is_new'] for b in grid)==18
(ROUND/'batch.json').write_text(json.dumps(batch,indent=2)+'\n');(ROUND/'grid_batch.json').write_text(json.dumps(grid,indent=2)+'\n')
forward=[];oldfb=json.loads((latest/'forward_batch.json').read_text())
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(b for b in oldfb if b.get('asset')==asset);sp=json.loads((ROOT/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)['fingerprint']
b=oldfb[-1];sp=json.loads((ROOT/b['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];sp['components']=[{'fingerprint':fps[a],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward)
(ROUND/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n');print('PASS:36new actual-capital historical and3new cutoff configurations reserved;18existing67.5/32.5 exact definitions read-only.')
