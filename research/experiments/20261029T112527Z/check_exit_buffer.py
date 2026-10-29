"""Synthetic exact boundary/state/future tests only; no market inputs or strategy PnL."""
from fractions import Fraction as F
from pathlib import Path
import ast,hashlib,importlib.util,itertools,json
import engine
R=Path(__file__).resolve().parent;ROOT=R.parents[2];src=ROOT/'research/experiments/20261029T052355Z/engine.py';sp=importlib.util.spec_from_file_location('zeroexit_source',src);old=importlib.util.module_from_spec(sp);sp.loader.exec_module(old)
rs=[F(x) for x in ['-.04','-.025','-.02','-.015','-.01','-.005','0','.005','.01','.015','.02','.025','.04']];slowsets=[[-F('.05')]*3,[F('.05')]*3,[F(0)]*3,[-F('.05'),F('.05'),F(0)],[-F('.05'),F('.05'),F('.02')]];n=regress=overshoots=0
for L,S,E,q,r,ss in itertools.product([2,3,4,5],[27,28,29],[F(0),F('.005'),F('.01'),F('.015')],[-1,0,1],rs,slowsets):
 i=34;j=i-1;v=[F(100)]*45;v[j-L]=F(100)/(1+r)
 for h,x in zip([S-1,S,S+1],ss):v[j-h]=F(100)/(1+x)
 H=F('.025');desired=-1 if r>H else 1 if r < -H else 1 if q==1 and r<E else -1 if q==-1 and r> -E else 0;allowed=1 if sum(x>0 for x in ss)>=2 else -1 if sum(x<0 for x in ss)>=2 else 0;expected=desired if q!=0 and desired==q else desired if desired==allowed else 0
 a=engine.majority_target(v,i,L,float(H),q,float(E),S,trend_gate_application='entries_only');assert a[0]==expected and F(a[1])==r and F(a[2])==sorted(ss)[1],(L,S,E,q,r,ss,a,expected)
 w=v[:];w[i:]=[F(999)]*(len(v)-i);assert engine.majority_target(w,i,L,float(H),q,float(E),S,trend_gate_application='entries_only')==a
 if E==0:
  assert a==old.majority_target(v,i,L,float(H),q,0,S,trend_gate_application='entries_only');assert engine.majority_target(v,i,L,float(H),q,0,S)==old.majority_target(v,i,L,float(H),q,0,S);regress+=2
 if E>0 and q and ((q==1 and 0<=r<E) or (q==-1 and -E<r<=0)):assert a[0]==q;overshoots+=1
 n+=1
assert n==9360 and regress==4680 and overshoots>0
for E,mode in [(-.005,'entries_only'),(.025,'entries_only'),(.03,'entries_only'),(.005,'entries_and_retention')]:
 try:engine.majority_target([F(100)]*45,34,3,.025,1,E,28,trend_gate_application=mode)
 except AssertionError:pass
 else:raise AssertionError(('invalid exit buffer accepted',E,mode))
def fs(s):return {x.name:ast.get_source_segment(s,x) for x in ast.parse(s).body if isinstance(x,ast.FunctionDef)}
a,b=fs(src.read_text()),fs((R/'engine.py').read_text());changed=[k for k in a if a[k]!=b[k]];assert a.keys()==b.keys() and changed==['majority_target']
x={'passed':True,'source_path':str(src.relative_to(ROOT)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'new_sha256':hashlib.sha256((R/'engine.py').read_bytes()).hexdigest(),'changed_functions':changed,'all_other_functions_byte_identical':True,'synthetic_cases':n,'default_old_rule_regression_checks':regress,'future_invariance_checks':n,'actual_position_overshoot_retention_cases':overshoots,'invalid_parameter_rejections_checked':4,'no_market_PnL':True};(R/'engine_change_verification.json').write_text(json.dumps(x,indent=2)+'\n');print('PASS',n,'exact E/entry/slow/state/future boundaries;',regress,'old E0 regressions;changed only',changed)
