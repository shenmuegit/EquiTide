"""After-current, before-future definition lookup only; no strategy, money or account execution."""
import copy,hashlib,itertools,json,sys
from decimal import Decimal
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rel=lambda p:str(p.relative_to(ROOT));put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');b=rd(R/'next_definition_followup_binding.json');assert b['bound_before_readonly_execution'] and sha(Path(__file__))==b['source_sha256'] and b['after_current_financial_evaluation_before_any_future_reservation']
for path,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/path)==h
prior=rd(R/'next_parameter_availability.json');assert prior['first_definition_only_available_batch'] is None and prior['batches'][0]['new_graphs']==0 and prior['batches'][0]['old_graphs']==9
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');before={rel(p):sha(p) for p in reg._ledger_paths(ROOT/'research/automation/registry.jsonl') if p.exists()};inv=rd(R/'source_inventory.json');ignored={'persistence','prior_370day_source_fingerprint'}
def key(xs):
 d={}
 for x in xs:d[x['fingerprint']]=d.get(x['fingerprint'],Decimal(0))+Decimal(str(x['weight']))
 return tuple(sorted(d.items()))
index={}
for fp,z in rs.items():
 q=z.get('spec',{}).get('parameters',{});sp=z.get('spec',{})
 if sp.get('kind')=='combination' and q.get('start_utc')=='2025-10-19T00:01:00Z' and q.get('end_utc')=='2026-11-14T00:01:00Z' and (z.get('result_available') or z.get('status')=='reserved'):index.setdefault(key(sp['components']),[]).append(fp)
def sources(asset,axis,values):
 base=inv['assets'][asset]['baseline_parameters'];out={}
 for v in values:
  xs=[x for x in inv['assets'][asset]['rows'] if x['parameters'].get(axis)==v and all(x['parameters'].get(k)==base.get(k) for k in set(base)|set(x['parameters']) if k not in ignored|{axis})]
  if len(xs)!=1:return None
  x=xs[0];z=rs[x['fingerprint']];assert z['result_available'] and z['report_sha256']==x['report_sha256']==sha(ROOT/x['report']);out[v]=x['fingerprint']
 return out
rows=[];first=None
for preset in b['priorities_fixed_before_this_definition_lookup']:
 ba,bv,ea,ev=preset['BTC_axis'],preset['BTC_values'],preset['ETH_axis'],preset['ETH_values'];BTC=sources('BTC',ba,bv);ETH=sources('ETH',ea,ev)
 if BTC is None or ETH is None:rows.append({**preset,'all_fixed_context_sources_available':False,'new_evaluations':0});continue
 cells=[{'BTC_value':w,'ETH_value':k,'BTC':BTC[w],'ETH':ETH[k],'existing_exact_graphs':index.get(key([{'fingerprint':BTC[w],'weight':1},{'fingerprint':ETH[k],'weight':1}]),[])} for w,k in itertools.product(bv,ev)]
 item={**preset,'all_fixed_context_sources_available':True,'BTC_sources':BTC,'ETH_sources':ETH,'cells':cells,'new_graphs':sum(not x['existing_exact_graphs'] for x in cells),'old_graphs':sum(bool(x['existing_exact_graphs']) for x in cells),'raw_bank_multipliers':[1,1],'capital_usdt':[3750,15000],'entry_notionals_usdt':[1000,4000],'representative_before_any_future_outcomes':{'BTC_value':bv[0],'ETH_value':ev[0]},'new_financial_or_account_evaluations':0};rows.append(item)
 if item['new_graphs'] and first is None:first=item
assert before=={rel(p):sha(p) for p in reg._ledger_paths(ROOT/'research/automation/registry.jsonl') if p.exists()} and len(events)==len(reg.read_events(ROOT/'research/automation/registry.jsonl'))
for path,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/path)==h
out={'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'bound_source_sha256':b['source_sha256'],'prior_predeclared_batch_exhausted_all9_actual_graphs':True,'prior_metadata_source':rel(R/'next_parameter_availability.json'),'prior_metadata_sha256':sha(R/'next_parameter_availability.json'),'timing':'Declared after current completed outcomes, solely by definition availability; before any future reservation or future outcomes. Does not replace the pre-current declaration or alter the current batch.','current_performance_used_for_selection':False,'complete_canonical_component_index_built_before_lookup':True,'registry_IDs_read':len(rs),'registry_events_read':len(events),'attempts_in_bound_definition_priority_order':rows,'first_definition_only_available_batch':first,'all_ledger_bytes_and_current_financial_account_reports_unchanged':True,'new_financial_account_cashflow_or_configuration_evaluations':0,'required_next_action':'Refresh full registry and actual sources, freeze complete future specs/parameters/weights/failure criteria, then successful reserve before any future calculation.'};put(R/'next_definition_followup.json',out)
summary={k:first[k] for k in ['BTC_axis','BTC_values','ETH_axis','ETH_values','new_graphs','old_graphs']} if first else None
text='事前拟定的下一批BTC入场阈值.0275/.03/.0325 × ETH趋势滞后2/3/4天已有9格真实结果，next_parameter_availability.json返回空候选；未重算，也不将旧结果当新结果。此补充在本轮结果完成后、任何未来reserve前，按预先写入本脚本绑定的定义优先次序查询，不使用收益排序，不修改本轮代表/参数网格、原账户或原有交接状态。\n\n首个定义可用批次：'+json.dumps(summary,ensure_ascii=False)+'。完整来源指纹、其他固定参数、已测/未测格见next_definition_followup.json；下一轮须重新读取完整登记，固定完整spec并reserve成功，才能计算。此处0新策略/账户/现金流评估。\n';(R/'next_definition_followup.md').write_text(text)
p=R/'result.md';p.write_text(p.read_text()+'\n后续定义补充：'+text)
print(json.dumps({'passed':True,'original_next_batch_new_graphs':0,'first_followup':summary,'new_evaluations':0},ensure_ascii=False))
