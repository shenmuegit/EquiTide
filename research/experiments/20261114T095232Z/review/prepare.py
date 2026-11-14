"""Declare BTC lookback neighbors and new original-account windows; no evaluation."""
from pathlib import Path
import ast,json
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2]
def edit(n,pairs):
 p=R/n;s=p.read_text()
 for a,b in pairs:assert a in s,(n,a);s=s.replace(a,b)
 p.write_text('\n'.join(x.rstrip() for x in s.splitlines())+'\n')
edit('freeze.py',[("20261114T055030Z","20261114T075131Z"),("entry-hurdle and funding-budget","lookback and funding-budget"),("BTC strictROC L29 momentum, symmetric newentry hurdle H in[.025,.03,.035], fixed symmetric exit retention buffer E.01","BTC strictROC lookback L in[28,29,30], fixed symmetric entry hurdle H.03 and exit retention buffer E.01"),("bs={.03:reuse(B,.03,.01)};es={r:reuse(c,.03,r)","bs={29:reuse(B,29,.01)};es={r:reuse(c,29,r)"),("for V in [.025,.035]:","for V in [28,30]:"),("name=f'BTC_L29_V14_cap3_H{str(V).replace(\".\",\"p\")}_391d'","name=f'BTC_L{V}_H3_E1_V14cap3_391d'"),("btc-entry-hurdle-neighborhood","btc-momentum-lookback-neighborhood"),("entry_volatility_window_days=14,exit_buffer_fraction=.01,return_hurdle=V","entry_volatility_window_days=14,exit_buffer_fraction=.01,return_hurdle=.03,lookback_days=V"),("[.025,.03,.035]","[28,29,30]"),("if V==.03:","if V==29:"),("name=f'parent_BTCH{str(V).replace(\".\",\"p\")}_V14_ETHR{str(r).replace(\".\",\"p\")}_391d'","name=f'parent_BTCL{V}_H3_E1_ETHR{str(r).replace(\".\",\"p\")}_391d'"),("btc-entry-hurdle-eth-carry-bank-combination","btc-lookback-eth-carry-bank-combination"),("==(.035,.01)","==(30,.01)"),("BTC_ENTRY_HURDLE","BTC_LOOKBACK_DAYS"),("symmetric BTC strict momentum entry threshold fraction; L29/E.01,V14cap.03 fixed","BTC completed-close ROC lookback in days; H.03/E.01,V14cap.03 fixed"),("{'W':.035,'K':.01}","{'W':30,'K':.01}"),("BTC_native_only_own_entry_axis","BTC_native_only_own_lookback_axis"),("BTCentryhurdle.025/.035newparameters;rawweightsremain1/1,notrenamedH.03.","BTClookback28/30newparameters;rawweightsremain1/1,notrenamedL29.")])
p=R/'freeze.py';s=p.read_text();a=s.index("'hypothesis':");b=s.index(",'rules':rules",a);s=s[:a]+"'hypothesis':'Does changing BTC momentum memory from29days to28/30days preserve chronological net performance after costs without increasing whipsaw? L[28,29,30]xETHR[.00875,.01],H.03/E.01/V14cap.03 fixed. L30/R.01 is preset before outcomes. ExistingL29,ETHbanks,centerparents,matchedholds readonly.'"+s[b:];p.write_text(s)
edit('definitions.py',[("20261114T055030Z","20261114T075131Z"),("q['return_hurdle'] in [.025,.035]","q['return_hurdle']==.03 and q['lookback_days'] in [28,30]")])
for n in ['run.py','audit.py','exports.py']:
 p=R/n;p.write_text(p.read_text().replace('BTC_ENTRY_HURDLE','BTC_LOOKBACK_DAYS'))
p=R/'parent_units.py';s=p.read_text();a=s.index('for H in ');b=s.index('for cap in ',a);s=s[:a]+'''H,E=F('.03'),F('.01')
for L in [28,29,30]:
 for actual in [-1,0,1]:
  for roc in sorted(set([-H-F('.00000001'),-H,-E-F('.00000001'),-E,F(0),E,E+F('.00000001'),H,H+F('.00000001')])):
   c=[F(200)]*50;c[39-L]=F(100);c[39]=100*(1+roc);want=1 if roc>H else -1 if roc<-H else 1 if actual==1 and roc>-E else -1 if actual==-1 and roc<E else 0;out,r=engine.btc.target(c,40,L,float(H),actual,float(E));assert want==out and F(r)==roc and engine.btc.target(c[:40]+[F(10**12),F(1)],40,L,float(H),actual,float(E))==(out,r);n+=1
'''+s[b:];s=s.replace("g['W']==.03","g['W']==29");p.write_text(s)
edit('forward_registry.py',[("PREV=ROOT/'research/experiments/20261114T055030Z'","PREV=ROOT/'research/experiments/20261114T075131Z'")])
edit('checks.py',[("P=ROOT/'research/experiments/20261114T055030Z'","P=ROOT/'research/experiments/20261114T075131Z'")])
p=R/'review/preflight.py';s=p.read_text().replace('2026-11-14T02:30:00Z','2026-11-14T04:30:00Z').replace('2026-11-14T06:10:00Z','2026-11-14T08:10:00Z');p.write_text(s)
p=R/'review/setup.py';s=p.read_text().replace("P=ROOT/'research/experiments/20261114T055030Z'","P=ROOT/'research/experiments/20261114T075131Z'").replace("'2026-11-14T02:30:00Z','2026-11-14T04:30:00Z'","'2026-11-14T04:30:00Z','2026-11-14T06:30:00Z'").replace("'2026-11-14T04:10:00Z','2026-11-14T06:10:00Z'","'2026-11-14T06:10:00Z','2026-11-14T08:10:00Z'");p.write_text(s)
p=R/'exports.py';s=p.read_text().replace('BTC entry hurdle; E1%, V14 cap3%','BTC ROC lookback days; H3%/E1%').replace("['2.5%','3.0%','3.5%']","['28','29','30']").replace('Preregistered BTC entry hurdle / ETH carry budget','Preregistered BTC momentum lookback / ETH carry budget');p.write_text(s)
p=R/'publish.py';p.write_text(p.read_text().replace('test BTC entry thresholds with reused ETH banks','test BTC momentum lookbacks with reused ETH banks'))
p=R/'finalize.py';s=p.read_text().replace("P=ROOT/'research/experiments/20261114T055030Z'","P=ROOT/'research/experiments/20261114T075131Z'").replace("['2026-11-14T04:30:00Z','2026-11-14T06:30:00Z']","['2026-11-14T06:30:00Z','2026-11-14T08:30:00Z']").replace("['2026-11-14T06:10:00Z','2026-11-14T08:10:00Z']","['2026-11-14T08:10:00Z','2026-11-14T10:10:00Z']");p.write_text(s)
for p in R.rglob('*.py'):p.write_text('\n'.join(x.rstrip() for x in p.read_text().splitlines())+'\n');ast.parse(p.read_text())
print('PASS preregistration source preparation forL28/29/30 xETHR, fixed original kernels;0financial calculations')
