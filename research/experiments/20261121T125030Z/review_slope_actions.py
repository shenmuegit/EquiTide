"""Compare saved new slope-gate decisions with matched old K.0075;no market/model execution."""
import gzip,json
from fractions import Fraction as F
from decimal import Decimal as D
from common import *
rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');r=rd(R/'report.json');rh=sha(R/'report.json');rows=[];totals={'saved_decision_pairs':0,'identical_completed_fast_ROC_and_slope':0,'strict_slope_gate_differences':0,'final_desired_differences':0,'position_state_differences':0,'same_allcost_native_paths':0}
for c in r['configs'].values():
 if c['scope']!='native':continue
 base=next(g for g in p['native_grid'] if g['W']==.0075 and g['K']==c['K']);ref=p['read_only_references'][base['fingerprint']];old=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()));new=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));assert sha(ROOT/ref['archive'])==ref['archive_sha256'];counts={k:0 for k in totals if k!='same_allcost_native_paths'};same=True
 for k,z in new['scenes'].items():
  oz=old['scenes'][k];same &= z['summary']['NAV_sha256_f64le']==oz['summary']['NAV_sha256_f64le'];assert len(z['decisions'])==len(oz['decisions'])==391
  for a,b in zip(z['decisions'],oz['decisions']):
   aa,bb=a['policy_audit'],b['policy_audit'];slope=F(aa['slow_distance_exact']);assert a['signal_available_ts_ns']==b['signal_available_ts_ns'] and slope==F(bb['slow_distance_exact']) and F(aa['return_exact'])==F(bb['return_exact']) and aa['slope_hurdle_fraction']==c['W'] and bb['slope_hurdle_fraction']==.0075 and aa['long_entry_return_hurdle']==bb['long_entry_return_hurdle']==.02;expected=lambda h:1 if slope>F(str(h)) else -1 if slope<-F(str(h)) else 0;assert aa['slowgate_direction']==expected(c['W']) and bb['slowgate_direction']==expected(.0075);counts['saved_decision_pairs']+=1;counts['identical_completed_fast_ROC_and_slope']+=1;counts['strict_slope_gate_differences']+=aa['slowgate_direction']!=bb['slowgate_direction'];counts['final_desired_differences']+=a['desired_direction']!=b['desired_direction'];counts['position_state_differences']+=D(a['state_before']['signed_units'])!=D(b['state_before']['signed_units'])
 for key,n in counts.items():totals[key]+=n
 totals['same_allcost_native_paths']+=int(same);rows.append({'fingerprint':c['fingerprint'],'slopeK':c['W'],'M':c['K'],'old_fingerprint':base['fingerprint'],**counts,'same_allcost_path':bool(same)})
assert len(rows)==6 and totals['saved_decision_pairs']==7038 and sha(R/'report.json')==rh;put(R/'slope_action_comparison.json',{'passed':True,'recorded_utc':now(),'financial_report_sha256_unchanged':rh,'rows':rows,**totals,'no_model_or_account_or_market_execution':True});print(json.dumps({'passed':True,**totals}))
