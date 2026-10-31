"""Freeze a semantic-deduplicated slow-regime/reversal neighborhood before valuation."""
import copy,gzip,itertools,json
from decimal import Decimal as D
import polars as pl
from common import *

records=reg.read_records(ROOT/'research/automation/registry.jsonl')
ETH='d0d984ab2ae7f899c6eb6e1e680c11cf91cf47177f946a93e13a95f7a08cd82e'
BTC='2122c03af949f66e9ab48802b8813121b9a94f1e0a5844a712c800a026a2fd4d'
PAR='9bef791333b2e6fb8166f7080ddad77af1b29bd73ad870baf928dd4ce72de21c'
base=json.loads((ROOT/'research/experiments/20261026T070542Z/plan_corrected.json').read_text())
rows=json.loads(gzip.decompress((R/'warmup_raw.json.gz').read_bytes()))
f=pl.read_parquet(ROOT/base['data']['assets']['ETH'][0]['path'])
assert D(rows[-1][4])==f['close'][1439]
assert abs(D(rows[-1][7])-sum(f['quote_volume'][:1440]))<D('.001')
warm={'passed':True,'raw':rel(R/'warmup_raw.json.gz'),'sha256':sha(R/'warmup_raw.json.gz'),'exact_overlap_close':rows[-1][4],'overlap_quote_volume_absolute_difference':str(abs(D(rows[-1][7])-sum(f['quote_volume'][:1440]))),'explicit_context_day_index_to_close':{str(i-3):x[4] for i,x in enumerate(rows[:3])},'scope':'Only three earlier ETH complete daily closes; all 8 minute/hour/funding/meta inputs and 370-day OOS axis remain unchanged. Negative context keys are explicit dictionary keys, never Python list wraparound.'}
put(R/'warmup_validation.json',warm)
old={};grid=[];batch=[];refs={}
def reference(fp):
 if fp in refs:return refs[fp]
 rec=records[fp];report=json.loads((ROOT/rec['report']).read_text());c=next(c for c in report['configs'].values() if c['fingerprint']==fp)
 x={**{k:c[k] for k in ['name','fingerprint','spec','archive','archive_sha256']},'scope':c.get('scope','native' if rec['spec']['kind']=='strategy' else 'parent'),'asset':c.get('asset','BTC' if fp==BTC else 'ETH' if rec['spec']['kind']=='strategy' else 'COMBO'),'capital_usdt':c.get('capital_usdt',rec['spec']['parameters']['initial_capital_usdt']),'report':rec['report'],'report_sha256':rec['report_sha256'],'status':rec['status'],'spec_sha256':sha(ROOT/c['spec'])}
 assert rec['result_available'] and sha(ROOT/x['archive'])==x['archive_sha256'] and sha(ROOT/x['report'])==x['report_sha256'];refs[fp]=x;return x
reference(BTC)
for S,H in itertools.product([21,28,35],[.01,.02,.03]):
 matches=[fp for fp,z in records.items() if z.get('result_available') and z['spec'].get('family')=='slow-trend-conditioned-short-roc-perpetual-reversal' and z['spec'].get('universe')==['ETH/USDT'] and all(z['spec']['parameters'].get(k)==v for k,v in {'fixed_entry_notional_usdt':3000,'lookback_days':3,'trend_lookback_days':S,'return_hurdle':H,'exit_buffer_fraction':0,'start_utc':'2025-10-19T00:01:00Z','end_utc':'2026-10-24T00:01:00Z'}.items())]
 assert len(matches)<=1
 if matches:fp=matches[0];reference(fp)
 else:
  spec=copy.deepcopy(records[ETH]['spec']);name=f'gatejoint370_ETH_N3000_S{S}_L3_H{int(H*100):02d}';spec['name']=name;spec['parameters'].update(trend_lookback_days=S,return_hurdle=H);spec['validation_plan']=rel(R/'plan.json')
  spec['logic']['signal']=spec['logic']['signal'].replace('L1/2/3,H2/4/6percent','L fixed3,H fixed parameters.return_hurdle').replace('S7/14/28','S fixed parameters.trend_lookback_days')
  spec['logic']['allocation']='One ETH10000USDT native bank; fixed entry N3000 =30% initial bank, actual prior-close LOT quantity held unchanged until rule exits. Opening debits fee only; no NAV scaling, transfers, cross-margin, hidden base position or parent rebalance.'
  fp=reg.fingerprint(spec);assert fp not in records
  row={'name':name,'scope':'native','asset':'ETH','role':'candidate','capital_usdt':10000,'fixed_entry_notional_usdt':3000,'trend_lookback_days':S,'lookback_days':3,'return_hurdle':H,'exit_buffer_fraction':0,'fingerprint':fp,'spec':rel(R/'specs'/(name+'.json'))}
  (R/'specs').mkdir(exist_ok=True);put(ROOT/row['spec'],spec);batch.append(row)
 parentmatches=[]
 for pfp,z in records.items():
  s=z.get('spec',{})
  if z.get('result_available') and s.get('kind')=='combination' and sorted((c['fingerprint'],c['weight']) for c in s.get('components',[]))==sorted([(BTC,1),(fp,1)]) and s.get('parameters',{}).get('start_utc')=='2025-10-19T00:01:00Z' and s.get('parameters',{}).get('end_utc')=='2026-10-24T00:01:00Z':parentmatches.append(pfp)
 assert len(parentmatches)<=1
 if parentmatches:pfp=parentmatches[0];reference(pfp)
 else:
  spec=copy.deepcopy(records[PAR]['spec']);name=f'gatejoint370_parent_B1000_E3000_S{S}_L3_H{int(H*100):02d}';spec['name']=name;spec['components']=[{'fingerprint':BTC,'weight':1},{'fingerprint':fp,'weight':1}];spec['parameters'].update(trend_filter_lookback_days=S,ETH_trend_lookback_days=S,reversal_return_hurdle=H,ETH_return_hurdle=H);spec['validation_plan']=rel(R/'plan.json')
  spec['logic']['composition']='One immutable actual BTC L31/H4%/E1%/N1000 bank and ETH L3/zero-exit slow-trend gated reversal S/H from parameters. Each bank10000, parent20000, raw weights[1,1] sum absolute NAV once. Fixed total entry budget4000 (20% parent) is not continual exposure; no parent orders, normalization, transfers or resizing.'
  spec['logic']['native_ETH_rule']=copy.deepcopy((records[fp]['spec'] if fp in records else json.loads((ROOT/batch[-1]['spec']).read_text()))['logic'])
  pfp=reg.fingerprint(spec);assert pfp not in records
  row={'name':name,'scope':'parent','asset':'COMBO','role':'candidate','capital_usdt':20000,'BTC_fixed_entry_notional_usdt':1000,'ETH_fixed_entry_notional_usdt':3000,'trend_filter_lookback_days':S,'reversal_lookback_days':3,'reversal_return_hurdle':H,'source_fingerprints':[BTC,fp],'fingerprint':pfp,'spec':rel(R/'specs'/(name+'.json'))};put(ROOT/row['spec'],spec);batch.append(row)
 grid.extend([{'S':S,'H':H,'scope':'native','fingerprint':fp,'readonly':fp in refs},{'S':S,'H':H,'scope':'parent','fingerprint':pfp,'readonly':pfp in refs}])
