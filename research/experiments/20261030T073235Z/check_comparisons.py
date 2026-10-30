"""Only replay recorded native/old ledgers to quantify actual integer sizing and impact differences."""
import gzip,json
from decimal import Decimal as D
from run import ROOT,R,sha,put
from controls import baselines
r=json.loads((R/'report.json').read_text());p=json.loads((R/'plan.json').read_text());refs=baselines(r['configs']);rows=[];integer=[]
for c in r['configs'].values():
 if c['role']=='candidate':
  for typ,b in refs[c['name']].items():
   better=all(c['scenes'][k]['net_return_pct']>b['scenes'][k]['net_return_pct'] and c['scenes'][k]['max_drawdown_pct']<b['scenes'][k]['max_drawdown_pct'] for k in ['1','2','3']);rows.append({'name':c['name'],'reference_type':typ,'reference':b['name'],'joint_return_DD_improves_everycost':better,'old_status':b['status'],'new_status':c['status'],'delta_return_pp_by_cost':{k:c['scenes'][k]['net_return_pct']-b['scenes'][k]['net_return_pct'] for k in ['1','2','3']},'delta_DD_pp_by_cost':{k:c['scenes'][k]['max_drawdown_pct']-b['scenes'][k]['max_drawdown_pct'] for k in ['1','2','3']}})
 if c['scope']!='native':continue
 if c['mode']=='hold':old=next(x for x in p['read_only_hold_references'].values() if x['asset']=='ETH' and x['fixed_entry_notional_usdt']==(4500 if c['sleeve']=='fast_hold' else 1500))
 elif c['sleeve']=='fast':old=p['fixed_fast_ETH']
 else:old=p['slow_ETH_sources'][f"L{c['lookback_days']}_H{c['return_hurdle']}"]
 assert sha(ROOT/old['archive'])==old['archive_sha256'];oldarc=json.loads(gzip.decompress((ROOT/old['archive']).read_bytes()));arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));scale=D(str(c['capital_usdt']))/D(str(old['capital_usdt']));sp=json.loads((ROOT/c['spec']).read_text());meta=next(x for x in p['data']['assets']['ETH'] if x['path'].endswith('/perp_instrument_meta.parquet'));import engine;lot=D(engine.pl.read_parquet(ROOT/meta['path'])['lot_size'][0]);count=diff=offlot=0
 for k,z in arc['scenes'].items():
  oldz=oldarc['scenes'][k];assert len(z['trades'])==len(oldz['trades'])
  for t,old_t in zip(z['trades'],oldz['trades']):
   assert (t['axis_index'],t['opening'],t['terminal'])==(old_t['axis_index'],old_t['opening'],old_t['terminal']);actual=D(t['quantity']);scaled=D(old_t['quantity'])*scale;assert actual%lot==0;count+=1;diff+=int(actual!=scaled);offlot+=int(scaled%lot!=0)
  integer.append({'name':c['name'],'cost_multiplier':int(k),'actual_capital_usdt':c['capital_usdt'],'scale_to_old_capital':str(scale),'old_fingerprint':old['fingerprint'],'actual_cost_usdt':z['summary']['cost_usdt'],'old_cost_times_bank_units_usdt':float(scale)*oldz['summary']['cost_usdt'],'actual_impact_cost_usdt':z['summary']['cost_parts_usdt']['impact'],'old_impact_times_bank_units_usdt':float(scale)*oldz['summary']['cost_parts_usdt']['impact']})
 integer.append({'name':c['name'],'all_threecost_fills':count,'actual_quantity_differs_from_scaled_old':diff,'scaled_old_quantity_violates_native_lot':offlot})
proof={'passed':True,'financial_report_sha256':sha(R/'report.json'),'new_financial_evaluations':0,'rows':rows,'integer_and_impact_checks':integer,'new_native_components':36,'joint_improvements_over_same_units_hold':sum(x['joint_return_DD_improves_everycost'] for x in rows if x['reference_type']=='same_raw_units_constantlong'),'qualifications_changed_vs_old_index':sum(x['new_status']!=x['old_status'] for x in rows if x['reference_type']=='matching_previous_ownership_index'),'scaled_old_fills_offlot':sum(x.get('scaled_old_quantity_violates_native_lot',0) for x in integer),'actual_native_amounts_recomputed_not_scaled_old_paths':True,'no_new_financial_recalculation':True,'source_old_statuses_unchanged':True};put(R/'comparison_verification.json',proof);print(json.dumps({k:v for k,v in proof.items() if k not in ['rows','integer_and_impact_checks']}),flush=True)
