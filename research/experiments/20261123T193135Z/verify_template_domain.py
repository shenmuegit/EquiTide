from common import *
import ast
P=ROOT/'research/experiments/20261123T173139Z'
assert all(sha(R/n)==sha(P/n) for n in ['engine.py','core391_tail_safe.py','market.py','portfolio.py','audit_native.py'])
assert all(json.loads((R/n).read_text())['passed'] for n in ['parent_primitive_verification.json','sizing_primitive_verification.json'])
put(R/'engine_domain_unit_verification.json',{'passed':True,'recorded_utc':now(),'five_accounting_kernels_byteexact_compared':True,'no_new_native_model_execution':True,'prior_synthetic_evidence_reused_without_relabeling':rel(P/'engine_domain_unit_verification.json'),'current_parent_synthetic_arithmetic_and_alignment_checks':True,'no_market_or_account_calculations':True})
identity=json.loads((R/'SMA_original_daily_kernel_identity.json').read_text());assert identity['passed'] and identity['simulate_AST_exact'] and identity['validate_AST_exact'] and sha(R/'forward.py')==identity['current_sha256']
put(R/'daily_template_verification.json',{'passed':True,'recorded_utc':now(),'current_source':rel(R/'forward.py'),'current_sha256':sha(R/'forward.py'),'original_daily_arithmetic_unchanged':True,'current_original_daily_events_by_account':{a:len(json.loads((R/'account_windows.json').read_text())[a]['expected_daily_events_utc']) for a in ['SMA','candidate','l4h02','fewm']}})
print('PASS five financial kernels and original daily SMA simulator/validator AST unchanged')
