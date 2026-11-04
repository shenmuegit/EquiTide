"""Preset minimum finite-EWM slope strength K and lag D; old controls are read only."""
import copy,itertools,json
from common import *
P=ROOT/'research/experiments/20261104T081405Z'
prior=json.loads((P/'plan.json').read_text())
oldreport=json.loads((P/'report.json').read_text())
records=reg.read_records(ROOT/'research/automation/registry.jsonl')
inventory=json.loads((R/'source_inventory_before_freeze.json').read_text())
assert not inventory['possible_existing_definitions']
Ks=[.001,.002,.003];Ds=[1,3,5];S=24
BTC='3eb8a6c512d66cb8cbc91ecbe84d0979bcb0141f3473dc4cbd250a1d00e865a5'
HOLD='a63ddc9c9bf7d21a06252319821d1a3e63486884f686a1b0f7a2181dfc855f90'
controls={scope:{str(c['D']):c['fingerprint'] for c in oldreport['configs'].values() if c['scope']==scope and c['S']==24} for scope in ['native','parent']}
assert all(len(v)==3 for v in controls.values())
refs={}
def reference(fp):
 if fp in refs:return
 z=records[fp];assert z['result_available'] and sha(ROOT/z['report'])==z['report_sha256']
 sp=z['spec'];c=next(x for x in json.loads((ROOT/z['report']).read_text())['configs'].values() if x['fingerprint']==fp)
 scope='native' if sp['kind']=='strategy' else 'parent'
 ref={k:c[k] for k in ['name','fingerprint','spec','archive','archive_sha256']}
 ref.update(scope=scope,asset=sp['universe'][0].split('/')[0] if scope=='native' else 'COMBO',capital_usdt=sp['parameters']['initial_capital_usdt'],report=z['report'],report_sha256=z['report_sha256'],spec_sha256=sha(ROOT/c['spec']),status=z['status'])
 assert sha(ROOT/ref['archive'])==ref['archive_sha256'];refs[fp]=ref
 if scope=='parent':
  ref.update(source_fingerprints=[x['fingerprint'] for x in sp['components']],raw_weights=[x['weight'] for x in sp['components']])
  for x in sp['components']:reference(x['fingerprint'])
