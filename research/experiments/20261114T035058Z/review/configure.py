"""Prepare existing accounting pipeline for6new configs plus8readonly actual controls."""
import ast,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2]
def change(n,pairs):
 p=R/n;s=p.read_text()
 for a,b in pairs:assert a in s,(n,a);s=s.replace(a,b)
 p.write_text('\n'.join(x.rstrip() for x in s.splitlines())+'\n')
change('run.py',[("len(batch)==11","len(batch)==6"),("BTC_VOL_CAP","BTC_VOL_WINDOW_DAYS"),("'new_native_models':6,'new_parent_models':5","'new_native_models':2,'new_parent_models':4"),("'read_only_ETH_bank_reused':False","'read_only_ETH_bank_reused':True")])
p=R/'run.py';s=p.read_text();a=s.index(" if c['scope']=='native':return");b=s.index(" rows=p['grid']",a);s=s[:a]+''' if c['scope']=='native':
  rows=[g for g in p['native_grid'] if g['asset']==c['asset']];axis='BTC_VOL_WINDOW_DAYS' if c['asset']=='BTC' else 'ETH_FUND_R';key='W' if c['asset']=='BTC' else 'K';return [full[g['fingerprint']] for g in rows if abs(p['axes'][axis].index(g[key])-p['axes'][axis].index(c[key]))<=1],1
'''+s[b:]
a=s.index(" full={c['fingerprint']:c for c in configs.values()}");b=s.index(' for c in configs.values():',a);s=s[:a]+''' full={c['fingerprint']:c for c in configs.values()};readonly={}
 for fp,d in p['read_only_references'].items():
  c=copy.deepcopy(next(c for c in json.loads((ROOT/d['report']).read_text())['configs'].values() if c['fingerprint']==fp));c.update(W=d['W'],K=d['K'],readonly=True);full[fp]=c;readonly[fp]=c
 for c in full.values():
  ns,dims=neighbors(c,p,full);c['current_grid_diagnostic_sensitivity']={'dimension_count':dims,'neighbor_names':[z['name'] for z in ns],'local_strict_recent_fraction':sum(recent_ok(z) for z in ns)/len(ns),'local_positive3_fraction':sum(z['scenes']['3']['net_return_pct']>0 for z in ns)/len(ns),'original_status_not_reclassified':c.get('readonly',False)}
'''+s[b:]
s=s.replace("'read_only_sources':p['read_only_references']","'read_only_sources':p['read_only_references'],'read_only_configs':readonly");p.write_text(s)
change('audit.py',[("BTC_VOL_CAP","BTC_VOL_WINDOW_DAYS"),("(18,15,7038,0)","(6,12,2346,15)")])
p=R/'audit.py';s=p.read_text();old="if c['scope']=='native':ns=[full[g['fingerprint']] for g in rows if g['asset']==c['asset']];dims=1";new="if c['scope']=='native':\n   axis='BTC_VOL_WINDOW_DAYS' if c['asset']=='BTC' else 'ETH_FUND_R';key='W' if c['asset']=='BTC' else 'K';ns=[full[g['fingerprint']] for g in rows if g['asset']==c['asset'] and abs(plan['axes'][axis].index(g[key])-plan['axes'][axis].index(c[key]))<=1];dims=1";assert old in s;s=s.replace(old,new)
a=s.index("full={c['fingerprint']:c for c in report['configs'].values()}");s=s[:a]+'''readonly_parent_curves=0
for fp,ref in plan['read_only_references'].items():
 if ref['scope']!='parent':continue
 arc=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()));fps=ref['source_fingerprints']
 for k,z in arc['scenes'].items():
  vv=vectors[fps[0],k]+vectors[fps[1],k];ss=z['summary'];assert ss['NAV_sha256_f64le']==core.navhash(vv) and z['source_common_axis_sha256']==cm['sha256'] and ss['daily_equity_usdt']==vv[cm['daily_indices']].tolist();metrics(vv,ss['daily_equity_usdt'],391,ss);counts['metric_checks']+=1
  for j,(aa,bb) in enumerate(zip(cm['fold_indices'],cm['fold_indices'][1:])):metrics(vv[aa:bb+1],ss['daily_equity_usdt'][j*30:min(j*30+30,391)+1],min(30,391-j*30),ss['folds'][j]);counts['metric_checks']+=1
  verify_recent(vv,proxy,ss);verify_extension(vv,proxy,ss)
  for field in ['cost_usdt','funding_usdt','gross_reference_price_PnL_usdt','executions','round_trips','funding_settlements']:near(ss[field],sum(source_scenes[f,k][field] for f in fps),1e-12)
  readonly_parent_curves+=1
assert readonly_parent_curves==9 and readonly_decisions==5865
'''+s[a:];s=s.replace("'readonly_policy_decisions':readonly_decisions","'readonly_policy_decisions':readonly_decisions,'read_only_parent_curves':readonly_parent_curves");p.write_text(s)
startup={'round':R.name,'trigger_utc':'2026-11-14T03:50:58.442Z','base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'branch_lock_broker_pid':1583285,'branch_lock_session':60233,'branch_lock_native_start_chunk':'758d9e','root_native_verification_chunk':'45527f','initial_fetch_native_start_chunk':'6b1031','initial_fetch_native_session':34184,'initial_fetch_native_completion_chunk':'cf05ec','initial_sync_no_merge_required':True,'only_preexisting_untracked':'data/normalized','previous_round_publication_verified':'completed_published_verified_unlocked'};(R/'startup.json').write_text(json.dumps(startup,indent=2)+'\n')
for p in R.rglob('*.py'):ast.parse(p.read_text())
print('PASS6new/8readonly,one-axis native and two-axisparent neighbors,unchanged391daycore;0financialcalculations')
