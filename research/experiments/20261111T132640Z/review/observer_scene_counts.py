"""Read-only correction of a frozen auditor display count; all actual ledgers/reports retained."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put,rel,now
rd=lambda p:json.loads(p.read_text());rows=[]
for stem in ['candidate','l4h02','fewm']:
 report=rd(R/(stem+'_observation/report.json'));v=rd(R/(stem+'_verification.json'));assert len(report['configs'])==3 and all(len(c['scenes'])==3 for c in report['configs'].values());actual=sum(len(c['scenes']) for c in report['configs'].values());assert actual==9 and v['cost_scenes']==36 and v['full_NAV_points_checked']==actual*v['NAV_points_per_scene']
 rows.append({'account':stem,'actual_cost_scenes':actual,'frozen_auditor_output_label':v['cost_scenes'],'actual_report':rel(R/(stem+'_observation/report.json')),'report_sha256':sha(R/(stem+'_observation/report.json')),'original_verification':rel(R/(stem+'_verification.json')),'original_verification_sha256':sha(R/(stem+'_verification.json')),'full_NAV_points_checked':v['full_NAV_points_checked']})
put(R/'observer_scene_count_verification.json',{'passed':True,'recorded_utc':now(),'rows':rows,'cause':'Preparationcountrewritechangedonlyauditorout.cost_scenes9to36;financialauditorloopsandfull_NAV_points_checkedremain9scenes.Uncoveredafterfinancialreserve,so36boundsourcesremainunchangedandnativeoutputiskept.Correctcount9derivedfromactualconfigs/scenesandfullNAVproof.','actual_financial_or_account_reports_rewritten':False,'bound_sources_changed_after_reserve':False,'new_financial_or_account_evaluations':0})
print('PASS actual9costscenes/account/fullNAV proof;frozen displaylabel36 explicitlycorrected,originaloutputandreports retained')
