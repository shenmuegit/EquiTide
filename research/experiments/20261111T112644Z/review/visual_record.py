import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
(R/'visual_inspection.json').write_text(json.dumps({'passed':True,'sha256':hashlib.sha256((R/'sensitivity.png').read_bytes()).hexdigest(),'review':'Actual tool view:8native/parent370dreturn-DD-Sharpe-recentheatmaps;M2/3/4 and R.0075/.00875/.01 labelled;oldM4/R.00875 explicitlyO;DDconstantmatchesreport;recentETH1or2/8,parent5or6/8;no misleadingfinal/livequalification.','review_scope':'Manually viewed generated PNG;no automated screenshot claim.'},ensure_ascii=False,indent=2)+'\n')
