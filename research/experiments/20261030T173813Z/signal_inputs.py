"""Reuse recorded pre-OPEN targets; independently verify their prior-close causality."""
import copy,gzip,json
from decimal import Decimal as D
from run import ROOT,R,sha,put,reg

def load_votes(plan):
 votes={a:[None]*404 for a in ['BTC','ETH']};allstates={a:[] for a in votes};n=0
 for fp,x in sorted(plan['signal_sources'].items()):
  assert sha(ROOT/x['archive'])==x['archive_sha256'] and sha(ROOT/x['spec'])==x['spec_sha256'] and sha(ROOT/x['report'])==x['report_sha256']
  arc=json.loads(gzip.decompress((ROOT/x['archive']).read_bytes()));assert arc['fingerprint']==fp==reg.fingerprint(arc['spec'])
  paths=[]
  for k in ['1','2','3']:
   z=arc['scenes'][k];assert z['summary']['rejected_orders']==z['summary']['cash_or_units_violations']==z['summary']['margin']['violations']==0 and len(z['decisions'])==370
   path=[]
   for i,d in enumerate(z['decisions'],33):
    assert d['decision_index']==i and d['signal_available_ts_ns']+60000000000==d['execution_ts_ns'] and d['channel_bounds']['channels_exclude_tested_close'] and d['channel_bounds']['tested_close_index']==i-1
    t=d['desired_direction'];assert t in [-1,0,1];q=D(d['state_after']['signed_units']);assert (1 if q>0 else -1 if q<0 else 0)==t
    path.append(t);n+=1
   paths.append(path)
  assert paths[0]==paths[1]==paths[2],'Source targets must be cost independent before reuse'
  allstates[x['asset']].append(paths[0])
 for a,paths in allstates.items():
  assert len(paths)==9
  for off in range(370):
   row=[z[off] for z in paths];votes[a][33+off]=(row.count(1),row.count(-1),row.count(0))
 assert n==19980
 return votes

def audit_votes(plan,markets):
 """Price-only source signal check, not a source financial strategy rerun."""
 independent={a:[[] for _ in range(404)] for a in ['BTC','ETH']};checks=0
 for fp,x in sorted(plan['signal_sources'].items()):
  arc=json.loads(gzip.decompress((ROOT/x['archive']).read_bytes()));m=markets[x['asset']];p=arc['spec']['parameters'];N=p['entry_lookback_days'];M=p['exit_lookback_days'];assert N in [20,25,30] and M in [5,10,15] and M<N
  prices=[int(v*D(10)**18) for v in m['closes']];prev=0;expected=[]
  for i in range(33,403):
   j=i-1;px=prices[j];upper=max(prices[j-N:j]);lower=min(prices[j-N:j]);xu=max(prices[j-M:j]);xl=min(prices[j-M:j]);entry=1 if px>upper else -1 if px<lower else 0
   if entry:t=entry
   elif prev>0:t=1 if px>=xl else 0
   elif prev<0:t=-1 if px<=xu else 0
   else:t=0
   expected.append(t)
   for k in ['1','2','3']:
    d=arc['scenes'][k]['decisions'][i-33];b=d['channel_bounds'];before=D(d['state_before']['signed_units']);after=D(d['state_after']['signed_units']);assert (1 if before>0 else -1 if before<0 else 0)==prev and (1 if after>0 else -1 if after<0 else 0)==t
    assert d['desired_direction']==t and d['signal_available_ts_ns']==m['start_ns']+(i-33)*86400000000000-60000000000 and d['execution_ts_ns']==d['signal_available_ts_ns']+60000000000
    assert b['entry_start_index']==j-N and b['exit_start_index']==j-M and b['entry_end_exclusive']==b['exit_end_exclusive']==j and b['tested_close_index']==j and b['channels_exclude_tested_close']
    assert int(D(b['entry_upper'])*D(10)**18)==upper and int(D(b['entry_lower'])*D(10)**18)==lower and int(D(b['exit_upper'])*D(10)**18)==xu and int(D(b['exit_lower'])*D(10)**18)==xl and b['final_direction']==t and b['fresh_entry_direction']==entry
    checks+=1
   independent[x['asset']][i].append(t);prev=t
 out={a:[None]*404 for a in independent}
 for a,rows in independent.items():
  for i in range(33,403):
   states=rows[i];assert len(states)==9;out[a][i]=(sum(t>0 for t in states),sum(t<0 for t in states),sum(t==0 for t in states))
 assert out==load_votes(plan) and checks==19980
 proof={'passed':True,'source_native_models':18,'source_cost_scenes_read':54,'source_preexecution_targets_independently_checked':checks,'source_signal_fingerprint_sets':{a:sorted(fp for fp,x in plan['signal_sources'].items() if x['asset']==a) for a in ['BTC','ETH']},'source_cost_paths_same_directions':True,'source_current_OPEN_fills_not_used_for_signal':True,'source_channel_bounds_exclude_tested_close':True,'source_PnL_not_used_to_select_votes_or_thresholds':True,'source_financial_model_reruns':0,'current_new_financial_evaluations':0}
 put(R/'source_signal_verification.json',proof);return out,{'source_signal_models_reused':18,'source_preexecution_targets_independently_checked':checks}
