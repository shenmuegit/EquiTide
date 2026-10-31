"""Read complete repository context and prepare only this round's evidence."""
import gzip,hashlib,importlib.util,json,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip()==str(ROOT)
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main'
assert subprocess.check_output(['git','rev-parse','origin/main'],cwd=ROOT,text=True).strip()==head
prior=json.loads((ROOT/'research/experiments/20261031T094316Z/context.json').read_text())
events=reg.read_events(ROOT/'research/automation/registry.jsonl');records=reg.read_records(ROOT/'research/automation/registry.jsonl')
conclusions=[]
for p in sorted((ROOT/'research/experiments').glob('*/result.md')):
 if p.parent==R:continue
 text=p.read_text();conclusions.append({'path':rel(p),'bytes':p.stat().st_size,'sha256':sha(p),'paragraphs':len(text.split('\n\n')),'conclusion':text[:450]})
extra=[]
paths=[ROOT/'AGENTS.md',ROOT/'research/automation/task.md',ROOT/'research/automation/README.md',ROOT/'research/monitor/README.md',*[ROOT/f'.agents/skills/{s}/SKILL.md' for s in ['walk-forward-validation','ml4t-sensitivity-analysis','ml4t-transaction-costs']],*sorted((ROOT/'checks').glob('*oos.py')),*sorted((ROOT/'freqtrade_trial/results').glob('*.json'))]
for p in paths:
 content=p.read_text()
 if p.suffix=='.json':json.loads(content)
 extra.append({'path':rel(p),'bytes':p.stat().st_size,'sha256':sha(p)})
zpath=ROOT/'freqtrade_trial/results/backtest-result-2026-09-29_02-15-46.zip'
with zipfile.ZipFile(zpath) as z:
 zipped=[{'member':n,'sha256':hashlib.sha256(z.read(n)).hexdigest(),'bytes':len(z.read(n))} for n in z.namelist()]
for fp,e in prior['initial_16_actual_evidence'].items():
 rec=records[fp]
 if e.get('result_available'):
  assert rec['result_available'] is True and rec['report_sha256']==e['report_sha256'] and sha(ROOT/e['report'])==e['report_sha256']
 else:
  assert rec['status']=='legacy-tested'
  for ev in e['actual_original_evidence']:assert sha(ROOT/ev['path'])==ev['sha256']
assert len(prior['initial_16_actual_evidence'])==16
protected_paths=[ROOT/p for p in subprocess.check_output(['git','ls-files','research/paper10'],cwd=ROOT,text=True).splitlines()]
protected_paths += [ROOT/f'research/experiments/{s}/{f}' for s,fs in [('20261026T170839Z',['report.json','forward_report.json','forward_state.json','next_research_state.json','plan.json','run.py']),('20261025T125437Z',['report.json','plan.json','engine.py','verification.json']),('20261025T065405Z',['report.json','plan.json','engine.py']),('20261024T184829Z',['report.json','plan.json']),('20261024T164729Z',['report.json','plan.json','engine.py']),('20261024T144658Z',['report.json','plan.json']),('20261024T124528Z',['report.json','plan.json']),('20261024T104557Z',['report.json','plan.json']),('20261024T084457Z',['report.json','plan.json']),('20261001T113625Z',['forward_plan.json'])] for f in fs]
protected_paths += [ROOT/'research/experiments/20261026T070542Z'/p for p in ['plan_corrected.json','candidate_validation.json','invalid_spec_report.json','data_manifest.json']]
protected_paths += [ROOT/'research/experiments/20261026T090537Z'/p for p in ['candidate_prospective_plan.json','data_manifest.json','candidate_validation.json']]
protected_paths += list((ROOT/'research/experiments/20261026T110637Z').glob('prospective*'))+[ROOT/'research/experiments/20261026T110637Z/observer_checks.json',ROOT/'research/experiments/20261026T110637Z/candidate_validation.json']
protected_paths += [ROOT/'research/experiments/20261026T130738Z'/p for p in ['data_manifest.json','candidate_validation.json','verification.json','plan.json','entry_threshold_comparison.json']]
protected_paths += [ROOT/'research/experiments/20261026T150838Z'/p for p in ['data_manifest.json','candidate_validation.json','verification.json','plan.json','lookback_comparison.json']]
protected_paths += [ROOT/'research/experiments/20261026T170839Z'/p for p in ['data_manifest.json','candidate_validation.json','verification.json','plan.json','joint_interaction_comparison.json']]
protected_paths += [ROOT/p for p in prior['account_hashes_before']]
protected_paths += [p for p in (ROOT/'research/experiments/20261031T094316Z').rglob('*') if p.is_file()]
protected={rel(p):sha(p) for p in protected_paths if p.is_file()}
canonical={reg.fingerprint(x['spec']) for x in records.values() if 'spec' in x and not (x['spec'].get('family')=='paper-live-portfolio-observation' or x['spec'].get('name','').startswith('forward_snapshot_') or 'observation_terminal_action' in x['spec'].get('parameters',{}))}
ctx={'registry_events':len(events),'registry_ids':len(records),'canonical_research_definitions_excluding_observations':len(canonical),'canonical_count_policy':'same is_observation predicate as readonly monitor; exclude paper observation and forward snapshot/terminal-action specs; canonical exact fingerprints kept','main_registry_sha256_before_reserve':sha(ROOT/'research/automation/registry.jsonl'),'ledger_fragments_before':{rel(p):sha(p) for p in reg._ledger_paths(ROOT/'research/automation/registry.jsonl') if p.exists()},'initial_16_missing_actual_results':0,'initial_16_actual_evidence':prior['initial_16_actual_evidence'],'initial_16_evidence_resolution':prior['initial_16_evidence_resolution'],'initial_16_original_ZIP_members':zipped,'prior_conclusions_read':conclusions,'additional_full_reads':extra,'account_hashes_before':protected,'reserved_other_owners':[{'fingerprint':fp,'owner':r.get('spec',{}).get('parameters',{}).get('owner_automation_id'),'name':r.get('spec',{}).get('name')} for fp,r in records.items() if r['status']=='reserved']}
put(R/'context.json',ctx)

print(json.dumps({'base':head,'events_read':len(events),'IDs':len(records),'conclusions_read':len(conclusions),'additional_full_reads':len(extra),'protected_files':len(protected),'reserved_other_owners':ctx['reserved_other_owners']},ensure_ascii=False),flush=True)
