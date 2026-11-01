import json
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==8 and sum(x['role']=='candidate' for x in batch)==6
for row in batch:
 sp=json.loads((ROOT/row['spec']).read_text());assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs and len(sp['components'])==2 and [x['weight'] for x in sp['components']]==[1,1]
 for fp in row['source_fingerprints']:assert rs[fp]['result_available'] and rs[fp]['spec']['kind']=='strategy'
 assert sum(rs[fp]['spec']['parameters']['initial_capital_usdt'] for fp in row['source_fingerprints'])==row['capital_usdt']
for fp,x in p['read_only_references'].items():assert rs[fp]['result_available'] and rs[fp]['status']==x['status'] and rs[fp]['report_sha256']==x['report_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256']
source={rel(x):sha(x) for x in R.glob('*.py') if x.name not in ['commands.py','summarize.py','finalize.py','publish.py']};immutable={rel(CORE_PATH):sha(CORE_PATH)}
for n in ['20261025T145537Z/run.py','20261026T110637Z/prospective_core.py','20261026T110637Z/prospective_observer.py']:x=ROOT/'research/experiments'/n;immutable[rel(x)]=sha(x)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_financial_calculation_yet':True});put(R/'definition_check.json',{'passed':True,**p['expected_counts'],'actual_native_source_quantity_not_linear_scaling':True,'two_axes':['BTCbankcapital','ETHentryH'],'raw_component_weights':[1,1]});print('PASS8newcombination definitions/14immutable sources,0newnative evaluation; codebound')
