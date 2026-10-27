"""Reserve/finish original frozen daily-crossing continuation."""
import sys
from run import R,module
m=module(R/'forward.py','daily_resume_entry')
assert sys.argv[1] in ['reserve','finish']
getattr(m,sys.argv[1])()
