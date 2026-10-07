"""Reuse allocation evaluator with the existing unfiltered channel component engine."""
import importlib.util,json,hashlib,sys
from pathlib import Path
T=Path(__file__).resolve().parent;R=T.parents[2]
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
allocation=load('allocation_reuse',R/'research/experiments/20261003T052049Z/evaluate.py')
channel=load('channel_reuse',R/'research/experiments/20261002T174933Z/evaluate.py')
allocation.ROUND=T;allocation.CACHE=R/'data/runs'/T.name
channel.signal=load('round_channel_signal',T/'signals.py');allocation.component=channel.component
if __name__=='__main__':
 plan=json.loads((T/'spec.json').read_text())
 for path,h in plan['reused_code_sha256'].items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==h
 allocation.main()
