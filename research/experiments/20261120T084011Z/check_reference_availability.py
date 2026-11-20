"""Complete economic definition screens for the two new local allocations."""
import json
from common import *
P=ROOT/'research/experiments/20261120T063909Z';rd=lambda p:json.loads(p.read_text());doc=rd(P/'report.json');allc={**doc['read_only_configs'],**{c['fingerprint']:c for c in doc['configs'].values()}};rs=reg.read_records(ROOT/'research/automation/registry.jsonl');CENTER=1250;CAPS=[.0525,.05625]
def select(scope,role,asset,N=None,W=None,K=None):
 cs=[x for x in allc.values() if x['scope']==scope and x['role']==role and x['asset']==asset and (scope!='parent' or x.get('NE')==3750) and (N is None or x.get('N')==N) and (W is None or x.get('W')==W) and (K is None or x.get('K')==K)];assert len(cs)==1,(scope,role,asset,N,W,K,len(cs));c=cs[0];z=rs[c['fingerprint']];assert z['result_available'] and sha(ROOT/z['report'])==z['report_sha256'];return c['fingerprint']
a={'passed':True,'center_BTC_N':CENTER,'center_ETH_N':3750,'BTC_strategies':{'1250':select('native','component','BTC',N=1250)},'BTC_holds':{'1250':select('native','benchmark','BTC',N=1250)},'ETH_strategies':{str(c):select('native','component','ETH',N=3750,K=c) for c in CAPS},'ETH_hold':select('native','benchmark','ETH',N=3750),'baseline_parents':{str(c):select('parent','candidate','COMBO',W=1250,K=c) for c in CAPS},'baseline_hold_parent':select('parent','benchmark','COMBO',W=1250),'source_report':rel(P/'report.json'),'source_report_sha256':sha(P/'report.json')}
excluded={'fixed_entry_notional_usdt','raw_entry_notional_fraction_of_initial_capital','persistence','prior_370day_source_fingerprint','warmup_days','embargo_days'};screens=[]
for asset,fp,news in [('BTC',a['BTC_strategies']['1250'],[750,1750]),*[( 'ETH',a['ETH_strategies'][str(c)],[4250,3250]) for c in CAPS]]:
 base=rs[fp]['spec'];q=base['parameters'];near=[]
 for f,z in rs.items():
  sp=z.get('spec',{});v=sp.get('parameters',{})
  if sp.get('kind')=='strategy' and sp.get('universe')==base['universe'] and {k:x for k,x in v.items() if k not in excluded}=={k:x for k,x in q.items() if k not in excluded}:near.append({'fingerprint':f,'N':v['fixed_entry_notional_usdt'],'C':v['initial_capital_usdt'],'status':z['status'],'result_available':z['result_available']})
 assert not any(z['N'] in news and (z['result_available'] or z['status']=='reserved') for z in near);screens.append({'asset':asset,'base_fp':fp,'new_N':news,'fixed_rule_matches':near})
a.update(complete_economic_screens=screens,ignored_nonfinancial_context_lineage_and_derived_fields=sorted(excluded),no_new_calculations=True);put(R/'sizing_reference_availability.json',a);put(R/'capital_screen_coupled_ratio_review.json',{'passed':True,'complete_registry_records_compared':len(rs),'screens':screens,'new_local_allocations_absent':True,'no_market_evaluations':True});print('PASS BTC750/1750 andETH4250/3250new under full coupled rules;center1250/3750 banks andparentsreadonly')
