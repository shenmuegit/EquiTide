import copy,gzip,json
import numpy as np
from common import *
from recent import recent
aligner=module(ROOT/'research/experiments/20261025T145537Z/run.py','immutable_full_axis_alignment')
def load(plan):
 ms={a:core.load_market(a,fs) for a,fs in plan['data']['assets'].items()}
 for a,m in ms.items():m.update(first_ns=int(m['frame']['open_ts'][0]),fund_lookup={x['settlement_ts']:x for x in m['funds']},terminal_reference_decimal=m['frame']['open'][403*1440+1])
 return ms,aligner.align(ms)
def recover(plan,ms,cm):
 vectors={};scenes={};configs={};native_arcs={};diagnostics={}
 for fp,ref in plan['read_only_references'].items():
  assert sha(ROOT/ref['archive'])==ref['archive_sha256'] and sha(ROOT/ref['report'])==ref['report_sha256'];doc=json.loads((ROOT/ref['report']).read_text());cfg=copy.deepcopy(next(x for x in doc['configs'].values() if x['fingerprint']==fp));cfg.update(scope=ref['scope'],asset=ref['asset'],capital_usdt=ref['capital_usdt']);configs[fp]=cfg
  if ref['scope']!='native':continue
  arc=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()));native_arcs[fp]=arc;m=ms[ref['asset']]
  for k,z in arc['scenes'].items():
   v=np.empty(len(m['ts']));last=0
   for s in z['state_segments']:
    a,b=s['axis_start'],s['axis_end_exclusive'];assert a==last and a<b;v[a:b]=float(s['cash'])+float(s['signed_units'])*(m['axis_prices'][a:b]-float(s['entry_price']));last=b
   assert last==len(v) and core.navhash(v)==z['summary']['NAV_sha256_f64le'] and v[0]==ref['capital_usdt'];vectors[fp,k]=v[cm['projections'][ref['asset']]];scenes[fp,k]=copy.deepcopy(z['summary'])
   if 'recent40' not in scenes[fp,k]:scenes[fp,k]['recent40']=recent(v,m);diagnostics.setdefault(fp,{})[k]=scenes[fp,k]['recent40']
   cfg['scenes'][k]=scenes[fp,k]
 pending={fp for fp,ref in plan['read_only_references'].items() if ref['scope']=='parent'}
 while pending:
  ready=[fp for fp in pending if all((source,'1') in vectors for source in plan['read_only_references'][fp]['source_fingerprints'])];assert ready
  for fp in ready:
   ref=plan['read_only_references'][fp];fps,weights=ref['source_fingerprints'],ref['raw_weights']
   for k,z in configs[fp]['scenes'].items():
    v=sum(w*vectors[source,k] for w,source in zip(weights,fps));assert core.navhash(v)==z['NAV_sha256_f64le'] and v[0]==ref['capital_usdt'];vectors[fp,k]=v
   pending.remove(fp)
 return vectors,scenes,configs,native_arcs,diagnostics
