"""Read-only syntax verification after the actual pre-execution formatter error."""
import ast,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import sha,put,now
before=sha(R/'report.json');files=list(R.rglob('*.py'))
for p in files:ast.parse(p.read_text())
assert sha(R/'report.json')==before and json.loads((R/'formatter_syntax_verification.json').read_text())['passed'];put(R/'source_AST_verification.json',{'passed':True,'recorded_utc':now(),'Python_files_checked':len(files),'financial_report_sha256_unchanged':before,'no_model_account_or_registry_execution':True});print('PASS all current Python source AST, financial report unchanged, no financial/account reruns')
