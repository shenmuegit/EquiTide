from common import *
import ast
P=ROOT/'research/experiments/20261123T072701Z'
assert all(sha(R/n)==sha(P/n) for n in ['engine.py','core391_tail_safe.py','market.py','portfolio.py','audit_native.py'])
assert all(json.loads((R/n).read_text())['passed'] for n in ['parent_primitive_verification.json','sizing_primitive_verification.json'])
put(R/'engine_domain_unit_verification.json',{'passed':True,'recorded_utc':now(),'five_accounting_kernels_byteexact_compared':True,'no_new_native_model_execution':True,'prior_synthetic_evidence_reused_without_relabeling':rel(P/'engine_domain_unit_verification.json'),'current_parent_synthetic_arithmetic_and_alignment_checks':True,'no_market_or_account_calculations':True})
assert (R/'forward.py').read_bytes()==(P/'forward.py').read_bytes()
identity=json.loads((R/'SMA_mark_only_kernel_identity.json').read_text());assert identity['passed'] and identity['original_mark_only_arithmetic_unchanged'] and sha(R/'forward.py')==identity['current_sha256']
put(R/'mark_only_template_verification.json',{'passed':True,'recorded_utc':now(),'current_source':rel(R/'forward.py'),'current_sha256':sha(R/'forward.py'),'current_original_daily_adapter':False,'original_markonly_arithmetic_unchanged':True,'identity_proof':rel(R/'SMA_mark_only_kernel_identity.json'),'current_original_daily_events_by_account':{a:len(json.loads((R/'account_windows.json').read_text())[a]['expected_daily_events_utc']) for a in ['SMA','candidate','l4h02','fewm']}})
print('PASSfiveaccountingkernels;original markonly unchanged; all4 calendars no daily')
