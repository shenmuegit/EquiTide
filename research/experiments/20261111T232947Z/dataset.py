"""Build a real closed-data later-period cohort from original official response archives.
No strategy target, trade, account transition or PnL evaluation occurs here.
"""
import gzip,hashlib,json,sys,urllib.parse
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal as D
import polars as pl
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));rel=lambda p:str(p.relative_to(ROOT));now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z');ns=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp())*10**9;put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
MIN=60*10**9;HOUR=60*MIN;DAY=24*HOUR;FIRST=ns('2026-09-21T00:00:00Z');START=ns('2026-10-24T00:01:00Z');END=ns('2026-11-11T00:01:00Z');INPUT_END=END+MIN;SWITCH=ns('2026-10-25T00:00:00Z');OUT=ROOT/'data/runs/automation'/R.name/'later_period_normalized';assert not (R/'cohort_inputs.json').exists();OUT.mkdir(parents=True,exist_ok=True)
minutes={a:{} for a in ['BTC','ETH']};hours={a:{} for a in ['BTC','ETH']};funds={a:{} for a in ['BTC','ETH']};meta={};sources=[];packet_sources=[];public_seen={};conflicts=[];overlap_equal=0
for a in ['BTC','ETH']:
 base=ROOT/f'data/normalized/binance/{a}/binance_{a}_20250916T000000Z_20261025T000000Z_extended_20261025';files={n:base/(n+'.parquet') for n in ['perp_bars','mark_hour_bars','funding_settlement','perp_instrument_meta']};frames={n:pl.read_parquet(f) for n,f in files.items()};meta[a]=frames['perp_instrument_meta'];sources.extend({'path':rel(f),'sha256':sha(f),'bytes':f.stat().st_size,'role':'original official normalized cache, only pre-Oct25 selection used'} for f in files.values())
 for label,target,step in [('perp_bars',minutes,MIN),('mark_hour_bars',hours,HOUR)]:
  for row in frames[label].filter((pl.col('open_ts')>=FIRST)&(pl.col('open_ts')<SWITCH)).to_dicts():assert row['available_ts']==row['open_ts']+step and row['is_closed'];target[a][row['open_ts']]=row
 for row in frames['funding_settlement'].filter((pl.col('settlement_ts')>=FIRST)&(pl.col('settlement_ts')<SWITCH)).to_dicts():funds[a][row['settlement_ts']]=row
point=rd(ROOT/'research/automation/candidate_forward_latest.json');seen=set();packets=[]
while point:
 assert point['delta'] not in seen;seen.add(point['delta']);folder=(ROOT/point['state']).parent;impath=folder/'input_manifest.json';im=rd(impath);packet=ROOT/im['packet'];assert sha(packet)==im['sha256'];d=gz(packet);assert d['plan_sha256']==point['plan_sha256'];packets.append((impath,im,packet,d));prev=point.get('previous_pointer');point=rd(ROOT/prev['path']) if prev else None
