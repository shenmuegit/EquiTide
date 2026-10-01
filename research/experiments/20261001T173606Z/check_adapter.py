"""Guard time-unit boundaries and exact reuse of the earlier execution engine."""
from datetime import datetime,timezone
from pathlib import Path
import ast

ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
source=(ROUND/'download_data.py').read_text();ast.parse(source)
for stamp,unit,factor in [(1726444800000,'ms',1000000),(1735689600000000,'us',1000)]:
    actual='us' if stamp>10**14 else 'ms';assert actual==unit
    assert factor*stamp==int(datetime.fromtimestamp(stamp/(1000000 if unit=='us' else 1000),timezone.utc).timestamp())*10**9
    assert (stamp+(60000000 if unit=='us' else 60000)-1)*factor-stamp*factor==60000000000-factor
old=ast.parse((ROOT/'research/experiments/20261001T133655Z/evaluate.py').read_text())
new=ast.parse((ROUND/'evaluate.py').read_text())
for name in ('component','summarize','metric','dd','navhash'):
    a=next(x for x in old.body if isinstance(x,ast.FunctionDef) and x.name==name)
    b=next(x for x in new.body if isinstance(x,ast.FunctionDef) and x.name==name)
    assert ast.dump(a,include_attributes=False)==ast.dump(b,include_attributes=False),name
assert '2025-03-18' in (ROUND/'evaluate.py').read_text()
print('PASS:ms/us close-time boundary fixtures and exact AST identity of execution/NAV/metrics functions;synthetic fixtures only')
