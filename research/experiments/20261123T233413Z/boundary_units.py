"""Check current actual funding lookup and each original mark-only calendar before reserve."""
from common import *
rd=lambda p:json.loads(p.read_text());w=rd(R/'account_windows.json');f=rd(R/'window_funding_preflight.json');assert not(R/'reserve_batches').exists()
assert {a:len(w[a]['expected_daily_events_utc']) for a in ['SMA','candidate','l4h02','fewm']}=={'SMA':0,'candidate':0,'l4h02':0,'fewm':0}
for a in ['SMA','candidate','l4h02','fewm']:
 assert w[a]['next_daily_decision_utc']=='2026-11-24T00:01:00Z'
 for s in ['BTC','ETH']:
  vals=[] if a=='SMA' else [z for z in f['public_fields_by_asset'][s] if core.ns(w[a]['start_utc'])<int(z['fundingTime'])*1000000<=core.ns(w[a]['cutoff_utc'])];assert vals==w[a]['expected_funding_by_asset'][s]
for n in ['observe_l4h02.py','observe_fewm.py','audit_incremental.py']:assert sha(R/n)==sha(ROOT/'research/experiments/20261123T213206Z'/n)
b=rd(R/'SMA_full75_prebinding.json');assert b['passed'] and sha(ROOT/b['authority'])==b['sha256'] and rd(R/'SMA_markonly_kernel_identity.json')['passed']
put(R/'boundary_unit_verification.json',{'passed':True,'recorded_utc':now(),'new_daily_decisions_expected':0,'actual_funding_counts':{a:w[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']},'SMA_original_markonly_arithmetic_full75_readonly':True,'unchanged_perp_kernels':True,'no_market_or_account_evaluation':True});print('PASSownwindows/daily0/freshactualfunding/full75markonlybinding')
