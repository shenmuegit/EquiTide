"""Exact real08.001 settlement fields, own ledgers and full chains; no account replay."""
import gzip,json,sys
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put
rd=lambda p:json.loads(p.read_text());pre=rd(R/'funding_preflight.json');receipts=rd(R/'funding_preflight_receipts.json');assert pre['account_or_strategy_calculations']==0;expected_ns=1794124800001000000;rows=[];counts={}
for receipt in receipts:
 assert sha(ROOT/receipt['raw'])==receipt['sha256'] and len(gzip.decompress((ROOT/receipt['raw']).read_bytes()))==receipt['bytes']
 for f in pre['public_fields_by_asset'][receipt['asset']]:assert int(f['fundingTime'])*1000000==expected_ns
for stem in ['candidate','l4h02','fewm']:
 W=R/(stem+'_observation');before=rd(ROOT/rd(W/'previous_pointer.json')['state']);state=rd(W/'state.json');v=rd(R/(stem+'_verification.json'));delta=json.loads(gzip.decompress((W/'delta.json.gz').read_bytes()));fund=[z for z in delta['journal'] if z['kind']=='funding'];counts[stem]=len(fund);assert v['passed'] and v['new_daily_events']==v['new_fills']==0 and len(fund)==(0 if stem=='candidate' else 6)
 for z in fund:
  a,k=z['asset'],str(z['cost_multiplier']);f=pre['public_fields_by_asset'][a][0];q=D(before['books'][a][k]['signed_units']);base=-q*D(f['markPrice'])*D(f['fundingRate']);amount=base*int(k) if base<0 else base;assert z['timestamp_ns']==expected_ns and z['timestamp_ns']!=1794124800000000000 and D(z['signed_units'])==q and D(z['rate'])==D(f['fundingRate']) and D(z['mark_price'])==D(f['markPrice']) and D(z['base_amount_usdt'])==base and D(z['amount_usdt'])==amount and D(z['cash_before'])==D(before['books'][a][k]['cash']) and D(z['cash_after'])==D(z['cash_before'])+amount;assert all(state['books'][a][k][field]==before['books'][a][k][field] for field in ['signed_units','entry_price','entry_reference']) and D(state['books'][a][k]['cash'])==D(z['cash_after']);rows.append({'account':stem,'asset':a,'cost':k,'actual_timestamp_ns':z['timestamp_ns'],'actual_rate':z['rate'],'actual_mark':z['mark_price'],'own_pre_settlement_q':str(q),'own_base_usdt':str(base),'own_amount_usdt':str(amount),'cash_before':z['cash_before'],'cash_after':z['cash_after']})
 point=rd(ROOT/('research/automation/'+stem+'_forward_latest.json'));seen=set();chain=[]
 while point:
  assert sha(ROOT/point['delta'])==point['delta_sha256'];journal=json.loads(gzip.decompress((ROOT/point['delta']).read_bytes()))['journal']
  for z in journal:
   if z['kind']=='funding' and z['timestamp_ns']==expected_ns:
    key=(z['asset'],str(z['cost_multiplier']));assert key not in seen;seen.add(key);chain.append(z)
  ref=point.get('previous_pointer');point=rd(ROOT/ref['path']) if ref else None
 assert len(chain)==(0 if stem=='candidate' else 6)
assert len(rows)==12 and counts=={'candidate':0,'l4h02':6,'fewm':6}
put(R/'actual08_funding_verification.json',{'passed':True,'actual_timestamp_ns':expected_ns,'actual_timestamp_utc':'2026-11-08T08:00:00.001Z','millisecond_precision_preserved':True,'public_preflight_sha256':sha(R/'funding_preflight.json'),'raw_preflight_receipts_sha256':sha(R/'funding_preflight_receipts.json'),'own_current_new_funding_records':counts,'own_cashflow_rows':rows,'each_eligible_asset_cost_once_across_full_own_chain':True,'positive_income_not_boosted_by_cost_multiplier':True,'single_08_not_yet_in_own_window':True,'no_account_policy_or_financial_replay':True});print('PASS12own08.001settlements;nanosecondtimestamp/rate/mark/q/cashflow/fullchains;single08notyetbooked')
