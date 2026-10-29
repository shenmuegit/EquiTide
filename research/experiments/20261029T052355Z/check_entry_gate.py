"""Synthetic independent fast/entry gating boundary tests; no market PnL."""
from fractions import Fraction as F
from pathlib import Path
import ast,importlib.util,itertools,json,hashlib
import engine
R=Path(__file__).resolve().parent;ROOT=R.parents[2];src=ROOT/'research/experiments/20261028T232123Z/engine.py'
s=importlib.util.spec_from_file_location('entry_gate_old',src);old=importlib.util.module_from_spec(s);s.loader.exec_module(old)
n=0;retained=0;defaults=0
for L,H,S,q,r,ss in itertools.product([3,4],[F('0.02'),F('0.025'),F('0.03')],[27,28,29],[-1,0,1],[F('-0.04'),F('-0.03'),F('-0.025'),F('-0.02'),F('-0.01'),F(0),F('0.01'),F('0.02'),F('0.025'),F('0.03'),F('0.04')],[[-F('.05')]*3,[F('.05')]*3,[0,0,0],[-F('.05'),F('.05'),0],[-F('.05'),F('.05'),F('.02')]]):
 i=34;j=i-1;v=[F(100)]*45;v[j-L]=F(100)/(1+r)
 for h,x in zip([S-1,S,S+1],ss):v[j-h]=F(100)/(1+x)
 desired=-1 if r>H else 1 if r < -H else 1 if q==1 and r<0 else -1 if q==-1 and r>0 else 0
 allowed=1 if sum(x>0 for x in ss)>=2 else -1 if sum(x<0 for x in ss)>=2 else 0
 expected=desired if q!=0 and desired==q else desired if desired==allowed else 0
 a=engine.majority_target(v,i,L,float(H),q,0,S,trend_gate_application='entries_only')
 assert a[0]==expected and F(a[1])==r and F(a[2])==sorted(ss)[1],(L,H,S,q,r,ss,a,expected)
 if q and desired==q and q!=allowed:retained+=1
 w=v[:];w[i:]=[F(999)]*(len(v)-i);assert engine.majority_target(w,i,L,float(H),q,0,S,trend_gate_application='entries_only')==a
 assert engine.majority_target(v,i,L,float(H),q,0,S)==old.majority_target(v,i,L,float(H),q,0,S);defaults+=1;n+=1
assert n==2970 and retained>0 and defaults==n
oldtxt=src.read_text();newtxt=(R/'engine.py').read_text()
def funcs(s):return {x.name:ast.get_source_segment(s,x) for x in ast.parse(s).body if isinstance(x,ast.FunctionDef)}
a,b=funcs(oldtxt),funcs(newtxt);changed=[k for k in a if a[k]!=b[k]];assert changed==['majority_target','simulate'] and a.keys()==b.keys()
put=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n')
put(R/'engine_change_verification.json',{'passed':True,'source_path':str(src.relative_to(ROOT)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'new_sha256':hashlib.sha256((R/'engine.py').read_bytes()).hexdigest(),'changed_functions':changed,'all_other_functions_byte_identical':True,'synthetic_cases':n,'default_old_rule_regression_checks':defaults,'held_actual_position_retained_despite_incompatible_slow_gate':retained,'future_invariance_checks':n,'no_market_PnL':True})
print('PASS',n,'entry/retention boundaries,default regressions,future invariance; changed only',changed)
