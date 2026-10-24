"""Synthetic rule/boundary causality tests and unchanged accounting source contract."""
import ast,hashlib,json
from decimal import Decimal as D
from fractions import Fraction as F
import engine
from run import ROOT,R,module
def main():
 path=ROOT/'research/experiments/20261023T184400Z/engine.py';old=module(path,'old_zeroexit_contract');before=path.read_text();after=(R/'engine.py').read_text();a={x.name:ast.get_source_segment(before,x) for x in ast.parse(before).body if isinstance(x,ast.FunctionDef)};b={x.name:ast.get_source_segment(after,x) for x in ast.parse(after).body if isinstance(x,ast.FunctionDef)};assert a.keys()==b.keys()
 for name in a.keys()-{'target','simulate'}:assert a[name]==b[name],name
 expected=a['simulate'].replace("1 if D(state['signed_units'])>0 else -1 if D(state['signed_units'])<0 else 0);q=", "1 if D(state['signed_units'])>0 else -1 if D(state['signed_units'])<0 else 0,p['exit_buffer_fraction']);q=");assert expected==b['simulate']
 n=0
 for H in [.01,.02,.04]:
  for E in [0,.0025,.005,.01]:
   for current in [-1,0,1]:
    for r in [F(-1,10),-F(str(H)),-F(str(E))-F(1,10**7),-F(str(E)),-F(str(E))+F(1,10**7),F(0),F(str(E))-F(1,10**7),F(str(E)),F(str(E))+F(1,10**7),F(str(H)),F(1,10)]:
     values=[D(100),D(100)*(1+D(r.numerator)/D(r.denominator))];result,roc=engine.target(values,2,1,H,current,E);h,e=F(str(H)),F(str(E));want=1 if r>h else -1 if r<-h else 1 if current==1 and r>-e else -1 if current==-1 and r<e else 0;assert result==want and F(roc)==r
     assert engine.target(values+[D('0.0000001'),D('9999999999')],2,1,H,current,E)==(result,roc)
     if E==0:assert (result,roc)==old.target(values,2,1,H,current)
     n+=1
 # Entry priority, opposite transition and exact equality must not be weakened.
 assert engine.target([D(100),D('99.5')],2,1,.02,1,.005)[0]==0
 assert engine.target([D(100),D('99.50001')],2,1,.02,1,.005)[0]==1
 assert engine.target([D(100),D('100.5')],2,1,.02,-1,.005)[0]==0
 assert engine.target([D(100),D('97.99')],2,1,.02,1,.005)[0]==-1
 assert engine.target([D(100),D('102.01')],2,1,.02,-1,.005)[0]==1
 print(json.dumps({'passed':True,'synthetic_cases':n,'zero_buffer_exactly_matches_existing_rule':True,'strict_entry_and_exit_equalities_verified':True,'future_tail_cannot_change_current_target':True,'only_target_and_parameter_passing_changed':True,'unchanged_source_functions':sorted(a.keys()-{'target','simulate'}),'source_original_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'synthetic_only_not_backtest_results':True}),flush=True)
if __name__=='__main__':main()
