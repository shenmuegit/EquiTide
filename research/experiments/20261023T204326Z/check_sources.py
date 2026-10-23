"""Verify exact sources,raw funded weights and non-repeated portfolio definitions."""
import json
from run import ROOT,R,LOOKS,HURDLES,sha,reg

def main():
 p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');refs=p['component_sources'];assert len(refs)==18 and len(batch)==81 and len({x['fingerprint'] for x in batch})==81
 for fp,ref in refs.items():
  spec=json.loads((ROOT/ref['spec']).read_text());q=spec['parameters'];assert spec['family']=='perpetual-daily-signed-momentum-zero-exit-hysteresis' and reg.fingerprint(spec)==fp and q['lookback_days'] in LOOKS and q['return_hurdle'] in HURDLES and q['exit_ROC']==0
  assert q['initial_capital_usdt']==10000 and q['fixed_entry_notional_usdt']==2000 and q['raw_entry_notional_fraction_of_initial_capital']==.2 and q['costs']==p['component_costs'];assert sha(ROOT/ref['archive'])==ref['archive_sha256'] and records[fp]['report_sha256']==ref['report_sha256'] and records[fp]['status']==ref['original_status'];assert q['start_utc']==p['time_boundaries']['oos_start_utc'] and q['end_utc']==p['time_boundaries']['oos_end_exclusive_utc']
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());assert reg.fingerprint(spec)==row['fingerprint'] and records[row['fingerprint']]['status']=='reserved';assert [x['fingerprint'] for x in spec['components']]==row['source_fingerprints'] and [x['weight'] for x in spec['components']]==[1,1] and [refs[x]['asset'] for x in row['source_fingerprints']]==['BTC','ETH'];assert spec['parameters']['initial_capital_usdt']==sum(refs[x]['capital_usdt'] for x in row['source_fingerprints'])==20000
 hold=p['read_only_hold_reference'];assert hold['fingerprint'] not in {x['fingerprint'] for x in batch};assert records[hold['fingerprint']]['report_sha256']==hold['report_sha256'] and sha(ROOT/hold['report'])==hold['report_sha256'] and sha(ROOT/hold['archive'])==hold['archive_sha256']
 print('PASS:18existingzeroexitcomponents/54costpaths,81newexactparents,1+1funded20000,2000entrypersleeve,unchangedsourcefees/funding/period/qualification,andoldholdreferenceonlyreadonly')

if __name__=='__main__':main()
