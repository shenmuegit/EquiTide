"""Bind fresh settlement fields while preserving the original public capture timestamp."""
import gzip,json,sys,subprocess
from datetime import datetime,timezone
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261116T000400Z';sys.path.insert(0,str(R))
from common import *
assert not (R/'code_binding_before_evaluation.json').exists()
(R/'bootstrap_receipt.json').write_bytes((R/'review/native_bootstrap.py_receipt.json').read_bytes())
receipts=json.loads((R/'initial_remote_sync_receipts.json').read_text())
for cmd in [['git','rev-parse','HEAD'],['git','rev-parse','origin/main']]:
 a=now();z=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);receipts.append({'command':cmd,'cwd':str(ROOT),'started_utc':a,'finished_utc':now(),'exit_code':z.returncode,'stdout':z.stdout,'stderr':z.stderr});assert z.returncode==0
assert receipts[-2]['stdout']==receipts[-1]['stdout'];put(R/'remote_sync_receipts.json',receipts)
fresh=json.loads((R/'window_funding_preflight.json').read_text())
assert fresh['passed'] and all(not xs for xs in fresh['public_fields_by_asset'].values())
for day in [13,14,15]:
 for hour in [0,8,16]:
  filename=f'funding{hour:02d}_nov{day}_preflight.json';(R/filename).write_bytes((P/filename).read_bytes())
original=json.loads((R/'funding16_nov15_preflight.json').read_text())
assert original['recorded_utc']=='2026-11-15T22:09:23.048575Z'
assert original['public_fields_by_asset']!=fresh['public_fields_by_asset']
ms=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*1000)
iso=lambda t:datetime.fromtimestamp(t/1000,timezone.utc).isoformat().replace('+00:00','Z')
rules='Current originalSMA/single16:30to18:30 andL4/FEWM18:10to20:10;fresh complete-window public funding arrays empty,allfund/daily/trades0. All3perps already booked actualNov15_16 eachonce,never repeat. Preserve own q,entries,cash,desired,capital,fullNAVprefix and original67daily authority. No account restart,transfers,forcedclose or adoption of research caps. Next18:30to20:30 and20:10to22:10 still require fresh actual settlement lookup,no nominal8hour or zero assumption.'
w={}
for account,begin,end in [('SMA','2026-11-15T16:30:00Z','2026-11-15T18:30:00Z'),('candidate','2026-11-15T16:30:00Z','2026-11-15T18:30:00Z'),('l4h02','2026-11-15T18:10:00Z','2026-11-15T20:10:00Z'),('fewm','2026-11-15T18:10:00Z','2026-11-15T20:10:00Z')]:
 fields={a:[] if account=='SMA' else [z for z in fresh['public_fields_by_asset'][a] if ms(begin)<z['fundingTime']<=ms(end)] for a in ['BTC','ETH']}
 w[account]={'start_utc':begin,'cutoff_utc':end,'expected_daily_events_utc':[],'expected_funding_utc':sorted({iso(z['fundingTime']) for xs in fields.values() for z in xs}),'expected_funding_by_asset':fields,'expected_funding_records':3*sum(len(xs) for xs in fields.values()),'next_daily_decision_utc':'2026-11-16T00:01:00Z'}
split={a:w[a]['expected_funding_records'] for a in w};assert split=={'SMA':0,'candidate':0,'l4h02':0,'fewm':0}
w.update(recorded_utc=now(),rules=rules);put(R/'account_windows.json',w)
for hour in [8,16]:
 filename=f'funding{hour:02d}_nov14_preflight.json';z=json.loads((R/filename).read_text())
 put(R/f'funding{hour:02d}_prebinding_verification.json',{'passed':True,'source':rel(R/filename),'sha256':sha(R/filename),'original_public_capture_UTC':z['recorded_utc'],'fresh_public_capture_UTC':fresh['recorded_utc'],'fresh_fields_equal_to_original':False,'fresh_current_window_fields_empty':True,'before_account_calculation':True,'old_capture_UTC_not_relabelled':True})