assert len(batch)==10 and sum(x['scope']=='native' for x in batch)==5 and len(refs)==9
batch.sort(key=lambda x:(x['scope']=='parent',x['name']))
put(R/'batch.json',batch)
plan={'round':R.name,'frozen_at_utc':now(),'hypothesis':'The slow-trend gate and fast reversal entry hurdle jointly control whipsaw and regime compatibility. Test fixed ETH L3/N3000/S21,28,35 x H1,2,3%; preserve original BTC N1000 component; no direction inversion or post-result axis selection.','grid':grid,'data':base['data'],'time_boundaries':{**base['time_boundaries'],'earliest_ETH_signal_context_close_utc':'2025-09-13T23:59:59.999Z','causality':'S35 earliest denominator explicit day -3 actual close; no future prices; no fitted labels so purge0, close available at UTC00:00 then execution00:01, continuous state through folds.'},'warmup':warm,'read_only_references':refs,'raw_weights':[1,1],'capital_and_notional':'BTC and ETH independent10000 each, parent20000. N1000/N3000 entry budgets=10%/30% own banks,20% combined. Not continuous portfolio weights or risk matching. No normalization, transfers, cross margin or compounding.','new_engine_sha256':sha(R/'engine.py'),'sensitivity':{'axes':{'S':[21,28,35],'H':[.01,.02,.03]},'radius_in_axis_indices':1,'include_center':True,'scope_separate':True,'old_qualification_unchanged':True,'local_3x_positive_required':.6,'local_recent_allcost_six_of_eight_required':.6},'gates':{'all_three_cost_returns_positive':True,'positive_complete30d_1x_min':9,'recent40_allcost_positive':True,'recent5d_positive_EACH_cost_min':6,'DD3_max_pct':25,'local3positive_min':.6,'local_recent_qualifying_min':.6,'native_closing_roundtrips_or_parent_sum_min':4,'gross_plus_funding_to_cost1_min':2.5,'zero_rejections_negative_cash_margin_proxy_violations':True,'terminal_flat':True,'minimum_days':180},'walk_forward':'12 chronological complete30day folds +10day tail, no fold resets, recent40 inherits day330 NAV/state; no OOS tuning. All repeated history is development, not untouched final or future qualification.','costs':records[ETH]['spec']['parameters']['costs'],'risk':records[ETH]['spec']['logic']['risk'],'skills':['walk-forward-validation','ml4t-sensitivity-analysis','ml4t-transaction-costs'],'sources':[{'url':'https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum','access_date':'2026-10-31','scope':'Traditional12month futures own-return persistence background only. Short ETH reversal conditioned on21/28/35-day trend is our unvalidated hypothesis, not a replication/profit claim.'},{'url':'https://fapi.binance.com/fapi/v1/klines','access_date':'2026-10-31','scope':'Actual public closed daily warmup response saved with verified TLS, hashes and exact overlap; developer documentation old URL redirects to catalog, actual payload validation is evidence.'}],'limits':'Linear perpetuals do not assume spot borrow availability. Funding actual settlement/mark/exposure, outflows stressed/inflows unchanged; 1% closed-hour adverse maintenance proxy, not tick historical liquidation, L2/TCA or capacity proof. All negative results retained.'}
put(R/'plan.json',plan)
print(json.dumps({'frozen_new_configs':len(batch),'native':5,'parents':5,'old_native_components':5,'old_parent_results':4,'warmup_overlap_passed':True,'plan_sha256':sha(R/'plan.json')}),flush=True)
