"""Predetermine adjacent4/6-day variants around actual5-day center;no returns calculated."""
import ast,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261116T080637Z';sys.path.insert(0,str(R));from common import *
assert not (R/'plan.json').exists()
def edit(n,pairs):
 f=R/n;s=f.read_text()
 for a,b in pairs:assert a in s,(n,a);s=s.replace(a,b)
 ast.parse(s);f.write_text(s)
for n in ['engine.py','audit.py']:
 edit(n,[("[3,5]","[3,4,5,6]")]+([('[0,3,5]','[0,3,4,5,6]')] if n=='engine.py' else []))
edit('freeze_confirmation.py',[
 ('HORIZONS=[0,3,5];NEW=[3,5]','HORIZONS=[4,5,6];NEW=[4,6]'),
 ("078ecce7a424462c86b0559ffae47e176f267d2841790565d4f092976bd88797","4820334331e1c14d0a37fcea1453968338ab94aaa9e4a77db68a8289d310a928"),
 ('dda0521e94bd136aadf60ea7a5ea011854a281dd5579559a21e7cb28d6cee36b','c0d773a597a5c71aab595dc396bf9aae25c495b697e42f932764ee3d84f66a35'),
 ('6c3e417f232a5eba7a7d44074d0415c085c283c49993f7a497d460c5222c24f0','e590cbde5788abceeccf4251ba3a2fc3d6ecef7eb4361cfa57bea40c25db3116'),
 ('bs={0:reuse(B,0,.01)}','bs={5:reuse(B,5,.01)}'),('if horizon==0:','if horizon==5:'),
 ('[0,3,5]','[4,5,6]'),('W3or5','W4or6,withW5readonly'),('W0 disables gate and is exact old readonly bank','W5 is the exact old confirmed readonly bank'),
 ('strict 3/5 completed-day momentum','strict 4/6 completed-day momentum around the existing 5-day bank'),('W0 old exact total-risk bank readonly','W5 old exact confirmed bank readonly'),('RepresentativeW3/R.01','RepresentativeW4/R.01'),
 ('==(3,.01)','==(4,.01)'),("'W':3,'K':.01","'W':4,'K':.01"),('horizon0/3/5','horizon4/5/6'),('W0 exact old readonly disabled gate','W5 exact old confirmed readonly bank'),
 ('horizon0 at lower boundary','horizon5 is the readonly center'),('Strict completed3/5day','Strict completed4/6day'),('W0/ETH banks readonly','W5/ETH banks readonly'),('strict3/5day','strict4/6day')])
edit('parent_units.py',[("g['W']==3","g['W']==5")])
edit('exports.py',[("['0 (off, old)','3 days','5 days']","['4 days','5 days (old)','6 days']")])
f=R/'definitions.py';s=f.read_text();a=s.index('\nfuns=lambda');b=s.index('\nassert len(batch)',a)
s=s[:a]+'''
class NormalizeAllowedHorizons(ast.NodeTransformer):
 def visit_List(self,node):
  self.generic_visit(node)
  if all(isinstance(x,ast.Constant) for x in node.elts) and [x.value for x in node.elts] in [[3,5],[3,4,5,6]]:node.elts=[ast.Constant(3),ast.Constant(5)]
  if all(isinstance(x,ast.Constant) for x in node.elts) and [x.value for x in node.elts] in [[0,3,5],[0,3,4,5,6]]:node.elts=[ast.Constant(0),ast.Constant(3),ast.Constant(5)]
  return node
normalize=lambda f:ast.dump(NormalizeAllowedHorizons().visit(ast.parse(f.read_text())),include_attributes=False)
assert normalize(P/'engine.py')==normalize(R/'engine.py') and sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py')
''' +s[b:];s=s.replace("q['entry_directional_confirmation_lookback_days'] in [3,5]","q['entry_directional_confirmation_lookback_days'] in [4,6]").replace('[0,3,5]','[4,5,6]').replace("'native_confirmation_periods':[3,5],'old_disabled_gate_readonly':0","'native_confirmation_periods':[4,6],'old_confirmed_bank_readonly':5").replace('BTC_entry_risk_policy_intentionally_changed\':True','BTC_entry_risk_policy_intentionally_changed\':False').replace('BTC strict recent-direction confirmation filter bound','BTC adjacent4/6 confirmations bound;onlyallowlist expanded');ast.parse(s);f.write_text(s)
edit('review/prepare_confirmation.py',[("in [3,5] and (z['result_available']","in [4,6] and (z['result_available']"),('for W in [0,3,5]','for W in [0,4,5,6]'),("'new_confirmation_days':[3,5]","'new_confirmation_days':[4,6]"),('completed3/5day','completed4/6day'),('previous path-efficiency gate not used','same strict recent-direction formula,onlypredeclared4/6allowlist added'),('W0 old bank readonly','W5 actualoldbank readonly;W0 syntheticdisabled equivalence only')])
for n in ['review/diagnostics.py','review/visual_review.py']:
 f=R/n;s=f.read_text().replace('btc[0]','btc[5]').replace('for V in [3,5]','for V in [4,6]').replace("c['W']==0","c['W']==5").replace("best['W'] in [0,5]","best['W'] in [4,6]").replace('confirmation0','confirmation5').replace('{0,3,5}','{4,5,6}').replace('==[3,5]','==[4,6]').replace("lookback_days']==0","lookback_days']==5").replace('old confirmation5 reference at the lower boundary','old confirmation5 reference at the center');ast.parse(s);f.write_text(s)
for name in ['forward.py','forward_registry.py','audit_forward.py']:
 s=(ROOT/'research/experiments/20261116T060605Z'/name).read_text().replace('20261116T040504Z','20261116T080637Z').replace('Nov15dailyalreadybooked','Nov16dailyalreadybooked').replace('next daily event2026-11-16UTC00:01','next daily event2026-11-17UTC00:01').replace('already completed Nov15 daily decision','already completed Nov16 daily decision');ast.parse(s);(R/name).write_text(s)
f=R/'commands.py';s=f.read_text();s='\n'.join(l for l in s.splitlines() if not l.startswith("if phase=='candidate_retry") and not l.startswith("if phase=='audit_retry"))+'\n';f.write_text(s)
put(R/'primary_source_reads_current.json',{'round':R.name,'observed_reads_recorded_utc':now(),'reads':[{'url':u,'web_reference':v,'access_UTC_date':'2026-11-16','read_success':True} for u,v in [('https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data','turn294view0'),('https://github.com/binance/binance-public-data/blob/master/README.md','turn294view1')]],'HTTP_capture_timestamp_not_claimed':True})
put(R/'stdout_label_notes.json',{'round':R.name,'notes':[],'current_scalar_and_window_labels_checked_before_binding':True,'old_round_raw_logs_and_errata_preserved':True,'financial_or_account_reruns':0})
(R/'research_work_plan.md').write_text('事前固定BTC确认W4/6新测试，W5实际旧结果只读；与ETH预算R.00875/.01联合敏感性，代表W4/R.01事前冻结。保持L29/H.03/E.005/V10cap.0275/原金额与未归一化wholebank[1,1]。新六配置逐个reserve再计算391复用开发日/逐折/连续NAV/三成本，独立审计与finish。原账户SMA/singleNov16_00:30→02:30，L4/FEWM02:10→04:10，只标记且先新查全窗实际资金费，不重复已记00及日决策。继承原SMA65与full68背景、全部账本。锁内monitor/check/main提交push与远端核验。\n')
print('PASS predeclared adjacent4/6 around5readonly,ETHbudgets,preset4/.01;unchangedmoneyformula;no financial calculations')
