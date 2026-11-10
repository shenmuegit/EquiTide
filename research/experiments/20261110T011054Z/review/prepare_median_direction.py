"""Prepare causal median-policy implementation before all reservations; no valuations."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'engine.py';s=p.read_text();a=s.index(" before_funding=wanted;");b=s.index("\n return wanted,",a);s=s[:a]+" before_funding=wanted;sn=int(m['frame']['available_ts'][i*1440-1]);event=median_funding(m['signal_funds'],sn,int(p['entry_funding_settlement_count']));wanted,funding_audit=funding_filter(wanted,actual,event,sn,D(str(p['entry_funding_outflow_cap'])))"+s[b:]
a=s.index('\ndef funding_filter(');b=s.index('\ndef slope_gate(',a)
s=s[:a]+'''
def median_funding(events,signal_ns,count):
 assert count in [2,3,4]
 eligible=sorted([e for e in events if HOUR<=signal_ns-e['settlement_ts']<=36*HOUR and e['available_ts']<=signal_ns],key=lambda e:e['settlement_ts'],reverse=True)
 assert len({e['settlement_ts'] for e in eligible})==len(eligible)
 selected=eligible[:count]
 if len(selected)<count:return None
 rates=sorted(e['realized_rate'] for e in selected);mid=count//2;rate=rates[mid] if count%2 else (rates[mid-1]+rates[mid])/D(2)
 return {'events':selected,'median_rate':rate,'count':count}

def funding_filter(raw,actual,event,signal_ns,cap):
 applied=bool(raw and raw!=actual)
 valid=event is not None and len(event['events'])==event['count'] and all(HOUR<=signal_ns-e['settlement_ts']<=36*HOUR and e['available_ts']<=signal_ns for e in event['events'])
 outflow=max(D(raw)*event['median_rate'],D(0)) if valid else None;blocked=applied and (not valid or outflow>cap)
 audit={'applied':applied,'blocked':blocked,'cap_fraction_per_settlement':str(cap),'minimum_age_ns':HOUR,'maximum_age_ns':36*HOUR,'signal_available_ts_ns':signal_ns,'selected_settlements':[{'settlement_ts_ns':e['settlement_ts'],'available_ts_ns':e['available_ts'],'realized_rate':str(e['realized_rate']),'source_index':e['source_index']} for e in event['events']] if valid else [],'median_realized_rate':str(event['median_rate']) if valid else None,'settlement_count':event['count'] if valid else None,'expected_outflow_fraction':str(outflow) if outflow is not None else None,'availability_policy':'sourceconservative1hdelay;actualsettlements1to36holdinclusiveandavailable<=signal;latestNmedian,no future rate;missing required recordsblocks newentryonly','scope':'new_or_reversed_position_only'}
 return (0 if blocked else raw),audit
''' +s[b:];p.write_text(s)
# Retain all native accounting and observation source implementations; change only financial signal-grid metadata below.
for name in ['run.py','audit.py','check_decisions.py','check_grid_diagnostics.py']:
 p=R/name;s=p.read_text();s=s.replace("p['entry_hurdles'].index(g['H'])-p['entry_hurdles'].index(c['H'])","p['funding_counts'].index(g['M'])-p['funding_counts'].index(c['M'])").replace("plan['entry_hurdles'].index(g['H'])-plan['entry_hurdles'].index(c['H'])","plan['funding_counts'].index(g['M'])-plan['funding_counts'].index(c['M'])").replace("p['entry_hurdles'].index(h['H'])-p['entry_hurdles'].index(g['H'])","p['funding_counts'].index(h['M'])-p['funding_counts'].index(g['M'])")
 s=s.replace("['L','H','E','S','K','D','N','VC','F']","['L','H','E','S','K','D','N','VC','F','M']").replace("'E':g['E'],'F':g['F']","'E':g['E'],'F':g['F'],'M':g['M']").replace("'E':g['E'],'VC':g['VC']","'E':g['E'],'M':g['M'],'F':g['F'],'VC':g['VC']")
 s=s.replace("g['H'] in [min(p['entry_hurdles']),max(p['entry_hurdles'])]","g['M'] in [min(p['funding_counts']),max(p['funding_counts'])]").replace("'varied_axes':['ETH_entry_hurdle_H','ETH_entry_funding_outflow_cap_F']","'varied_axes':['ETH_past_funding_count_M','ETH_entry_funding_outflow_cap_F']").replace('SixnewETHfundingcaps0/.00005xH.0175/.02/.0225plus6parents/36costscenes;fixedE.0075L5K.0075VC5S16D3V10. OldcapOffthreeHcolumn','SixnewETHpastfundingmedianM2/3/4xcaps0/.00005plus6parents/36costscenes;fixedH.02E.0075L5K.0075VC5S16D3V10. OldlatestM1twoFrow')
 p.write_text(s)
# Independent policy audit sorts the actual eligible source records and recomputes median with Fraction.
p=R/'audit.py';s=p.read_text();a=s.index('   pre_funding=wanted;');b=s.index("   assert audit['ungated_desired']",a)
s=s[:a]+'''   pre_funding=wanted;sn=int(m['frame']['available_ts'][i*1440-1]);count=int(p['entry_funding_settlement_count']);assert count in [2,3,4];eligible=[e for e in m['signal_funds'] if sn-36*HOUR<=e['settlement_ts']<=sn-HOUR and e['available_ts']<=sn];selected=list(reversed(sorted(eligible,key=lambda e:e['settlement_ts'])))[:count];assert len(selected)==count;rates=sorted(F(e['realized_rate']) for e in selected);median=rates[count//2] if count%2 else (rates[count//2-1]+rates[count//2])/2;fa=audit['funding_filter'];fc=F(str(p['entry_funding_outflow_cap']));out=max(F(wanted)*median,F(0));ap=bool(wanted and wanted!=actual);block=ap and out>fc;wanted=0 if block else wanted
   expected_fields=[{'settlement_ts_ns':e['settlement_ts'],'available_ts_ns':e['available_ts'],'realized_rate':str(e['realized_rate']),'source_index':e['source_index']} for e in selected]
   assert audit['raw_desired_before_funding_filter']==pre_funding and fa['applied']==ap and fa['blocked']==block and F(fa['cap_fraction_per_settlement'])==fc and fa['signal_available_ts_ns']==sn and fa['selected_settlements']==expected_fields and fa['settlement_count']==count and F(fa['median_realized_rate'])==median and F(fa['expected_outflow_fraction'])==out and fa['minimum_age_ns']==HOUR and fa['maximum_age_ns']==36*HOUR
''' +s[b:];p.write_text(s)
# CSV row cardinalities change to a 4x2 surface; all actual6+6/36scenes/old18banks unchanged.
p=R/'check_exports.py';s=p.read_text().replace("'sensitivity_grid.csv':27","'sensitivity_grid.csv':24").replace("'native_sensitivity_grid.csv':27","'native_sensitivity_grid.csv':24").replace("'adjacent_edges.csv':72","'adjacent_edges.csv':60").replace("'matched_hold_comparisons.csv':27","'matched_hold_comparisons.csv':24").replace("'fixed_allocations.csv':10","'fixed_allocations.csv':9");p.write_text(s)
print('Prepared median M/F signal, independent Fraction median audit and4x2 grids;0valuations')
