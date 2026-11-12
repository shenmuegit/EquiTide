"""Official bounded funding-history reads and definition-only exact component lookup."""
import gzip, json, subprocess, sys, urllib.parse
from datetime import datetime, timezone
from pathlib import Path
R=Path(__file__).resolve().parents[1]; ROOT=R.parents[2]
sys.path.insert(0,str(R));from common import *
ms=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*1000)
lo=ms('2026-11-12T00:30:00Z');hi=ms('2026-11-12T04:10:00Z')
out=R/'window_funding_preflight';out.mkdir();receipts=[];fields={}
for asset in ['BTC','ETH']:
 url='https://fapi.binance.com/fapi/v1/fundingRate?'+urllib.parse.urlencode({'symbol':asset+'USDT','startTime':lo+1,'endTime':hi,'limit':1000})
 for attempt in range(3):
  started=now();cmd=['curl','--ipv4','--compressed','--http1.1','--silent','--show-error','--connect-timeout','10','--max-time','30','--write-out','\n%{http_code}',url];z=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=40);body,code=z.stdout.rsplit(b'\n',1) if b'\n' in z.stdout else (z.stdout,b'000');path=out/f'{asset}_{attempt}.json.gz';path.write_bytes(gzip.compress(body,mtime=0));rec={'asset':asset,'url':url,'started_utc':started,'finished_utc':now(),'http_status':int(code),'curl_exit_code':z.returncode,'raw':rel(path),'sha256':sha(path),'body_sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body),'stderr':z.stderr.decode(errors='replace')};receipts.append(rec);put(R/'window_funding_preflight_attempts.json',receipts)
  if z.returncode==0 and int(code)==200:
   rows=json.loads(body);assert isinstance(rows,list) and all(v['symbol']==asset+'USDT' and lo<v['fundingTime']<=hi for v in rows);fields[asset]=rows;break
 else:raise RuntimeError('Official funding preflight blocked; no dependent account calculation')
put(R/'window_funding_preflight.json',{'passed':True,'recorded_utc':now(),'start_exclusive_utc':'2026-11-12T00:30:00Z','end_inclusive_utc':'2026-11-12T04:10:00Z','public_fields_by_asset':fields,'raw_responses':receipts,'new_GETs':len(receipts),'financial_or_account_calculations':0,'scope':'Actual public settlement timestamps determine windows; nominal eight-hour schedule not assumed.'})
rs=reg.read_records(ROOT/'research/automation/registry.jsonl')
btc={.03:'76ddc848b244802d98e85e01a389e79ce3a36d0ff4af81f823498003ae95f030',.04:'8a6f349c528b65754e29a5efabbf04e5a76d5b50a8380d9c042c3768dac48a95',.05:'8e25c505446e24c640f6d0054a191866355136c65b6471cda110f01d2d409c48'}
eth={.00875:'d2188e34f6d96f2205823e74b834003e1b5d5dd8c2994f0ccd8b72062fed4a53',.01:'ee5d9cea8f250a0b6151bf8d6ff7824ce472dc557265589594b200f0110de0f9',.01125:'00093933f37c94a2df842d4ed7efdd45fa293bfa5085a52fd33bacbd5a500eea'}
for H,fp in btc.items():
 z=rs[fp];p=z['spec']['parameters'];assert z['result_available'] and p['return_hurdle']==H and p['exit_buffer_fraction']==.01 and p['fixed_entry_notional_usdt']==1000 and p['initial_capital_usdt']==3750
for ratio,fp in eth.items():
 z=rs[fp];p=z['spec']['parameters'];assert z['result_available'] and p['entry_funding_volatility_ratio']==ratio and p['entry_funding_budget_volatility_window_days']==8 and p['fixed_entry_notional_usdt']==4000 and p['initial_capital_usdt']==15000
rows=[]
for H,b in btc.items():
 for ratio,e in eth.items():
  matches=[]
  for fp,z in rs.items():
   sp=z.get('spec',{});cs=sp.get('components',[])
   if sp.get('kind')=='combination' and len(cs)==2 and sorted((c['fingerprint'],float(c['weight'])) for c in cs)==sorted([(b,1.),(e,1.)]):
    assert z['result_available'],(fp,z['status']);matches.append(fp)
  rows.append({'BTC_H':H,'ETH_R':ratio,'sources':[b,e],'existing_parent_matches':matches})
put(R/'predeclared_parent_grid_inventory.json',{'recorded_utc':now(),'economic_hypothesis':'BTC entry selectivity H3/4/5percent versus ETH financing tolerance R.00875/.01/.01125. Whole unchanged banks,N1000/4000,C3750/15000,raw1/1,no normalization or transfers. Joint recent robustness is tested; reused development history gives no untouched evidence.','fixed_BTC_L':29,'fixed_BTC_E':.01,'fixed_ETH_rules':'L5/H.02/E.0075,S16/D3/K.0075,V6/cap.05625,VW8/M4','candidate_axes':{'BTC_H':list(btc),'ETH_R':list(eth)},'planned_representative':{'BTC_H':.04,'ETH_R':.01},'rows':rows,'old_native_quantity_or_policy_runs_planned':0,'financial_or_NAV_calculations_done':0})
print('PASS actual settlement fields',fields,'grid old/new',sum(bool(x['existing_parent_matches']) for x in rows),sum(not x['existing_parent_matches'] for x in rows),flush=True)
