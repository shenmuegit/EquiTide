"""Definition-only numeric parent lookup; no NAV/result statistics calculated."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');prior=json.loads((ROOT/'research/experiments/20261112T073021Z/plan.json').read_text());btc={v:next(z['fingerprint'] for z in prior['native_grid'] if z['V']==v and z['CAP']==.03) for v in [6,10,14]};eth={.00875:'d2188e34f6d96f2205823e74b834003e1b5d5dd8c2994f0ccd8b72062fed4a53',.01:'ee5d9cea8f250a0b6151bf8d6ff7824ce472dc557265589594b200f0110de0f9',.01125:'00093933f37c94a2df842d4ed7efdd45fa293bfa5085a52fd33bacbd5a500eea'};rows=[]
for V,b in btc.items():
 p=rs[b]['spec']['parameters'];assert rs[b]['result_available'] and p['entry_volatility_window_days']==V and p['entry_volatility_ceiling']==.03 and p['fixed_entry_notional_usdt']==1000 and p['initial_capital_usdt']==3750
 for ratio,e in eth.items():
  p=rs[e]['spec']['parameters'];assert rs[e]['result_available'] and p['entry_funding_volatility_ratio']==ratio and p['entry_funding_budget_volatility_window_days']==8 and p['fixed_entry_notional_usdt']==4000 and p['initial_capital_usdt']==15000
  matches=[]
  for fp,z in rs.items():
   s=z.get('spec',{});cs=s.get('components',[])
   if s.get('kind')=='combination' and len(cs)==2 and sorted((c['fingerprint'],float(c['weight'])) for c in cs)==sorted([(b,1.),(e,1.)]):assert z['result_available'];matches.append(fp)
  rows.append({'BTC_V':V,'ETH_R':ratio,'sources':[b,e],'existing_parent_matches':matches})
put(R/'predeclared_parent_grid_inventory.json',{'recorded_utc':now(),'economic_hypothesis':'Cross fixed3percent BTCnewentryvolatilitygate horizon6/10/14 withETHfinancingbudgetratio.00875/.01/.01125,inspect jointdevelopmentrisk/recentrobustness. ExactwholebanksC3750/15000,N1000/4000,raw1/1,no resizing/transfers. PriorBTC6/14gatepathscoincided andfewblockedentries;newpairsarenotindependentalphaproof. Do not densify volcap after seeing outcomes.','fixed_BTC_L_H_E':[29,.03,.01],'fixed_BTC_volcap':.03,'fixed_ETH_rules':'L5/H.02/E.0075,S16beta15/17,D3K.0075,new/reversedonly,V6cap.05625,VW8/M4actualintervalfundbudget','candidate_axes':{'BTC_V':[6,10,14],'ETH_R':[.00875,.01,.01125]},'planned_representative':{'BTC_V':10,'ETH_R':.01},'rows':rows,'old_native_quantity_or_policy_runs_planned':0,'financial_or_NAV_calculations_done':0,'registry_IDs_read':len(rs)});print('PASS plannedold/new',sum(bool(x['existing_parent_matches']) for x in rows),sum(not x['existing_parent_matches'] for x in rows))
