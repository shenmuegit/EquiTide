"""Calendar geometry only; all policy and native-money formulas remain unchanged."""
import ast,json,re,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2]
def save(n,s):(R/n).write_text('\n'.join(x.rstrip() for x in s.splitlines())+'\n')
def alter(n,pairs):
 s=(R/n).read_text()
 for a,b in pairs:
  assert a in s,(n,a);s=s.replace(a,b)
 save(n,s)
def numbers(s,m):return re.sub(r'\b(?:'+'|'.join(map(str,m))+r')\b',lambda z:str(m[int(z[0])]),s)
assert json.loads((R/'extended_data_manifest.json').read_text())['passed']
s=(R/'core390.py').read_text();s=numbers(s,{390:391,423:424,424:425,609122:610562,10152:10176,1270:1273,1170:1173,574473:575946});s=s.replace('2026-11-13T00:01:00Z','2026-11-14T00:01:00Z');save('core391.py',s);(R/'core390.py').unlink();alter('common.py',[('core390.py','core391.py')])
for n in ['market.py','run.py','audit.py','audit_native.py','portfolio.py','recent.py','audit_helpers_complete.py']:
 s=(R/n).read_text().replace("'daily_boundaries':391","'daily_boundaries':DAILYBOUND").replace('len(daily)==391','len(daily)==DAILYBOUND')
 s=numbers(s,{390:391,350:351,355:356,423:424,1270:1273,1170:1173,7020:7038});s=s.replace('DAILYBOUND','392').replace('2026-11-13T00:01:00Z','2026-11-14T00:01:00Z').replace('2026-10-04T00:01:00Z','2026-10-05T00:01:00Z').replace('extension20','extension21').replace('389day','391day').replace('389days','391days').replace('day349','day351')
 s=s.replace('core.stats(tail,daily[370:],20)','core.stats(tail,daily[370:],21)').replace('len(daily[370:])==21','len(daily[370:])==22').replace('metrics(v[a:],daily[370:],20,s)','metrics(v[a:],daily[370:],21,s)')
 s=s.replace("for f in one['folds'])>=10","for f in one['folds'][:13])>=10").replace("for f in scenes['1']['folds'])","for f in scenes['1']['folds'][:13])").replace("'folds':13,'daily_boundaries'","'folds':14,'daily_boundaries'")
 if n=='run.py':s=s.replace("c['scope']=='native' and c['status']=='rejected'","c['scope']=='native' and c['role']=='component' and c['status']=='rejected'")
 save(n,s)
for n in ['freeze.py','definitions.py']:
 s=(R/n).read_text().replace('390','CURRENT391').replace('389','390').replace('CURRENT391','391').replace('2026-11-13T00:01:00Z','2026-11-14T00:01:00Z').replace('2026-10-04T00:01:00Z','2026-10-05T00:01:00Z').replace('recent40day350','recent40day351').replace('extension20','extension21').replace('tail_fold_days=0','tail_fold_days=1').replace('walk_forward_tail_days=0','walk_forward_tail_days=1').replace('walk_forward_folds=13','walk_forward_folds=14').replace("'tail_fold_days':0","'tail_fold_days':1").replace("q['tail_fold_days']==0","q['tail_fold_days']==1").replace('day3704x5','day3705+5+5+6').replace('13full30dayfolds,','13full30dayfolds+1daytail,').replace("extension21_positive5d_eachcost_min","extension21_positive_fold_eachcost_min")
 if n=='definitions.py':s=s.replace("funs(P/'core390.py'),funs(R/'core391.py')","funs(P/'core390.py'),funs(R/'core391.py')")
 save(n,s)
