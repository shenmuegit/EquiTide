"""Read exact saved trade amounts as Decimal; do not execute a strategy or account."""
from pathlib import Path
from decimal import Decimal as D
from datetime import datetime,timezone
import json,gzip,hashlib
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=json.loads((R/'plan.json').read_text());binding=json.loads((R/'extra_trade_review_binding.json').read_text());assert sha(Path(__file__))==binding['source_sha256'];rpt=sha(R/'report.json')
a='282194186530e2e7093ae2a6e0cb4071b0270f48c2a118f734caa801846597de';b='41de4309229b892489a07574af07a73ae93229a35c118558ed60362285e90c89';arc={}
for fp in [a,b]:
 ref=p['read_only_references'][fp];assert sha(ROOT/ref['archive'])==ref['archive_sha256'];arc[fp]=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()))
key=lambda z:(z['trade_ts_ns'],z['opening'],z['terminal']);rows=[]
for k in ['1','2','3']:
 x,y=arc[a]['scenes'][k],arc[b]['scenes'][k];old={key(z):z for z in y['trades']};new={key(z):z for z in x['trades']};assert len(old)==len(y['trades']) and len(new)==len(x['trades'])
 extra=[z for z in x['trades'] if key(z) not in old];missing=[z for z in y['trades'] if key(z) not in new];assert len(extra)==2 and not missing and [z['opening'] for z in extra]==[True,False]
 gross=sum((D(z['reference_price_PnL_usdt']) for z in extra),D(0));allgross=sum((D(z['reference_price_PnL_usdt']) for z in x['trades']),D(0))-sum((D(z['reference_price_PnL_usdt']) for z in y['trades']),D(0));assert gross==allgross and gross<0
 assert abs(float(gross)-(x['summary']['gross_reference_price_PnL_usdt']-y['summary']['gross_reference_price_PnL_usdt']))<1e-9
 for z in x['trades']:
  if key(z) not in old:continue
  prev=old[key(z)];assert z['side']==prev['side'] and all(D(z[f])==D(prev[f]) for f in ['quantity','execution','reference','cost_usdt','reference_price_PnL_usdt'])
 rows.append({'cost':int(k),'extra_actual_trades':extra,'extra_reference_price_PnL_usdt':str(gross),'all_matched_execution_quantity_reference_cost_fields_identical':True})
assert sha(R/'report.json')==rpt
out={'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'saved_actual_source_ledgers_only':True,'new_financial_or_account_evaluations':0,'failed_native_attempt':'readonly_trade_review_failure.json','failure_recovery':'Exact trade monetary strings parsed with Decimal;stable real trade_ts_ns,opening,terminal keys;no parameters,ledgers,thresholds or model results changed.','source_archives':{f:{'path':p['read_only_references'][f]['archive'],'sha256':p['read_only_references'][f]['archive_sha256']} for f in [a,b]},'rows':rows,'financial_report_sha256_unchanged':rpt}
(R/'BTC_extra_roundtrip_review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':True,'extra_trades_per_cost':2,'extra_roundtrips_per_cost':1,'extra_gross_reference_PnL_usdt':[z['extra_reference_price_PnL_usdt'] for z in rows],'matched_fields_identical':True,'financial_or_account_runs':0}))
