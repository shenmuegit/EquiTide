"""Predeclare BTC entry thresholds with fixed early exit, plus actual16UTC account funding."""
from pathlib import Path
import ast,json,subprocess,hashlib
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2]
def edit(n,pairs):
 p=R/n;s=p.read_text()
 for a,b in pairs:assert a in s,(n,a);s=s.replace(a,b)
 ast.parse(s);p.write_text(s)
# Reuse the actual E.005/H.03 source and its two actual parents as immutable centers.
edit('freeze.py',[
 ('BTC exit persistence buffers','BTC entry thresholds with fixed early exit'),
 ('40bac3ad75e2414c7295baaa489193ae534a306660ef826edde826dea8dc9610','6d32222e05db56bb439cd76d708d291670c576aa1f30579a5bc0b8656ad1e893'),
 ('bf81331e1132b6fc12306dcc263fc28cfcf5d535abf4f459128a5a5110b738f2','a6095f34ce5ba20456c593e855262fd5f1e71863eba86a01b45d339cbdf0e311'),
 ('b2b4f0e8e56c8f01cae7a87b8fc9c02256c642e9ff881252e5beed668231aac9','5f647294c1af82ab332231c4c4d1901cb73a608f72981b771d1dfb561c188c86'),
 ('bs={.01:reuse(B,.01,.01)};es={r:reuse(c,.01,r)','bs={.03:reuse(B,.03,.01)};es={r:reuse(c,.03,r)'),
 ('for E in [.005,.015]:','for H in [.025,.035]:'),
 ("BTC_L29_H3_E{str(E).replace(\".\",\"p\")}_V14cap3_391d","BTC_L29_H{str(H).replace(\".\",\"p\")}_E0p005_V14cap3_391d"),
 ('btc-momentum-exit-buffer-neighborhood','btc-momentum-entry-threshold-earlyexit-neighborhood'),
 ("sp['parameters']['exit_buffer_fraction']=E","sp['parameters']['return_hurdle']=H"),
 ('W=E,K=.01','W=H,K=.01'),('bs[E]=row','bs[H]=row'),
 ('for E,r in itertools.product([.005,.01,.015]','for H,r in itertools.product([.025,.03,.035]'),
 ('if E==.01:row=reuse(C0 if r==.00875 else C1,E,r)','if H==.03:row=reuse(C0 if r==.00875 else C1,H,r)'),
 ('left,right=bs[E],es[r]','left,right=bs[H],es[r]'),
 ('parent_BTCE{str(E).replace(".","p")}_L29_ETHR','parent_BTCH{str(H).replace(".","p")}_E0p005_L29_ETHR'),
 ('btc-exit-buffer-eth-carry-bank-combination','btc-entry-threshold-earlyexit-eth-carry-bank-combination'),('W=E,K=r','W=H,K=r'),
 ('[bs[E] for E in [.005,.01,.015]]','[bs[H] for H in [.025,.03,.035]]'),
 ('==(.005,.01)','==(.025,.01)'),("'W':.005","'W':.025"),
 ('BTC_EXIT_BUFFER','BTC_ENTRY_HURDLE'),("[.005,.01,.015]","[.025,.03,.035]"),
 ('BTC_native_only_own_exit_axis','BTC_native_only_own_entry_axis'),
 ('ThreeBTC exitbuffers','ThreeBTC entrythresholds'),
 ('BTCexitparameterE.005/.015new391daydefinitions;E.01and2ETHbanks/centerparents readonly;not equivalent renames.','BTCentryH.025/.035withfixedE.005new391daydefinitions;H.03and2ETHbanks/centerparents readonly;not equivalent renames.'),
 ('3BTCexitx2ETHbudget','3BTCentryx2ETHbudget')])
