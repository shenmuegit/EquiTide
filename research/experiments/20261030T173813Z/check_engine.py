"""Exhaustive nine-state vote fixtures and unchanged accounting AST proof."""
import ast
from run import ROOT,R,sha,put
import engine
old=ROOT/'research/experiments/20261030T153707Z/engine.py';a=ast.parse(old.read_text());b=ast.parse((R/'engine.py').read_text());fa={n.name:n for n in a.body if isinstance(n,ast.FunctionDef)};fb={n.name:n for n in b.body if isinstance(n,ast.FunctionDef)};unchanged=[n for n in fa if n not in ['target','simulate']]
assert set(fa)==set(fb) and all(ast.dump(fa[n],include_attributes=False)==ast.dump(fb[n],include_attributes=False) for n in unchanged)
cases=future=0
for E in [5,6,7]:
 for H in [2,3,4]:
  for pos in range(10):
   for neg in range(10-pos):
    flat=9-pos-neg;v=[(0,0,9)]*404;v[33]=(pos,neg,flat)
    for actual in [-1,0,1]:
     allowed=[s for s,n in [(1,pos),(-1,neg)] if n>=E];assert len(allowed)<=1
     expected=allowed[0] if allowed else actual if actual!=0 and {1:pos,-1:neg}[actual]>=H else 0
     got,proof=engine.target(v,33,E,H,actual);assert got==expected and proof['final_direction']==expected and proof['source_targets_known_before_execution'] and proof['long_votes']+proof['short_votes']+proof['flat_votes']==9
     changed=v[:34]+[(9,0,0)]*370;assert engine.target(changed,33,E,H,actual)==(got,proof);cases+=1;future+=1
assert cases==1485 and future==1485
put(R/'engine_change_verification.json',{'passed':True,'base_engine_sha256':sha(old),'new_engine_sha256':sha(R/'engine.py'),'unchanged_accounting_functions':unchanged,'unchanged_accounting_AST':True,'synthetic_vote_and_priority_fixtures':cases,'synthetic_future_vote_mutations':future,'majority_no_conflicting_entries':True,'retention_equality_preserved':True,'new_native_cells_planned':18,'financial_evaluations':0});print('PASS1485vote/1485futurecases,majority/retention equality/reversal/flat,accountingASTunchanged')
