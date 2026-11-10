import gzip,hashlib,importlib.util,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def gzwrite(p,x):p.write_bytes(gzip.compress(json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode(),mtime=0))
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
CORE_PATH=ROOT/'research/experiments/20261030T173813Z/engine.py';core=module(CORE_PATH,'immutable_native_accounting')
MIN,HOUR,DAY=core.MIN,core.HOUR,core.DAY
ENTRIES=[2,2.5,3];EXITS=[.5,1,1.5]
def call(command,row,*args):
 p=subprocess.run([sys.executable,'research/automation/registry.py',command,row['spec'],*args],cwd=ROOT,capture_output=True,text=True);x={'name':row['name'],'fingerprint':row['fingerprint'],'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};print(json.dumps(x),flush=True);assert p.returncode==0 and p.stdout.strip()==row['fingerprint'];return x
