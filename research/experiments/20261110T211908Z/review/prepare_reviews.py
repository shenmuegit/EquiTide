"""Prepare only unbound saved-evidence/account audits for L/S; no valuation."""
import ast
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def edit(n,pairs):
 f=R/'review'/n;s=f.read_text()
 for a,b in pairs:
  assert a in s,(n,a);s=s.replace(a,b)
 ast.parse(s);f.write_text(s)
# Original public16 anchor intentionally stays171502; account PREV must be191703.
for n in ['account_windows.py','metadata.py','sma_source_identity.py']:
 f=R/'review'/n;s=f.read_text().replace("P=ROOT/'research/experiments/20261110T171502Z'","P=ROOT/'research/experiments/20261110T191703Z'");ast.parse(s);f.write_text(s)
edit('control_diagnostics.py',[("old['VC']==.05","old['VC']==.055 and old['V']==6"),("c['S']==16 and c['D']==3 and c['L']==5 and c['V'] in [6,7,8] and c['VC'] in [.045,.05,.055]","c['S'] in [12,16,20] and c['D']==3 and c['L'] in [4,5,6] and c['V']==6 and c['VC']==.055")])
edit('unfiltered_control.py',[("['entry_volatility_window_days','entry_volatility_ceiling']","['entry_volatility_window_days','entry_volatility_ceiling','lookback_days','trend_lookback_days','trend_window_days','trend_decay_numerator','trend_decay_denominator']")])
edit('materialize_status.py',[("'axes':{'PRICE_V':p['price_vol_windows'],'VC':p['volatility_ceilings']}","'axes':{'L':p['fast_lookbacks'],'S':p['slow_windows']}"),("'fixed_price':{'H':.02,'E':.0075,'K':.0075,'L':5,'S':16,'D':3}","'fixed_price':{'H':.02,'E':.0075,'K':.0075,'V':6,'VC':.055,'D':3}"),("'current_axes':['PRICE_V','VC'],'L_values':[5],'PRICE_V_values':p['price_vol_windows'],'VC_values':p['volatility_ceilings']","'current_axes':['L','S'],'L_values':p['fast_lookbacks'],'S_values':p['slow_windows'],'PRICE_V_values':[6],'VC_values':[.055]"),("'fixed_VC':.05","'fixed_VC':.055"),("NextSMA_single16:30to18:30marks;NextL4_FEWM18:10to20:10marks/risk.","NextSMA_single18:30to20:30marks;NextL4_FEWM20:10to22:10marks/risk.")])
edit('metadata.py',[("{(z['V'],z['VC']) for z in b if z['scope']=='parent'}=={(vv,vc) for vv in [6,7,8] for vc in [.045,.05,.055] if (vv,vc)!=(8,.05)}","{(z['L'],z['S']) for z in b if z['scope']=='parent'}=={(ll,ss) for ll in [4,5,6] for ss in [12,16,20] if (ll,ss)!=(5,16)}"),("all(a[n]==c[n] for n in a if n!='decide')","a==c and (P/'engine.py').read_bytes()==(R/'engine.py').read_bytes()"),("==210","==213"),("==8289","==8409"),("'L':[5],'PRICE_V':[6,7,8],'S':[16]","'L':[4,5,6],'PRICE_V':[6],'S':[12,16,20]"),("'VC':[.045,.05,.055]","'VC':[.055]"),("'pricegate_V':[6,7,8]","'pricegate_V':[6]")])
edit('evidence.py',[("row['VC'] in [.045,.05,.055]","row['VC']==.055"),("row['S']==16 and row['D']==3 and row['L']==5 and row['V'] in [6,7,8] and (row['V'],row['VC'])!=(8,.05)","row['S'] in [12,16,20] and row['D']==3 and row['L'] in [4,5,6] and row['V']==6 and (row['L'],row['S'])!=(5,16)"),("'price_V':[6,7,8],'L':[5],'S':[16]","'price_V':[6],'L':[4,5,6],'S':[12,16,20]"),("'VC':[.045,.05,.055]","'VC':[.055]"),("['entry_volatility_ceiling']==.05","['entry_volatility_ceiling']==.055"),("z['V'] in [6,8] or z['VC'] in [.045,.055]","z['L'] in [4,6] or z['S'] in [12,20]"),("'axes':['PRICE_V','VC']","'axes':['L','S']"),("{'candidate':6,'l4h02':0,'fewm':0}","{'candidate':0,'l4h02':0,'fewm':0}")])
edit('round_conclusion.py',[("b['entry_volatility_ceiling']==.05","b['entry_volatility_ceiling']==.055"),("b['volatility_window_days']==8 and a['return_exact']==b['return_exact']","b['volatility_window_days']==6"),("for n in ['slow_mean_exact','slow_reference_mean_exact','slow_distance_exact']:assert a[n]==b[n]","for n in ['observed_sample_logvol','volatility_window_days']:assert a[n]==b[n]"),("(b,.0075,.05,.02,.0075)","(b,.0075,.055,.02,.0075)"),("'axes':['PRICE_V','VC']","'axes':['L','S']")])
# Allthree already booked16 last round: current delta contains zero funding for each.
f=R/'review/current_account_events.py';s=f.read_text().replace("(6 if stem=='candidate' else 0)","0").replace("{'candidate':6,'l4h02':0,'fewm':0} and len(rows)==6","{'candidate':0,'l4h02':0,'fewm':0} and len(rows)==0");ast.parse(s);f.write_text(s)
print('Independent L/S reviews and four ownmark windows ready; account PREV191703, original16capture171502 retained')
