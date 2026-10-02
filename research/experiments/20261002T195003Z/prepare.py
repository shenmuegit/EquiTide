"""Freeze channel/asymmetric-SMA portfolios from unchanged costed component evidence."""
import copy,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=ROOT/'research/automation/registry.jsonl';records=registry.read_records(ledger);canonical={registry.fingerprint(v['spec']) for v in records.values()}
assert len(canonical)==695 and all(v.get('result_available') and v['status']!='reserved' for v in records.values())
source=ROOT/'research/experiments/20261002T174933Z';channel=json.loads((source/'report.json').read_text());asym_path=ROOT/'research/experiments/20261002T094655Z/report.json';asym=json.loads(asym_path.read_text());base=json.loads((source/'spec.json').read_text())
plan={'round':ROUND.name,'trigger_utc':'2026-10-02T19:50:03.427Z','actual_first_tool_utc':'2026-10-02T19:50:39Z','frozen_at_utc':datetime.now(timezone.utc).isoformat(),
 'hypothesis':'Combine close-channel breakout and asymmetricSMA65 on opposite assets to test whether different causal timing diversifies fold returns and drawdowns.The same BTC/ETH trend may dominate both;new combinations may remain concentrated or add whipsaws.Freeze both directions and full two-parameter grid before evaluating new portfolio NAV.',
 'grid':{'CHANNEL_entry_days':[10,15,20],'CHANNEL_exit_days':30,'ASMA_lookback_days':65,'ASMA_entry_band':[.0125,.015,.02],'ASMA_exit_band':.005,'directions':['BTC_CHANNEL_ETH_ASMA','BTC_ASMA_ETH_CHANNEL'],'raw_weights':[.75,.25],'capital_usdt':2000,'component_capitals_usdt':[1500,500],'predeclared_center':{'CHANNEL_entry_days':15,'ASMA_entry_band':.015}},
 'new_configs':36,'new_cost_scenes':108,'prior_canonical_trials':695,'walk_forward':copy.deepcopy(base['walk_forward']),'execution':base['execution'],'costs':base['costs'],'gates':base['gates'],
 'CHANNEL_rules':base['rules'],'CHANNEL_definition':base['channel_definition'],'CHANNEL_initialization':base['signal_initialization'],'ASMA_rules':asym['plan']['rules'],'ASMA_initialization':asym['plan']['signal_initialization'],
 'allocation':'Raw BTC/ETH75/25 means initial1500/500USDT of2000. Reuse fully costed absolute minute NAV at exactly those funded sizes;no second weighting,no auto-normalisation,capital transfers,maintained weights or rebalance.Both separate spot accounts retain their own cash/units.No new component simulations.',
 'sensitivity':'Each historical year/direction:complete3x3 channel entry10/15/20days x asymmetricSMA entry1.25/1.5/2percent.All exits fixedchannel30days/SMA0.5percent;lookbackSMA65.All36 concrete combinations reserve before summing NAV.Record all cost/fold/return/risk and adjacent2sd descriptions.No OOS selection or frozen-observer change.',
 'periods':base['periods'],'development_history_reused':True,'component_report_rounds':{'CHANNEL':'20261002T174933Z','ASMA':'20261002T094655Z'},
 'interpretation':'Both histories are repeatedly used development periods,and existing component results motivated this combination hypothesis.Causal trades do not remove retrospective selection/multiple-testing bias.Not untouched finalholdout,statistical significance or stable live profit.Same realised NAV for different parameters is disclosed,not independent evidence.',
 'cross_period_confirmation':'Same direction/channel entry/ASMA entry/rawweights must meet all gates in EACH separately reported sixfold period.No new cross-year compounded backtest.',
 'reference':{'title':'Portfolio Selection','author':'Harry Markowitz','version':'Journal of Finance7(1),March1952,77-91','url':'https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1952.tb01525.x','accessed_utc_date':'2026-10-02','scope':'Publisher bibliographic metadata accessed;fulltext not supplied by this page.Combination diversification is our explicit economic hypothesis,not replication of this paper,mean-variance optimisation or proof of crypto profit.'},
 'market_data_reference':{'url':'https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market','accessed_utc_date':'2026-10-02','scope':'Official current public klines interface for cumulative shadow marks;raw actual replies archived.'},
 'forward_plan':copy.deepcopy(base['forward_plan']),
 'forward_resume':{'source_state':str((source/'forward_state.json').relative_to(ROOT)),'state_sha256':sha(source/'forward_state.json'),'source_report':str((source/'forward_report.json').relative_to(ROOT)),'report_sha256':sha(source/'forward_report.json'),'resume_utc':'2026-10-02T17:40:00Z','cutoff_utc':'2026-10-02T19:40:00Z','new_minutes':120,'cumulative_minutes':1179,'action':'Append closed minutes to original positions/costs only;next daily decisionOct3UTC00:01.No reset,repeat buys or terminal liquidation.','new_configs':3,'new_cost_scenes':9,'qualification':'Partial1179minutes/0complete days;no180day/sixfold qualification,longrun plan remains collecting.'}}
