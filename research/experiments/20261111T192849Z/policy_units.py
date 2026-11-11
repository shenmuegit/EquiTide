"""Synthetic strict hurdle, actual interval funding budgets and publication-time causality."""
import ast,copy,json,sys
from fractions import Fraction as F
from decimal import Decimal as D
from common import *
import engine
if '--inclusive' in sys.argv:
 src=(ROOT/'research/experiments/20261025T065405Z/engine.py').read_text();fn=next(n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name=='target');body=ast.get_source_segment(src,fn);exec(compile(body.replace('r>h','r>=h').replace('r < -h','r <= -h'),'<synthetic_inclusive_mutant>','exec'),engine.btc.__dict__)
if '--future-publication' in sys.argv:
 src=(R/'engine.py').read_text();fn=next(n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name=='median_funding');body=ast.get_source_segment(src,fn);assert " and e['available_ts']<=signal_ns" in body;exec(compile(body.replace(" and e['available_ts']<=signal_ns",''),'<synthetic_future_funding_mutant>','exec'),engine.__dict__)
if '--fixed-interval' in sys.argv:
 src=(R/'engine.py').read_text();fn=next(n for n in ast.parse(src).body if isinstance(n,ast.FunctionDef) and n.name=='carry_cap');body=ast.get_source_segment(src,fn);assert "hours=event['events'][0].get('entry_interval_hours')" in body;exec(compile(body.replace("hours=event['events'][0].get('entry_interval_hours')","hours=D(8)"),'<synthetic_fixed8h_mutant>','exec'),engine.__dict__)
cases=0
for h in [.0275,.03,.0325]:
 for end in [D('103'),D('97'),D('99'),D('101')]:
  for actual in [-1,0,1]:
   m={'asset':'BTC','closes':[D('100')]*35};m['closes'][32]=end;sp={'parameters':{'lookback_days':29,'return_hurdle':h,'exit_buffer_fraction':.01}};r=F(end)/100-1;hh=F(str(h));ee=F('.01');wanted=1 if r>hh else -1 if r<-hh else 1 if actual==1 and r>-ee else -1 if actual==-1 and r<ee else 0;got,audit=engine.decide(sp,m,33,actual);assert got==wanted and audit['return_exact']==str(r);future=copy.deepcopy(m);future['closes'][33]=D('99999');future['closes'][34]=D('.001');assert engine.decide(sp,future,33,actual)==(got,audit);cases+=1
sn=100*DAY;latest=sn-HOUR;interval=8*HOUR+1000000;times=[latest,latest-interval,latest-interval-8*HOUR,latest-interval-16*HOUR];rates=['.00011','.00009','.0002','-.0001'];events=[{'settlement_ts':t,'available_ts':t+HOUR,'realized_rate':D(rate),'source_index':j,'entry_interval_hours':D(interval)/D(HOUR) if j==0 else D(8)} for j,(t,rate) in enumerate(zip(times,rates))];unpublished={'settlement_ts':sn-HOUR-HOUR//2,'available_ts':sn+1,'realized_rate':D(10),'source_index':999,'entry_interval_hours':D(8)};event=engine.median_funding(events+[unpublished],sn,4);assert event['count']==4 and event['median_rate']==D('.0001') and [x['source_index'] for x in event['events']]==[0,1,2,3]
for ratio in [.00875,.01,.01125]:
 cap=engine.carry_cap(D('.03'),ratio,event);expected=min(D('.0002'),D(str(ratio))*D('.03')*(D(interval)/D(HOUR))/24);assert cap==expected
 for raw,actual in [(1,0),(1,1),(-1,0),(-1,-1)]:
  got,a=engine.funding_filter(raw,actual,event,sn,cap);out=max(D(raw)*D('.0001'),D(0));block=raw!=actual and out>expected;assert got==(0 if block else raw) and a['blocked']==block and a['applied']==(raw!=actual);cases+=1
assert engine.median_funding(events[:3],sn,4) is None and engine.carry_cap(D('.03'),.01,None) is None
assert engine.funding_filter(1,0,None,sn,None)[0]==0 and engine.funding_filter(1,1,None,sn,None)[0]==1
if len(sys.argv)==1:put(R/'policy_primitive_verification.json',{'passed':True,'synthetic_only':True,'cases':cases,'actual_engine_decide_and_funding_helpers_executed':True,'BTC_strict_entry_and_exit_boundaries':True,'BTC_future_close_invariance':True,'funding4_even_signed_median':True,'funding_unpublished_settlement_excluded':True,'actual8hour_plus1ms_interval_preserved':True,'all3_budget_ratios_checked':True,'new_or_reverse_only_and_missing_blocks_only_new_entry':True,'real_market_or_account_calculations':0})
print('PASS',cases,'synthetic strictBTC/fundingR/available-time/actualinterval/missing-field cases;0realmarket/accountcalculations')
