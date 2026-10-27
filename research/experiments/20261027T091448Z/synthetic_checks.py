"""Synthetic only: longer-lookback causality, strict thresholds and trend gating."""
from decimal import Decimal as D
from fractions import Fraction as F
import json
from run import ROOT,R,sha,put
import engine
base=ROOT/'research/experiments/20261026T190909Z/engine.py';assert (R/'engine.py').read_text().replace('look in [1,2,3,4,5]','look in [1,2,3]')==base.read_text();checks=0
for L in [4,5]:
 for S in [28,31]:
  prices=[D(100)]*65;i=64;prices[i-1-S]=D(120);prices[i-1]=D(103);a=engine.target(prices,i,L,.02,0,0,S);assert a[0]==-1 and F(a[1])==F(3,100);prices[i]=D(999999999);assert engine.target(prices,i,L,.02,0,0,S)==a;checks+=2
  prices[i-1]=D(102);assert engine.target(prices,i,L,.02,0,0,S)[0]==0;prices[i-1]=D(101);assert engine.target(prices,i,L,.02,-1,0,S)[0]==-1;prices[i-1]=D(100);assert engine.target(prices,i,L,.02,-1,0,S)[0]==0;checks+=3
  prices[i-1]=D(97);prices[i-1-S]=D(90);assert engine.target(prices,i,L,.02,0,0,S)[0]==1;prices[i-1-S]=D(97);assert engine.target(prices,i,L,.02,1,0,S)[0]==0;checks+=2
put(R/'synthetic_checks.json',{'passed':True,'synthetic_only':True,'financial_results_created':0,'checks':checks,'signals_exact_and_no_future_close_dependency':True,'only_engine_change':'Add4/5 to permittedlookbacks;all signal/order/funding/risk/metrics code otherwise byteidentical','base_engine_sha256':sha(base),'new_engine_sha256':sha(R/'engine.py')});print('PASS:synthetic-only28 strictthreshold/persistence/slowgate/causality checks;no backtest result or order.')