plan['walk_forward']['fit']='No fit/labels or per-fold tuning. Reuse fixed causal Decimal close-channel/ASMA decisions;180train/3gap/purge0,continuous6x30 diagnostics.Cash/units crossfolds with sameOOS183cash initialization.'
plan['forward_plan']['status_at_freeze']='Collecting;source174933 cumulative1059minutes retains original symmetricSMA65/1percent and original frozen hash.'
comps=[]
for y,period in base['periods'].items():
 for rp,kind in [(ROOT/period['report'],'SMA_or_hold'),(asym_path,'ASMA_center'),(source/'report.json','CHANNEL15_30')]:
  old=json.loads(rp.read_text())
  for name,c in old['configs'].items():
   if c.get('year',y)!=y:continue
   keep=(kind=='SMA_or_hold' and (c['role']=='comparator_combination' or (c['role']=='combination' and c['lookback_days']==65 and c['raw_weights']==[.75,.25]))) or (kind=='ASMA_center' and c['role']=='combination' and c['entry_band']==.015 and c['exit_band']==.005) or (kind=='CHANNEL15_30' and c['role']=='combination' and c['entry_days']==15 and c['exit_days']==30)
   if keep:comps.append({'name':name,'year':y,'kind':kind,'report':str(rp.relative_to(ROOT)),'report_sha256':sha(rp)})
assert len(comps)==8;plan['read_only_comparator_refs']=comps
(ROUND/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
batch=[]
def save(sp,fields,target):
 fp=registry.fingerprint(sp);assert fp not in canonical
 path=ROUND/'specs'/f'{sp["name"]}.json';path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(sp,indent=2)+'\n')
 run=subprocess.run([sys.executable,'research/automation/registry.py','reserve',str(path.relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True);print(sp['name'],run.returncode,run.stdout.strip(),flush=True)
 if run.returncode:raise RuntimeError('STOP before evaluation:'+run.stdout+run.stderr)
 target.append({'name':sp['name'],'fingerprint':fp,'spec':str(path.relative_to(ROOT)),**fields});return fp
for y in ('2025','2026'):
 template=next(c for c in channel['configs'].values() if c['role']=='combination' and c['year']==y)
 def lookup(kind,asset,value):
  report=channel if kind=='CHANNEL' else asym;rp=source/'report.json' if kind=='CHANNEL' else asym_path
  matches=[(n,c) for n,c in report['configs'].items() if c['role']=='component' and c['asset']==asset and c['year']==y and ((kind=='CHANNEL' and c['entry_days']==value and c['exit_days']==30) or (kind=='ASMA' and c['lookback_days']==65 and c['entry_band']==value and c['exit_band']==.005))]
  assert len(matches)==1;name,c=matches[0];sp=c.get('spec_path',c.get('spec'));capital=1500 if asset=='BTC' else 500
  assert records[c['fingerprint']]['result_available'] and json.loads((ROOT/sp).read_text())['parameters']['initial_capital_usdt']==capital
  return {'kind':kind,'name':name,'report':str(rp.relative_to(ROOT)),'report_sha256':sha(rp),'source_round':Path(c['archive']).parts[2],'fingerprint':c['fingerprint'],'archive':c['archive'],'archive_sha256':c['archive_sha256'],'spec':sp,'capital_usdt':capital,'asset':asset}
 for direction in plan['grid']['directions']:
  for entry in plan['grid']['ASMA_entry_band']:
   for days in plan['grid']['CHANNEL_entry_days']:
    kinds=('CHANNEL','ASMA') if direction=='BTC_CHANNEL_ETH_ASMA' else ('ASMA','CHANNEL');refs=[lookup(kind,asset,days if kind=='CHANNEL' else entry) for kind,asset in zip(kinds,('BTC','ETH'))]
    name=f'channel_asma_{y}_{direction}_e{entry}_d{days}';sp=copy.deepcopy(json.loads((ROOT/template['spec']).read_text()));sp.update(name=name,family='channel-asymmetric-sma-initial-capital',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['components']=[{'fingerprint':ref['fingerprint'],'weight':w} for ref,w in zip(refs,(.75,.25))]
    save(sp,{'year':y,'direction':direction,'ASMA_entry_band':entry,'CHANNEL_entry_days':days,'raw_weights':[.75,.25],'component_refs':refs},batch)
assert len(batch)==36 and len({c['fingerprint'] for c in batch})==36 and len({ref['fingerprint'] for c in batch for ref in c['component_refs']})==24
(ROUND/'batch.json').write_text(json.dumps(batch,indent=2)+'\n')
forward=[];oldfb=json.loads((source/'forward_batch.json').read_text());fps={}
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(b for b in oldfb if b.get('asset')==asset);sp=json.loads((ROOT/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)
b=next(b for b in oldfb if b['name']=='forward_snapshot_combo');sp=json.loads((ROOT/b['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];sp['components']=[{'fingerprint':fps[a],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward)
(ROUND/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n')
print('PASS:36 new combinations and3 new cutoff snapshots reserved before calculation;24 actual-result size-matched components only reused.')
