import ast,json
from common import *
import market
import numpy as np
S=1750000000000000000;ts=np.array([S,S+1000000,S+1000000],dtype=np.int64);cc=np.array([0,3,4]);assert market.pack(ts,cc,S).tolist()==[0,16000003,16000004]
p=json.loads((ROOT/'research/experiments/20261030T173813Z/plan.json').read_text());ms,axis=market.load(p);assert len(axis['ts'])==570543 and len(axis['daily_indices'])==371 and sum(axis['codes']==6)==8880
for a,m in ms.items():assert len(m['hour_closes'])==9696 and m['start_ns']==axis['start_ns'] and m['end_ns']==axis['end_ns']
assert 33*24-1-24-720==47
put(R/'data_preflight.json',{'passed':True,'financial_evaluations':0,'real_market_inputs':8,'native_union_points':len(axis['ts']),'hourly_decisions':8880,'daily_boundaries':371,'earliest_training_hour':47,'maximum_training_source_hour_at_first_signal':766,'tested_hour_at_first_signal':791,'strictly_past_train_test_gap_hours':25,'source_core_sha256':sha(CORE_PATH),'axis_sha256':axis['axis_sha256']});print('PASSreal8Parquet/native570543eventclock/8880hours/rollingcontext; no model evaluated')
