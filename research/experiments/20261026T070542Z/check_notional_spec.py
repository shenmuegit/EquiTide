"""Fail before simulation if the budget and its declared fraction disagree."""
import json
from decimal import Decimal as D
from run import ROOT,R,reg
batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==108
for row in batch:
 sp=json.loads((ROOT/row['spec']).read_text());p=sp['parameters'];assert reg.fingerprint(sp)==row['fingerprint']
 if row['scope']=='native':
  n=D(str(p['fixed_entry_notional_usdt']));f=D(str(p['raw_entry_notional_fraction_of_initial_capital']));capital=D(str(p['initial_capital_usdt']));assert n==f*capital,(row['name'],'fixed_entry_notional_usdt',str(n),'raw_fraction',str(f),'capital',str(capital))
 else:
  assert p['component_initial_entry_notionals_usdt']==[row['BTC_fixed_entry_notional_usdt'],row['ETH_fixed_entry_notional_usdt']] and sum(p['component_initial_entry_notionals_usdt'])==4000
  for c,n in zip(sp['components'],p['component_initial_entry_notionals_usdt']):assert records[c['fingerprint']]['spec']['parameters']['fixed_entry_notional_usdt']==n
print('PASS:108fixedbudgets,derivednativefractions,parent4000totalandcomponentsconsistent;zero financial evaluation.')
