"""Independent raw completed-bar, daily SMA/state/cost and cumulative minute-NAV audit."""
import gzip,hashlib,json,math,statistics,sys,urllib.parse
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ms=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*1000)
iso=lambda t:datetime.fromtimestamp(t/1000,timezone.utc).isoformat().replace('+00:00','Z')
def main():
 r=json.loads((ROUND/'forward_report.json').read_text());prior=json.loads((ROOT/r['source_report']).read_text());state=json.loads((ROOT/r['source_state']).read_text());nextstate=json.loads((ROUND/'forward_state.json').read_text());data=json.loads(gzip.decompress((ROUND/'forward_inputs.json.gz').read_bytes()));batch=json.loads((ROUND/'forward_batch.json').read_text());raw=[json.loads(x) for x in (ROOT/'research/automation/registry.jsonl').read_text().splitlines()];ledger=registry.read_records(ROOT/'research/automation/registry.jsonl')
 for p,h in r['source_hashes'].items():assert sha(ROOT/p)==h
 assert sha(ROOT/r['source_report'])==r['source_report_sha256'] and sha(ROOT/r['source_state'])==r['source_state_sha256'] and sha(ROUND/'forward_inputs.json.gz')==r['input_sha256']
 assert sha(ROOT/r['frozen_plan_path'])==r['frozen_plan_sha256']=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
 assert nextstate['source_report_sha256']==sha(ROUND/'forward_report.json') and nextstate['last_completed_mark_utc']==r['cutoff_utc'];assert nextstate['next_daily_decision_utc']=='2026-10-10T00:01:00Z'
 cut,begin,event=ms(r['cutoff_utc']),ms(r['resume_utc']),ms(state['next_daily_decision_utc']);day=event-60000
 oldinputs=json.loads(gzip.decompress((ROOT/prior['source_inputs_path']).read_bytes()));assert sha(ROOT/r['daily_overlap_source']['path'])==r['daily_overlap_source']['sha256'];first=json.loads(gzip.decompress((ROOT/r['daily_overlap_source']['path']).read_bytes()))
 assert len(r['provenance'])==4
 reconstructed={a:{k:[] for k in ('1m','1d')} for a in ('BTC','ETH')}
 for p in r['provenance']:
  bb=gzip.decompress((ROOT/p['raw_gzip_path']).read_bytes());assert hashlib.sha256(bb).hexdigest()==p['raw_response_sha256'] and sha(ROOT/p['raw_gzip_path'])==p['raw_gzip_sha256'];reconstructed[p['asset']][p['interval']]+=json.loads(bb)
  q=urllib.parse.parse_qs(urllib.parse.urlparse(p['url']).query);assert q['symbol']==[p['asset']+'USDT'] and q['interval']==[p['interval']] and int(q['endTime'][0])==ms(p['as_of_end_utc'])-1;assert p['status']==200 and p['timestamp_unit']=='milliseconds'
  assert p['retrieved_utc']>r['cutoff_utc']
 assert reconstructed==data
 for b in batch:
  fp=b['fingerprint'];assert registry.fingerprint(json.loads((ROOT/b['spec']).read_text()))==fp
  reserve=[x for x in raw if x['fingerprint']==fp and x['status']=='reserved'];assert len(reserve)==1 and reserve[0]['recorded_at_utc']<r['observation_started_utc']
  if ledger[fp]['status']!='reserved':assert ledger[fp]['status']=='rejected' and ledger[fp]['report_sha256']==sha(ROUND/'forward_report.json')
 axis=[];fills=0;dailychecks=0
 for z in data['BTC']['1m'][1:]:
  if z[0]==event:axis.append({'kind':'execution_reference','open_ts_ms':z[0],'available_utc':iso(z[0]),'NAV_index':10027+len(axis)})
  axis.append({'kind':'closed_minute_mark','open_ts_ms':z[0],'available_utc':iso(z[6]+1),'NAV_index':10027+len(axis)})
 assert r['append_axis']==axis and len(axis)==121 and axis[61]['NAV_index']==10088
 for asset in ('BTC','ETH'):
  bars=data[asset]['1m'];daily=data[asset]['1d'];prev=oldinputs[asset];prev=prev['1m'] if isinstance(prev,dict) else prev
  assert bars[0]==prev[-1] and len(bars)==121 and [z[0] for z in bars]==list(range(begin-60000,cut,60000))
  assert len(daily)==65 and [z[0] for z in daily]==list(range(day-65*86400000,day,86400000));assert daily[:-1]==first[asset]['1d'][1:]
  for seq,step,end in [(bars,60000,cut),(daily,86400000,day)]:assert all(z[6]+1==z[0]+step and z[6]+1<=end and D(z[3])<=D(z[4])<=D(z[2]) for z in seq)
  assert D(daily[-1][4])==D(next(z for z in bars if z[0]==day-60000)[4]);assert daily[-1][6]+1<event
  mean=sum(D(z[4]) for z in daily)/D(65);last=D(daily[-1][4]);adv=statistics.mean(float(z[7]) for z in daily[-20:]);cc=[float(z[4]) for z in daily[-21:]];sigma=statistics.stdev([math.log(b/a) for a,b in zip(cc,cc[1:])]);d=r['daily_decisions_by_asset'][asset]
  assert D(d['SMA65'])==mean and D(d['prior_close'])==last and d['lagged_daily_quote_ADV']==adv and d['lagged_daily_volatility']==sigma
  for k,s in r['configs']['forward_snapshot_'+asset]['scenes'].items():
   old=prior['configs']['forward_snapshot_'+asset]['scenes'][k];pos=state['positions_by_asset_and_cost'][asset][k];before=pos['desired_long'];want=before
   if before and last<mean*D('.99'):want=False
   elif not before and last>mean*D('1.01'):want=True
   assert d['before_desired_long']==before and d['desired_long']==want;assert d['action']==('enter' if want and not before else 'exit' if before and not want else 'hold_long' if want else 'hold_cash');dailychecks+=1
   cash,units=pos['cash_usdt'],pos['units'];v=old['equity_usdt'][:];new=[]
   for z in bars[1:]:
    if z[0]==event:
     reference=float(z[1]);assert d['reference_minute_open']==reference
     need_buy=want and units==0;need_sell=not want and units>0
     if need_buy or need_sell:
      budget=cash if need_buy else units*reference;assert budget/adv<=.001
      factor=int(k);impact=.5*sigma*math.sqrt(budget/adv)*factor;fee=.001*factor;spread=.0001*factor;slip=.0002*factor;price=reference*(1+(spread+slip+impact)*(1 if need_buy else -1));qty=cash/(price*(1+fee)) if need_buy else units
      if need_buy:cost=cash-qty*reference;cash=0.;units=qty
      else:cash=qty*price*(1-fee);cost=qty*reference-cash;units=0.
      new.append({'side':'buy' if need_buy else 'sell','reference':reference,'execution':price,'quantity':qty,'fee_rate':fee,'half_spread_rate':spread,'slippage_rate':slip,'impact_rate':impact,'lagged_daily_quote_ADV':adv,'lagged_daily_volatility':sigma,'participation':budget/adv,'cost_usdt':cost,'executed_at_utc':iso(event),'cash_after':cash,'units_after':units});fills+=1
     v.append(cash+units*reference)
    v.append(cash+units*float(z[4]));assert cash>=0 and units>=0
   assert v==s['equity_usdt'] and v[:10027]==old['equity_usdt'];assert s['trades']==old['trades']+new and s['cost_usdt']==old['cost_usdt']+sum(t['cost_usdt'] for t in new)
   assert s['new_executions']==len(new) and s['executions']==old['executions']+len(new) and s['round_trips']==old['round_trips']+sum(t['side']=='sell' for t in new)
   assert s['units']==units and s['cash_usdt']==cash and s['desired_long']==want
   assert nextstate['positions_by_asset_and_cost'][asset][k]=={'cash_usdt':cash,'units':units,'desired_long':want}
 assert [z[0] for z in data['BTC']['1m']]==[z[0] for z in data['ETH']['1m']]
 for k,s in r['configs']['forward_snapshot_combo']['scenes'].items():
  a=r['configs']['forward_snapshot_BTC']['scenes'][k];b=r['configs']['forward_snapshot_ETH']['scenes'][k];old=prior['configs']['forward_snapshot_combo']['scenes'][k]
  assert s['equity_usdt']==[x+y for x,y in zip(a['equity_usdt'],b['equity_usdt'])] and s['equity_usdt'][:10027]==old['equity_usdt']
  assert s['cost_usdt']==a['cost_usdt']+b['cost_usdt'] and s['executions']==a['executions']+b['executions'] and s['new_executions']==a['new_executions']+b['new_executions']
  assert s['component_states']=={aa:{'cash':r['configs']['forward_snapshot_'+aa]['scenes'][k]['cash_usdt'],'units':r['configs']['forward_snapshot_'+aa]['scenes'][k]['units']} for aa in ('BTC','ETH')}
 for cfg in r['configs'].values():
  for s in cfg['scenes'].values():
   v=s['equity_usdt'];assert len(v)==10148 and s['elapsed_minutes']==10139 and s['elapsed_complete_days']==7 and s['new_mark_minutes']==120 and s['new_reference_points']==1
   assert abs(s['net_return_pct']-100*(v[-1]/cfg['capital_usdt']-1))<1e-12
   peak=v[0];drawdown=0.
   for value in v:peak=max(peak,value);drawdown=max(drawdown,100*(1-value/peak))
   assert abs(drawdown-s['max_drawdown_pct'])<1e-12
   assert s['terminal_action']=='mark only;no forced exit'
 assert dailychecks==6
 print(json.dumps({'passed':True,'forward_scenes':9,'new_closed_marks_per_asset':120,'cumulative_minutes':10139,'complete_days':7,'NAV_points_per_scene':10148,'daily_reference_points_added':1,'original_daily_decisions_independently_checked':dailychecks,'daily_bars_per_asset':65,'overlap_daily_bars_checked_per_asset':64,'prior_NAV_prefix_preserved':10027,'new_component_executions':fills,'next_daily_decision_utc':nextstate['next_daily_decision_utc'],'report_sha256':sha(ROUND/'forward_report.json')}),flush=True)
if __name__=='__main__':main()
