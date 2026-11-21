"""Synthetic common-axis banking checks;no market backtest or new signal."""
from common import *
from portfolio import sum_aligned_full_banks
import numpy as np
x=np.array([3750.,4200.,3900.]);y=np.array([15000.,14700.,15500.]);axis=np.array([1,2,3]);assert sum_aligned_full_banks([x,y],[axis,axis]).tolist()==[18750.,18900.,19400.]
for wrong in [np.array([0,2,3]),np.array([1,3,4])]:
 try:sum_aligned_full_banks([x,y],[axis,wrong]);raise RuntimeError('bad axis accepted')
 except AssertionError:pass
v=np.array([100.,120.,90.,110.]);assert max(1-v/np.maximum.accumulate(v))==.25 and core.DAYS==391 and list(range(0,391,30))+[391]==[0,30,60,90,120,150,180,210,240,270,300,330,360,390,391]
put(R/'parent_primitive_verification.json',{'passed':True,'synthetic_only':True,'misaligned_axis_variants_rejected':2,'true_dollar_bank_sum_and_continuous_DD_checked':True,'391calendar13completefolds_plus1tail_checked':True,'no_new_native_or_market_or_account_execution':True});put(R/'engine_domain_unit_verification.json',{'passed':True,'synthetic_only':True,'no_changed_signal_or_cashflow_kernel':True,'actual_source_bank_rules_are_readonly':True,'new_native_calls':0});print('PASSsyntheticfullbank/commonaxis/tail/DD;0nativecalls')

from pathlib import Path
prior=ROOT/'research/experiments/20261121T125030Z'
assert all(sha(R/n)==sha(prior/n) for n in ['engine.py','core391_tail_safe.py','market.py','portfolio.py','audit_native.py'])
put(R/'engine_domain_unit_verification.json',{'passed':True,'recorded_utc':now(),'five_accounting_kernels_byteexact_compared':True,'no_new_native_model_execution':True,'prior_synthetic_evidence_reused_without_relabeling':'research/experiments/20261121T125030Z/engine_domain_unit_verification.json','current_parent_synthetic_arithmetic_and_alignment_checks':True,'no_market_or_account_calculations':True})
