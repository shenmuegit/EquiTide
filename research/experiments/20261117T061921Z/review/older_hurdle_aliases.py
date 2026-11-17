"""Read older complete M/R family monetary paths without recomputing any configuration."""
import gzip,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));h=sha(R/'report.json');cur=rd(R/'report.json');look=rd(R/'entry_hurdle_semantic_screen.json');rs=reg.read_records(ROOT/'research/automation/registry.jsonl');eth={z['fingerprint'] for z in look['all_same_other_parameter_H_R'] if z['result_available']};btc={'41de4309229b892489a07574af07a73ae93229a35c118558ed60362285e90c89','621cdb34d10b83962a72a65c19e0c1597765071f9edac9e0465b0c69e3cb5bf6'};wanted=set(eth)
for fp,z in rs.items():
 sp=z.get('spec',{});q=sp.get('parameters',{});cc=sp.get('components',[])
 if z.get('result_available') and sp.get('kind')=='combination' and q.get('continuous_oos_days')==391 and q.get('initial_capital_usdt')==18750 and len(cc)==2 and all(c['weight']==1 for c in cc):
  fs={c['fingerprint'] for c in cc}
  if len(fs&eth)==1 and len(fs&btc)==1:wanted.add(fp)
assert not wanted & {c['fingerprint'] for c in cur['configs'].values()};docs={};old=[];sources={}
for fp in sorted(wanted):
 z=rs[fp];rp=ROOT/z['report'];assert z['result_available'] and sha(rp)==z['report_sha256']
 if rp not in docs:docs[rp]=rd(rp)
 c=next(c for c in docs[rp]['configs'].values() if c['fingerprint']==fp);assert sha(ROOT/c['archive'])==c['archive_sha256'];old.append(c);sources[rel(rp)]=z['report_sha256']
rows=[]
for c in cur['configs'].values():
 sig=tuple(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']);matches=[]
 for o in old:
  if o['scope']!=c['scope'] or tuple(o['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3'])!=sig:continue
  stateproof=None
  if c['scope']=='native':
   a,b=gz(ROOT/c['archive']),gz(ROOT/o['archive']);stateproof=all(x['trades']==y['trades'] and x['funding_events']==y['funding_events'] and len(x['decisions'])==len(y['decisions'])==391 and all((d['desired_direction'],d['state_before'],d['state_after'])==(e['desired_direction'],e['state_before'],e['state_after']) for d,e in zip(x['decisions'],y['decisions'])) for k in ['1','2','3'] for x,y in [(a['scenes'][k],b['scenes'][k])]);assert stateproof
  matches.append({'fingerprint':o['fingerprint'],'name':o['name'],'archive':o['archive'],'archive_sha256':o['archive_sha256'],'status':o['status'],'allcost_NAV_and_native_state_if_applicable_identical':stateproof if c['scope']=='native' else True})
 rows.append({'new_fingerprint':c['fingerprint'],'scope':c['scope'],'H':c['W'],'BTC_H':c['K'],'matches':matches})
assert sha(R/'report.json')==h;put(R/'older_hurdle_path_alias_verification.json',{'passed':True,'recorded_utc':now(),'financial_report_sha256':h,'old_native_configurations_read':len(eth),'old_same_BTC_bank_parent_configurations_read':len(wanted)-len(eth),'source_report_sha256':sources,'rows':rows,'new_configurations_matching_saved_paths':sum(bool(z['matches']) for z in rows),'native_matches':sum(z['scope']=='native' and bool(z['matches']) for z in rows),'parent_matches':sum(z['scope']=='parent' and bool(z['matches']) for z in rows),'scope':'All pre-round exact other-parameter ETH H/R banks from semantic screen plus actually completed raw1/1 sameBTC-bank parents. Saved paths/states only;not independent market evidence or a global all-strategy alias census.','new_market_model_account_or_registry_executions':0});print('PASS olderH/R savedpath comparison',len(eth),len(wanted)-len(eth),'old;current matches',sum(bool(z['matches']) for z in rows))
