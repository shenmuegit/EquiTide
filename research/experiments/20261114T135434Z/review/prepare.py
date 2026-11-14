"""Adapt existing validated sources to the preregistered funding-median count study."""
from pathlib import Path
import ast,json,subprocess
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2]
def edit(n,pairs):
 p=R/n;s=p.read_text()
 for a,b in pairs:
  assert a in s,(n,a);s=s.replace(a,b)
 ast.parse(s);p.write_text(s)
for n in ['run.py','audit.py','exports.py']:edit(n,[('ETH_BUDGET_VOL_WINDOW_DAYS','ETH_FUNDING_MEDIAN_COUNT')])
edit('freeze.py',[
 ('Predeclare ETH budget-volatility windows','Predeclare ETH funding-median settlement counts'),
 ('M4signedmature1to36hfundmedian','M in[2,3,4] signedmature1to36hfundmedian'),
 ('sampledailylogvolVW*latesteligibleactualpastintervalhours/24),VW in[8,10,12]','sampledailylogvolV8*latesteligibleactualpastintervalhours/24),VW fixed8'),
 ('bs={.03:reuse(B0,.03,8),.035:reuse(B1,.035,8)};es={8:reuse(E0,.03,8)}','bs={.03:reuse(B0,.03,4),.035:reuse(B1,.035,4)};es={4:reuse(E0,.03,4)}'),
 ('VW','M'),('for M in [10,12]:','for M in [2,3]:'),
 ("ETH_budgetM{M}_R0p01_391d","ETH_fundM{M}_V8_R0p01_391d"),
 ('eth-funding-budget-volatility-window-neighborhood','eth-mature-funding-median-count-neighborhood'),
 ("sp['parameters']['entry_funding_budget_volatility_window_days']=M","sp['parameters']['entry_funding_settlement_count']=M"),
 ('[8,10,12]','[2,3,4]'),('if M==8:','if M==4:'),
 ('ETHM{M}_R0p01_391d','ETHM{M}_V8_R0p01_391d'),
 ('btc-threshold-eth-budget-window-bank-combination','btc-threshold-eth-funding-median-bank-combination'),
 ("==(.03,12)","==(.03,3)"),("'K':12","'K':3"),
 ('Does smoothing the ETH funding-budget volatility estimate over8/10/12 completed days alter carry-entry selection without creating an isolated performance peak? Fixed ratio.01, crossed with already-completed BTC H.03/H.035 banks. Preset H.03/M12 before outcomes. Existing8dayETH,2BTC,2centerparents,matchedholds readonly.','Does a median of2/3 rather than4 mature actual funding settlements respond faster without robustness loss? BudgetV8 and ratio.01 fixed; cross readonly BTC H.03/H.035. Preset H.03/M3 before outcomes. ExistingM4ETH,2BTC,2M4parents,matchedholds readonly.'),
 ('ETH_BUDGET_VOL_WINDOW_DAYS','ETH_FUNDING_MEDIAN_COUNT'),
 ('ETH completed daily samplelogvol lookback for funding budget;ratio.01,entryV6cap.05625 fixed','ETH count of latest mature1to36h signed actual funding settlements;median even counts average middle pair;budgetV8/ratio.01 fixed'),
 ('ETH_native_only_own_budget_window_axis','ETH_native_only_own_median_count_axis'),
 ('ETH funding-budget volatility windows10/12 are new exact391day definitions','ETH funding-median settlement counts2/3 are new exact391day definitions'),
 ('2BTCx3ETHwindow surface','2BTCx3ETHmedian surface')])
