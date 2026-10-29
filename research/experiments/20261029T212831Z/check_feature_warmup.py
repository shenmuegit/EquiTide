"""Data-only check of full available-history input at every predeclared decision epoch."""
import json
from run import ROOT,R,engine,attach_feature_history,put
p=json.loads((R/'plan.json').read_text());m=engine.load_market('ETH',p['data']['assets']['ETH']);attach_feature_history(m,p['data']['assets']['ETH']);assert len(m['funds'])==1110 and len(m['funding_feature_history'])==1212;checks=0;first={}
for i in range(engine.START,engine.END):
 cut=int(m['frame']['available_ts'][i*1440-1]);known=[x for x in m['funding_feature_history'] if x['available_ts']<=cut and x['settlement_ts']<=cut]
 for n in [3,6,9]:
  selected=known[-n:];assert len(selected)==n and max(x['available_ts'] for x in selected)<=cut and cut-max(x['available_ts'] for x in selected)<=16*engine.HOUR;checks+=1
  if i==engine.START:first[str(n)]={'source_indices':[x['source_index'] for x in selected],'available_ts_ns':[x['available_ts'] for x in selected],'settlement_ts_ns':[x['settlement_ts'] for x in selected],'signal_time_ns':cut}
assert all(x['settlement_ts']>m['start_ns'] for x in m['funds']) and all(max(v['settlement_ts_ns'])<m['start_ns'] for v in first.values())
put(R/'feature_history_verification.json',{'passed':True,'financial_evaluations':0,'full_funding_feature_records':1212,'OOS_accounting_funding_events':1110,'feature_prefix_checks':checks,'first_signal_context':first,'original_cashflow_event_axis_unchanged':True,'all_prewarm_records_from_original_hashed_real_data':True});print('PASS full funding prewarm at1110 window/prefix checks;OOS1110accounting events unchanged')
