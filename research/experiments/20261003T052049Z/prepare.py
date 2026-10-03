"""Freeze allocation/entry grid with real sleeve capitals and read-only exact75/25 results."""
import copy,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=ROOT/'research/automation/registry.jsonl';records=registry.read_records(ledger);canonical={registry.fingerprint(v['spec']) for v in records.values()}
assert len(canonical)==869 and len(records)==871 and all(v.get('result_available') and v['status']!='reserved' for v in records.values())
prior=json.loads(gzip.decompress((ROUND/'prior_summary.json.gz').read_bytes()));assert sha(ledger)==prior['ledger_sha256'] and prior['lines']==1762
latest=ROOT/'research/experiments/20261003T015203Z';source=ROOT/'research/experiments/20261002T235103Z';plan=copy.deepcopy(json.loads((latest/'spec.json').read_text()));old=json.loads((source/'report.json').read_text());oldbatch=json.loads((source/'batch.json').read_text())
plan.update(round=ROUND.name,trigger_utc='2026-10-03T05:20:49.476Z',actual_first_tool_utc='2026-10-03T05:21:27Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),
 hypothesis='Changing originalBTC/ETH initial allocations may alter continuous combined risk and fold consistency without changing fixed channel/EMA signal.BTC-heavy portfolios may reduce ETH exposure but sacrifice upside;ETH-heavy portfolios may increase drawdown or change fold signs.Resimulate changed real1200/800 and1800/200USDT sleeve budgets with impact and exchange rounding;never scale1500/500 NAV.Freeze all cells first.',
 grid={'entry_lookback_days':[10,15,20],'exit_lookback_days':30,'EMA_span_days':50,'EMA_symmetric_band':.015,'BTC_initial_weights':[.6,.75,.9],'raw_weight_pairs':[[.6,.4],[.75,.25],[.9,.1]],'capital_usdt':2000,'component_capital_pairs_usdt':[[1200,800],[1500,500],[1800,200]],'predeclared_center':[15,.75],'center_is_read_only_existing_anchor':True},
 allocation='RawBTC60/75/90percent and rawETH40/25/10percent are explicit initial fractions of2000USDT,not maintained exposure.Independent1200/800,1500/500,1800/200sleeves.Never automatically normalize,rebalance or transfer.New sizes resimulated with own volume impact/tick/LOT;absolute NAVs summed once.',
 sensitivity='Six3x3 surfaces entry10/15/20 x originalBTCweight60/75/90percent,exit30 andEMA50/band1.5percent fixed.Each component is simulated with capital of its corresponding sleeve,so its weight-axis is a size/rounding/impact sensitivity rather than second risk allocation.36new exact configs/108scenes reserved;18exact75/25configs/54scenes read-only.',
 reuse_source={'round':source.name,'report':str((source/'report.json').relative_to(ROOT)),'report_sha256':sha(source/'report.json')},
 qualification_scope='Unchanged gates applied on full9cell entry/initial allocation neighbourhood for new definitions.Old75/25 ledger status and original criteria untouched;expanded-neighbourhood qualification separately descriptive.',
 cross_period_confirmation='Identical rule,entry,asset/sleeve actual capital or original raw weights must pass2025and2026 separately.No cross-year pooled reset returns.',
 forward_resume={'source_state':str((latest/'forward_state.json').relative_to(ROOT)),'state_sha256':sha(latest/'forward_state.json'),'source_report':str((latest/'forward_report.json').relative_to(ROOT)),'report_sha256':sha(latest/'forward_report.json'),'resume_utc':'2026-10-03T01:40:00Z','cutoff_utc':'2026-10-03T05:10:00Z','new_minutes':210,'cumulative_minutes':1749,'prior_NAV_points':1542,'new_reference_points':0,'total_NAV_points':1752,'action':'Append210new closed minute marks to original per-costSMA65/1percent positions,trades,costs,desired.Next daily decisionOct4UTC00:01;no rescaling,new buys,forced liquidation or applying current historical allocation weights.','new_configs':3,'new_cost_scenes':9,'qualification':'Partial1749minutes/1complete day insufficient180day/sixfold;original plan collecting.'})
plan['forward_plan']['status_at_freeze']='Original frozenSMA65/1percent75/25 still collecting with latest daily decisionOct3UTC00:01 already processed.Current new historical weights never applied;terminal2027Mar31 unchanged.'
plan['knowledge_sources']=[{'url':'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html','accessed_utc_date':'2026-10-03','scope':'Same EMA recurrence;localpandas2.2.3 audit,not profitability evidence.'},{'url':'https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market','accessed_utc_date':'2026-10-03','scope':'Closed real minute bars using startTime/endTime for original shadow continuation.'}]
for y in plan['periods']:
 c=next(c for c in old['configs'].values() if c['year']==y and c['role']=='combination' and c['entry_days']==15 and c['span_days']==50)
 plan['read_only_comparator_refs'].append({'name':c['name'],'year':y,'kind':'original_filtered75_25_anchor','report':str((source/'report.json').relative_to(ROOT)),'report_sha256':sha(source/'report.json')})
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
  assert fields['BTC_weight']==.75
  prev=next(b for b in oldbatch if b['fingerprint']==fp);r=old['configs'][prev['name']]
  assert records[fp]['result_available'] and records[fp]['report_sha256']==sha(source/'report.json')
  b={**prev,**fields,'is_new':False,'source_ref':{'source_round':source.name,'report':plan['reuse_source']['report'],'report_sha256':plan['reuse_source']['report_sha256'],'archive':r['archive'],'archive_sha256':r['archive_sha256'],'spec_sha256':sha(ROOT/prev['spec'])}}
  print('READ_ONLY_EXACT',prev['name'],flush=True)
 else:b=save(sp,{**fields,'is_new':True},batch)
 grid.append(b);return fp
for y in plan['periods']:
 for ia,asset in enumerate(('BTC','ETH')):
  t=next(c for c in old['configs'].values() if c['year']==y and c.get('asset')==asset and c['entry_days']==15 and c['span_days']==50)
  for entry in plan['grid']['entry_lookback_days']:
   for weights in plan['grid']['raw_weight_pairs']:
    capital=int(D('2000')*D(str(weights[ia])));sp=copy.deepcopy(json.loads((ROOT/t['spec']).read_text()));sp.update(name=f'filtered_alloc_{y}_{asset}_e{entry}_s50_c{capital}',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters'].update(entry_lookback_days=entry,initial_capital_usdt=capital)
    fps[(y,asset,entry,weights[0])]=cell(sp,{'year':y,'role':'component','asset':asset,'entry_days':entry,'exit_days':30,'span_days':50,'BTC_weight':weights[0],'raw_weights':weights,'capital_usdt':capital})
 t=next(c for c in old['configs'].values() if c['year']==y and c['role']=='combination' and c['entry_days']==15 and c['span_days']==50)
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
(ROUND/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n');print('PASS:36new actual-capital historical and3new cutoff configurations reserved;18existing75/25 exact definitions read-only.')
