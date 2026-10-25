"""Read-only extended input hash/prefix/coverage check; no financial simulation."""
import hashlib,json
from pathlib import Path
import polars as pl
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 d=json.loads((R/'extended_data_manifest.json').read_text());assert d['network_downloads']==0 and d['financial_computation_performed'] is False
 for fs in [*d['original_annual_inputs'].values(),*d['recent_inputs'].values()]:
  for x in fs:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 for a,fs in d['normalized'].items():
  old={Path(x['path']).stem:x for x in d['original_annual_inputs'][a]}
  for x in fs:
   p=ROOT/x['path'];assert sha(p)==x['sha256'] and p.stat().st_size==x['bytes'];f=pl.read_parquet(p);assert f.height==x['rows'];k=p.stem;g=pl.read_parquet(ROOT/old[k]['path'])
   if k=='perp_instrument_meta':assert f.equals(g);continue
   t='settlement_ts' if k=='funding_settlement' else 'open_ts';assert f[t].n_unique()==f.height and f.head(g.height).equals(g)
   if k=='funding_settlement':assert f.height==1212 and (f['available_ts']>=f['settlement_ts']).all() and (f['mark_price_at_settlement']>0).all()
   else:
    step=60000000000 if k=='perp_bars' else 3600000000000;assert f.height==(581760 if k=='perp_bars' else 9696) and f['is_closed'].all() and (f[t].diff().drop_nulls()==step).all() and (f['available_ts']-f[t]==step).all();assert (f['low']>0).all() and (f['low']<=f['open']).all() and (f['open']<=f['high']).all() and (f['low']<=f['close']).all() and (f['close']<=f['high']).all()
 print(json.dumps({'passed':True,'extended_files':8,'source_annual_and_recent_files':16,'original_annual_dataframe_prefix_exact':True,'actual404day_continuous_inputs':True,'no_network_or_strategy_rerun':True}),flush=True)
if __name__=='__main__':main()
