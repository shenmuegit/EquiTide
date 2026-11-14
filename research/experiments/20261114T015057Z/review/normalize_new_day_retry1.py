"""Append verified new raw rows while preserving every old normalized input row."""
import gzip,json,sys
from pathlib import Path
from decimal import Decimal as D
import polars as pl
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import sha,put,now,rel,core,HOUR,MIN,DAY
old=json.loads((ROOT/'research/experiments/20261113T234922Z/plan.json').read_text());ready=json.loads((R/'new_day_readiness.json').read_text());assert ready['passed'];dest=ROOT/'data/runs/automation'/R.name/'extended391';dest.mkdir(parents=True,exist_ok=False);assets={};quality={}
for a in ['BTC','ETH']:
 b=ready['bundles'][a];assert sha(ROOT/b['path'])==b['sha256'];packet=json.loads(gzip.decompress((ROOT/b['path']).read_bytes()));prior={Path(x['path']).stem:pl.read_parquet(ROOT/x['path']) for x in old['data']['assets'][a]};folder=dest/a;folder.mkdir()
 for x in old['data']['assets'][a]:assert sha(ROOT/x['path'])==x['sha256']
 def append_bars(rows,f,mark=False):
  last=int(f['open_ts'][-1]);extra=[{'open_ts':int(x[0])*1000000,**{k:D(x[j]) for k,j in [('open',1),('high',2),('low',3),('close',4)]},'base_volume':D(0) if mark else D(x[5]),'quote_volume':D(0) if mark else D(x[7]),'available_ts':(int(x[6])+1)*1000000,'is_closed':True} for x in rows if int(x[0])*1000000>last];return pl.concat([f,pl.DataFrame(extra,schema=f.schema)])
 minute=append_bars(packet['minutes']+packet['terminal_reference_minutes'],prior['perp_bars']);hour=append_bars(packet['closed_mark_hours'],prior['mark_hour_bars'],True);f=prior['funding_settlement'];last=int(f['settlement_ts'][-1]);extra=[]
 for z in packet['actual_funding_with_two_day_context']:
  t=int(z['fundingTime'])*1000000
  if t>last:extra.append({'settlement_ts':t,'available_ts':t+HOUR,'realized_rate':D(z['fundingRate']),'mark_price_at_settlement':D(z['markPrice']),'actual_interval_hours':D(t-last)/D(HOUR)});last=t
 funds=pl.concat([f,pl.DataFrame(extra,schema=f.schema)]);frames={'perp_bars':minute,'mark_hour_bars':hour,'funding_settlement':funds,'perp_instrument_meta':prior['perp_instrument_meta']};assert minute.height==610562 and hour.height==10176 and funds.height==1273 and len(extra)==3 and (minute['open_ts'].diff().drop_nulls()==MIN).all() and (hour['open_ts'].diff().drop_nulls()==HOUR).all() and all(frames[k].head(prior[k].height).equals(prior[k]) for k in frames)
 daily=minute.with_columns((pl.col('open_ts')//DAY).alias('d')).group_by('d').len().sort('d');assert daily['len'].to_list()==[1440]*424+[2];assets[a]=[]
 for key,f in frames.items():
  out=folder/(key+'.parquet');f.write_parquet(out,compression='zstd');assets[a].append({'path':rel(out),'sha256':sha(out),'bytes':out.stat().st_size,'rows':f.height})
 quality[a]={'all_old_rows_byte_values_equal':True,'minutes':minute.height,'hours':hour.height,'funding_events':funds.height,'new_minutes':1440,'new_hours':24,'new_actual_funding_events':len(extra),'complete_context_and_evaluation_days':424,'last_minute_open_utc':core.stamp(int(minute['open_ts'][-1])),'last_funding_time_utc':core.stamp(int(funds['settlement_ts'][-1]))}
put(R/'extended_data_manifest.json',{'passed':True,'recorded_utc':now(),'data':{'assets':assets,'provenance_manifest':rel(R/'new_day_readiness.json'),'provenance_manifest_sha256':sha(R/'new_day_readiness.json')},'old_data':old['data'],'quality':quality,'no_strategy_or_account_calculations':True});print(json.dumps(quality),flush=True)
