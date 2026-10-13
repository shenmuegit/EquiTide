import json
from pathlib import Path
R=Path(__file__).resolve().parent;d=json.loads((R/'report.json').read_text())
W,H=1050,475;s=['<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="475" viewBox="0 0 1050 475">','<rect width="100%" height="100%" fill="#101820"/>','<style>text{font-family:Arial,sans-serif;fill:#edf2f4}.title{font-size:23px;font-weight:bold}.head{font-size:18px;font-weight:bold}.small{font-size:13px}</style>','<text x="24" y="34" class="title">Quarter-hour event: 1× net return sensitivity (all cells near −100%)</text>']
for ai,a in enumerate(('BTC','ETH')):
 for ci,cap in enumerate((5000,10000)):
  x0=24+ai*520;y0=65+ci*190;s.append(f'<text x="{x0}" y="{y0}" class="head">{a} · ${cap:,}</text>')
  cw,ch=158,41
  for phase in (0,1,2):s.append(f'<text x="{x0+phase*cw+10}" y="{y0+18}" class="small">phase +{phase}m</text>')
  for hi,hold in enumerate((1,2,3)):
   for pi,phase in enumerate((0,1,2)):
    name=f'turn15_{a.lower()}_cap{cap}_phase{phase}_hold{hold}m';v=d['configs'][name]['scenarios']['1']['net_return_pct']
    x=x0+pi*cw;y=y0+28+hi*ch;fill='#7f1d26' if v < -99.95 else '#a32d34'
    s.append(f'<rect x="{x}" y="{y}" width="{cw-4}" height="{ch-4}" rx="3" fill="{fill}" stroke="#edf2f4"/>')
    s.append(f'<text x="{x+9}" y="{y+23}" class="small">{hold}m · {v:.3f}%</text>')
s.append('<text x="24" y="461" class="small">1× includes 10bp/side fee, spread/slippage estimates, square-root impact and exchange filters; 2×/3× values are in sensitivity.csv.</text>');s.append('</svg>')
(R/'sensitivity_surface.svg').write_text('\n'.join(s)+'\n')