# Oldest retrieval first; repeated exact data stays exact, no averaging or filling.
packets.sort(key=lambda z:z[3]['retrieved_ns'])
for impath,im,packet,d in packets:
 used=False;rawmap={a:{'minutes':{},'hours':{},'funding':{}} for a in ['BTC','ETH']}
 for rec in im['provenance']:
  path=ROOT/rec['raw']
  if rec['raw'] not in public_seen:assert sha(path)==rec['sha256'];public_seen[rec['raw']]={**rec,'sha256_verified':True}
  if rec.get('http_status',200)!=200 or rec.get('curl_exit_code',0):continue
  u=urllib.parse.urlparse(rec['url']);q=urllib.parse.parse_qs(u.query);symbol=q.get('symbol',[''])[0];a=symbol.removesuffix('USDT')
  if a not in rawmap:continue
  kind='hours' if u.path.endswith('/markPriceKlines') else 'minutes' if u.path.endswith('/klines') else 'funding' if u.path.endswith('/fundingRate') else None
  if kind is None:continue
  payload=gz(path);assert isinstance(payload,list)
  for row in payload:
   key=int(row['fundingTime']) if kind=='funding' else int(row[0]);rawmap[a][kind][key]=row
 for a,x in d['assets'].items():
  assert a in minutes
  for kind,target,step in [('minutes',minutes,MIN),('hours',hours,HOUR)]:
   for z in x[kind]:
    t=int(z[0])*1000000;av=(int(z[6])+1)*1000000
    if not SWITCH<=t<INPUT_END or av>INPUT_END:continue
    assert z==rawmap[a][kind][int(z[0])] and av==t+step and d['retrieved_ns']>=av
    row={'open_ts':t,'open':D(z[1]),'high':D(z[2]),'low':D(z[3]),'close':D(z[4]),'base_volume':D(z[5]),'quote_volume':D(z[7]),'available_ts':av,'is_closed':True};old=target[a].get(t)
    if old is not None:
     if old!=row:conflicts.append({'asset':a,'kind':kind,'time_ns':t,'earlier':{k:str(v) for k,v in old.items()},'later':{k:str(v) for k,v in row.items()},'packet':rel(packet)})
     else:overlap_equal+=1
    else:target[a][t]=row
    used=True
  for z in x['funding']:
   t=int(z['fundingTime'])*1000000
   if not SWITCH<=t<=END:continue
   assert z==rawmap[a]['funding'][int(z['fundingTime'])] and d['retrieved_ns']>=t
   row={'settlement_ts':t,'available_ts':t+HOUR,'realized_rate':D(z['fundingRate']),'mark_price_at_settlement':D(z['markPrice'])};old=funds[a].get(t)
   if old is not None:
    if any(old[k]!=v for k,v in row.items()):conflicts.append({'asset':a,'kind':'funding','time_ns':t,'packet':rel(packet)})
    else:overlap_equal+=1
   else:funds[a][t]=row
   used=True
 if used:packet_sources.append({'input_manifest':rel(impath),'input_manifest_sha256':sha(impath),'packet':rel(packet),'packet_sha256':sha(packet),'original_retrieved_ns':d['retrieved_ns'],'original_provenance':im['provenance']})
gap=rd(R/'mark_hour_gap_source.json');assert gap['passed']
for rec in gap['receipts']:
 if rec['curl_exit_code'] or rec['http_status']!=200:continue
 path=ROOT/rec['raw'];assert sha(path)==rec['sha256'];a=rec['asset']
 for z in gz(path):
  t=int(z[0])*1000000;av=(int(z[6])+1)*1000000;assert t in gap['missing_hour_ns'] and t not in hours[a] and av==t+HOUR
  hours[a][t]={'open_ts':t,'open':D(z[1]),'high':D(z[2]),'low':D(z[3]),'close':D(z[4]),'base_volume':D(z[5]),'quote_volume':D(z[7]),'available_ts':av,'is_closed':True}
official=rd(R/'cohort_funding_source.json');assert official['passed'];official_ts={a:set() for a in ['BTC','ETH']};fund_gap_counts={a:0 for a in ['BTC','ETH']}
for rec in official['receipts']:
 if rec['curl_exit_code'] or rec['http_status']!=200:continue
 path=ROOT/rec['raw'];assert sha(path)==rec['sha256'];a=rec['asset']
 for z in gz(path):
  t=int(z['fundingTime'])*1000000;row={'settlement_ts':t,'available_ts':t+HOUR,'realized_rate':D(z['fundingRate']),'mark_price_at_settlement':D(z['markPrice'])};official_ts[a].add(t);old=funds[a].get(t)
  if old is not None:assert all(old[k]==v for k,v in row.items()),'Authoritative official funding differs from original archived value'
  else:fund_gap_counts[a]+=1;funds[a][t]=row
 assert official_ts[a]=={t for t in funds[a] if START<t<=END}
