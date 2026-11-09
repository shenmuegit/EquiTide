"""Descriptive comparison with actually executed priorL4; no policy or NAV evaluation."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];P=ROOT/'research/experiments/20261108T065441Z';sys.path.insert(0,str(R));from common import put,sha
rd=lambda p:json.loads(p.read_text());prior=rd(P/'report.json');manifest=rd(P/'data_manifest.json');cur=rd(R/'report.json');assert sha(P/'report.json')==manifest['finished_report_sha256'];rows=[]
for c in cur['configs'].values():
 old=next(z for z in prior['configs'].values() if z['scope']==c['scope'] and z['D']==6 and z['L']==4);assert old['E']==.01 and c['E']==.01 and c['VC'] in [.05,.055] and old['K']==.015 and c['K'] in [.005,.0075,.01] and old['capital_usdt']==c['capital_usdt'];costs={}
 for k,s in c['scenes'].items():
  q=old['scenes'][k];costs[k]={'return_pct':s['net_return_pct'],'old_L4_return_pct':q['net_return_pct'],'return_delta_pp':s['net_return_pct']-q['net_return_pct'],'whole_DD_pct':s['max_drawdown_pct'],'old_L4_whole_DD_pct':q['max_drawdown_pct'],'Sharpe365':s['sharpe_365'],'old_L4_Sharpe365':q['sharpe_365'],'Calmar':s['calmar'],'old_L4_Calmar':q['calmar']}
 rows.append({'name':c['name'],'fingerprint':c['fingerprint'],'scope':c['scope'],'D':c['D'],'old_D':old['D'],'new_K':c['K'],'old_K':old['K'],'new_S':c['S'],'old_S':old['S'],'new_L':c['L'],'new_H':c['H'],'old_H':old['H'],'old_L':4,'old_fingerprint':old['fingerprint'],'cost_comparisons':costs,'current_status':c['status']})
assert len(rows)==12;put(R/'prior_L4_comparison.json',{'passed':True,'current_report_sha256':sha(R/'report.json'),'read_only_prior_report':str((P/'report.json').relative_to(ROOT)),'read_only_prior_report_sha256':sha(P/'report.json'),'rows':rows,'scope':'Descriptive fixedoldD6L4 versuscurrentD3S16L5_E1_VC5or5.5_K0.5or0.75or1;multi-axis descriptiveC/N/fixedE comparison only; no priorqualification rewrite,additionalstrategytrial,marketwindow,sourcecurvevaluationorpostoutcomegate.'});print('PASS12currentdefinitions versus exactpriorL4 metrics/36costcomparisons;priorreport unchanged,nopolicy/NAVrerun')
