"""Synthetic-only rule boundaries, actual-position persistence and future invariance."""
from decimal import Decimal as D
from fractions import Fraction as F
import ast
from pathlib import Path
import engine

def case(last,short_past,slow_past,held,expected,h='.02',S=7):
 v=[D(100)]*40;v[32]=D(last);v[31]=D(short_past);v[32-S]=D(slow_past);got,r,slow=engine.target(v,33,1,float(h),held,0,S);assert got==expected and F(r)==F(v[32])/F(v[31])-1 and F(slow)==F(v[32])/F(v[32-S])-1
 v[33:]=[D(999999)]*7;assert engine.target(v,33,1,float(h),held,0,S)==(got,r,slow)
for S in [7,14,28]:
 for args in [('100','110','80',0,1),('100','90','120',0,-1),('100','90','80',-1,0),('100','110','120',1,0),('100','110','100',1,0),('100','100','80',1,0),('100','100','120',-1,0),('99','100','80',1,1),('99','100','80',0,0),('101','100','120',-1,-1),('102','100','120',0,0),('102','100','120',-1,-1),('98','100','80',0,0),('98','100','80',1,1)]:case(*args,S=S)
base=ast.parse((Path(__file__).resolve().parents[1]/'20261025T165608Z/engine.py').read_text());new=ast.parse(Path(engine.__file__).read_text());a={n.name:ast.dump(n) for n in base.body if isinstance(n,ast.FunctionDef)};b={n.name:ast.dump(n) for n in new.body if isinstance(n,ast.FunctionDef)};changed=[k for k in a if a[k]!=b[k]];assert changed==['target','simulate'];print('PASS:42 syntheticcases,threshold/ROCzero/slowzero/regimeforcedexit/currentstate/futureinvariance;onlytargetandsimulatecall+signalprovenancechanged,no marketbacktest')
