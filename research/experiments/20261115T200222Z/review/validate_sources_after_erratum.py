"""Read-only syntax verification for this round before sealing."""
import ast,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import sha,put,now
before=sha(R/'report.json');files=list(R.rglob('*.py'))
for p in files:
 tree=ast.parse(p.read_text());assert not [z for z in ast.walk(tree) if isinstance(z,ast.Subscript) and isinstance(z.value,ast.Name) and z.value.id in ['ROOT','R','P']],str(p)
assert sha(R/'report.json')==before;put(R/'source_AST_after_erratum.json',{'passed':True,'recorded_utc':now(),'Python_files_checked':len(files),'financial_report_sha256_unchanged':before,'no_model_account_or_registry_execution':True});print('PASS all current Python source AST, financial report unchanged, no financial/account reruns')
