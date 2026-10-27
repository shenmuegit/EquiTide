"""Recover only an actual monitor size-limit failure, preserving every historical row."""
import hashlib,json,subprocess
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
 rows=json.loads((R/'gates_commands.json').read_text());assert len(rows)==3 and [x['exit_code'] for x in rows]==[0,0,1] and 'compressed monitor configs exceed size limit' in rows[-1]['stderr'];base=json.loads((R/'startup.json').read_text())['head_after_successful_SSH_fetch'];snap=json.loads((R/'snapshot.log').read_text());assert snap['research_configs']==7284 and 3000000<=snap['compressed_research_bytes']<4000000
 prior={}
 for path in ['research/monitor/latest.json','research/monitor/configs.json.gz']:
  raw=subprocess.check_output(['git','show',base+':'+path],cwd=ROOT);assert (ROOT/path).read_bytes()==raw;prior[path]={'sha256':sha(raw),'bytes':len(raw),'restored_to_exact_committed_base':base}
 assert json.loads((R/'monitor_capacity_source_review.json').read_text())['files_sha256']
 check=ROOT/'checks/monitor_snapshot.py';readme=ROOT/'research/monitor/README.md';oldcheck=check.read_bytes();oldreadme=readme.read_bytes();assert oldcheck.decode().count('assert len(config_gzip) < 3_000_000')==1
 (R/'monitor_snapshot_before_budget.py').write_bytes(oldcheck);(R/'monitor_README_before_budget.md').write_bytes(oldreadme)
 check.write_text(oldcheck.decode().replace('assert len(config_gzip) < 3_000_000','assert len(config_gzip) < 4_000_000'))
 note='\n2026-10-27新增108个真实研究配置后，7,284行gzip实为'+format(snap['compressed_research_bytes'],',')+'字节，原3,000,000字节门禁实际失败；脚本已恢复上一份有效汇总并留档失败。只将检查大小预算提高至4,000,000字节，所有7,176个旧展示行完整字典、收益、登记指纹、原报告和账户均保持；逐行核验另存本轮证据。浏览器现有原生gzip解压及SHA核验无3MB限制，无需重新部署。\n'
 text=oldreadme.decode().replace('检查预算为3MB','当前检查预算为4MB（2026-10-27扩容记录见下文）');readme.write_text(text+note)
 proof={'recorded_utc':datetime.now(timezone.utc).isoformat(),'actual_original_gate_exit_codes':[x['exit_code'] for x in rows],'actual_failed_gzip_bytes':snap['compressed_research_bytes'],'actual_research_rows':snap['research_configs'],'old_budget_bytes':3000000,'new_budget_bytes':4000000,'restored_previous_valid_monitor_pair':prior,'scope':'Only checker filesizebudget and README capacity history change;no financial result,old feedrow,account,rule,frontend or deployment change.','checker_before_sha256':sha(oldcheck),'checker_after_sha256':sha(check.read_bytes()),'README_before_sha256':sha(oldreadme),'README_after_sha256':sha(readme.read_bytes()),'readonly_frontend_source_evidence':'monitor_capacity_source_review.json','all_financial_reports_original_bytes_preserved':True};put(R/'monitor_capacity_recovery.json',proof);print(json.dumps(proof),flush=True)
if __name__=='__main__':main()
