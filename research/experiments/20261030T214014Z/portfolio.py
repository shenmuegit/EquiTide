"""Recover immutable source ledgers and value raw owned units without new trades."""
import json,gzip,copy
import numpy as np
from common import *
import market

def native_curve(scene,m):
 v=np.empty(len(m['ts']));end=0
 for z in scene['state_segments']:
  a,b=z['axis_start'],z['axis_end_exclusive'];assert a==end and b>a
  v[a:b]=float(z['cash'])+float(z['signed_units'])*(m['axis_prices'][a:b]-float(z['entry_price']));end=b
 assert end==len(v) and core.navhash(v)==scene['summary']['NAV_sha256_f64le'];return v

def expand(scene,source_m,new_m,axis):
 dt=axis['keys'].dtype;keys=np.empty(len(source_m['ts']),dtype=dt);keys['t']=source_m['ts'];keys['k']=source_m['codes'];idx=np.searchsorted(axis['keys'],keys);assert np.array_equal(axis['keys'][idx],keys)
 source=native_curve(scene,source_m);v=np.empty(len(axis['ts']));segments=scene['state_segments']
 for j,z in enumerate(segments):
  a=int(idx[z['axis_start']]);b=int(idx[segments[j+1]['axis_start']]) if j+1<len(segments) else len(v)
  v[a:b]=float(z['cash'])+float(z['signed_units'])*(new_m['axis_prices'][a:b]-float(z['entry_price']))
 assert np.array_equal(v[idx],source) and core.navhash(v[idx])==scene['summary']['NAV_sha256_f64le'];assert np.isfinite(v).all() and (v>0).all()
 return v,{'original_points':len(source),'expanded_points':len(v),'original_NAV_sha256_f64le':core.navhash(source),'expanded_NAV_sha256_f64le':core.navhash(v),'original_points_byte_identical':True,'extra_price_points':len(v)-len(source),'source_axis_sha256':source_m['axis_sha256'],'expanded_axis_sha256':axis['axis_sha256']}

def read_sources(plan):
 ms,axis=market.load(plan);oldms={a:core.load_market(a,files) for a,files in plan['data']['assets'].items()};curves={};scenes={};proof={};archives={fp:json.loads(gzip.decompress((ROOT/x['archive']).read_bytes())) for fp,x in plan['source_results'].items() if fp in {plan['trend_parent']['fingerprint'],*[z['fingerprint'] for z in plan['trend_native']],*[z['fingerprint'] for z in plan['paired_parents'].values()]}}
 for fp,arc in archives.items():assert arc['fingerprint']==fp and reg.fingerprint(arc['spec'])==fp
 for k in ['1','2','3']:
  vv=[];native_old=[]
  for asset,x in zip(['BTC','ETH'],plan['trend_native']):
   fp=x['fingerprint'];z=archives[fp]['scenes'][k];v,p=expand(z,oldms[asset],ms[asset],axis);vv.append(v);native_old.append(native_curve(z,oldms[asset]));proof[fp+':'+k]=p;scenes[(fp,k)]=z
  fp=plan['trend_parent']['fingerprint'];z=archives[fp]['scenes'][k];old=native_old[0]+native_old[1];assert core.navhash(old)==z['summary']['NAV_sha256_f64le'] and [core.navhash(v) for v in native_old]==z['source_full_NAV_sha256'];v=vv[0]+vv[1];curves[(fp,k)]=v;scenes[(fp,k)]=z;proof[fp+':'+k]={'original_NAV_sha256_f64le':core.navhash(old),'original_points':len(old),'expanded_NAV_sha256_f64le':core.navhash(v),'expanded_points':len(v),'source_native_original_hashes_verified':True}
  for x in plan['paired_parents'].values():
   fp=x['fingerprint'];z=archives[fp]['scenes'][k];legs=[native_curve(z['legs'][a],ms[a]) for a in ['BTC','ETH']];v=legs[0]+legs[1];assert core.navhash(v)==z['summary']['NAV_sha256_f64le'];curves[(fp,k)]=v;scenes[(fp,k)]=z;proof[fp+':'+k]={'original_NAV_sha256_f64le':core.navhash(v),'expanded_NAV_sha256_f64le':core.navhash(v),'original_points':len(v),'expanded_points':len(v),'source_native_original_hashes_verified':True}
 return ms,oldms,axis,curves,scenes,proof

def recent(v,m):
 ix=m['daily_indices'];daily=v[ix].tolist();tail=v[ix[330]:];s=core.stats(tail,daily[330:],40);s.update(start_utc='2026-09-14T00:01:00Z',end_exclusive_utc='2026-10-24T00:01:00Z',initial_NAV_usdt=float(tail[0]),final_NAV_usdt=float(tail[-1]),NAV_points=len(tail),NAV_sha256_f64le=core.navhash(tail),daily_equity_usdt=daily[330:],state_policy='Inherited source day330 accounts and raw ownership,no reset or diagnostic orders.',folds=[])
 for j in range(8):
  l,h=330+5*j,335+5*j;a,b=ix[[l,h]];s['folds'].append({'fold':j+1,'start_utc':core.stamp(int(m['ts'][a])),'end_exclusive_utc':core.stamp(int(m['ts'][b])),'duration_days':5,**core.stats(v[a:b+1],daily[l:h+1],5)})
 return s

def summary(v,axis,source_summaries,weights,capital):
 daily=v[axis['daily_indices']].tolist();s=core.stats(v,daily,370);s['folds']=[]
 for j,(a,b) in enumerate(zip(axis['fold_indices'],axis['fold_indices'][1:])):
  days=min(30,370-30*j);s['folds'].append({'fold':j+1,'start_utc':core.stamp(int(axis['ts'][a])),'end_exclusive_utc':core.stamp(int(axis['ts'][b])),'duration_days':days,**core.stats(v[a:b+1],daily[30*j:30*j+days+1],days)})
 money=['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','gross_reference_price_PnL_usdt'];counts=['executions','rejected_orders','cash_or_units_violations','funding_settlements','nonzero_funding_settlements'];s.update({k:sum(w*x[k] for x,w in zip(source_summaries,weights)) for k in money});s.update({k:sum(x[k] for x in source_summaries) for k in counts});parts=source_summaries[0]['cost_parts_usdt'];s['cost_parts_usdt']={k:sum(w*x['cost_parts_usdt'][k] for x,w in zip(source_summaries,weights)) for k in parts}
 s.update(initial_capital_usdt=capital,final_NAV_usdt=float(v[-1]),cost_pct_initial=100*s['cost_usdt']/capital,round_trips=sum(x['round_trips'] for x in source_summaries),source_round_trips=[x['round_trips'] for x in source_summaries],source_operations_counts_not_fractional_orders=True,terminal_flat=all(float(x['terminal_units'])==0 for x in source_summaries),daily_equity_usdt=daily,NAV_points=len(v),NAV_sha256_f64le=core.navhash(v),axis_sha256=axis['axis_sha256'],margin={'independent_sleeve_violations':sum(x['margin'].get('independent_sleeve_violations',x['margin'].get('violations',0)) for x in source_summaries),'no_cross_margin_netting':True},recent40=recent(v,axis))
 s['gross_reference_PnL_to_execution_cost']=(s['gross_reference_price_PnL_usdt']+s['funding_usdt'])/s['cost_usdt'] if s['cost_usdt'] else None
 assert v[0]==capital and abs(s['gross_reference_price_PnL_usdt']+s['funding_usdt']-s['cost_usdt']-(v[-1]-capital))<1e-8;return s
