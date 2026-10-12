"""Invoke the frozen paper10 executor with a GET-only curl transport shim."""
import runpy,sys,urllib.request
from pathlib import Path
T=Path(__file__).resolve().parents[1]
ROOT=T.parents[1]
sys.path.insert(0,str(Path(__file__).resolve().parent))
import curl_public_get
urllib.request.urlopen=curl_public_get.urlopen
sys.argv=[str(T/'run.py'),'--hold-lock']
runpy.run_path(str(T/'run.py'),run_name='__main__')
