"""Causalchannel,self-inclusion,ties/exit/reversalfixtures; allaccountingfunctionsexactlegacyAST."""
import ast
from decimal import Decimal as D
from run import ROOT,R,sha,put
import engine
old=ROOT/'research/experiments/20261030T073235Z/engine.py';a=ast.parse(old.read_text());b=ast.parse((R/'engine.py').read_text());fa={n.name:n for n in a.body if isinstance(n,ast.FunctionDef)};fb={n.name:n for n in b.body if isinstance(n,ast.FunctionDef)};unchanged=[n for n in fa if n not in ['target','simulate']]
assert set(fa)==set(fb) and all(ast.dump(fa[n],include_attributes=False)==ast.dump(fb[n],include_attributes=False) for n in unchanged)
fixtures=causal=0
for N in [20,25,30]:
 for M in [5,10,15]:
  j=32;assert j-N>=0 and M<N
  for typ in ['flat','up','down','long_exit','short_exit']:
   v=[D(100)]*70
   if typ=='up':v[j]=D(101)
   if typ=='down':v[j]=D(99)
   if typ=='long_exit':v[j-N]=D(90);v[j]=D(95)
   if typ=='short_exit':v[j-N]=D(110);v[j]=D(105)
   for current in [-1,0,1]:
    got,bounds=engine.target(v,33,N,M,current);expected=(1 if typ=='up' else -1 if typ=='down' else 0 if typ=='long_exit' and current==1 or typ=='short_exit' and current==-1 else current);assert got==expected and bounds['entry_end_exclusive']==j and bounds['entry_start_index']==j-N and bounds['channels_exclude_tested_close']
    future=v[:33]+[D(999999)]*(len(v)-33);assert engine.target(future,33,N,M,current)==(got,bounds);fixtures+=1;causal+=1
assert fixtures==135 and causal==135;put(R/'engine_change_verification.json',{'passed':True,'base_engine_sha256':sha(old),'new_engine_sha256':sha(R/'engine.py'),'unchanged_accounting_functions':unchanged,'unchanged_accounting_AST':True,'synthetic_channel_and_priority_fixtures':fixtures,'synthetic_future_price_mutations':causal,'tested_close_excluded_from_channel':True,'new_native_cells_planned':18,'financial_evaluations':0});print('PASS135channel/135futurecases,self-exclusion/tie/exit/reversal,unchangedaccountingAST')
