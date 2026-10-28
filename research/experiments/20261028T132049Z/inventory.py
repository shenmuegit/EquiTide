"""Exact metadata inventory for new majority-rule entry hurdles; no financial calculation."""
import copy,hashlib,itertools,json,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text());rel=lambda p:str(p.relative_to(ROOT));put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
records=reg.read_records(ROOT/'research/automation/registry.jsonl');source='research/experiments/20261028T112019Z/plan.json';prior=read(ROOT/source);holds=copy.deepcopy(prior['read_only_hold_references']);btc=copy.deepcopy(prior['fixed_BTC']);pool={btc['fingerprint']:btc,holds['ETH']['fingerprint']:copy.deepcopy(holds['ETH'])};anchors={};path='research/experiments/20261028T112019Z/report.json'
for c in read(ROOT/path)['configs'].values():
 p=read(ROOT/c['spec'])['parameters'];x={'name':c['name'],'fingerprint':c['fingerprint'],'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'archive':c['archive'],'archive_sha256':c['archive_sha256'],'report':path,'report_sha256':sha(ROOT/path),'scope':c['scope'],'asset':c['asset'],'role':c['role'],'capital_usdt':c['capital_usdt'],'original_status':c['status'],'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()},**{k:p.get(k) for k in ['fixed_entry_notional_usdt','lookback_days','return_hurdle','exit_buffer_fraction','trend_lookback_days']}}
 anchors[x['name']]=x
 if c['scope']=='native':assert p['trend_gate_mode']=='adjacent_horizon_majority' and p['return_hurdle']==.025;pool[x['fingerprint']]=x
assert len(pool)==8 and len(anchors)==12 and len(holds)==2
for x in [*pool.values(),*anchors.values(),*holds.values()]:
 z=records[x['fingerprint']];assert z['result_available'] is True and z['status']==x['original_status'] and z['report_sha256']==x['report_sha256'] and sha(ROOT/x['report'])==x['report_sha256'] and sha(ROOT/x['spec'])==x['spec_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256']
new=[]
for H,S,L in itertools.product([.02,.03],[27,28,29],[3,4]):
 matches=[]
 for fp,z in records.items():
  sp=z.get('spec',{});p=sp.get('parameters',{})
  if sp.get('universe')==['ETH/USDT'] and p.get('trend_gate_mode')=='adjacent_horizon_majority' and p.get('trend_lookback_days')==S and p.get('lookback_days')==L and p.get('return_hurdle')==H and p.get('exit_buffer_fraction')==0 and p.get('initial_capital_usdt')==10000 and p.get('fixed_entry_notional_usdt')==3000 and p.get('start_utc')==prior['time_boundaries']['oos_start_utc'] and p.get('end_utc')==prior['time_boundaries']['oos_end_exclusive_utc']:matches.append({'fingerprint':fp,'status':z['status'],'result_available':z.get('result_available')})
 assert not any(x['result_available'] is True or x['status']=='reserved' for x in matches);new.append({'H':H,'S':S,'L':L,'retryable_missing_result_matches':matches})
put(R/'inventory.json',{'recorded_at_utc':datetime.now(timezone.utc).isoformat(),'registry_sha256_before_reserve':sha(ROOT/'research/automation/registry.jsonl'),'source_plan':source,'source_plan_sha256':sha(ROOT/source),'component_sources':pool,'fixed_BTC':btc,'read_only_anchor_references':anchors,'read_only_hold_references':holds,'new_native_metadata':new,'new_native_configs':12,'new_passive_parents':12,'existing_same_majority_H025_cells':12,'unique_old_results':15,'financial_evaluations':0,'novelty':'Same actual adjacent-horizon-majority rule,entryH2/3percent are new concrete parameters. H2.5old6native+6parentcells readonly. Earlier single-S H2/3rules differ. No name/order/number-format novelty.'});print('INVENTORY_12_NEW_NATIVE_12_NEW_PARENT_12_OLD_H025_MAJORITY_CELLS_15_OLD_UNIQUE_RESULTS',flush=True)
