"""Synthetic-only target/domain checks; no price history, account or return evaluation."""
import importlib.util,json,hashlib
from pathlib import Path
from fractions import Fraction as F
import engine
R=Path(__file__).resolve().parent;ROOT=R.parents[2];basepath=ROOT/'research/experiments/20261025T185633Z/engine.py';raw=basepath.read_text();changed=(R/'engine.py').read_text();assert changed.replace('trend_lookback_days in [7,14,21,28,31]','trend_lookback_days in [7,14,28]')==raw
spec=importlib.util.spec_from_file_location('immutable_gate_rule',basepath);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
paths=[[F(100)]*35,[F(100+x) for x in range(35)],[F(150-x) for x in range(35)],[F(100+x) for x in range(30)]+[F(130),F(125),F(120),F(9999),F(1)],[F(150-x) for x in range(30)]+[F(120),F(125),F(130),F(1),F(9999)]];checks=oldchecks=0
for values in paths:
 for S in [7,14,21,28,31]:
  for L in [1,2,3]:
   for H in [.02,.04,.06]:
    for current in [-1,0,1]:
     i=33;j=i-1;r=values[j]/values[j-L]-1;slow=values[j]/values[j-S]-1;h=F(str(H));base=-1 if r>h else 1 if r< -h else 1 if current==1 and r<0 else -1 if current==-1 and r>0 else 0;allowed=1 if slow>0 else -1 if slow<0 else 0;want=base if base==allowed else 0
     got=engine.target(values,i,L,H,current,0,S);assert got==(want,str(r),str(slow)) and got==engine.target(values[:i]+[F(10**20),F(1,10**20)],i,L,H,current,0,S);checks+=1
     if S in [7,14,28]:assert got==old.target(values,i,L,H,current,0,S);oldchecks+=1
try:engine.target(paths[0],31,3,.02,0,0,31)
except AssertionError:pass
else:raise AssertionError('negative feature index accepted')
out={'passed':True,'scope':'Only artificial close vectors, exactFraction gate/causality regression, no actual financial configuration or account.','synthetic_targets_checked':checks,'old_supported_S_results_exactly_equal':oldchecks,'new_S_supported':[21,31],'no_future_feature_or_negative_index':True,'engine_only_changed_domain_assertion':True,'base_engine_sha256':hashlib.sha256(basepath.read_bytes()).hexdigest(),'new_engine_sha256':hashlib.sha256((R/'engine.py').read_bytes()).hexdigest(),'new_financial_evaluations':0};(R/'engine_domain_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
