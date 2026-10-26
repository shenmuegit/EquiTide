"""Independent frozen-rule daily decision, floating-book, raw-data and full NAV audit."""
import gzip,hashlib,json,math,statistics,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ms=lambda t:int(datetime.fromisoformat(t.replace('Z','+00:00')).timestamp()*1000)
iso=lambda t:datetime.fromtimestamp(t/1000,timezone.utc).isoformat().replace('+00:00','Z')
readgz=lambda p:json.loads(gzip.decompress(p.read_bytes()))
def near(a,b,tol=1e-9):assert math.isclose(float(a),float(b),rel_tol=1e-10,abs_tol=tol),(a,b)
def drawdown(values):
 peak=values[0];loss=0.
 for v in values:peak=max(peak,v);loss=max(loss,100*(1-v/peak))
 return loss

def main():
 report=json.loads((R/'forward_report.json').read_text());plan=json.loads((R/'forward_resume_plan.json').read_text());state=json.loads((ROOT/plan['source_state']).read_text());old=json.loads((ROOT/plan['source_report']).read_text());nxt=json.loads((R/'forward_state.json').read_text());inputs=readgz(R/'forward_inputs.json.gz');batch=json.loads((R/'forward_batch.json').read_text())
 assert sha(ROOT/plan['source_report'])==plan['report_sha256']==report['source_report_sha256']
 assert sha(ROOT/plan['source_state'])==plan['state_sha256']==report['source_state_sha256']
 assert sha(ROOT/plan['frozen_original_plan'])==report['frozen_plan_sha256']==state['frozen_plan_sha256']=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
 assert sha(R/'forward_inputs.json.gz')==report['input_sha256'] and nxt['source_report_sha256']==sha(R/'forward_report.json')
 assert nxt['source_report']==str((R/'forward_report.json').relative_to(ROOT))
 for path,h in report['source_hashes'].items():assert sha(ROOT/path)==h
 begin,cut=ms(plan['resume_utc']),ms(plan['cutoff_utc']);events=list(range(ms(state['next_daily_decision_utc']),cut,86400000));assert len(events)==1 and iso(events[0])=='2026-10-26T00:01:00Z'
 assert begin==ms(old['cutoff_utc']) and cut<=ms(report['observation_started_utc'])
 points=len(old['configs']['forward_snapshot_combo']['scenes']['1']['equity_usdt']);newminutes=(cut-begin)//60000;totalpoints=points+newminutes+len(events);elapsed=old['configs']['forward_snapshot_combo']['scenes']['1']['elapsed_minutes']+newminutes
 assert newminutes==120 and nxt['last_completed_mark_utc']==plan['cutoff_utc'] and nxt['next_daily_decision_utc']==iso(events[-1]+86400000)
 axis=report['append_axis'];assert axis['closed_minute_open_ms_range']==[begin,cut,60000] and axis['old_NAV_points_preserved']==points and axis['new_NAV_points_per_scene']==newminutes+1
 assert axis['daily_execution_references']==[{'open_ts_ms':e,'NAV_index':points+(e-begin)//60000+i} for i,e in enumerate(events)]
 ledger=registry.read_records(ROOT/'research/automation/registry.jsonl');all_events=registry.read_events(ROOT/'research/automation/registry.jsonl')
 for row in batch:
  fp=row['fingerprint'];assert registry.fingerprint(json.loads((ROOT/row['spec']).read_text()))==fp
  reservations=[e for e in all_events if e['fingerprint']==fp and e['status']=='reserved'];assert len(reservations)==1 and ms(reservations[0]['recorded_at_utc'])<ms(report['observation_started_utc'])
  assert ledger[fp]['status'] in ('reserved','rejected')
  if ledger[fp]['status']=='rejected':assert ledger[fp]['report_sha256']==sha(R/'forward_report.json') and ledger[fp]['result_available'] is True
 assert len(report['provenance'])==4
 for item in report['provenance']:
  raw=gzip.decompress((ROOT/item['raw_gzip_path']).read_bytes());assert sha(ROOT/item['raw_gzip_path'])==item['raw_gzip_sha256'] and hashlib.sha256(raw).hexdigest()==item['raw_response_sha256']
  assert json.loads(raw)==inputs[item['asset']][item['interval']] and item['status']==200 and ms(item['retrieved_utc'])>cut
 original_inputs=readgz(ROOT/old['source_inputs_path']);overlap=readgz(ROOT/plan['daily_overlap_source']);assert sha(ROOT/plan['daily_overlap_source'])==plan['daily_overlap_sha256']
 orders=0
 for asset,capital in [('BTC',1500),('ETH',500)]:
  bars=inputs[asset]['1m'];daily=inputs[asset]['1d'];priorbars=original_inputs[asset];priorbars=priorbars['1m'] if isinstance(priorbars,dict) else priorbars
  assert bars[0]==priorbars[-1] and len(bars)==newminutes+1 and [b[0] for b in bars]==list(range(begin-60000,cut,60000))
  assert all(b[6]+1==b[0]+60000 and b[6]+1<=cut and D(b[3])<=D(b[4])<=D(b[2]) and D(b[4])>0 for b in bars)
  assert len(daily)==65 and [b[0] for b in daily]==list(range(events[0]-60000-65*86400000,events[0]-60000,86400000))
  assert all(b[6]+1==b[0]+86400000 and b[6]+1<=events[0]-60000 for b in daily)
  indexed={b[0]:b for b in daily};matches=[b for b in overlap[asset]['1d'] if b[0] in indexed];assert len(matches)==64 and all(indexed[b[0]]==b for b in matches)
  assert D(daily[-1][4])==D(next(b[4] for b in bars if b[0]==daily[-1][6]+1-60000))
  close=D(daily[-1][4]);sma=sum(D(b[4]) for b in daily)/65;adv=statistics.mean(float(b[7]) for b in daily[-20:]);closes=[float(b[4]) for b in daily[-21:]];sigma=statistics.stdev(math.log(b/a) for a,b in zip(closes,closes[1:]))
  decisions=report['daily_decisions_by_asset'][asset];assert len(decisions)==1;decision=decisions[0]
  assert D(decision['SMA65'])==sma and D(decision['prior_close'])==close and ms(decision['executed_at_utc'])==events[0] and ms(decision['last_daily_close_available_utc'])==events[0]-60000
  near(decision['lagged_daily_quote_ADV'],adv);near(decision['lagged_daily_volatility'],sigma)
  cfg=report['configs']['forward_snapshot_'+asset];oldcfg=old['configs']['forward_snapshot_'+asset];assert cfg['latest_daily_decision']==decision
  for key,scene in cfg['scenes'].items():
   prior=oldcfg['scenes'][key];position=state['positions_by_asset_and_cost'][asset][key];cash,units,want=position['cash_usdt'],position['units'],position['desired_long'];values=prior['equity_usdt'][:];assert len(values)==points and scene['trades'][:len(prior['trades'])]==prior['trades']
   expected_want=False if want and close<sma*D('.99') else True if not want and close>sma*D('1.01') else want
   assert decision['before_desired_long']==want and decision['desired_long']==expected_want
   newtrades=scene['trades'][len(prior['trades']):];trade_by_time={ms(t['executed_at_utc']):t for t in newtrades};assert len(trade_by_time)==len(newtrades)
   assert all(t in events for t in trade_by_time)
   for bar in bars[1:]:
    if bar[0] in events:
     ref=float(bar[1]);near(decision['reference_minute_open'],ref);buy=expected_want and units==0;sell=not expected_want and units>0;trade=trade_by_time.get(bar[0])
     if buy or sell:
      assert trade is not None and trade['side']==('buy' if buy else 'sell');mult=int(key);budget=cash if buy else units*ref;part=budget/adv;assert 0<=part<=.001
      fee=D('.001')*mult;adverse=(D('.0001')+D('.0002')+D('.5')*D(str(sigma))*D(str(part)).sqrt())*mult
      execution=D(str(ref))*(1+adverse if buy else 1-adverse);quantity=D(str(cash))/(execution*(1+fee)) if buy else D(str(units));newcash=D(0) if buy else quantity*execution*(1-fee);newunits=quantity if buy else D(0)
      near(trade['reference'],ref);near(trade['execution'],execution);near(trade['quantity'],quantity,1e-12);near(trade['cash_after'],newcash);near(trade['units_after'],newunits,1e-12);near(trade['fee_rate'],fee);near(trade['half_spread_rate'],D('.0001')*mult);near(trade['slippage_rate'],D('.0002')*mult);near(trade['impact_rate'],D('.5')*D(str(sigma))*D(str(part)).sqrt()*mult)
      near(cash+units*ref-trade['cash_after']-trade['units_after']*ref,trade['cost_usdt']);cash,units=trade['cash_after'],trade['units_after'];orders+=1
     else:assert trade is None
     want=expected_want;values.append(cash+units*ref)
    values.append(cash+units*float(bar[4]));assert cash>=0 and units>=0
   assert scene['equity_usdt']==values and values[:points]==prior['equity_usdt'] and len(values)==totalpoints
   assert scene['cash_usdt']==cash and scene['units']==units and scene['desired_long']==want and nxt['positions_by_asset_and_cost'][asset][key]=={'cash_usdt':cash,'units':units,'desired_long':want}
   near(scene['cost_usdt'],prior['cost_usdt']+sum(t['cost_usdt'] for t in newtrades));assert scene['executions']==prior['executions']+len(newtrades) and scene['new_executions']==len(newtrades) and scene['new_reference_points']==1
   assert scene['round_trips']==prior['round_trips']+sum(t['side']=='sell' for t in newtrades)
   near(scene['net_return_pct'],100*(values[-1]/capital-1));near(scene['max_drawdown_pct'],drawdown(values));assert scene['elapsed_minutes']==elapsed and scene['elapsed_complete_days']==elapsed//1440
 for key,scene in report['configs']['forward_snapshot_combo']['scenes'].items():
  a=report['configs']['forward_snapshot_BTC']['scenes'][key];b=report['configs']['forward_snapshot_ETH']['scenes'][key];prior=old['configs']['forward_snapshot_combo']['scenes'][key];values=[x+y for x,y in zip(a['equity_usdt'],b['equity_usdt'])]
  assert scene['equity_usdt']==values and values[:points]==prior['equity_usdt'];near(scene['cost_usdt'],a['cost_usdt']+b['cost_usdt']);near(scene['max_drawdown_pct'],drawdown(values));near(scene['net_return_pct'],100*(values[-1]/2000-1))
  assert scene['executions']==a['executions']+b['executions'] and scene['new_reference_points']==1
 baseline=json.loads((R/'context.json').read_text())['account_hashes_before'];assert all(sha(ROOT/p)==h for p,h in baseline.items())
 out={'passed':True,'report_sha256':sha(R/'forward_report.json'),'daily_decisions_per_asset':1,'cost_scenes':9,'forward_scenes':9,'new_closed_marks_per_asset':newminutes,'new_reference_points_per_scene':1,'original_NAV_prefix':points,'NAV_points_per_scene':totalpoints,'cumulative_minutes':elapsed,'complete_days':elapsed//1440,'new_component_virtual_orders_all_costs':orders,'next_daily_decision_utc':nxt['next_daily_decision_utc'],'raw_pages':4,'independent_frozen_signal_cost_balance_NAV_and_nextstate_verified':True,'paper10_and_old_sources_unchanged':True}
 (R/'forward_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)

if __name__=='__main__':main()
