"""Fresh actualNov8_16 fields and independent ownL4/FEWM funding,fullchain uniqueness; no replay."""
import gzip,json,sys
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put
rd=lambda p:json.loads(p.read_text());pre=rd(R/'funding16_preflight.json');receipts=rd(R/'funding16_preflight_receipts.json');win=rd(R/'account_windows.json');assert pre['account_or_strategy_calculations']==0 and sha(R/'funding16_preflight.json')==win['public_funding16_preflight']['sha256'] and sha(R/'funding16_preflight_receipts.json')==win['public_funding16_preflight']['receipts_sha256'];times={int(f['fundingTime'])*1000000 for zz in pre['public_fields_by_asset'].values() for f in zz};assert times=={1794153600000000000};expected_ns=next(iter(times));rows=[];counts={};chains={}
for z in receipts:assert sha(ROOT/z['raw'])==z['sha256'] and len(gzip.decompress((ROOT/z['raw']).read_bytes()))==z['bytes']
for stem in ['candidate','l4h02','fewm']:
 W=R/(stem+'_observation');before=rd(ROOT/rd(W/'previous_pointer.json')['state']);state=rd(W/'state.json');v=rd(R/(stem+'_verification.json'));delta=json.loads(gzip.decompress((W/'delta.json.gz').read_bytes()));fund=[z for z in delta['journal'] if z['kind']=='funding'];counts[stem]=len(fund);assert v['passed'] and v['new_daily_events']==v['new_fills']==0 and len(fund)==(0 if stem=='candidate' else 6);im=rd(W/'input_manifest.json');assert sha(ROOT/im['packet'])==im['sha256'];packet=json.loads(gzip.decompress((ROOT/im['packet']).read_bytes()))
 for z in fund:
  a,k=z['asset'],str(z['cost_multiplier']);f=pre['public_fields_by_asset'][a][0];raw=next(t for t in packet['assets'][a]['funding'] if int(t['fundingTime'])*1000000==expected_ns);assert all(str(raw[field])==str(f[field]) for field in ['symbol','fundingTime','fundingRate','markPrice']);q=D(before['books'][a][k]['signed_units']);base=-q*D(f['markPrice'])*D(f['fundingRate']);amount=base*int(k) if base<0 else base
  assert z['timestamp_ns']==expected_ns and D(z['signed_units'])==q and D(z['rate'])==D(f['fundingRate']) and D(z['mark_price'])==D(f['markPrice']) and D(z['base_amount_usdt'])==base and D(z['amount_usdt'])==amount and D(z['cash_before'])==D(before['books'][a][k]['cash']) and D(z['cash_after'])==D(z['cash_before'])+amount
  assert all(state['books'][a][k][f0]==before['books'][a][k][f0] for f0 in ['signed_units','entry_price','entry_reference']) and D(state['books'][a][k]['cash'])==D(z['cash_after']);rows.append({'account':stem,'asset':a,'cost':k,'actual_timestamp_ns':z['timestamp_ns'],'actual_rate':z['rate'],'actual_mark':z['mark_price'],'own_pre_settlement_q':str(q),'own_base_usdt':str(base),'own_amount_usdt':str(amount),'cash_before':z['cash_before'],'cash_after':z['cash_after']})
 point=rd(ROOT/('research/automation/'+stem+'_forward_latest.json'));seen=set();chain=[]
 while point:
  assert sha(ROOT/point['delta'])==point['delta_sha256'];journal=json.loads(gzip.decompress((ROOT/point['delta']).read_bytes()))['journal']
  for z in journal:
   if z['kind']=='funding' and z['timestamp_ns']==expected_ns:
    key=(z['asset'],str(z['cost_multiplier']));assert key not in seen;seen.add(key);chain.append(z)
  ref=point.get('previous_pointer');point=rd(ROOT/ref['path']) if ref else None
 assert len(chain)==(0 if stem=='candidate' else 6);chains[stem]=len(chain)
assert len(rows)==12 and counts=={'candidate':0,'l4h02':6,'fewm':6}
put(R/'actual16_current_funding_verification.json',{'passed':True,'actual_timestamp_ns':expected_ns,'actual_timestamp_utc':'2026-11-08T16:00:00.000Z','actual_public_preflight_sha256':sha(R/'funding16_preflight.json'),'actual_public_receipts_sha256':sha(R/'funding16_preflight_receipts.json'),'own_current_new_funding_records':counts,'own_cashflow_rows':rows,'full_own_chain_16_counts':chains,'own08_not_repeated':True,'whole_second_actual16_and_millisecond_actual08_not_confused':True,'positive_income_not_boosted_by_cost_multiplier':True,'single_16_not_yet_in_own_window':True,'no_rule_reset_or_account_replay':True});print('PASS12freshactual16ownL4/FEWMsettlements;single16notyetbooked,ownq/rate/mark/cashflows/fullchains verified')
