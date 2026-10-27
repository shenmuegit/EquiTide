"""Inventory exact quantity-specific native models and existing raw-bank pairs; no evaluation."""
import copy,gzip,hashlib,json,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text());rel=lambda p:str(p.relative_to(ROOT));put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
records=reg.read_records(ROOT/'research/automation/registry.jsonl');prior=read(ROOT/'research/experiments/20261027T191814Z/plan.json');pool={};btc={};eth={};docs={}
def ref(c,path,scope='native'):
 p=read(ROOT/c['spec'])['parameters'];return {**{k:c[k] for k in ['name','fingerprint','spec','archive','archive_sha256']},'report':path,'report_sha256':sha(ROOT/path),'spec_sha256':sha(ROOT/c['spec']),'asset':'COMBO' if scope=='parent' else c['asset'],'scope':scope,'role':c['role'],'original_status':c['status'],'capital_usdt':20000 if scope=='parent' else 10000,'NAV_sha256_by_cost':{k:z['NAV_sha256_f64le'] for k,z in c['scenes'].items()},**{k:c.get(k,p.get(k)) for k in ['fixed_entry_notional_usdt','lookback_days','return_hurdle','exit_buffer_fraction','trend_lookback_days']}}
def addbtc(fp,x):
 if x['asset']=='BTC' and x['role']=='candidate' and x['fixed_entry_notional_usdt'] in [1000,2000,3000] and x['lookback_days']==31 and x['exit_buffer_fraction']==.01 and x['return_hurdle'] in [.02,.04,.06]:pool[fp]=copy.deepcopy(x);btc[str([x['fixed_entry_notional_usdt'],x['return_hurdle']])]=fp
for rnd in ['20261027T051247Z','20261027T071317Z','20261027T191814Z']:
 for fp,x in read(ROOT/f'research/experiments/{rnd}/plan.json')['component_sources'].items():addbtc(fp,x)
path='research/experiments/20261025T065405Z/report.json'
for c in read(ROOT/path)['configs'].values():
 if c.get('asset')=='BTC' and c['role']=='candidate':
  x=ref(c,path);addbtc(x['fingerprint'],x)
for fp,x in prior['component_sources'].items():
 if x['asset']=='ETH' and x['role']=='candidate' and x['fixed_entry_notional_usdt']==3000 and x['return_hurdle']==.02 and x['lookback_days'] in [3,4,5] and x['trend_lookback_days'] in [28,29,30,31]:pool[fp]=copy.deepcopy(x);eth[str([x['trend_lookback_days'],x['lookback_days']])]=fp
assert len(btc)==9 and len(eth)==12 and len(pool)==21,(len(btc),len(eth),len(pool))
for fp,x in pool.items():
 assert sha(ROOT/x['spec'])==x['spec_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256'] and sha(ROOT/x['report'])==x['report_sha256'] and records[fp]['status']==x['original_status'] and records[fp]['result_available'] is True and records[fp]['report_sha256']==x['report_sha256']
seen={}
for fp,rec in records.items():
 sp=rec.get('spec',{});p=sp.get('parameters',{});cc=sp.get('components',[])
 if sp.get('kind')=='combination' and len(cc)==2 and all(z['weight']==1 for z in cc) and p.get('initial_capital_usdt')==20000 and p.get('component_capitals_usdt')==[10000,10000] and p.get('start_utc')==prior['time_boundaries']['oos_start_utc'] and p.get('end_utc')==prior['time_boundaries']['oos_end_exclusive_utc'] and (rec.get('result_available') is True or rec['status']=='reserved'):
  pair=tuple(sorted(z['fingerprint'] for z in cc));old=seen.get(pair)
  if old is None or rec.get('result_available') is True:seen[pair]=rec
def oldref(rec):
 assert rec['result_available'] is True and rec['status'] in ['passed','rejected'];path=rec['report']
 if path not in docs:docs[path]=read(ROOT/path)
 return ref(next(c for c in docs[path]['configs'].values() if c['fingerprint']==rec['fingerprint']),path,'parent')
anchors={};new=[]
for B in [1000,2000,3000]:
 for H in [.02,.04,.06]:
  for S in [28,29,30,31]:
   for L in [3,4,5]:
    fps=[btc[str([B,H])],eth[str([S,L])]];rec=seen.get(tuple(sorted(fps)))
    if rec:x=oldref(rec);anchors[x['name']]=x
    else:new.append({'BTC_fixed_entry_notional_usdt':B,'BTC_return_hurdle':H,'trend_filter_lookback_days':S,'reversal_lookback_days':L,'source_fingerprints':fps})
assert len(anchors)==48 and len(new)==60,(len(anchors),len(new))
holds={}
for name,x in read(ROOT/'research/experiments/20261027T071317Z/plan.json')['read_only_hold_references'].items():
 p=read(ROOT/x['spec'])['parameters']
 if p['BTC_fixed_entry_notional_usdt'] in [1000,2000,3000] and p['ETH_fixed_entry_notional_usdt']==3000:holds['B'+str(p['BTC_fixed_entry_notional_usdt'])+'_E3000']=copy.deepcopy(x)
assert len(holds)==3
put(R/'inventory.json',{'recorded_at_utc':datetime.now(timezone.utc).isoformat(),'registry_sha256_before_reserve':sha(ROOT/'research/automation/registry.jsonl'),'source_plan':'research/experiments/20261027T191814Z/plan.json','source_plan_sha256':sha(ROOT/'research/experiments/20261027T191814Z/plan.json'),'component_sources':pool,'BTC':btc,'ETH':eth,'read_only_anchor_references':anchors,'read_only_hold_references':holds,'new_pairs':new,'financial_evaluations':0,'semantic_check':'Complete componentfingerprintpair,raw1/1,two10000banks,parent20000,exact370dayboundaries. Completedandreservedpairs readonly;abandoned/noresult remainrecoverable. Names/family/order/numberformat do notcreate novelty.'});print(json.dumps({'native_components':len(pool),'old_parent_cells':len(anchors),'new_parent_configs':len(new),'full_grid_cells':108,'new_native_models':0,'old_hold_controls':3}),flush=True)
