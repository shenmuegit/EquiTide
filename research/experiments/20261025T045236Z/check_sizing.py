"""Synthetic regression: reject a simulator that silently uses2000 for every spec."""
import ast,importlib.util,json,sys
from pathlib import Path
from collections import defaultdict
from decimal import Decimal as D
import numpy as np
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
path=R/'engine.py' if (R/'engine.py').exists() else ROOT/'research/experiments/20261024T164729Z/engine.py'
s=importlib.util.spec_from_file_location('sizing_engine_under_test',path);e=importlib.util.module_from_spec(s);s.loader.exec_module(e)
def synthetic(N):
 refs=np.asarray([i for i in range(e.START,e.END) for _ in [6,7]]+[e.END]);codes=np.asarray([k for i in range(e.START,e.END) for k in [6,7]]+[9]);n=len(codes)
 m={'asset':'BTC','ts':np.arange(n,dtype=np.int64),'controls':np.arange(n),'refs':refs,'codes':codes,'axis_prices':np.full(n,101.),'cost_inputs':{i:(D('100000000'),D('.02')) for i in range(e.START,e.END+1)},'closes':[D(100)]*365,'frame':{'open':defaultdict(lambda:D(101)),'available_ts':defaultdict(int)},'meta':{'lot_size':'.001','tick_size':'.01','min_notional':'5'}}
 old=e.summary;e.summary=lambda *args:{'synthetic_only':True}
 try:return e.simulate({'parameters':{'signal_mode':'constant_long_reference','fixed_entry_notional_usdt':N}},m,1)[1]
 finally:e.summary=old
for N,want in [(1000,D(10)),(2000,D(20)),(3000,D(30))]:
 scene=synthetic(N);opening=scene['trades'][0];assert D(opening['quantity'])==want,f'spec notional{N} ignored: expected priorclose-sized quantity{want}, got{opening["quantity"]}'
 assert opening['reference']=='101' and all(x['fixed_entry_notional_usdt']==N for x in scene['decisions']);assert len(scene['trades'])==2 and scene['terminal_state']['signed_units']=='0'
for invalid in [0,-1000,10001]:
 try:synthetic(invalid)
 except AssertionError:pass
 else:raise AssertionError('Invalid notional accepted')
source=ROOT/'research/experiments/20261024T164729Z/engine.py';a={x.name:ast.get_source_segment(source.read_text(),x) for x in ast.parse(source.read_text()).body if isinstance(x,ast.FunctionDef)};b={x.name:ast.get_source_segment(path.read_text(),x) for x in ast.parse(path.read_text()).body if isinstance(x,ast.FunctionDef)}
assert a.keys()==b.keys()
for name in a.keys()-{'simulate','load_market','summary'}:assert a[name]==b[name]
print(json.dumps({'passed':True,'synthetic_only_not_real_backtests':True,'notionals1000_2000_3000_actual_quantities10_20_30_at_priorclose100':True,'future_reference101_not_used_for_size':True,'invalid_notional_rejected':True,'existing_target_trade_funding_margin_stats_functions_byte_unchanged':True}))
