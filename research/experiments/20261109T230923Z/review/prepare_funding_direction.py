"""Prepare funding-feature implementation; executes no valuations or registrations."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'engine.py';s=p.read_text().replace('E in [.00625,.0075,.00875]','E==.0075')
s=s.replace(" return wanted,{'kind':'ETH_finite_EWMslope_entry_gate_reversal_entry_vol'", " before_funding=wanted;event=latest_funding(m['signal_funds'],int(m['frame']['available_ts'][i*1440-1]));wanted,funding_audit=funding_filter(wanted,actual,event,int(m['frame']['available_ts'][i*1440-1]),D(str(p['entry_funding_outflow_cap'])))\n return wanted,{'funding_filter':funding_audit,'raw_desired_before_funding_filter':before_funding,'kind':'ETH_finite_EWMslope_entry_gate_reversal_entry_vol'")
pos=s.index('\ndef slope_gate(')
s=s[:pos]+'''
def latest_funding(events,signal_ns):
 eligible=[e for e in events if HOUR<=signal_ns-e['settlement_ts']<=12*HOUR and e['available_ts']<=signal_ns]
 return max(eligible,key=lambda e:e['settlement_ts']) if eligible else None

def funding_filter(raw,actual,event,signal_ns,cap):
 applied=bool(raw and raw!=actual)
 valid=event is not None and HOUR<=signal_ns-event['settlement_ts']<=12*HOUR and event['available_ts']<=signal_ns
 outflow=max(D(raw)*event['realized_rate'],D(0)) if valid else None
 blocked=applied and (not valid or outflow>cap)
 audit={'applied':applied,'blocked':blocked,'cap_fraction_per_settlement':str(cap),'minimum_age_ns':HOUR,'maximum_age_ns':12*HOUR,'signal_available_ts_ns':signal_ns,'selected_settlement_ts_ns':event['settlement_ts'] if valid else None,'selected_available_ts_ns':event['available_ts'] if valid else None,'selected_realized_rate':str(event['realized_rate']) if valid else None,'selected_source_index':event['source_index'] if valid else None,'expected_outflow_fraction':str(outflow) if outflow is not None else None,'availability_policy':'source records carry conservative 1h publication delay; eligible past actualsettlement1to12h inclusive,latesttime,no future rate; missing blocks newentryonly','scope':'new_or_reversed_position_only'}
 return (0 if blocked else raw),audit
''' +s[pos:];p.write_text(s)
p=R/'market.py';s=p.read_text();s=s.replace('import numpy as np','import numpy as np\nimport polars as pl');s=s.replace(" for a,m in ms.items():m.update(first_ns=int(m['frame']['open_ts'][0]),fund_lookup={x['settlement_ts']:x for x in m['funds']},terminal_reference_decimal=m['frame']['open'][403*1440+1])", " for a,m in ms.items():\n  f=next(x for x in plan['data']['assets'][a] if x['path'].endswith('funding_settlement.parquet'));assert sha(ROOT/f['path'])==f['sha256'];events=pl.read_parquet(ROOT/f['path']).to_dicts();assert len(events)==1212 and all(e['available_ts']-e['settlement_ts']==HOUR for e in events);m.update(signal_funds=[{**e,'source_index':j} for j,e in enumerate(events)],first_ns=int(m['frame']['open_ts'][0]),fund_lookup={x['settlement_ts']:x for x in m['funds']},terminal_reference_decimal=m['frame']['open'][403*1440+1])")
p.write_text(s)
# A separate grid axis F never replaces or aliases the actual fixed exit E.
for n in ['run.py','audit.py','check_decisions.py','check_grid_diagnostics.py']:
 p=R/n;s=p.read_text();s=s.replace("p['exit_buffers'].index(g['E'])-p['exit_buffers'].index(c['E'])","p['funding_caps'].index(g['F'])-p['funding_caps'].index(c['F'])").replace("p['exit_buffers'].index(h['E'])-p['exit_buffers'].index(g['E'])","p['funding_caps'].index(h['F'])-p['funding_caps'].index(g['F'])")
 s=s.replace("['L','H','E','S','K','D','N','VC']","['L','H','E','S','K','D','N','VC','F']").replace("'E':g['E'],'VC':g['VC'],'H':g['H']","'E':g['E'],'F':g['F'],'VC':g['VC'],'H':g['H']")
 s=s.replace("g['E'] in [min(p['exit_buffers']),max(p['exit_buffers'])]","g['F'] in [p['funding_caps'][0],p['funding_caps'][-1]]")
 s=s.replace("'varied_axes':['ETH_entry_hurdle_H','ETH_exit_buffer_E']","'varied_axes':['ETH_entry_hurdle_H','ETH_entry_funding_outflow_cap_F']").replace('CurrentETH H/E diagnostics','CurrentETH H/F diagnostics')
 s=s.replace('SixnewETHentryH1.75/2.25percentxE0.625/0.75/0.875percentplus6parents/36costscenes;fixedL5K.0075VC5S16D3V10. OldH2threeErow,fixedBTC29H3E1bankandmatchedholdreadonly.', 'SixnewETHfundingcaps0/.00005xH.0175/.02/.0225plus6parents/36costscenes;fixedE.0075L5K.0075VC5S16D3V10. OldcapOffthreeHcolumn,fixedBTC29H3E1bankandmatchedholdreadonly.')
 p.write_text(s)
# Independent arithmetic policy auditor: select causal source rows without calling engine helpers.
p=R/'audit.py';s=p.read_text();s=s.replace("E in [.00625,.0075,.00875]","E==.0075")
s=s.replace("   assert audit['ungated_desired']==base", "   pre_funding=wanted;sn=int(m['frame']['available_ts'][i*1440-1]);past=[e for e in m['signal_funds'] if e['settlement_ts']<=sn-HOUR and e['settlement_ts']>=sn-12*HOUR and e['available_ts']<=sn];ev=sorted(past,key=lambda e:e['settlement_ts'])[-1] if past else None;fa=audit['funding_filter'];fc=D(str(p['entry_funding_outflow_cap']));out=max(D(wanted)*ev['realized_rate'],D(0)) if ev else None;ap=bool(wanted and wanted!=actual);block=ap and (ev is None or out>fc);wanted=0 if block else wanted\n   assert audit['raw_desired_before_funding_filter']==pre_funding and fa['applied']==ap and fa['blocked']==block and D(fa['cap_fraction_per_settlement'])==fc and fa['signal_available_ts_ns']==sn and fa['selected_source_index']==(ev['source_index'] if ev else None) and fa['selected_settlement_ts_ns']==(ev['settlement_ts'] if ev else None) and fa['selected_available_ts_ns']==(ev['available_ts'] if ev else None) and fa['selected_realized_rate']==(str(ev['realized_rate']) if ev else None) and fa['expected_outflow_fraction']==(str(out) if ev else None)\n   assert audit['ungated_desired']==base")
p.write_text(s)
print('Prepared pure funding selector/filter and independent policy audit; no market evaluation')
