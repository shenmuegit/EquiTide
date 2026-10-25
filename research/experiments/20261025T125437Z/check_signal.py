"""Engineering-only signal boundary, persistence, flip and causal checks."""
from fractions import Fraction as F
import engine
def main():
 def check(prev,cur,h,state,want):
  v=[F(prev),F(cur),F(9999)];d,r=engine.target(v,2,1,h,state,0);assert d==want and F(r)==F(cur)/F(prev)-1
 check(100,102,.02,0,0);check(100,98,.02,0,0)
 check(100,103,.02,0,-1);check(100,97,.02,0,1)
 check(100,99,.02,1,1);check(100,101,.02,-1,-1)
 check(100,100,.02,1,0);check(100,100,.02,-1,0)
 check(100,101,.02,1,0);check(100,99,.02,-1,0)
 check(100,103,.02,1,-1);check(100,97,.02,-1,1)
 v=[F(100+i%4) for i in range(12)];i=7
 for L in [1,2,3]:
  for H in [.02,.04,.06]:
   for state in [-1,0,1]:
    want=engine.target(v,i,L,H,state,0);changed=list(v);changed[i:]=[F(999999)]*(len(v)-i);assert engine.target(changed,i,L,H,state,0)==want
 try:engine.target(v,2,3,.02,0,0)
 except AssertionError:pass
 else:raise AssertionError('Missing completed historical close must fail')
 print('PASS:strictsymmetricentry,equalitynoentry,contrariandirection,retainonlysameROCsign,zeroequalityexit,oppositeextremeflip,futureclosesinvariant,historyguard;syntheticengineeringonly')
if __name__=='__main__':main()
