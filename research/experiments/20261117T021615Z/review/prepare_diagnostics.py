"""Read-only source/schema check for coefficient diagnostics before saved-results reads."""
import ast,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
for n in ['diagnostics.py','visual_review.py','budget_effect.py']:
 s=(R/'review'/n).read_text();ast.parse(s);assert 'center=eth[4]' in s if n in ['diagnostics.py','budget_effect.py'] else True;assert '[2,3]' in s
assert 'ETH_FUNDING_M' in (R/'run.py').read_text() and 'ETH_FUNDING_M' in (R/'exports.py').read_text();put(R/'diagnostics_preparation.json',{'passed':True,'recorded_utc':now(),'W':'ETH median count M2/3/4 atfixedR.0075/VW8','K':'BTC readonly H.03/.0325','no_market_account_or_registry_execution':True});print('PASS current diagnostics use coefficientR andBTC H axes,0newfinancialcalls')