alter('parent_units.py',[("assert core.END-core.START==core.DAYS==390 and list(range(0,391,30))==[0,30,60,90,120,150,180,210,240,270,300,330,360,390] and 390-350==40 and 390-370==20","assert core.END-core.START==core.DAYS==391 and list(range(0,391,30))+[391]==[0,30,60,90,120,150,180,210,240,270,300,330,360,390,391] and 391-351==40 and 391-370==21"),('calendar390_13fullfold_recent40_extension20_checked','calendar391_13fullfold_1daytail_recent40_extension21_checked')])
alter('checks.py',[('7020','7038'),("len(s['folds'])==13","len(s['folds'])==14"),("s['extension20']","s['extension21']"),("len(s['daily_equity_usdt'])==391","len(s['daily_equity_usdt'])==392")])
for n in ['exports.py','review/attribution.py','review/final_result_review.py','review/visual_review.py']:
 s=(R/n).read_text().replace('390','CURRENT391').replace('389','390').replace('CURRENT391','391').replace('extension20','extension21').replace('WF390','WF391');save(n,s)
# Original-account windows are independent from research calendars.
alter('review/setup.py',[('2026-11-13T20:30:00Z','SINGLE_END'),('2026-11-13T18:30:00Z','2026-11-13T20:30:00Z'),('SINGLE_END','2026-11-13T22:30:00Z'),('2026-11-13T22:10:00Z','L4_END'),('2026-11-13T20:10:00Z','2026-11-13T22:10:00Z'),('L4_END','2026-11-14T00:10:00Z'),("'expected_daily_events_utc':[]","'expected_daily_events_utc':['2026-11-14T00:01:00Z'] if a in ['l4h02','fewm'] else []"),("'next_daily_decision_utc':'2026-11-14T00:01:00Z'","'next_daily_decision_utc':'2026-11-15T00:01:00Z' if a in ['l4h02','fewm'] else '2026-11-14T00:01:00Z'"),('==[0,0,0,0]','==[0,0,6,6]'),("assert fresh['public_fields_by_asset']=={'BTC':[],'ETH':[]} and prior", "assert all(len(xs)==1 and xs[0]['fundingTime']<ms('2026-11-14T00:01:00Z') for xs in fresh['public_fields_by_asset'].values()) and prior"),('All3 perp accounts already booked actual00/08/16once. Fresh full-window public captures show no new settlement;do not repeat previous funding. Actual timestamps determine records;no schedule assumption. No daily decisions/fills/reset/forcedexit/research adoption;SMA full65 authority033939 unchanged.','All3 perp accounts booked Nov13 actual00/08/16 once. L4/FEWM now cover Nov14 actual00 and original00:01 decisions, using own q/cash and completed1440minute dailyvolume. SMA/single end22:30 before midnight. No reset/forcedexit/research-rule adoption. Funding actual timestamps determine records;original sources retained. SMA full65 authority033939 unchanged.'),('PASS frozen actual funding split0/0/0/0,no daily;sourcebinding before0calculations','PASS frozen actual funding0/0/6/6 and L4FEWM original daily, before0calculations')])
p=R/'review/setup.py';s=p.read_text().replace("w.update(recorded_utc=now()", "put(R/'funding00_nov14_preflight.json',fresh)\nw.update(recorded_utc=now()");save('review/setup.py',s)
startup={'round':R.name,'trigger_utc':'2026-11-14T01:50:57.835Z','base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'branch_lock_broker_pid':1552430,'branch_lock_session':99279,'branch_lock_native_start_chunk':'b40768','root_native_verification_chunk':'1d2b40','initial_fetch_native_start_chunk':'ca2779','initial_fetch_native_session':49797,'initial_fetch_native_completion_chunk':'c63170','initial_sync_no_merge_required':True,'only_preexisting_untracked':'data/normalized','previous_round_publication_verified':'completed_published_verified_unlocked','primary_docs_browsed':['https://github.com/binance/binance-public-data/blob/master/README.md','https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data']};save('startup.json',json.dumps(startup,indent=2))
for f in R.rglob('*.py'):
 ast.parse(f.read_text());assert not any(x!=x.rstrip() for x in f.read_text().splitlines()),f
print('PASS391calendar:13fullmonths+1daytail,monthlygateexcludestail,recent40day351,extension21=5+5+5+6;originalaccountsL4FEWMmidnight;0financialcalculations')
