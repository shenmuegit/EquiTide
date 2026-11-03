"""Read-only regression using an already completed real L4 midnight observation.
No capture, transition, trade or registry call; old reports and cashflows remain unchanged.
"""
import gzip,json
from decimal import Decimal as D
from fractions import Fraction as F
from common import *
A=ROOT/'research/experiments/20261101T235656Z/l4h02_observation';src=ROOT/'research/experiments/20261031T174613Z/prospective_l4/core.py';c=module(src,'unchanged_archived_L4_normalizer');b=c.bindings();rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));prev=rd(A/'previous_pointer.json');before=rd(ROOT/prev['state']);state=rd(A/'state.json');delta=gz(A/'delta.json.gz');im=rd(A/'input_manifest.json');packet=gz(ROOT/im['packet']);oldproof=rd(A.parent/'l4h02_verification.json');guard={str(p.relative_to(ROOT)):sha(p) for p in [*A.glob('*'),src,ROOT/im['packet']] if p.is_file()}
assert sha(ROOT/prev['state'])==prev['state_sha256'] and sha(ROOT/im['packet'])==im['sha256'];lo,cut,actions,ctx=c.normalize(packet,before,b);day=c.ns('2026-11-02T00:01:00Z');assert lo==c.ns('2026-11-01T22:10:00Z') and cut==c.ns('2026-11-02T00:10:00Z') and state['context']==ctx and sorted(t for t,k in actions if k==5)==[day]
assert [(z['timestamp_ns'],z['event_code']) for z in delta['NAV']]==sorted(actions) and len(actions)==122+3+2*len({t for t,k in actions if k==4})
for a in ['BTC','ETH']:
 partial=before['context'][a]['partial'];end=(partial['day']+1)*c.DAY;bars=[z for z in packet['assets'][a]['minutes'] if lo<=int(z[0])*c.MS<end];completed=next(z for z in ctx[a]['daily'] if z['day']==partial['day']);assert partial['count']+len(bars)==1440 and D(completed['quote_volume'])==D(partial['quote_volume'])+sum((D(z[7]) for z in bars),D(0)) and D(completed['close'])==D(bars[-1][4])
funds=[z for z in delta['journal'] if z['kind']=='funding'];decs=[z for z in delta['journal'] if z['kind']=='decision'];trades=[z for z in delta['journal'] if z['kind']=='trade'];assert len(funds)==6 and len(decs)==6 and not trades and oldproof['new_fills']==0
fundproof=[]
for z in funds:
 a=z['asset'];k=str(z['cost_multiplier']);q=D(before['books'][a][k]['signed_units']);base=-q*D(z['mark_price'])*D(z['rate']);amount=base*int(k) if base<0 else base;assert D(z['signed_units'])==q and D(z['base_amount_usdt'])==base and D(z['amount_usdt'])==amount and D(z['cash_before'])==D(before['books'][a][k]['cash']) and D(z['cash_after'])==D(z['cash_before'])+amount==D(state['books'][a][k]['cash']);assert lo<z['timestamp_ns']<day;fundproof.append({'asset':a,'cost':k,'timestamp_ns':z['timestamp_ns'],'held_units':str(q),'amount_usdt':str(amount)})
for z in decs:
 a=z['asset'];k=str(z['cost_multiplier']);rule=b['rules'][a];cls=[D(v['close']) for v in ctx[a]['daily'] if v['day']<day//c.DAY];q=D(before['books'][a][k]['signed_units']);actual=(q>0)-(q<0);rr=F(cls[-1])/F(cls[-1-rule['L']])-1;h=F(str(rule['H']))
 if a=='BTC':e=F(str(rule['E']));target=1 if rr>h else -1 if rr<-h else 1 if actual==1 and rr>-e else -1 if actual==-1 and rr<e else 0;returns=[str(rr)]
 else:slow=F(cls[-1])/F(cls[-1-rule['S']])-1;base=-1 if rr>h else 1 if rr<-h else actual if actual==1 and rr<0 or actual==-1 and rr>0 else 0;gate=(slow>0)-(slow<0);target=base if base==gate else 0;returns=[str(rr),str(slow)];assert rule['E']==0
 assert z['timestamp_ns']==day and z['wanted']==target and z['returns_exact']==returns and D(z['prior_complete_close'])==cls[-1]
assert state['nav_points']==before['nav_points']+len(actions) and all(sha(ROOT/p)==h for p,h in guard.items());put(R/'midnight_archive_verification.json',{'passed':True,'archived_round':A.parent.name,'source_sha256':guard,'read_only_archive':True,'new_current_observations_or_backtests':0,'new_current_registry_events':0,'archived_daily_events':1,'archived_original_daily_decisions':6,'archived_trades':0,'archived_actual_settlement_cashflows':fundproof,'complete_day_volume_close_reconstructed':True,'funding_before_original_daily_decision_verified':True,'scope':'Actual already-finished Nov2 midnight ledger regression only. This does not calculate or assert any Nov3 current funding/target/fill result; those require fresh reservation, closed capture and complete independent audit.'});print('PASS archived actual midnight day-volume/close,6fund cashflows,6original decisions and source hashes;0current calculations or writes to old evidence')