known=json.loads((R/'funding08_nov15_preflight.json').read_text());assert known['recorded_utc']=='2026-11-15T14:06:10.992989Z'
put(R/'funding08_nov15_reuse_verification.json',{'passed':True,'recorded_utc':now(),'original_source':rel(P/'funding08_nov15_preflight.json'),'original_source_sha256':sha(P/'funding08_nov15_preflight.json'),'copied_source_sha256':sha(R/'funding08_nov15_preflight.json'),'original_capture_UTC':known['recorded_utc'],'current_fresh_query':rel(R/'window_funding_preflight.json'),'current_fresh_query_sha256':sha(R/'window_funding_preflight.json'),'current_fresh_capture_UTC':fresh['recorded_utc'],'public_fields_exactly_equal':False,'fresh_current_window_fields_empty':True,'original_capture_not_relabelled':True,'only_public_fields_reused_not_account_cashflows':True,'old_actual08_already_booked_all3_once_no_current_rebooking':True})
put(R/'funding16_nov15_prebinding_verification.json',{'passed':True,'recorded_utc':now(),'source':rel(R/'funding16_nov15_preflight.json'),'sha256':sha(R/'funding16_nov15_preflight.json'),'original_capture_UTC':original['recorded_utc'],'fresh_capture_UTC':fresh['recorded_utc'],'fresh_query':rel(R/'window_funding_preflight.json'),'fresh_query_sha256':sha(R/'window_funding_preflight.json'),'actual_public_fields':fresh['public_fields_by_asset'],'fresh_public_fields_exactly_equal_to_original':False,'different_current_window_empty_not_relabelling_original':True,'original_source_bytes_and_capture_UTC_preserved':True,'account_record_counts':split,'before_account_calculation':True,'own_q_and_cashflow_not_copied':True})
orig=json.loads((R/'funding00_nov14_preflight.json').read_text());neworig=json.loads((R/'funding00_nov15_preflight.json').read_text())
put(R/'funding00_public_reuse.json',{'passed':True,'original_source':rel(P/'funding00_nov14_preflight.json'),'original_source_sha256':sha(P/'funding00_nov14_preflight.json'),'original_capture_recorded_utc':orig['recorded_utc'],'actual_Nov15_source':rel(R/'funding00_nov15_preflight.json'),'actual_Nov15_source_sha256':sha(R/'funding00_nov15_preflight.json'),'actual_Nov15_original_capture_utc':neworig['recorded_utc'],'fresh_capture_utc':fresh['recorded_utc'],'fresh_current_window_fields_empty':True,'all3_perp_Nov15_midnight_and_daily_already_booked_once':True,'current_window_funding_record_split':split,'public_fields_only_not_cashflows':True})
l=json.loads((P/'l4h02_resume_plan.json').read_text());point=ROOT/'research/automation/l4h02_forward_latest.json'
l.update(frozen_at_utc=now(),recorded_utc=now(),round=R.name,previous_pointer=json.loads(point.read_text()),previous_pointer_sha256=sha(point),cutoff_utc=w['l4h02']['cutoff_utc'],cutoff_ns=ms(w['l4h02']['cutoff_utc'])*1000000,branch_lock_broker_pid=2289809,rules=rules);put(R/'l4h02_resume_plan.json',l)
full=ROOT/'research/experiments/20261115T075947Z/forward_inputs.json.gz';old66=ROOT/'research/experiments/20261114T035058Z/forward_inputs.json.gz';old65=ROOT/'research/experiments/20261113T033939Z/forward_inputs.json.gz'
assert sha(full)=='fbab89bc11a94af387d5f0ca7d168f9901e0a0eed4fd2b47e41a0b265d3fe576'
dd,od,sd=[json.loads(gzip.decompress(p.read_bytes())) for p in [full,old66,old65]]
assert all(len(dd[a]['1d'])==67 and dd[a]['1d'][:66]==od[a]['1d'] and od[a]['1d'][:65]==sd[a]['1d'] and dd[a]['1d'][-1][6]+1==1794700800000 for a in ['BTC','ETH'])
put(R/'sma66_background_verification.json',{'passed':True,'recorded_utc':now(),'full67_authority':rel(full),'full67_sha256':sha(full),'full66_authority':rel(old66),'full66_sha256':sha(old66),'old65_authority':rel(old65),'old65_sha256':sha(old65),'actual_old_daily_bars_preserved':66,'actual_completed_daily_context':67,'raw_arrays_exactly_equal_on_all_old_bars':True,'SMA_indicator_lookback_unchanged':65,'no_new_daily_capture_or_decision':True,'financial_or_account_calculations':0})
paths=[R/n for n in ['observe_l4h02.py','observe_fewm.py','observe_candidate.py','forward.py','forward_registry.py','audit_incremental.py','audit_l4h02.py','audit_fewm.py','audit_candidate.py','audit_forward.py']]+[ROOT/x for x in l['source_sha256']]+[full,old66,old65,R/'window_funding_preflight.json',*[R/f'funding{hour:02d}_nov{day}_preflight.json' for day,hour in [(14,8),(14,16),(15,0),(15,8),(15,16)]]]
put(R/'original_accounts_binding.json',{'recorded_utc':now(),'sources_sha256':{rel(x):sha(x) for x in paths},'frozen_before_current_account_calculation':True,'original_kernels_unchanged':True,'SMA_original_daily_adapter':'research/experiments/20261113T033939Z/forward.py','SMA_current_mark_only_adapter':rel(R/'forward.py'),'SMA_old_full65_authority':rel(old65),'SMA_current_full67_authority':rel(full),'SMA_current_full67_authority_sha256':sha(full),'SMA_raw_path_dynamic_current_round':True})
print('PASS observed actual16 original UTC preserved:fresh current-window empty;all3actual16alreadyOnce;SMA0/single0/L4zero/FEWMzero;full67 unchanged;0account calculations')
