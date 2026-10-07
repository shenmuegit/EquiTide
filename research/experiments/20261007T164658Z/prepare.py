"""Freeze pure-close-channel entry/initial allocation grid; preserve exact old anchors."""
import copy,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=ROOT/'research/automation/registry.jsonl';records=registry.read_records(ledger);canonical={registry.fingerprint(v['spec']) for v in records.values()}
prior=json.loads(gzip.decompress((ROUND/'prior_summary.json.gz').read_bytes()));assert sha(ledger)==prior['ledger_sha256'] and len(records)==2119 and len(canonical)==2117
latest=ROOT/'research/experiments/20261007T143820Z';source=latest
old=json.loads((source/'report.json').read_text());plan=json.loads((ROOT/'research/experiments/20261003T052049Z/spec.json').read_text())
plan.update(round=ROUND.name,trigger_utc='2026-10-07T16:46:58.419Z',actual_first_tool_utc=None,frozen_at_utc=datetime.now(timezone.utc).isoformat(),
 hypothesis='The prior BTC65/ETH35 close-channel15/30 result improved2026 return and drawdown versus75/25 on reused development histories. Predeclare entry10/15/20 by BTC55/60/65percent to probe the lowerBTC boundary. MoreETH may increase upside but worsen fold signs and drawdown. Freeze every cell before results;resimulate1100/900 and1200/800 actual budgets,read exact1300/700 anchors;no scaling old NAV or independence claim.',
 grid={'entry_lookback_days':[10,15,20],'exit_lookback_days':30,'BTC_initial_weights':[.55,.60,.65],'raw_weight_pairs':[[.55,.45],[.60,.40],[.65,.35]],'capital_usdt':2000,'component_capital_pairs_usdt':[[1100,900],[1200,800],[1300,700]],'predeclared_center':[15,.60],'center_is_read_only_existing_anchor':False,'read_only_anchor_weight':.65},
 allocation='Explicit rawBTC55/60/65percent and rawETH45/40/35percent of2000USDT initial independent sleeves;no automatic normalization,maintained weights,transfers or rebalance. Resimulate1100/900 and1200/800USDT with actual budget-dependent impact/tick/LOT. Sum absolute costed sleeve NAV once.',
 sensitivity='Six full3x3 surfaces:entry10/15/20 x initialBTC55/60/65percent,exit30 fixed. Components vary entry and actual capital,which is execution-size sensitivity;combination weights change exposure.36new exact definitions/108cost scenes;18exact65/35 definitions/54scenes only read.',
 reuse_source={'round':source.name,'report':str((source/'report.json').relative_to(ROOT)),'report_sha256':sha(source/'report.json')},
 prior_canonical_trials=prior['canonical'],qualification_scope='Same eight predeclared gates;new cells use complete allocation-entry neighbourhood. Existing exact anchors retain original ledger status/report/criteria;current expanded grid diagnosis does not overwrite old records.',
 cross_period_confirmation='Require identical rule,entry and real capital/raw initial weights to pass2025and2026 separately. Both histories are reused development,not untouched final tests. No pooled account across reset years.')
plan.pop('EMA_definition',None);plan.pop('reference',None)
component_template=next(c for c in old['configs'].values() if c['role']=='component' and c['entry_days']==15 and c['exit_days']==30)
sp0=json.loads((ROOT/component_template['spec']).read_text());plan['rules']=copy.deepcopy(sp0['logic']);plan['channel_definition']=sp0['parameters']['channel_definition']
plan['walk_forward']['fit']='No labels,fit or per-fold/OOS selection;fixed causal daily close-channel rules;180train/3gap/purge0 and six continuous30day diagnostic folds. OOS starts desired cash;do not reset cash,units or desired at fold boundaries.'
plan['forward_plan']['status_at_freeze']='Original frozenSMA65/band1percent75/25 collecting;Oct7 daily decision already processed,next Oct8UTC00:01,end2027Mar31. Historical channel allocations do not modify this account.'
plan['forward_resume']={'source_state':str((latest/'forward_state.json').relative_to(ROOT)),'state_sha256':sha(latest/'forward_state.json'),'source_report':str((latest/'forward_report.json').relative_to(ROOT)),'report_sha256':sha(latest/'forward_report.json'),'resume_utc':'2026-10-07T14:10:00Z','cutoff_utc':'2026-10-07T16:40:00Z','new_minutes':150,'cumulative_minutes':8199,'prior_NAV_points':8056,'new_reference_points':0,'total_NAV_points':8206,'action':'Append150 closed minute valuation marks to original frozen per-cost positions;zero daily decisions,fills or forced liquidation;next Oct8UTC00:01. This legacy delayed shadow is separate from newly scheduled10-strategy actual-quote paper accounts.','new_configs':3,'new_cost_scenes':9,'qualification':'Actual8199minute partial delayed shadow,5complete days;insufficient180days/sixfold;original long-term plan collecting.'}
plan['read_only_comparator_refs']=[x for x in plan['read_only_comparator_refs'] if x['kind'] in ('SMA_or_hold','CHANNEL15_30')]
plan['knowledge_sources']=[{'url':'https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1992.tb04681.x','original_access_utc_date':'2026-10-02','scope':'Reuse existing channel rationale,not original-paper replication or evidence of crypto profitability.'},{'url':'https://github.com/binance/binance-public-data','scope':'Same cached official spot archive/checksums;all four normalized hashes rechecked.'},{'url':'https://data-api.binance.vision/api/v3/klines','scope':'Actual closed-minute HTTP responses for unchanged frozen account will be retained this round.'}]
plan['reused_code_sha256']={str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'research/experiments/20261003T052049Z/evaluate.py',source/'evaluate.py',source/'signals.py',ROOT/'research/experiments/20261002T174933Z/evaluate.py',ROOT/'research/experiments/20261001T133655Z/evaluate.py',ROOT/'research/experiments/20261001T133655Z/kernel.py']}
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
  assert fields['BTC_weight']==.65
  rec=records[fp];rp=ROOT/rec['report'];assert rec['result_available'] and rec['report_sha256']==sha(rp)
  src=json.loads(rp.read_text());prev=next(c for c in src['configs'].values() if c['fingerprint']==fp)
  b={**{k:prev[k] for k in ('name','fingerprint','spec')},**fields,'is_new':False,'source_ref':{'source_round':Path(prev['archive']).parts[2],'report':rec['report'],'report_sha256':sha(rp),'archive':prev['archive'],'archive_sha256':prev['archive_sha256'],'spec_sha256':sha(ROOT/prev['spec'])}}
  print('READ_ONLY_EXACT',prev['name'],flush=True)
 else:b=save(sp,{**fields,'is_new':True},batch)
 grid.append(b);return fp
