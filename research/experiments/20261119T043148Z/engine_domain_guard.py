"""Before any reserve, independently verify the only engine AST difference is the H allowlist."""
import ast,copy,json
from common import *
P=ROOT/'research/experiments/20261119T023142Z';b=json.loads((R/'engine_domain_extension_binding.json').read_text());old=ast.parse((P/'engine.py').read_text());new=ast.parse((R/'engine.py').read_text());assert sha(P/'engine.py')==b['old_engine_sha256'] and sha(R/'engine.py')==b['new_engine_sha256'] and sha(R/'core391_tail_safe.py')==sha(P/'core391_tail_safe.py')==b['native_accounting_sha256']
class RestoreDomain(ast.NodeTransformer):
 def __init__(self):self.count=0
 def visit_Compare(self,node):
  self.generic_visit(node)
  if isinstance(node.left,ast.Name) and node.left.id=='H' and len(node.ops)==1 and isinstance(node.ops[0],ast.In) and len(node.comparators)==1 and isinstance(node.comparators[0],ast.List):
   assert ast.literal_eval(node.comparators[0])==b['new_H_allowlist'];node.comparators[0].elts=[ast.Constant(value=v) for v in b['old_H_allowlist']];self.count+=1
  return node
restore=RestoreDomain();normalized=restore.visit(copy.deepcopy(new));assert restore.count==1 and ast.dump(normalized,include_attributes=False)==ast.dump(old,include_attributes=False)
records=reg.read_records(ROOT/'research/automation/registry.jsonl');batch=json.loads((R/'batch.json').read_text());assert all(x['fingerprint'] not in records for x in batch) and not(R/'reserve_0_commands.json').exists()
assert json.loads((R/'units_commands.json').read_text())[-1]['exit_code']==1
put(R/'engine_domain_guard_verification.json',{'passed':True,'verified_utc':now(),'binding_sha256':sha(R/'engine_domain_extension_binding.json'),'old_engine_sha256':sha(P/'engine.py'),'new_engine_sha256':sha(R/'engine.py'),'changed_H_membership_nodes':restore.count,'adding_only_preregistered_H_values':b['added_numeric_domain_values'],'engine_AST_identical_after_restoring_only_domain_list':True,'every_calculation_formula_and_branch_unchanged':True,'native_accounting_bytes_identical':True,'original_account_kernels_untouched':True,'before_any_new_financial_reservation':True,'financial_evaluations':0,'initial_native_failure_retained':True});print('PASS only one scalar H domain allowlist differs;all mathematical/accounting AST and original accounts unchanged;zero reservations/evaluations')
