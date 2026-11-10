"""Read exact old unfiltered H2 bank/parent for incremental evidence; no new valuation."""
import json,sys
from pathlib import Path
from decimal import Decimal as D
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import reg,sha,put,rel
rd=lambda p:json.loads(p.read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');p=rd(R/'plan.json');r=rd(R/'report.json');B=p['fixed_BTC_fingerprint'];E='dd44fcda1ac5e61dcf9c2350625af79811695d323e58f7048c6e0b37d5b66569';key=lambda sp:sorted((x['fingerprint'],D(str(x['weight']))) for x in sp['components']);ps=[fp for fp,z in rs.items() if z.get('spec',{}).get('kind')=='combination' and key(z['spec'])==sorted([(B,D(1)),(E,D(1))])];assert len(ps)==1;refs={};configs={}
for scope,fp in [('native',E),('parent',ps[0])]:
 z=rs[fp];assert z['result_available'] and sha(ROOT/z['report'])==z['report_sha256'];c=next(c for c in rd(ROOT/z['report'])['configs'].values() if c['fingerprint']==fp);sp=rs[fp]['spec'];assert sp['parameters']['initial_capital_usdt']==(15000 if scope=='native' else 18750)
 for name in ['spec','archive']:assert (ROOT/c[name]).exists()
 configs[scope]=c;refs[scope]={'fingerprint':fp,'status':z['status'],'report':z['report'],'report_sha256':z['report_sha256'],'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'archive':c['archive'],'archive_sha256':sha(ROOT/c['archive'])}
rows=[]
for c in r['configs'].values():
 old=configs[c['scope']]
 if c['scope']=='native':
  q=rd(ROOT/c['spec'])['parameters'];base=rs[E]['spec']['parameters'];assert {k:v for k,v in q.items() if not k.startswith('entry_funding_')}==base
 else:assert c['source_fingerprints'][0]==B and c['capital_usdt']==18750
 ss={}
 for k,z in c['scenes'].items():
  q=old['scenes'][k];same=z['NAV_sha256_f64le']==q['NAV_sha256_f64le'];dom=q['net_return_pct']>=z['net_return_pct'] and q['max_drawdown_pct']<=z['max_drawdown_pct'] and (q['net_return_pct']>z['net_return_pct'] or q['max_drawdown_pct']<z['max_drawdown_pct']);ss[k]={'new_net_return_pct':z['net_return_pct'],'old_unfiltered_net_return_pct':q['net_return_pct'],'new_whole_DD_pct':z['max_drawdown_pct'],'old_unfiltered_whole_DD_pct':q['max_drawdown_pct'],'old_unfiltered_dominates_return_and_DD':dom,'complete_saved_NAV_hash_equal':same}
 rows.append({'fingerprint':c['fingerprint'],'scope':c['scope'],'M':c['M'],'R':c['R'],'VW':c['VW'],'status':c['status'],'unfiltered_control_fingerprint':old['fingerprint'],'scenes':ss,'all3_saved_NAV_hashes_equal':all(z['complete_saved_NAV_hash_equal'] for z in ss.values()),'unfiltered_strictly_dominates_at_all3costs':all(z['old_unfiltered_dominates_return_and_DD'] for z in ss.values())})
assert len(rows)==16
put(R/'unfiltered_control_comparison.json',{'passed':True,'report_sha256':sha(R/'report.json'),'source_results':refs,'rows':rows,'summary':{'new_current_configs':16,'all3_saved_NAV_equal_to_unfiltered':sum(x['all3_saved_NAV_hashes_equal'] for x in rows),'new_historical_passed_parents':len(r['summary']['passed']),'passed_parents_same_unfiltered_path':sum(x['scope']=='parent' and x['status']=='passed' and x['all3_saved_NAV_hashes_equal'] for x in rows),'new_models_strictly_dominated_by_unfiltered_at_all3costs':sum(x['unfiltered_strictly_dominates_at_all3costs'] for x in rows)},'new_strategy_or_account_valuations':0,'old_statuses_and_bytes_unchanged':True,'interpretation':'MatchedC/NH2unfilteredbaselineisactualoldresult. Fullpathmatchesarenotindependentnewprofitevidence;remainingcandidatecanpasshistoricalgateswhilebeingdominatedbyoldunfilteredbaseline. Thisdescriptiveincrementalcomparisondoesnotalterfrozenqualificationgates/statusesororiginalaccounts.'});print('PASSactualoldunfilteredH2samebanks/36savedcomparisons,no newevaluations;oldpathmatches',sum(x['all3_saved_NAV_hashes_equal'] for x in rows))