for fp in [BTC,HOLD,*controls['parent'].values()]:reference(fp)
assert len(refs)==10 and sum(x['scope']=='native' for x in refs.values())==6
logic={'signal':'ETH fast L5 ROC r=C[i-1]/C[i-6]-1. Strict r>.02 short, r<-.02 long; otherwise actual long retained only r<.005, actual short only r>-.005. Entry/exit equalities do not retain/enter. Finite M(i,24)=sum_{j=0..23}[beta^j*C[i-1-j]]/sumweights, beta=23/25. Slope s=M(i,24)/M(i-D,24)-1. Gate +1 only s>K, -1 only s<-K, otherwise0 including both equalities. K=.001/.002/.003 and D1/3/5. Retain raw reversal desired only if equal to gate; zero/opposite forces flat, including current position. Entry-only sample logvol V10/cap.045 applies only fresh/reversal. Both mean windows strictly completed closes, no future/fitting/labels.',
'allocation':'Actual ETH bank C15000/N4500. Parent sums full BTC C3750/N500 old bank and full new ETH bank, raw[1,1], total18750, capital shares20/80%, initial nominal shares2.6666666667/24%. No weight normalization, old NAV/quantity resizing, parent orders, transfers, rebalance or cross margin. Signal geometric weights normalized only as its fixed formula.',
'execution':prior['rules']['execution'],'costs':prior['rules']['costs'],
'validation':'All9 new ETH natives+9 parents reserve before any valuation. Preset K .001/.002/.003 by D1/3/5, S24/L5/H.02/E.005/V10/.045 fixed. Separate K/D index-radius1 neighborhoods including center. Maximum S+D29 complete past closes within existing33 context. Continuous370d12x30+10tail, recent40/8x5, no fold resets. Fixed rules no fit/labels, purge0. Reused development history, not untouched final/independent future. No postoutcome batch/gate changes.',
'benchmark':'Old zero-strength slope controls S24 with the same D1/3/5 are preregistered references. They match capital,N,L,H,E,V,costs and calendar; only K changes. Their complete NAV and canonical status are read only. Matchedcapital/budget constant-long BTC500+ETH4500 and cash0% also read only. Differences are descriptive on reused history, no causal alpha proof.'}
impl={'path':rel(R/'engine.py'),'sha256':sha(R/'engine.py'),'accounting_unchanged_from':rel(P/'engine.py'),'signal_change':'Only ETH slope gate gains strict symmetric minimum-strength K; simulation AST/trade/funding/summary unchanged.'}
logic['native_implementation']=impl
sources=copy.deepcopy(prior['sources']);nb=[];pb=[];ng=[];pg=[];newsp={};mapping={};refwindows={}
for K,D in itertools.product(Ks,Ds):
 oldfp=controls['native'][str(D)];sp=copy.deepcopy(records[oldfp]['spec']);name=f'fewmStrength_ETH_S24_K{round(K*1000000)}ppm_D{D}_L5_H200bp_E5000ppm'
 sp.update(name=name,family='native-finite-ewmslope-strength-gated-reversal-entry-vol',logic=copy.deepcopy(logic),validation_plan=rel(R/'plan.json'),sources=sources)
 sp['parameters'].update(trend_slope_hurdle_fraction=K,signal_mode='finite_EWMslope_strength_gated_reversal_entry_vol',persistence='Executed position only; raw L5/H2 reversal with E.005 hysteresis, strict slope>K or slope<-K, neutral/equality/opposite flat, entry-only volatility.')
 path=R/'specs'/(name+'.json');path.parent.mkdir(exist_ok=True);put(path,sp);fp=reg.fingerprint(sp);assert fp not in records;newsp[fp]=(sp,rel(path))
 row={'name':name,'fingerprint':fp,'scope':'native','role':'component','asset':'ETH','capital_usdt':15000,'L':5,'H':.02,'S':24,'K':K,'D':D,'E':.005,'N':4500,'reference_fingerprint':oldfp,'reference_window_S':24,'reference_window_matched':True,'reference_lag_matched':True,'reference_strength_K':0,'spec':rel(path)}
 nb.append(row);ng.append({k:row[k] for k in ['L','H','S','K','D','E','fingerprint']}|{'readonly':False,'role':'component'});mapping[fp]=oldfp;refwindows[fp]=24
for g in ng:
 K,D,eth=g['K'],g['D'],g['fingerprint'];oldfp=controls['parent'][str(D)];sp=copy.deepcopy(records[oldfp]['spec']);name=f'fewmStrength_parent_BTC500_ETHS24_K{round(K*1000000)}ppm_D{D}'
 sp.update(name=name,family='native-finite-ewmslope-strength-gated-reversal-entry-vol',logic=copy.deepcopy(logic),components=[{'fingerprint':BTC,'weight':1},{'fingerprint':eth,'weight':1}],validation_plan=rel(R/'plan.json'),sources=sources)
 sp['parameters'].update(ETH_trend_slope_hurdle_fraction=K,ETH_signal_mode='finite_EWMslope_strength_gated_reversal_entry_vol',source_component_spec_sha256=[refs[BTC]['spec_sha256'],sha(ROOT/newsp[eth][1])])
 path=R/'specs'/(name+'.json');put(path,sp);fp=reg.fingerprint(sp);assert fp not in records
 row={'name':name,'fingerprint':fp,'scope':'parent','role':'candidate','asset':'COMBO','capital_usdt':18750,'BTC_capital_usdt':3750,'ETH_capital_usdt':15000,'BTC_N':500,'ETH_N':4500,'L':5,'H':.02,'S':24,'K':K,'D':D,'E':.005,'N':500,'source_fingerprints':[BTC,eth],'reference_fingerprint':oldfp,'reference_window_S':24,'reference_window_matched':True,'reference_lag_matched':True,'reference_strength_K':0,'spec':rel(path)}
 pb.append(row);pg.append({k:row[k] for k in ['L','H','S','K','D','E','N','fingerprint']}|{'readonly':False,'role':'candidate'});mapping[fp]=oldfp;refwindows[fp]=24
