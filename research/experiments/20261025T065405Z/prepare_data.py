"""Merge existing actual normalized inputs, preserve annual prefix; no strategy evaluation."""
import hashlib,json
from pathlib import Path
from datetime import datetime,timezone
import polars as pl
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
old=json.loads((ROOT/'research/experiments/20261025T005204Z/plan.json').read_text())['data']['assets'];recent=json.loads((ROOT/'research/experiments/20261025T045236Z/plan.json').read_text())['data']['assets'];CUT=1789516800000000000
out={'recorded_at_utc':datetime.now(timezone.utc).isoformat(),'original_annual_inputs':old,'recent_inputs':recent,'precedence':'Annual data preserved verbatim before2026-09-16UTC00;recent actualdata appended only thereafter. Original reports/cold40daychecks unchanged.','normalized':{},'overlap_checks':{},'network_downloads':0,'financial_computation_performed':False}
for asset in ['BTC','ETH']:
 oldby={Path(x['path']).stem:x for x in old[asset]};newby={Path(x['path']).stem:x for x in recent[asset]};target=ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20250916T000000Z_20261025T000000Z_extended_20261025';target.mkdir(parents=True,exist_ok=True);out['normalized'][asset]=[];out['overlap_checks'][asset]={}
 for kind in ['perp_bars','mark_hour_bars','funding_settlement','perp_instrument_meta']:
  a,b=oldby[kind],newby[kind];assert sha(ROOT/a['path'])==a['sha256'] and sha(ROOT/b['path'])==b['sha256'];f=pl.read_parquet(ROOT/a['path']);g=pl.read_parquet(ROOT/b['path']);path=target/(kind+'.parquet')
  if kind=='perp_instrument_meta':assert (ROOT/a['path']).read_bytes()==(ROOT/b['path']).read_bytes();path.write_bytes((ROOT/a['path']).read_bytes())
  else:
   time='settlement_ts' if kind=='funding_settlement' else 'open_ts';prefix=g.filter(pl.col(time)<CUT);oldpart=f.filter(pl.col(time)>=prefix[time][0]);same=prefix.equals(oldpart);out['overlap_checks'][asset][kind]={'rows':prefix.height,'exactly_equal':same,'policy':'Annual original authoritative;no prior source rewrite.'}
   if kind!='funding_settlement':assert same
   tail=g.filter(pl.col(time)>=CUT).cast(f.schema).select(f.columns);combined=pl.concat([f,tail]).sort(time);assert combined[time].n_unique()==combined.height and combined.head(f.height).equals(f)
   expected={'perp_bars':404*1440,'mark_hour_bars':404*24,'funding_settlement':404*3}[kind];assert combined.height==expected
   if kind!='funding_settlement':assert (combined[time].diff().drop_nulls()==(60000000000 if kind=='perp_bars' else 3600000000000)).all()
   combined.write_parquet(path)
  out['normalized'][asset].append({'path':str(path.relative_to(ROOT)),'sha256':sha(path),'bytes':path.stat().st_size,'rows':pl.read_parquet(path).height})
put(R/'extended_data_manifest.json',out);print(json.dumps({'normalized':out['normalized'],'overlap_checks':out['overlap_checks'],'no_network_or_strategy_run':True}),flush=True)
