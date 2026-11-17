"""Adapt unchanged native kernels to the predeclared VW10/12 batch and next account windows."""
import ast,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;P=ROOT/'research/experiments/20261117T182123Z'
assert not (R/'plan.json').exists()
for f in P.glob('*.py'):
 if f.name in {'bootstrap.py','configure_current.py'}:continue
 s=f.read_text().replace('20261117T162156Z','20261117T182123Z').replace('2931227','2964144')
 (R/f.name).write_text(s)
def change(name,pairs):
 f=R/name;s=f.read_text()
 for a,b in pairs:
  assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);f.write_text(s)
change('freeze_confirmation.py',[
 ("in [7,9] for z", "in [10,12] for z"),('VS=[7,8,9];NEW=[7,9]','VS=[9,10,12];NEW=[10,12]'),
 ("E=actual('cb3c8bf2ba5106ebd505174ea724e4d767a6c738743e2418f527c39ea06863c1');C0=actual('738ee4c044465340a268f19087660ca23dc03bbc3f4c21f73c903c2633d3e18c');C1=actual('ae6cc9880e24680794ad824bda0e0c2296820b9eccfb1b01aa300fd2334fe1ec')", "selected=json.loads((R/'baseline_reference_selection.json').read_text());assert selected['passed'];E=actual(selected['ETH_fingerprint']);C0=actual(selected['parent_fingerprints']['0.03']);C1=actual(selected['parent_fingerprints']['0.0325'])"),
 ('es={8:reuse(E,8,.03)}','es={9:reuse(E,9,.03)}'),('if window==8:', 'if window==9:'),('(7,.03)', '(10,.03)'),("'W':7", "'W':10"),
 ('[7,8readonly,9]','[9readonly,10,12]'),('OldVW8','OldVW9'),('VW7/8/9','VW9/10/12'),('days7/9','days10/12'),
 ('Faster/slower carry-budget sample-log-vol windowsVW7/VW9 versus readonlyVW8','Longer carry-budget sample-log-vol windowsVW10/VW12 versus readonlyVW9'),('RepresentativeETHVW7','RepresentativeETHVW10'),('VW7/8readonly/9','VW9readonly/10/12'),('presetVW7','presetVW10'),('ETHbudgetVW7/9','ETHbudgetVW10/12')])
change('definitions.py',[("in [7,9]", "in [10,12]"),("'new_ETH_budget_window':[7,9],'old_ETH_budget_window':8", "'new_ETH_budget_window':[10,12],'old_ETH_budget_window':9")])
change('units_budget_window.py',[("in [7,9]", "in [10,12]"),('new_budget_VW7_VW9','new_budget_VW10_VW12'),('carryVW8','carryVW9')])
change('prepare.py',[("'units_funding_ratio.py'", "'units_budget_window.py'"),('1794904200000','1794911400000'),('1794917460000','1794924660000'),("['2026-11-17T08:30:00Z','2026-11-17T12:11:00Z']", "['2026-11-17T10:30:00Z','2026-11-17T14:11:00Z']"),('SMA/single08:30to10:30;L4/FEWM10:10to12:10','SMA/single10:30to12:30;L4/FEWM12:10to14:10'),('VW7/VW9 faster/slower completed sample logvol','VW10/VW12 longer completed sample logvol'),('oldVW8readonly','oldVW9readonly'),('RepresentativeVW7','RepresentativeVW10'),("'ETH_FUNDING_BUDGET_WINDOW':[7,8,9]", "'ETH_FUNDING_BUDGET_WINDOW':[9,10,12]"),("'new_ETH_budget_windows':[7,9],'readonly_ETH_budget_window':8", "'new_ETH_budget_windows':[10,12],'readonly_ETH_budget_window':9"),("'ETH_budget_window':7", "'ETH_budget_window':10")])
change('exports.py',[("['7','8 (old)','9']", "['9 (old)','10','12']"),('VW 7/8/9','VW 9/10/12')])
change('collect.py',[("refETH=allc['cb3c8bf2ba5106ebd505174ea724e4d767a6c738743e2418f527c39ea06863c1']", "refETH=allc[rd(R/'baseline_reference_selection.json')['ETH_fingerprint']]"),('paired_differences_to_old_VW8','paired_differences_to_old_VW9'),("'old_budget_window':8", "'old_budget_window':9"),('VW7/VW9','VW10/VW12'),('VW=[7,8只读,9]','VW=[9只读,10,12]'),('代表固定VW7','代表固定VW10'),('预算VW7/8/9','预算VW9/10/12'),('较短或较长的预算波动率窗口','较长的预算波动率窗口'),('M2/M3旧配置已有真实结果，本轮只读，不精确重跑。','旧VW9及BTC银行已有真实结果，本轮只读复用，不精确重跑。'),('相对旧VW8父组合','相对旧VW9父组合'),('Nextsingle10:30to12:30andL4/FEWM12:10to14:10','Nextsingle12:30to14:30andL4/FEWM14:10to16:10'),('本轮SMA/single Nov17_08:30→10:30；L4/FEWM10:10→12:10。','本轮SMA/single Nov17_10:30→12:30；L4/FEWM12:10→14:10。'),('下一轮SMA/single10:30→12:30（12:31闭合），L4/FEWM12:10→14:10（14:11闭合）','下一轮SMA/single12:30→14:30（14:31闭合），L4/FEWM14:10→16:10（16:11闭合），后者可能包含新的实际结算，须先查完整实际记录后再按自有持仓计账')])
for name in ['finalize.py']:
 change(name,[("['2026-11-17T10:30:00Z','2026-11-17T12:30:00Z']", "['2026-11-17T12:30:00Z','2026-11-17T14:30:00Z']"),("['2026-11-17T12:10:00Z','2026-11-17T14:10:00Z']", "['2026-11-17T14:10:00Z','2026-11-17T16:10:00Z']")])
# Private transport and verification orchestration stays outside sealed research outputs.
F=ROOT/'.git/automation_proofs'
for suffix in ['pipeline.py','run_stage.py','final_git.py','postrelease.py']:
 s=(F/('20261117T182123Z_'+suffix)).read_text().replace('20261117T182123Z','20261117T202125Z').replace('20261117T162156Z','20261117T182123Z')
 if suffix=='postrelease.py':
  s=s.replace("'ETH_FUNDING_BUDGET_WINDOW':[7,8,9]", "'ETH_FUNDING_BUDGET_WINDOW':[9,10,12]").replace("{'W':7,'K':.03}", "{'W':10,'K':.03}")
  s=s.replace("['2026-11-17T10:30:00Z','2026-11-17T12:30:00Z']", "['2026-11-17T12:30:00Z','2026-11-17T14:30:00Z']").replace("['2026-11-17T12:10:00Z','2026-11-17T14:10:00Z']", "['2026-11-17T14:10:00Z','2026-11-17T16:10:00Z']")
  s=s.replace("assert len(r['summary']['passed'])==4 and len(r['summary']['rejected_source_components'])==2 and not r['summary']['passed_source_components'];", "assert len(r['configs'])==6;")
  s=s.replace("'historical_parent_gate_passed':4,'historical_components_rejected':2", "'historical_parent_gate_passed':len(r['summary']['passed']),'historical_components_rejected':len(r['summary']['rejected_source_components'])")
 ast.parse(s);(F/(R.name+'_'+suffix)).write_text(s)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert all(sha(R/n)==sha(P/n) for n in ['engine.py','core391_tail_safe.py'])
for f in R.glob('*.py'):ast.parse(f.read_text())
print('CONFIGURED VW9readonly/10/12; new10/12; preset10; native engine/accounting exact; actual account windows from pointers')
