"""Append verified actual public bars/funding to immutable old inputs, no strategy calculation."""
import gzip,json,sys,shutil
from pathlib import Path
from decimal import Decimal as D
import polars as pl
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
P=ROOT/'research/experiments/20261112T213530Z';p=json.loads((P/'plan.json').read_text());ready=json.loads((P/'recent_data_readiness.json').read_text());assert ready['passed'] and json.loads((P/'recent_data_verification.json').read_text())['passed']
for x in ready['inputs']:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
out=ROOT/'data/runs/automation'/R.name/'extended389';out.mkdir(parents=True,exist_ok=False);assets={};quality={}
for asset in ['BTC','ETH']:
 packet=json.loads(gzip.decompress(next(ROOT/x['path'] for x in ready['inputs'] if x['path'].endswith(asset+'_public_bundle.json.gz')).read_bytes()));folder=out/asset;folder.mkdir();old={Path(x['path']).stem:pl.read_parquet(ROOT/x['path']) for x in p['data']['assets'][asset]}
 for x in p['data']['assets'][asset]:assert sha(ROOT/x['path'])==x['sha256']
 def bars(rows,frame,mark=False):
  last=int(frame['open_ts'][-1]);r=[{'open_ts':int(x[0])*1000000,**{k:D(x[j]) for k,j in [('open',1),('high',2),('low',3),('close',4)]},'base_volume':D(0) if mark else D(x[5]),'quote_volume':D(0) if mark else D(x[7]),'available_ts':(int(x[6])+1)*1000000,'is_closed':True} for x in rows if int(x[0])*1000000>last];return pl.concat([frame,pl.DataFrame(r,schema=frame.schema)])
 minute=bars(packet['minutes']+packet['terminal_reference_minutes'],old['perp_bars']);hour=bars(packet['closed_mark_hours'],old['mark_hour_bars'],True);fund=old['funding_settlement'];last=int(fund['settlement_ts'][-1]);extra=[]
 for x in packet['actual_funding_with_two_day_context']:
  t=int(x['fundingTime'])*1000000
  if t<=last:continue
  extra.append({'settlement_ts':t,'available_ts':t+HOUR,'realized_rate':D(x['fundingRate']),'mark_price_at_settlement':D(x['markPrice']),'actual_interval_hours':D(t-last)/D(HOUR)});last=t
 funds=pl.concat([fund,pl.DataFrame(extra,schema=fund.schema)]);frames={'perp_bars':minute,'mark_hour_bars':hour,'funding_settlement':funds,'perp_instrument_meta':old['perp_instrument_meta']}
 assert minute.height==607682 and hour.height==10128 and funds.height==1267 and (minute['open_ts'].diff().drop_nulls()==MIN).all() and (hour['open_ts'].diff().drop_nulls()==HOUR).all();assert all(frames[k].head(old[k].height).equals(old[k]) for k in frames)
 daily=minute.with_columns((pl.col('open_ts')//DAY).alias('day')).group_by('day').agg(pl.len().alias('n')).sort('day');assert daily.height==423 and daily['n'][:-1].to_list()==[1440]*422 and daily['n'][-1]==2
 assets[asset]=[]
 for key,f in frames.items():
  path=folder/(key+'.parquet');f.write_parquet(path,compression='zstd');assets[asset].append({'path':rel(path),'sha256':sha(path),'bytes':path.stat().st_size,'rows':f.height})
 quality[asset]={'all_old_rows_unchanged':True,'minute_rows':minute.height,'hour_rows':hour.height,'funding_rows':funds.height,'new_minutes':minute.height-old['perp_bars'].height,'new_hours':hour.height-old['mark_hour_bars'].height,'new_actual_settlements':len(extra),'complete_days':422,'terminal_reference_minutes':2,'last_minute_open_utc':core.stamp(int(minute['open_ts'][-1])),'last_actual_funding_utc':core.stamp(int(funds['settlement_ts'][-1]))}
put(R/'extended_data_manifest.json',{'passed':True,'recorded_utc':now(),'data':{'assets':assets,'provenance_manifest':rel(P/'recent_data_readiness.json'),'provenance_manifest_sha256':sha(P/'recent_data_readiness.json')},'quality':quality,'old_data':p['data'],'raw_public_preparation_manifest':rel(P/'recent_data_readiness.json'),'new_financial_calculations':0,'funding_arrival_policy':'Retain conservative source fundingTime+1hour assumption, not historical arrival evidence; latest actual intervals derived from consecutive source timestamps.'});print(json.dumps(quality),flush=True)
