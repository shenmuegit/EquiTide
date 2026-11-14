"""Declare a BTC entry-hurdle batch while retaining audited engines and original accounts."""
from pathlib import Path
import ast,json
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2]
def edit(n,pairs):
 p=R/n;s=p.read_text()
 for a,b in pairs:assert a in s,(n,a);s=s.replace(a,b)
 p.write_text('\n'.join(x.rstrip() for x in s.splitlines())+'\n')
edit('freeze.py',[("20261114T035058Z","20261114T055030Z"),("BTC strictROC L29/H.03 momentum, symmetric exit retention buffer E in[.005,.01,.015]","BTC strictROC L29 momentum, symmetric newentry hurdle H in[.025,.03,.035], fixed symmetric exit retention buffer E.01"),("bs={.01:reuse(B,.01,.01)};es={r:reuse(c,.01,r)","bs={.03:reuse(B,.03,.01)};es={r:reuse(c,.03,r)"),("for V in [.005,.015]:","for V in [.025,.035]:"),("cap3_E{str(V)","cap3_H{str(V)"),("btc-exit-buffer-neighborhood","btc-entry-hurdle-neighborhood"),("entry_volatility_window_days=14,exit_buffer_fraction=V","entry_volatility_window_days=14,exit_buffer_fraction=.01,return_hurdle=V"),("[.005,.01,.015]","[.025,.03,.035]"),("if V==.01:","if V==.03:"),("parent_BTCE{str(V)","parent_BTCH{str(V)"),("btc-exit-buffer-eth-carry-bank-combination","btc-entry-hurdle-eth-carry-bank-combination"),("==(.015,.01)","==(.035,.01)"),("Does increasing the BTC exit-retention buffer reduce whipsaw and execution cost without losing chronological robustness?E.015/R.01 preset before all results; E in[.025,.03,.035],BTC V14 cap.03 fixed. ExistingE.01,ETHbanks,centerparents andmatchedholds readonly.","Does a stricter BTC momentum entry threshold suppress marginal signals enough to preserve chronological net performance after execution/funding costs? Predeclare H[.025,.03,.035] andETHR[.00875,.01],L29/E.01/V14cap.03 fixed. H.035/R.01 preset before outcomes. ExistingH.03,ETHbanks,centerparents,matchedholds readonly."),("BTC_EXIT_BUFFER","BTC_ENTRY_HURDLE"),("symmetric BTC exit retention buffer fraction; L29/H.03,V14cap.03 fixed","symmetric BTC strict momentum entry threshold fraction; L29/E.01,V14cap.03 fixed"),("{'W':.015,'K':.01}","{'W':.035,'K':.01}"),("BTC_native_only_own_exit_axis","BTC_native_only_own_entry_axis"),("BTCexitbuffer.005/.015newparameters;rawweightsremain1/1,notrenamedE.01.","BTCentryhurdle.025/.035newparameters;rawweightsremain1/1,notrenamedH.03.")])
edit('definitions.py',[("20261114T035058Z","20261114T055030Z"),("q['exit_buffer_fraction'] in [.005,.015]","q['exit_buffer_fraction']==.01 and q['return_hurdle'] in [.025,.035]")])
for n in ['run.py','audit.py','exports.py']:
 p=R/n;p.write_text(p.read_text().replace('BTC_EXIT_BUFFER','BTC_ENTRY_HURDLE'))
p=R/'parent_units.py';s=p.read_text();a=s.index('for E in ');b=s.index('for cap in ',a);s=s[:a]+'''for H in [F('.025'),F('.03'),F('.035')]:
 E=F('.01')
 for actual in [-1,0,1]:
  for roc in sorted(set([-H-F('.00000001'),-H,-E-F('.00000001'),-E,F(0),E,E+F('.00000001'),H,H+F('.00000001')])):
   c=[F(100)]*50;c[39]=100*(1+roc);want=1 if roc>H else -1 if roc<-H else 1 if actual==1 and roc>-E else -1 if actual==-1 and roc<E else 0;out,r=engine.btc.target(c,40,29,float(H),actual,float(E));assert want==out and F(r)==roc and engine.btc.target(c[:40]+[F(10**12),F(1)],40,29,float(H),actual,float(E))==(out,r);n+=1
'''+s[b:];s=s.replace("g['W']==.01","g['W']==.03");p.write_text(s)
edit('forward_registry.py',[("PREV=ROOT/'research/experiments/20261114T035058Z'","PREV=ROOT/'research/experiments/20261114T055030Z'")])
edit('checks.py',[("P=ROOT/'research/experiments/20261114T035058Z'","P=ROOT/'research/experiments/20261114T055030Z'"),("full=P/'forward_inputs.json.gz'","full=ROOT/'research/experiments/20261114T035058Z/forward_inputs.json.gz'")])
# Move current mark windows forward two hours; full66 background remains the real035058 source.
p=R/'review/preflight.py';p.write_text(p.read_text().replace('2026-11-14T00:30:00Z','2026-11-14T02:30:00Z').replace('2026-11-14T04:10:00Z','2026-11-14T06:10:00Z'))
p=R/'review/setup.py';s=p.read_text().replace("P=ROOT/'research/experiments/20261114T035058Z'","P=ROOT/'research/experiments/20261114T055030Z'").replace("full=P/'forward_inputs.json.gz'","full=ROOT/'research/experiments/20261114T035058Z/forward_inputs.json.gz'");s=s.replace("'2026-11-14T00:30:00Z','2026-11-14T02:30:00Z'","'2026-11-14T02:30:00Z','2026-11-14T04:30:00Z'").replace("'2026-11-14T02:10:00Z','2026-11-14T04:10:00Z'","'2026-11-14T04:10:00Z','2026-11-14T06:10:00Z'");p.write_text(s)
p=R/'exports.py';s=p.read_text().replace('BTC symmetric exit buffer; V14 cap3%','BTC entry hurdle; E1%, V14 cap3%').replace("['0.5%','1.0%','1.5%']","['2.5%','3.0%','3.5%']").replace('Preregistered BTC exit buffer / ETH carry budget','Preregistered BTC entry hurdle / ETH carry budget');p.write_text(s)
p=R/'publish.py';p.write_text(p.read_text().replace('test BTC exit buffers with reused ETH banks','test BTC entry thresholds with reused ETH banks'))
# Finalizer and plain reporting may be edited without changing evaluated source bindings.
p=R/'finalize.py';s=p.read_text().replace("P=ROOT/'research/experiments/20261114T035058Z'","P=ROOT/'research/experiments/20261114T055030Z'").replace(", 'formatter_syntax_verification.json'",'').replace("'adapt.py'","'prepare.py'").replace("['2026-11-14T02:30:00Z','2026-11-14T04:30:00Z']","['2026-11-14T04:30:00Z','2026-11-14T06:30:00Z']").replace("['2026-11-14T04:10:00Z','2026-11-14T06:10:00Z']","['2026-11-14T06:10:00Z','2026-11-14T08:10:00Z']");p.write_text(s)
for p in R.rglob('*.py'):p.write_text('\n'.join(x.rstrip() for x in p.read_text().splitlines())+'\n');ast.parse(p.read_text())
print('PASS H2.5/3/3.5pct andETHR2axis definitions prepared; policy/core unchanged;0financialcalculations')
