"""Engineering-only causal/boundary checks; synthetic values are not financial evidence."""
from decimal import Decimal as D
import math,statistics
import engine
def main():
 values=[D(str(100*math.exp(.02*i+.015*(-1)**i))) for i in range(45)];i=34
 for w in [10,20,30]:
  rr=[math.log(float(values[j])/float(values[j-1])) for j in range(i-w,i)];expected=statistics.stdev(rr)*math.sqrt(365);assert engine.lagged_annualized_volatility(values,i,w)==expected
  mutated=list(values);mutated[i:]=[D(999999)]*(len(values)-i);assert engine.lagged_annualized_volatility(mutated,i,w)==expected
  p={'lookback_days':31,'return_hurdle':.04,'exit_buffer_fraction':.01,'volatility_lookback_days':w,'annualized_volatility_cap':expected};wanted,r,raw,vol,allowed=engine.gated_target(values,i,p,1);assert raw==1 and wanted==1 and allowed and vol==expected
  p['annualized_volatility_cap']=math.nextafter(expected,0);wanted,r,raw,vol,allowed=engine.gated_target(values,i,p,1);assert raw==1 and wanted==0 and not allowed
  assert engine.gated_target(mutated,i,p,-1)==engine.gated_target(values,i,p,-1)
 try:engine.lagged_annualized_volatility(values,30,30)
 except AssertionError:pass
 else:raise AssertionError('W+1 prior closes boundary must fail')
 print('PASS:priorW+1closes-only,sampleSDsqrt365,equalitypermitsrisk,strictlyaboveflat,futuremutationsinvariant,insufficientcontextguard;syntheticengineeringonly')
if __name__=='__main__':main()
