"""Read exact source and rule metadata only; no performance calculation."""
import copy,hashlib,itertools,json,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text());rel=lambda p:str(p.relative_to(ROOT));put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
records=reg.read_records(ROOT/'research/automation/registry.jsonl');source='research/experiments/20261028T092048Z/plan.json';prior=read(ROOT/source);holds=copy.deepcopy(read(ROOT/'research/experiments/20261028T072053Z/plan.json')['read_only_hold_references']);pool={};controls={};btc=None
for fp,x in prior['component_sources'].items():
 if x['asset']=='BTC' and x['return_hurdle']==.04 and x['fixed_entry_notional_usdt']==1000:btc=copy.deepcopy(x);pool[fp]=btc
 if x['asset']=='ETH' and x['return_hurdle']==.025 and x['fixed_entry_notional_usdt']==3000 and x['trend_lookback_days'] in [27,28,29] and x['lookback_days'] in [3,4]:pool[fp]=copy.deepcopy(x);controls[x['name']]=copy.deepcopy(x)
for x in prior['read_only_anchor_references'].values():
 p=read(ROOT/x['spec'])['parameters']
 if p['BTC_return_hurdle']==.04 and p['ETH_return_hurdle']==.025 and p['ETH_trend_lookback_days'] in [27,28,29] and p['ETH_lookback_days'] in [3,4]:controls[x['name']]=copy.deepcopy(x)
pool[holds['ETH']['fingerprint']]=copy.deepcopy(holds['ETH']);assert btc and len(pool)==8 and len(controls)==12 and len(holds)==2
for x in [*pool.values(),*controls.values(),*holds.values()]:
 z=records[x['fingerprint']];assert z['result_available'] is True and z['status']==x['original_status'] and z['report_sha256']==x['report_sha256'] and sha(ROOT/x['report'])==x['report_sha256'] and sha(ROOT/x['spec'])==x['spec_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256']
new=[]
for S,L in itertools.product([27,28,29],[3,4]):
 matches=[]
 for fp,z in records.items():
  sp=z.get('spec',{});p=sp.get('parameters',{})
  if sp.get('universe')==['ETH/USDT'] and p.get('trend_gate_mode')=='adjacent_horizon_majority' and p.get('trend_lookback_days')==S and p.get('lookback_days')==L and p.get('return_hurdle')==.025 and p.get('exit_buffer_fraction')==0 and p.get('initial_capital_usdt')==10000 and p.get('fixed_entry_notional_usdt')==3000 and p.get('start_utc')==prior['time_boundaries']['oos_start_utc'] and p.get('end_utc')==prior['time_boundaries']['oos_end_exclusive_utc']:matches.append({'fingerprint':fp,'status':z['status'],'result_available':z.get('result_available')})
 assert not any(x['result_available'] is True or x['status']=='reserved' for x in matches);new.append({'S':S,'L':L,'mode':'adjacent_horizon_majority','lookbacks':[S-1,S,S+1],'retryable_missing_results':matches})
put(R/'inventory.json',{'recorded_at_utc':datetime.now(timezone.utc).isoformat(),'registry_sha256_before_reserve':sha(ROOT/'research/automation/registry.jsonl'),'source_plan':source,'source_plan_sha256':sha(ROOT/source),'component_sources':pool,'fixed_BTC':btc,'read_only_anchor_references':controls,'read_only_hold_references':holds,'new_native_metadata':new,'new_native_configs':6,'new_passive_parents':6,'original_single_horizon_controls':12,'unique_old_results':len({x['fingerprint'] for x in [*pool.values(),*controls.values(),*holds.values()]}),'financial_evaluations':0,'novelty':'Real rule change: majority of signs at S-1/S/S+1 vs original single-S ROC. Existingfundingmedian,imputation andspotrollingprice-medianrules differ. Same newmajorityrule/params/assets/capital/datesdeduped;oldsingle-S results readonly,not added to new-rule sensitivity neighbors.'});print('INVENTORY_6_NEW_NATIVE_6_NEW_PARENT_12_OLD_SINGLE_GATE_CONTROLS_15_UNIQUE_OLD_RESULTS',flush=True)
