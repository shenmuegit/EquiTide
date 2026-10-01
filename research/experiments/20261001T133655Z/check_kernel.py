"""Adversarial executable-contract checks; synthetic fixtures are not backtests."""
from decimal import Decimal as D
from kernel import fill, floor_step, adverse_tick

f={'PRICE_FILTER':{'minPrice':'0.01','maxPrice':'1000000','tickSize':'0.01'},'LOT_SIZE':{'minQty':'0.001','maxQty':'9000','stepSize':'0.001'},'NOTIONAL':{'minNotional':'5','maxNotional':'9000000'}}
assert floor_step(D('0.002999'),D('0.001'))==D('0.002')
assert adverse_tick(D('100.001'),D('.01'),True)==D('100.01')
assert adverse_tick(D('100.009'),D('.01'),False)==D('100.00')
c,u,t=fill(D('10'),D(0),True,D('100'),D('100000000'),D('.02'),1,f,D('100'))
assert 0<=c<D('0.11') and u%D('.001')==0 and t['status']=='filled'
assert abs(c+u*D('100')+D(t['cost_usdt'])-D('10'))<D('1e-20')
c2,u2,t2=fill(c,u,False,D('100'),D('100000000'),D('.02'),3,f,D('100'))
assert u2==0 and c2>=0 and t2['status']=='filled'
c,u,t=fill(D('4'),D(0),True,D('100'),D('100000000'),D('.02'),1,f,D('100'))
assert t['status']=='rejected' and t['reason']=='notional' and c==4 and u==0
c,u,t=fill(D('1000000'),D(0),True,D('100'),D('100'),D('.02'),1,f,D('100'))
assert t['status']=='rejected' and t['reason']=='participation'
f['PERCENT_PRICE_BY_SIDE']={'bidMultiplierUp':'1.2','bidMultiplierDown':'.5','askMultiplierUp':'2','askMultiplierDown':'.8'}
c,u,t=fill(D('100'),D(0),True,D('200'),D('100000000'),D('.02'),1,f,D('100'))
assert t['reason']=='percent_price_proxy' and c==100 and u==0
print('PASS:lot flooring, adverse tick rounding, exact cash conservation, failed-order state, capacity and VWAP proxy bounds')
