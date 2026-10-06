"""Freeze allocation/entry grid with real sleeve capitals and read-only exact exit30 results."""
import copy,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=ROOT/'research/automation/registry.jsonl';records=registry.read_records(ledger);canonical={registry.fingerprint(v['spec']) for v in records.values()}
assert len(canonical)==1883 and len(records)==1885 and all(v.get('result_available') and v['status']!='reserved' for v in records.values())
prior=json.loads(gzip.decompress((ROUND/'prior_summary.json.gz').read_bytes()));assert sha(ledger)==prior['ledger_sha256'] and prior['lines']==3865
latest=ROOT/'research/experiments/20261006T054259Z';source=ROOT/'research/experiments/20261005T113611Z'
plan=copy.deepcopy(json.loads((latest/'spec.json').read_text()));old=json.loads((source/'report.json').read_text());oldbatch=json.loads((source/'batch.json').read_text())
plan.update(round=ROUND.name,trigger_utc='2026-10-06T11:45:30.186Z',actual_first_tool_utc='Registry and computation timestamps authoritative; firsttool not precisely recorded',frozen_at_utc=datetime.now(timezone.utc).isoformat(),
 hypothesis='Prior24/76day windows passed historical gates but early-fold returns weakened. Extend predeclared span neighbourhood without claiming independent OOS. Predeclare faster24/slower76day EMA with old50day readonly, fixed3percent band and exit30;joint entry10/15/20 sensitivity tests reaction speed against whipsaw losses and early-fold gains. No OOS winner selection,all outcomes saved.',
 grid={'entry_lookback_days':[10,15,20],'exit_lookback_days':[30],'EMA_span_days':[24,50,76],'EMA_symmetric_bands':[.03],'BTC_initial_weights':[.675],'raw_weight_pairs':[[.675,.325]],'capital_usdt':2000,'component_capital_pairs_usdt':[[1350,650]],'predeclared_center':[15,50],'center_is_read_only_existing_anchor':True},
 allocation='Raw .675/.325 explicit initial fractions of2000USDT:1350BTC/650ETH independent sleeves. No normalization,rebalancing,maintained exposure or transfers. All changedEMA-band components use own trades/costs;combination sum actual-costed absoluteNAV once.',
 sensitivity='Two axes entry10/15/20 x EMA_span24/50/76,band3percent/exit30/funding67.5:32.5 fixed.36new24/76span configs108scenes,18oldspan50 configs54scenes readonly;centre entry15/span50 old.',
 reuse_source={'round':source.name,'report':str((source/'report.json').relative_to(ROOT)),'report_sha256':sha(source/'report.json')},
 qualification_scope='Unchanged fixed eight gates;oldexit30 source/report/spec/archive/ledger untouched;full entry/EMA-band neighbourhood descriptive on repeated development history.',
 cross_period_confirmation='Same rule,entry,exit,band,asset/capital or full combination must pass2025and2026 separately;no pooling reset periods.',
 forward_resume={'source_state':str((latest/'forward_state.json').relative_to(ROOT)),'state_sha256':sha(latest/'forward_state.json'),'source_report':str((latest/'forward_report.json').relative_to(ROOT)),'report_sha256':sha(latest/'forward_report.json'),'resume_utc':'2026-10-06T05:10:00Z','cutoff_utc':'2026-10-06T11:10:00Z','daily_decision_utc':None,'new_minutes':360,'cumulative_minutes':6429,'prior6435points':6075,'new_reference_points':0,'total6435points':6435,'action':'Continue originalSMA65/1percent75/25 holdings with360closedminutes from last actual05:10cutoff,cover missing中间interval;zero new daily decisions,retain allpositions/costs/history,no reset/forcedexit.','new_configs':3,'new_cost_scenes':9,'qualification':'Actual6429minutes/4complete days partial snapshot insufficient180days/sixfolds;original plan collecting.'})
