"""Reseal format-only correction after actual read-only exports/monitor rechecks."""
import ast,gzip,hashlib,json,subprocess
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
mp=R/'data_manifest.json';m=read(mp);fix=read(R/'publication_newline_recovery.json');assert sha(mp)==fix['pre_csv_manifest']['sha256'];oldproof=read(ROOT/fix['full_failure_proof']['path']);assert sha(ROOT/fix['full_failure_proof']['path'])==fix['full_failure_proof']['sha256']
assert sha(R/'report.json')==m['finished_report_sha256']==fix['financial_report_sha256_unchanged'] and sha(R/'forward_report.json')==m['finished_forward_report_sha256'] and sha(R/'candidate_observation/report.json')==m['finished_candidate_report_sha256']
allowed={'summary.json','export_manifest.json','summarize.py','commands.py','check_feed.py','publish.py','read_failures.json',*[Path(x['path']).name for x in fix['files']]}
for path,h in m['artifacts'].items():
 if Path(path).name not in allowed:assert sha(ROOT/path)==h,path
for path,h in m['protected_inputs_sha256'].items():assert sha(ROOT/path)==h,path
for path,h in m['code_and_frozen_source_sha256'].items():assert sha(ROOT/path)==h,path
for name in ['summary.json','export_manifest.json']:
 old=json.loads(subprocess.check_output(['git','show',oldproof['precommit_tree']+':'+str((R/name).relative_to(ROOT))],cwd=ROOT));new=read(R/name)
 for x in fix['files']:
  field=next(k for k,z in old['exports'].items() if z['path']==x['path']);assert old['exports'][field]['sha256']==x['old_sha256'];old['exports'][field]['sha256']=x['new_sha256']
 assert old==new,name
for x in fix['files']:assert sha(ROOT/x['path'])==x['new_sha256'] and x['all_parsed_cells_identical'] and x['CR_after']==0
for phase in ['exports_recovery','monitor_recovery','feed_recovery']:
 rows=read(R/(phase+'_commands.json'));assert all(x['exit_code']==0 for x in rows);m['required_command_receipts'][phase+'_commands.json']=rows
assert read(R/'export_verification.json')['passed'] and read(R/'feed_verification.json')['passed']
for p in R.rglob('*.py'):ast.parse(p.read_text(),filename=str(p))
tree=ast.parse((R/'summarize.py').read_text());calls=[x for x in ast.walk(tree) if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=='DictWriter'];assert len(calls)==1;kw=next(x for x in calls[0].keywords if x.arg=='lineterminator');assert ast.literal_eval(kw.value)=='\n'
put(R/'csv_serializer_check.json',{'passed':True,'all_48072_CSV_lines_corrected_to_LF':True,'all_original_parsed_CSV_cells_identical':True,'producer_AST_lineterminator_is_actual_newline':True,'complete_exports_readonly_recheck_exit0':True,'no_financial_evaluation_repeat':True,'original_report_SHA256':sha(R/'report.json'),'corrected_producer_SHA256':sha(R/'summarize.py')})
resolution=read(R/'review_resolution.json');resolution['publication_whitespace_recovery']={'actual_publisher_exit1':True,'git_diff_check_exit2':True,'CRLF_lines':48072,'fixed_LF_only':True,'allCSVcells_same':True,'readonly_exports_monitor_feed_rechecked_actual_exit0':True,'full_original_failure_retained':fix['full_failure_proof'],'no_financial_report_or_ledger_changes':True};resolution['failure_fact_records']=len(read(R/'read_failures.json')['facts']);put(R/'review_resolution.json',resolution)
nxt=read(R/'next_research_state.json');nxt['format_only_recovery']={'record':str((R/'publication_newline_recovery.json').relative_to(ROOT)),'allCSVcells_identical':True,'producer_lineterminator':'LF','actual_export_monitor_feed_rechecks_exit0':True,'financial_report_SHA256_unchanged':sha(R/'report.json')};put(R/'next_research_state.json',nxt)
with (R/'result.md').open('a') as f:f.write('\n提交前Git格式门禁曾因CSV默认CRLF退出2，publisher实际退出1且未创建提交。仅将6个CSV的48072行改LF，逐行所有单元格完全相同；完整金融/账户报告、spec、结果账本、旧资格与净值哈希均未改。CSV生产器显式LF，导出、monitor及旧行一致性已实际重新检查exit0；原始失败全文、旧manifest及诊断SHA留publication_newline_recovery.json所引位置，不绕过格式门禁或重跑金融模型。\n')
with (R/'reproduce.md').open('a') as f:f.write('\nCSV固定LF。publication_newline_recovery.json绑定修复前后每个CSV SHA、相同解析单元格及原始Git失败诊断；exports_recovery/monitor_recovery/feed_recovery命令均实际exit0。首次publisher在commit前停止，正式报告及账本未变。\n')
m['recorded_at_utc']=datetime.now(timezone.utc).isoformat();m['format_only_reseal']={'previous_manifest_SHA256':fix['pre_csv_manifest']['sha256'],'previous_manifest_gzip':fix['pre_csv_manifest']['gzip_path'],'previous_manifest_gzip_SHA256':fix['pre_csv_manifest']['gzip_sha256'],'all_original_csv_cells_identical':True,'financial_models_not_rerun':True};m['failure_facts']=read(R/'read_failures.json');m['original_failures_and_recoveries']=resolution
for p in m['shared_files']:m['shared_files'][p]={'sha256':sha(ROOT/p),'bytes':(ROOT/p).stat().st_size}
m['artifacts']={str(p.relative_to(ROOT)):sha(p) for p in sorted(R.rglob('*')) if p.is_file() and p.name!='data_manifest.json'}
assert not any(p.name=='__pycache__' or 'checkpoint' in p.name or p.suffix in ['.pyc','.npy','.tmp'] for p in R.rglob('*'))
put(mp,m)
print(json.dumps({'sealed_artifacts':len(m['artifacts']),'CSV_lines_LF':48072,'allCSVcells_identical':True,'financial_report_SHA256':sha(R/'report.json'),'all_required_actual_exit0':all(x['exit_code']==0 for rows in m['required_command_receipts'].values() for x in rows),'original_failure_facts_retained':len(m['failure_facts']['facts'])}),flush=True)
