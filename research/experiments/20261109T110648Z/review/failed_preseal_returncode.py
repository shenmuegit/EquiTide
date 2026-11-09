import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1]
args=["git","diff","--no-index","--check","/dev/null",str(R/"review/looser_entry_diagnostics_retry1.py")]
p=subprocess.run(args,cwd=ROOT,capture_output=True,text=True)
assert p.returncode==0