plan['forward_plan']['status_at_freeze']='OriginalSMA65/1percent75/25 collecting;No new daily decision;nextOct7UTC00:01;terminal2027Mar31 unchanged.'
plan['knowledge_sources']=[{'url':'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html','accessed_utc_date':'2026-10-05','scope':'EMA recurrence,localpandas2.2.3 independently audited;not profitability evidence.'},{'url':'https://developers.binance.com/en/docs/binance-spot-api-docs/rest-api/market-data-endpoints','accessed_utc_date':'2026-10-05','scope':'Closed1m/1d query endpoints,retained rawresponses/URL/timestamp/hash.'}]
plan['next_research_basis']='Compare all changedEMAspan24/76 variants with oldEMAspan50/band3percent results;prioritize fold/DD stability,not headline winner;freeze any subsequent variants separately.'
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
  assert fields['exit_days']==30 and fields['EMA_band']==.03 and fields['span_days']==50
  prev=next(b for b in oldbatch if b['fingerprint']==fp);r=old['configs'][prev['name']]
  assert records[fp]['result_available'] and records[fp]['report_sha256']==sha(source/'report.json')
  b={**prev,**fields,'is_new':False,'source_ref':{'source_round':source.name,'report':plan['reuse_source']['report'],'report_sha256':plan['reuse_source']['report_sha256'],'archive':r['archive'],'archive_sha256':r['archive_sha256'],'spec_sha256':sha(ROOT/prev['spec'])}}
  print('READ_ONLY_EXACT',prev['name'],flush=True)
 else:b=save(sp,{**fields,'is_new':True},batch)
 grid.append(b);return fp
weights=[.675,.325]
for y in plan['periods']:
 for ia,asset in enumerate(('BTC','ETH')):
  t=next(c for c in old['configs'].values() if c['year']==y and c.get('asset')==asset and c['entry_days']==15 and c['BTC_weight']==.675 and c['EMA_band']==.03)
  for entry in plan['grid']['entry_lookback_days']:
   for span in plan['grid']['EMA_span_days']:
    band=.03
    exit=30
    capital=int(D('2000')*D(str(weights[ia])));sp=copy.deepcopy(json.loads((ROOT/t['spec']).read_text()));sp.update(name=f'filtered_span_{y}_{asset}_e{entry}_b0.03_x30_s{span}_c{capital}',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters'].update(entry_lookback_days=entry,exit_lookback_days=exit,EMA_symmetric_band=band,EMA_span_days=span)
    fps[(y,asset,entry,span)]=cell(sp,{'year':y,'role':'component','asset':asset,'entry_days':entry,'exit_days':exit,'EMA_band':band,'span_days':span,'BTC_weight':weights[0],'raw_weights':weights,'capital_usdt':capital})
 t=next(c for c in old['configs'].values() if c['year']==y and c['role']=='combination' and c['entry_days']==15 and c['BTC_weight']==.675 and c['EMA_band']==.03)
 for entry in plan['grid']['entry_lookback_days']:
  for span in plan['grid']['EMA_span_days']:
   band=.03
   exit=30
   sp=copy.deepcopy(json.loads((ROOT/t['spec']).read_text()));sp.update(name=f'filtered_span_{y}_combo_e{entry}_b0.03_x30_s{span}_btc0.675',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['components']=[{'fingerprint':fps[(y,a,entry,span)],'weight':w} for a,w in zip(('BTC','ETH'),weights)]
   cell(sp,{'year':y,'role':'combination','entry_days':entry,'exit_days':exit,'EMA_band':band,'span_days':span,'BTC_weight':weights[0],'raw_weights':weights,'capital_usdt':2000})
assert len(batch)==36 and len(grid)==54 and sum(not b['is_new'] for b in grid)==18
(ROUND/'batch.json').write_text(json.dumps(batch,indent=2)+'\n');(ROUND/'grid_batch.json').write_text(json.dumps(grid,indent=2)+'\n')
forward=[];oldfb=json.loads((latest/'forward_batch.json').read_text())
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(b for b in oldfb if b.get('asset')==asset);sp=json.loads((ROOT/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)['fingerprint']
b=oldfb[-1];sp=json.loads((ROOT/b['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];sp['components']=[{'fingerprint':fps[a],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward)
(ROUND/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n');print('PASS:36new actual-capital historical and3new cutoff configurations reserved;18existing EMAspan50/band3percent exact definitions read-only.')
