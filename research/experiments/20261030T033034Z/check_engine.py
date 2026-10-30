"""Unchanged proven momentum accounting and synthetic strict/hysteresis timing checks."""
from decimal import Decimal as D
from fractions import Fraction as F
from run import ROOT,R,sha,put
import engine
P=ROOT/'research/experiments/20261030T013003Z';assert sha(R/'engine.py')==sha(R/'btc_engine.py')==sha(P/'btc_engine.py')
tests=0
for L in [20,25,30]:
 for H in [.02,.04,.06]:
  for price in [D(90),D(99),D(100),D(101),D(110)]:
   values=[D(100)]*34+[price]
   for current in [-1,0,1]:
    r=F(price)/100-1;h=F(str(H));e=F('.01');expected=1 if r>h else -1 if r<-h else 1 if current==1 and r>-e else -1 if current==-1 and r<e else 0;out=engine.target(values,35,L,H,current,.01);assert out==(expected,str(r)) and out==engine.target(values+[D(100000)],35,L,H,current,.01);tests+=1
put(R/'engine_change_verification.json',{'passed':True,'financial_evaluations':0,'engine_source_unchanged':True,'source_round':P.name,'engine_sha256':sha(R/'engine.py'),'BTC_engine_sha256':sha(R/'btc_engine.py'),'synthetic_strict_hysteresis_future_append_checks':tests});print('PASS unchanged momentum engine;',tests,'synthetic signal/timingchecks')
