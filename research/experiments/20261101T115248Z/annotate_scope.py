"""Correct an inherited descriptive count after valuation; preserve every executed byte."""
import copy,gzip,hashlib,json
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();p=R/'report.json';raw=p.read_bytes();before=json.loads(raw);after=copy.deepcopy(before);backup=R/'report_as_executed.json.gz';assert not backup.exists();backup.write_bytes(gzip.compress(raw,mtime=0));assert gzip.decompress(backup.read_bytes())==raw
old=after['execution_scope'];assert 'TwofreshBTC2500/N250' in old
new='FourfreshBTCnativepaths at3125/N312.5 and4375/N437.5 (two momentum components,two constantlongcontrols),sixnewparentcandidates andtwo newmatchedholdparents; sixoldnative andfouroldparentresultsreadonly. Raw1/1ownership,no parentorders,transfers orlinearNAVscaling. Controls matchactualbanks/initialN,not equalrisk/fullinvestedhold.'
after['execution_scope']=new;assert after['configs']==before['configs'] and after['summary']==before['summary'];p.write_text(json.dumps(after,ensure_ascii=False,indent=2,allow_nan=False)+'\n');assert {k:v for k,v in after.items() if k!='execution_scope'}=={k:v for k,v in before.items() if k!='execution_scope'}
proof={'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'phase':'Afteractualvaluation,beforeindependentauditandfinish','field':'execution_scope','before':old,'after':new,'original_report_sha256':hashlib.sha256(raw).hexdigest(),'original_report_compressed':str(backup.relative_to(ROOT)),'original_report_compressed_sha256':sha(backup),'corrected_report_sha256':sha(p),'all_other_report_fields_identical':True,'rules_specs_hashes_statuses_folds_metrics_archives_unchanged':True,'financial_or_observation_reruns':0,'bound_valuation_source_edited':False}
(R/'scope_annotation.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps(proof,ensure_ascii=False))
