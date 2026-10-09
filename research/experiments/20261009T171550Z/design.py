"""Predeclared ETH quote-turnover entry confirmation; definitions only,no backtest."""
from copy import deepcopy
VOLUME_LOGIC={
 'entry':'At daily decision i,use only completed prior close C[i-1]. It must strictly exceed max(C[i-16:i-1]) AND completed prior quote volume Q[i-1]>=minimum_volume_ratio*mean(Q[i-volume_lookback_days-1:i-1]),with positive reference mean,to set desired-long. Both reference ranges end i-2 and exclude the tested close/volume i-1. Quote volume is USDT turnover,not base units.',
 'exit':'Prior close C[i-1] strictly below min(C[i-31:i-1]) sets desired-cash regardless of quote-volume eligibility. Exit takes precedence;otherwise eligible joint entry sets long;all other cases and price equality preserve desired. Low volume alone never forces liquidation. Volume equality at threshold qualifies. No delayed arming,extra confirmation,EMA,SMA,ATR,stop or shorting.',
 'state':'Start OOS183 with cash and desired-cash. Historical closes/quote volumes only warm windows;no warmup fills/state replay. Carry cash,units,desired across six folds. Zero reference quote mean disables entry;no division by zero.',
 'sizing':'At next UTC00:01 real minute open,buy maximum affordable LOT_SIZE quantity and keep residue;exit all valid units on desired cash/terminal. Existing Decimal28 PRICE/LOT/NOTIONAL/5minuteVWAP/participation execution with same500USDT funds. No leverage,borrow,transfers,rebalancing or cash yield.'}
AXES={'volume_lookback_days':[10,20,30],'minimum_volume_ratio':[.75,1.,1.25]}
def source_spec(old,n,ratio):
 sp=deepcopy(old);sp['family']='daily-close-range-relative-quote-volume';sp['logic']=deepcopy(VOLUME_LOGIC)
 sp['parameters'].update(volume_lookback_days=n,minimum_volume_ratio=ratio,volume_definition='Prior fully completed UTC day USDT quote turnover divided by Decimal28 arithmetic mean of precedingN completed quote volumes excluding tested day. >=threshold eligible;reference mean>0;entry filter only,exit unfiltered.',signal_initialization='Cash/desired-cash at OOS183;only prior completed bars;carry across all folds;no warmup trades.')
 return sp
