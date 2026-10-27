"""Read-only independent continuous candidate NAV, carried books and hourly risk audit."""
import copy,gzip,hashlib,json,sys,urllib.parse
from collections import defaultdict
from decimal import Decimal as D
from datetime import datetime
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;W=R/'candidate_observation';SRC=ROOT/'research/experiments/20261026T110637Z';sys.path.insert(0,str(SRC));import prospective_core as c
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
read=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def near(a,b):assert abs(float(a)-float(b))<=1e-11*max(1,abs(float(a)),abs(float(b))),(a,b)
def main():
 point=read(ROOT/'research/automation/candidate_forward_latest.json');previous=read(W/'previous_pointer.json');before=read(ROOT/previous['state']);state=read(W/'state.json');rep=read(W/'report.json');delta=gz(W/'delta.json.gz');im=read(W/'input_manifest.json');complete=read(W/'complete.json');binding=c.bindings();guard={str(p):sha(p) for p in [W/'state.json',W/'report.json',W/'delta.json.gz',W/'complete.json',W/'previous_pointer.json',ROOT/'research/automation/candidate_forward_latest.json']}
 assert point['previous_pointer']=={'path':str((W/'previous_pointer.json').relative_to(ROOT)),'sha256':sha(W/'previous_pointer.json')} and complete['previous_pointer_sha256']==hashlib.sha256(c.canonical(previous)).hexdigest()
 for key,file in [('state','state.json'),('report','report.json'),('delta','delta.json.gz'),('complete','complete.json')]:assert point[key]==str((W/file).relative_to(ROOT)) and point[key+'_sha256']==sha(W/file)
 for key in ['state','report','delta','complete']:assert sha(ROOT/previous[key])==previous[key+'_sha256']
 assert sha(ROOT/im['packet'])==im['sha256'];packet=gz(ROOT/im['packet']);lo,cut,actions,contexts=c.normalize(packet,before,binding);assert lo==c.ns('2026-10-27T04:30:00Z') and cut==c.ns('2026-10-27T06:30:00Z')==state['cutoff_ns'] and state['context']==contexts and state['daily']==before['daily'] and state['books']==before['books']
 rawby=defaultdict(list)
 for item in im['provenance']:
  assert item['http_status']==200 and item['curl_exit_code']==0 and sha(ROOT/item['raw'])==item['sha256'];raw=gzip.decompress((ROOT/item['raw']).read_bytes());assert len(raw)==item['bytes'];data=json.loads(raw);u=urllib.parse.urlparse(item['url']);q=urllib.parse.parse_qs(u.query)
  if u.path in ['/fapi/v1/klines','/fapi/v1/markPriceKlines','/fapi/v1/fundingRate']:rawby[q['symbol'][0][:-4],u.path].extend(data)
 for a in ['BTC','ETH']:
  assert rawby[a,'/fapi/v1/klines']==packet['assets'][a]['minutes'] and rawby[a,'/fapi/v1/markPriceKlines']==packet['assets'][a]['hours'] and rawby[a,'/fapi/v1/fundingRate']==packet['assets'][a]['funding'] and len(packet['assets'][a]['minutes'])==122 and len(contexts[a]['daily'])==33
 assert delta['journal']==[] and len(actions)==len(delta['NAV'])==122 and {k for _,k in actions}=={1,2} and delta['previous_nav_chain_sha256']==before['nav_chain_sha256']
 prices=copy.deepcopy(before['last_prices']);risk=copy.deepcopy(before['risk']);checks=defaultdict(int);breaches=defaultdict(int);chain=before['nav_chain_sha256'];cushions=[]
 for row,key in zip(delta['NAV'],sorted(actions)):
  t,code=key;assert [row['timestamp_ns'],row['event_code']]==list(key) and tuple(before['last_key'])<key
  for a,p in actions[key].items():
   prices[a]=float(p['price'])
   if code==2:
    op=p['hour_open_ns']
    for k,book in before['books'][a].items():
     stack=risk[a][k]
     if op>=c.START:
      for i,item in enumerate(stack):
       end=stack[i+1]['t'] if i+1<len(stack) else t;b=item['state'];units=D(b['signed_units'])
       if units and item['t']<t and end>op and end>item['t']:
        adverse=D(p['low'] if units>0 else p['high']);cushion=D(b['cash'])+units*(adverse-D(b['entry_price']))-D('.01')*abs(units)*adverse;checks[a,k]+=1;breaches[a,k]+=int(cushion<=0);cushions.append(float(cushion))
     risk[a][k]=[{'t':t,'state':copy.deepcopy(book)}]
  values={a:{k:float(b['cash'])+float(b['signed_units'])*(prices[a]-float(b['entry_price'])) for k,b in books.items()} for a,books in before['books'].items()};values['COMBO']={k:values['BTC'][k]+values['ETH'][k] for k in ['1','2','3']};assert values==row['NAV'];chain=hashlib.sha256(bytes.fromhex(chain)+c.canonical(row)).hexdigest()
 assert state['last_prices']==prices and state['risk']==risk and chain==state['nav_chain_sha256']==delta['nav_chain_sha256']==rep['NAV_chain_sha256'] and state['nav_points']==before['nav_points']+122==399 and tuple(state['last_key'])==sorted(actions)[-1]
 for a in ['BTC','ETH']:
  for k,z in state['counters'][a].items():
   old=before['counters'][a][k]
   for f,v in z.items():assert v==(old[f]+checks[a,k] if f=='margin_checks' else old[f]+breaches[a,k] if f=='margin_proxy_violations' else old[f]),(a,k,f)
 pointers=[];p=previous
 while p:
  assert sha(ROOT/p['delta'])==p['delta_sha256'];pointers.append(gz(ROOT/p['delta']));ref=p.get('previous_pointer');assert ref is None or sha(ROOT/ref['path'])==ref['sha256'];p=read(ROOT/ref['path']) if ref else None
 prefix=[row for d in reversed(pointers) for row in d['NAV']];assert len(prefix)==before['nav_points']==277
 full=prefix+delta['NAV'];assert len(full)==399 and all((a['timestamp_ns'],a['event_code'])<(b['timestamp_ns'],b['event_code']) for a,b in zip(full,full[1:]));records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl')
 for a in ['BTC','ETH','COMBO']:
  sp=read(W/(a+'_spec.json'));fp=reg.fingerprint(sp);cfg=rep['configs']['forward_snapshot_candidate_'+a];assert cfg['fingerprint']==fp and records[fp]['status']=='rejected' and records[fp]['result_available'] is True and records[fp]['report_sha256']==sha(W/'report.json') and sp['parameters']['previous_state_sha256']==previous['state_sha256'];rv=[x for x in events if x['fingerprint']==fp and x['status']=='reserved'];assert len(rv)==1 and int(datetime.fromisoformat(rv[0]['recorded_at_utc'].replace('Z','+00:00')).timestamp()*1e9)<(W/'complete.json').stat().st_mtime_ns
  assert cfg['partial_observation'] and cfg['does_not_cancel_or_reset_frozen_plan'] and not cfg['criteria']['full180days'] and not cfg['criteria']['six_complete_folds']
  for k,z in cfg['scenes'].items():
   v=np.array([x['NAV'][a][k] for x in full]);capital=20000 if a=='COMBO' else 10000;near(z['net_return_pct'],100*(v[-1]/capital-1));near(z['max_drawdown_pct'],100*max(1-v/np.maximum.accumulate(v)));assert z['NAV_sha256_f64le']==hashlib.sha256(v.astype('<f8').tobytes()).hexdigest() and z['NAV_points']==399 and len(z['folds'])==0 and z['recent40'] is None and z['sharpe_365'] is None
 assert all(sha(Path(p))==h for p,h in guard.items()) and all(sha(ROOT/p)==h for p,h in read(R/'context.json')['account_hashes_before'].items())
 proof={'passed':True,'actual_observation_configs':3,'cumulative_finished_candidate_observations':12,'first_actual_window':False,'window_start_utc':'2026-10-27T04:30:00Z','cutoff_utc':'2026-10-27T06:30:00Z','new_elapsed_minutes':120,'elapsed_minutes':389,'cost_scenes':9,'complete30day_folds':0,'NAV_points_per_scene':399,'prior_NAV_prefix':277,'new_NAV_points_per_scene':122,'full_NAV_points_checked':3591,'new_exact_causal_decisions':0,'new_fills':0,'new_funding_settlements':0,'new_closed_hour_risk_checks':sum(checks.values()),'new_risk_proxy_violations':sum(breaches.values()),'minimum_checked_cushion_usdt':min(cushions) if cushions else None,'actual_HTTP200_response_pages_verified':len(im['provenance']),'raw_minutes_per_asset':122,'partial_first_hour_before_originalstart_not_liquidation_evidence':True,'partial_annualized_metrics_not_interpreted':True,'new_strategy_trials':0,'carried_books_cash_quantity_entry_cost_funding_unchanged':True,'original_candidate_and_paper10_unchanged':True,'no_financial_model_rerun':True,'report_sha256':sha(W/'report.json'),'state_sha256':sha(W/'state.json'),'pointer_sha256':sha(ROOT/'research/automation/candidate_forward_latest.json'),'parent_returns_pct':{k:s['net_return_pct'] for k,s in rep['configs']['forward_snapshot_candidate_COMBO']['scenes'].items()},'parent_drawdowns_pct':{k:s['max_drawdown_pct'] for k,s in rep['configs']['forward_snapshot_candidate_COMBO']['scenes'].items()}};put(R/'candidate_verification.json',proof);print(json.dumps(proof),flush=True)
if __name__=='__main__':main()