edit('definitions.py',[("q['entry_funding_budget_volatility_window_days'] in [10,12]","q['entry_funding_settlement_count'] in [2,3] and q['entry_funding_budget_volatility_window_days']==8")])
edit('parent_units.py',[("g['K']==10","g['K']==3")])
p=R/'parent_units.py';s=p.read_text();i=s.index("put(R/'parent_primitive_verification.json'");s=s[:i]+'''# Synthetic mature-prefix medians: exact even/odd rules, age boundaries and future exclusion.
signal=50*HOUR
base=[{'settlement_ts':signal-age*HOUR,'available_ts':signal-(age-1)*HOUR,'realized_rate':core.D(rate),'source_index':j+1,'entry_interval_hours':core.D(8)} for j,(age,rate) in enumerate([(1,'.0001'),(9,'.0004'),(17,'-.0002'),(25,'.0003')])]
for count,expected in [(2,'.00025'),(3,'.0001'),(4,'.0002')]:
 out=engine.median_funding(base,signal,count);assert out['median_rate']==core.D(expected) and out['count']==count
 future={'settlement_ts':signal+HOUR,'available_ts':signal+2*HOUR,'realized_rate':core.D(999),'source_index':99}
 immature={'settlement_ts':signal-HOUR+1,'available_ts':signal,'realized_rate':core.D(999),'source_index':98}
 stale={'settlement_ts':signal-36*HOUR-1,'available_ts':signal,'realized_rate':core.D(999),'source_index':97}
 assert engine.median_funding(base+[future,immature,stale],signal,count)==out
 assert engine.median_funding(base[:count-1],signal,count) is None
edge=[{**base[0],'settlement_ts':signal-HOUR},{**base[1],'settlement_ts':signal-36*HOUR}];assert engine.median_funding(edge,signal,2) is not None
assert engine.median_funding([{**edge[0],'available_ts':signal+1},edge[1]],signal,2) is None
''' +s[i:];ast.parse(s);p.write_text(s)
edit('exports.py',[("ETH funding-budget volatility window (days)","ETH mature funding settlements in median"),("['8','10','12']","['2','3','4']"),('ETH carry-budget volatility window','ETH mature-funding median count')])
for n in ['observe_fewm.py']:
 edit(n,[('1698571','1726860')])
