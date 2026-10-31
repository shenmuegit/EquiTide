"""Engineering and readonly policy identity only; no future financial result/account."""
import ast,copy,gzip,hashlib,importlib.util,json,os,subprocess,sys,time
from decimal import Decimal as D
from pathlib import Path
F=Path(__file__).resolve().parent;ROOT=F.parents[3];sys.path.insert(0,str(F));import core as c
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');binding=c.bindings();plan=json.loads(c.PLAN.read_text());assert time.time_ns()<c.START and c.END-c.START==180*c.DAY
assert binding['capitals']=={'BTC':5000,'ETH':15000} and binding['rules']['ETH']['L']==4 and not(ROOT/'research/automation/l4h02_forward_latest.json').exists()
def fn(path,name):return next(x for x in ast.parse(path.read_text()).body if isinstance(x,ast.FunctionDef) and x.name==name)
for name in ['trade','funding_amount']:assert ast.dump(fn(Path(c.GATE.__file__),name))==ast.dump(fn(ROOT/'research/experiments/20261030T173813Z/engine.py',name))
# Actual baseline saved decisions checked as readonly rule identity, not a backtest.
parent=json.loads((ROOT/plan['original_candidate']['spec']).read_text());sys.path.insert(0,str(ROOT/'research/automation'));import registry;records=registry.read_records(ROOT/'research/automation/registry.jsonl');decisions=0
for comp in plan['components']:
 a=comp['asset'];p=comp['parameters'];path=next(x for x in p['input_hashes'] if x.endswith('perp_bars.parquet'));assert sha(ROOT/path)==p['input_hashes'][path];df=c.GATE.pl.read_parquet(ROOT/path,columns=['open_ts','close']);daily=df.with_columns((c.GATE.pl.col('open_ts')//c.DAY).alias('day')).group_by('day',maintain_order=True).agg(c.GATE.pl.col('close').last()).sort('day');values=daily['close'].to_list();rec=records[comp['fingerprint']];rep=json.loads((ROOT/rec['report']).read_text());cfg=next(z for z in rep['configs'].values() if z['fingerprint']==comp['fingerprint']);arc=json.loads(gzip.decompress((ROOT/cfg['archive']).read_bytes()))
 for leg in arc['scenes'].values():
  for z in leg['decisions']:
   q=D(z['state_before']['signed_units']);direction=(q>0)-(q<0);i=z['decision_index'];res=c.TREND.target(values,i,31,.04,direction,.01) if a=='BTC' else c.target_eth(values,i,direction);assert res[0]==z['desired_direction'];decisions+=1
assert decisions==2220
# Ephemeral synthetic books/actions; never persisted as a real account or PnL evidence.
csB=[D(100000)]*40;csB[-1]=D(110000);csE=[D(3000)]*40;csE[11]=D(3500);csE[-1]=D(3300)
payload={'BTC':{'price':'110000','closes':[str(x) for x in csB],'ADV':'100000000','sigma':'.03'},'ETH':{'price':'3300','closes':[str(x) for x in csE],'ADV':'100000000','sigma':'.03'}}
actions={(c.START,0):{a:{'price':p['price']} for a,p in payload.items()}}
for code in [5,6,7]:actions[c.START,code]=copy.deepcopy(payload)
s,delta=c.transition(None,actions,c.START,binding);assert all(D(s['books']['BTC'][k]['signed_units'])==D('.004') and D(s['books']['ETH'][k]['signed_units'])==D('-1.363') for k in ['1','2','3']);assert delta['NAV'][0]['NAV']['COMBO']['1']==20000
T=(c.START//c.HOUR+2)*c.HOUR;fund={a:{'price':p['price'],'rate':'.0001'} for a,p in payload.items()};hour={a:{'price':p['price'],'low':str(D(p['price'])*D('.99')),'high':str(D(p['price'])*D('1.01')),'hour_open_ns':T-c.HOUR} for a,p in payload.items()};before=copy.deepcopy(s);s,d=c.transition(s,{(T,2):hour,(T,3):fund,(T,4):fund},T,binding)
for a in ['BTC','ETH']:
 for k in ['1','2','3']:
  stack=s['risk'][a][k];assert stack[-2]['t']==stack[-1]['t']==T;amount=-D(before['books'][a][k]['signed_units'])*D(payload[a]['price'])*D('.0001');expected=amount*int(k) if amount<0 else amount;assert D(s['books'][a][k]['cash'])==D(before['books'][a][k]['cash'])+expected
hour2=copy.deepcopy(hour)
for p in hour2.values():p['hour_open_ns']=T
old=copy.deepcopy(s);s,d=c.transition(s,{(T+c.HOUR,2):hour2},T+c.HOUR,binding)
assert sum(s['counters'][a][k]['margin_checks']-old['counters'][a][k]['margin_checks'] for a in ['BTC','ETH'] for k in ['1','2','3'])==6
# Closed-bar temporal rejection and no-write prestart CLI guard.
raw=[[c.START//c.MS,'1','1','1','1','0',(c.START+c.MIN)//c.MS-1,'0',0,0,0,0]]
try:c.closed_bars(raw,c.MIN,c.START);raise AssertionError('unclosedbaraccepted')
except AssertionError as e:assert str(e)!='unclosedbaraccepted'
ledger=ROOT/'research/automation/registry.jsonl';oldsha=sha(ledger);cmd=[sys.executable,str(F/'observer.py'),'run','--round',F.parent.name,'--cutoff','2026-11-01T00:03:00Z','--lock-pid','570432'];z=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);assert z.returncode==1 and 'before planned start' in z.stderr and sha(ledger)==oldsha and not(ROOT/'research/automation/l4h02_forward_latest.json').exists() and not(F.parent/'l4h02_observation').exists()
status=subprocess.run([sys.executable,str(F/'observer.py'),'status'],cwd=ROOT,capture_output=True,text=True);assert status.returncode==0;out=json.loads(status.stdout);assert out['status']=='waiting_for_planned_start' and not out['account_created'] and out['network_requests']==out['filesystem_writes']==out['registry_writes']==0
put(F/'engineering_checks.json',{'passed':True,'engineering_only_no_financial_trials':True,'readonly_actual_baseline_decision_identity_checks':decisions,'trade_funding_AST_identical_to_native_accounting':True,'synthetic_cases':['actual5000/15000capitaland500/4500nativeLOTentry','strictL4zeroexitbaselineidentity','fundingoutflowstressedandincomenotamplified','same-nszerodurationprefundexcludednexthour','unclosedbarrejected','prestartCLIblockedbeforefilesystem/network/registry'],'prestart_denial':{'exit_code':z.returncode,'stderr':z.stderr},'status':out,'registry_sha256_before_after':oldsha,'actual_future_accounts':0,'actual_future_observations':0,'new_backtests':0,'plan_sha256':sha(c.PLAN),'binding_sha256':sha(c.FREEZE),'core_sha256':sha(F/'core.py'),'observer_sha256':sha(F/'observer.py')});print('PASS futureL4/H2 engineering,2220readonlybaseline decisions;0futureaccounts/GET/registrywrites',flush=True)
