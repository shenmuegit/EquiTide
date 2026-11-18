"""Initialize frozen EWM-span research and original account continuation templates."""
import ast,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;P=ROOT/'research/experiments/20261117T222256Z';assert not(R/'plan.json').exists()
for f in P.glob('*.py'):
 if f.name in {'bootstrap.py','configure_current.py','units_fast_entry.py','bind_new_settlement_source.py'}:continue
 s=f.read_text().replace('20261117T202125Z','20261117T222256Z').replace('2998936','3033269')
 if f.name in {'run.py','audit.py','parent_units.py','exports.py'}:s=s.replace('ETH_FAST_ENTRY_H','ETH_EWM_SPAN')
 (R/f.name).write_text(s)
def edit(name,pairs):
 f=R/name;s=f.read_text()
 for a,b in pairs:assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);f.write_text(s)
edit('commands.py',[("'units_fast_entry.log',['units_fast_entry.py']","'units_ewm_span.log',['units_ewm_span.py']")])
edit('prepare.py',[
 ('1794918600000','1794925800000'),('1794931860000','1794939060000'),("['2026-11-17T12:30:00Z','2026-11-17T16:11:00Z']", "['2026-11-17T14:30:00Z','2026-11-17T18:11:00Z']"),
 ("'first_public_capture_for_this_rounds_new_events':True", "'fresh_capture_for_existing_actual_settlement':True,'original_first_source_retained':True"),
 ('SMA/single12:30to14:30;L4/FEWM14:10to16:10.', 'SMA/single14:30to16:30;L4/FEWM16:10to18:10.'),
 ('New events require own held q/rate/mark and cost stress.', 'Single now books the actual16 event using ownq/rate/mark/cost;L4/FEWM alreadybooked16 and mustneverrepeat. First16sourceUTC/bytes retained;freshquery separately saved.'),
 ('no newresearchH adoption','no newresearchS adoption'),
 ("'hypothesis':'ETH fast ROC reversal H1.75%/2.25% versus old2% may alter event frequency and entry quality; finite EWM/trend/risk V6cap.05625/M4/R.0075/budgetVW9/native money fixed. RepresentativeETHH.0175/BTCH.03 before outcomes.'", "'hypothesis':'Finite normalized ETH EWM span12/20 versus readonly16 may change trend responsiveness and reversal entry quality; beta=(S-1)/(S+1) coupled,lag3/K.0075 fixed. L5/H.02/E.0075,riskV6cap.05625/M4R.0075/budgetVW9/native money fixed. RepresentativeS12/BTCH.03 before outcomes.'"),
 ("'ETH_FAST_ENTRY_H':[.0175,.02,.0225]", "'ETH_EWM_SPAN':[12,16,20]"),
 ("'new_ETH_fast_hurdles':[.0175,.0225],'readonly_ETH_fast_hurdle':.02", "'new_ETH_EWM_spans':[12,20],'readonly_ETH_EWM_span':16,'fixed_fast_H':.02"),
 ("'ETH_fast_entry_hurdle':.0175", "'ETH_EWM_span':12")])
# Independent finite-span Horner validation, with unchanged fast-H/risk/carry kernels.
s=(P/'units_fast_entry.py').read_text().replace('Synthetic carry-budget windows, strict gates and independent causal ETH policy checks.','Synthetic finite EWM spans, causal support, strict fast/trend gates and fixed risk/carry checks.')
s=s.replace('beta=F(15,17)',"S=int(p['trend_lookback_days']);beta=F(S-1,S+1)").replace('range(i-16,i)','range(i-S,i)').replace('range(i-19,i-3)','range(i-S-3,i-3)')
s=s.replace("p['return_hurdle'] in [.0175,.0225]", "p['return_hurdle']==.02 and S in [12,20] and p['trend_window_days']==S and p['trend_decay_numerator']==S-1 and p['trend_decay_denominator']==S+1")
s=s.replace('fast_entry_verification.json','ewm_span_verification.json').replace('fixed_VW9_budget_and_new_H0175_H0225_checked','new_EWM_S12_S20_beta_window_consistency_and_fixed_H2_VW9_checked')
needle="altered=copy.deepcopy(m);altered['closes']=closes[:i]+['1000000000000','1']*10;assert engine.decide(sp,altered,i,actual)==(out,a);n+=1"
rep=needle+"\n   older=copy.deepcopy(m);older['closes'][i-S-3-1]='1000000000000';assert engine.decide(sp,older,i,actual)==(out,a)"
assert needle in s;s=s.replace(needle,rep).replace("'closed_prefix_only':True", "'closed_prefix_only':True,'outside_finite_S_plus_lag_support_invariant':True")
s=s.replace('across new H;no marketbacktest','across new S;no marketbacktest')
ast.parse(s);(R/'units_ewm_span.py').write_text(s)
F=ROOT/'.git/automation_proofs'
for suffix in ['pipeline.py','run_stage.py','final_git.py','postrelease.py','review_scope.py']:
 s=(F/('20261117T222256Z_'+suffix)).read_text().replace('20261117T222256Z','20261118T002327Z').replace('20261117T202125Z','20261117T222256Z');ast.parse(s);(F/(R.name+'_'+suffix)).write_text(s)
assert all(hashlib.sha256((R/n).read_bytes()).digest()==hashlib.sha256((P/n).read_bytes()).digest() for n in ['engine.py','core391_tail_safe.py'])
print('EWM-span source templates ready; no strategy reserve or actual calculation yet; full engine/money bytes exact')
