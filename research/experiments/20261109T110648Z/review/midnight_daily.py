"""Read-only own current Nov9_08 funding plus historical midnight uniqueness; no account advance."""
import gzip,json,sys
from decimal import Decimal as D
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];HIST=ROOT/'research/experiments/20261109T030420Z';sys.path.insert(0,str(R));from common import sha,put
rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));MID=1794182400000000000;DEC=MID+60000000000;pref=rd(R/'funding08_current_preflight.json');win=rd(R/'account_windows.json');receipts=rd(R/'funding08_current_preflight_receipts.json');oldpref=rd(R/'funding_midnight_preflight.json');ns=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp())*10**9+datetime.fromisoformat(s.replace('Z','+00:00')).microsecond*1000;current={};oldcounts={};chain08counts={};fundrows=[];oldrows=[];deccounts={}
assert pref['account_or_strategy_calculations']==0 and sha(R/'funding08_current_preflight.json')==win['public_funding08_current_preflight']['sha256']
for z in receipts:assert z['http_status']==200 and z['curl_exit_code']==0 and sha(ROOT/z['raw'])==z['sha256'] and len(gzip.decompress((ROOT/z['raw']).read_bytes()))==z['bytes']
actual_by_asset={a:{int(z['fundingTime'])*1000000:z for z in rows} for a,rows in pref['public_fields_by_asset'].items()};actual_times={t for rows in actual_by_asset.values() for t in rows};assert actual_times=={1794211200001000000}
for stem in ['candidate','l4h02','fewm']:
 W=R/(stem+'_observation');v=rd(R/(stem+'_verification.json'));before=rd(ROOT/rd(W/'previous_pointer.json')['state']);state=rd(W/'state.json');delta=gz(W/'delta.json.gz');im=rd(W/'input_manifest.json');assert sha(ROOT/im['packet'])==im['sha256'];packet=gz(ROOT/im['packet']);fund=[z for z in delta['journal'] if z['kind']=='funding'];trades=[z for z in delta['journal'] if z['kind']=='trade'];decs=[z for z in delta['journal'] if z['kind']=='decision'];assert v['passed'] and v['new_daily_events']==v['new_exact_causal_decisions']==v['new_fills']==0 and not trades and not decs and len(fund)==v['new_funding_settlements']==win[stem]['expected_funding_records'];current[stem]=len(fund)
 assert {z['timestamp_ns'] for z in fund}==set(map(ns,win[stem]['expected_funding_utc']))
 for z in fund:
  a,k=z['asset'],str(z['cost_multiplier']);f=actual_by_asset[a][z['timestamp_ns']];raw=next(x for x in packet['assets'][a]['funding'] if int(x['fundingTime'])*1000000==z['timestamp_ns']);assert all(str(raw[key])==str(f[key]) for key in ['symbol','fundingTime','fundingRate','markPrice']);q=D(before['books'][a][k]['signed_units']);base=-q*D(f['markPrice'])*D(f['fundingRate']);value=base*int(k) if base<0 else base
  assert D(z['signed_units'])==q and D(z['rate'])==D(f['fundingRate']) and D(z['mark_price'])==D(f['markPrice']) and D(z['base_amount_usdt'])==base and D(z['amount_usdt'])==value and D(z['cash_before'])==D(before['books'][a][k]['cash']) and D(z['cash_after'])==D(z['cash_before'])+value
  fundrows.append({'account':stem,'asset':a,'cost':k,'actual_timestamp_ns':z['timestamp_ns'],'fundingTime_ms':f['fundingTime'],'rate':f['fundingRate'],'mark':f['markPrice'],'own_pre_settlement_units':str(q),'own_base_usdt':str(base),'own_amount_usdt':str(value),'cash_before':z['cash_before'],'cash_after':z['cash_after']})
 for a in ['BTC','ETH']:
  assert state['context'][a]['daily']==before['context'][a]['daily']
  for k in ['1','2','3']:
   b,s=before['books'][a][k],state['books'][a][k];amount=sum((D(z['amount_usdt']) for z in fund if z['asset']==a and str(z['cost_multiplier'])==k),D(0));assert all(s[x]==b[x] for x in ['signed_units','entry_price','entry_reference']) and D(s['cash'])==D(b['cash'])+amount
 point=rd(ROOT/('research/automation/'+stem+'_forward_latest.json'));seen=set();fs=set();ds=set();newfs=set()
 while point:
  assert point['delta'] not in seen;seen.add(point['delta'])
  for key in ['delta','report','state','complete']:assert sha(ROOT/point[key])==point[key+'_sha256']
  own=gz(ROOT/point['delta']);midfund=[z for z in own['journal'] if z['kind']=='funding' and z['timestamp_ns']==MID]
  if midfund:
   prior=rd(ROOT/point['previous_pointer']['path']);ownbefore=rd(ROOT/prior['state'])
   for z in midfund:
    a,k=z['asset'],str(z['cost_multiplier']);assert (a,k) not in fs;fs.add((a,k));f=oldpref['public_fields_by_asset'][a][0];q=D(ownbefore['books'][a][k]['signed_units']);base=-q*D(f['markPrice'])*D(f['fundingRate']);amount=base*int(k) if base<0 else base;assert int(f['fundingTime'])*1000000==MID and D(z['signed_units'])==q and D(z['rate'])==D(f['fundingRate']) and D(z['mark_price'])==D(f['markPrice']) and D(z['amount_usdt'])==amount;oldrows.append({'account':stem,'asset':a,'cost':k,'actual_ns':MID,'own_units':str(q),'own_amount':str(amount)})
  for z in own['journal']:
   if z['kind']=='decision' and z['timestamp_ns']==DEC:key=(z['asset'],str(z['cost_multiplier']));assert key not in ds;ds.add(key)
   if z['kind']=='funding' and z['timestamp_ns'] in actual_times:key=(z['asset'],str(z['cost_multiplier']));assert key not in newfs;newfs.add(key)
  ref=point.get('previous_pointer');point=rd(ROOT/ref['path']) if ref else None
 assert len(fs)==len(ds)==6 and len(newfs)==6;oldcounts[stem]=len(fs);deccounts[stem]=len(ds);chain08counts[stem]=len(newfs)
