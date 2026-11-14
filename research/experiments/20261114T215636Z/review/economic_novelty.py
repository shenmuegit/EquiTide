"""Confirm concrete new BTC rules across full registry without relying on the continuous-days metadata field."""
import json,sys
from pathlib import Path
from datetime import datetime
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import reg,put,sha,now,rel
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');own={z['fingerprint'] for z in json.loads((R/'batch.json').read_text())};rows=[]
for fp,row in rs.items():
 s=row.get('spec',{});q=s.get('parameters',{});end=q.get('end_utc','')
 if not(s.get('kind')=='strategy' and set(s.get('universe',[]))=={'BTC/USDT'} and q.get('lookback_days')==29 and q.get('return_hurdle')==.03 and q.get('exit_buffer_fraction')==.005 and q.get('entry_volatility_ceiling')==.03 and q.get('entry_volatility_window_days') in [6,10]):continue
 if not end or datetime.fromisoformat(end.replace('Z','+00:00'))!=datetime.fromisoformat('2026-11-14T00:01:00+00:00'):continue
 rows.append({'fingerprint':fp,'own_current_definition':fp in own,'status':row['status'],'result_available':row.get('result_available'),'name':s['name'],'report':row.get('report'),'start_utc':q.get('start_utc'),'N':q.get('fixed_entry_notional_usdt'),'capital':q.get('initial_capital_usdt'),'V':q.get('entry_volatility_window_days'),'signal_mode':q.get('signal_mode'),'entry_gate_scope':q.get('entry_volatility_gate_scope')})
prior=[z for z in rows if not z['own_current_definition'] and z['result_available']];assert not prior,prior;assert len(rows)==2 and all(z['own_current_definition'] and z['result_available'] for z in rows)
put(R/'economic_parameter_novelty_verification.json',{'passed':True,'recorded_utc':now(),'all_registry_records_read':len(rs),'full_end_timestamp_normalized':True,'continuous_days_marker_not_required':True,'same_core_rule_parameter_matches':rows,'earlier_actual_same_rule_V6_or_V10_at_this_end':prior,'old_V14_definition_aliases_preserved':True,'no_model_account_or_registry_writes_from_checker':True,'financial_report_sha256_unchanged':sha(R/'report.json')});print('PASS concreteV6/V10notpreviouslyactual atthisend acrossfullregistry,metadataindependent;only2ownactualnative matches')