edit('checks.py',[("assert win['candidate']['expected_funding_by_asset']==fresh['public_fields_by_asset'] and all(win[a]['expected_funding_by_asset']=={'BTC':[],'ETH':[]} for a in ['l4h02','fewm']) and [win[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']]==[0,6,0,0] and len(cashflows)==6","assert all(win[a]['expected_funding_by_asset']=={'BTC':[],'ETH':[]} for a in ['SMA','candidate','l4h02','fewm']) and not cashflows and all(not xs for xs in fresh['public_fields_by_asset'].values())"),('singleactual08plus1ms6owncashflows, L4/FEWM0new;all3once','all4marks0currentfunds,no newdaily/fills;all3prior08once')])
edit('publish.py',[('test ETH budget windows with reused BTC banks','test ETH funding medians with reused BTC banks')])
edit('finalize.py',[(", 'formatter_syntax_verification.json'",''),('validate_sources_retry1.py','validate_sources.py'),("{'SMA':0,'candidate':6,'l4h02':0,'fewm':0}","{'SMA':0,'candidate':0,'l4h02':0,'fewm':0}"),("['2026-11-14T08:30:00Z','2026-11-14T10:30:00Z']","['2026-11-14T10:30:00Z','2026-11-14T12:30:00Z']"),("['2026-11-14T10:10:00Z','2026-11-14T12:10:00Z']","['2026-11-14T12:10:00Z','2026-11-14T14:10:00Z']")])
# Setup uses actual empty current union and retains the original08 capture with its original UTC.
p=R/'review/setup.py';s=p.read_text();start=s.index("fresh=json.loads");end=s.index("for n in ['funding00_nov13",start)
s=s[:start]+'''fresh=json.loads((R/'window_funding_preflight.json').read_text());orig=json.loads((P/'funding00_nov14_preflight.json').read_text());assert fresh['passed'] and all(not xs for xs in fresh['public_fields_by_asset'].values());(R/'funding08_nov14_preflight.json').write_bytes((P/'funding08_nov14_preflight.json').read_bytes());original08=json.loads((R/'funding08_nov14_preflight.json').read_text());assert all(len(xs)==1 and xs[0]['fundingTime']==1794643200001 for xs in original08['public_fields_by_asset'].values());put(R/'funding08_prebinding_verification.json',{'passed':True,'recorded_utc':now(),'actual_settlement_ns':1794643200001000000,'source':rel(R/'funding08_nov14_preflight.json'),'sha256':sha(R/'funding08_nov14_preflight.json'),'original_public_capture_UTC':original08['recorded_utc'],'fresh_public_capture_UTC':fresh['recorded_utc'],'current_window_empty_separate_from_original08_capture':True,'all3_prior_accounts08_already_once':True,'no_account_or_financial_calculation':True})
''' +s[end:]
s=s.replace("'fresh_current_window_fields_empty':False","'fresh_current_window_fields_empty':True").replace("{'SMA':0,'candidate':6,'l4h02':0,'fewm':0}","{'SMA':0,'candidate':0,'l4h02':0,'fewm':0}")
s=s.replace("'2026-11-14T06:30:00Z','2026-11-14T08:30:00Z'","'2026-11-14T08:30:00Z','2026-11-14T10:30:00Z'").replace("'2026-11-14T08:10:00Z','2026-11-14T10:10:00Z'","'2026-11-14T10:10:00Z','2026-11-14T12:10:00Z'").replace('[0,6,0,0]','[0,0,0,0]').replace('1698571','1726860').replace('Single currentwindow includes actual08plus1ms and books ownq/cash once; L4/FEWM alreadybooked08 do not repeat.','All3perp alreadybooked08 once;currentclosedwindowsmarks/risk only,allcurrentfunding0.').replace('fund0/6/0/0actual08plus1ms','fund0/0/0/0prior08preserved')
ast.parse(s);p.write_text(s)
# Read-only source syntax gate has no inherited old error dependency.
p=R/'review/validate_sources.py';s=p.read_text().replace('after the actual pre-execution formatter error','for this round before sealing').replace(" and json.loads((R/'formatter_syntax_verification.json').read_text())['passed']",'');ast.parse(s);p.write_text(s)
# Diagnostics compare actual count variants to the immutable M4 reference.
edit('review/diagnostics.py',[("center=eth[8]","center=eth[4]"),('for VW in [10,12]:','for VW in [2,3]:'),("'ETH_budget_window'","'ETH_funding_median_count'"),('vs_old_VW8','vs_old_M4'),("c['K']==8","c['K']==4"),("[8,12]","[2,4]"),('ETH_window_axis_boundary','ETH_median_axis_boundary'),('matched_VW8','matched_M4'),('ETH funding-budget trade changes','ETH funding-median trade changes')])
for p in R.rglob('*.py'):ast.parse(p.read_text())
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();previous=json.loads((ROOT/'.git/automation_proofs/20261114T115333Z.json').read_text());assert previous['status']=='completed_published_verified_unlocked' and previous['final_main_commit']=='1dcd10bf484a614f03a7f884f9f91301b7b01a9c'
(R/'startup.json').write_text(json.dumps({'round':R.name,'trigger_utc':'2026-11-14T13:54:34.634Z','base_commit':head,'branch_lock_broker_pid':1726860,'branch_lock_session':45920,'branch_lock_native_start_chunk':'ac3d63','root_native_verification_chunk':'a6d78d','initial_fetch_native_start_chunk':'363d5d','initial_fetch_native_completion_chunk':'e5fbdb','initial_fetch_native_session':51271,'initial_sync_no_merge_required':True,'only_preexisting_untracked':'data/normalized','previous_round_publication_verified':previous['status'],'previous_final_main_commit':previous['final_main_commit']},indent=2)+'\n')
print('PASS prepared current2/3/4fundmedian ETH study,readonly BTC,all4closedmarks,currentfunds0;0financialcalculations')
