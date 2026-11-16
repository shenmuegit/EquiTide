"""Declare an exact completed-price-path gate before looking at any new returns."""
import ast,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];P=ROOT/'research/experiments/20261116T040504Z';sys.path.insert(0,str(R));from common import *
assert not any((R/n).exists() for n in ['plan.json','batch.json','report.json','code_binding_before_evaluation.json'])
def edit(name,pairs):
 p=R/name;s=p.read_text()
 for a,b in pairs:
  assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);p.write_text(s)
old="raw,r=btc.target(m['closes'],i,int(p['lookback_days']),float(p['return_hurdle']),actual,float(p['exit_buffer_fraction']));sigma=btc_entry_sigma(m['closes'],i,V);wanted=entry_filter(raw,actual,sigma,cap)"
new="raw,r=btc.target(m['closes'],i,int(p['lookback_days']),float(p['return_hurdle']),actual,float(p['exit_buffer_fraction']));sigma=btc_entry_sigma(m['closes'],i,V);before_efficiency=entry_filter(raw,actual,sigma,cap)\n  from fractions import Fraction as F\n  floor=F(str(p.get('entry_path_efficiency_floor',0)));efficiency=btc_path_efficiency(m['closes'],i,int(p['lookback_days']));wanted=efficiency_filter(before_efficiency,actual,efficiency,floor)\n  if floor:assert p['entry_path_efficiency_window_days']==p['lookback_days']==29 and p['entry_path_efficiency_estimator']=='absolute_net_price_displacement_over_sum_absolute_daily_price_changes' and p['entry_path_efficiency_gate_scope']=='new_or_reversed_position_only'"
edit('engine.py',[(old,new),("'entry_volatility_gate_scope':'new_or_reversed_position_only'}","'entry_volatility_gate_scope':'new_or_reversed_position_only','raw_desired_before_efficiency_filter':before_efficiency,'entry_path_efficiency_exact':str(efficiency),'entry_path_efficiency_floor':str(floor),'entry_path_efficiency_applied':bool(before_efficiency and before_efficiency!=actual)}")])
p=R/'engine.py';s=p.read_text();at=s.index('\ndef latest_funding(');s=s[:at]+'''
def btc_path_efficiency(closes,i,window):
 from fractions import Fraction as F
 assert window==29 and i-window-1>=0
 path=sum((abs(F(closes[j])-F(closes[j-1])) for j in range(i-window,i)),F(0))
 return abs(F(closes[i-1])-F(closes[i-window-1]))/path if path else F(0)

def efficiency_filter(raw,actual,ratio,floor):
 return 0 if raw and raw!=actual and ratio<floor else raw

'''+s[at:];ast.parse(s);p.write_text(s)
# Independently derive net displacement by telescoping the signed increments.
old="wanted=0 if raw and raw!=actual and sigma>cap else raw\n   assert audit['kind']=='BTC_momentum_entry_vol'"
new="wanted=0 if raw and raw!=actual and sigma>cap else raw\n   if p.get('entry_path_efficiency_floor',0):\n    steps=[F(m['closes'][j])-F(m['closes'][j-1]) for j in range(i-L,i)];distance=sum(map(abs,steps),F(0));ratio=abs(sum(steps,F(0)))/distance if distance else F(0);floor=F(str(p['entry_path_efficiency_floor']));before_efficiency=wanted;wanted=0 if before_efficiency and before_efficiency!=actual and ratio<floor else before_efficiency\n    assert p['entry_path_efficiency_window_days']==L==29 and p['entry_path_efficiency_gate_scope']=='new_or_reversed_position_only' and p['entry_path_efficiency_estimator']=='absolute_net_price_displacement_over_sum_absolute_daily_price_changes' and audit['raw_desired_before_efficiency_filter']==before_efficiency and F(audit['entry_path_efficiency_exact'])==ratio and F(audit['entry_path_efficiency_floor'])==floor and audit['entry_path_efficiency_applied']==bool(before_efficiency and before_efficiency!=actual)\n   assert audit['kind']=='BTC_momentum_entry_vol'"
edit('audit.py',[(old,new),('BTC_ENTRY_VOL_CAP','BTC_PATH_EFFICIENCY_FLOOR')])
for name in ['run.py','exports.py']:edit(name,[('BTC_ADVERSE_BLEND','BTC_PATH_EFFICIENCY_FLOOR')])
edit('exports.py',[('BTC adverse-risk blend gamma','BTC close-path efficiency floor'),("['0 (old)','0.25','0.50']","['0 (old)','0.125','0.250']"),('Preregistered BTC directional adverse-risk blend','Preregistered BTC completed-price-path efficiency')])
edit('parent_units.py',[("g['W']==.25","g['W']==.125")])
edit('commands.py',[("['freeze_blend.py']","['freeze_efficiency.py']")])
for name in ['review/diagnostics.py','review/visual_review.py']:
 p=R/name;s=p.read_text().replace('BTC_adverse_volatility_blend','BTC_path_efficiency_floor').replace('gamma0','efficiency0').replace('[.25,.5]','[.125,.25]').replace('{0,.25,.5}','{0,.125,.25}').replace('[0,.5]','[0,.25]').replace('three BTC gamma values','three BTC efficiency floors').replace('old gamma0','old efficiency0').replace('actual BTC directional adverse-risk trade changes','actual BTC price-path efficiency trade changes');ast.parse(s);p.write_text(s)
