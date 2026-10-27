"""Read complete exact native definitions and source-pair metadata before evaluating thresholds."""
import copy,json,hashlib,sys,itertools
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text());rel=lambda p:str(p.relative_to(ROOT))
records=reg.read_records(ROOT/'research/automation/registry.jsonl');prior=read(ROOT/'research/experiments/20261027T171814Z/plan.json');pool=copy.deepcopy(prior['component_sources']);anchors=copy.deepcopy(prior['read_only_anchor_references']);holds=copy.deepcopy(prior['read_only_hold_references']);found={};other=[]
for fp,rec in records.items():
 sp=rec.get('spec',{});p=sp.get('parameters',{})
 if sp.get('universe')==['ETH/USDT'] and p.get('initial_capital_usdt')==10000 and p.get('fixed_entry_notional_usdt')==3000 and p.get('lookback_days') in [3,4,5] and p.get('trend_lookback_days') in [28,31] and p.get('exit_buffer_fraction')==0 and p.get('return_hurdle') in [.01,.02,.03] and p.get('start_utc')==prior['time_boundaries']['oos_start_utc'] and p.get('end_utc')==prior['time_boundaries']['oos_end_exclusive_utc']:
  key=(p['return_hurdle'],p['trend_lookback_days'],p['lookback_days']);found.setdefault(key,[]).append({'fingerprint':fp,'status':rec['status'],'result_available':rec.get('result_available'),'report':rec.get('report')})
new=[]
for H,S,L in itertools.product([.01,.03],[28,31],[3,4,5]):
 matches=found.get((H,S,L),[]);assert not any(x['result_available'] is True or x['status']=='reserved' for x in matches),(H,S,L,matches);new.append({'return_hurdle':H,'trend_lookback_days':S,'lookback_days':L,'missing_result_retries':matches})
assert len(new)==12 and len(pool)==8 and len(anchors)==12 and len(holds)==2
for fp,x in pool.items():
 assert records[fp]['result_available'] is True and records[fp]['report_sha256']==x['report_sha256'] and sha(ROOT/x['report'])==x['report_sha256'] and sha(ROOT/x['spec'])==x['spec_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256']
for S,L in itertools.product([28,31],[3,4,5]):assert any(x['result_available'] is True for x in found[.02,S,L])
out={'recorded_at_utc':datetime.now(timezone.utc).isoformat(),'registry_sha256_before_reserve':sha(ROOT/'research/automation/registry.jsonl'),'source_plan':'research/experiments/20261027T171814Z/plan.json','source_plan_sha256':sha(ROOT/'research/experiments/20261027T171814Z/plan.json'),'component_sources':pool,'read_only_anchor_references':anchors,'read_only_hold_references':holds,'existing_exact_native_matches':{str(k):v for k,v in found.items()},'new_native_metadata':new,'new_native_configs':12,'new_parent_configs':12,'full_grid_native':18,'full_grid_parent':18,'old_cell_count':12,'financial_evaluations':0,'novelty':'Complete realrule/parameters/asset/capital/boundary metadata,notnames/family/order. Only H1/H3 absentactualnativepaths advance;existingH2cells readonly. Parentpairs audited again afterconcretespecgeneration before reserve.'}
(R/'inventory.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'new_native':12,'new_parents':12,'old_cells':12,'native_sources':8,'hold_controls':2,'financial_evaluations':0}),flush=True)
