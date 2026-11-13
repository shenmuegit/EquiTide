"""Freeze six genuinely new pairings and three exact read-only cells before calculation."""
import copy,itertools,json
from common import *
P=ROOT/'research/experiments/20261113T033939Z';A=ROOT/'research/experiments/20261112T233703Z';old=json.loads((P/'plan.json').read_text());annual=json.loads((A/'plan.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');refs={}
def ref(fp):
 if fp in refs:return
 z=rs[fp];assert z['result_available'] and sha(ROOT/z['report'])==z['report_sha256'];c=next(x for x in json.loads((ROOT/z['report']).read_text())['configs'].values() if x['fingerprint']==fp);sp=z['spec'];scope='native' if sp['kind']=='strategy' else 'parent';d={k:c[k] for k in ['name','fingerprint','spec','archive','archive_sha256']};d.update(scope=scope,asset=sp['universe'][0].split('/')[0] if scope=='native' else 'COMBO',capital_usdt=sp['parameters']['initial_capital_usdt'],report=z['report'],report_sha256=z['report_sha256'],spec_sha256=sha(ROOT/c['spec']),status=z['status']);assert sha(ROOT/d['archive'])==d['archive_sha256'];refs[fp]=d
 if scope=='parent':
  d.update(source_fingerprints=[x['fingerprint'] for x in sp['components']],raw_weights=[x['weight'] for x in sp['components']])
  for x in sp['components']:ref(x['fingerprint'])
BTC={g['W']:g['source_fingerprints'][0] for g in old['grid'] if g['K']==.01};ETH={g['R']:g['source_fingerprints'][1] for g in annual['grid'] if g['BVC']==.04};hold=annual['benchmark_parent_fingerprint'];ref(hold)
for fp in [*BTC.values(),*ETH.values()]:ref(fp)
rules=copy.deepcopy(old['rules']);rules.update(signal={'BTC':'Read-only389day C3750/N1000 L29/H.03/E.01,V10cap.04;new/reversed-only ETHsame-direction ROC confirmation W3/7/14 and fixedK.01.','ETH':'Read-only389day C15000/N4000 L5/H.02/E.0075,S16beta15/17,D3strictK.0075,V6cap.05625;median4pasteligiblefundrates ages1..36h,available<=signal;budget min(.0002,R[.00875,.01,.01125]*VW8samplelogvol*latestactualintervalhours/24).'},allocation='Raw[1,1] independent complete BTC3750 and ETH15000 actualbanks,total18750;no normalization,NAVscaling,transfers,rebalancing,parentorders,crossmargin or resized native quantities.',validation='Fixed full3x3W versus ETHR grid;middleR.01 cells alreadytested and read-only. Sixoff-middle genuine newpairings only. Continuous389days,13folds,recent40/extension19 and all original qualification gates unchanged. Repeatedhistoricalvalidation,notuntouchedfinal orindependentfuture.')
axes={'CROSS_W':[3,7,14],'FUND_R':[.00875,.01,.01125]};batch=[];grid=[];dedup=[];(R/'specs').mkdir(exist_ok=True)
template=rs[old['grid'][0]['fingerprint']]['spec']
for W,F in itertools.product(axes['CROSS_W'],axes['FUND_R']):
 fps=[BTC[W],ETH[F]];matches=[]
 for fp,z in rs.items():
  sp=z.get('spec',{});cs=sp.get('components',[])
  if len(cs)==2 and {q['fingerprint']:float(q['weight']) for q in cs}=={fps[0]:1.,fps[1]:1.} and sp.get('parameters',{}).get('end_utc')=='2026-11-12T00:01:00Z' and sp.get('parameters',{}).get('initial_capital_usdt')==18750:matches.append(fp)
 row=dict(scope='parent',role='candidate',asset='COMBO',capital_usdt=18750,NB=1000,NE=4000,source_fingerprints=fps,W=W,F=F)
 if matches:
  assert F==.01 and len(matches)==1;fp=matches[0];ref(fp);row.update(name=refs[fp]['name'],fingerprint=fp,spec=refs[fp]['spec'],readonly=True);dedup.append({'W':W,'F':F,'fingerprint':fp,'reason':'Exact component fingerprints/rawweights/C/calendar already have actual result; no reservation or recomputation'})
 else:
  assert F!=.01;sp=copy.deepcopy(template);name=f'crosscarry389_W{W}_R{int(F*1000000)}ppm';sp.update(name=name,family='cross-confirmation-carry-passive-bank-pairing',components=[{'fingerprint':f,'weight':1} for f in fps],logic=rules,validation_plan=rel(R/'plan.json'));sp['parameters'].update(entry_cross_asset_window_days=W,entry_cross_asset_minimum_signed_return=.01,ETH_entry_funding_volatility_ratio=F,source_component_spec_sha256=[refs[f]['spec_sha256'] for f in fps],BTC_existing_actual_bank_reused=True,ETH_existing_actual_bank_reused=True,BTC_new_native_quantity_and_impact_computed=False,ETH_new_native_quantity_and_impact_computed=False,actual_native_quantity_and_impact_reused=True);path=R/'specs'/(name+'.json');put(path,sp);fp=reg.fingerprint(sp);assert fp not in rs;row.update(name=name,fingerprint=fp,spec=rel(path),readonly=False);batch.append(row)
 grid.append(row)
assert len(batch)==6 and len(dedup)==3 and len(refs)==12 and sum(x['scope']=='native' for x in refs.values())==8
p={k:copy.deepcopy(old[k]) for k in ['limits','sources','data','time_boundaries','qualification_gates']};p.update(round=R.name,frozen_at_utc=now(),hypothesis='Different existing BTC cross-confirmation windows and ETH carry budgets may have complementary realized paths; genuine new combinations reuse actual native NAV, no sourcepolicy rerun or OOSselection.',rules=rules,axes=axes,grid=grid,native_grid=[],benchmark_parent_fingerprint=hold,read_only_references=refs,representative_preset={'W':7,'F':.00875},bank_capitals_usdt=[3750,15000],fixed_entry_notionals_usdt=[1000,4000],raw_component_weights=[1,1],expected_counts=dict(new_configs=6,new_native=0,new_parents=6,new_candidate_configs=6,new_benchmark_configs=0,new_source_components=0,new_cost_scenes=18,read_only_unique_results=12,grid_cells=9,read_only_grid_cells=3),sensitivity={'axes':['CROSS_W','FUND_R'],'index_radius':1,'local_positive3_min':.6,'local_recent_allcost6of8_min':.6},prior_report={'path':rel(P/'report.json'),'sha256':sha(P/'report.json')},primary_source_reads=[{'url':'https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data','access_utc_date':now()[:10],'browsed':True}],deduplication=dedup)
for n,z in [('plan.json',p),('spec.json',p),('batch.json',batch)]:put(R/n,z)
put(R/'novelty_before_reservation.json',{'passed':True,'registry_IDs_scanned':len(rs),'new_pairings':6,'existing_exact_cells_read_only':dedup,'no_native_strategy_trials':True,'weights_preserved':[1,1]})
print('PASS6newpairings+3exactread-onlycells,8actualnativebanks/12uniquerefs;0newvaluation')
