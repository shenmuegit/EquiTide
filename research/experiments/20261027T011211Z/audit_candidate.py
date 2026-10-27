"""Independent first-window input, integer-signal, Decimal-fill, cash and NAV audit."""
import csv,gzip,hashlib,importlib.util,json,math,statistics,sys,urllib.parse
from collections import Counter,defaultdict
from decimal import Decimal as D,ROUND_CEILING,ROUND_FLOOR
from fractions import Fraction as F
from datetime import datetime
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;W=R/'candidate_observation';SRC=ROOT/'research/experiments/20261026T110637Z';sys.path.insert(0,str(SRC));import prospective_core as c
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
read=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def near(a,b,tol=1e-11):assert abs(float(a)-float(b))<=tol*max(1,abs(float(a)),abs(float(b))),(a,b)
def main():
 binding=c.bindings();point=read(ROOT/'research/automation/candidate_forward_latest.json');state=read(W/'state.json');rep=read(W/'report.json');delta=gz(W/'delta.json.gz');complete=read(W/'complete.json');im=read(W/'input_manifest.json');before={str(p):sha(p) for p in [W/'state.json',W/'report.json',W/'delta.json.gz',W/'complete.json',ROOT/'research/automation/candidate_forward_latest.json']};assert complete['previous_pointer_sha256'] is None and point['previous_pointer'] is None and point['plan_sha256']==binding['plan_sha256']
 for key,file in [('state','state.json'),('report','report.json'),('delta','delta.json.gz'),('complete','complete.json')]:assert point[key]==str((W/file).relative_to(ROOT)) and point[key+'_sha256']==sha(W/file)
 for key,file in [('state','state.json'),('report','report.json'),('delta','delta.json.gz')]:assert complete[key+'_sha256']==sha(W/file)
 assert sha(ROOT/im['packet'])==im['sha256'];packet=gz(ROOT/im['packet']);assert packet['cutoff_ns']==c.ns('2026-10-27T00:30:00Z')==state['cutoff_ns'];lo,cut,actions,contexts=c.normalize(packet,None,binding);assert lo==c.START and state['context']==contexts and cut-lo==29*c.MIN
 rawby=defaultdict(list);response_count=0;cached=0
 for item in im['provenance']:
  assert item['http_status']==200 and sha(ROOT/item['raw'])==item['sha256'];raw=gzip.decompress((ROOT/item['raw']).read_bytes());assert len(raw)==item['bytes'];data=json.loads(raw);u=urllib.parse.urlparse(item['url']);q=urllib.parse.parse_qs(u.query);response_count+=1;cached+=int(item.get('reused_verified_prior_capture',False))
  if u.path in ['/fapi/v1/klines','/fapi/v1/markPriceKlines','/fapi/v1/fundingRate']:rawby[q['symbol'][0][:-4],u.path].extend(data)
 for a in ['BTC','ETH']:
  assert rawby[a,'/fapi/v1/klines']==packet['assets'][a]['minutes'] and rawby[a,'/fapi/v1/markPriceKlines']==packet['assets'][a]['hours'] and rawby[a,'/fapi/v1/fundingRate']==packet['assets'][a]['funding'];assert len(packet['assets'][a]['minutes'])==47551 and len(contexts[a]['daily'])==33
 books={a:{str(k):{'cash':D(10000),'signed_units':D(0),'entry_price':D(0),'entry_reference':D(0)} for k in [1,2,3]} for a in ['BTC','ETH']};journal=defaultdict(list)
 for x in delta['journal']:journal[x['timestamp_ns'],x['event_code']].append(x)
 keys=sorted(actions);assert [(x['timestamp_ns'],x['event_code']) for x in delta['NAV']]==keys and len(keys)==state['nav_points']==33 and delta['previous_nav_chain_sha256']=='0'*64
 prices={};want={};decisions=trades=0;costs=defaultdict(lambda:D(0));chain='0'*64;series={a:{k:[] for k in ['1','2','3']} for a in ['BTC','ETH','COMBO']};daily_first={}
 for row,key in zip(delta['NAV'],keys):
  ts,code=key
  for a,p in actions[key].items():prices[a]=float(p['price'])
  for x in journal[key]:
   a=x['asset'];k=str(x['cost_multiplier']);book=books[a][k];p=actions[key][a];q=book['signed_units'];direction=1 if q>0 else -1 if q<0 else 0
   if x['kind']=='decision':
    closes=[F(D(v)) for v in p['closes']];L=31 if a=='BTC' else 3;roc=closes[-1]/closes[-1-L]-1;H=F('0.04') if a=='BTC' else F('0.02');ret=x['returns_exact'];assert F(ret[0])==roc
    if a=='BTC':target=1 if roc>H else -1 if roc<-H else 1 if direction==1 and roc>F('-0.01') else -1 if direction==-1 and roc<F('0.01') else 0
    else:
     slow=closes[-1]/closes[-29]-1;assert F(ret[1])==slow;base=-1 if roc>H else 1 if roc<-H else 1 if direction==1 and roc<0 else -1 if direction==-1 and roc>0 else 0;target=base if (base==1 and slow>0 or base==-1 and slow<0) else 0
    assert code==6 and x['wanted']==target and D(x['prior_complete_close'])==D(p['closes'][-1]);want[a,k]=target;decisions+=1
   elif x['kind']=='trade':
    assert code==7 and x['opening'] and x['status']=='filled' and q==0 and {f:D(v) for f,v in x['state_before'].items()}==book;meta=binding['metadata'][a];lot=D(meta['lot_size']);tick=D(meta['tick_size']);qty=(D(binding['rules'][a]['N'])/D(p['closes'][-1])/lot).to_integral_value(rounding=ROUND_FLOOR)*lot;change=qty*want[a,k];assert change==D(x['change_signed_units']) and qty==D(x['quantity']) and change!=0
    ref=D(p['price']);ADV=D(p['ADV']);sigma=D(p['sigma']);part=qty*ref/ADV;assert 0<part<=D('.001') and D(x['participation'])==part and D(x['lagged_ADV'])==ADV and D(x['lagged_sigma'])==sigma;m=int(k);fee=D('.0005')*m;spread=D('.0001')*m;slip=D('.0002')*m;impact=D('.5')*sigma*part.sqrt()*m;theory=ref*(1+(spread+slip+impact)*(1 if change>0 else -1));px=(theory/tick).to_integral_value(rounding=ROUND_CEILING if change>0 else ROUND_FLOOR)*tick;parts={'fee':qty*px*fee,'half_spread':qty*ref*spread,'slippage':qty*ref*slip,'impact':qty*ref*impact,'tick_rounding':qty*abs(px-theory)}
    for f,v in parts.items():assert abs(v-D(x['cost_parts'][f]))<D('1e-18')
    assert D(x['execution'])==px and qty%lot==0 and qty*px>=D(meta['min_notional']);new={'cash':book['cash']-parts['fee'],'signed_units':change,'entry_price':px,'entry_reference':ref};assert qty*px<=new['cash'] and {f:D(v) for f,v in x['state_after'].items()}==new;books[a][k]=new;costs[a,k]+=sum(parts.values());near(x['cost_usdt'],sum(parts.values()));trades+=1
   else:raise AssertionError('No funding/close should occur in first29minute interval')
  assert set(prices)=={'BTC','ETH'}
  for k in ['1','2','3']:
   vals={a:float(books[a][k]['cash'])+float(books[a][k]['signed_units'])*(prices[a]-float(books[a][k]['entry_price'])) for a in ['BTC','ETH']};vals['COMBO']=vals['BTC']+vals['ETH']
   for a,v in vals.items():assert v==row['NAV'][a][k];series[a][k].append(v)
  chain=hashlib.sha256(bytes.fromhex(chain)+c.canonical(row)).hexdigest()
 assert decisions==6 and trades==3 and chain==state['nav_chain_sha256']==delta['nav_chain_sha256']==rep['NAV_chain_sha256'];records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl')
 for a in ['BTC','ETH']:
  for k in ['1','2','3']:
   assert {f:D(v) for f,v in state['books'][a][k].items()}==books[a][k];z=state['counters'][a][k];assert not any(z[f] for f in ['rejected_orders','cash_violations','margin_proxy_violations','margin_checks','funding_settlements','round_trips']);assert D(z['funding_usdt'])==0 and D(z['cost_usdt'])==costs[a,k]
 for a in ['BTC','ETH','COMBO']:
  sp=read(W/(a+'_spec.json'));fp=reg.fingerprint(sp);cfg=rep['configs']['forward_snapshot_candidate_'+a];assert cfg['fingerprint']==fp and records[fp]['status']=='rejected' and records[fp]['result_available'] is True and records[fp]['report_sha256']==sha(W/'report.json');reservations=[x for x in events if x['fingerprint']==fp and x['status']=='reserved'];assert len(reservations)==1 and int(datetime.fromisoformat(reservations[0]['recorded_at_utc'].replace('Z','+00:00')).timestamp()*1_000_000_000)<(W/'complete.json').stat().st_mtime_ns
  assert cfg['partial_observation'] and cfg['does_not_cancel_or_reset_frozen_plan'] and not cfg['criteria']['full180days'] and not cfg['criteria']['six_complete_folds']
  for k,z in cfg['scenes'].items():
   v=np.asarray(series[a][k]);capital=20000 if a=='COMBO' else 10000;near(z['net_return_pct'],100*(v[-1]/capital-1));near(z['max_drawdown_pct'],100*max(1-v/np.maximum.accumulate(v)));assert z['NAV_sha256_f64le']==hashlib.sha256(v.astype('<f8').tobytes()).hexdigest() and z['NAV_points']==33 and len(z['folds'])==0 and z['recent40'] is None and z['sharpe_365'] is None
 assert all(sha(Path(p))==h for p,h in before.items());assert all(sha(ROOT/p)==h for p,h in read(R/'context.json')['account_hashes_before'].items())
 proof={'passed':True,'first_actual_candidate_observations':3,'window_start_utc':'2026-10-27T00:01:00Z','cutoff_utc':'2026-10-27T00:30:00Z','elapsed_minutes':29,'cost_scenes':9,'complete30day_folds':0,'NAV_points_per_scene':33,'full_NAV_points_checked':297,'independent_exact_causal_decisions':decisions,'independent_Decimal_fills':trades,'actual_HTTP200_response_pages_verified':response_count,'cached_successful_closed_pages_reused':cached,'raw_minutes_per_asset':47551,'funding_settlements_during_window':0,'closed_hour_margin_checks':0,'partial_hours_not_exact_liquidation_evidence':True,'partial_annualized_metrics_not_interpreted':True,'new_strategy_trials':0,'original_candidate_and_paper10_unchanged':True,'no_financial_model_rerun':True,'report_sha256':sha(W/'report.json'),'state_sha256':sha(W/'state.json'),'pointer_sha256':sha(ROOT/'research/automation/candidate_forward_latest.json'),'parent_returns_pct':{k:s['net_return_pct'] for k,s in rep['configs']['forward_snapshot_candidate_COMBO']['scenes'].items()},'parent_drawdowns_pct':{k:s['max_drawdown_pct'] for k,s in rep['configs']['forward_snapshot_candidate_COMBO']['scenes'].items()}};put(R/'candidate_verification.json',proof);print(json.dumps(proof),flush=True)
if __name__=='__main__':main()
