"""Independent raw OHLC completeness/containment proof; no strategy evaluation."""
import json,sys
from pathlib import Path
import polars as pl
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
p=json.loads((R/'plan.json').read_text());rows=[]
for asset in ['BTC','ETH']:
 source=next(x for x in p['data']['assets'][asset] if x['path'].endswith('/perp_bars.parquet'));assert sha(ROOT/source['path'])==source['sha256'];df=pl.read_parquet(ROOT/source['path']);stats=df.select(pl.len().alias('rows'),*[pl.col(k).null_count().alias(k+'_nulls') for k in ['open','high','low','close','available_ts']],(pl.col('high')>=pl.max_horizontal('open','close','low')).all().alias('high_contains_all'),(pl.col('low')<=pl.min_horizontal('open','close','high')).all().alias('low_contains_all'),(pl.col('low')>0).all().alias('positive_low'),pl.col('is_closed').all().alias('all_closed'),((pl.col('available_ts')-pl.col('open_ts'))==MIN).all().alias('minute_availability_exact')).to_dicts()[0];days=df.with_columns((pl.col('open_ts')//DAY).alias('day')).group_by('day').agg(pl.len().alias('bars'));assert stats['rows']==581760 and all(v==0 for k,v in stats.items() if k.endswith('_nulls')) and all(stats[k] for k in ['high_contains_all','low_contains_all','positive_low','all_closed','minute_availability_exact']) and days.height==404 and (days['bars']==1440).all();rows.append({'asset':asset,'source':source,'stats':stats,'UTC_days':404,'bars_each_day':1440})
put(R/'HLC_input_quality.json',{'passed':True,'recorded_utc':now(),'assets':rows,'raw_input_quality_only':True,'new_strategy_or_account_evaluations':0});print('PASS actual raw minute OHLC no nulls,all closes/opens within full range,404UTCdays x1440 closed/available bars perasset')
