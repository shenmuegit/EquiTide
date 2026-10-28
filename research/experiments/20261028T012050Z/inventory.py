"""Metadata-only exact native-bank and component-pair inventory before new combinations."""
import copy,json,hashlib,sys,itertools
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
records=reg.read_records(ROOT/'research/automation/registry.jsonl');priorpath='research/experiments/20261027T211845Z/plan.json';prior=read(ROOT/priorpath);pool={};btc={};eth={};docs={}
def ref(c,path,scope='native'):
 p=read(ROOT/c['spec'])['parameters'];return {**{k:c[k] for k in ['name','fingerprint','spec','archive','archive_sha256']},'report':path,'report_sha256':sha(ROOT/path),'spec_sha256':sha(ROOT/c['spec']),'asset':'COMBO' if scope=='parent' else c['asset'],'scope':scope,'role':c['role'],'original_status':c['status'],'capital_usdt':20000 if scope=='parent' else 10000,'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()},**{k:c.get(k,p.get(k)) for k in ['fixed_entry_notional_usdt','lookback_days','return_hurdle','exit_buffer_fraction','trend_lookback_days']}}
for fp,x in prior['component_sources'].items():
 if x['asset']=='BTC' and x['fixed_entry_notional_usdt']==1000 and x['lookback_days']==31 and x['exit_buffer_fraction']==.01 and x['return_hurdle'] in [.02,.04,.06]:pool[fp]=copy.deepcopy(x);btc[str(x['return_hurdle'])]=fp
 if x['asset']=='ETH' and x['fixed_entry_notional_usdt']==3000 and x['trend_lookback_days'] in [28,31] and x['lookback_days'] in [3,4,5] and x['return_hurdle']==.02:pool[fp]=copy.deepcopy(x);eth[str([.02,x['trend_lookback_days'],x['lookback_days']])]=fp
path='research/experiments/20261027T231921Z/report.json'
for c in read(ROOT/path)['configs'].values():
 if c['scope']=='native':x=ref(c,path);pool[x['fingerprint']]=x;eth[str([x['return_hurdle'],x['trend_lookback_days'],x['lookback_days']])]=x['fingerprint']
assert len(pool)==21 and len(btc)==3 and len(eth)==18
for fp,x in pool.items():assert records[fp]['result_available'] is True and records[fp]['status']==x['original_status'] and records[fp]['report_sha256']==x['report_sha256'] and sha(ROOT/x['report'])==x['report_sha256'] and sha(ROOT/x['spec'])==x['spec_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256']
seen={}
for fp,rec in records.items():
 sp=rec.get('spec',{});p=sp.get('parameters',{});cc=sp.get('components',[])
 if sp.get('kind')=='combination' and len(cc)==2 and all(z['weight']==1 for z in cc) and p.get('initial_capital_usdt')==20000 and p.get('component_capitals_usdt')==[10000,10000] and p.get('start_utc')==prior['time_boundaries']['oos_start_utc'] and p.get('end_utc')==prior['time_boundaries']['oos_end_exclusive_utc'] and (rec.get('result_available') is True or rec['status']=='reserved'):
  key=tuple(sorted(z['fingerprint'] for z in cc))
  if key not in seen or rec.get('result_available') is True:seen[key]=rec
anchors={};new=[]
for B,H,S,L in itertools.product([.02,.04,.06],[.01,.02,.03],[28,31],[3,4,5]):
 fps=[btc[str(B)],eth[str([H,S,L])]];rec=seen.get(tuple(sorted(fps)))
 if rec:
  assert rec['result_available'] is True and rec['status'] in ['passed','rejected'];p=rec['report']
  if p not in docs:docs[p]=read(ROOT/p)
  x=ref(next(c for c in docs[p]['configs'].values() if c['fingerprint']==rec['fingerprint']),p,'parent');anchors[x['name']]=x
 else:new.append({'BTC_return_hurdle':B,'reversal_return_hurdle':H,'trend_filter_lookback_days':S,'reversal_lookback_days':L,'source_fingerprints':fps})
assert len(anchors)==30 and len(new)==24
holds={'COMBO':copy.deepcopy(prior['read_only_hold_references']['B1000_E3000'])}
put(R/'inventory.json',{'recorded_at_utc':datetime.now(timezone.utc).isoformat(),'registry_sha256_before_reserve':sha(ROOT/'research/automation/registry.jsonl'),'source_plan':priorpath,'source_plan_sha256':sha(ROOT/priorpath),'component_sources':pool,'BTC':btc,'ETH':eth,'read_only_anchor_references':anchors,'read_only_hold_references':holds,'new_pairs':new,'financial_evaluations':0,'semantic_check':'Complete componentfingerprintpair,raw1/1,two10000banks,parent20000,exact370dayboundaries;oldactual/reservedpairsreadonly;noresultblocked/abandonedrecoverable. Differentnames/order/equivalentnumbersarenotnovel.'});print(json.dumps({'native_sources':21,'old_parent_cells':30,'new_passive_parents':24,'full_parent_cells':54,'new_native_models':0,'old_holds':1}),flush=True)