put(R/'official_funding_coverage.json',{'passed':True,'actual_counts':official['actual_settlement_counts'],'new_real_rows_missing_from_prior_candidate_archives':fund_gap_counts,'financial_calculations':0})
put(R/'data_overlap_conflicts.json',{'conflicts':conflicts,'identical_duplicate_rows':overlap_equal,'strategy_or_account_calculations':0});assert not conflicts,'Real response revisions/conflicts need resolution before any financial calculation'
assets={};counts={};dec=pl.Decimal(38,18);bar_schema={'open_ts':pl.Int64,**{k:dec for k in ['open','high','low','close','base_volume','quote_volume']},'available_ts':pl.Int64,'is_closed':pl.Boolean};fund_schema={'settlement_ts':pl.Int64,'available_ts':pl.Int64,'realized_rate':dec,'mark_price_at_settlement':dec,'actual_interval_hours':dec}
for a in ['BTC','ETH']:
 ms=sorted(minutes[a]);hs=sorted(hours[a]);expected_m=list(range(FIRST,INPUT_END,MIN));expected_h=list(range(FIRST,END//HOUR*HOUR,HOUR));missing_m=sorted(set(expected_m)-set(ms));missing_h=sorted(set(expected_h)-set(hs));put(R/(a+'_coverage.json'),{'expected_minutes':len(expected_m),'actual_minutes':len(ms),'missing_minutes':missing_m,'expected_closed_hours':len(expected_h),'actual_hours':len(hs),'missing_hours':missing_h,'financial_calculations':0});assert ms==expected_m and hs==expected_h,(a,'real data unavailable; no gap filling',len(missing_m),len(missing_h))
 rows=[]
 for j,t in enumerate(sorted(funds[a])):
  row={**funds[a][t]};row['actual_interval_hours']=D(t-sorted(funds[a])[j-1])/D(HOUR) if j else row['actual_interval_hours'];assert row['realized_rate'].is_finite() and row['mark_price_at_settlement']>0 and row['actual_interval_hours']>0;rows.append(row)
 assert len([x for x in rows if START<x['settlement_ts']<=END])==official['actual_settlement_counts'][a]
 dest=OUT/a;dest.mkdir(exist_ok=True);frames={'perp_bars':pl.DataFrame([minutes[a][t] for t in ms],schema=bar_schema),'mark_hour_bars':pl.DataFrame([hours[a][t] for t in hs],schema=bar_schema),'funding_settlement':pl.DataFrame(rows,schema=fund_schema),'perp_instrument_meta':meta[a]};assets[a]=[]
 for name,frame in frames.items():
  path=dest/(name+'.parquet');frame.write_parquet(path);assets[a].append({'path':rel(path),'sha256':sha(path),'bytes':path.stat().st_size})
 counts[a]={'minutes':len(ms),'closed_mark_hours':len(hs),'all_funding_rows':len(rows),'OOS_funding_rows':official['actual_settlement_counts'][a],'full_past_and_OOS_days':51,'terminal_day_closed_reference_minutes':2}
put(R/'cohort_inputs.json',{'recorded_utc':now(),'assets':assets,'bounds':{'input_start_utc':'2026-09-21T00:00:00Z','OOS_start_utc':'2026-10-24T00:01:00Z','OOS_end_utc':'2026-11-11T00:01:00Z','input_end_exclusive_utc':'2026-11-11T00:02:00Z','warmup_days':33,'continuous_OOS_days':18,'walk_forward_folds':6,'fold_days':3},'counts':counts,'source_policy':'Real oldnormalized cache untilOct25 and original official archived candidate HTTP responses fromOct25 onward. No generated/fill/interpolated market rows. Captured later means retrospective shadow validation, not untouched final test; other original accounts already observed this period. Source1h funding availability remains a conservative modeling assumption. Current4 accounts untouched.','original_normalized_sources':sources,'original_packet_sources':packet_sources,'all_HTTP_source_receipts_verified':list(public_seen.values()),'original_capture_UTC_or_ns_preserved':True,'overlap_identical_rows':overlap_equal,'original_perp_metadata_frozen':True,'new_public_GETs':gap['new_public_GETs']+official['new_public_GETs'],'new_official_cohort_funding_source':official,'new_mark_hour_gap_source':gap,'financial_or_account_calculations':0});print(json.dumps({'built_real_data':True,'assets':counts,'packets_read':len(packets),'packets_used':len(packet_sources),'HTTP_gzip_sources_verified':len(public_seen),'new_GETs':gap['new_public_GETs']+official['new_public_GETs'],'strategy_account_calculations':0}),flush=True)