for y in plan['periods']:
 for ia,asset in enumerate(('BTC','ETH')):
  t=next(c for c in old['configs'].values() if c['year']==y and c.get('asset')==asset and c['entry_days']==15 and c['exit_days']==30)
  for entry in plan['grid']['entry_lookback_days']:
   for weights in plan['grid']['raw_weight_pairs']:
    capital=int(D('2000')*D(str(weights[ia])));sp=copy.deepcopy(json.loads((ROOT/t['spec']).read_text()));sp.update(name=f'channel_alloc_{y}_{asset}_e{entry}_x30_c{capital}',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters'].update(entry_lookback_days=entry,initial_capital_usdt=capital)
    fps[(y,asset,entry,weights[0])]=cell(sp,{'year':y,'role':'component','asset':asset,'entry_days':entry,'exit_days':30,'BTC_weight':weights[0],'raw_weights':weights,'capital_usdt':capital})
 t=next(c for c in old['configs'].values() if c['year']==y and c['role']=='combination' and c['entry_days']==15 and c['exit_days']==30)
 for entry in plan['grid']['entry_lookback_days']:
  for weights in plan['grid']['raw_weight_pairs']:
   sp=copy.deepcopy(json.loads((ROOT/t['spec']).read_text()));sp.update(name=f'channel_alloc_{y}_combo_e{entry}_x30_btc{weights[0]}',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['components']=[{'fingerprint':fps[(y,a,entry,weights[0])],'weight':w} for a,w in zip(('BTC','ETH'),weights)]
   cell(sp,{'year':y,'role':'combination','entry_days':entry,'exit_days':30,'BTC_weight':weights[0],'raw_weights':weights,'capital_usdt':2000})
assert len(batch)==36 and len(grid)==54 and sum(not b['is_new'] for b in grid)==18
(ROUND/'batch.json').write_text(json.dumps(batch,indent=2)+'\n');(ROUND/'grid_batch.json').write_text(json.dumps(grid,indent=2)+'\n')
forward=[];oldfb=json.loads((latest/'forward_batch.json').read_text())
for asset,capital in [('BTC',1500),('ETH',500)]:
 b=next(b for b in oldfb if b.get('asset')==asset);sp=json.loads((ROOT/b['spec']).read_text());sp.update(name='forward_snapshot_'+asset,validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];fps[asset]=save(sp,{'asset':asset,'capital_usdt':capital},forward)['fingerprint']
b=oldfb[-1];sp=json.loads((ROOT/b['spec']).read_text());sp.update(name='forward_snapshot_combo',validation_plan=str((ROUND/'spec.json').relative_to(ROOT)));sp['parameters']['end_utc']=plan['forward_resume']['cutoff_utc'];sp['components']=[{'fingerprint':fps[a],'weight':w} for a,w in zip(('BTC','ETH'),(.75,.25))];save(sp,{'capital_usdt':2000},forward)
(ROUND/'forward_batch.json').write_text(json.dumps(forward,indent=2)+'\n');print('PASS:36new actual-capital historical and3new cutoff definitions reserved;18old exact anchors read-only.')
