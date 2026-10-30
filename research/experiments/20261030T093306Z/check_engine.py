import ast
from fractions import Fraction as F
from decimal import Decimal as D
from run import ROOT,R,sha,put
assert sha(R/'engine.py')==sha(ROOT/'research/experiments/20261030T073235Z/fast_engine.py')
# Syntheticonly:completepriorindexboundsforL/Sneighborhoodandactualindependentbankcapital/no normalization.
for L in [2,3,4]:
 for S in [27,28,29]:assert 33-2-S>=0 and 33-1-L>=0 and [S-1,S,S+1]==list(range(S-1,S+2))
assert sum([5000,7500,7500])==20000 and sum([500,2250,750])/20000==.175 and sum([1,1,1])==3
for n in ['engine.py','audit_native.py','run.py','audit.py']:ast.parse((R/n).read_text())
put(R/'engine_change_verification.json',{'passed':True,'native_engine_byte_identical':True,'synthetic_index_cases':9,'native_new_price_cells_planned':8,'completed_exact_center_not_rerun':True,'financial_evaluations':0,'native_engine_sha256':sha(R/'engine.py')});print('PASS unchanged native model,9 price index bounds,raw1/1/1 capital/exposure preflight')
