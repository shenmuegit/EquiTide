"""Date adapter only; existing causal signals and Decimal execution are unchanged."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
import numpy as np
import polars as pl

ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
def prepare_data():
    s=importlib.util.spec_from_file_location('archive_daily',ROOT/'checks/obv_trend_oos.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    source=json.loads((ROUND/'download_manifest.json').read_text());data={};frames={};manifest={}
    assert len(source['archives'])==26 and not source['errors']
    for asset,p in source['normalized'].items():
        path=ROOT/p['path'];h=hashlib.sha256(path.read_bytes()).hexdigest();assert h==p['sha256']
        rows,digest=m.daily_data(path);assert digest==h
        frame=pl.read_parquet(path);assert frame.height==525600 and frame['is_closed'].all()
        assert (frame['available_ts']-frame['open_ts']==60000000000).all()
        volumes=frame.group_by((pl.col('open_ts')//86400000000000).alias('day')).agg(pl.col('quote_volume').sum()).sort('day')['quote_volume']
        for i,(r,qv) in enumerate(zip(rows,volumes)):
            r['quote_volume']=qv;idx=i*1440+1;hist=frame.slice(idx-5,5)
            if i:
                assert hist['available_ts'].max()<=r['trade_ts'];r['proxy_vwap5']=str(hist['quote_volume'].sum()/hist['base_volume'].sum())
            else:r['proxy_vwap5']='0'
        assert rows[0]['date']=='2024-09-16' and rows[-1]['date']=='2025-09-15' and rows[183]['date']=='2025-03-18' and rows[363]['date']=='2025-09-14'
        data[asset]=rows;frames[asset]={'close':np.asarray(frame['close'].cast(pl.Float64)),'open':np.asarray(frame['open'].cast(pl.Float64))}
        manifest[asset]={'path':p['path'],'sha256':h,'minutes':525600,'first_open_ns':frame['open_ts'][0],'last_available_ns':frame['available_ts'][-1]}
    return data,frames,manifest