# Create the new spec source from the prior workflow, replacing its entire signal and hypothesis.
s=(P/'freeze_blend.py').read_text().replace('20261116T020401Z','20261116T040504Z');s=s.replace('GAMMAS','FLOORS').replace('gamma','floor').replace('Gamma','Floor').replace('GAMMA','FLOOR');s=s.replace('FLOORS=[0,.25,.5];NEW=[.25,.5]','FLOORS=[0,.125,.25];NEW=[.125,.25]')
s=s.replace('AdverseBlend','PathEfficiency').replace('adverse-risk-blend','price-path-efficiency').replace('adverse-risk-eth','price-path-efficiency-eth')
start=s.index("rules=copy.deepcopy(old['rules']);rules['signal']=");end=s.index('\nfor floor in NEW:',start)
descriptor='BTC completedROC L29/strictentryH.03/fixedexitE.005/V10samplelogvolCap.0275/pathEfficiencyFloor[0,.125,.25]. Entry priority ROC>H long,ROC<-H short;otherwise actual long retained only ROC>-.005,actual short only ROC<.005,equality exits,retain actual q. On completed29 daily price increments delta:ER=abs(close_last-close_29back)/sum(abs(delta)),zero path ER0;new/reversed entry requires prior V10 sample logvol<=.0275 then exact ER>=floor. Floor0 old total-risk bank reused readonly. ETH readonly longonly L5/H.02/E.0075,finiteEWMS16beta15/17,D3K.0075,V6cap.05625,M4mature1to36h signed actual funding median;budgetmin(.0002,R*pastV8samplelogvol*latesteligiblepastactualintervalhours/24),R[.00875,.01]. No fit,labels or future values. Execution impact uses unchanged past20 total sample logvol.'
s=s[:start]+"rules=copy.deepcopy(old['rules']);rules['signal']="+repr(descriptor)+s[end:]
s=s.replace("entry_volatility_estimator='directional_adverse_RMS_blend',entry_adverse_volatility_blend=floor,entry_adverse_volatility_target_logreturn=0,entry_adverse_volatility_denominator='population_n'","entry_path_efficiency_estimator='absolute_net_price_displacement_over_sum_absolute_daily_price_changes',entry_path_efficiency_window_days=29,entry_path_efficiency_floor=floor,entry_path_efficiency_gate_scope='new_or_reversed_position_only'")
s=s.replace('BTC_ADVERSE_BLEND','BTC_PATH_EFFICIENCY_FLOOR').replace('==(.25,.01)','==(.125,.01)').replace("'W':.25,'K':.01","'W':.125,'K':.01")
a=s.index('hypothesis=');b=s.index(',rules=rules',a);s=s[:a]+"hypothesis="+repr('Hypothesis: a minimum completed29day absolute net price displacement / total absolute price-path length may avoid choppy momentum entries but miss reversals or reduce diversification. Floors[0,.125,.25] x readonly ETH R[.00875,.01]. BTC L29/H.03/E.005/V10/cap.0275/C3750/N1000 and all costs fixed. Floor0 exact old total-risk bank readonly;representative floor.125/R.01 fixed before outcomes,no after-result extension or reselection.')+s[b:]
a=s.index("axis_semantics=");b=s.index(',grid=grid',a);s=s[:a]+"axis_semantics="+repr({'W':'BTC completed29day price-path efficiency floor0/.125/.25;ER=abs(net displacement)/sum(abs(daily changes)),zero path0,strict below blocks new/reversed only;sampleV10cap.0275/L29/H.03/E.005 fixed;0 old actual readonly','K':'ETH budget ratio .00875/.01 to completed V8samplelogvol,actual past interval,M4 fixed'})+s[b:]
s=s.replace('own_adverse_blend_axis','own_path_efficiency_floor_axis').replace('Three BTC blend values','Three BTC efficiency floors').replace('floor0 at lower boundary','floor0 at lower boundary')
a=s.index("'novelty':");b=s.index('})',a);s=s[:a]+"'novelty':"+repr('New exact completed29day path-efficiency floors.125/.25 after unchanged total-vol entry gate,not renaming or number-format variants;old floor0 and ETH banks readonly.')+s[b:]
s=s.replace('Directional adverse RMS blend','Completed price-path efficiency').replace('directional adverse-risk mechanism','completed price-path efficiency mechanism');ast.parse(s);(R/'freeze_efficiency.py').write_text(s)
# Bind only the intended BTC entry policy change; simulate, costs, funding and ETH remain exact.
s=(P/'definitions.py').read_text().replace('20261116T020401Z','20261116T040504Z');a=s.index('\nfuns=lambda');b=s.index('\nassert len(batch)',a)
s=s[:a]+'''
funs=lambda f:{x.name:ast.dump(x,include_attributes=False) for x in ast.parse(f.read_text()).body if isinstance(x,ast.FunctionDef)}
before,after=funs(P/'engine.py'),funs(R/'engine.py');assert set(after)-set(before)=={'btc_path_efficiency','efficiency_filter'} and set(before)-set(after)=={'btc_directional_risk'} and all(before[k]==after[k] for k in set(before)&set(after) if k!='base_decide')
oldbase=next(x for x in ast.parse((P/'engine.py').read_text()).body if isinstance(x,ast.FunctionDef) and x.name=='base_decide');newbase=next(x for x in ast.parse((R/'engine.py').read_text()).body if isinstance(x,ast.FunctionDef) and x.name=='base_decide')
assert len(oldbase.body)==len(newbase.body) and all(ast.dump(x,include_attributes=False)==ast.dump(y,include_attributes=False) for x,y in zip(oldbase.body[3:],newbase.body[3:]))
assert sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py')
'''+s[b:]
s=s.replace("q['entry_adverse_volatility_blend'] in [.25,.5]","q['entry_path_efficiency_floor'] in [.125,.25] and q['entry_path_efficiency_window_days']==29")
s=s.replace("descriptor.startswith('BTC completedROC L29/strictentryH.03/fixedexitE.005/V10directionalAdverseBlend[0,.25,.5]/cap.0275.')","descriptor.startswith('BTC completedROC L29/strictentryH.03/fixedexitE.005/V10samplelogvolCap.0275/pathEfficiencyFloor[0,.125,.25].')")
s=s.replace("['parameters']['entry_adverse_volatility_blend']==z['W']","['parameters']['entry_path_efficiency_floor']==z['W']").replace("'native_blends':[.25,.5],'old_blend_readonly':0","'native_efficiency_floors':[.125,.25],'old_floor_readonly':0").replace('BTC directional adverse-risk formula','BTC exact price-path efficiency filter');ast.parse(s);(R/'definitions.py').write_text(s)
put(R/'primary_source_reads_current.json',{'round':R.name,'observed_reads_recorded_utc':now(),'reads':[{'url':u,'web_reference':w,'access_UTC_date':'2026-11-16','read_success':True} for u,w in [('https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data','turn292view0'),('https://github.com/binance/binance-public-data/blob/master/README.md','turn292view1')]],'tool_timeouts':0,'HTTP_capture_timestamp_not_claimed':True})
put(R/'stdout_label_notes.json',{'round':R.name,'notes':[],'current_scalar_and_window_labels_checked_before_binding':True,'old_round_raw_logs_and_errata_preserved':True,'financial_or_account_reruns':0})
(R/'research_work_plan.md').write_text('本轮仅新研究BTC完成29日价格路径效率门槛：ER=abs(首尾价格位移)/sum(abs(逐日价格变化))，分母0时0；floor0/.125/.25，旧0只读、新两档与只读ETH R.00875/.01形成四父；代表floor.125/R.01。固定BTC L29/H.03/E.005、V10总样本logvol上限.0275、本金3750/名义1000；ETH15000/4000，raw[1,1]不归一化。六新配置先reserve再完整391日、逐折/敏感性/三成本/连续NAV核验并finish，全部正负保留。\n\n原账户SMA/single20:30→22:30，L4/FEWM22:10→Nov16_00:10跨原00:01日决策；实际结算由完整公共GET确认后按各自持仓记一次，原日线partial累加到1440后独立核对。下一轮SMA/single22:30→00:30跨日，L4/FEWM00:10→02:10不跨日；各保留现金/仓位/desired/规则及完整链，不采用新研究参数。\n\n锁内检查/只读snapshot并main提交push，核验远端后解锁；不下真实订单、不委派、不建分支或定时任务。\n')
print('PASS exact BTC close-path efficiency mechanism and floor0/.125/.25 x ETH R axes configured before first reservation')