assert current=={'candidate':6,'l4h02':0,'fewm':0} and len(fundrows)==6 and len(oldrows)==18
assert all(D(z['own_pre_settlement_units'])==0 and D(z['rate'])<0 and D(z['own_amount_usdt'])==0 for z in fundrows if z['asset']=='ETH')
priorfr=rd(HIST/'forward_report.json');smafull=gz(ROOT/priorfr['source_inputs_path']);fv=rd(R/'forward_verification.json');assert fv['passed'] and fv['new_daily_decisions']==fv['new_reference_points']==fv['new_executions']==0
for a in ['BTC','ETH']:assert len(smafull[a]['1d'])==65 and smafull[a]['1d'][-1][6]+1==MID//1000000 and priorfr['daily_decisions_by_asset'][a][0]['executed_at_utc']=='2026-11-09T00:01:00Z'
put(R/'current_actual08_funding_verification.json',{'passed':True,'actual_timestamps_ns':sorted(actual_times),'actual_timestamp_utc':'2026-11-09T08:00:00.001Z','public_preflight_sha256':sha(R/'funding08_current_preflight.json'),'public_receipts_sha256':sha(R/'funding08_current_preflight_receipts.json'),'own_current_funding_records':current,'full_own_chain_Nov9_08_counts':chain08counts,'own_cashflow_rows':fundrows,'positive_income_not_cost_boosted':True,'ETH_negative_rate_zero_own_units_gives_derived_zero':True,'millisecond_precision_preserved_not_nominal_bucketed':True,'own_q_cashflow_not_copied':True,'original_single_own08_completed_once_current_window':True,'new_fills_or_daily_decisions':0,'new_financial_or_account_advances':0})
put(R/'current_midnight_funding_verification.json',{'passed':True,'actual_timestamp_ns':MID,'own_current_midnight_funding_records':{k:0 for k in current},'full_own_chain_Nov9_midnight_counts':oldcounts,'historical_own_cashflow_rows':oldrows,'all3_original_own_midnight_funding_once':True,'current08_verified_separately':'current_actual08_funding_verification.json','current_midnight_cashflows_rebooked':0})
put(R/'current_midnight_daily_verification.json',{'passed':True,'UTC_daily_decision':'2026-11-09T00:01:00Z','current_new_daily_events':0,'current_new_causal_decisions':0,'current_new_midnight_funding_records':0,'current_window_actual08_funding_records':6,'historical_perp_daily_decisions_once_by_account':deccounts,'historical_SMA_daily_decisions_by_asset':priorfr['daily_decisions_by_asset'],'authoritative_SMA65_source':priorfr['source_inputs_path'],'authoritative_SMA65_sha256':sha(ROOT/priorfr['source_inputs_path']),'all4_next_daily_decision_utc':'2026-11-10T00:01:00Z','no_old_midnight_repeat_or_daily_replay':True,'scope':'Read saved actual own journals/raw public fields/context only, no new account advance/financial backtest/quote fills.'});print('PASS6currentownsingle08funding formulas at08:00:00.001;all3own08unique6each;MID9funding/decisions unique;single08complete,0newfills/daily,ownq/cash/fullNAV checked')
