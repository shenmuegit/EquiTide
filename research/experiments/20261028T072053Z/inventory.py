"""Read complete exact definitions and immutable source metadata; no evaluation."""
import copy,hashlib,itertools,json,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text());rel=lambda p:str(p.relative_to(ROOT))
records=reg.read_records(ROOT/'research/automation/registry.jsonl');source='research/experiments/20261028T032051Z/plan.json';prior=read(ROOT/source);holds=copy.deepcopy(prior['read_only_hold_references']);anchors={}
for x in prior['read_only_anchor_references'].values():
 if x['scope']=='native':S,L=x['trend_lookback_days'],x['lookback_days']
 else:p=read(ROOT/x['spec'])['parameters'];S,L=p['ETH_trend_lookback_days'],p['ETH_lookback_days']
 if S==28 and L in [3,4]:anchors[x['name']]=copy.deepcopy(x)
def ref(c,path):
 p=read(ROOT/c['spec'])['parameters'];return {'name':c['name'],'fingerprint':c['fingerprint'],'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'archive':c['archive'],'archive_sha256':c['archive_sha256'],'report':path,'report_sha256':sha(ROOT/path),'asset':c['asset'],'scope':c['scope'],'role':c['role'],'original_status':c['status'],'capital_usdt':c['capital_usdt'],'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()},**{k:p.get(k) for k in ['fixed_entry_notional_usdt','lookback_days','return_hurdle','exit_buffer_fraction','trend_lookback_days']}}
for stamp,Ss,H in [('20261027T131648Z',[27],.02),('20261027T171814Z',[29],.02),('20261028T032051Z',[28],.025)]:
 path=f'research/experiments/{stamp}/report.json';doc=read(ROOT/path)
 for c in doc['configs'].values():
  p=read(ROOT/c['spec'])['parameters'];scope=c['scope'];S=p.get('trend_lookback_days') if scope=='native' else p.get('ETH_trend_lookback_days');L=p.get('lookback_days') if scope=='native' else p.get('ETH_lookback_days');h=p.get('return_hurdle') if scope=='native' else p.get('ETH_return_hurdle')
  if S in Ss and L in [3,4] and h==H:anchors[c['name']]=ref(c,path)
assert len(anchors)==16 and len({x['fingerprint'] for x in anchors.values()})==16
pool={prior['fixed_BTC']['fingerprint']:copy.deepcopy(prior['fixed_BTC']),holds['ETH']['fingerprint']:copy.deepcopy(holds['ETH'])}
for x in anchors.values():
 if x['scope']=='native':pool[x['fingerprint']]=x
assert len(pool)==10
found={}
for fp,rec in records.items():
 sp=rec.get('spec',{});p=sp.get('parameters',{})
 if sp.get('universe')==['ETH/USDT'] and p.get('initial_capital_usdt')==10000 and p.get('fixed_entry_notional_usdt')==3000 and p.get('lookback_days') in [3,4] and p.get('trend_lookback_days') in [27,28,29] and p.get('exit_buffer_fraction')==0 and p.get('return_hurdle') in [.02,.025] and p.get('start_utc')==prior['time_boundaries']['oos_start_utc'] and p.get('end_utc')==prior['time_boundaries']['oos_end_exclusive_utc']:
  key=(p['return_hurdle'],p['trend_lookback_days'],p['lookback_days']);found.setdefault(key,[]).append({'fingerprint':fp,'status':rec['status'],'result_available':rec.get('result_available'),'report':rec.get('report')})
new=[]
for H,S,L in itertools.product([.025],[27,29],[3,4]):
 matches=found.get((H,S,L),[]);assert not any(x['result_available'] is True or x['status']=='reserved' for x in matches),(H,S,L,matches);new.append({'return_hurdle':H,'trend_lookback_days':S,'lookback_days':L,'missing_result_retries':matches})
for x in [*pool.values(),*anchors.values(),*holds.values()]:
 rec=records[x['fingerprint']];assert rec['result_available'] is True and rec['status']==x['original_status'] and rec['report_sha256']==x['report_sha256'] and sha(ROOT/x['report'])==x['report_sha256'] and sha(ROOT/x['spec'])==x['spec_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256']
out={'recorded_at_utc':datetime.now(timezone.utc).isoformat(),'registry_sha256_before_reserve':sha(ROOT/'research/automation/registry.jsonl'),'source_plan':source,'source_plan_sha256':sha(ROOT/source),'component_sources':pool,'read_only_anchor_references':anchors,'read_only_hold_references':holds,'existing_exact_native_matches':{str(k):v for k,v in found.items()},'new_native_metadata':new,'new_native_configs':4,'new_parent_configs':4,'full_grid_native':12,'full_grid_parent':12,'old_cell_count':16,'financial_evaluations':0,'novelty':'Completeeconomicdefinitions,notnames/family/order. OnlyH2.5S27/29L3/4nativepathsabsentactualresult;old16cellsreadonly. Concreteparentpairscheckedagainbefore reserve.'}
(R/'inventory.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'new_native':4,'new_parent':4,'old_cells':16,'native_sources':10,'unique_old_refs':len({x['fingerprint'] for x in [*pool.values(),*anchors.values(),*holds.values()]}),'financial_evaluations':0}),flush=True)
