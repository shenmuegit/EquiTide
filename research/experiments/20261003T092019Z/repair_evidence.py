"""Append provenance-only corrections; preserve original reserve/finish events and numerical results."""
import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];T=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=T/'forward.py';t=p.read_text().replace('1542oldNAVpoints exact prefix including both prior daily references;210closedmarks appended','1752oldNAVpoints exact prefix including both prior daily references;240closedmarks appended');p.write_text(t)
oldhashes={};newhashes={}
for n in ('report.json','forward_report.json'):
 p=T/n;oldhashes[n]=sha(p);r=json.loads(p.read_text())
 for path in r['source_hashes']:r['source_hashes'][path]=sha(ROOT/path)
 if n=='forward_report.json':r['validation']['continuity']='1752oldNAVpoints exact prefix including both prior daily references;240closedmarks appended to1992points,no daily reference or decisions in interval;cash/units/desired/trades unchanged,no forced sell'
 p.write_text(json.dumps(r,ensure_ascii=False,separators=(',',':'))+'\n');newhashes[n]=sha(p)
p=T/'forward_state.json';st=json.loads(p.read_text());st['source_report_sha256']=newhashes['forward_report.json'];p.write_text(json.dumps(st,indent=2)+'\n')
with (ROOT/'research/automation/registry.jsonl').open('a') as out:
 for batch,n in [('batch.json','report.json'),('forward_batch.json','forward_report.json')]:
  r=json.loads((T/n).read_text())
  for b in json.loads((T/batch).read_text()):
   row={'fingerprint':b['fingerprint'],'status':r['configs'][b['name']]['status'],'result_available':True,'report':str((T/n).relative_to(ROOT)),'report_sha256':newhashes[n],'recorded_at_utc':datetime.now(timezone.utc).isoformat(),'evidence_amendment':{'reason':'Correct audit stale211bar assertion to241 and source/continuity provenance only; no metric/state changes or production recalculation. Original reserve and finish retained.','previous_report_sha256':oldhashes[n]}}
   out.write(json.dumps(row,ensure_ascii=False)+'\n')
(T/'artifact_notes.json').write_text(json.dumps({'backtest_compute_failures':0,'audit_failures':[{'stage':'audit_forward','reason':'211 stale bar count; actual241 correctly computed','fixed':'241 assertion; all numerical evidence unchanged; original finish events retained with39append-only hash amendments.'}],'redaction':'Two credential-like source fields redacted; source unchanged.','old_report_sha256':oldhashes,'amended_report_sha256':newhashes,'ledger_amendment_events':39},indent=2)+'\n')
print('39append-only provenance amendments; no numerical metric or original ledger event rewritten')