counts={'new_configs':18,'new_native':9,'new_parents':9,'new_candidate_configs':9,'new_source_components':9,'new_benchmark_configs':0,'new_cost_scenes':54,'old_current_parent_cells':0,'old_current_native_cells':0,'old_external_contrarian_controls':3,'old_benchmark_parents':1,'read_only_unique_results':10}
calendar={**prior['time_boundaries'],'calendar_frozen_before_current_evaluation_utc':now(),'causality':'M(i,24)/M(i-D,24)-1, D1/3/5, K strict symmetric hurdle. Maximum29 past complete closes; source context33. Fast i-1/i-6. No current/future bars or fits; next00:01 OPEN; continuous370d/no fold reset. All18 reserve before valuation. Reused development history.'}
plan={'round':R.name,'frozen_at_utc':now(),'hypothesis':'上轮仅按有限指数均值斜率正负过滤仍近期失败。本轮固定S24及其他交易规则，预先给斜率增加0.1/0.2/0.3%的最小强度K，并联合D1/3/5，检验过滤弱趋势是否减少反复进出与成本、以及是否丢失收益。九格9新原生+9新组合先reserve；相同D的旧K0斜率结果只读。门槛和网格事前冻结，不按本批结果调节。已知开发历史探索，不是独立未来/最终测试。',
'data':prior['data'],'time_boundaries':calendar,'trend_windows':[24],'fixed_trend_window_S':24,'slope_strengths':Ks,'slope_lags':Ds,'fixed_fast_L':5,'fixed_entry_H':.02,'fixed_exit_buffer':.005,'lookbacks':[5],'hurdles':[.02],'slow_estimator':'finite_normalized_exponentially_weighted_mean_slope','fixed_entry_volatility_window':10,'fixed_entry_volatility_cap':.045,'fixed_BTC_entry_notional':500,'fixed_ETH_entry_notional':4500,'fixed_bank_capitals':[3750,15000],'grid':pg,'native_grid':ng,
'benchmarks':[{'fingerprint':HOLD,'readonly':True,'role':'benchmark'}],'benchmark_parent_fingerprint':HOLD,'external_control_fingerprints':list(controls['parent'].values()),'primary_control_fingerprint':controls['parent']['3'],'predeclared_reference_by_fingerprint':mapping,'reference_window_by_fingerprint':refwindows,'read_only_references':refs,'rules':logic,'costs':records[controls['native']['3']]['spec']['parameters']['costs'],'gates':prior['gates'],
'sensitivity':{'candidate_axes':['slope_hurdle_K','slope_lag_D'],'index_radius':1,'includes_center':True,'local_positive3_min':.6,'local_recent_allcost6of8_min':.6,'scope':'9 new native and9 new parent cells separately; old K0 controls outside grid, canonical qualifications unchanged.'},
'expected_counts':counts,'representative_preset':{'S':24,'K':.002,'D':3,'scope':'Preset center before outcomes.'},'prior_report':{'path':rel(P/'report.json'),'sha256':sha(P/'report.json')},'new_native_policy_implementation':impl,'native_policy_sources':{'finiteEWMstrength':impl,'accounting':{'path':rel(CORE_PATH),'sha256':sha(CORE_PATH)}},'sources':sources,
'limits':'Repeated historical development and multiple selection, no untouched final holdout or independent future qualification. Missing historical L2/TCA, full tier/max-quantity and tick liquidation evidence; hour maintenance proxy and past ADV participation cap do not prove capacity. Fixed no-fit rules use context, no labels/learned model; purge0. A positive backtest is not stable live profit. Original frozen accounts unchanged. Official Binance documentation read successfully this round; actual current API data still required and audited.',
'skills':['walk-forward-validation','ml4t-sensitivity-analysis','ml4t-transaction-costs']}
put(R/'plan.json',plan);put(R/'spec.json',plan);put(R/'batch.json',nb+pb)
put(R/'semantic_inventory.json',{'scope':inventory['scope'],'new_configs':nb+pb,'new_native_evaluations':9,'read_only_unique_results':10,'zero_strength_native_controls_by_D':controls['native'],'all_references_S_and_D_matched':True})
print(json.dumps(counts),flush=True)
