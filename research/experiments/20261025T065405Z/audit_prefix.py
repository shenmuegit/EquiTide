"""Independent original330day ledger recovery and exact preterminal prefix equality."""
import csv,gzip,hashlib,json,io
from decimal import Decimal as D
import numpy as np
import engine
from run import ROOT,R,module,sha,put,reg

def near(a,b,tol=1e-9):assert abs(float(a)-float(b))<=tol*max(1,abs(float(a)),abs(float(b))),(a,b)

def recover_from_recorded_events(m,scene,counters,multiplier):
 state={'cash':D(10000),'signed_units':D(0),'entry_price':D(0),'entry_reference':D(0)};v=np.empty(len(m['ts']));events=sorted([(int(t['axis_index']),'trade',t) for t in scene['trades']]+[(int(f['axis_index']),'fund',f) for f in scene['funding_events']]);assert len({i for i,_,_ in events})==len(events);start=0
 for idx,kind,e in events:
  v[start:idx]=float(state['cash'])+float(state['signed_units'])*(m['axis_prices'][start:idx]-float(state['entry_price']))
  if kind=='trade':
   assert e['status']=='filled' and {k:D(x) for k,x in e['state_before'].items()}==state and e['trade_ts_ns']==int(m['ts'][idx]);q=state['signed_units'];cash=state['cash'];change=D(e['change_signed_units']);ref=D(e['reference']);px=D(e['execution']);fee=D(e['cost_parts']['fee']);cost=sum(D(x) for x in e['cost_parts'].values());assert abs(change)==D(e['quantity'])
   if e['opening']:
    assert q==0;new={'cash':cash-fee,'signed_units':change,'entry_price':px,'entry_reference':ref};assert abs(change)*px<=new['cash']
   else:
    assert change==-q;near(D(e['reference_price_PnL_usdt']),q*(ref-state['entry_reference']),1e-13);new={'cash':cash+q*(px-state['entry_price'])-fee,'signed_units':D(0),'entry_price':D(0),'entry_reference':D(0)}
   assert abs(cash+q*(ref-state['entry_price'])-(new['cash']+new['signed_units']*(ref-new['entry_price']))-cost)<D('1e-18');assert {k:D(x) for k,x in e['state_after'].items()}==new;state=new;counters['source_recorded_trades_checked']+=1
  else:
   assert int(m['codes'][idx])==4 and e['settlement_ts_ns']==int(m['ts'][idx]) and D(e['signed_units'])==state['signed_units'] and D(e['cash_before'])==state['cash'];base=-state['signed_units']*D(e['mark_price'])*D(e['realized_rate']);assert base==D(e['base_amount_usdt']);amount=D(e['amount_usdt']);assert amount==(base if base>=0 else base*multiplier)
   if amount:state['cash']+=amount
   assert state['cash']==D(e['cash_after']);counters['source_recorded_funding_checked']+=1
  start=idx
 v[start:]=float(state['cash'])+float(state['signed_units'])*(m['axis_prices'][start:]-float(state['entry_price']));assert state['signed_units']==0 and {k:D(x) for k,x in scene['terminal_state'].items()}==state
 # The actual event ledger and independent saved-state encoding must produce every same point.
 n=0
 for s in scene['state_segments']:
  a,b=s['axis_start'],s['axis_end_exclusive'];assert a==n;other=float(s['cash'])+float(s['signed_units'])*(m['axis_prices'][a:b]-float(s['entry_price']));assert np.array_equal(v[a:b],other);n=b
 assert n==len(v) and hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==scene['summary']['NAV_sha256_f64le'];return v

