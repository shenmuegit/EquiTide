"""Adversarial timing check for28d-label maturity and exact settlement boundaries."""
import numpy as np
from long_carry import train_mask,events_between,make_folds,HOUR,MINUTE,DAY
end=100*DAY;t=np.array([end-672*HOUR-2*HOUR,end-672*HOUR,end-20*DAY]);ends=t+672*HOUR+MINUTE;av=ends+HOUR
assert train_mask(t,ends,av,0,end).tolist()==[True,False,False]
# An already-realized label still must be purged when publication reaches cutoff.
assert not train_mask(np.array([0]),np.array([1]),np.array([end]),0,end)[0]
# New position cannot receive a settlement at or just before its entry.
events=[{'ts':100},{'ts':101},{'ts':200},{'ts':201}]
assert [e['ts'] for e in events_between(events,100,200)]==[101,200]
f=make_folds();assert len(f)==4
for x in f:assert x['test_start_signal_ns']-x['train_end_exclusive_ns']==56*DAY
assert f[-1]['test_end_signal_ns']-f[0]['test_start_signal_ns']==112*DAY
print('PASS:28d mature-label+publication purge, funding(entry,exit] and56dayembargo4folds')
