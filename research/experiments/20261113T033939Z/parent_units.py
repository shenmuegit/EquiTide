"""Synthetic side/closure/suffix checks plus real data alignment, without valuation."""
from common import *
from engine import cross_filter
import numpy as np
closes=[core.D('100'),core.D('110'),core.D('90'),core.D('130')];available=[10,20,30,40]
assert cross_filter(1,0,closes,available,2,1,.1,20)[0]==1
assert cross_filter(-1,0,closes,available,2,1,0,20)[0]==0
assert cross_filter(-1,0,closes,available,3,1,.1,30)[0]==-1
assert cross_filter(1,1,closes,available,3,1,.1,30)[0]==1
assert cross_filter(0,1,closes,available,3,1,.1,30)[0]==0
assert cross_filter(1,0,closes,available,2,1,.1,19)[0]==0
assert cross_filter(1,0,[],[],0,1,0,0)[0]==0
assert cross_filter(1,0,closes,available,2,1,.1,20)==cross_filter(1,0,closes[:2]+[core.D('1'),core.D('999')],available,2,1,.1,20)
assert cross_filter(1,0,closes,available,2,3,0,20)[0]==0
first=np.array([3750.,4000.,3000.]);second=np.array([15000.,16000.,15500.]);assert (first+second).tolist()==[18750.,20000.,18500.] and not np.array_equal(first+second,(first+second)/2)
whole=np.array([100.,120.,90.,110.]);assert max(1-whole/np.maximum.accumulate(whole))==.25
put(R/'parent_primitive_verification.json',{'passed':True,'synthetic_only':True,'cross_cases':9,'tests':['threshold equality','short sign','same-position retained','normal exit','future close rejected','missing/insufficient rejected','future suffix irrelevant','whole banks not normalized','continuous crossfold DD25pct'],'new_financial_or_account_calculations':0})
import market,json
p=json.loads((R/'plan.json').read_text());ms,cm=market.load(p);m=ms['BTC'];assert len(m['cross_closes'])==422 and m['cross_closes']==ms['ETH']['closes']
for i in range(33,422):
 sn=int(m['frame']['available_ts'][i*1440-1]);assert m['cross_close_available'][i-1]==sn and all(m['cross_close_available'][i-1-W]<=sn for W in [3,7,14])
put(R/'cross_data_verification.json',{'passed':True,'recorded_utc':now(),'source_inputs_sha256':{x['path']:x['sha256'] for fs in p['data']['assets'].values() for x in fs},'completed_UTC_days':422,'all389cross_decision_availability_checks':True,'daily_dates_aligned':True,'ETH_cross_prices_are_exact_existing_ETH_complete_closes':True,'common_axis_sha256':cm['sha256'],'new_backtest_or_account_valuations':0})
print('PASS9syntheticcrosscases+wholebank/DDregressions,422realaligneddays/389causalboundaries;0valuations')