p=R/'freeze.py';s=p.read_text();a=s.index("rules=copy.deepcopy");b=s.index('\ndef reuse',a);s=s[:a]+"rules=copy.deepcopy(old['rules']);rules['signal']='BTC strictROC L29,entryH in[.025,.03,.035],fixedexitE.005. Strict ROC>Hlong/<-Hshort entry haspriority;otherwise retainactual longwhileROC>-.005/shortwhileROC<.005,elseflat. New/reversedentryonly samplelogvolV14ceiling.03;retainq. ETH exactlongonly L5/H.02/E.0075,finiteEWMS16beta15/17,D3K.0075,V6cap.05625,M4mature1to36hfundmedian,budgetmin(.0002,R*samplelogvolV8*latesteligiblepastintervalhours/24),R[.00875,.01]. No fit/labels/futurevalues.'"+s[b:]
a=s.index("'hypothesis':");b=s.index(",'rules':rules",a);s=s[:a]+"'hypothesis':'With BTC earlyexitE.005 fixed,can fasterentryH.025 recover netreturn or stricterH.035 reduce whipsaw without losing chronological robustness? L29/V14cap.03 unchanged. H[.025,.03,.035] x readonlyETHR[.00875,.01];H.025/R.01 representative preset before outcomes. ExistingH.03E.005bank,ETHbanks/centerparents/holds readonly.'"+s[b:]
s=s.replace('BTC strict retention exit buffer fraction E;newentry H.03,L29,V14cap.03 fixed','BTC strict entry threshold H;L29/exitE.005/V14cap.03 fixed').replace('exitbuffers by2','entrythresholds by2');ast.parse(s);p.write_text(s)
for n in ['run.py','audit.py','exports.py']:edit(n,[('BTC_EXIT_BUFFER','BTC_ENTRY_HURDLE')])
edit('definitions.py',[("q['exit_buffer_fraction'] in [.005,.015] and q['lookback_days']==29 and q['return_hurdle']==.03","q['exit_buffer_fraction']==.005 and q['lookback_days']==29 and q['return_hurdle'] in [.025,.035]")])
edit('parent_units.py',[("H=F('.03')\nfor E in [F('.005'),F('.01'),F('.015')]:","E=F('.005')\nfor H in [F('.025'),F('.03'),F('.035')]:"),("g['W']==.01","g['W']==.03")])
edit('exports.py',[("ylabel='BTC exit retention buffer; L29/H3%/V14cap3%'","ylabel='BTC entry threshold; L29/exit0.5%/V14cap3%'"),("['0.5%','1.0%','1.5%']","['2.5%','3.0%','3.5%']"),('Preregistered BTC exit retention / ETH funding-budget ratio','Preregistered BTC entry with early exit / ETH funding-budget ratio')])
for n in ['observe_fewm.py','observe_candidate.py','review/setup.py']:edit(n,[('1758091','1789665')])
edit('forward.py',[("ROOT/'data/runs/automation/20261114T135434Z/forward_raw'","ROOT/'data/runs/automation'/ROUND.name/'forward_raw'")])
# Keep old committed immutable raw copies; recover colliding ignored paths into separate per-round archives.
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();recovery=[]
for tag in ['20261114T135434Z','20261114T155436Z']:
 old=ROOT/'research/experiments'/tag;idx=json.loads((old/'raw_evidence_index.json').read_text())
 for z in idx['artifacts']:
  if '/forward_raw/' not in z['original_path']:continue
  src=ROOT/z['committed_copy'];assert sha(src)==z['sha256'];dest=ROOT/'data/runs/automation'/tag/'forward_raw_recovered'/src.name;dest.parent.mkdir(parents=True,exist_ok=True)
  if dest.exists():assert sha(dest)==z['sha256']
  else:dest.write_bytes(src.read_bytes())
  recovery.append({**z,'source_round':tag,'current_ignored_original_path_sha256':sha(ROOT/z['original_path']),'original_ignored_path_matches_archived_round':sha(ROOT/z['original_path'])==z['sha256'],'unique_recovered_path':str(dest.relative_to(ROOT)),'recovered_sha256':sha(dest),'committed_public_copy_preserved':True})
