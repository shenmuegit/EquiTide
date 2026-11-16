"""Read saved ROC/held-unit records to explain unchanged exit paths; no new model."""
import gzip,json,sys
from fractions import Fraction as F
from decimal import Decimal as D
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
r=json.loads((R/'report.json').read_text());h=sha(R/'report.json');c=next(c for c in r['all_current_native_grid'].values() if c['asset']=='BTC' and c['W']==.005);arc=ROOT/c['archive'];a=json.loads(gzip.decompress(arc.read_bytes()));rows=[];low=F('.00375');high=F('.00625')
for k,s in a['scenes'].items():
 events=s['decisions'];assert len(events)==391;held=[];flat_near=0;occupied_near=[]
 for z in events:
  roc=F(z['policy_audit']['return_exact']);q=D(z['state_before']['signed_units']);d=1 if q>0 else -1 if q<0 else 0
  if d:held.append((d,roc,z['signal_available_ts_ns']))
  if d==1 and -high<=roc<=-low or d==-1 and low<=roc<=high:occupied_near.append({'timestamp_ns':z['signal_available_ts_ns'],'direction':d,'ROC':str(roc)})
  if d==0 and (low<=roc<=high or -high<=roc<=-low):flat_near+=1
 assert not occupied_near
 rows.append({'cost':int(k),'saved_decisions':len(events),'actually_held_decisions':len(held),'held_decisions_inside_exit_difference_bands':len(occupied_near),'flat_decisions_inside_these_bands':flat_near,'bands_exact':{'long':[-float(high),-float(low)],'short':[float(low),float(high)]},'closest_held_distance_to_any_exit_band_edge_exact':str(min(min(abs(roc+x) if d==1 else abs(roc-x) for x in [low,high]) for d,roc,_ in held))})
assert sha(R/'report.json')==h
put(R/'exit_activation_audit.json',{'passed':True,'recorded_utc':now(),'financial_report_sha256':h,'source_archive':rel(arc),'source_archive_sha256':sha(arc),'rows':rows,'interpretation':'No actual held-state ROC enters bands where E.00375 andE.00625 could differ. Savednewdecisions/books/trades/funding/NAV already proven identical to oldE.005. Newscalarparametersarevalidnewconfigs,butidenticalhistoricalpathsaddnoindependentalphaevidence.','new_market_account_configuration_or_registry_evaluations':0});print('PASS savedexitactivationbands',json.dumps(rows))
