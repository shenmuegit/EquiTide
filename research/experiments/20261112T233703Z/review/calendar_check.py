"""Calendar/source invariants only; no policy, trade, NAV or registry calculation."""
import json,sys
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
import market
p=json.loads((R/'plan.json').read_text());ms,cm=market.load(p);rows={}
for asset,m in ms.items():
 old=core.START+370;boundary=m['first_ns']+old*DAY+MIN;ix=np.flatnonzero(m['ts']==boundary);codes=m['codes'][ix].copy()
 if '--mutant-old-terminal' in sys.argv:codes[-1]=9
 assert 9 not in codes and 8 not in codes and all(x in codes for x in [1,5,6,7]),'Old Oct24 terminal must become a continuous ordinary daily decision'
 origin=330 if '--mutant-recent-origin' in sys.argv else 349
 assert m['daily_indices'][origin]==m['daily_indices'][-41],'Recent40 origin must move to day349 in389day calendar'
 assert len(m['ts'])==573000 and len(m['daily_indices'])==390 and len(m['funds'])==1167 and int(m['codes'][-1])==9 and (m['codes']==6).sum()==389
 rows[asset]={'events':len(m['ts']),'daily_boundaries':390,'actual_funding_settlements':1167,'old_boundary_event_codes':codes.tolist(),'recent40_origin_day':origin,'end_utc':core.stamp(m['end_ns'])}
put(R/'calendar_verification.json',{'passed':True,'rows':rows,'union_points':len(cm['keys']),'union_axis_sha256':cm['sha256'],'new_financial_or_account_calculations':0,'old_Oct24_terminal_removed_before_evaluation':True,'recent40_origin349_not330':True});print('PASS389calendar/source axes,1167funds each,Oct24daily decision not terminal,recent40day349;0finance')
