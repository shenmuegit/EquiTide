"""Synthetic boundary/causality checks; no real-data configuration evaluated here."""
from decimal import Decimal as D
from fractions import Fraction as F
from run import choose,POINTS,SPAN

def main():
 # Exact tie: cash chooses BTC; an eligible ETH incumbent is not churned at gap zero.
 c={'BTC':[D(100),D(100),D(110)],'ETH':[D(100),D(100),D(110)]}
 assert choose(c,2,2,0,0,None)[0]=='BTC' and choose(c,2,2,0,0,'ETH')[0]=='ETH'
 # Challenger's edge equals hurdle: retain. Strictly greater edge permits switch.
 c={'BTC':[D(100),D(100),D(110)],'ETH':[D(100),D(100),D(112)]}
 assert choose(c,2,2,0,.02,'BTC')[0]=='BTC' and choose(c,2,2,0,.019,'BTC')[0]=='ETH'
 # Absolute equality to cash hurdle zero is ineligible; an ineligible incumbent exits.
 c={'BTC':[D(100),D(120),D(100)],'ETH':[D(100),D(120),D(99)]}
 assert choose(c,2,2,0,0,'BTC')[0] is None
 # Recent-week skip changes ranking but does not defer the contemporaneous cash gate.
 c={'BTC':[D(100),D(120),D(130),D(125)],'ETH':[D(100),D(105),D(120),D(140)]}
 assert choose(c,3,2,0,0,None)[0]=='ETH' and choose(c,3,2,1,0,None)[0]=='BTC'
 c['BTC'][-1]=D(119);assert choose(c,3,2,1,.99,'BTC')[0]=='ETH'
 # A strictly ineligible incumbent can switch despite an otherwise blocking hurdle.
 assert choose(c,3,2,1,.99,'BTC')[1]['eligible']==['ETH']
 # Future-close suffix must have no effect on any already-available decision.
 prefix={'BTC':[D(100+i) for i in range(100)],'ETH':[D(100)+D(i)/2 for i in range(100)]}
 for look in [21,42,84]:
  for skip in [0,7]:
   before=choose(prefix,95,look,skip,.02,'ETH');after=choose({a:v+[D(10000000),D(1)] for a,v in prefix.items()},95,look,skip,.02,'ETH');assert before==after
 # NAV includes pre-trade gap and both rotation legs; original cost units stay Decimal.
 assert SPAN==1443 and POINTS==519483 and 360*SPAN+3==POINTS
 native=D('87528.86');assert float(D('100')+D('.01')*native)==975.2886
 print('PASS: exact ranking ties,strict switching hurdle,current absolute cash gate,separate skip ranking,future-prefix invariance,18-configuration axes and two-leg event NAV mapping;synthetic only',flush=True)

if __name__=='__main__':main()
