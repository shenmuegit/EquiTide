"""Reproduce failed OPEN conversion and verify archived native-Decimal recovery; no new strategy evaluation."""
from pathlib import Path
from decimal import Decimal as D
from datetime import datetime,timezone
import gzip,json,hashlib
import numpy as np,polars as pl
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
plan=json.loads((R/'plan.json').read_text());ref=plan['component_refs'][0];arc=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()));f=pl.read_parquet(ROOT/plan['periods'][ref['year']]['normalized_data'][ref['asset']]['path']);cl=np.asarray(f['close'].cast(pl.Float64));op=np.asarray(f['open'].cast(pl.Float64));out=[];sample=None
for k,z in arc['scenes'].items():
 states={d:st for st in z['position_segments'] for d in range(st['day_offset'],st['end_day_exclusive'])};bad=np.empty(259382);good=np.empty(259382);bad[0]=good[0]=ref['capital_usdt']
 for d in range(180):
  i=183+d;st=states[d];cash,qty=D(st['cash']),D(st['units']);mi=i*1440+1;bad[d*1441+1]=float(cash+qty*D(str(op[mi])));good[d*1441+1]=float(cash+qty*f['open'][mi]);bad[d*1441+2:(d+1)*1441+1]=good[d*1441+2:(d+1)*1441+1]=float(cash)+float(qty)*cl[mi:mi+1440]
 bad[-1]=good[-1]=float(D(z['terminal_cash']));h=lambda v:hashlib.sha256(v.astype('<f8').tobytes()).hexdigest();assert h(good)==z['summary']['NAV_sha256_f64le'];idx=np.flatnonzero(bad!=good);assert len(idx)>0 and all(int(i)%1441==1 for i in idx)
 if sample is None:
  ix=int(idx[0]);d=(ix-1)//1441;mi=(183+d)*1440+1;st=states[d];sample={'price':str(f['open'][mi]),'cash':st['cash'],'units':st['units'],'original_native_Decimal_NAV':float(good[ix]),'failed_float_roundtrip_NAV':float(bad[ix]),'Polars_float_price':str(op[mi]),'day_offset':d,'NAV_index':ix}
 out.append({'cost_multiplier':k,'archived_NAV_sha256':z['summary']['NAV_sha256_f64le'],'failed_float_roundtrip_sha256':h(bad),'native_Decimal_recovery_sha256':h(good),'post_decision_points_differing':int(len(idx)),'minute_close_encoding_unchanged':True,'final_NAV_unchanged':bool(bad[-1]==good[-1])})
failed=json.loads((R/'research_commands.json').read_text())[0];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
proof={'recorded_at_utc':datetime.now(timezone.utc).isoformat(),'failed_command':failed,'failed_log_path':str((R/'evaluate.log').relative_to(ROOT)),'failed_log_sha256':sha(R/'evaluate.log'),'failed_reader_code_sha256':sha(R/'run.py'),'parent_configurations_computed_before_failure':0,'new_parent_result_files_created_before_failure':0,'hypothesis_confirmed':'Postdecision OPEN passed through Polars Decimal->Float64->string->Decimal,losing low bits before cash+qty*price. Archived source postdecision opens used native Decimal-equivalent prices. Keep minute CLOSE PolarsFloat64 encoding unchanged;use native Decimal OPEN for postdecision/terminal NAV,then float once.','source_component':ref,'same_original_parquet_sha256':plan['periods'][ref['year']]['normalized_data'][ref['asset']]['sha256'],'regression_case':sample,'diagnostic_three_cost_scenes':out,'historical_report_or_archive_bytes_rewritten':False,'diagnostic_serialization_failure_retained':'diagnostic_serialization_failure.json'}
if not (R/'recovery_failure.json').exists():(R/'recovery_failure.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
else:assert json.loads((R/'recovery_failure.json').read_text())['regression_case']==sample
print(json.dumps({'root_cause_confirmed':True,'regression_case':sample,'three_native_recovery_hashes_match':True,'initial_evaluate_exit':failed['exit_code'],'parent_results_computed':0},ensure_ascii=False),flush=True)
