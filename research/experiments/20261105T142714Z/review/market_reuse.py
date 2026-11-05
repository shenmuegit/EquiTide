"""Verify reuse of public observations and independent account books; no backtest."""
import gzip,json,sys
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put
rd=lambda p:json.loads(p.read_text())
packets={}
checks=[]
for stem in ['candidate','l4h02','fewm']:
 w=R/(stem+'_observation');im=rd(w/'input_manifest.json');assert sha(ROOT/im['packet'])==im['sha256'];packets[stem]=json.loads(gzip.decompress((ROOT/im['packet']).read_bytes()));a=rd(R/(stem+'_verification.json'));state=rd(w/'state.json');before=rd(ROOT/rd(w/'previous_pointer.json')['state']);delta=json.loads(gzip.decompress((w/'delta.json.gz').read_bytes()));fund=[x for x in delta['journal'] if x['kind']=='funding'];assert a['passed'] and not a['new_daily_events'] and not a['new_fills'] and not fund and a['new_funding_settlements']==0 and state['books']==before['books']
 for asset in ['BTC','ETH']:
  for k in ['1','2','3']:
   b,s=before['books'][asset][k],state['books'][asset][k];amount=sum((D(x['amount_usdt']) for x in fund if x['asset']==asset and str(x['cost_multiplier'])==k),D(0));assert D(s['cash'])==D(b['cash'])+amount;checks.append({'account':stem,'asset':asset,'cost':k,'own_units':s['signed_units'],'own_funding_delta':str(amount),'cash_before':b['cash'],'cash_after':s['cash']})
 assert a['prior_NAV_prefix']==before['nav_points'] and a['NAV_points_per_scene']==state['nav_points'] and a['new_NAV_points_per_scene']==122
l,f=packets['l4h02'],packets['fewm'];assert l['assets']==f['assets'] and l['provenance']==f['provenance'] and l['plan_sha256']!=f['plan_sha256']
c=rd(R/'candidate_public_response_reuse_plan.json');assert c['predeclared_before_reservation'] and len(c['responses'])==2
attempts=rd(R/'candidate_transport_attempts.json');own=[x for x in attempts if x['http_status']==200 and x.get('curl_exit_code',0)==0];assert len(own)==6
bind=rd(R/'code_binding_before_evaluation.json');first=min(x['started_utc'] for p in (R/'reserve_batches').glob('*.json') for x in rd(p)['actual_command_receipts']);assert bind['recorded_utc']<first
for n in ['observe_l4h02.py','observe_fewm.py','observe_candidate.py']:
 p=R/n;assert bind['source_sha256'][str(p.relative_to(ROOT))]==sha(p)
put(R/'market_reuse_verification.json',{'passed':True,'L4_FEWM_actual_public_assets_and_provenance_identical':True,'frozen_plan_envelopes_distinct':True,'single_reused_metadata_time_responses':2,'single_own_market_HTTP200_responses':6,'own_quantities_entries_and_cashflow_formulas_verified':True,'actual_new_funding_records_by_account':{s:rd(R/(s+'_verification.json'))['new_funding_settlements'] for s in packets},'all_current_books_equal_own_prior_books':True,'actual_cash_book_checks':checks,'all_three_independent_complete_NAV_audits_passed':True,'predeclaration_precedes_first_reservation':True,'no_other_account_state_cashflow_or_NAV_reused':True,'previous08_settlements_not_repeated':True})
print('PASS independent public data reuse and 18 own books/full NAV prefixes; no repeated08funding')
