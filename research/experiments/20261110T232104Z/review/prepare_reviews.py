"""Prepare unbound independent H/E saved-evidence audits; no market/account valuation."""
import ast
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def edit(n,pairs):
 f=R/'review'/n;s=f.read_text()
 for a,b in pairs:
  assert a in s,(n,a);s=s.replace(a,b)
 ast.parse(s);f.write_text(s)
edit('control_diagnostics.py',[("old['H']==c['H']==.02 and old['E']==c['E']==.0075","old['H']==.02 and old['E']==.0075 and c['H'] in [.0175,.02,.0225] and c['E'] in [.00625,.0075,.00875]"),("c['S'] in [12,16,20]","c['S']==16"),("c['L'] in [4,5,6]","c['L']==5")])
edit('unfiltered_control.py',[("['entry_volatility_window_days','entry_volatility_ceiling','lookback_days','trend_lookback_days','trend_window_days','trend_decay_numerator','trend_decay_denominator']","['entry_volatility_window_days','entry_volatility_ceiling','return_hurdle','long_entry_return_hurdle','short_entry_return_hurdle','exit_buffer_fraction']")])
edit('materialize_status.py',[("'axes':{'L':p['fast_lookbacks'],'S':p['slow_windows']}","'axes':{'H':p['entry_hurdles'],'E':p['exit_buffers']}"),("'fixed_price':{'H':.02,'E':.0075,'K':.0075,'V':6,'VC':.055,'D':3}","'fixed_price':{'L':5,'S':16,'K':.0075,'V':6,'VC':.055,'D':3}"),("'current_axes':['L','S'],'L_values':p['fast_lookbacks'],'S_values':p['slow_windows']","'current_axes':['H','E'],'H_values':p['entry_hurdles'],'E_values':p['exit_buffers'],'L_values':[5],'S_values':[16]"),("'fixed_H':.02,'fixed_E':.0075","'old_center_H':.02,'old_center_E':.0075"),("NextSMA_single18:30to20:30marks;NextL4_FEWM20:10to22:10marks/risk.","NextSMA_single20:30to22:30marks;NextL4_FEWM22:10toNov11_00:10 requires freshactualNov11_00 source after00:11closure beforebinding/reserve,andown00:01daily oncompleteNov10 context.")])
edit('metadata.py',[("{(z['L'],z['S']) for z in b if z['scope']=='parent'}=={(ll,ss) for ll in [4,5,6] for ss in [12,16,20] if (ll,ss)!=(5,16)}","{(z['H'],z['E']) for z in b if z['scope']=='parent'}=={(hh,ee) for hh in [.0175,.02,.0225] for ee in [.00625,.0075,.00875] if (hh,ee)!=(.02,.0075)}"),("==213","==216"),("==8409","==8529"),("'L':[4,5,6],'PRICE_V':[6],'S':[12,16,20]","'L':[5],'PRICE_V':[6],'S':[16]"),("'H':[.02],'E':[.0075]","'H':[.0175,.02,.0225],'E':[.00625,.0075,.00875]")])
edit('evidence.py',[("row['H']==.02 and row['E']==.0075 and row['S'] in [12,16,20] and row['D']==3 and row['L'] in [4,5,6] and row['V']==6 and (row['L'],row['S'])!=(5,16)","row['H'] in [.0175,.02,.0225] and row['E'] in [.00625,.0075,.00875] and row['S']==16 and row['D']==3 and row['L']==5 and row['V']==6 and (row['H'],row['E'])!=(.02,.0075)"),("'L':[4,5,6],'S':[12,16,20]","'L':[5],'S':[16]"),("'H':[.02],'E':[.0075]","'H':[.0175,.02,.0225],'E':[.00625,.0075,.00875]"),("z['L'] in [4,6] or z['S'] in [12,20]","z['H'] in [.0175,.0225] or z['E'] in [.00625,.00875]"),("'axes':['L','S']","'axes':['H','E']")])
edit('round_conclusion.py',[("'axes':['L','S']","'axes':['H','E']")])
print('Unbound H/E audits prepared;fixedL5/S16,V6/VC055;current4mark windows/no funding;next L4/FEWM midnight requirements explicit')
