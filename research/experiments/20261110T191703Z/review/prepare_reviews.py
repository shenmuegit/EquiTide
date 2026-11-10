"""Prepare independent saved-evidence audits for PRICE_V/VC and own single16; no valuation."""
import ast
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def edit(name,pairs):
 f=R/'review'/name;s=f.read_text()
 for a,b in pairs:
  assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);f.write_text(s)
edit('control_diagnostics.py',[("c['L'] in [4,5,6] and c['V'] in [8,10,12]","c['L']==5 and c['V'] in [6,7,8] and c['VC'] in [.045,.05,.055]")])
edit('unfiltered_control.py',[("['lookback_days','entry_volatility_window_days']","['entry_volatility_window_days','entry_volatility_ceiling']")])
edit('materialize_status.py',[("'axes':{'L':p['fast_lookbacks'],'PRICE_V':p['price_vol_windows']}","'axes':{'PRICE_V':p['price_vol_windows'],'VC':p['volatility_ceilings']}"),("'VC':.05,'S':16,'D':3","'L':5,'S':16,'D':3"),("'current_axes':['L','PRICE_V'],'L_values':p['fast_lookbacks'],'PRICE_V_values':p['price_vol_windows']","'current_axes':['PRICE_V','VC'],'L_values':[5],'PRICE_V_values':p['price_vol_windows'],'VC_values':p['volatility_ceilings']"),("NextSMA_single14:30to16:30:single must book own16 using current immutableactualfields;SMA marks. NextL4_FEWM16:10to18:10marks,no repeat16. CurrentL4/FEWM own16 alreadyonce.","NextSMA_single16:30to18:30marks;NextL4_FEWM18:10to20:10marks/risk. All3 ownNov10_16.002 now once;no repeats;no daily/fills untilNov11UTC00:01.")])
edit('metadata.py',[("{(z['L'],z['V']) for z in b if z['scope']=='parent'}=={(ll,vv) for ll in [4,5,6] for vv in [8,10,12] if (ll,vv)!=(5,10)}","{(z['V'],z['VC']) for z in b if z['scope']=='parent'}=={(vv,vc) for vv in [6,7,8] for vc in [.045,.05,.055] if (vv,vc)!=(8,.05)}"),("==207","==210"),("==8169","==8289"),("'L':[4,5,6],'PRICE_V':[8,10,12]","'L':[5],'PRICE_V':[6,7,8]"),("'VC':[.05]","'VC':[.045,.05,.055]"),("'pricegate_V':[8,10,12]","'pricegate_V':[6,7,8]")])
edit('evidence.py',[("row['VC']==.05","row['VC'] in [.045,.05,.055]"),("row['L'] in [4,5,6] and row['V'] in [8,10,12] and (row['L'],row['V'])!=(5,10)","row['L']==5 and row['V'] in [6,7,8] and (row['V'],row['VC'])!=(8,.05)"),("'price_V':[8,10,12],'L':[4,5,6]","'price_V':[6,7,8],'L':[5]"),("'VC':[.05]","'VC':[.045,.05,.055]"),("z['L'] in [4,6] or z['V'] in [8,12]","z['V'] in [6,8] or z['VC'] in [.045,.055]"),("'axes':['L','PRICE_V']","'axes':['PRICE_V','VC']"),("{'candidate':0,'l4h02':6,'fewm':6}","{'candidate':6,'l4h02':0,'fewm':0}")])
edit('round_conclusion.py',[("b['fast_lookback_days']==5 and b['volatility_window_days']==10","b['fast_lookback_days']==5 and b['volatility_window_days']==8 and a['return_exact']==b['return_exact']"),("'axes':['L','PRICE_V']","'axes':['PRICE_V','VC']"),("attempts+li['provenance']+qi['provenance']+rd(R/'funding16_nov10_preflight_receipts.json')","attempts+li['provenance']+qi['provenance']"),("'fresh16_public_GETs':len(rd(R/'funding16_nov10_preflight_receipts.json'))","'fresh16_public_GETs':0,'originalNov10_16_GETs':len(rd(R/'funding16_nov10_preflight_receipts.json'))")])
edit('realized_aliases.py',[("'L':c['L']","'L':c['L'],'PRICE_V':c['V']")])
# The fresh16 source was actually captured last round; current round only reuses public fields.
f=R/'review/current_account_events.py';s=f.read_text();s=s.replace("receipt=rd(R/'review_capture_nov10_16_public.py_receipt.json');assert receipt['exit_code']==0", "receipt=rd(R/'review_public_nov10_16_reuse.py_receipt.json');original=ROOT/'research/experiments/20261110T171502Z/review_capture_nov10_16_public.py_receipt.json';assert receipt['actual_exit_code']==0 and rd(original)['exit_code']==0")
s=s.replace("'review/capture_nov10_16_public.py','review_capture_nov10_16_public.py_receipt.json'","'review/public_nov10_16_reuse.py','review_public_nov10_16_reuse.py_receipt.json','funding16_nov10_reuse.json'")
s=s.replace("(0 if stem=='candidate' else 6)","(6 if stem=='candidate' else 0)").replace("(NOV10_08 if stem=='candidate' else max(newtimes))","max(newtimes)")
s=s.replace("assert sum(len(sets[t]) for t in newtimes)==(6 if stem=='candidate' else 0)","assert sum(len(sets[t]) for t in newtimes)==6")
s=s.replace("{'candidate':0,'l4h02':6,'fewm':6} and len(rows)==12","{'candidate':6,'l4h02':0,'fewm':0} and len(rows)==6")
s=s.replace("rel(R/'review_capture_nov10_16_public.py_receipt.json')","rel(original)").replace("sha(R/'review_capture_nov10_16_public.py_receipt.json')","sha(original)").replace("'fresh_public_GETs':len(rr)","'fresh_public_GETs':0,'original_public_GETs':len(rr),'current_reuse_native_receipt':rel(R/'review_public_nov10_16_reuse.py_receipt.json')").replace("'single_pending_own14_30to16_30_window':True","'all_three_own_Nov10_16_completed_once':True,'single_pending_own_window':False")
ast.parse(s);f.write_text(s)
print('Saved evidence reviews prepared for PRICE_V6/7/8 x VC.045/.05/.055; current ownfund counts single6/L4_0/FEWM0')
