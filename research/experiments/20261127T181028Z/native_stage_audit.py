"""Run the same independently bound full ledger/policy audit on completed native banks before parent use."""
from pathlib import Path
import hashlib,json,ast
R=Path(__file__).resolve().parent;ROOT=R.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();b=json.loads((R/'code_binding_before_evaluation.json').read_text());old=R/'audit.py';assert sha(old)==b['source_sha256'][str(old.relative_to(ROOT))]
s=old.read_text();s=s.replace("R/'report.json'","R/'native_report.json'").replace("R/'verification.json'","R/'native_stage_verification.json'");ast.parse(s);exec(compile(s,str(old)+'[native_stage]','exec'),{'__name__':'__main__','__file__':str(old)})
