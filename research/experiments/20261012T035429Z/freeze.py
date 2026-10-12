"""Freeze the complete allocation × ETH-entry grid, reserve every fresh definition, then permit calculation."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal as D
import copy,hashlib,json,subprocess,sys
T=Path(__file__).resolve().parent;ROOT=T.parents[2]
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sys.path.insert(0,str(T));from design import definitions,BTC_WEIGHTS,ETH_ENTRIES,eth_weight,allocations
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
prior=json.loads(__import__('gzip').decompress((T/'prior_summary.json.gz').read_bytes()));records=registry.read_records(ROOT/'research/automation/registry.jsonl');canonical={registry.fingerprint(v['spec']):v for v in records.values()}
assert not [v for v in records.values() if v.get('status')=='reserved']
base=json.loads((ROOT/'research/experiments/20261012T015432Z/spec.json').read_text())
plan=copy.deepcopy(base);plan['round']=T.name;plan['trigger_utc']='2026-10-12T03:54:29.198Z';plan['frozen_at_utc']=datetime.now(timezone.utc).isoformat();plan['prior_canonical_trials']=len(canonical);plan['development_history_reused']=True
plan['direction']={'before_new_calculation':True,'parameter_family':'initial BTC/ETH capital allocation × ETH EMA entry threshold','BTC_rule':'Frozen BTC volume-confirmed close-channel15/30; EMA15 entry1%,exit3%;quote-volume lookback40,minimum1.1.','ETH_rule':'Frozen close-channel15/30 and recursive EMA34 asymmetric entry band;exit0.5%.','grid':'BTC initial weight .45/.50/.55/.60/.65 and ETH EMA entry .75/1/1.25/1.5/1.75%; ETH weight is exact complement, capital total $2000. Two reused 180-day windows 2025 and 2026.','focus_before_results':{'BTC_initial_weight':0.50,'ETH_initial_weight':0.50,'ETH_EMA_entry_band_fraction':0.0125},'interpretation':'Expand predeclared two-axis grid outward from R48; all prior histories are reused development/validation, not independent final holdout. Exact existing definitions are read-only; changed weights/entry bands get independently reserved, independently capital-costed components.','no_paper10_changes':True}
plan['hypothesis']='A broad allocation/entry plateau may persist at lower and higher ETH initial fractions; no improvement assumed. The fixed middle allocation/entry remains the named comparator, and all parameter/weight variants are predeclared before new calculations.'
plan['grid']={**plan['grid'],'BTC_initial_weights':BTC_WEIGHTS,'ETH_initial_weights':[eth_weight(w) for w in BTC_WEIGHTS],'ETH_EMA_entry_band_fraction':ETH_ENTRIES,'initial_funds_by_BTC_weight':{str(w):allocations(w)for w in BTC_WEIGHTS},'predeclared_focus':{'BTC_initial_weight':0.50,'ETH_EMA_entry_band_fraction':0.0125}}
plan['allocation']='Raw BTC initial fractions [.45,.50,.55,.60,.65]; ETH is exact decimal complement [.55,.50,.45,.40,.35]. Total fixed at $2000 per portfolio. Actual starting sleeve USDT [900/1100,1000/1000,1100/900,1200/800,1300/700]. No normalization, maintenance of target weights, transfers, or rebalance. Each changed component is simulated from its own cash budget.'
plan['sensitivity']={'axes':['BTC_initial_weight','ETH_EMA_entry_band_fraction'],'BTC_initial_weights':BTC_WEIGHTS,'ETH_EMA_entry_band_fraction':ETH_ENTRIES,'ETH_EMA_span_days_fixed':34,'ETH_exit_band_fixed':0.005,'BTC_rules_fixed':True,'cells_per_period':25,'groups':['BTC component','ETH component','summed BTC/ETH portfolio'],'note':'Predeclared full 5x5 grid; descriptive sensitivity on repeatedly reused development histories only, not an independent final test.'}
plan['full_grid_configs']=110;plan['read_only_configs']=42;plan['new_configs']=68;plan['new_BTC_components']=4;plan['new_ETH_components']=32;plan['new_component_configs']=36;plan['new_combination_configs']=32;plan['new_cost_scenes']=204
plan['read_only_component_refs']=[];plan['read_only_grid_refs']=[];plan['read_only_comparators']=base['read_only_comparators'];plan['read_only_comparator_refs']=base['read_only_comparator_refs'];plan['read_only_background_refs']=base['read_only_background_refs']
plan['source_research_round']='20261012T015432Z';plan['paper10_state_sha256']=sha(ROOT/'research/paper10/state.json');plan['paper10_plan_sha256']=sha(ROOT/'research/paper10/plan.json')
plan['preflight_sha256']=sha(T/'preflight.py');plan['frozen_setup_sha256']=sha(T/'freeze.py')
plan['new_code_sha256']={n:sha(T/n)for n in ['design.py','evaluate.py','audit.py','signals.py','volume_signals.py','volume_ema_signals.py']}
plan['source_registry_sha256_before_reserve']=sha(ROOT/'research/automation/registry.jsonl');plan['source_registry_rows_before_reserve']=sum(1 for _ in (ROOT/'research/automation/registry.jsonl').open())
all_defs=definitions(registry.fingerprint);assert len(all_defs)==110
fresh=[];old=[];grid=[]
for sp,fields in all_defs:
 fp=registry.fingerprint(sp)
 if fp in canonical:
  rec=canonical[fp];assert rec.get('result_available') and rec.get('report')
  rp=ROOT/rec['report'];assert sha(rp)==rec['report_sha256'];report=json.loads(rp.read_text())
  name=next((n for n,c in report['configs'].items()if c.get('fingerprint')==fp),None);assert name
  c=report['configs'][name];archive=c.get('archive');assert archive and sha(ROOT/archive)==c['archive_sha256']
  ref={'source_round':rp.parent.name,'report':rec['report'],'report_sha256':rec['report_sha256'],'archive':archive,'archive_sha256':c['archive_sha256'],'spec':c.get('spec'),'spec_sha256':sha(ROOT/c['spec'])}
  row={'name':name,'fingerprint':fp,'spec':c['spec'],'source_ref':ref,'is_new':False,**fields}
  if fields['role']=='component':plan['read_only_component_refs'].append({'name':name,'fingerprint':fp,'year':fields['year'],'asset':fields['asset'],'capital_usdt':fields['capital_usdt'],**ref})
  else:plan['read_only_grid_refs'].append({'name':name,'fingerprint':fp,'year':fields['year'],'capital_usdt':2000,**ref})
  old.append(row)
 else:
  path=T/'specs'/(sp['name']+'.json');path.write_text(json.dumps(sp,ensure_ascii=False,indent=2)+'\n');rel=str(path.relative_to(ROOT))
  row={'name':sp['name'],'fingerprint':fp,'spec':rel,'source_ref':None,'is_new':True,**fields};fresh.append((row,sp))
 grid.append(row)
assert len(fresh)==68 and len(old)==42 and len(plan['read_only_component_refs'])==24 and len(plan['read_only_grid_refs'])==18
plan['read_only_component_configs']=24;plan['read_only_grid_portfolios']=18
plan['novelty']={'new':len(fresh),'read_only':len(old),'new_BTC_components':sum(x['role']=='component'and x.get('asset')=='BTC'for x,_ in fresh),'new_ETH_components':sum(x['role']=='component'and x.get('asset')=='ETH'for x,_ in fresh),'new_combinations':sum(x['role']=='combination'for x,_ in fresh),'all_variant_weights_sum_exact':True}
# Exact component/portfolio claims after the complete grid is frozen.
plan['complete_rules']['allocation']=plan['allocation']
# These source hashes are tied to immutable historical inputs already pinned by R48.
(T/'spec.json').write_text(json.dumps(plan,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
(T/'grid_batch.json').write_text(json.dumps(grid,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
(T/'batch.json').write_text(json.dumps([x for x,_ in fresh],ensure_ascii=False,sort_keys=True,indent=2)+'\n')
# All specs and the full grid exist before the first reserve; definitions are component-first.
for row,sp in fresh:
 assert registry.fingerprint(json.loads((ROOT/row['spec']).read_text()))==row['fingerprint']
# Assert source/plan sizes and one-dimensional exact budgets before freezing reservations.
assert [allocations(w)for w in BTC_WEIGHTS]==[[900,1100],[1000,1000],[1100,900],[1200,800],[1300,700]]
assert all(D(str(w))+D(str(eth_weight(w)))==D(1)for w in BTC_WEIGHTS)
(T/'freeze_summary.json').write_text(json.dumps({'frozen_at_utc':plan['frozen_at_utc'],'base_head':prior['base_head'],'base_tree':prior['base_tree'],'source_registry_sha256':plan['source_registry_sha256_before_reserve'],'source_registry_rows':plan['source_registry_rows_before_reserve'],'full_grid':110,'new':68,'readonly':42,'new_components':36,'new_combinations':32,'new_scenes':204,'weights_and_budgets':{str(w):allocations(w)for w in BTC_WEIGHTS},'entries':ETH_ENTRIES,'all_specs_written_before_reserve':True},indent=2)+'\n')
# Reserve components then portfolios. Registry enforces every component exists before its dependent combination.
with(T/'reserve.log').open('w')as log:
 for row,_ in fresh:
  r=subprocess.run([sys.executable,'research/automation/registry.py','reserve',row['spec']],cwd=ROOT,capture_output=True,text=True)
  log.write(row['name']+' '+str(r.returncode)+' '+r.stdout.strip()+'\n'+r.stderr);log.flush()
  if r.returncode:raise RuntimeError('reserve failed: '+row['name']+' '+r.stdout+r.stderr)
print(json.dumps({'reserved':len(fresh),'readonly':len(old),'grid':len(grid),'spec_sha256':sha(T/'spec.json')}))