(R/'legacy_raw_path_recovery.json').write_text(json.dumps({'passed':True,'rows':recovery,'old_public_reports_states_specs_and_raw_copies_unchanged':True,'old_ignored_shared_path_not_overwritten':True,'current_round_raw_path_dynamic_unique':True,'financial_or_account_recalculations':0,'description':'A legacy literal ignored forward_raw path was reused by155436 after135434. Original public raw copies remain exact and sufficient; immutable per-round ignored recovery copies preserve both versions without rewriting old reports or choosing one to overwrite the shared path.'},indent=2)+'\n')
f=R/'read_failures.json';d=json.loads(f.read_text());d['facts'].append({'action':'Prelaunch audit of inherited SMA raw storage path','error':'Legacy ignored path135434 reused by155436;135434 original ignored bytes differ from its retained immutable public copy','resolved':True,'resolution':'Verified both rounds committed raw SHA and copied each to unique recovered ignored path; changed current forward transport storage to dynamic current round path before binding/capture; no old public evidence,book orrule changed.','financial_or_account_recalculations':0});f.write_text(json.dumps(d,indent=2)+'\n')
# The actual16:00 public records are distinct from the preserved08 source.
p=R/'review/setup.py';s=p.read_text().replace("all(not xs for xs in fresh['public_fields_by_asset'].values())","all(len(xs)==1 and xs[0]['fundingTime']==1794672000000 for xs in fresh['public_fields_by_asset'].values())");s=s.replace("'current_window_empty_separate_from_original08_capture':True","'current_window_has_actual16_separate_from_original08_capture':True");s=s.replace("'fresh_current_window_fields_empty':True","'fresh_current_window_fields_empty':False").replace("{'SMA':0,'candidate':0,'l4h02':0,'fewm':0}","{'SMA':0,'candidate':0,'l4h02':6,'fewm':6}").replace('[0,0,0,0]','[0,0,6,6]')
s=s.replace("'2026-11-14T10:30:00Z','2026-11-14T12:30:00Z'","'2026-11-14T12:30:00Z','2026-11-14T14:30:00Z'").replace("'2026-11-14T12:10:00Z','2026-11-14T14:10:00Z'","'2026-11-14T14:10:00Z','2026-11-14T16:10:00Z'")
s=s.replace('currentclosedwindowsmarks/risk only,allcurrentfunding0.','currentL4/FEWMwindowsbookactual16onceonownq/cash;singlecut14:30hasnotreached16. Marks/risk,no daily/fills.').replace('fund0/0/0/0prior08preserved','fund0/0/6/6actual16andprior08preserved')
s=s.replace("ms=lambda t:","(R/'funding16_nov14_preflight.json').write_bytes((R/'window_funding_preflight.json').read_bytes());put(R/'funding16_prebinding_verification.json',{'passed':True,'source':rel(R/'funding16_nov14_preflight.json'),'sha256':sha(R/'funding16_nov14_preflight.json'),'original_capture_utc':fresh['recorded_utc'],'actual_funding_time_ms':1794672000000,'before_account_calculation':True})\nms=lambda t:")
s=s.replace("R/'funding08_nov14_preflight.json']","R/'funding08_nov14_preflight.json',R/'funding16_nov14_preflight.json']");ast.parse(s);p.write_text(s)
edit('checks.py',[("assert all(win[a]['expected_funding_by_asset']=={'BTC':[],'ETH':[]} for a in ['SMA','candidate','l4h02','fewm']) and not cashflows and all(not xs for xs in fresh['public_fields_by_asset'].values())","assert all(win[a]['expected_funding_by_asset']=={'BTC':[],'ETH':[]} for a in ['SMA','candidate']) and all(win[a]['expected_funding_by_asset']==fresh['public_fields_by_asset'] for a in ['l4h02','fewm']) and len(cashflows)==sum(win[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm'])==12"),('all4marks0currentfunds,no newdaily/fills;all3prior08once','L4FEWMactual16own6each,singlebefore16zero,no daily/fills;prior08once')])
edit('publish.py',[('test BTC exit buffers with reused ETH banks','test BTC entry thresholds with early exit and reused ETH banks')])
p=R/'finalize.py';s=p.read_text().replace("{'SMA':0,'candidate':0,'l4h02':0,'fewm':0}","{'SMA':0,'candidate':0,'l4h02':6,'fewm':6}").replace("['2026-11-14T12:30:00Z','2026-11-14T14:30:00Z']","['2026-11-14T14:30:00Z','2026-11-14T16:30:00Z']").replace("['2026-11-14T14:10:00Z','2026-11-14T16:10:00Z']","['2026-11-14T16:10:00Z','2026-11-14T18:10:00Z']").replace("'sensitivity_metric_boundaries.json']:assert","'sensitivity_metric_boundaries.json','legacy_raw_path_recovery.json','funding16_prebinding_verification.json']:assert");ast.parse(s);p.write_text(s)
previous=json.loads((ROOT/'.git/automation_proofs/20261114T155436Z.json').read_text());assert previous['status']=='completed_published_verified_unlocked';head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip()==head
(R/'startup.json').write_text(json.dumps({'round':R.name,'trigger_utc':'2026-11-14T17:55:37.737Z','base_commit':head,'branch_lock_broker_pid':1789665,'branch_lock_session':96005,'branch_lock_native_start_chunk':'3ffa8d','root_native_verification_chunk':'0a3cf5','initial_fetch_native_start_chunk':'477fd1','initial_fetch_native_completion_chunk':'b80542','initial_fetch_native_session':40201,'initial_sync_no_merge_required':True,'only_preexisting_untracked':'data/normalized','previous_round_publication_verified':previous['status'],'previous_commit':previous['commit']},indent=2)+'\n')
for p in R.rglob('*.py'):ast.parse(p.read_text())
print('PASS preparedH.025/.03/.035fixedE.005 xETHR;original accountactual16funding0/0/6/6;dynamic raw storage and immutable archive recovery beforebinding;0newcalculations')
