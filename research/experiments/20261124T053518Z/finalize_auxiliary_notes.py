"""Retain a genuine supplemental read-only failure and its successful Decimal recovery."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
b=json.loads((R/'auxiliary_notes_binding.json').read_text());assert sha(Path(__file__))==b['source_sha256']
expected=json.loads((R/'verification.json').read_text())['report_sha256'];sma=json.loads((R/'forward_verification.json').read_text())['report_sha256'];assert sha(R/'report.json')==expected and sha(R/'forward_report.json')==sma
failure=json.loads((R/'readonly_trade_review_failure.json').read_text());recovery=json.loads((R/'BTC_extra_roundtrip_review.json').read_text());assert failure['native_chunk_id']=='64459c' and failure['exit_code']==1 and recovery['passed'] and recovery['new_financial_or_account_evaluations']==0 and recovery['financial_report_sha256_unchanged']==expected
p=R/'result.md';text=p.read_text();before=sha(p);assert text.count('原生命令非零阶段[]')==1;text=text.replace('原生命令非零阶段[]','已登记流水线原生命令非零阶段[]')
paragraph='补充只读逐笔归因检查有一次真实TypeError（工具64459c、退出1）：将原账本的Decimal金额字符串直接求和。原始失败和字段类型见readonly_trade_review_failure.json，Decimal修正版源码及先执行绑定见verify_extra_roundtrip.py和extra_trade_review_binding.json，成功证据见BTC_extra_roundtrip_review.json。新增往返在每个成本场景的毛亏损为97.3365 USDT；其余匹配成交的数量、价格、成本一致。另一次时间键预检使用了不存在字段，其空差分已弃用，正式检查采用账本真实trade_ts_ns、opening、terminal键。金融回测与已完成账户窗口未重放。'
marker='本轮30条原始reserve/finish事件';assert marker in text;text=text.replace(marker,paragraph+'\n\n'+marker);p.write_text(text)
f=R/'read_failures.json';doc=json.loads(f.read_text());assert 'supplemental_readonly_failure_and_recovery' not in doc
info={'failed_native_chunk':'64459c','failed_native_exit':1,'failure_record':'readonly_trade_review_failure.json','failure_record_sha256':sha(R/'readonly_trade_review_failure.json'),'effective_source':'verify_extra_roundtrip.py','effective_source_sha256':sha(R/'verify_extra_roundtrip.py'),'pre_execution_binding':'extra_trade_review_binding.json','successful_native_chunk':'a7def6','successful_native_exit':0,'effective_review':'BTC_extra_roundtrip_review.json','effective_review_sha256':sha(R/'BTC_extra_roundtrip_review.json'),'discarded_metadata_key_probe_native_chunk':'e4fb87','strategy_or_account_replays':0};doc['supplemental_readonly_failure_and_recovery']=info;f.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
assert sha(R/'report.json')==expected and sha(R/'forward_report.json')==sma
out={'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'source_binding':'auxiliary_notes_binding.json','result_before_notes_sha256':before,'result_after_notes_sha256':sha(p),'financial_report_sha256_unchanged':expected,'SMA_report_sha256_unchanged':sma,'failure_and_recovery':info,'rendered_prose_and_failure_index_only':True,'financial_or_account_evaluations':0};(R/'auxiliary_recovery_notes.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':True,'original_type_error_retained':True,'Decimal_recovery_passed':True,'financial_and_original_account_reports_unchanged':True,'strategy_or_account_runs':0}))
