"""Independent M/R median, Decimal budget, retention and future invariance synthetic check."""
import copy,json,math,statistics,sys
from fractions import Fraction as F
from decimal import Decimal as D
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));import engine
p=json.loads((R/'plan.json').read_text());ref=p['read_only_references'][p['current_center']['native']];spec=json.loads((ROOT/ref['spec']).read_text());sn=33*engine.DAY
m={'asset':'ETH','closes':[D(100)+D(j%7)*D('.03') for j in range(33)],'frame':{'available_ts':{33*1440-1:sn}},'signal_funds':[{'settlement_ts':sn-age*engine.HOUR,'available_ts':sn-(age-1)*engine.HOUR,'realized_rate':D(rate),'entry_interval_hours':D('8.000000555555555555555555556'),'source_index':j} for j,(age,rate) in enumerate([(8,'-.0002'),(16,'.0001'),(24,'.0003'),(32,'.0007')])]}
if '--fixed-ratio-bug' in sys.argv:
 original=engine.carry_cap
 engine.carry_cap=lambda sigma,ratio,event:original(sigma,.00875,event)
checked=0
for M in [2,3,4]:
 for ratio in [.0075,.00875,.01]:
  sp=copy.deepcopy(spec);sp['parameters'].update(entry_funding_settlement_count=M,entry_funding_volatility_ratio=ratio)
  for rr in [F('-.020001'),F('-.02'),F('-.007501'),F('-.0075'),F(0),F('.0075'),F('.007501'),F('.02'),F('.020001')]:
   mm=copy.deepcopy(m);mm['closes'][27]=D(100);mm['closes'][32]=D(100)*(1+D(rr.numerator)/D(rr.denominator))
   for actual in [-1,0,1]:
    want,a=engine.decide(sp,mm,33,actual);r=F(mm['closes'][32])/F(mm['closes'][27])-1;assert F(a['return_exact'])==r==rr;h,e=F('.02'),F('.0075');base=-1 if rr>h else 1 if rr<-h else actual if actual==1 and rr<e or actual==-1 and rr>-e else 0;assert a['ungated_desired']==base
    beta=F(15,17);left=right=mass=F(0)
    for j in range(17,33):left=F(mm['closes'][j])+beta*left;mass=1+beta*mass
    for j in range(14,30):right=F(mm['closes'][j])+beta*right
    assert F(a['slow_mean_exact'])==left/mass and F(a['slow_reference_mean_exact'])==right/mass;slow=left/right-1;gate=(slow>F('.0075'))-(slow<F('-.0075'));raw=base if base==actual or base==gate else 0
    xs=[math.log(float(mm['closes'][j])/float(mm['closes'][j-1])) for j in range(27,33)];sigma=statistics.stdev(xs);assert math.isclose(a['observed_sample_logvol'],sigma,rel_tol=1e-12,abs_tol=1e-12);pre=0 if raw and raw!=actual and sigma>.05625 else raw
    fa=a['funding_filter'];selected=mm['signal_funds'][:M];rates=sorted(D(x['realized_rate']) for x in selected);median=rates[M//2] if M%2 else (rates[M//2-1]+rates[M//2])/2;bx=[math.log(float(mm['closes'][j])/float(mm['closes'][j-1])) for j in range(25,33)];budget=min(D('.0002'),D(str(ratio))*D(str(statistics.stdev(bx)))*selected[0]['entry_interval_hours']/24);out=max(D(pre)*median,D(0));expected=0 if pre and pre!=actual and out>budget else pre
    assert fa['settlement_count']==M and D(fa['median_realized_rate'])==median and D(fa['budget_ratio'])==D(str(ratio)) and fa['budget_volatility_window_days']==8 and D(fa['cap_fraction_per_settlement'])==budget and want==expected
    assert [z['source_index'] for z in fa['selected_settlements']]==list(range(M))
    future=copy.deepcopy(mm);future['closes']+=[D(1),D(99999)];future['signal_funds']+=[{**m['signal_funds'][0],'settlement_ts':sn+engine.HOUR,'available_ts':sn-engine.HOUR,'realized_rate':D('999')}];assert engine.decide(sp,future,33,actual)==(want,a);checked+=1
for ratio in [.0075,.00875,.01]:
 for sigma in [.0001,.1,1]:
  ev=engine.median_funding(m['signal_funds'],sn,3);assert engine.carry_cap(sigma,ratio,ev)==min(D('.0002'),D(str(sigma))*D(str(ratio))*ev['events'][0]['entry_interval_hours']/24)
print('PASS',checked,'jointM/R exactmedian/FractionROC/Horner/budget/actualinterval/retention/reversal/future;9ratiohardcap checks;unchangedengine,0marketvaluations')
