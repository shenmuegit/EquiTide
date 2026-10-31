import numpy as np
from common import *
parent=module(ROOT/'research/experiments/20261025T145537Z/run.py','immutable_parent_alignment')
def load(plan):
 ms={a:core.load_market(a,fs) for a,fs in plan['data']['assets'].items()}
 for a,m in ms.items():m.update(first_ns=int(m['frame']['open_ts'][0]),fund_lookup={x['settlement_ts']:x for x in m['funds']},terminal_reference_decimal=m['frame']['open'][403*1440+1])
 return ms,parent.align(ms)
def recover(plan,ms,cm):
 vectors={};scenes={};configs={}
 for fp,ref in plan['read_only_references'].items():
  assert sha(ROOT/ref['archive'])==ref['archive_sha256'] and sha(ROOT/ref['report'])==ref['report_sha256'];rep=__import__('json').loads((ROOT/ref['report']).read_text());c=next(z for z in rep['configs'].values() if z['fingerprint']==fp);configs[fp]={**c,'scope':ref['scope'],'asset':ref['asset'],'capital_usdt':ref['capital_usdt']}
  if ref['scope']!='native':continue
  arc=__import__('json').loads(__import__('gzip').decompress((ROOT/ref['archive']).read_bytes()));m=ms[ref['asset']]
  for k,z in arc['scenes'].items():
   v=np.empty(len(m['ts']));last=0
   for s in z['state_segments']:
    a,b=s['axis_start'],s['axis_end_exclusive'];assert last==a<b;v[a:b]=float(s['cash'])+float(s['signed_units'])*(m['axis_prices'][a:b]-float(s['entry_price']));last=b
   assert last==len(v) and core.navhash(v)==z['summary']['NAV_sha256_f64le'] and z['summary']['daily_equity_usdt']==v[m['daily_indices']].tolist();vectors[fp,k]=v[cm['projections'][ref['asset']]];scenes[fp,k]=z['summary']
 for fp,ref in plan['read_only_references'].items():
  if ref['scope']!='parent':continue
  for k,z in configs[fp]['scenes'].items():
   b,e=ref['source_fingerprints'];wb,we=ref['raw_weights'];v=wb*vectors[b,k]+we*vectors[e,k];assert core.navhash(v)==z['NAV_sha256_f64le'];vectors[fp,k]=v
 return vectors,scenes,configs
