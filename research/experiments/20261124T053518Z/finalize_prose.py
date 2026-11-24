"""Correct only a stale template noun in the rendered result; financial evidence is immutable."""
import hashlib,json
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected=json.loads((R/'verification.json').read_text())['report_sha256'];assert sha(R/'report.json')==expected
b=json.loads((R/'prose_formatter_binding.json').read_text());assert sha(Path(__file__))==b['source_sha256']
p=R/'result.md';s=p.read_text();old='BTC波动上限实际desired与交易差分';new='BTC入场门槛H实际desired与交易差分';assert s.count(old)==1
before=sha(p);p.write_text(s.replace(old,new));assert sha(R/'report.json')==expected
out={'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'source_binding':'prose_formatter_binding.json','rendered_result_before_sha256':before,'rendered_result_after_sha256':sha(p),'replacement':{'old':old,'new':new},'reason':'W is BTC 29day entry ROC hurdle H;BTC volatility ceiling is fixed .0275. Only the stale template noun is corrected.','legacy_field_semantics':{'same_cap_alias_graphs':'same ETH K, old BTC H.03 matched control;not a BTC volatility-cap comparison'},'financial_report_sha256_unchanged':expected,'financial_or_account_evaluations':0}
(R/'prose_review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
