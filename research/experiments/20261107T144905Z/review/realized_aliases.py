"""Read only saved exact NAV hashes/points/bounds; no strategy or account valuation."""
import json,sys
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import reg,sha,put
rd=lambda p:json.loads(p.read_text());report=rd(R/'report.json');rs=reg.read_records(ROOT/'research/automation/registry.jsonl');new={c['fingerprint'] for c in report['configs'].values()};ETH='3e0b88eeb2791e92cd32a0f7af780cb84502249a17b662a9850e466df045aa4b';cache={};oldnative={};oldparent={}
def config(fp,z):
 path=z['report'];assert sha(ROOT/path)==z['report_sha256']
 if path not in cache:cache[path]=rd(ROOT/path)
 return next(c for c in cache[path]['configs'].values() if c['fingerprint']==fp)
def sig(c):return tuple((str(k),c['scenes'][str(k)]['NAV_sha256_f64le'],c['scenes'][str(k)]['NAV_points']) for k in [1,2,3])
for fp,z in rs.items():
 sp=z.get('spec',{});q=sp.get('parameters',{})
 if fp not in new and z.get('result_available') and sp.get('kind')=='strategy' and sp.get('universe')==['BTC/USDT'] and q.get('exit_buffer_fraction')==.01 and all(q.get(k)==v for k,v in {'initial_capital_usdt':3750,'fixed_entry_notional_usdt':1000,'start_utc':'2025-10-19T00:01:00Z','end_utc':'2026-10-24T00:01:00Z'}.items()):oldnative[fp]=config(fp,z)
for fp,z in rs.items():
 sp=z.get('spec',{});q=sp.get('parameters',{});parts=sp.get('components',[])
 if fp not in new and z.get('result_available') and sp.get('kind')=='combination' and len(parts)==2 and all(Decimal(str(x['weight']))==1 for x in parts) and ETH in {x['fingerprint'] for x in parts} and any(x['fingerprint'] in oldnative for x in parts) and q.get('initial_capital_usdt')==18750 and q.get('start_utc')=='2025-10-19T00:01:00Z' and q.get('end_utc')=='2026-10-24T00:01:00Z':oldparent[fp]=config(fp,z)
rows=[]
for c in report['configs'].values():
 old=oldnative if c['scope']=='native' else oldparent;matches=[fp for fp,z in old.items() if sig(c)==sig(z)];rows.append({'fingerprint':c['fingerprint'],'name':c['name'],'scope':c['scope'],'L':c['L'],'H':c['H'],'E':c['E'],'matched_old_actual_NAV_fingerprints':matches,'all_three_cost_paths_seen_before':bool(matches)})
put(R/'same_bank_realized_NAV_alias_diagnostic.json',{'passed':True,'report_sha256':sha(R/'report.json'),'prior_native_definitions_compared':len(oldnative),'prior_parent_definitions_compared':len(oldparent),'rows':rows,'new_allcost_signatures_seen_in_prior_results':sum(bool(x['matched_old_actual_NAV_fingerprints']) for x in rows),'only_saved_full_NAV_hashes_points_and_same_time_bounds_compared':True,'no_new_backtest_policy_order_metrics_or_registry_write':True,'scope':'Posthoc description of realized paths,not mathematical strategy equivalence,independentmarketdata or new qualification gate. Distinct real parameters remain distinct definitions;oldstatusesunchanged.'});print('PASS saved NAV alias comparison',len(oldnative),len(oldparent),'prior definitions;matches',sum(bool(x['matched_old_actual_NAV_fingerprints']) for x in rows))
