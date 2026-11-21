from common import *
import ast
P=ROOT/'research/experiments/20261121T165204Z'
assert all(sha(R/n)==sha(P/n) for n in ['engine.py','core391_tail_safe.py','market.py','portfolio.py','audit_native.py'])
assert all(json.loads((R/n).read_text())['passed'] for n in ['parent_primitive_verification.json','sizing_primitive_verification.json'])
put(R/'engine_domain_unit_verification.json',{'passed':True,'recorded_utc':now(),'five_accounting_kernels_byteexact_compared':True,'no_new_native_model_execution':True,'prior_synthetic_evidence_reused_without_relabeling':rel(P/'engine_domain_unit_verification.json'),'current_parent_synthetic_arithmetic_and_alignment_checks':True,'no_market_or_account_calculations':True})
a=ast.parse((R/'forward.py').read_text());b=ast.parse((ROOT/'research/experiments/20261121T145102Z/forward.py').read_text());assert ast.dump(a)==ast.dump(b).replace('SMA_full72_prebinding','SMA_full73_prebinding').replace('already completed Nov20 daily','already completed Nov21 daily')
put(R/'mark_only_template_verification.json',{'passed':True,'current_source':rel(R/'forward.py'),'current_sha256':sha(R/'forward.py'),'prior_markonly_source':'research/experiments/20261121T145102Z/forward.py','AST_unchanged_except_full73_authority_key_and_completed_day_label':True,'current_original_daily_events_all4':0,'current_mark_only_original_Float_cash_units_desired_costs_kernel_unchanged':True})
print('PASSfiveaccountingkernels/sourceidentity/syntheticparents/markonlyAST')