def main():
 plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());refs=json.loads((R/'prefix_sources.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');p=plan['prefix_comparison'];assert sha(ROOT/p['original_engine'])==p['original_engine_sha256'];oldengine=module(ROOT/p['original_engine'],'original_330_axis_for_prefix');oldmarkets={a:oldengine.load_market(a,fs) for a,fs in p['original_data'].items()};newmarkets={a:engine.load_market(a,fs) for a,fs in plan['data']['assets'].items()};counters={'source_recorded_trades_checked':0,'source_recorded_funding_checked':0};out=[]
 for row in batch:
  ref=refs[row['prefix_reference_index']];assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['spec'])==ref['spec_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'];rec=records[ref['fingerprint']];assert rec['result_available'] is True and rec['report_sha256']==ref['report_sha256'] and rec['status']==ref['original_status'];arc=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()));assert reg.fingerprint(arc['spec'])==ref['fingerprint'];newc=report['configs'][row['name']];newarc=json.loads(gzip.decompress((ROOT/newc['archive']).read_bytes()));a=row['asset'];oldm,newm=oldmarkets[a],newmarkets[a];oldidx=np.flatnonzero(oldm['ts']<oldm['end_ns']);newidx=np.flatnonzero(newm['ts']<oldm['end_ns']);assert len(oldidx)==len(newidx)==486090 and np.array_equal(oldm['ts'][oldidx],newm['ts'][newidx]) and np.array_equal(oldm['codes'][oldidx],newm['codes'][newidx]) and np.array_equal(oldm['axis_prices'][oldidx],newm['axis_prices'][newidx])
  for k,oldscene in arc['scenes'].items():
   original=recover_from_recorded_events(oldm,oldscene,counters,int(k));newscene=newarc['scenes'][k];v=np.empty(len(newm['ts']));covered=0
   for seg in newscene['state_segments']:
    left,right=seg['axis_start'],seg['axis_end_exclusive'];assert left==covered;v[left:right]=float(seg['cash'])+float(seg['signed_units'])*(newm['axis_prices'][left:right]-float(seg['entry_price']));covered=right
   assert covered==len(v) and hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==newc['scenes'][k]['NAV_sha256_f64le'];assert np.array_equal(original[oldidx],v[newidx]),(row['name'],k,'oldpreterminalprefix changed')
   indices=newm['daily_indices'][330:];tail=v[indices[0]:];daily=v[indices];ex=newc['scenes'][k]['extension40'];assert len(indices)==41 and len(tail)==58922 and daily.tolist()==ex['daily_equity_usdt'];assert ex['NAV_sha256_f64le']==hashlib.sha256(tail.astype('<f8').tobytes()).hexdigest();assert float(tail[0])==ex['start_NAV_usdt']==float(original[np.flatnonzero(oldm['codes']==8)[0]]) and float(tail[-1])==ex['end_NAV_usdt'];near(ex['net_return_pct'],100*(tail[-1]/tail[0]-1));near(ex['max_drawdown_pct'],100*np.max(1-tail/np.maximum.accumulate(tail)))
   for j,z in enumerate(ex['folds']):
    aa,bb=indices[j*5],indices[(j+1)*5];vv=v[aa:bb+1];near(z['net_return_pct'],100*(vv[-1]/vv[0]-1));near(z['max_drawdown_pct'],100*np.max(1-vv/np.maximum.accumulate(vv)))
   out.append({'name':row['name'],'fingerprint':row['fingerprint'],'original_fingerprint':ref['fingerprint'],'cost_multiplier':int(k),'old_report':ref['report'],'old_report_sha256':ref['report_sha256'],'old_full_NAV_sha256':oldscene['summary']['NAV_sha256_f64le'],'new_full_NAV_sha256':newc['scenes'][k]['NAV_sha256_f64le'],'exact_preterminal_prefix_points':len(oldidx),'prefix_sha256':hashlib.sha256(original[oldidx].astype('<f8').tobytes()).hexdigest(),'prefix_equal':True,'old_terminal_cost_left_in_old_report':True})
 assert len(out)==126;buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=list(out[0]),lineterminator='\n');w.writeheader();w.writerows(out);(R/'prefix_checks.csv').write_text(buf.getvalue());summary={'passed':True,'new_extended_configs':42,'old_source_results_unchanged':42,'cost_paths':126,'shared_points_per_path':486090,'shared_NAV_points_exactly_equal':126*486090,'old_full_NAV_sha_verified':True,'old_terminal_cost_kept_in_old_report':True,'new_continuous_state_not_reset_at_old_end':True,'old_signals_or_strategy_not_rerun':True,'extension40_inherited_state_NAV_and8x5day_diagnostics_verified':True,**counters,'report_sha256_when_checked':sha(R/'report.json')};put(R/'prefix_verification.json',summary);print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
