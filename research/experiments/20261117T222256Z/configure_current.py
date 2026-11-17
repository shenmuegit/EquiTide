"""Pre-evaluation setup for a genuinely new ETH fast hurdle batch; immutable money kernels."""
import ast,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;P=ROOT/'research/experiments/20261117T202125Z';assert not (R/'plan.json').exists()
for f in P.glob('*.py'):
 if f.name in {'bootstrap.py','configure_current.py','units_budget_window.py'}:continue
 s=f.read_text().replace('20261117T182123Z','20261117T202125Z').replace('2964144','2998936')
 if f.name in {'run.py','audit.py','parent_units.py','exports.py'}:s=s.replace('ETH_FUNDING_BUDGET_WINDOW','ETH_FAST_ENTRY_H')
 (R/f.name).write_text(s)
def edit(name,pairs):
 f=R/name;s=f.read_text()
 for a,b in pairs:assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);f.write_text(s)
edit('commands.py',[("'units_budget_window.log',['units_budget_window.py']","'units_fast_entry.log',['units_fast_entry.py']")])
edit('prepare.py',[
 ('1794911400000','1794918600000'),('1794924660000','1794931860000'),("assert responses=={'BTC':[],'ETH':[]},responses", "assert all(isinstance(xs,list) for xs in responses.values())"),
 ("['2026-11-17T10:30:00Z','2026-11-17T14:11:00Z']", "['2026-11-17T12:30:00Z','2026-11-17T16:11:00Z']"),
 ('SMA/single10:30to12:30;L4/FEWM12:10to14:10. Freshcompleteactualfundinglookup hasnoevents;all3perpsalreadybooked08once,neverrepeat.', 'SMA/single12:30to14:30;L4/FEWM14:10to16:10. Derive each actual settlement strictly in its own (start,cutoff] from fresh complete lookup;all3perpsalreadybooked08once,neverrepeat. New events require own held q/rate/mark and cost stress.'),
 ('no newresearchVW adoption','no newresearchH adoption'),
 ("'hypothesis':'VW10/VW12 longer completed sample logvol may adapt the carry budget to changing risk; oldVW9readonly. FixedR.0075/M4/entryriskV6cap.05625/fastROC/finiteEWM/native money. RepresentativeVW10/BTCH.03 setbeforeoutcomes.'", "'hypothesis':'ETH fast ROC reversal H1.75%/2.25% versus old2% may alter event frequency and entry quality; finite EWM/trend/risk V6cap.05625/M4/R.0075/budgetVW9/native money fixed. RepresentativeETHH.0175/BTCH.03 before outcomes.'"),
 ("'ETH_FUNDING_BUDGET_WINDOW':[9,10,12]", "'ETH_FAST_ENTRY_H':[.0175,.02,.0225]"),
 ("'new_ETH_budget_windows':[10,12],'readonly_ETH_budget_window':9", "'new_ETH_fast_hurdles':[.0175,.0225],'readonly_ETH_fast_hurdle':.02,'fixed_budget_window':9"),
 ("'ETH_budget_window':10", "'ETH_fast_entry_hurdle':.0175")])
# Native full query is the immutable first capture for new actual events in this window.
s=(R/'prepare.py').read_text();needle="previous=rd(P/'next_research_state.json')['UTC_midnight_handoff'];windows={}"
s=s.replace(needle,"put(R/'new_actual_settlement_preflight.json',{**fresh,'first_public_capture_for_this_rounds_new_events':True,'no_cashflow_calculation_yet':True})\n"+needle)
s=s.replace("'SMA_background_authorities.json']", "'SMA_background_authorities.json','new_actual_settlement_preflight.json']")
ast.parse(s);(R/'prepare.py').write_text(s)
# Synthetic scalar and future-prefix checks use the actual H in every frozen spec.
s=(P/'units_budget_window.py').read_text().replace('h=F(\'.02\')',"h=F(str(p['return_hurdle']))").replace("p['entry_funding_budget_volatility_window_days'] in [10,12]", "p['entry_funding_budget_volatility_window_days']==9 and p['return_hurdle'] in [.0175,.0225]")
s=s.replace("put(R/'budget_window_verification.json'", "put(R/'fast_entry_verification.json'").replace('new_budget_VW10_VW12_sample_vol_formula_and_closed_prefix_checked','fixed_VW9_budget_and_new_H0175_H0225_checked')
(R/'units_fast_entry.py').write_text(s)
for suffix in ['pipeline.py','run_stage.py','final_git.py','postrelease.py','review_scope.py']:
 s=(ROOT/'.git/automation_proofs'/('20261117T202125Z_'+suffix)).read_text().replace('20261117T202125Z','20261117T222256Z').replace('20261117T182123Z','20261117T202125Z')
 ast.parse(s);(ROOT/'.git/automation_proofs'/(R.name+'_'+suffix)).write_text(s)
assert all(hashlib.sha256((R/n).read_bytes()).digest()==hashlib.sha256((P/n).read_bytes()).digest() for n in ['engine.py','core391_tail_safe.py'])
for f in R.glob('*.py'):ast.parse(f.read_text())
print('Prepared source templates; fastH grid not yet frozen/reserved/calculated; original engine and money bytes exact')
