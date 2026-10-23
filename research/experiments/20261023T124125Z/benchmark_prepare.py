"""Before any financial calculation,reserve two exact-budget constant-long controls."""
import copy,json
from run import ROOT,R,reg,put,sha,rel,now,call

def main():
 assert not (R/'report.json').exists() and not (R/'evaluate.log').exists() and not (R/'benchmark_plan.json').exists();batch=json.loads((R/'batch.json').read_text());assert len(batch)==18
 plan={'frozen_at_utc':now(),'main_plan_sha256':sha(R/'plan.json'),'stage':'All18primarycandidatesreserved;no real financial calculation started.','purpose':'Two same330day/10000collateral/2000initialnotionalperpetualconstantlong controls,oneperasset;cashzeroyieldanalyticalbaseline.','primary_rules_and_parameters_changed':False,'candidate_configs':18,'additional_reference_configs':2,'total_financial_configs':20,'reference_qualification':'Actualresultsretainedasrejected/referenceonly;notalphaqualification.'};put(R/'benchmark_plan.json',plan);done=[]
 for asset in ['BTC','ETH']:
  src=next(x for x in batch if x['asset']==asset);spec=copy.deepcopy(json.loads((ROOT/src['spec']).read_text()));spec['name']='perp_hold_'+asset;spec['family']='perpetual-fixed-initial-notional-long-reference';spec['logic']['signal']='Constantlong+1fromdeclaredOOSstart,noROCselection;firstnext00:01buy,thenkeepactualquantitythroughend,costedterminalclose. Samefunding/collateral/cost/riskledger as candidates.';spec['parameters'].pop('lookback_days');spec['parameters'].pop('return_hurdle');spec['parameters']['signal_mode']='constant_long_reference';spec['validation_plan']=rel(R/'benchmark_plan.json');path=R/'specs'/(spec['name']+'.json');put(path,spec);row={'name':spec['name'],'spec':rel(path),'fingerprint':reg.fingerprint(spec),'asset':asset,'lookback_days':None,'return_hurdle':None,'capital_usdt':10000,'role':'benchmark'};done.append(call('reserve',row));batch.append(row);put(R/'benchmark_reserve.json',done)
 put(R/'batch.json',batch);print('RESERVED_TWO_BENCHMARKS_BEFORE_ANY_FINANCIAL_EVALUATION',sha(R/'benchmark_plan.json'),flush=True)

if __name__=='__main__':main()
