"""Small synthetic accounting checks; these are not strategy backtest results."""
from carry import Ledger, FundingBook, b1_actions

l=Ledger(10000)
l.trade(1,100,101,0,0)
assert l.spot_cash == 4900 and l.perp_cash == 5000
assert l.nav(100,101) == 10000
book=FundingBook([{'ts':10,'available':20,'rate':.01,'mark':101,'hours':8}])
assert book.hourly_rate(19,1) is None
assert book.hourly_rate(20,1) == .00125
assert book.settle(0,10,l,3) == 1
assert abs(l.perp_cash-5001.01) < 1e-8
negative=FundingBook([{'ts':30,'available':40,'rate':-.01,'mark':100,'hours':8}])
assert negative.settle(0,29,l,3) == 0
assert negative.settle(0,30,l,3) == 1
assert abs(l.perp_cash-4998.01) < 1e-8
l.trade(-1,100,101,0,0)
assert abs(l.nav(100,101)-9998.01) < 1e-8
assert negative.settle(0,30,l,3) == 1 and abs(l.perp_cash-4998.01)<1e-8
loss=Ledger(10000);loss.trade(1,100.1,100.9,.001,.0005);loss.trade(-1,99.9,101.1,.001,.0005)
assert abs(loss.nav(100,101)-9999.299) < 1e-8
assert b1_actions(.001,1000,8,1,.002,.001,False)=='enter'
assert b1_actions(.0001,1000,8,1,.002,.001,False)=='skip'
assert b1_actions(.001,1000,2,1,.0002,.0001,True)=='hold'
assert b1_actions(.001,1000,2,1,.0002,.0001,True)!='exit'  # only future EXIT costs, no sunk entry costs
assert b1_actions(.001,1000,1,1,.0002,.0001,True)=='exit'
print('PASS: separate ledgers, actual funding cutoff/sign/stress, information delay, flat-price roundtrip costs and unsunk exit gate')
