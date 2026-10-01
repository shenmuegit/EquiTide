"""Detect false numeric conflicts without accepting changed rates/instruments/times."""
import importlib.util
from pathlib import Path
s=importlib.util.spec_from_file_location('okx_download',Path(__file__).with_name('download_okx_carry.py'))
m=importlib.util.module_from_spec(s)
s.loader.exec_module(m)
archive={'instrument_name':'BTC-USDT-SWAP','funding_rate':'7.019044316E-7','funding_time':'1788566400000'}
api={'instrument_name':'BTC-USDT-SWAP','funding_rate':'0.0000007019044316','funding_time':'1788566400000'}
# Before the fix this falls back to the existing raw-dict conflict rule and fails.
same=getattr(m,'same_funding',lambda a,b:a==b)
assert same(archive,api),'equivalent actual archive/API funding representations falsely conflict'
assert not same(archive,{**api,'funding_rate':'0.0000007019044317'})
assert not same(archive,{**api,'funding_time':'1788595200000'})
assert not same(archive,{**api,'instrument_name':'ETH-USDT-SWAP'})
print('PASS: equivalent funding numbers accepted; actual rate/time/instrument conflicts rejected')
