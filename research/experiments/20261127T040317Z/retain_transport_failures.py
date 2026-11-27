"""Preserve all actual failed GET attempts, including success-only observer adapters."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
b=rd(R/'transport_failure_binding.json');assert sha(Path(__file__))==b['source_sha256'];first=rd(R/'verification.json')['report_sha256'];sma=rd(R/'forward_verification.json')['report_sha256'];assert sha(R/'report.json')==first and sha(R/'forward_report.json')==sma
faildoc=rd(R/'read_failures.json');facts=faildoc['facts'];key=lambda z:(z['url'],z.get('started_utc'),z['sha256']);seen={key(z) for z in facts};new=[];attempt_sources=[]
for file in sorted(R.glob('*transport_attempts.json')):
 rows=rd(file);assert isinstance(rows,list);attempt_sources.append({'path':str(file.relative_to(ROOT)),'sha256':sha(file)})
 for i,z in enumerate(rows):
  if z['http_status']==200 and not z.get('curl_exit_code',0):continue
  if key(z) in seen:continue
  resolved=any(x['url']==z['url'] and x['http_status']==200 and not x.get('curl_exit_code',0) for x in rows[i+1:]);entry={**z,'attempt_source':str(file.relative_to(ROOT)),'resolved_within_same_capture':resolved,'completed_account_window_replayed':False};facts.append(entry);new.append(entry);seen.add(key(z))
indexfile=R/'raw_evidence_index.json';before_index=sha(indexfile);index=rd(indexfile);retained=R/'retained_raw';have={(z['original_path'],z['sha256']) for z in index['artifacts']}
for z in facts:
 raw=z.get('raw') or z.get('raw_gzip_path');assert raw and sha(ROOT/raw)==z['sha256'];dest=retained/(z['sha256']+'.gz')
 if not dest.exists():dest.write_bytes((ROOT/raw).read_bytes())
 assert sha(dest)==z['sha256']
 if (raw,z['sha256']) not in have:
  index['artifacts'].append({'original_path':raw,'committed_copy':str(dest.relative_to(ROOT)),'sha256':z['sha256'],'bytes':(ROOT/raw).stat().st_size,'kind':'actual_failed_public_GET_response','original_first_capture_UTC_preserved_in_provenance':True,'restoration_rule':'Restore the exact committed bytes to original_path if absent before readonly verification;no new market request or account execution.'});have.add((raw,z['sha256']))
index['distinct_copies']=len({z['committed_copy'] for z in index['artifacts']});index['total_distinct_bytes']=sum(p.stat().st_size for p in retained.iterdir());index['failed_response_bytes_included']=True;index['supplemental_failure_retention']='transport_failure_supplement.json';put(indexfile,index)
faildoc['facts']=facts;faildoc['all_observer_adapter_attempt_logs_indexed']=attempt_sources;put(R/'read_failures.json',faildoc)
p=R/'result.md';text=p.read_text();before_result=sha(p);assert len(re.findall(r'公共GET失败\d+条',text))==1;text=re.sub(r'公共GET失败\d+条','公共GET失败'+str(len(facts))+'条',text);text+='\n补充传输核对：逐一索引全部实际GET重试日志，包含candidate适配器仅将成功请求写入输入清单时另外保存的失败尝试。失败原始gzip、实际URL/UTC/退出码和同次抓取内恢复证据均保留，见transport_failure_supplement.json；未重放策略或已完成账户窗口。\n';p.write_text(text)
assert sha(R/'report.json')==first and sha(R/'forward_report.json')==sma
out={'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'source_binding':'transport_failure_binding.json','actual_attempt_sources':attempt_sources,'new_failed_attempts_indexed':new,'all_actual_failed_GET_attempts':facts,'raw_index_before_sha256':before_index,'raw_index_after_sha256':sha(indexfile),'rendered_result_before_sha256':before_result,'rendered_result_after_sha256':sha(p),'financial_report_sha256_unchanged':first,'SMA_report_sha256_unchanged':sma,'financial_or_completed_account_window_replays':0};put(R/'transport_failure_supplement.json',out);print(json.dumps({'passed':True,'all_failed_GETs':len(facts),'newly_retained_failures':len(new),'retained_distinct_copies':index['distinct_copies'],'financial_and_account_reports_unchanged':True,'completed_window_replays':0}))
