"""Repair only independent neighbor selection's wrong-axis eager evaluation;retain failed audit."""
import ast,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
rd=lambda p:json.loads(p.read_text());plan=rd(R/'plan.json');report=rd(R/'report.json');h=sha(R/'report.json');original=R/'audit.py';bound=rd(R/'code_binding_before_evaluation.json');assert sha(original)==bound['source_sha256'][rel(original)] and rd(R/'audit_commands.json')[0]['exit_code']==1
old="  rows=plan['grid'] if c['scope']=='parent' else plan['native_grid'];ns=[full[g['fingerprint']] for g in rows if abs(plan['axes']['BTC_RECENT_CONFIRM_DAYS'].index(g['W'])-plan['axes']['BTC_RECENT_CONFIRM_DAYS'].index(c['W']))<=1 and abs(plan['axes']['ETH_FUND_R'].index(g['K'])-plan['axes']['ETH_FUND_R'].index(c['K']))<=1];dims=2"
new="  rows=plan['grid'] if c['scope']=='parent' else plan['native_grid'];ns=[];dims=2\n  if c['scope']=='parent':ns=[full[g['fingerprint']] for g in rows if abs(plan['axes']['BTC_RECENT_CONFIRM_DAYS'].index(g['W'])-plan['axes']['BTC_RECENT_CONFIRM_DAYS'].index(c['W']))<=1 and abs(plan['axes']['ETH_FUND_R'].index(g['K'])-plan['axes']['ETH_FUND_R'].index(c['K']))<=1]"
source=original.read_text();assert source.count(old)==1
# Minimal regression: old expression raises on ETH's unrelated W=0; new branch uses only applicable axis.
regression=[]
for c in [z for z in plan['native_grid'] if z['asset']=='BTC']:
 try:[g for g in plan['native_grid'] if abs(plan['axes']['BTC_RECENT_CONFIRM_DAYS'].index(g['W'])-plan['axes']['BTC_RECENT_CONFIRM_DAYS'].index(c['W']))<=1]
 except ValueError:raised=True
 else:raised=False
 assert raised
 same=[g for g in plan['native_grid'] if g['asset']=='BTC' and abs(plan['axes']['BTC_RECENT_CONFIRM_DAYS'].index(g['W'])-plan['axes']['BTC_RECENT_CONFIRM_DAYS'].index(c['W']))<=1];assert len(same)==(3 if c['W']==5 else 2);regression.append({'W':c['W'],'original_wrong_axis_raises':raised,'fixed_BTC_neighbors':len(same)})
fixed=source.replace(old,new);ast.parse(fixed);dest=R/'audit_retry1.py';dest.write_text(fixed);assert fixed.replace(new,old)==source and sha(R/'report.json')==h
put(R/'audit_repair_binding.json',{'passed':True,'recorded_utc':now(),'completed_report_sha256':h,'supplemental_readonly_source_sha256':{rel(dest):sha(dest)},'original_bound_audit_sha256_unchanged':sha(original),'failed_native_receipt':rel(R/'audit_commands.json'),'root_cause':'Independent audit eagerly applied BTC axis to readonly ETH W0 before native-specific branch;0 absent from new4/5/6axis. Valuation run.neighbors already correctly filters native asset first.','minimal_regression':regression,'only_difference':{'before':old,'after':new},'no_return_policy_accounting_or_gate_changed':True,'no_strategy_or_account_reevaluation':True,'audit_reads_only_saved_native_archives':True})
f=R/'commands.py';s=f.read_text();anchor="out=[];dest=R/(phase+'_commands.json')";assert anchor in s;s=s.replace(anchor,"if phase=='audit_retry1':jobs=[('audit_retry1.log',['audit_retry1.py'])]\n"+anchor);ast.parse(s);f.write_text(s)
f=R/'finalize.py';s=f.read_text();anchor="key=('candidate_retry2_commands.json' if";assert anchor in s;s=s.replace("key=('candidate_retry2_commands.json' if phase=='candidate' and (R/'candidate_transport_recovery_binding.json').exists() else phase+'_commands.json')","key=('audit_retry1_commands.json' if phase=='audit' and (R/'audit_repair_binding.json').exists() else 'candidate_retry2_commands.json' if phase=='candidate' and (R/'candidate_transport_recovery_binding.json').exists() else phase+'_commands.json')");ast.parse(s);f.write_text(s)
print('PASS reproduced wrong-axis ValueError;3syntheticneighbors verified,onlyread-only auditbranch repaired/bound;0financialreruns')
