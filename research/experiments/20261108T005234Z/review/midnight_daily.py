"""Independently aggregate currentNov7 closedday from carriedpartial+realminutes."""
import gzip,json,sys
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put
rd=lambda p:json.loads(p.read_text());out=[];DAY=86400000000000;MS=1000000
for stem in ['l4h02','fewm']:
 w=R/(stem+'_observation');prev=rd(w/'previous_pointer.json');before=rd(ROOT/prev['state']);state=rd(w/'state.json');im=rd(w/'input_manifest.json');assert sha(ROOT/im['packet'])==im['sha256'];packet=json.loads(gzip.decompress((ROOT/im['packet']).read_bytes()));delta=json.loads(gzip.decompress((w/'delta.json.gz').read_bytes()));v=rd(R/(stem+'_verification.json'));assert v['passed'] and v['new_daily_events']==1 and v['new_exact_causal_decisions']==6 and v['new_funding_settlements']==6
 for a in ['BTC','ETH']:
  partial=before['context'][a]['partial'];end=(partial['day']+1)*DAY;bars=[z for z in packet['assets'][a]['minutes'] if before['cutoff_ns']<=int(z[0])*MS<end];complete=next(z for z in state['context'][a]['daily'] if z['day']==partial['day']);volume=D(partial['quote_volume'])+sum((D(z[7]) for z in bars),D(0));assert partial['count']+len(bars)==1440 and D(complete['quote_volume'])==volume and D(complete['close'])==D(bars[-1][4])
  ds=[x for x in delta['journal'] if x['kind']=='decision' and x['asset']==a];assert len(ds)==3 and all(D(x['prior_complete_close'])==D(complete['close']) for x in ds);assert all(x['timestamp_ns']>end for x in ds)
  out.append({'account':stem,'asset':a,'closed_day':partial['day'],'full_minute_count':1440,'carried_partial_minutes':partial['count'],'new_minutes':len(bars),'independent_full_quote_volume':str(volume),'independent_close':complete['close'],'state_daily_context_bars':len(state['context'][a]['daily']),'all3cost_decisions_use_completed_close':True,'actual_own_fills':v['new_fills']})
put(R/'current_midnight_daily_verification.json',{'passed':True,'raw_plus_carried_own_partial_independently_aggregated':True,'current_closed_day':'2026-11-07','daily_decision_utc':'2026-11-08T00:01:00Z','funding_utc':'2026-11-08T00:00:00Z','rows':out,'no_policy_or_account_rerun':True});print('PASS4ownclosedNov7days1440minutes/quotevolume/close;all12causaldailydecisionsusecorrectday')
