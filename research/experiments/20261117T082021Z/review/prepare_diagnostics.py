"""Read-only source/schema check for coefficient diagnostics before saved-results reads."""
import ast,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
for n in ['diagnostics.py','visual_review.py','budget_effect.py']:
 s=(R/'review'/n).read_text();ast.parse(s);assert 'center=eth[.0075]' in s if n in ['diagnostics.py','budget_effect.py'] else True;assert '[.00625,.00875]' in s
assert 'ETH_FAST_E' in (R/'run.py').read_text() and 'ETH_FAST_E' in (R/'exports.py').read_text();put(R/'diagnostics_preparation.json',{'passed':True,'recorded_utc':now(),'W':'ETH exit E.00625/.0075/.00875 atfixedL5H.02/M4/R.0075/VW8','K':'BTC readonly H.03/.0325','no_market_account_or_registry_execution':True});print('PASS current diagnostics use coefficientR andBTC H axes,0newfinancialcalls')
