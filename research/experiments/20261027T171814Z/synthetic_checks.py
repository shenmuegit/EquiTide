"""Synthetic only: strict thresholds, state persistence, new slow gates and no future close."""
from decimal import Decimal as D
from fractions import Fraction as F
from run import ROOT,R,sha,put
import engine
base=ROOT/'research/experiments/20261027T151819Z/engine.py';assert (R/'engine.py').read_text().replace('trend_lookback_days in [7,14,21,22,25,26,27,28,29,30,31]','trend_lookback_days in [7,14,21,22,25,26,27,28,31]')==base.read_text();checks=0
for L in [3,4,5]:
 for S in [29,30]:
  prices=[D(100)]*65;i=64;prices[i-1-S]=D(120);prices[i-1]=D(103);a=engine.target(prices,i,L,.02,0,0,S);assert a[0]==-1 and F(a[1])==F(3,100);prices[i]=D(999999999);assert engine.target(prices,i,L,.02,0,0,S)==a;checks+=2
  prices[i-1]=D(102);assert engine.target(prices,i,L,.02,0,0,S)[0]==0;prices[i-1]=D(101);assert engine.target(prices,i,L,.02,-1,0,S)[0]==-1;prices[i-1]=D(100);assert engine.target(prices,i,L,.02,-1,0,S)[0]==0;checks+=3
  prices[i-1]=D(97);prices[i-1-S]=D(90);assert engine.target(prices,i,L,.02,0,0,S)[0]==1;prices[i-1-S]=D(97);assert engine.target(prices,i,L,.02,1,0,S)[0]==0;checks+=2
put(R/'synthetic_checks.json',{'passed':True,'synthetic_only':True,'financial_results_created':0,'checks':checks,'signals_exact_and_no_future_close_dependency':True,'only_engine_change':'Permit slow29/30;all signal/order/funding/risk/metrics otherwise byteidentical','base_engine_sha256':sha(base),'new_engine_sha256':sha(R/'engine.py')});print('PASS:42 synthetic-only strictthreshold/persistence/slowgate/causality checks;no backtest/account/order.')
