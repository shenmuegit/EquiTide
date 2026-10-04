"""Freeze allocation/entry grid with real sleeve capitals and read-only exact60/40 results."""
import copy,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=ROOT/'research/automation/registry.jsonl';records=registry.read_records(ledger);canonical={registry.fingerprint(v['spec']) for v in records.values()}
assert len(canonical)==1142 and len(records)==1144 and all(v.get('result_available') and v['status']!='reserved' for v in records.values())
prior=json.loads(gzip.decompress((ROUND/'prior_summary.json.gz').read_bytes()));assert sha(ledger)==prior['ledger_sha256'] and prior['lines']==2383
latest=ROOT/'research/experiments/20261003T232437Z';source=ROOT/'research/experiments/20261003T212439Z';plan=copy.deepcopy(json.loads((latest/'spec.json').read_text()));old=json.loads((source/'report.json').read_text());oldbatch=json.loads((source/'batch.json').read_text())
plan.update(round=ROUND.name,trigger_utc='2026-10-04T03:25:07.824Z',actual_first_tool_utc='2026-10-04T03:25:08Z',frozen_at_utc=datetime.now(timezone.utc).isoformat(),
 hypothesis='Previously BTC30/45percent had positive totals but only3of6positive2026folds;BTC60percent had4of6.With no OOS tuning within this batch,freeze50/55/60percent x entry10/15/20 to describe the allocation transition,not claim independent confirmation.Resimulate1000/1000and1100/900sleeves with impact and exchange rounding;never scale oldNAV.',
 grid={'entry_lookback_days':[10,15,20],'exit_lookback_days':30,'EMA_span_days':50,'EMA_symmetric_band':.015,'BTC_initial_weights':[.635,.675,.715],'raw_weight_pairs':[[.635,.365],[.675,.325],[.715,.285]],'capital_usdt':2000,'component_capital_pairs_usdt':[[1270,730],[1350,650],[1430,570]],'predeclared_center':[15,.675],'center_is_read_only_existing_anchor':False},
 allocation='RawBTC50/55/60percent and rawETH50/45/40percent are explicit initial fractions of2000USDT,not maintained exposure.Independent1000/1000,1100/900,1200/800sleeves.Never automatically normalize,rebalance or transfer.New sizes resimulated with own volume impact/tick/LOT;absolute NAVs summed once.',
 sensitivity='Six3x3 surfaces entry10/15/20 x originalBTCweight50/55/60percent,exit30 andEMA50/band1.5percent fixed.Each component is simulated with capital of its corresponding sleeve,so its weight-axis is a size/rounding/impact sensitivity rather than second risk allocation.36new exact configs/108scenes reserved;18exact60/40configs/54scenes read-only.',
 reuse_source={'round':source.name,'report':str((source/'report.json').relative_to(ROOT)),'report_sha256':sha(source/'report.json')},
 qualification_scope='Unchanged gates applied on full9cell entry/initial allocation neighbourhood for new definitions.Old60/40 ledger status and original criteria untouched;expanded-neighbourhood qualification separately descriptive.',
 cross_period_confirmation='Identical rule,entry,asset/sleeve actual capital or original raw weights must pass2025and2026 separately.No cross-year pooled reset returns.',
 forward_resume={'source_state':str((latest/'forward_state.json').relative_to(ROOT)),'state_sha256':sha(latest/'forward_state.json'),'source_report':str((latest/'forward_report.json').relative_to(ROOT)),'report_sha256':sha(latest/'forward_report.json'),'resume_utc':'2026-10-03T23:10:00Z','cutoff_utc':'2026-10-04T03:10:00Z','daily_decision_utc':'2026-10-04T00:01:00Z','new_minutes':240,'cumulative_minutes':3069,'prior_NAV_points':2832,'new_reference_points':1,'total_NAV_points':3073,'action':'Append240new closed minute marks to original per-costSMA65/1percent positions,trades,costs,desired.Next daily decisionOct4UTC00:01;no rescaling,new buys,forced liquidation or applying current historical allocation weights.','new_configs':3,'new_cost_scenes':9,'qualification':'Partial2709minutes/1complete day insufficient180day/sixfold;original plan collecting.'})
plan['forward_plan']['status_at_freeze']='Original frozenSMA65/1percent75/25 still collecting with latest daily decisionOct3UTC00:01 already processed.Current new historical weights never applied;terminal2027Mar31 unchanged.'
plan['knowledge_sources']=[{'url':'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html','accessed_utc_date':'2026-10-03','scope':'Same EMA recurrence;localpandas2.2.3 audit,not profitability evidence.'},{'url':'https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market','accessed_utc_date':'2026-10-03','scope':'Closed real minute bars using startTime/endTime for original shadow continuation.'}]
for y in plan['periods']:
 c=next(c for c in old['configs'].values() if c['year']==y and c['role']=='combination' and c['entry_days']==15 and c['span_days']==50 and c['BTC_weight']==.675)
 plan['read_only_comparator_refs'].append({'name':c['name'],'year':y,'kind':'original_filtered75_25_anchor','report':str((source/'report.json').relative_to(ROOT)),'report_sha256':sha(source/'report.json')})
plan.update(hypothesis='Describe a narrow allocation neighbourhood around previously qualified67.5/32.5;freezeBTC65.5/67.5/69.5percent xentry10/15/20 before looking at new results.Only65.5and69.5new;67.5read-only.Not independent evidence on repeatedly used history.',allocation='Original weights .655/.345,.675/.325,.695/.305 are initial fractions of2000USDT:1310/690,1350/650,1390/610.Independent sleeves,no normalization,rebalancing,transfer or maintained exposure.New components resimulated at own actual size then absolute NAVs summed once.',sensitivity='entry10/15/20 and BTCinitial65.5/67.5/69.5percent two axes;36new definitions/108costscenes;18exact67.5percent configs/54costscenes read-only.',qualification_scope='Unchanged gates;old67.5percent ledger untouched;neighbourhood qualification separately descriptive.')
plan['forward_resume']['action']='Append120closedminutes to unchanged original positions;no daily decision or new fills beforeOct4UTC00:01.'
plan.update(hypothesis='Freeze63.5/67.5/71.5 initialBTCfractions xentry10/15/20 to widen the prior narrow neighbourhood around read-only67.5;check net returns and wholepath risk without claiming independent or continuous robustness.',allocation='Originalrawweights .635/.365,.675/.325,.715/.285 represent initial2000USDT funds1270/730,1350/650,1430/570.Independent actual-size accounts,no normalization,rebalancing or transfers;sum component absolute NAVs once.',sensitivity='Two axes entry10/15/20 andBTCinitial63.5/67.5/71.5percent;36newconfigs/108costscenes plus18readonly67.5configs/54scenes.')
plan['forward_resume']['action']='Continue originalSMA65/1percent75/25 accounts through Oct4UTC00:01 daily decision;append240closedminute marks plus1execution reference.Originalfloatingcostmodel,not current historicalparameters.'
plan['forward_plan']['status_at_freeze']='Collecting;Oct4UTC00:01 decision pending reconstruction from complete daily bars,terminal2027Mar31 unchanged.'
plan['knowledge_sources']=[{'url':'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html','accessed_utc_date':'2026-10-04','scope':'EMArecurrence;local2.2.3'},{'url':'https://developers.binance.com/en/docs/binance-spot-api-docs/rest-api/market-data-endpoints','accessed_utc_date':'2026-10-04','scope':'Actualclosedminute/dailybars.'}]
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
(ROUND/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n');print('PASS:36new actual-capital historical and3new cutoff configurations reserved;18existing60/40 exact definitions read-only.')
